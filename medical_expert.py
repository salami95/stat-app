# medical_expert.py

import os
import sys
from langchain_community.chains import RetrievalQA
from langchain_community.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_models import ChatOpenAI


def load_file(filepath: str) -> str:
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"❌ File not found: {filepath}")
    with open(filepath, 'r') as f:
        return f.read()


def generate_clarified_explanations(transcription_path: str, education_path: str) -> str:
    print(f"📄 Loading transcription from: {transcription_path}")
    transcription_text = load_file(transcription_path)

    print(f"📄 Loading education expert analysis from: {education_path}")
    education_text = load_file(education_path)

    # Combine transcript and education expert reflection
    combined_input = transcription_text + "\n\n# Education Analysis\n\n" + education_text

    print("📦 Loading MedRAG FAISS index...")
    retriever = FAISS.load_local(
        "./rag/medrag_index",
        OpenAIEmbeddings(),
        index_name="index"
    ).as_retriever()

    # Construct the RAG prompt
    prompt_template = PromptTemplate.from_template(
        """
You are a medical expert with deep understanding of the complexities of medicine.
You are provided with a text file containing an educational evaluation from a medical student's study session that outlines pitfalls, mistakes, and gaps in knowledge.

Your task is to supply detailed, comprehensive information addressing these gaps,
ensuring the student has all the necessary content to answer similar questions correctly in the future.

Additionally, reinforce the topics the student answered correctly to aid in spaced repetition,
as the student will be reviewing the content you provide on a regular basis.

Use only the context provided to support your answer.
Deliver your response as plain text with no extra formatting.

STUDENT STUDY SESSION:
{question}
"""
    )

    print("🧠 Initializing LangChain RAG pipeline...")
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model="gpt-4", temperature=0.7),
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt_template}
    )

    print("🤖 Generating RAG-based explanation...")
    result = qa_chain.run(combined_input)
    return result


def main():
    if len(sys.argv) < 3:
        print("❌ Usage: python3 medical_expert.py <transcription_path> <education_analysis_path>")
        sys.exit(1)

    transcription_path = sys.argv[1]
    education_path = sys.argv[2]

    try:
        final_output = generate_clarified_explanations(transcription_path, education_path)

        base_name = os.path.splitext(os.path.basename(transcription_path))[0].replace("_transcription", "")
        output_path = os.path.join(os.path.dirname(transcription_path), f"{base_name}_medical_expert_analysis.txt")

        with open(output_path, 'w') as f:
            f.write(final_output)

        print(f"✅ Saved medical expert analysis to: {output_path}")

    except Exception as e:
        print(f"❌ General error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
