import json
import os
from typing import TypedDict, List, Annotated
from typing_extensions import Literal

from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_text_splitters import CharacterTextSplitter
from langgraph.graph import StateGraph, END, START

# --- Configuration ---
MODEL_NAME = "claude-3-5-sonnet-20241022"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
KNOWLEDGE_FILE = os.path.join(os.path.dirname(__file__), "knowledge.txt")
CATEGORIES_FILE = os.path.join(os.path.dirname(__file__), "categories.json")

# --- State ---
class AgentState(TypedDict):
    query: str
    category: str
    context: str
    response: str

# --- Initialization ---

def load_knowledge_base():
    """Loads knowledge.txt into a FAISS vector store."""
    if not os.path.exists(KNOWLEDGE_FILE):
         # Fallback for demo if file doesn't exist
        text = "Claude is an AI assistant created by Anthropic."
    else:
        with open(KNOWLEDGE_FILE, "r") as f:
            text = f.read()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.create_documents([text])

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = FAISS.from_documents(docs, embeddings)
    return db

def load_categories():
    """Loads categories from JSON."""
    if not os.path.exists(CATEGORIES_FILE):
        return []
    with open(CATEGORIES_FILE, "r") as f:
        return json.load(f)

# Initialize global resources (lazy loading in a real app might be better, but acceptable for demo)
# We wrap them in functions or lazy load to avoid issues during import if env vars aren't set yet.
_vector_store = None
_categories = None

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        _vector_store = load_knowledge_base()
    return _vector_store

def get_categories():
    global _categories
    if _categories is None:
        _categories = load_categories()
    return _categories

# --- Nodes ---

def categorize(state: AgentState):
    """Categorizes the user query."""
    query = state["query"]
    categories = get_categories()

    cat_names = [c["name"] for c in categories]
    cat_desc = "\n".join([f"- {c['name']}: {c['description']}" for c in categories])

    llm = ChatAnthropic(model=MODEL_NAME, temperature=0)

    prompt = ChatPromptTemplate.from_template(
        "Categorize the following query into one of these categories:\n"
        "{cat_desc}\n\n"
        "Query: {query}\n\n"
        "Return ONLY the category name."
    )

    chain = prompt | llm
    response = chain.invoke({"cat_desc": cat_desc, "query": query})

    # Ensure content is extracted properly
    category = ""
    if isinstance(response, str):
        category = response.strip()
    elif hasattr(response, "content"):
        # If content is a mock, we might need to convert it to string
        category = str(response.content).strip()
    else:
        category = str(response).strip()

    # Clean up any potential mock artifact string representation if it happened to be a string like "<MagicMock...>"
    # which shouldn't happen if we test correctly, but let's be safe.

    print(f"DEBUG: LLM returned category: '{category}'")

    # Fallback if LLM hallucinates a category
    if category not in cat_names:
        print("DEBUG: Category mismatch, using fallback.")
        category = "General Inquiry"

    return {"category": category}

def retrieve(state: AgentState):
    """Retrieves relevant documents based on query."""
    query = state["query"]
    db = get_vector_store()

    # Simple retrieval
    docs = db.similarity_search(query, k=2)
    context = "\n\n".join([d.page_content for d in docs])

    return {"context": context}

def generate(state: AgentState):
    """Generates a response using the category and context."""
    query = state["query"]
    category = state["category"]
    context = state["context"]

    llm = ChatAnthropic(model=MODEL_NAME, temperature=0)

    prompt = ChatPromptTemplate.from_template(
        "You are a customer support agent specialized in {category}.\n"
        "Use the following context to answer the user's question.\n"
        "If the answer is not in the context, politely say you don't know.\n\n"
        "Context:\n{context}\n\n"
        "Question: {query}\n\n"
        "Answer:"
    )

    chain = prompt | llm
    response = chain.invoke({"category": category, "context": context, "query": query})

    content = ""
    if isinstance(response, str):
        content = response
    elif hasattr(response, "content"):
        content = str(response.content)
    else:
        content = str(response)

    return {"response": content}

# --- Graph ---

def create_customer_support_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("categorize", categorize)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)

    workflow.add_edge(START, "categorize")
    workflow.add_edge("categorize", "retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()

# --- Entry Point ---
if __name__ == "__main__":
    # Test run
    import sys

    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "How much does the API cost?"

    print(f"Processing query: {user_query}")
    graph = create_customer_support_graph()
    result = graph.invoke({"query": user_query})

    print("\n--- Result ---")
    print(f"Category: {result['category']}")
    print(f"Context retrieved: {len(result['context'])} chars")
    print(f"Response: {result['response']}")
