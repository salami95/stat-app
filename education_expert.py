# education_expert.py

import os
import re
import sys


def extract_topics(transcript: str) -> list:
    """
    Naive topic extraction based on keyword patterns.
    In production, this can be replaced with an LLM chain or vector search.
    """
    possible_topics = [
        "cardiac output", "heart rate", "stroke volume", "renal physiology",
        "acid-base balance", "pH", "nephrons", "glomerulus", "diabetes", "electrolytes"
    ]

    found_topics = set()
    for topic in possible_topics:
        if re.search(rf"\b{re.escape(topic)}\b", transcript, re.IGNORECASE):
            found_topics.add(topic.lower())

    return list(found_topics)


def identify_gaps(topics: list) -> list:
    """
    Simulated educational analysis of common weak spots.
    In production, this would analyze speaker confidence, coverage, or correctness.
    """
    gap_lookup = {
        "cardiac output": ("major", "You mentioned heart rate and stroke volume, but not how they determine cardiac output."),
        "acid-base balance": ("moderate", "You talked about pH but didn’t explain how the body compensates for acidosis."),
        "renal physiology": ("minor", "You briefly mentioned nephrons, but didn’t expand on their role in filtration."),
    }

    gaps = []
    for topic in topics:
        if topic in gap_lookup:
            severity, description = gap_lookup[topic]
            gaps.append({
                "topic": topic.title(),
                "severity": severity,
                "description": description
            })

    if not gaps:
        gaps.append({
            "topic": "No Gaps Found",
            "severity": "info",
            "description": "We couldn’t detect specific weaknesses, but it’s always good to review core concepts."
        })

    return gaps


def analyze_transcript(transcript: str) -> dict:
    """
    Creates a structured result including:
    - A mock podcast script
    - A list of detected knowledge gaps ("opportunities")
    - A list of topics found
    """
    try:
        intro = "# Welcome to Your Personalized Study Review\n"
        summary = (
            "Based on your recent study session, here are some key insights we noticed. "
            "We’ll walk you through the material, highlight strengths, and address areas for improvement.\n"
        )
        conclusion = (
            "\nWe recommend reviewing the sections mentioned and keeping up the great work!"
        )

        # Extract topics and identify gaps
        topics = extract_topics(transcript)
        gaps = identify_gaps(topics)

        # Script is still a placeholder for now
        full_script = intro + "\n" + summary + "\n" + transcript[:500] + "..." + conclusion

        return {
            "script": full_script,
            "opportunities": gaps,
            "topics": topics
        }

    except Exception as e:
        return {
            "script": "Error generating script. Please try again later.",
            "opportunities": [{
                "topic": "Error",
                "severity": "major",
                "description": f"An exception occurred during analysis: {str(e)}"
            }],
            "topics": []
        }


# ✅ Used by orchestrator.py
def analyze_student_performance(transcript: str) -> str:
    result = analyze_transcript(transcript)
    return result["script"]


def main():
    if len(sys.argv) < 2:
        print("❌ No transcription file path provided.")
        sys.exit(1)

    transcript_path = sys.argv[1]
    if not os.path.isfile(transcript_path):
        print(f"❌ File not found: {transcript_path}")
        sys.exit(1)

    base_name = os.path.splitext(os.path.basename(transcript_path))[0].replace("_transcription", "")
    output_path = os.path.join(os.path.dirname(transcript_path), f"{base_name}_education_expert_analysis.txt")

    print(f"📄 Loading transcription from: {transcript_path}")
    with open(transcript_path, 'r') as f:
        transcript = f.read()

    if not transcript.strip():
        print("⚠️ Transcription appears to be empty.")

    result = analyze_transcript(transcript)

    print(f"💾 Saving education expert analysis to: {output_path}")
    with open(output_path, 'w') as f:
        f.write("# Podcast Script\n")
        f.write(result['script'])
        f.write("\n\n# Opportunities\n")
        for opp in result['opportunities']:
            f.write(f"- [{opp['severity'].upper()}] {opp['topic']}: {opp['description']}\n")
        f.write("\n\n# Topics Found\n")
        for topic in result['topics']:
            f.write(f"- {topic.title()}\n")

    print("✅ Saved education expert analysis successfully.")


if __name__ == "__main__":
    main()
