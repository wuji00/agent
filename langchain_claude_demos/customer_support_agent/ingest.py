import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Define paths
DATA_PATH = "data.txt"
INDEX_PATH = "faiss_index"

def ingest_data():
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found.")
        return

    print("Loading data...")
    loader = TextLoader(DATA_PATH)
    documents = loader.load()

    print("Splitting text...")
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    print("Creating embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("Creating vector store...")
    db = FAISS.from_documents(docs, embeddings)

    print(f"Saving index to {INDEX_PATH}...")
    db.save_local(INDEX_PATH)
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_data()
