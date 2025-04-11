from flask import Flask, request, jsonify
import requests
import os
import tempfile
import redis
from rq import Queue

# Configure Redis connection
redis_url = os.getenv("REDIS_URL", "redis://redis.railway.internal:6379")
conn = redis.from_url(redis_url)
queue = Queue(connection=conn)

app = Flask(__name__)

WHISPER_URL = os.getenv("WHISPER_URL", "http://whisperservice-production.up.railway.app:80")
TOPIC_URL = os.getenv("TOPIC_URL", "http://topicservice-production.up.railway.app:80")
RAG_URL = os.getenv("RAG_URL", "http://ragservice-production.up.railway.app:80")
SCRIPTGEN_URL = os.getenv("SCRIPTGEN_URL", "http://scriptgenservice-production.up.railway.app:80")

@app.route("/start-job", methods=["GET", "POST"])
def start_job():
    if request.method == "GET":
        return jsonify({"status": "Job queue service is running."})

    data = request.get_json()
    filepath = data.get("filepath")

    if not filepath:
        return jsonify({"error": "Missing filepath"}), 400

    # Check if the filepath is a URL (starts with "http")
    if filepath.startswith("http"):
        try:
            # Download the file from the URL
            r = requests.get(filepath, stream=True)
            r.raise_for_status()
            # Save to a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            with open(temp_file.name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            filepath = temp_file.name
        except Exception as e:
            return jsonify({"error": f"Failed to download file: {str(e)}"}), 500
    else:
        # For backward compatibility: if a local filepath is given, check its existence
        if not os.path.exists(filepath):
            return jsonify({"error": "Local file not found."}), 400

    try:
        # Step 1: Transcription using Whisper
        with open(filepath, "rb") as f:
            whisper_response = requests.post(WHISPER_URL, files={"audio": f})
        transcript = whisper_response.json().get("transcript")
        if transcript is None:
            return jsonify({"error": "Whisper service did not return a valid transcript"}), 500

        # Step 2: Topic extraction + analysis
        topic_response = requests.post(TOPIC_URL, json={"transcript": transcript})
        topic_data = topic_response.json()
        topics = topic_data.get("topics")
        summary = topic_data.get("summary")
        if topics is None or summary is None:
            return jsonify({"error": "Topic service returned invalid data"}), 500

        # Step 3: Retrieve RAG facts
        rag_response = requests.post(RAG_URL, json={"topics": topics})
        rag_data = rag_response.json()

        # Step 4: Generate scripts for each topic
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
