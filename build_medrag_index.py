import os
from datasets import load_dataset
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document

OUTPUT_DIR = "rag/medrag_index"

def load_pubmed_dataset():
    print("[INFO] Loading MedRAG PubMed dataset...")
    dataset = load_dataset("MedRAG/pubmed", split="train[:2000]")  # Limit for speed, remove slice for full set
    return dataset

def chunk_documents(texts):
    print(f"[INFO] Chunking {len(texts)} entries...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    docs = [Document(page_content=text) for text in texts]
    return splitter.split_documents(docs)

def build_and_save_index(docs, output_dir):
    print(f"[INFO] Creating FAISS vector store with {len(docs)} chunks...")
    os.makedirs(output_dir, exist_ok=True)
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(output_dir)
    print(f"[INFO] Vector index saved to {output_dir}")

def main():
    dataset = load_pubmed_dataset()
    texts = [entry["text"] for entry in dataset]
    docs = chunk_documents(texts)
    build_and_save_index(docs, OUTPUT_DIR)

if __name__ == "__main__":
    main()
