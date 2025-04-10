from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
import os

app = Flask(__name__)
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Prompt for topic extraction
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

extract_chain = extract_prompt | llm | (lambda output: [x.strip("- ") for x in output.content.split("\n") if x.strip()])

# Prompt for student performance analysis
analyze_prompt = PromptTemplate.from_template(
    """
    You are an education expert. Analyze this transcript for the learner's performance
    across the topics provided. Identify strengths, weaknesses, knowledge gaps,
    and opportunities for improvement in a detailed but concise summary.

    Transcript:
    ---
    {transcript}
    ---

    Topics:
    - {topics}

    Summary:
    """
)

analyze_chain = analyze_prompt | llm | (lambda output: output.content.strip())

def load_medrag_vectorstore():
    persist_dir = os.path.join(os.path.dirname(__file__), "../rag/medrag_index")
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    index = load_index_from_storage(storage_context)
    return index

def retrieve_facts_for_topics(topics):
    index = load_medrag_vectorstore()
    retriever = index.as_retriever(similarity_top_k=5)
    return {topic: retriever.retrieve(topic) for topic in topics}

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    transcript = data.get("transcript")
    if not transcript:
        return jsonify({"error": "Transcript is required"}), 400

    try:
        topics = extract_chain.invoke({"transcript": transcript})
        summary = analyze_chain.invoke({"transcript": transcript, "topics": ", ".join(topics)})
        return jsonify({"topics": topics, "summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
