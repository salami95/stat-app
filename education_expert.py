# education_expert.py

import re

def analyze_transcript(transcript):
    """
    Analyze the transcript and return a structured result including:
    - A mock podcast script
    - A list of detected knowledge gaps ("opportunities")

    Parameters:
    transcript (str): Full text from transcription

    Returns:
    dict: {
        "script": str,
        "opportunities": list of dicts with keys: topic, severity, description
    }
    """

    try:
        # === Generate dummy podcast script ===
        intro = "# Welcome to Your Personalized Study Review\n"
        summary = (
            "Based on your recent study session, here are some key insights we noticed. "
            "We’ll walk you through the material, highlight strengths, and address areas for improvement.\n"
        )
        conclusion = (
            "\nWe recommend reviewing the sections mentioned and keeping up the great work!"
        )

        full_script = intro + "\n" + summary + "\n" + transcript[:500] + "..." + conclusion

        # === Generate dummy opportunities (gaps) ===
        gaps = []

        # Example logic: if a keyword is missing or weakly explained, flag it
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

        # If no keywords found, return a default "no gaps" message
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
        # Error fallback to prevent crashing
        return {
            "script": "Error generating script. Please try again later.",
            "opportunities": [{
                "topic": "Error",
                "severity": "major",
                "description": f"An exception occurred during analysis: {str(e)}"
            }]
        }
