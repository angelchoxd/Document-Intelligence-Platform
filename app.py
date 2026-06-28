import streamlit as st

from document_loader import process_uploaded_documents
from analytics import calculate_document_stats
from vector_store import create_vector_database
from ui.sidebar import render_sidebar
from ui.dashboard import render_dashboard
from ui.document_viewer import render_document_viewer
from ui.chat_interface import render_chat_interface
from ui.search_page import render_search_page
from ui.settings_page import render_settings_page
from ui.export_page import render_export_page


st.set_page_config(
    page_title="Document Intelligence Platform",
    page_icon="📄",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 4rem;
        max-width: 1400px;
    }

    h1 {
        margin-bottom: 0.4rem;
    }

    h2, h3 {
        margin-top: 1.4rem;
    }

    section[data-testid="stSidebar"] {
        min-width: 260px !important;
    }

    div[data-testid="stFileUploader"] {
        padding: 0.75rem;
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.03);
    }

    div[data-testid="stMetric"] {
        padding: 0.7rem;
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.03);
    }

    .stButton > button {
        border-radius: 10px;
        height: 2.6rem;
    }

    textarea {
        border-radius: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("Document Intelligence Platform")
st.write(
    "Upload documents or images, generate summaries, search semantically, "
    "and chat with your files using a local AI model."
)


default_values = {
    "chat_history": [],
    "documents_processed": False,
    "all_document_text": "",
    "all_chunks": [],
    "collection": None,
    "embeddings_model": None,
    "document_names": [],
    "document_stats": {},
    "ai_insights": "",
    "uploaded_file_signature": [],
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value


selected_page, selected_ocr_engine, selected_llm_model = render_sidebar()


if selected_page == "Settings":
    render_settings_page()
    st.stop()


uploaded_files = st.file_uploader(
    "Upload PDF, TXT, PNG, JPG or JPEG files",
    type=["pdf", "txt", "png", "jpg", "jpeg"],
    accept_multiple_files=True
)


current_file_signature = [
    (file.name, file.size, selected_ocr_engine)
    for file in uploaded_files
] if uploaded_files else []


if uploaded_files and current_file_signature != st.session_state.uploaded_file_signature:
    all_document_text, all_chunks, document_names = process_uploaded_documents(
        uploaded_files,
        ocr_engine=selected_ocr_engine
    )

    collection, embeddings_model = create_vector_database(all_chunks)

    stats = calculate_document_stats(
        all_document_text,
        all_chunks,
        document_names
    )

    st.session_state.all_document_text = all_document_text
    st.session_state.all_chunks = all_chunks
    st.session_state.document_names = document_names
    st.session_state.collection = collection
    st.session_state.embeddings_model = embeddings_model
    st.session_state.document_stats = stats
    st.session_state.documents_processed = True
    st.session_state.uploaded_file_signature = current_file_signature
    st.session_state.chat_history = []
    st.session_state.ai_insights = ""

    st.success("Documents processed successfully!")
    st.rerun()


if not st.session_state.documents_processed:
    st.info("Upload one or more PDF/TXT/image files to begin.")
else:
    if selected_page == "Dashboard":
        render_dashboard()

    elif selected_page == "Documents":
        render_document_viewer()

    elif selected_page == "Chat":
        render_chat_interface()

    elif selected_page == "Search":
        render_search_page()

    elif selected_page == "Export":
        render_export_page()