import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Constants
DATA_DIR = "medrag_docs"
INDEX_DIR = "medrag_index"

def build_medrag_index():
    print("Building MedRAG index...")

    loader = TextLoader(os.path.join(DATA_DIR, "medrag.txt"))
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    os.makedirs(INDEX_DIR, exist_ok=True)
    db.save_local(INDEX_DIR)

    print("✓ MedRAG vectorstore built and saved to", INDEX_DIR)

if __name__ == "__main__":
    build_medrag_index()
