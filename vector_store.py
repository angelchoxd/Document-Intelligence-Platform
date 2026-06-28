import chromadb

from config import COLLECTION_NAME, EMBEDDING_MODEL, TOP_K_RESULTS
from langchain_huggingface import HuggingFaceEmbeddings


def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )


def create_vector_database(chunks):
    embeddings_model = load_embeddings()
    client = chromadb.Client()

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    for i, chunk in enumerate(chunks):
        embedding = embeddings_model.embed_query(chunk["text"])

        collection.add(
            ids=[str(i)],
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[
                {
                    "chunk_id": i + 1,
                    "page": chunk["page"],
                    "document": chunk["document"],
                }
            ],
        )

    return collection, embeddings_model


def retrieve_relevant_chunks(question, collection, embeddings_model):
    question_embedding = embeddings_model.embed_query(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K_RESULTS,
    )

    return results["documents"][0], results["metadatas"][0]