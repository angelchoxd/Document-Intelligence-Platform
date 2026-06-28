def calculate_document_stats(all_document_text, all_chunks, document_names):
    words = all_document_text.split()

    return {
        "Documents": len(document_names),
        "Words": len(words),
        "Characters": len(all_document_text),
        "Chunks": len(all_chunks),
    }