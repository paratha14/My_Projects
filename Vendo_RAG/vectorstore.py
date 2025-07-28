from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from user_utils import supplier_to_text

def build_vectorstore(suppliers):
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    supplier_docs = [
        Document(page_content=supplier_to_text(s), metadata={"username": s["username"]})
        for s in suppliers
    ]
    print("Embedding and storing supplier info in vector store...")
    return FAISS.from_documents(supplier_docs, embedding)
