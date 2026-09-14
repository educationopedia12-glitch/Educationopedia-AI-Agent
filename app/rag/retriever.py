from app.rag.vector_store import get_vector_store


RETRIEVAL_K = 5


def retrieve_documents(query: str):
    results = get_vector_store().similarity_search_with_relevance_scores(
        query=query,
        k=RETRIEVAL_K,
    )

    relevant_documents = []

    for document, score in results:
        if score >= 0.5:
            relevant_documents.append(document)

    return relevant_documents