from flask import Flask, render_template, request, redirect, url_for
import os
import io
import sys
from contextlib import redirect_stdout

from education_expert import run_education_analysis
from medical_expert import run_medical_analysis
from podcast_script_generator import generate_podcast_script
from eleven_labs_scribe import generate_audio_file

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

    # Redirect to processing and pass filename via query parameter
    return redirect(url_for('processing', filename=audio.filename))

@app.route('/processing')
def processing():
    filename = request.args.get('filename')
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Capture all print output from backend processing
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        try:
            print(f"Processing started for: {filename}")
            # STEP 1: Transcribe (simulate here for now)
            transcription_path = audio_path.replace('.mp3', '.txt')  # just example
            with open(transcription_path, 'w') as f:
                f.write("Simulated transcription from audio...")  # Simulated

            print(f"Transcription saved to: {transcription_path}")

            # STEP 2: Education expert
            run_education_analysis(transcription_path)

            # STEP 3: Medical expert
            run_medical_analysis()

            # STEP 4: Script generation
            generate_podcast_script()

            # STEP 5: Audio generation
            generate_audio_file()

            print("All processing complete ✅")

        except Exception as e:
            print(f"❌ Error during processing: {e}")

    # Get the output
    output = buffer.getvalue()
    return render_template('processing.html', log_output=output)

if __name__ == '__main__':
    app.run(debug=True)
