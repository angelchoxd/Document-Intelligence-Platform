def get_document_chunk_counts(chunks):
    counts = {}

    for chunk in chunks:
        document_name = chunk["document"]

        if document_name not in counts:
            counts[document_name] = 0

        counts[document_name] += 1

    return counts


def get_chunks_for_document(chunks, document_name):
    return [
        chunk for chunk in chunks
        if chunk["document"] == document_name
    ]