from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

analyze_prompt = PromptTemplate.from_template(
    """
    You are an education expert. Analyze this transcript for the learner's performance
    across the topics provided. Identify strengths, weaknesses, knowledge gaps,
    and opportunities for improvement in a detailed but concise summary.

    Transcript:
    ---
    {transcript}
    ---

    Topics:
    - {topics}

    Summary:
    """
)

llm = ChatOpenAI(model="gpt-4", temperature=0.3)

analyze_chain = analyze_prompt | llm | (lambda output: output.content.strip())

def analyze_student_performance(transcript, topics):
    return analyze_chain.invoke({"transcript": transcript, "topics": ", ".join(topics)})
