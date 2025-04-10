import os
import tempfile
import requests
from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "stat_secret_key")
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# URLs for backend services
BACKEND_JOB_URL = os.getenv("BACKEND_JOB_URL", "http://jobqueue-production.up.railway.app/start-job")
WHISPER_URL = os.getenv("WHISPER_URL", "http://whisperservice-production.up.railway.app:80")
TOPIC_URL = os.getenv("TOPIC_URL", "http://topicservice-production.up.railway.app:80")
RAG_URL = os.getenv("RAG_URL", "http://ragservice-production.up.railway.app:80")
SCRIPTGEN_URL = os.getenv("SCRIPTGEN_URL", "http://scriptgenservice-production.up.railway.app:80")

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('audio')
    if not file:
        return "No file uploaded", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    session['log_output'] = "Upload received. Starting processing...\n"
    session.modified = True

    try:
        # Trigger backend processing (this communicates with the job queue service)
        response = requests.post(BACKEND_JOB_URL, json={"filepath": filepath})
        response.raise_for_status()
        session['log_output'] += "✓ Processing job submitted successfully.\n"
    except Exception as e:
        session['log_output'] += f"✗ Failed to start processing: {str(e)}\n"

    return redirect('/processing')

@app.route('/processing')
def processing():
    return render_template("processing.html", log_output=session.get("log_output", ""))

@app.route('/results')
def results():
    return render_template("results.html", session=session)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
