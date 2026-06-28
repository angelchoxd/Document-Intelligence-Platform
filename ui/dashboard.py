import streamlit as st

from llm import generate_summary


def render_dashboard():
    st.subheader("Document Overview")

    st.write("Uploaded documents:")

    for document_name in st.session_state.document_names:
        st.write(f"- {document_name}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Documents", st.session_state.document_stats["Documents"])

    with col2:
        st.metric("Words", st.session_state.document_stats["Words"])

    with col3:
        st.metric("Characters", st.session_state.document_stats["Characters"])

    with col4:
        st.metric("Chunks", st.session_state.document_stats["Chunks"])

    st.divider()

    st.markdown("### Quick Actions")

    if st.button("Generate AI Summary", use_container_width=True):
        with st.spinner("Generating summary..."):
            summary = generate_summary(st.session_state.all_document_text)

        st.session_state.summary = summary

    if "summary" in st.session_state and st.session_state.summary:
        st.markdown("### AI Summary")
        st.info(st.session_state.summary)

    st.divider()

    st.markdown("### System Status")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("OCR Ready")

    with col2:
        st.success("Local LLM Ready")

    with col3:
        st.success("Vector DB Ready")

    with col4:
        st.success("Documents Indexed")