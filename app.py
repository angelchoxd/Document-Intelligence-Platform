import os
import shutil
import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
import ollama


st.set_page_config(
    page_title="Document Intelligence Platform",
    page_icon="📄",
    layout="wide"
)

st.title("Document Intelligence Platform")
st.write(
    "Upload documents, generate summaries, search semantically, "
    "and chat with your files using a local AI model."
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "collection" not in st.session_state:
    st.session_state.collection = None

if "embeddings_model" not in st.session_state:
    st.session_state.embeddings_model = None

if "document_name" not in st.session_state:
    st.session_state.document_name = ""

if "document_stats" not in st.session_state:
    st.session_state.document_stats = {}

if "ai_insights" not in st.session_state:
    st.session_state.ai_insights = ""


with st.sidebar:
    st.header("Controls")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    if st.button("Reset Document", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.document_processed = False
        st.session_state.document_text = ""
        st.session_state.chunks = []
        st.session_state.collection = None
        st.session_state.embeddings_model = None
        st.session_state.document_name = ""
        st.session_state.document_stats = {}
        st.session_state.ai_insights = ""

        if os.path.exists("vector_db"):
            shutil.rmtree("vector_db")

        st.rerun()

    st.divider()
    st.caption("Local AI Model: Qwen3 4B")
    st.caption("Vector DB: ChromaDB")
    st.caption("Embedding Model: all-MiniLM-L6-v2")


uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf", "txt"]
)


def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    page_texts = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"
            page_texts.append(
                {
                    "page": page_number,
                    "text": page_text
                }
            )

    return text, page_texts


def read_txt(file):
    text = file.read().decode("utf-8")
    page_texts = [
        {
            "page": 1,
            "text": text
        }
    ]

    return text, page_texts


def split_text_with_pages(page_texts):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = []

    for page in page_texts:
        page_number = page["page"]
        page_text = page["text"]

        page_chunks = splitter.split_text(page_text)

        for chunk in page_chunks:
            chunks.append(
                {
                    "text": chunk,
                    "page": page_number
                }
            )

    return chunks


def calculate_document_stats(document_text, chunks):
    words = document_text.split()
    characters = len(document_text)
    word_count = len(words)
    chunk_count = len(chunks)

    return {
        "Words": word_count,
        "Characters": characters,
        "Chunks": chunk_count,
    }


@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def create_vector_database(chunks):
    embeddings_model = load_embeddings()
    client = chromadb.Client()

    try:
        client.delete_collection("documents")
    except:
        pass

    collection = client.create_collection(name="documents")

    for i, chunk in enumerate(chunks):
        embedding = embeddings_model.embed_query(chunk["text"])

        collection.add(
            ids=[str(i)],
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[
                {
                    "chunk_id": i + 1,
                    "page": chunk["page"]
                }
            ]
        )

    return collection, embeddings_model


def retrieve_relevant_chunks(question, collection, embeddings_model):
    question_embedding = embeddings_model.embed_query(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    retrieved_chunks = results["documents"][0]
    retrieved_metadata = results["metadatas"][0]

    return retrieved_chunks, retrieved_metadata


def ask_ollama(question, context):
    prompt = f"""
You are an AI assistant for document question answering.

Answer the user's question using only the context below.
If the answer is not in the context, say that the document does not contain that information.
Keep the answer clear and concise.
Do not show your thinking process.

Context:
{context}

Question:
{question}

Final answer:
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


def generate_summary(text):
    prompt = f"""
You are an AI assistant that summarizes documents.

Create a clear and professional summary of the document below.
Use bullet points.
Focus on key facts, numbers, recommendations, risks, and important conclusions.
Do not show your thinking process.

Document:
{text}

Summary:
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


def generate_ai_insights(text):
    prompt = f"""
You are an AI assistant that extracts insights from documents.

Analyze the document below and return:
- Main topics
- Important numbers or KPIs
- Key risks
- Recommendations
- Important dates if any

Keep the answer structured and concise.
Do not show your thinking process.

Document:
{text}

AI Insights:
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


if uploaded_file is not None and not st.session_state.document_processed:

    st.session_state.document_name = uploaded_file.name

    if uploaded_file.type == "application/pdf":
        document_text, page_texts = read_pdf(uploaded_file)
    else:
        document_text, page_texts = read_txt(uploaded_file)

    chunks = split_text_with_pages(page_texts)
    stats = calculate_document_stats(document_text, chunks)

    collection, embeddings_model = create_vector_database(chunks)

    st.session_state.document_text = document_text
    st.session_state.chunks = chunks
    st.session_state.collection = collection
    st.session_state.embeddings_model = embeddings_model
    st.session_state.document_stats = stats
    st.session_state.document_processed = True

    st.success("Document processed successfully!")
    st.rerun()


if st.session_state.document_processed:

    st.subheader("Document Overview")

    st.write(f"Uploaded document: **{st.session_state.document_name}**")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Words", st.session_state.document_stats["Words"])

    with col2:
        st.metric("Characters", st.session_state.document_stats["Characters"])

    with col3:
        st.metric("Chunks", st.session_state.document_stats["Chunks"])

    st.divider()

    col_summary, col_insights = st.columns(2)

    with col_summary:
        if st.button("Generate AI Summary", use_container_width=True):
            with st.spinner("Generating summary..."):
                summary = generate_summary(st.session_state.document_text)

            st.markdown("### AI Summary")
            st.write(summary)

    with col_insights:
        if st.button("Generate AI Insights", use_container_width=True):
            with st.spinner("Extracting insights..."):
                insights = generate_ai_insights(st.session_state.document_text)

            st.session_state.ai_insights = insights

    if st.session_state.ai_insights:
        st.markdown("### AI Insights")
        st.write(st.session_state.ai_insights)

    with st.expander("Preview Extracted Text"):
        st.text_area(
            "",
            st.session_state.document_text,
            height=250
        )

    with st.expander("Preview Chunks with Page References"):
        for i, chunk in enumerate(st.session_state.chunks):
            st.markdown(f"### Chunk {i + 1} | Page {chunk['page']}")
            st.text_area(
                "",
                chunk["text"],
                height=170,
                key=f"chunk_preview_{i}"
            )

    st.divider()

    st.subheader("Chat With Your Document")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask anything about the uploaded document...")

    if prompt:

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": prompt
            }
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
            answer = ask_ollama(prompt, context)

        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

            with st.expander("Sources"):
                for item in metadata:
                    st.write(
                        f"Chunk {item['chunk_id']} | Page {item['page']}"
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
    st.info("Upload a PDF or TXT document to begin.")