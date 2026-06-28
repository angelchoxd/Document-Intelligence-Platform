import streamlit as st


def render_settings_page():
    st.subheader("Settings")

    st.markdown("### Current Configuration")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "LLM Model",
            st.session_state.get("selected_llm_model", "qwen3:4b")
        )

    with col2:
        st.metric(
            "OCR Engine",
            st.session_state.get("selected_ocr_engine", "Auto")
        )

    with col3:
        st.metric("Vector DB", "ChromaDB")

    st.markdown("### About This Workspace")

    st.info(
        "This application runs locally and uses uploaded documents to build a "
        "searchable knowledge base with embeddings, ChromaDB, OCR and local LLM models."
    )

    st.markdown("### Supported Inputs")

    st.write("- PDF documents")
    st.write("- TXT files")
    st.write("- PNG / JPG / JPEG images with OCR")

    st.markdown("### Notes")

    st.write("- The selected LLM and OCR engine can be changed from the sidebar.")
    st.write("- Uploaded documents are processed locally.")
    st.write("- Search and chat answers are based on retrieved document chunks.")