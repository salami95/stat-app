import os
import tempfile
import openai

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(file_path):
    """
    Transcribes audio using OpenAI Whisper API.
    
    Args:
        file_path (str): Path to the input audio file.

    Returns:
        str: The transcribed text.
    """
    try:
        print(f"[Whisper] Starting transcription for: {file_path}")

        with open(file_path, "rb") as audio_file:
            transcript_response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

        print("[Whisper] Transcription completed successfully.")
        return transcript_response

    except Exception as e:
        print(f"[Whisper] Error during transcription: {e}")
        return ""
