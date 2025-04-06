import os
from elevenlabs import generate, save, set_api_key
from dotenv import load_dotenv
import tempfile
import whisper

load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
set_api_key(ELEVENLABS_API_KEY)

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def generate_audio_narration(topic, script_text):
    if not ELEVENLABS_API_KEY:
        raise EnvironmentError("ELEVENLABS_API_KEY not set in environment.")

    # Generate the audio from script text using ElevenLabs
    audio = generate(
        text=script_text,
        voice="Rachel",  # Change this to your preferred voice
        model="eleven_multilingual_v2"
    )

    # Save to a temp file
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, f"{topic.replace(' ', '_')}_narration.mp3")
    save(audio, output_path)

    return output_path
