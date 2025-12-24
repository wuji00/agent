import json
from typing import TypedDict, List, Optional, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel, Field

# Load categories (mocking the file read or putting it inline)
CATEGORIES = [
    "account", "billing", "feature", "internal", "legal", "other", "technical", "usage"
]

# 1. State Definition
class AgentState(TypedDict):
    messages: List[BaseMessage]
    retrieved_context: str
    analysis: dict

# 2. Setup Vector Store (Load)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# 3. Define Output Model (Pydantic)
class RedirectToAgent(BaseModel):
    should_redirect: bool
    reason: Optional[str] = None

class DebugInfo(BaseModel):
    context_used: bool

class ResponseSchema(BaseModel):
    thinking: str = Field(description="Brief explanation of reasoning")
    response: str = Field(description="Concise response to the user")
    user_mood: str = Field(description="positive|neutral|negative|curious|frustrated|confused")
    suggested_questions: List[str]
    debug: DebugInfo
    matched_categories: Optional[List[str]] = Field(description="List of category IDs")
    redirect_to_agent: Optional[RedirectToAgent]

# 4. Nodes

def retrieve(state: AgentState):
    """Retrieves context based on the last message."""
    last_message = state["messages"][-1].content
    docs = vector_store.similarity_search(last_message, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    return {"retrieved_context": context}

def analyze(state: AgentState):
    """Calls Claude to analyze the query and context."""
    context = state.get("retrieved_context", "")
    messages = state["messages"]

    # We construct the system prompt dynamically
    system_prompt = f"""You are acting as an Anthropic customer support assistant chatbot.

    Context retrieved:
    {context if context else "No information found."}

    Available Categories: {", ".join(CATEGORIES)}

    Answer the user's question using the context. If unrelated, redirect to human agent.
    Identify user mood, suggested questions, and categories.
    """

    model = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
    structured_llm = model.with_structured_output(ResponseSchema)

    # LangChain handles the messages + system prompt
    # Note: with_structured_output usually handles the schema enforcement.
    # We pass the conversation history + system prompt.

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{messages}")
    ])

    chain = prompt | structured_llm
    response = chain.invoke({"messages": messages})

    return {"analysis": response.dict()}

# 5. Graph Construction
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve)
workflow.add_node("analyze", analyze)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "analyze")
workflow.add_edge("analyze", END)

app = workflow.compile()

# 6. Runnable function
def run_agent(user_query: str):
    print(f"User: {user_query}")
    initial_state = {"messages": [HumanMessage(content=user_query)]}
    result = app.invoke(initial_state)
    print("Agent Response:", json.dumps(result["analysis"], indent=2))
    return result["analysis"]

if __name__ == "__main__":
    # Test cases
    run_agent("How do I manage my billing?")
    run_agent("What is Claude 3 Opus?")
    run_agent("I am very angry about the downtime!")
