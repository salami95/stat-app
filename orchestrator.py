# orchestrator.py

import os
import logging
from eleven_labs_scribe import transcribe_audio
from topic_processor import extract_topics
from education_expert import analyze_student_performance
from build_medrag_index import query_medrag
from medical_expert import generate_clarified_explanations
from podcast_script_generator import generate_script
from generate_audio import generate_audio_narration

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def run_phase_1(audio_path):
    try:
        session_dir = os.path.dirname(audio_path)
        base_name = os.path.splitext(os.path.basename(audio_path))[0].replace("_audio", "")

        logger.info("🎙️ Transcribing audio...")
        transcript = transcribe_audio(audio_path)
        transcript_path = os.path.join(session_dir, f"{base_name}_transcript.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        logger.info(f"✅ Transcript saved to {transcript_path}")

        logger.info("📊 Analyzing student performance...")
        performance_report = analyze_student_performance(transcript)
        opportunities_path = os.path.join(session_dir, "opportunities.txt")
        with open(opportunities_path, "w", encoding="utf-8") as f:
            f.write(performance_report)
        logger.info(f"✅ Opportunities saved to {opportunities_path}")

        logger.info("🧠 Extracting topics...")
        topics = extract_topics(transcript, performance_report)
        topics_path = os.path.join(session_dir, "topics.txt")
        with open(topics_path, "w", encoding="utf-8") as f:
            for topic in topics:
                f.write(topic + "\n")
        logger.info(f"✅ Topics saved to {topics_path}")

        return {
            "session_dir": session_dir,
            "transcript_path": transcript_path,
            "topics_path": topics_path,
            "opportunities_path": opportunities_path,
        }

    except Exception as e:
        logger.error(f"❌ Phase 1 failed: {e}", exc_info=True)
        raise

# ✅ THIS IS REQUIRED:
orchestrate_initial_phase = run_phase_1
