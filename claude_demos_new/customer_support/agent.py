import json
import os
from typing import TypedDict, List, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langgraph.graph import StateGraph, END
from langchain_text_splitters import CharacterTextSplitter

# Load categories
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")
KNOWLEDGE_PATH = os.path.join(os.path.dirname(__file__), "knowledge.txt")

with open(CATEGORIES_PATH) as f:
    CATEGORIES = json.load(f)["categories"]
    CATEGORY_IDS = [c["id"] for c in CATEGORIES]

# Initialize RAG
_vectorstore = None

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        print("Initializing Knowledge Base (this may take a moment to download embeddings)...")
        if os.path.exists(KNOWLEDGE_PATH):
            with open(KNOWLEDGE_PATH) as f:
                text = f.read()
        else:
            text = "Anthropic is an AI safety company."

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.create_documents([text])

        # using a small model
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        _vectorstore = FAISS.from_documents(docs, embeddings)
        print("Knowledge Base Initialized.")
    return _vectorstore

class AgentState(TypedDict):
    query: str
    context: Optional[str]
    response: Optional[dict]

def retrieve(state: AgentState):
    query = state["query"]
    vs = get_vectorstore()
    # Search
    docs = vs.similarity_search(query, k=2)
    context = "\n\n".join([d.page_content for d in docs])
    return {"context": context}

def generate(state: AgentState):
    query = state["query"]
    context = state.get("context", "")

    categories_str = ", ".join(CATEGORY_IDS)

    system_prompt = f"""You are a customer support agent for Anthropic.
    Use the following context to answer the user's question.
    Context:
    {context}

    If the answer is not in the context, say so, but try to be helpful.

    Also, categorize the inquiry into one or more of these categories: {categories_str}.

    Return your response as a JSON object with these keys:
    - "thinking": your reasoning
    - "response": the answer to the user
    - "matched_categories": list of category IDs
    - "user_mood": guess the user's mood
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{query}")
    ])

    # Using Sonnet 3.5
    llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
    chain = prompt | llm | JsonOutputParser()

    try:
        response = chain.invoke({"query": query})
    except Exception as e:
        response = {
            "response": "I encountered an error processing your request.",
            "thinking": f"Error: {str(e)}",
            "matched_categories": [],
            "user_mood": "unknown"
        }

    return {"response": response}

def build_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("generate", generate)

    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()
