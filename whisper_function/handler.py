import os
import tempfile
import json
import base64
from openai import OpenAI

client = OpenAI()

def handle(event, context):
    try:
        # Check for base64 audio content in event body
        body = json.loads(event.get("body", "{}"))
        audio_b64 = body.get("audio_base64")

        if not audio_b64:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing audio_base64"})
            }

        # Decode and save to a temp file
        audio_data = base64.b64decode(audio_b64)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
            filepath = temp.name
            temp.write(audio_data)

        # Send to Whisper
        with open(filepath, "rb") as file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=file,
                response_format="text"
            )

        os.remove(filepath)

        return {
            "statusCode": 200,
            "body": json.dumps({"transcript": transcript.strip()})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
