import streamlit as st
import ollama

from config import DEFAULT_LLM_MODEL
from prompts import (
    question_answering_prompt,
    summary_prompt,
)


def get_selected_llm_model():
    return st.session_state.get(
        "selected_llm_model",
        DEFAULT_LLM_MODEL
    )


def _generate(prompt: str) -> str:
    response = ollama.chat(
        model=get_selected_llm_model(),
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
    prompt = f"""
You are an AI Document Analyst.

Analyze the following document and produce a professional markdown report.

Document:

{document_text}
"""

    return _generate(prompt)