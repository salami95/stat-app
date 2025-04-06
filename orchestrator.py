# orchestrator.py

import os
import logging
from generate_audio import transcribe_audio
from topic_processor import extract_topics
from education_expert import analyze_student_performance
from build_medrag_index import query_medrag
from medical_expert import generate_clarified_explanations
from podcast_script_generator import generate_script

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

        logger.info("🧠 Extracting topics...")
        topics = extract_topics(transcript)
        topics_path = os.path.join(session_dir, "topics.txt")
        with open(topics_path, "w", encoding="utf-8") as f:
            for topic in topics:
                f.write(topic + "\n")
        logger.info(f"✅ Topics saved to {topics_path}")

        logger.info("📊 Analyzing student performance...")
        performance_report = analyze_student_performance(transcript)
        opportunities_path = os.path.join(session_dir, "opportunities.txt")
        with open(opportunities_path, "w", encoding="utf-8") as f:
            for opp in performance_report["opportunities"]:
                f.write(f"[{opp['severity'].upper()}] {opp['topic']}: {opp['description']}\n")
        logger.info(f"✅ Opportunities saved to {opportunities_path}")

        return {
            "session_dir": session_dir,
            "transcript_path": transcript_path,
            "topics_path": topics_path,
            "opportunities_path": opportunities_path,
        }

    except Exception as e:
        logger.error(f"❌ Phase 1 failed: {e}", exc_info=True)
        raise

def run_phase_2(session_dir):
    try:
        topics_path = os.path.join(session_dir, "topics.txt")
        opportunities_path = os.path.join(session_dir, "opportunities.txt")
        topics_dir = os.path.join(session_dir, "topics")
        scripts_dir = os.path.join(session_dir, "scripts")
        audio_dir = os.path.join(session_dir, "audio")
        os.makedirs(topics_dir, exist_ok=True)
        os.makedirs(scripts_dir, exist_ok=True)
        os.makedirs(audio_dir, exist_ok=True)

        with open(topics_path, "r", encoding="utf-8") as f:
            topics = [line.strip() for line in f if line.strip()]

        with open(opportunities_path, "r", encoding="utf-8") as f:
            opportunities_text = f.read()

        scripts = {}
        audio_files = {}

        for topic in topics:
            logger.info(f"🔍 Querying MedRAG for topic: {topic}")
            facts = query_medrag(topic)
            facts_path = os.path.join(topics_dir, f"{topic.replace(' ', '_')}_facts.txt")
            with open(facts_path, "w", encoding="utf-8") as f:
                f.write(facts)

            logger.info(f"🧠 Generating script for: {topic}")
            script = generate_script(topic, opportunities_text, facts)
            script_path = os.path.join(scripts_dir, f"{topic.replace(' ', '_')}.txt")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script)
            scripts[topic] = script

            logger.info(f"🎧 Generating audio for: {topic}")
            audio_path = os.path.join(audio_dir, f"{topic.replace(' ', '_')}.mp3")
            generate_audio_narration(topic, script, output_path=audio_path)
            audio_files[topic] = audio_path

        logger.info("✅ Phase 2 complete.")
        return {
            "scripts": scripts,
            "audio_files": audio_files,
        }

    except Exception as e:
        logger.error(f"❌ Phase 2 failed: {e}", exc_info=True)
        raise
