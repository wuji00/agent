import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

class RAGSystem:
    def __init__(self, knowledge_file: str):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = self._initialize_vector_store(knowledge_file)

    def _initialize_vector_store(self, knowledge_file: str):
        if not os.path.exists(knowledge_file):
            print(f"Warning: Knowledge file {knowledge_file} not found. RAG will be empty.")
            # Initialize empty FAISS
            return FAISS.from_texts([""], self.embeddings)

        loader = TextLoader(knowledge_file)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)

        return FAISS.from_documents(docs, self.embeddings)

    def retrieve(self, query: str, k: int = 3) -> str:
        docs = self.vector_store.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in docs])
