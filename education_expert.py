# education_expert.py

import re
import os
import sys
import json

def analyze_transcript(transcript):
    """
    Analyze the transcript and return a structured result including:
    - A mock podcast script
    - A list of detected knowledge gaps ("opportunities")
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

        full_script = intro + "\n" + summary + "\n" + transcript[:500] + "..." + conclusion

        gaps = []

        weak_spots = [
            ("cardiac output", "major", "You mentioned heart rate and stroke volume, but not how they determine cardiac output."),
            ("acid-base balance", "moderate", "You talked about pH but didn’t explain how the body compensates for acidosis."),
            ("renal physiology", "minor", "You briefly mentioned nephrons, but didn’t expand on their role in filtration."),
        ]

        for term, severity, explanation in weak_spots:
            if re.search(term, transcript, re.IGNORECASE):
                gaps.append({
                    "topic": term.title(),
                    "severity": severity,
                    "description": explanation
                })

        if not gaps:
            gaps = [{
                "topic": "No Gaps Found",
                "severity": "info",
                "description": "We couldn’t detect specific weaknesses, but it’s always good to review core concepts."
            }]

        return {
            "script": full_script,
            "opportunities": gaps
        }

    except Exception as e:
        return {
            "script": "Error generating script. Please try again later.",
            "opportunities": [{
                "topic": "Error",
                "severity": "major",
                "description": f"An exception occurred during analysis: {str(e)}"
            }]
        }


def main():
    if len(sys.argv) < 2:
        print("❌ No transcription file path provided.")
        sys.exit(1)

    transcript_path = sys.argv[1]
    if not os.path.isfile(transcript_path):
        print(f"❌ File not found: {transcript_path}")
        sys.exit(1)

    # Determine output base name
    base_name = os.path.splitext(os.path.basename(transcript_path))[0].replace("_transcription", "")
    output_path = os.path.join(os.path.dirname(transcript_path), f"{base_name}_education_expert_analysis.txt")

    print(f"📄 Loading transcription from: {transcript_path}")
    with open(transcript_path, 'r') as f:
        transcript = f.read()

    if not transcript.strip():
        print("⚠️ Transcription appears to be empty.")
    
    result = analyze_transcript(transcript)

    # Save as a JSON-ish text file (line-separated key: value)
    print(f"💾 Saving education expert analysis to: {output_path}")
    with open(output_path, 'w') as f:
        f.write("# Podcast Script\n")
        f.write(result['script'])
        f.write("\n\n# Opportunities\n")
        for opp in result['opportunities']:
            f.write(f"- [{opp['severity'].upper()}] {opp['topic']}: {opp['description']}\n")

    print("✅ Saved education expert analysis successfully.")


if __name__ == "__main__":
    main()
