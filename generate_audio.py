# generate_audio.py

import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# Load ElevenLabs API key
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not ELEVENLABS_API_KEY:
    raise EnvironmentError("❌ ELEVENLABS_API_KEY not set in environment variables.")

# Initialize ElevenLabs TTS client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)


def generate_audio_narration(topic: str, script_text: str, output_path: str = None) -> str:
    """
    Converts the script text into spoken audio using ElevenLabs.
    Saves to the specified output path (or temp path if not provided).
    Returns the full path to the audio file.
    """
    # Generate audio from text
    audio = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel (update if needed)
        model_id="eleven_multilingual_v2",
        text=script_text,
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.5)
    )

    # Determine output path
    if output_path is None:
        from tempfile import gettempdir
        output_path = os.path.join(gettempdir(), f"{topic.replace(' ', '_')}_narration.mp3")

    # Write the audio file
    with open(output_path, "wb") as f:
        f.write(audio)

    print(f"✅ Audio narration saved to {output_path}")
    return output_path


# ✅ Compatibility alias for app.py
generate_all_audio = generate_audio_narration
