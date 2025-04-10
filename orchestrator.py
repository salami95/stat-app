import os
from topic_processor import process_topics
from medical_expert import generate_medical_analysis
from education_expert import generate_educational_summary
from podcast_script_generator import generate_podcast_script
from generate_audio import generate_audio_files


def process_audio_session(session_id, session_dir, transcript):
    """
    Orchestrates the end-to-end processing of an audio session.
    This includes topic extraction, RAG grounding, educational analysis, and podcast generation.

    Args:
        session_id (str): Unique identifier for the user session.
        session_dir (str): Directory for session files and outputs.
        transcript (str): Transcript text of the uploaded audio.

    Returns:
        dict: Results dictionary with topics, scripts, and metadata.
    """
    try:
        print("[Orchestrator] Starting session orchestration...")

        # Extract and RAG-ground topics
        topics = process_topics(transcript)
        print(f"[Orchestrator] Topics extracted: {topics}")

        # Prepare result containers
        scripts = {}
        audio_output_dir = os.path.join("static", session_dir, "audio")
        os.makedirs(audio_output_dir, exist_ok=True)

        # Process each topic individually
        for topic in topics:
            print(f"[Orchestrator] Processing topic: {topic}")

            # Medical RAG + Expert Synthesis
            medical_insight = generate_medical_analysis(topic)
            print(f"[Orchestrator] Medical insight generated.")

            # Educational Synthesis (non-redundant, higher level)
            education_summary = generate_educational_summary(transcript, topic)
            print(f"[Orchestrator] Educational summary complete.")

            # Podcast script generation
            script = generate_podcast_script(topic, medical_insight, education_summary)
            scripts[topic] = script
            print(f"[Orchestrator] Podcast script written.")

            # Text-to-speech synthesis
            # Audio generation temporarily disabled
            print(f"[TTS] Skipped audio generation for topic: {topic}")

        print("[Orchestrator] All topics processed successfully.")
        return {
            "topics": topics,
            "scripts": scripts,
            "session_dir": session_dir
        }

    except Exception as e:
        print(f"[Orchestrator] Error during session processing: {e}")
        raise
