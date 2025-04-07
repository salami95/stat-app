# eleven_labs_scribe.py

import os
from io import BytesIO
from elevenlabs import Scribe


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes a study session audio file using ElevenLabs Scribe.
    Returns the raw transcription text.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("❌ ELEVENLABS_API_KEY not set in environment variables.")

    scribe = Scribe(api_key=api_key)

    try:
        with open(audio_path, "rb") as audio_file:
            audio_data = BytesIO(audio_file.read())

        print(f"🎧 Transcribing audio from {audio_path}...")

        result = scribe.transcribe(
            audio=audio_data,
            model="scribe-v1",
            diarize=True,
            summarize=False
        )

        print("✅ Transcription complete.")
        print(f"🗣️ Speakers detected: {len(set([seg['speaker'] for seg in result.segments]))}")
        print(f"📝 Total segments: {len(result.segments)}")

        return result.text

    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        raise
