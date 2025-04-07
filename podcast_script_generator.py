# podcast_script_generator.py

import os
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


# Generate a script for a single topic using student context + grounded facts
def generate_script(topic: str, opportunities_text: str, facts_text: str) -> str:
    prompt = ChatPromptTemplate.from_template("""
You are the host of a medical education podcast. Your job is to teach the topic: "{topic}" to a student who recently completed a self-guided study session.

Use the student's performance summary to guide tone and focus. Then use the factual context to build your episode. Avoid hallucinations. Do not include information not found in the factual context.

Create a 2–5 minute segment (~300–600 words) that is:
- Friendly but focused
- Clear, concise, and medically accurate
- Structured with a brief intro, core teaching, and a single key takeaway
- Designed for students reviewing high-yield content for exams

STUDENT PERFORMANCE NOTES:
{opportunities}

FACTUAL CONTEXT (trusted RAG output):
{facts}

Start your segment below:
""")

    llm = ChatOpenAI(temperature=0.5, model="gpt-4")
    chain = prompt | llm

    response = chain.invoke({
        "topic": topic,
        "opportunities": opportunities_text,
        "facts": facts_text
    })

    output = response.content.strip()
    print(f"[LENGTH] Script for '{topic}' is {len(output.split())} words")
    return output


# Orchestrate per-topic podcast generation
def generate_all_scripts(session_dir: str) -> str:
    topics_file = os.path.join(session_dir, "topics.txt")
    topics_dir = os.path.join(session_dir, "topics")
    output_dir = os.path.join(session_dir, "scripts")
    os.makedirs(output_dir, exist_ok=True)

    with open(topics_file, "r", encoding="utf-8") as f:
        topics = [line.strip() for line in f if line.strip()]

    with open(os.path.join(session_dir, "opportunities.txt"), "r", encoding="utf-8") as f:
        opportunities_text = f.read()

    for topic in topics:
        facts_path = os.path.join(topics_dir, f"{topic.replace(' ', '_')}_facts.txt")
        if not os.path.exists(facts_path):
            print(f"[WARN] Missing facts for topic: {topic}")
            continue

        with open(facts_path, "r", encoding="utf-8") as f:
            facts_text = f.read()

        print(f"[INFO] Generating script for topic: {topic}")
        script = generate_script(topic, opportunities_text, facts_text)

        script_path = os.path.join(output_dir, f"{topic.replace(' ', '_')}.txt")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)

    print(f"[INFO] All topic scripts written to: {output_dir}")
    return output_dir


# Compatibility alias for orchestrator.py
generate_podcast_script = generate_all_scripts
