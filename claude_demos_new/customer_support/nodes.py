import json
import os
from typing import List, Dict, Any
from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .state import AgentState

# Initialize LLM
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)

# Load Data Paths
DATA_DIR = Path(__file__).parent / "data"
CATEGORIES_FILE = DATA_DIR / "categories.json"
KNOWLEDGE_FILE = DATA_DIR / "knowledge.txt"

# Lazy load variables
_CATEGORIES = None
_RETRIEVER = None

def get_categories():
    global _CATEGORIES
    if _CATEGORIES is None:
        with open(CATEGORIES_FILE, "r") as f:
            _CATEGORIES = json.load(f)
    return _CATEGORIES

def get_retriever():
    global _RETRIEVER
    if _RETRIEVER is None:
        with open(KNOWLEDGE_FILE, "r") as f:
            text = f.read()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_text(text)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = FAISS.from_texts(texts, embeddings)
        _RETRIEVER = vectorstore.as_retriever()
    return _RETRIEVER

def categorize(state: AgentState) -> Dict[str, Any]:
    """Categorize the user's query."""
    messages = state["messages"]
    last_message = messages[-1].content

    categories = get_categories()
    categories_str = json.dumps(categories, indent=2)

    system_prompt = (
        "You are a customer support triage agent. "
        "Categorize the following user query into one of the following categories:\n"
        f"{categories_str}\n\n"
        "Return ONLY the category ID."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{query}")
    ])

    chain = prompt | llm | StrOutputParser()
    category_id = chain.invoke({"query": last_message}).strip()

    # Validate category
    valid_ids = [c["id"] for c in categories]
    if category_id not in valid_ids:
        # Fallback or default
        category_id = "general"

    return {"category": category_id}

def retrieve(state: AgentState) -> Dict[str, Any]:
    """Retrieve relevant documents based on the query."""
    messages = state["messages"]
    last_message = messages[-1].content

    retriever = get_retriever()
    docs = retriever.get_relevant_documents(last_message)
    context = "\n\n".join([doc.page_content for doc in docs])

    return {"context": context}

def generate(state: AgentState) -> Dict[str, Any]:
    """Generate a response using the category and context."""
    messages = state["messages"]
    last_message = messages[-1].content
    category = state["category"]
    context = state["context"]

    system_prompt = (
        "You are a helpful customer support agent for Acme Cloud Storage. "
        f"The user query falls under the category: {category}.\n"
        "Use the following context to answer the user's question. "
        "If the answer is not in the context, politely say you don't know and suggest contacting human support.\n\n"
        f"Context:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{query}")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"query": last_message})

    return {"answer": response}
