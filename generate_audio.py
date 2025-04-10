import os
from elevenlabs import generate, save, Voice, VoiceSettings
from dotenv import load_dotenv

load_dotenv()
ELEVEN_LABS_API_KEY = os.getenv("ELEVEN_LABS_API_KEY")


def generate_audio_files(script, topic, output_dir):
    """
    Generates an audio file from the given script using ElevenLabs TTS.

    Args:
        script (str): The podcast script text.
        topic (str): The topic name (used for naming the output file).
        output_dir (str): The directory where audio files will be saved.
    """
    try:
        print(f"[TTS] Generating audio for: {topic}")
        
        voice = Voice(
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice
            settings=VoiceSettings(
                stability=0.3,
                similarity_boost=0.75
            )
        )

        audio = generate(
            text=script,
            voice=voice,
            api_key=ELEVEN_LABS_API_KEY
        )

        output_path = os.path.join(output_dir, f"{topic.replace(' ', '_')}.mp3")
        save(audio, output_path)

        print(f"[TTS] Audio saved to: {output_path}")

    except Exception as e:
        print(f"[TTS] Error generating audio for '{topic}': {e}")
