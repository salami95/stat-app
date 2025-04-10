import os
import tempfile
from flask import Flask, render_template, request, redirect, session, send_from_directory
from werkzeug.utils import secure_filename
from whisper import transcribe_audio
from topic_processor import process_topics
from education_expert import analyze_student_performance
from podcast_script_generator import generate_podcast_scripts

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "stat_secret_key")
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['audio']
    if not file:
        return "No file uploaded", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    session['log_output'] = "Processing started...\n"
    session.modified = True

    try:
        # Step 1: Transcription
        transcript = transcribe_audio(filepath)
        session['log_output'] += "✓ Transcription completed.\n"

        # Step 2: Topic Extraction + RAG Fact Retrieval
        topics, topic_facts = process_topics(transcript)
        session['log_output'] += f"✓ Extracted {len(topics)} topics.\n"

        # Step 3: Education Expert Analysis
        performance_summary = analyze_student_performance(transcript, topics)
        session['log_output'] += "✓ Student performance analyzed.\n"

        # Step 4: Script Generation
        scripts = generate_podcast_scripts(topic_facts)
        session['log_output'] += "✓ Podcast scripts generated.\n"

        session['topics'] = topics
        session['scripts'] = scripts
        session['summary'] = performance_summary

        return redirect('/results')

    except Exception as e:
        session['log_output'] += f"✗ Error: {str(e)}\n"
        return redirect('/processing')

@app.route('/processing')
def processing():
    return render_template("processing.html", log_output=session.get("log_output", ""))

@app.route('/results')
def results():
    return render_template("results.html", session=session)

if __name__ == '__main__':
    app.run(debug=True)
