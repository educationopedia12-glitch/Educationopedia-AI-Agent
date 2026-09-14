from langchain_chroma import Chroma

from app.config import CHROMA_PERSIST_DIRECTORY
from app.rag.embeddings import embeddings


COLLECTION_NAME = "educationopedia_universities"

_vector_store = None


def get_vector_store():
    global _vector_store

    if _vector_store is None:
        _vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_PERSIST_DIRECTORY,
        )

    return _vector_store