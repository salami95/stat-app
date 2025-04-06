import os
import tempfile
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings

# Load API key
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Initialize Whisper for transcription
def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

# Initialize ElevenLabs TTS client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def generate_audio_narration(topic, script_text):
    if not ELEVENLABS_API_KEY:
        raise EnvironmentError("ELEVENLABS_API_KEY not set in environment.")

    # Generate audio
    audio = client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel's ID, update if needed
        model_id="eleven_multilingual_v2",
        text=script_text,
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.5)
    )

    # Save to a temp file
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"{topic.replace(' ', '_')}_narration.mp3")
    with open(output_path, "wb") as f:
        f.write(audio)

    return output_path
