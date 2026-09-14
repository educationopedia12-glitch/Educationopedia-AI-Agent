def format_retrieved_context(documents):
    if not documents:
        return ""

    context_parts = []

    for index, document in enumerate(documents, start=1):
        context_parts.append(
            f"Retrieved Educationopedia Knowledge {index}:\n"
            f"{document.page_content}"
        )

    return "\n\n---\n\n".join(context_parts)