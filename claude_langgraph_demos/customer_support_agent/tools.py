from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    try:
        vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except RuntimeError:
        # Fallback if not run from the correct directory
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        index_path = os.path.join(current_dir, "faiss_index")
        vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    return vectorstore.as_retriever()
