# eleven_labs_scribe.py

import os
import sys
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings

def load_script(script_path):
    if not os.path.isfile(script_path):
        raise FileNotFoundError(f"❌ Script file not found: {script_path}")
    with open(script_path, 'r') as f:
        return f.read()

def synthesize_speech(script_text, output_path):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("❌ ELEVENLABS_API_KEY not found in environment.")

    client = ElevenLabs(api_key=api_key)

    try:
        print("🎙️ Starting text-to-speech synthesis...")
        audio = client.text_to_speech.convert(
            voice=Voice(
                voice_id="Rachel",  # You can change this to a different ElevenLabs voice ID
                settings=VoiceSettings(stability=0.7, similarity_boost=0.75)
            ),
            model="eleven_multilingual_v2",  # Current best TTS model
            text=script_text
        )

        print(f"💾 Saving MP3 to: {output_path}")
        audio.save(filename=output_path)
        print("✅ Podcast audio file generated successfully.")

    except Exception as e:
        print(f"❌ Error during ElevenLabs TTS generation: {e}")
        raise

def main():
    if len(sys.argv) < 3:
        print("❌ Usage: python3 eleven_labs_scribe.py <script_path> <base_name>")
        sys.exit(1)

    script_path = sys.argv[1]
    base_name = sys.argv[2]
    output_path = os.path.join("uploads", f"{base_name}_final_podcast.mp3")

    try:
        print(f"📖 Loading podcast script: {script_path}")
        script_text = load_script(script_path)

        synthesize_speech(script_text, output_path)

    except Exception as e:
        print(f"❌ Final error in TTS flow: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
