import os
import shutil
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
from orchestrator import process_audio_session
from dotenv import load_dotenv

from whisper import transcribe_audio  # ✅ NEW: Whisper-based transcription

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default_secret_key")
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return "No audio file uploaded", 400

    file = request.files["audio"]
    if file.filename == "":
        return "No selected file", 400

    filename = secure_filename(file.filename)
    session_id = os.path.splitext(filename)[0].replace(" ", "_")
    session_dir = os.path.join(app.config["UPLOAD_FOLDER"], session_id)
    os.makedirs(session_dir, exist_ok=True)

    filepath = os.path.join(session_dir, filename)
    file.save(filepath)
    print(f"[Flask] Audio uploaded to: {filepath}")

    # ✅ Whisper transcription
    transcript = transcribe_audio(filepath)
    if not transcript:
        return "Transcription failed", 500

    session["session_id"] = session_id
    session["session_dir"] = session_dir
    session["transcript"] = transcript

    return redirect(url_for("processing"))


@app.route("/processing")
def processing():
    transcript = session.get("transcript", "")
    session_id = session.get("session_id", "")
    session_dir = session.get("session_dir", "")

    if not transcript or not session_dir:
        return "Missing session data", 400

    try:
        results = process_audio_session(session_id, session_dir, transcript)
        session.update(results)
        print("[Flask] Session processing completed.")
    except Exception as e:
        print(f"[Flask] Error in processing: {e}")
        return "Processing failed", 500

    return redirect(url_for("results"))


@app.route("/results")
def results():
    return render_template("results.html", session=session)


if __name__ == "__main__":
    app.run(debug=True)
