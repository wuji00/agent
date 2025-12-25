import os
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

def setup_knowledge_base():
    # Load the dummy knowledge base
    loader = TextLoader("dummy_kb.txt")
    documents = loader.load()

    # Split text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Initialize Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create Vector Store
    db = FAISS.from_documents(texts, embeddings)

    # Save locally
    db.save_local("faiss_index")
    print("Knowledge base created and saved to 'faiss_index'")

if __name__ == "__main__":
    setup_knowledge_base()
