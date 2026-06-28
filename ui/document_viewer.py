import streamlit as st

from document_explorer import get_document_chunk_counts, get_chunks_for_document


def render_document_viewer():
    st.subheader("Documents Explorer")

    document_counts = get_document_chunk_counts(
        st.session_state.all_chunks
    )

    if not document_counts:
        st.info("No documents available.")
        return

    selected_document = st.selectbox(
        "Select a document",
        list(document_counts.keys())
    )

    selected_chunks = get_chunks_for_document(
        st.session_state.all_chunks,
        selected_document
    )

    st.markdown("### Document Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Document", selected_document)

    with col2:
        st.metric("Chunks", document_counts[selected_document])

    st.divider()

    st.markdown("### Extracted Chunks")

    for i, chunk in enumerate(selected_chunks):
        with st.expander(
            f"Page {chunk['page']} | Chunk {i + 1}"
        ):
            st.write(chunk["text"])

    st.divider()

    with st.expander("Full Extracted Text From All Documents"):
        st.text_area(
            "",
            st.session_state.all_document_text,
            height=300
        )