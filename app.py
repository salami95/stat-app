from flask import Flask, render_template, request, redirect, url_for
import os
import io
import subprocess
from contextlib import redirect_stdout

app = Flask(__name__)
UPLOAD_FOLDER = '/home/salami95/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'audio' not in request.files:
        return 'No audio file provided', 400

    audio = request.files['audio']
    if audio.filename == '':
        return 'No selected file', 400

    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)
    audio.save(audio_path)

    return redirect(url_for('processing', filename=audio.filename))

@app.route('/processing')
def processing():
    filename = request.args.get('filename')
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        try:
            print(f"Processing started for: {filename}")

            # STEP 1: Simulate transcription
            transcription_path = audio_path.replace('.mp3', '.txt')  # update extension
            with open(transcription_path, 'w') as f:
                f.write("Simulated transcription from audio...")

            print(f"Transcription saved to: {transcription_path}")

            # STEP 2: Run each expert script as a separate process
            subprocess.run(['python3', 'education_expert.py'], check=True)
            subprocess.run(['python3', 'medical_expert.py'], check=True)
            subprocess.run(['python3', 'podcast_script_generator.py'], check=True)
            subprocess.run(['python3', 'eleven_labs_scribe.py'], check=True)

            print("All processing complete ✅")

        except subprocess.CalledProcessError as e:
            print(f"❌ Subprocess error: {e}")
        except Exception as e:
            print(f"❌ Error during processing: {e}")

    output = buffer.getvalue()
    return render_template('processing.html', log_output=output)

if __name__ == '__main__':
    app.run(debug=True)
