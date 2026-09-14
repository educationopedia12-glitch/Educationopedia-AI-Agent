from app.rag.documents import create_university_document
from app.rag.prepare import prepare_university
from app.rag.vector_store import get_vector_store
from app.rag.persistence import backup_chroma_to_storage
from app.rag.sync_lock import rag_sync_lock


def sync_university(university: dict):
    prepared_university = prepare_university(university)

    university_id = prepared_university.get("id")

    if not university_id:
        raise ValueError("University is missing a stable 'id' field.")

    document = create_university_document(prepared_university)

    try:
        with rag_sync_lock:
            vector_store = get_vector_store()

            existing = vector_store.get(ids=[university_id])

            if existing["ids"]:
                vector_store.update_documents(
                    ids=[university_id],
                    documents=[document],
                )

                action = "updated"
                print(f"Updated university: {university_id}")

            else:
                vector_store.add_documents(
                    documents=[document],
                    ids=[university_id],
                )

                action = "created"
                print(f"Added university: {university_id}")

            backup_chroma_to_storage()

            return action

    except Exception as error:
        print(f"Failed to sync university {university_id}: {error}")
        raise


def delete_university(university_id: str):
    if not university_id:
        raise ValueError("University ID is required.")

    try:
        with rag_sync_lock:
            vector_store = get_vector_store()

            vector_store.delete(ids=[university_id])

            print(f"Deleted university vector: {university_id}")

            backup_chroma_to_storage()

            return "deleted"

    except Exception as error:
        print(f"Failed to delete university vector {university_id}: {error}")
        raise