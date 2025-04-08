# topic_processor.py

import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# 1. Extract topics using LLM
def extract_topics(transcript: str, opportunities: str) -> list:
    prompt = ChatPromptTemplate.from_template("""
    You're a study assistant analyzing a student's study session.
    Given the transcript and analysis below, extract a list of discrete medical topics discussed.
    - Keep topics concise (e.g., 'psoriasis', 'types of skin cancer', 'histamine signaling')
    - Avoid duplications or overly broad groupings
    - Return one topic per line, no numbering

    Transcript:
    {transcript}

    Expert Analysis:
    {opportunities}

    Topics:
    """)

    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.2,
        api_key=os.getenv("OPENAI_API_KEY")  # ✅ Corrected usage
    )
    chain = prompt | llm
    response = chain.invoke({"transcript": transcript, "opportunities": opportunities})
    return [t.strip() for t in response.content.strip().splitlines() if t.strip()]

# 2. Load MedRAG index for RAG-based enrichment
def load_medrag_vectorstore(index_path="rag/medrag_index"):
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    return vectorstore

# 3. Retrieve RAG facts for each topic
def retrieve_facts_for_topics(topics, vectorstore, session_dir):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0.2,
        api_key=os.getenv("OPENAI_API_KEY")  # ✅ Corrected usage here too
    )
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

    facts_dir = os.path.join(session_dir, "topics")
    os.makedirs(facts_dir, exist_ok=True)

    for topic in topics:
        response = qa_chain.run(f"Provide accurate, concise educational content on: {topic}")
        path = os.path.join(facts_dir, f"{topic.replace(' ', '_')}_facts.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(response)

    return facts_dir

# 4. Orchestrate topic extraction + RAG enrichment
def process_topics(transcription_path, opportunities_path, session_dir):
    with open(transcription_path, "r", encoding="utf-8") as f:
        transcript = f.read()
    with open(opportunities_path, "r", encoding="utf-8") as f:
        opportunities = f.read()

    print("[INFO] Extracting topics...")
    topics = extract_topics(transcript, opportunities)

    topics_file = os.path.join(session_dir, "topics.txt")
    with open(topics_file, "w", encoding="utf-8") as f:
        f.write("\n".join(topics))
    print(f"[INFO] Topics extracted and saved to {topics_file}")

    print("[INFO] Loading MedRAG vectorstore...")
    vectorstore = load_medrag_vectorstore()

    print("[INFO] Retrieving facts for each topic...")
    facts_dir = retrieve_facts_for_topics(topics, vectorstore, session_dir)

    print(f"[INFO] Completed RAG enrichment. Facts saved in {facts_dir}")
    return topics_file, facts_dir
