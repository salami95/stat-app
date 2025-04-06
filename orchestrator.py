import logging
from generate_audio import transcribe_audio
from topic_processor import extract_topics
from build_medrag_index import query_medrag
from education_expert import analyze_student_performance
from medical_expert import generate_clarified_explanations
from podcast_script_generator import generate_podcast_script
from eleven_labs_scribe import generate_audio_narration

logger = logging.getLogger(__name__)

def orchestrate_initial_phase(audio_path):
    try:
        logger.info("Starting transcription...")
        transcript = transcribe_audio(audio_path)
        logger.info("Transcription complete.")

        logger.info("Extracting topics...")
        topics = extract_topics(transcript)
        logger.info(f"Topics extracted: {topics}")

        logger.info("Querying MedRAG for each topic...")
        grounded_info = {
            topic: query_medrag(topic) for topic in topics
        }
        logger.info("MedRAG grounding complete.")

        logger.info("Analyzing student performance...")
        performance_report = analyze_student_performance(transcript)
        logger.info("Performance analysis complete.")

        logger.info("Generating expert explanations...")
        expert_explanations = {
            topic: generate_clarified_explanations(topic, grounded_info[topic]) for topic in topics
        }
        logger.info("Explanations complete.")

        logger.info("Generating podcast scripts...")
        scripts = {
            topic: generate_podcast_script(topic, expert_explanations[topic]) for topic in topics
        }
        logger.info("Scripts generated.")

        logger.info("Generating audio narrations...")
        audio_files = {
            topic: generate_audio_narration(topic, scripts[topic]) for topic in topics
        }
        logger.info("Audio narration complete.")

        return {
            "transcript": transcript,
            "topics": topics,
            "performance_report": performance_report,
            "scripts": scripts,
            "audio_files": audio_files,
        }

    except Exception as e:
        logger.error(f"Error during orchestration: {e}", exc_info=True)
        raise
