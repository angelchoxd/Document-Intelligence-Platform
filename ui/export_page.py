import streamlit as st

from export_utils import (
    export_chat_as_markdown,
    export_documents_as_markdown,
)


def render_export_page():
    st.subheader("Export")

    st.write("Export chat history or extracted document content.")

    chat_export = export_chat_as_markdown(
        st.session_state.chat_history
    )

    st.download_button(
        label="Download Chat as Markdown",
        data=chat_export,
        file_name="chat_export.md",
        mime="text/markdown",
        use_container_width=True,
    )

    document_export = export_documents_as_markdown(
        st.session_state.document_names,
        st.session_state.all_document_text
    )

    st.download_button(
        label="Download Extracted Documents as Markdown",
        data=document_export,
        file_name="documents_export.md",
        mime="text/markdown",
        use_container_width=True,
    )