import os
import shutil
import streamlit as st


def reset_documents():
    st.session_state.chat_history = []
    st.session_state.documents_processed = False
    st.session_state.all_document_text = ""
    st.session_state.all_chunks = []
    st.session_state.collection = None
    st.session_state.embeddings_model = None
    st.session_state.document_names = []
    st.session_state.document_stats = {}
    st.session_state.ai_insights = ""
    st.session_state.uploaded_file_signature = []

    if os.path.exists("vector_db"):
        shutil.rmtree("vector_db")


def render_sidebar():
    with st.sidebar:
        st.header("Workspace")

        selected_page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Documents",
                "Chat",
                "Search",
                "Export",
                "Settings",
            ],
            index=0,
        )

        st.divider()

        st.header("Controls")

        selected_llm_model = st.selectbox(
            "LLM Model",
            [
                "Qwen3 4B",
                "Llama 3.2 3B",
            ],
            index=0,
        )

        selected_ocr_engine = st.selectbox(
            "OCR Engine",
            [
                "Auto",
                "GLM-OCR",
                "DeepSeek-OCR",
            ],
            index=0,
            key="selected_ocr_engine",
        )

        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        if st.button("Reset Documents", use_container_width=True):
            reset_documents()
            st.rerun()

        st.divider()

        st.caption(f"LLM: {selected_llm_model}")
        st.caption(f"OCR: {selected_ocr_engine}")
        st.caption("Embeddings: all-MiniLM-L6-v2")
        st.caption("Vector DB: ChromaDB")

    return selected_page, selected_ocr_engine, selected_llm_model