import streamlit as st

from vector_store import retrieve_relevant_chunks
from llm import ask_question
from ui.citations import render_sources


def build_chat_memory(chat_history, max_messages=6):
    recent_messages = chat_history[-max_messages:]

    memory = ""

    for message in recent_messages:
        role = message["role"]
        content = message["content"]
        memory += f"{role.upper()}: {content}\n"

    return memory


def render_chat_interface():
    st.subheader("Chat With Your Documents")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask anything about the uploaded documents...")

    if prompt:
        st.session_state.chat_history.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        retrieved_chunks, metadata = retrieve_relevant_chunks(
            prompt,
            st.session_state.collection,
            st.session_state.embeddings_model
        )

        document_context = "\n\n".join(retrieved_chunks)

        chat_memory = build_chat_memory(
            st.session_state.chat_history
        )

        full_context = f"""
Previous conversation:
{chat_memory}

Relevant document context:
{document_context}
"""

        with st.spinner("Thinking..."):
            answer = ask_question(prompt, full_context)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)
            render_sources(metadata)