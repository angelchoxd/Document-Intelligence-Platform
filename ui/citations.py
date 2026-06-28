import streamlit as st


def render_sources(metadata):
    st.markdown("### Sources")

    for i, item in enumerate(metadata, start=1):
        with st.expander(
            f"Source {i} | {item['document']} | Page {item['page']} | Chunk {item['chunk_id']}"
        ):
            st.write(f"Document: {item['document']}")
            st.write(f"Page: {item['page']}")
            st.write(f"Chunk: {item['chunk_id']}")


def render_retrieved_context(chunks):
    st.markdown("### Retrieved Context")

    for i, chunk in enumerate(chunks, start=1):
        with st.expander(f"Retrieved Chunk {i}"):
            st.text_area(
                "",
                chunk,
                height=170,
                key=f"retrieved_context_{i}"
            )