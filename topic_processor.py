from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from llama_index.vector_stores.faiss import FAISSVectorStore
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
import os, tempfile

# Topic extraction
extract_prompt = PromptTemplate.from_template(
    """
    Extract a concise list of topics discussed in this transcript. Avoid redundancy.

    Transcript:
    ---
    {transcript}
    ---

    Topics:
    """
)

llm = ChatOpenAI(model="gpt-4", temperature=0)

extract_chain = extract_prompt | llm | (lambda output: [x.strip("- ") for x in output.content.split("\n") if x.strip()])

def load_medrag_vectorstore():
    persist_dir = os.path.join(os.path.dirname(__file__), "medrag_index")
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    return index

def retrieve_facts_for_topics(topics):
    index = load_medrag_vectorstore()
    retriever = index.as_retriever(similarity_top_k=5)
    return {topic: retriever.retrieve(topic) for topic in topics}

def process_topics(transcript):
    topics = extract_chain.invoke({"transcript": transcript})
    facts = retrieve_facts_for_topics(topics)
    return topics, facts
