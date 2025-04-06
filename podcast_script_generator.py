import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Generate a script for a single topic using student context + facts
def generate_script(topic, opportunities_text, facts_text):
    prompt = ChatPromptTemplate.from_template("""
    You are a medical education podcast host. Your task is to teach the topic: "{topic}"
    to a student who recently completed a study session. 

    First, consider the student's performance summary (opportunities).
    Then, reference the medically accurate facts (below) to ensure you're not hallucinating.

    Deliver a 2-5 minute educational segment (~300-600 words) that's:
    - Clear and efficient
    - Friendly but not overly casual
    - Avoids repetition or tangents
    - Covers the core info relevant to this student's needs

    STUDENT'S PERFORMANCE NOTES:
    {opportunities}

    FACTUAL CONTEXT (from trusted medical sources):
    {facts}

    Begin your podcast segment script now:
    """)
    
    llm = ChatOpenAI(temperature=0.5, model="gpt-4")
    chain = prompt | llm
    response = chain.invoke({
        "topic": topic,
        "opportunities": opportunities_text,
        "facts": facts_text
    })
    return response.content.strip()

# Orchestrate per-topic script generation
def generate_all_scripts(session_dir):
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
