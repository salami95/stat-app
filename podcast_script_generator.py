from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

script_prompt = PromptTemplate.from_template(
    """
    Write an educational podcast script about the topic below using only the factual notes provided.
    Keep the tone friendly, informative, and engaging—like a solo podcast narrator teaching students.

    Topic: {topic}

    Notes:
    ---
    {notes}
    ---

    Script:
    """
)

llm = ChatOpenAI(model="gpt-4", temperature=0.5)

script_chain = script_prompt | llm | (lambda output: output.content.strip())

def generate_podcast_scripts(topic_facts):
    return {
        topic: script_chain.invoke({
            "topic": topic,
            "notes": "\n".join([str(n) for n in facts])
        })
        for topic, facts in topic_facts.items()
    }
