from app.rag.documents import create_university_document
from app.rag.loader import load_universities_batch
from app.rag.prepare import prepare_university
from app.rag.vector_store import get_vector_store


def ingest_universities():
    last_document = None
    total_ingested = 0

    while True:
        universities, documents = load_universities_batch(last_document)

        if not universities:
            break

        prepared_universities = [
            prepare_university(university)
            for university in universities
        ]

        rag_documents = [
            create_university_document(university)
            for university in prepared_universities
        ]

        university_ids = [
            university["id"]
            for university in prepared_universities
        ]

        get_vector_store().add_documents(
            documents=rag_documents,
            ids=university_ids,
        )

        total_ingested += len(rag_documents)

        print(
            f"Ingested batch: {len(rag_documents)} | "
            f"Total: {total_ingested}"
        )

        last_document = documents[-1]

    print(f"\nIngestion complete. Total universities: {total_ingested}")


if __name__ == "__main__":
    ingest_universities()