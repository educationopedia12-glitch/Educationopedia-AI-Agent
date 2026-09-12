import firebase_admin
from firebase_admin import credentials, firestore

from app.config import RAG_INGESTION_BATCH_SIZE


SERVICE_ACCOUNT_PATH = "firebase-service-account.json"


if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)


db = firestore.client()


def load_universities_batch(last_document=None):
    query = (
        db.collection("universities")
        .order_by("id")
        .limit(RAG_INGESTION_BATCH_SIZE)
    )

    if last_document:
        query = query.start_after(last_document)

    documents = list(query.stream())

    universities = []

    for document in documents:
        university = document.to_dict()
        universities.append(university)

    return universities, documents