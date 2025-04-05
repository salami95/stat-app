from flask import Flask, render_template, request, redirect, url_for, Response
import time
import os

UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with a secure key for production

# 🔁 Global status log to store backend updates
status_log = []

# ✅ Function to record each step (we'll use this in backend processing code later)
def log_status(message):
    timestamp = time.strftime("[%H:%M:%S] ")
    status_log.append(f"{timestamp}{message}")
    print(f"{timestamp}{message}")  # Optional: prints to terminal

@app.route("/get-log")
def get_log():
    return {"log": status_log}

# 🟩 Welcome screen (upload audio)
@app.route('/', methods=['GET'])
def welcome():
    return render_template('welcome.html')

# 🟦 Upload route – starts processing
@app.route('/upload', methods=['POST'])
def upload():
    audio_file = request.files.get('audio')
    if audio_file:
        audio_file.save(os.path.join(UPLOAD_DIR, 'temp_audio.wav'))
        status_log.clear()
        log_status("Audio file received. Preparing to begin processing...")
        return redirect(url_for('processing'))
    return redirect(url_for('welcome'))

from threading import Thread

@app.route('/processing')
def processing():
    def background_process():
        log_status("Starting transcription using Whisper...")
        time.sleep(1)
        log_status("Transcription complete.")
        time.sleep(1)
        log_status("Analyzing with education expert...")
        time.sleep(1)
        log_status("Education expert analysis done.")
        time.sleep(1)
        log_status("Running medical expert analysis...")
        time.sleep(1)
        log_status("Medical expert analysis complete.")
        time.sleep(1)
        log_status("Creating podcast script...")
        time.sleep(1)
        log_status("Podcast script generated.")
        time.sleep(1)
        log_status("Sending to ElevenLabs for voice generation...")
        time.sleep(1)
        log_status("Final podcast audio ready.")

    Thread(target=background_process).start()
    return render_template('processing.html')


# 🎧 Final results screen (will later show script/audio)
@app.route('/results')
def results():
    return "Results page placeholder. Podcast download link will appear here."

if __name__ == '__main__':
    app.run(debug=True)
