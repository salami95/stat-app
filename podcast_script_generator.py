# podcast_script_generator.py

import os
import sys
import openai

# Set API key from environment
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in environment.")

openai.api_key = api_key

def load_file(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ File not found: {path}")
    with open(path, 'r') as f:
        return f.read()

def split_text(text, max_tokens=1500, overlap=100):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(len(words), start + max_tokens)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap  # Overlap for continuity

    return chunks

def generate_script_chunk(chunk):
    prompt = f"""
You are a professional podcast scriptwriter. Your task is to create a structured, engaging, and informative script for a single-person podcast. Use a warm and helpful tone, and organize the material with clear headings:

# Strengths
# Areas for Improvement
# Medical Reinforcement Content

Focus on clinical relevance, study advice, and emotional encouragement.

Content to include:
{chunk}
"""
    try:
        print("🧠 Sending chunk to OpenAI...")
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Or "o3-mini" if that's your target
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"❌ Error in OpenAI request: {e}")
        return f"[ERROR IN THIS SECTION: {e}]"

def main():
    if len(sys.argv) < 3:
        print("❌ Usage: python3 podcast_script_generator.py <education_path> <medical_path>")
        sys.exit(1)

    education_path = sys.argv[1]
    medical_path = sys.argv[2]

    try:
        print(f"📖 Loading education expert analysis: {education_path}")
        education_text = load_file(education_path)

        print(f"📖 Loading medical expert content: {medical_path}")
        medical_text = load_file(medical_path)

        # Combine content
        combined = f"# Education Analysis\n\n{education_text}\n\n# Medical Expert Content\n\n{medical_text}"
        chunks = split_text(combined)
        print(f"🔍 Split into {len(chunks)} chunks")

        all_script_parts = []
        for idx, chunk in enumerate(chunks):
            print(f"▶️ Processing chunk {idx + 1} of {len(chunks)}")
            part = generate_script_chunk(chunk)
            all_script_parts.append(part)
            print(f"✅ Chunk {idx + 1} complete")

        full_script = "\n\n---\n\n".join(all_script_parts)

        base_name = os.path.splitext(os.path.basename(education_path))[0].replace("_education_expert_analysis", "")
        output_path = os.path.join(os.path.dirname(education_path), f"{base_name}_podcast_script.txt")

        with open(output_path, 'w') as f:
            f.write(full_script)

        print(f"✅ Saved podcast script to: {output_path}")

    except Exception as e:
        print(f"❌ General error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
