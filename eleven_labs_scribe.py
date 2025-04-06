# eleven_labs_scribe.py

import os
from io import BytesIO
from elevenlabs.client import ElevenLabs


def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes a study session audio file using ElevenLabs Scribe.
    Returns the raw transcription text.
    """
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("❌ ELEVENLABS_API_KEY not set in environment variables.")

    client = ElevenLabs(api_key=api_key)

    try:
        with open(audio_path, "rb") as audio_file:
            audio_data = BytesIO(audio_file.read())

        print(f"🎧 Transcribing audio from {audio_path}...")

        result = client.speech_to_text.convert(
            file=audio_data,
            model_id="scribe_v1",
            tag_audio_events=True,
            language_code="eng",
            diarize=True
        )

        # Log metadata
        print("✅ Transcription complete.")
        print(f"🗣️ Speakers detected: {len(set([seg['speaker'] for seg in result.segments]))}")
        print(f"📝 Total segments: {len(result.segments)}")

        # Optionally: return full JSON or just raw text
        return result.text

    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        raise
