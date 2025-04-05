from flask import Flask, render_template, request, redirect, url_for
import os
import io
import subprocess
import uuid
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

    # Generate a safe unique base name
    original_filename = os.path.splitext(audio.filename)[0]
    unique_id = uuid.uuid4().hex[:8]
    base_name = f"{original_filename}_{unique_id}"

    # Save the uploaded file
    audio_filename = f"{base_name}{os.path.splitext(audio.filename)[1]}"
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
    audio.save(audio_path)

    return redirect(url_for('processing', base=base_name))

@app.route('/processing')
def processing():
    base_name = request.args.get('base')
    if not base_name:
        return "Missing session base name.", 400

    # Set up paths
    transcription_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_name}_transcription.txt")

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        try:
            print(f"🟡 Processing session: {base_name}")

            # STEP 1: Simulate transcription
            with open(transcription_path, 'w') as f:
                f.write("Simulated transcription from audio...")
            print(f"✅ Transcription saved: {transcription_path}")

            # STEP 2: Run education expert
            print("▶️ Running education_expert.py...")
            subprocess.run(['python3', 'education_expert.py', transcription_path], check=True)

            # Check for expected file
           education_output = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_name}_education_expert_analysis.txt")
            print("▶️ Running medical_expert.py...")
            subprocess.run(['python3', 'medical_expert.py', transcription_path, education_output], check=True)

            # STEP 3: Run medical expert
            print("▶️ Running medical_expert.py...")
            subprocess.run(['python3', 'medical_expert.py'], check=True)

            medical_output = os.path.join(app.config['UPLOAD_FOLDER'], "medical_expert_analysis.txt")
            if not os.path.exists(medical_output):
                raise FileNotFoundError("medical_expert_analysis.txt not found after script.")

            # STEP 4: Run podcast script generator
            print("▶️ Running podcast_script_generator.py...")
            subprocess.run([
                'python3', 'podcast_script_generator.py',
                education_output, medical_output
            ], check=True)


            script_output = os.path.join(app.config['UPLOAD_FOLDER'], "podcast_script.txt")
            if not os.path.exists(script_output):
                raise FileNotFoundError("podcast_script.txt not found after script.")

            # STEP 5: Run Eleven Labs TTS
            print("▶️ Running eleven_labs_scribe.py...")
            subprocess.run(['python3', 'eleven_labs_scribe.py'], check=True)

            print("✅ All processing steps completed successfully!")

        except subprocess.CalledProcessError as e:
            print(f"❌ Subprocess failed: {e}")
        except Exception as e:
            print(f"❌ General error: {e}")

    output = buffer.getvalue()
    return render_template('processing.html', log_output=output)

if __name__ == '__main__':
    app.run(debug=True)
