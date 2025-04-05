import os
from io import BytesIO
from elevenlabs.client import ElevenLabs

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes the audio file at the given file_path using the Eleven Labs Scribe API.

    Parameters:
      file_path (str): The path to the audio file.

    Returns:
      str: The transcribed text from the audio.
    """
    # Retrieve the API key from environment variables.
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not set in environment variables.")

    # Initialize the ElevenLabs client with your API key.
    client = ElevenLabs(api_key=api_key)

    # Read the audio file into a BytesIO object.
    with open(file_path, "rb") as audio_file:
        audio_data = BytesIO(audio_file.read())

    # Convert the audio to text.
    transcription = client.speech_to_text.convert(
        file=audio_data,
        model_id="scribe_v1",       # Model to use for transcription
        tag_audio_events=True,      # Option to tag audio events (e.g., laughter)
        language_code="eng",        # Language of the audio file
        diarize=True,               # Annotate who is speaking
    )

    return transcription.text

# For testing purposes, you could add:
if __name__ == "__main__":
    # Replace with an actual path to a test audio file (ensure this file exists on your server)
    test_file_path = "uploads/your_test_audio_file.m4a"
    try:
        result = transcribe_audio(test_file_path)
        print("Transcription:", result)
    except Exception as e:
        print("Error during transcription:", e)
