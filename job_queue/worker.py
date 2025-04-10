from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

WHISPER_URL = os.getenv("WHISPER_URL", "http://whisper_service:8000/transcribe")
TOPIC_URL = os.getenv("TOPIC_URL", "http://topic_service:8001/analyze")
RAG_URL = os.getenv("RAG_URL", "http://rag_service:8002/retrieve")
SCRIPTGEN_URL = os.getenv("SCRIPTGEN_URL", "http://scriptgen_service:8003/generate")

@app.route("/start-job", methods=["POST"])
def start_job():
    data = request.get_json()
    filepath = data.get("filepath")

    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "Missing or invalid filepath"}), 400

    try:
        # Step 1: Transcription
        with open(filepath, "rb") as f:
            whisper_response = requests.post(WHISPER_URL, files={"audio": f})
        transcript = whisper_response.json()["transcript"]

        # Step 2: Topic extraction + analysis
        topic_response = requests.post(TOPIC_URL, json={"transcript": transcript})
        topic_data = topic_response.json()
        topics = topic_data["topics"]
        summary = topic_data["summary"]

        # Step 3: Retrieve RAG facts
        rag_response = requests.post(RAG_URL, json={"topics": topics})
        rag_data = rag_response.json()

        # Step 4: Generate scripts
        scripts = {}
        for topic in topics:
            notes = [str(chunk) for chunk in rag_data.get(topic, [])]
            script_response = requests.post(SCRIPTGEN_URL, json={"topic": topic, "notes": notes})
            scripts[topic] = script_response.json().get("script", "[Error generating script]")

        return jsonify({
            "topics": topics,
            "summary": summary,
            "scripts": scripts
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004)
