from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

OpenAI.api_key = api_key
client = OpenAI(api_key=api_key)

try:
    # Load the transcription file
    with open("/Users/kevinsalimi_1/STAT/NBME_FORM_8_OB-GYN.txt", "r") as file:  # Updated file path
        transcription_text = file.read()
    print("Loaded NBME_FORM_8_OB-GYN.txt successfully.")  # Updated log message
except FileNotFoundError:
    print("Error: NBME_FORM_8_OB-GYN.txt not found.")  # Updated error message
    exit(1)

# Function to split the transcription into chunks
def split_transcription(transcription, max_tokens=1500):
    """Split the transcription into smaller chunks to fit within the model's token limit."""
    words = transcription.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1  # Account for spaces
        if current_length >= max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# Split the transcription into chunks
chunks = split_transcription(transcription_text)

# Initialize a list to store the results
results = []

# Process each chunk
for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i + 1} of {len(chunks)}...")
    chunk_prompt = f"""
    You are a medical expert with deep understanding of the complexities of medicine. Below is a transcription of a medical student's study session that outlines pitfalls, mistakes, and gaps in knowledge. Your task is to supply detailed, comprehensive information addressing these gaps, ensuring the student has all the necessary content to answer similar questions correctly in the future. Additionally, reinforce the topics the student answered correctly to aid in spaced repetition as the student will be reviewing the content you provide on a regular basis to remind themselves of topics they have covered. Deliver your response as plain text with no extra formatting.

    Transcription:
    {chunk}
    """

    try:
        print("Sending request to OpenAI API...")
        # Generate the analysis for the current chunk
        response = client.responses.create(
            model="o3-mini",
            reasoning={"effort": "medium"},
            input=[
                {
                    "role": "user", 
                    "content": chunk_prompt
                }
            ],
            timeout=600  # Add a timeout to prevent indefinite hanging
        )
        results.append(response.output_text)
        print(f"Processed chunk {i + 1} successfully.")
    except Exception as e:
        print(f"Error during OpenAI API call for chunk {i + 1}: {e}")
        exit(1)

# Combine all results into a single output
final_output = "\n\n".join(results)

try:
    # Save the combined results to a new file
    with open("medical_expert.txt", "w") as file:
        file.write(final_output)
    print("Saved medical_expert.txt successfully.")
except Exception as e:
    print(f"Error saving medical_expert.txt: {e}")
    exit(1)



