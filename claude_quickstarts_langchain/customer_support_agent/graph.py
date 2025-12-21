import os
import json
import logging
from typing import Annotated, TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# --- Setup RAG ---
def setup_retriever():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "knowledge_base.txt")

    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    # Use a small, local embedding model
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    db = FAISS.from_documents(docs, embeddings)
    return db.as_retriever()

# Initialize retriever lazily or globally
try:
    retriever = setup_retriever()
except Exception as e:
    print(f"Failed to initialize retriever: {e}")
    retriever = None

# --- Load Categories ---
def load_categories():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "customer_support_categories.json")
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            return data["categories"]
    except Exception as e:
        print(f"Failed to load categories: {e}")
        return []

CATEGORIES = load_categories()
CATEGORY_LIST_STRING = ", ".join([c["id"] for c in CATEGORIES])

# --- State Definition ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    retrieved_context: Optional[str]
    analysis: Optional[Dict[str, Any]]

# --- Nodes ---

def retrieve_node(state: AgentState):
    """Retrieves relevant context from the knowledge base."""
    # With add_messages, state["messages"] is a list of messages.
    latest_message = state["messages"][-1].content

    if retriever:
        docs = retriever.invoke(latest_message)
        context = "\n\n".join([doc.page_content for doc in docs])
    else:
        context = "No knowledge base available."

    return {"retrieved_context": context}

def generate_node(state: AgentState):
    """Generates the response using Claude and the retrieved context."""

    context = state.get("retrieved_context", "")
    messages = state["messages"]

    # System prompt adapted from the reference
    system_prompt = f"""You are acting as an Anthropic customer support assistant chatbot.

    To help you answer the user's question, we have retrieved the following information:
    {context}

    The available categories are: {CATEGORY_LIST_STRING}

    You must format your entire response as a valid JSON object with the following structure:
    {{
      "thinking": "Brief explanation of your reasoning",
      "response": "Your concise response to the user",
      "user_mood": "positive|neutral|negative|curious|frustrated|confused",
      "suggested_questions": ["Question 1?", "Question 2?"],
      "debug": {{ "context_used": true|false }},
      "matched_categories": ["category_id"],
      "redirect_to_agent": {{
        "should_redirect": boolean,
        "reason": "Reason if true"
      }}
    }}

    If the question is unrelated to Anthropic's products and services, redirect to a human agent.
    Ensure the JSON is valid. Do not include any markdown formatting like ```json ... ```. Just the raw JSON string.
    """

    # Prepare messages for Claude
    prompt_messages = [SystemMessage(content=system_prompt)] + messages

    llm = ChatAnthropic(model="claude-3-haiku-20240307", temperature=0.3)

    response = llm.invoke(prompt_messages)
    content = response.content

    # Clean up response if it contains markdown code blocks
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].strip()

    try:
        analysis = json.loads(content)
        final_response_text = analysis["response"]
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {content}")
        analysis = {
            "thinking": "Failed to parse response",
            "response": content,
            "user_mood": "neutral",
            "suggested_questions": [],
            "debug": {"context_used": False},
            "matched_categories": [],
            "redirect_to_agent": {"should_redirect": False}
        }
        final_response_text = content

    return {
        "messages": [AIMessage(content=final_response_text)],
        "analysis": analysis
    }

# --- Graph Construction ---
workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()
