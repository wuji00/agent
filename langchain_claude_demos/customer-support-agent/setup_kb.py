from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from uuid import uuid4

# Dummy knowledge base
texts = [
    "Anthropic is an AI safety and research company that's working to build reliable, interpretable, and steerable AI systems.",
    "Claude is a family of foundational AI models developed by Anthropic.",
    "Claude 3 Opus is our most intelligent model, capable of complex tasks.",
    "Claude 3 Sonnet is the best combination of skills and speed.",
    "Claude 3 Haiku is our fastest and most compact model.",
    "You can manage your account settings in the dashboard.",
    "We accept major credit cards for billing.",
    "Our API allows you to integrate Claude into your applications.",
    "Data privacy is a core value at Anthropic. We do not train on your data by default.",
    "If you have technical issues, please check our status page or contact support.",
]

def setup_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    documents = [Document(page_content=t) for t in texts]
    uuids = [str(uuid4()) for _ in range(len(documents))]
    vector_store = FAISS.from_documents(documents=documents, embedding=embeddings, ids=uuids)
    return vector_store

if __name__ == "__main__":
    vs = setup_vector_store()
    vs.save_local("faiss_index")
    print("Vector store created and saved to faiss_index")
