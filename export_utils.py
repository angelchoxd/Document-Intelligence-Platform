def export_chat_as_markdown(chat_history):
    content = "# Chat Export\n\n"

    for message in chat_history:
        role = message["role"].capitalize()
        content += f"## {role}\n\n"
        content += message["content"] + "\n\n"

    return content


def export_summary_as_markdown(summary_text):
    return f"# AI Summary\n\n{summary_text}"


def export_documents_as_markdown(document_names, document_text):
    content = "# Uploaded Documents\n\n"

    for name in document_names:
        content += f"- {name}\n"

    content += "\n# Extracted Text\n\n"
    content += document_text

    return content