import os
import time
from eleven_labs_scribe import transcribe_audio
from education_expert import analyze_transcript

# Step 1: Create timestamped output directory for this session
def create_session_dir(base_path="outputs"):
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    session_dir = os.path.join(base_path, timestamp)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir

# Step 2: Transcribe uploaded audio file
def run_transcription(audio_path, session_dir):
    transcription_output_path = os.path.join(session_dir, "raw_transcription.txt")
    transcription = transcribe_audio(audio_path)
    with open(transcription_output_path, "w", encoding="utf-8") as f:
        f.write(transcription)
    return transcription_output_path

# Step 3: Analyze transcript with education expert prompt
def run_education_analysis(transcription_path, session_dir):
    with open(transcription_path, "r", encoding="utf-8") as f:
        transcript = f.read()
    opportunities_output_path = os.path.join(session_dir, "opportunities.txt")
    analysis = analyze_transcript(transcript)
    with open(opportunities_output_path, "w", encoding="utf-8") as f:
        f.write(analysis)
    return opportunities_output_path

# Master function for Step 1
def orchestrate_initial_phase(audio_path):
    print(f"[INFO] Starting pipeline for: {audio_path}")
    session_dir = create_session_dir()
    print(f"[INFO] Session directory: {session_dir}")

    transcription_path = run_transcription(audio_path, session_dir)
    print(f"[INFO] Transcription saved at: {transcription_path}")

    opportunities_path = run_education_analysis(transcription_path, session_dir)
    print(f"[INFO] Opportunities saved at: {opportunities_path}")

    return {
        "session_dir": session_dir,
        "transcription_path": transcription_path,
        "opportunities_path": opportunities_path
    }

# CLI runner (optional if calling manually)
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py path/to/audio/file.mp3")
    else:
        audio_file = sys.argv[1]
        orchestrate_initial_phase(audio_file)
