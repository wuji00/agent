import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = "./chroma_db"
KNOWLEDGE_BASE_PATH = "./customer_support/knowledge_base.txt"

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def initialize_rag():
    if os.path.exists(DB_DIR) and os.listdir(DB_DIR):
        # We assume it is populated
        return Chroma(persist_directory=DB_DIR, embedding_function=get_embeddings())

    print("Initializing ChromaDB...")
    # Check current path to adjust
    kb_path = KNOWLEDGE_BASE_PATH
    if not os.path.exists(kb_path):
        kb_path = "claude_quickstarts_langchain/customer_support/knowledge_base.txt"
        if not os.path.exists(kb_path):
            # Try relative to this file
            kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")

    if not os.path.exists(kb_path):
        raise FileNotFoundError(f"Could not find knowledge base at {KNOWLEDGE_BASE_PATH} or {kb_path}")

    loader = TextLoader(kb_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    db = Chroma.from_documents(docs, get_embeddings(), persist_directory=DB_DIR)
    return db

def retrieve_context(query: str, k: int = 3) -> str:
    db = initialize_rag()
    docs = db.similarity_search(query, k=k)
    return "\n\n".join([d.page_content for d in docs])
