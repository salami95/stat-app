import os
from flask import Flask, request, redirect, render_template, session, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import uuid

# Import pipeline modules
from orchestrator import orchestrate_initial_phase
from topic_processor import process_topics
from podcast_script_generator import generate_all_scripts
from generate_audio import generate_all_audio

# === INIT APP ===
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET", "dev-key")  # Replace in production
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# === ROUTES ===

@app.route("/", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@app.route("/upload", methods=["POST"])
def upload():
    # 1. Save audio file
    audio = request.files["audio"]
    if not audio:
        return "No audio file uploaded", 400

    filename = secure_filename(audio.filename)
    uid = str(uuid.uuid4())[:8]
    audio_path = os.path.join(UPLOAD_FOLDER, f"{uid}_{filename}")
    audio.save(audio_path)

    # 2. Run Orchestrator Phases
    pipeline = orchestrate_initial_phase(audio_path)
    topics_file, facts_dir = process_topics(
        transcription_path=pipeline["transcription_path"],
        opportunities_path=pipeline["opportunities_path"],
        session_dir=pipeline["session_dir"]
    )
    scripts_dir = generate_all_scripts(pipeline["session_dir"])
    generate_all_audio(pipeline["session_dir"])

    # 3. Load everything into session
    topics = []
    scripts = {}

    with open(topics_file, "r", encoding="utf-8") as f:
        topics = [line.strip() for line in f if line.strip()]

    for topic in topics:
        topic_file = os.path.join(scripts_dir, f"{topic.replace(' ', '_')}.txt")
        if os.path.exists(topic_file):
            with open(topic_file, "r", encoding="utf-8") as f:
                scripts[topic] = f.read()

    session["topics"] = topics
    session["scripts"] = scripts
    session["session_dir"] = pipeline["session_dir"].split("/")[-1]  # For static path

    return redirect(url_for("results"))

@app.route("/results", methods=["GET"])
def results():
    return render_template("results.html")

