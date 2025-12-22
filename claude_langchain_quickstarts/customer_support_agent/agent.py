import os
import json
from typing import List, Dict, Any, TypedDict, Optional
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

# Try importing HuggingFaceEmbeddings
try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
    except ImportError:
        # Fallback to a mock embedding if necessary, or error out
        print("Warning: Could not import HuggingFaceEmbeddings. RAG might fail if not mocked.")
        HuggingFaceEmbeddings = None

# Load categories
try:
    with open("customer_support_categories.json", "r") as f:
        CATEGORIES = json.load(f)["categories"]
except FileNotFoundError:
    # Fallback if running from root
    with open("claude_langchain_quickstarts/customer_support_agent/customer_support_categories.json", "r") as f:
        CATEGORIES = json.load(f)["categories"]

CATEGORY_IDS = [c["id"] for c in CATEGORIES]

# --- RAG Setup ---
def setup_rag():
    if HuggingFaceEmbeddings is None:
        raise ImportError("HuggingFaceEmbeddings not available.")

    # Load data from data.txt
    data_path = "data.txt"
    if not os.path.exists(data_path):
        data_path = "claude_langchain_quickstarts/customer_support_agent/data.txt"

    if not os.path.exists(data_path):
        # Create dummy data if not exists
        with open(data_path, "w") as f:
            f.write("Anthropic offers Claude, a helpful AI assistant.\n")

    with open(data_path, "r") as f:
        text = f.read()

    # Simple chunking by line
    texts = [line.strip() for line in text.split("\n") if line.strip()]
    docs = [Document(page_content=t) for t in texts]

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

# Lazy init
_vectorstore = None
def get_retriever():
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = setup_rag()
    return _vectorstore.as_retriever(search_kwargs={"k": 3})

# --- Structured Output Schema ---
class RedirectToAgent(BaseModel):
    should_redirect: bool = Field(description="Whether to redirect to a human agent")
    reason: Optional[str] = Field(description="Reason for redirection if any")

class ResponseSchema(BaseModel):
    thinking: str = Field(description="Brief explanation of reasoning")
    response: str = Field(description="Concise response to the user")
    user_mood: str = Field(description="User mood: positive, neutral, negative, curious, frustrated, confused")
    suggested_questions: List[str] = Field(description="List of 3 suggested follow-up questions")
    debug: Dict[str, bool] = Field(description="Debug info, e.g. {'context_used': true}")
    matched_categories: List[str] = Field(description=f"Matched categories from: {', '.join(CATEGORY_IDS)}")
    redirect_to_agent: RedirectToAgent

# --- State ---
class AgentState(TypedDict):
    messages: List[BaseMessage]
    context: str
    final_response: dict

# --- Nodes ---

def retrieve_node(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1].content
    try:
        retriever = get_retriever()
        docs = retriever.invoke(last_message)
        context = "\n".join([d.page_content for d in docs])
    except Exception as e:
        print(f"RAG Error: {e}")
        context = "No context available due to error."
    return {"context": context}

def generate_node(state: AgentState):
    context = state["context"]
    messages = state["messages"]

    system_prompt = f"""You are acting as an Anthropic customer support assistant.
    Use the following context to answer the user's question:
    {context}

    If the context is not relevant, you can say so or redirect to a human.
    Categorize the inquiry into one of these: {', '.join(CATEGORY_IDS)}.
    """

    # We use a standard model for structured output
    llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0)
    structured_llm = llm.with_structured_output(ResponseSchema)

    # Prepend system message
    final_messages = [SystemMessage(content=system_prompt)] + messages

    response = structured_llm.invoke(final_messages)

    return {"final_response": response.dict()}

# --- Graph ---
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()

# --- Demo Run ---
if __name__ == "__main__":
    if "ANTHROPIC_API_KEY" not in os.environ:
        print("Please set ANTHROPIC_API_KEY env var.")
    else:
        print("Initializing RAG (this may take a moment)...")
        try:
            setup_rag()
            user_input = "How do I update my billing information?"
            print(f"User: {user_input}")

            result = app.invoke({"messages": [HumanMessage(content=user_input)]})
            print("\nAgent Response:")
            print(json.dumps(result["final_response"], indent=2))
        except Exception as e:
            print(f"Execution failed: {e}")
