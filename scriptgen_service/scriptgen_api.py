from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

app = Flask(__name__)
llm = ChatOpenAI(model="gpt-4", temperature=0.5)

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

script_chain = script_prompt | llm | (lambda output: output.content.strip())

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic")
    notes = data.get("notes", [])

    if not topic or not isinstance(notes, list):
        return jsonify({"error": "Missing or invalid input"}), 400

    try:
        joined_notes = "\n".join(notes)
        script = script_chain.invoke({"topic": topic, "notes": joined_notes})
        return jsonify({"script": script})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8003)
