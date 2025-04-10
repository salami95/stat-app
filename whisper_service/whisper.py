from flask import Flask, request, jsonify
from openai import OpenAI
import os
import tempfile

app = Flask(__name__)
client = OpenAI()

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    if not audio_file:
        return jsonify({"error": "Invalid file"}), 400

    with tempfile.NamedTemporaryFile(delete=False) as temp:
        filepath = temp.name
        audio_file.save(filepath)

    try:
        with open(filepath, "rb") as file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=file,
                response_format="text"
            )
        return jsonify({"transcript": transcript.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        os.remove(filepath)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
