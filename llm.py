import ollama

from config import OLLAMA_MODEL
from prompts import (
    question_answering_prompt,
    summary_prompt,
    insights_prompt,
)


def _generate(prompt: str) -> str:
    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"]


def ask_question(question, context):
    prompt = question_answering_prompt(question, context)
    return _generate(prompt)


def generate_summary(document_text):
    prompt = summary_prompt(document_text)
    return _generate(prompt)


def generate_ai_insights(document_text):
    prompt = insights_prompt(document_text)
    return _generate(prompt)