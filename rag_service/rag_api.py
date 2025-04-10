from flask import Flask, request, jsonify
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
import os

app = Flask(__name__)

# URL for external communication (if needed)
WHISPER_URL = os.getenv("WHISPER_URL", "http://whisperservice-production.up.railway.app:80")
TOPIC_URL = os.getenv("TOPIC_URL", "http://topicservice-production.up.railway.app:80")
RAG_URL = os.getenv("RAG_URL", "http://ragservice-production.up.railway.app:80")
SCRIPTGEN_URL = os.getenv("SCRIPTGEN_URL", "http://scriptgenservice-production.up.railway.app:80")

def load_medrag_vectorstore():
    persist_dir = os.path.join(os.path.dirname(__file__), "../rag/medrag_index")
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    return load_index_from_storage(storage_context)

@app.route("/retrieve", methods=["POST"])
def retrieve():
    data = request.get_json()
    topics = data.get("topics", [])

    if not topics or not isinstance(topics, list):
        return jsonify({"error": "Invalid or missing topics list"}), 400

    try:
        index = load_medrag_vectorstore()
        retriever = index.as_retriever(similarity_top_k=5)
        results = {topic: [str(chunk) for chunk in retriever.retrieve(topic)] for topic in topics}
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002)
