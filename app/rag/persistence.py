import shutil
from pathlib import Path

from google.cloud import storage

from app.config import (
    CHROMA_PERSIST_DIRECTORY,
    CHROMA_STORAGE_BUCKET,
    ENVIRONMENT,
)


CHROMA_STORAGE_PREFIX = "chroma/"


def restore_chroma_from_storage():
    if ENVIRONMENT != "production":
        print("Skipping Chroma restore in development.")
        return

    if not CHROMA_STORAGE_BUCKET:
        raise ValueError(
            "CHROMA_STORAGE_BUCKET is required in production."
        )

    chroma_directory = Path(CHROMA_PERSIST_DIRECTORY)

    # Start with a clean working directory
    if chroma_directory.exists():
        shutil.rmtree(chroma_directory)

    chroma_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    storage_client = storage.Client()

    bucket = storage_client.bucket(
        CHROMA_STORAGE_BUCKET
    )

    blobs = list(
        bucket.list_blobs(
            prefix=CHROMA_STORAGE_PREFIX
        )
    )

    # First production deployment:
    # no Chroma backup exists yet.
    if not blobs:
        print(
            "No Chroma backup found in Cloud Storage. "
            "Starting with an empty Chroma database."
        )
        return

    for blob in blobs:
        if blob.name.endswith("/"):
            continue

        relative_path = blob.name[
            len(CHROMA_STORAGE_PREFIX):
        ]

        destination = (
            chroma_directory / relative_path
        )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        blob.download_to_filename(
            str(destination)
        )

    print(
        f"Restored Chroma from Cloud Storage "
        f"to {chroma_directory}"
    )


def backup_chroma_to_storage():
    if ENVIRONMENT != "production":
        print("Skipping Chroma backup in development.")
        return

    if not CHROMA_STORAGE_BUCKET:
        raise ValueError(
            "CHROMA_STORAGE_BUCKET is required in production."
        )

    chroma_directory = Path(CHROMA_PERSIST_DIRECTORY)

    if not chroma_directory.exists():
        raise ValueError(
            f"Chroma directory does not exist: {chroma_directory}"
        )

    storage_client = storage.Client()

    bucket = storage_client.bucket(
        CHROMA_STORAGE_BUCKET
    )

    for file_path in chroma_directory.rglob("*"):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(
            chroma_directory
        )

        blob_name = (
            f"{CHROMA_STORAGE_PREFIX}{relative_path.as_posix()}"
        )

        blob = bucket.blob(blob_name)

        blob.upload_from_filename(
            str(file_path)
        )

    print(
        f"Backed up Chroma from {chroma_directory} "
        f"to Cloud Storage"
    )