
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Dummy data for the knowledge base
# Mimicking a tech product knowledge base
documents = [
    Document(page_content="The ACME Phone X100 has a 6.5 inch OLED display and 4500mAh battery.", metadata={"source": "product_specs"}),
    Document(page_content="To reset the ACME Phone X100, hold the power button and volume down for 10 seconds.", metadata={"source": "troubleshooting"}),
    Document(page_content="The warranty for ACME products is 2 years for defects and 1 year for battery.", metadata={"source": "warranty"}),
    Document(page_content="CloudSync allows you to back up photos and contacts automatically on ACME devices.", metadata={"source": "features"}),
    Document(page_content="Error 505 means the device is overheating. Turn it off and let it cool down.", metadata={"source": "troubleshooting"}),
]

print("Creating vector store...")
vectorstore = FAISS.from_documents(documents, embeddings)

# Save the index locally
save_path = os.path.join(os.path.dirname(__file__), "faiss_index")
vectorstore.save_local(save_path)
print(f"Vector store saved to {save_path}")
