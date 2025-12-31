import json
import os
from typing import Annotated, TypedDict, List, Dict, Any, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field

# --- Configuration ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
KNOWLEDGE_FILE = os.path.join(DATA_DIR, "knowledge.txt")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")
MODEL_NAME = "claude-3-5-sonnet-20241022"

# --- State Definition ---
class AgentState(TypedDict):
    messages: List[BaseMessage]
    context: str
    categories: List[str]
    is_rag_working: bool
    final_response: Dict[str, Any]

# --- RAG Setup ---
def setup_retriever():
    if not os.path.exists(KNOWLEDGE_FILE):
        print(f"Warning: {KNOWLEDGE_FILE} not found. RAG will not work.")
        return None

    with open(KNOWLEDGE_FILE, "r") as f:
        text = f.read()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(splits, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

retriever = setup_retriever()

# --- Load Categories ---
def load_categories():
    if not os.path.exists(CATEGORIES_FILE):
        return []
    with open(CATEGORIES_FILE, "r") as f:
        data = json.load(f)
        return data.get("categories", [])

categories_data = load_categories()
category_list_string = ", ".join([c["id"] for c in categories_data])

# --- Nodes ---

def retrieve_node(state: AgentState):
    query = state["messages"][-1].content
    if retriever:
        try:
            docs = retriever.invoke(query)
            context = "\n\n".join([d.page_content for d in docs])
            return {"context": context, "is_rag_working": True}
        except Exception as e:
            print(f"RAG Error: {e}")
            return {"context": "", "is_rag_working": False}
    else:
        return {"context": "", "is_rag_working": False}

def generate_node(state: AgentState):
    query = state["messages"][-1].content
    context = state["context"]
    is_rag_working = state["is_rag_working"]

    categories_context = ""
    if categories_data:
        categories_context = f"""
    To help with our internal classification of inquiries, we would like you to categorize inquiries in addition to answering them. We have provided you with {len(categories_data)} customer support categories.
    Check if your response fits into any category and include the category IDs in your "matched_categories" array.
    The available categories are: {category_list_string}
    If multiple categories match, include multiple category IDs. If no categories match, return an empty array.
        """

    system_prompt = f"""You are acting as an Anthropic customer support assistant chatbot.

    To help you answer the user's question, we have retrieved the following information for you. It may or may not be relevant:
    {context if is_rag_working else "No information found for this query."}

    Please provide responses that only use the information you have been given. If no information is available or if the information is not relevant for answering the question, you can redirect the user to a human agent.

    {categories_context}

    To display your responses correctly, you must format your entire response as a valid JSON object with the following structure:
    {{
        "thinking": "Brief explanation of your reasoning",
        "response": "Your concise response to the user",
        "user_mood": "positive|neutral|negative|curious|frustrated|confused",
        "suggested_questions": ["Question 1?", "Question 2?"],
        "debug": {{
            "context_used": true|false
        }},
        "matched_categories": ["category_id1", "category_id2"],
        "redirect_to_agent": {{
            "should_redirect": boolean,
            "reason": "Reason for redirection (optional)"
        }}
    }}
    """

    llm = ChatAnthropic(model=MODEL_NAME, temperature=0.3)

    # We enforce JSON output by pre-filling the assistant message
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query),
        AIMessage(content="{")
    ]

    response = llm.invoke(messages)

    # Reconstruct the full JSON
    full_json_str = "{" + response.content

    try:
        final_response = json.loads(full_json_str)
    except json.JSONDecodeError:
         # Fallback if the model didn't output valid JSON despite the pre-fill
        final_response = {
            "response": "Error processing response.",
            "thinking": "Failed to parse JSON",
            "redirect_to_agent": {"should_redirect": True, "reason": "JSON Error"}
        }

    return {"final_response": final_response}

# --- Graph Construction ---
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)

workflow.set_entry_point("retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

app = workflow.compile()

# --- Main Execution ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        user_query = sys.argv[1]
    else:
        user_query = "What models does Anthropic offer?"

    print(f"User Query: {user_query}")
    result = app.invoke({"messages": [HumanMessage(content=user_query)]})

    print("\n--- Final Response ---")
    print(json.dumps(result["final_response"], indent=2))
