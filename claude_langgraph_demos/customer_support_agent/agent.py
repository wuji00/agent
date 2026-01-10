import os
import json
from typing import Annotated, TypedDict, List, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

# --- State Definition ---

class RedirectToAgent(BaseModel):
    should_redirect: bool
    reason: Optional[str] = None

class AgentResponse(BaseModel):
    thinking: str
    response: str
    user_mood: str = Field(..., description="positive|neutral|negative|curious|frustrated|confused")
    suggested_questions: List[str]
    debug: dict
    matched_categories: Optional[List[str]] = None
    redirect_to_agent: Optional[RedirectToAgent] = None

class AgentState(TypedDict):
    messages: List[BaseMessage]
    context: str
    final_response: Optional[AgentResponse]

# --- Categories ---
CATEGORIES = [
    {"id": "account", "name": "Account"},
    {"id": "billing", "name": "Billing"},
    {"id": "feature", "name": "Feature"},
    {"id": "internal", "name": "Internal"},
    {"id": "legal", "name": "Legal"},
    {"id": "other", "name": "Other"},
    {"id": "technical", "name": "Technical"},
    {"id": "usage", "name": "Usage"}
]

# --- Nodes ---

def retrieve(state: AgentState):
    """Retrieves context from FAISS."""
    query = state["messages"][-1].content

    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = db.similarity_search(query, k=1)
        context = "\n\n".join([doc.page_content for doc in docs])
        print(f"DEBUG: Retrieved context: {context[:50]}...")
    except Exception as e:
        print(f"DEBUG: Error retrieving context: {e}")
        context = ""

    return {"context": context}

def generate_response(state: AgentState):
    """Generates the response using Claude."""
    messages = state["messages"]
    context = state["context"]

    # Check if we have context
    is_rag_working = bool(context)

    category_list_string = ", ".join([c["id"] for c in CATEGORIES])

    system_prompt = f"""You are acting as an Anthropic customer support assistant chatbot inside a chat window on a website. You are chatting with a human user who is asking for help about Anthropic's products and services. When responding to the user, aim to provide concise and helpful responses while maintaining a polite and professional tone.

  To help you answer the user's question, we have retrieved the following information for you. It may or may not be relevant (we are using a RAG pipeline to retrieve this information):
  {context if is_rag_working else "No information found for this query."}

  Please provide responses that only use the information you have been given. If no information is available or if the information is not relevant for answering the question, you can redirect the user to a human agent for further assistance.

  To help with our internal classification of inquiries, we would like you to categorize inquiries in addition to answering them. We have provided you with {len(CATEGORIES)} customer support categories.
  Check if your response fits into any category and include the category IDs in your "matched_categories" array.
  The available categories are: {category_list_string}
  If multiple categories match, include multiple category IDs. If no categories match, return an empty array.

  If the question is unrelated to Anthropic's products and services, you should redirect the user to a human agent.

  You are the first point of contact for the user and should try to resolve their issue or provide relevant information. If you are unable to help the user or if the user explicitly asks to talk to a human, you can redirect them to a human agent for further assistance.
  """

    # We use with_structured_output to enforce the JSON schema
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.3)
    structured_llm = llm.with_structured_output(AgentResponse)

    # We need to construct the prompt with system message
    # LangChain ChatAnthropic handles system parameter, but with_structured_output might behave differently regarding system prompts depending on implementation.
    # It is safer to pass SystemMessage + Messages

    from langchain_core.messages import SystemMessage

    prompt_messages = [SystemMessage(content=system_prompt)] + messages

    response = structured_llm.invoke(prompt_messages)

    # Inject debug info about context used (approximated)
    if response.debug is None:
         response.debug = {}
    response.debug["context_used"] = is_rag_working

    return {"final_response": response}

# --- Graph Construction ---

workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate_response)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()

if __name__ == "__main__":
    # Test the agent
    import sys
    from langchain_core.runnables import RunnableLambda

    # Fake LLM for testing
    class FakeLLM:
        def with_structured_output(self, schema):
            return RunnableLambda(lambda x: AgentResponse(
                thinking="I should help the user.",
                response="To reset your password, please go to settings.",
                user_mood="neutral",
                suggested_questions=["How do I log in?"],
                debug={},
                matched_categories=["account"],
                redirect_to_agent=None
            ))

    # Mock ChatAnthropic for test mode
    if os.environ.get("TEST_MODE"):
        print("Running in TEST MODE")
        # Monkey patch ChatAnthropic
        global ChatAnthropic
        ChatAnthropic = lambda **kwargs: FakeLLM()

    # Basic interactive loop
    print("Customer Support Agent (Type 'quit' to exit)")
    messages = []

    # Non-interactive mode handling
    import select
    if select.select([sys.stdin,],[],[],0.0)[0]:
        # Input available
        try:
            while True:
                line = sys.stdin.readline()
                if not line:
                    break
                user_input = line.strip()
                if not user_input or user_input.lower() in ["quit", "exit"]:
                    break

                print(f"User: {user_input}")
                messages.append(HumanMessage(content=user_input))

                state = {"messages": messages, "context": "", "final_response": None}
                result = app.invoke(state)

                final_resp = result["final_response"]
                print(f"Assistant: {final_resp.response}")
                print(f"Thinking: {final_resp.thinking}")
                print(f"Mood: {final_resp.user_mood}")
        except Exception as e:
            print(f"Error: {e}")

    else:
        # Interactive mode
        while True:
            try:
                user_input = input("User: ")
            except EOFError:
                break
            if user_input.lower() in ["quit", "exit"]:
                break

            messages.append(HumanMessage(content=user_input))

            state = {"messages": messages, "context": "", "final_response": None}
            result = app.invoke(state)

            final_resp = result["final_response"]
            print(f"Assistant: {final_resp.response}")
            print(f"Thinking: {final_resp.thinking}")
            print(f"Mood: {final_resp.user_mood}")
            if final_resp.matched_categories:
                print(f"Categories: {final_resp.matched_categories}")
            if final_resp.redirect_to_agent and final_resp.redirect_to_agent.should_redirect:
                print(f"REDIRECT: {final_resp.redirect_to_agent.reason}")

            messages.append(AIMessage(content=final_resp.response))
