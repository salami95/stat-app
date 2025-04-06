# medical_expert.py

import os
import sys
import openai

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in environment.")

openai.api_key = api_key


def load_file(filepath: str) -> str:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")
    with open(filepath, 'r') as f:
        return f.read()


def split_transcription(text: str, max_tokens: int = 1500, overlap: int = 100) -> list:
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(len(words), start + max_tokens)
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks


def generate_response(chunk: str) -> str:
    prompt = f"""
You are a medical expert with deep understanding of clinical and scientific medicine. Below is a transcription of a medical student's study session, including analysis of their learning gaps and strengths. 

Your task is to:
1. Clarify misunderstood or incomplete concepts using accurate, detailed medical information.
2. Reinforce correct information for spaced repetition.
3. Avoid excessive verbosity—focus on educational impact.

Return your answer as plain text with no extra formatting.

Content:
{chunk}
"""
    try:
        print("⏳ Sending request to OpenAI API...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"❌ Error during OpenAI API call: {e}")
        return f"[Error processing this chunk: {e}]"


# ✅ Exposed function for orchestration
def generate_clarified_explanations(transcription_path: str, education_path: str) -> str:
    print(f"📄 Loading transcription from: {transcription_path}")
    transcription_text = load_file(transcription_path)

    print(f"📄 Loading education expert analysis from: {education_path}")
    education_text = load_file(education_path)

    combined_input = transcription_text + "\n\n# Education Analysis\n\n" + education_text
    chunks = split_transcription(combined_input)

    print(f"🔍 Split into {len(chunks)} chunks for processing.")
    results = []
    for idx, chunk in enumerate(chunks):
        print(f"▶️ Processing chunk {idx + 1} of {len(chunks)}")
        result = generate_response(chunk)
        results.append(result)
        print(f"✅ Finished chunk {idx + 1}")

    return "\n\n---\n\n".join(results)


def main():
    if len(sys.argv) < 3:
        print("❌ Usage: python3 medical_expert.py <transcription_path> <education_analysis_path>")
        sys.exit(1)

    transcription_path = sys.argv[1]
    education_path = sys.argv[2]

    try:
        final_output = generate_clarified_explanations(transcription_path, education_path)

        base_name = os.path.splitext(os.path.basename(transcription_path))[0].replace("_transcription", "")
        output_path = os.path.join(os.path.dirname(transcription_path), f"{base_name}_medical_expert_analysis.txt")

        with open(output_path, 'w') as f:
            f.write(final_output)

        print(f"✅ Saved medical expert analysis to: {output_path}")

    except Exception as e:
        print(f"❌ General error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
