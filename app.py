import os
import shutil
import streamlit as st

from document_loader import process_uploaded_documents
from analytics import calculate_document_stats
from vector_store import create_vector_database, retrieve_relevant_chunks
from llm import ask_question, generate_summary, generate_ai_insights


st.set_page_config(
    page_title="Document Intelligence Platform",
    page_icon="📄",
    layout="wide",
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


with st.sidebar:
    st.header("Controls")

    selected_ocr_engine = st.selectbox(
        "OCR Engine",
        ["GLM-OCR", "DeepSeek-OCR", "Auto"],
        index=0,
        key="selected_ocr_engine",
    )

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("Reset Documents", use_container_width=True):
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

        st.rerun()

    st.divider()
    st.caption("Local AI: Qwen3 4B")
    st.caption("Embeddings: all-MiniLM-L6-v2")
    st.caption("Vector DB: ChromaDB")


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


if st.session_state.documents_processed:
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

    col_summary, col_insights = st.columns(2)

    with col_summary:
        if st.button("Generate AI Summary", use_container_width=True):
            with st.spinner("Generating summary..."):
                summary = generate_summary(st.session_state.all_document_text)

            st.markdown("### AI Summary")
            st.write(summary)

    with col_insights:
        if st.button("Generate AI Insights", use_container_width=True):
            with st.spinner("Extracting insights..."):
                insights = generate_ai_insights(st.session_state.all_document_text)

            st.session_state.ai_insights = insights

    if st.session_state.ai_insights:
        st.markdown("### AI Insights")
        st.write(st.session_state.ai_insights)

    with st.expander("Preview Extracted Text"):
        st.text_area("", st.session_state.all_document_text, height=250)

    with st.expander("Preview Chunks with Document and Page References"):
        for i, chunk in enumerate(st.session_state.all_chunks):
            st.markdown(
                f"### Chunk {i + 1} | Document: {chunk['document']} | Page {chunk['page']}"
            )
            st.text_area(
                "",
                chunk["text"],
                height=170,
                key=f"chunk_preview_{i}"
            )

    st.divider()

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

        context = "\n\n".join(retrieved_chunks)

        with st.spinner("Thinking..."):
            answer = ask_question(prompt, context)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

            with st.expander("Sources"):
                for item in metadata:
                    st.write(
                        f"Document: {item['document']} | Page {item['page']} | Chunk {item['chunk_id']}"
                    )

            with st.expander("Retrieved Context"):
                for i, chunk in enumerate(retrieved_chunks):
                    st.markdown(f"#### Retrieved Chunk {i + 1}")
                    st.text_area(
                        "",
                        chunk,
                        height=170,
                        key=f"retrieved_{i}_{len(st.session_state.chat_history)}"
                    )

else:
    st.info("Upload one or more PDF/TXT/image files to begin.")