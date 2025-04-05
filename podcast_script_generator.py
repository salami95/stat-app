import os
from openai import OpenAI
print("Initializing OpenAI client...")
print("Initializing podcast script generator...")

# File paths
opportunities_file = "/Users/kevinsalimi_1/STAT/opportunities.txt"
medical_expert_file = "/Users/kevinsalimi_1/STAT/medical_expert.txt"
output_file = "/Users/kevinsalimi_1/STAT/podcast_script.txt"

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

OpenAI.api_key = api_key
client = OpenAI(api_key=api_key)

# Function to split text into chunks
def split_text(text, max_tokens=1500):
    """Split the text into smaller chunks to fit within the model's token limit."""
    words = text.split()
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

# Read and process opportunities.txt
try:
    with open(opportunities_file, "r") as file:
        opportunities_text = file.read()
    print("Loaded opportunities.txt successfully.")
except FileNotFoundError:
    print("Error: opportunities.txt not found.")
    exit(1)

# Read and process medical_expert.txt
try:
    with open(medical_expert_file, "r") as file:
        medical_expert_text = file.read()
    print("Loaded medical_expert.txt successfully.")
except FileNotFoundError:
    print("Error: medical_expert.txt not found.")
    exit(1)

# Combine the content of both files
combined_content = f"""
Below is the combined content from two sources:

1. Opportunities for improvement and strengths:
{opportunities_text}

2. Detailed medical insights:
{medical_expert_text}
"""

# Split the combined content into chunks
chunks = split_text(combined_content)

# Initialize a list to store the podcast script
podcast_script = []

# Process each chunk
for i, chunk in enumerate(chunks):
    print(f"Processing chunk {i + 1} of {len(chunks)}...")
    chunk_prompt = f"""
    You are a professional podcast scriptwriter. Your task is to create a well-written, engaging, and informative script for a single-person podcast. The script should cover all the information provided below in a structured and detailed manner. Ensure the script flows naturally, uses conversational language, and emphasizes key points effectively.

    Content:
    {chunk}
    """

    try:
        print("Sending request to OpenAI API...")
        # Generate the script for the current chunk
        response = client.responses.create(
            model="o3-mini",
            reasoning={"effort": "high"},
            input=[
                {
                    "role": "user",
                    "content": chunk_prompt
                }
            ],
            timeout=600  # Add a timeout to prevent indefinite hanging
        )
        podcast_script.append(response.output_text)
        print(f"Processed chunk {i + 1} successfully.")
    except Exception as e:
        print(f"Error during OpenAI API call for chunk {i + 1}: {e}")
        exit(1)

# Combine all parts into a single script
final_script = "\n\n".join(podcast_script)

# Save the podcast script to a file
try:
    with open(output_file, "w") as file:
        file.write(final_script)
    print(f"Saved podcast script to {output_file} successfully.")
except Exception as e:
    print(f"Error saving podcast script: {e}")
    exit(1)
