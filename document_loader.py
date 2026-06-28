from pypdf import PdfReader

from config import CHUNK_SIZE, CHUNK_OVERLAP
from langchain_text_splitters import RecursiveCharacterTextSplitter


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
                    "text": page_text,
                }
            )

    return text, page_texts


def read_txt(file):
    text = file.read().decode("utf-8")

    page_texts = [
        {
            "page": 1,
            "text": text,
        }
    ]

    return text, page_texts


def read_uploaded_file(file):
    if file.type == "application/pdf":
        return read_pdf(file)

    return read_txt(file)


def split_text_with_pages(page_texts, document_name):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
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
                    "page": page_number,
                    "document": document_name,
                }
            )

    return chunks


def process_uploaded_documents(uploaded_files):
    all_text = ""
    all_chunks = []
    document_names = []

    for file in uploaded_files:
        document_name = file.name
        document_names.append(document_name)

        document_text, page_texts = read_uploaded_file(file)

        all_text += f"\n\n--- Document: {document_name} ---\n"
        all_text += document_text

        chunks = split_text_with_pages(page_texts, document_name)
        all_chunks.extend(chunks)

    return all_text, all_chunks, document_names