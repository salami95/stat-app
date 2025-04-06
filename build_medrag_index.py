import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Constants
DATA_DIR = "medrag_docs"
INDEX_FILE = "medrag_index.pkl"

# Load and index documents
def build_medrag_index():
    print("Building MedRAG index...")

    loader = TextLoader(os.path.join(DATA_DIR, "medrag.txt"))
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(docs, embeddings)

    with open(INDEX_FILE, "wb") as f:
        pickle.dump(db, f)

    print("Index built and saved to disk.")
    return db

# Querying
def query_medrag(query):
    if not os.path.exists(INDEX_FILE):
        raise FileNotFoundError("Index file not found. Please build the index first.")

    with open(INDEX_FILE, "rb") as f:
        db = pickle.load(f)

    result = db.similarity_search(query, k=3)
    return "\n\n".join(doc.page_content for doc in result)
