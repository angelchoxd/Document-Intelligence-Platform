import re
import streamlit as st

from vector_store import search_relevant_chunks


def calculate_match_percentage(distance):
    score = max(0, 1 - distance)
    return round(score * 100, 2)


def highlight_query_terms(text, query):
    words = query.split()

    highlighted_text = text

    for word in words:
        if len(word) < 3:
            continue

        highlighted_text = re.sub(
            f"({re.escape(word)})",
            r"**\1**",
            highlighted_text,
            flags=re.IGNORECASE
        )

    return highlighted_text


def render_search_page():
    st.subheader("Semantic Search")

    query = st.text_input(
        "Search across uploaded documents",
        placeholder="Example: electricity cost, recommendations, risks..."
    )

    document_filter = st.selectbox(
        "Filter by document",
        ["All Documents"] + st.session_state.document_names
    )

    if not query:
        st.info("Enter a search query to find relevant document chunks.")
        return

    documents, metadatas, distances = search_relevant_chunks(
        query,
        st.session_state.collection,
        st.session_state.embeddings_model,
        n_results=5
    )

    filtered_results = []

    for document, metadata, distance in zip(documents, metadatas, distances):
        if document_filter == "All Documents" or metadata["document"] == document_filter:
            filtered_results.append(
                {
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                    "score": calculate_match_percentage(distance),
                }
            )

    st.markdown("### Search Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Results Found", len(filtered_results))

    with col2:
        st.metric("Search Scope", document_filter)

    st.markdown("### Search Results")

    if not filtered_results:
        st.warning("No matching results found for this document filter.")
        return

    for i, result in enumerate(filtered_results):
        metadata = result["metadata"]
        highlighted_text = highlight_query_terms(
            result["text"],
            query
        )

        with st.expander(
            f"Result {i + 1} | "
            f"{metadata['document']} | Page {metadata['page']} | Chunk {metadata['chunk_id']}"
        ):
            st.markdown(highlighted_text)

            st.text_area(
                "Copy chunk text",
                result["text"],
                height=160,
                key=f"copy_search_result_{i}"
            )