import os
import tempfile
from openai import OpenAI

client = OpenAI()

def transcribe_audio(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError("Audio file not found")

    with open(filepath, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return transcript.strip()
