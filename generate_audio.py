import os
from elevenlabs import ElevenLabs

# === CONFIGURATION ===
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"  # Replace with your preferred voice ID
MODEL_ID = "eleven_multilingual_v2"
OUTPUT_FORMAT = "mp3_44100_128"  # Best compatibility and audio quality

client = ElevenLabs(
    api_key=os.environ["RelentlessKomodoDragon"]
)


def generate_audio_for_script(text, topic_name, output_dir):
    response = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        text=text,
        model_id=MODEL_ID,
        output_format=OUTPUT_FORMAT,
    )

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{topic_name.replace(' ', '_')}.mp3")
    with open(output_path, "wb") as f:
        f.write(response)
    return output_path

def generate_all_audio(session_dir):
    scripts_dir = os.path.join(session_dir, "scripts")
    output_dir = os.path.join(session_dir, "audio")
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(scripts_dir):
        if filename.endswith(".txt"):
            topic = filename.replace(".txt", "").replace("_", " ")
            with open(os.path.join(scripts_dir, filename), "r", encoding="utf-8") as f:
                text = f.read().strip()

            print(f"[INFO] Generating audio for topic: {topic}")
            generate_audio_for_script(text, topic, output_dir)

    print(f"[INFO] Audio generation complete. Files saved to: {output_dir}")
    return output_dir
