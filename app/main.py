from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import APP_NAME, APP_VERSION, ENVIRONMENT

from app.api.chat import router as chat_router
from app.api.rag_sync import router as rag_sync_router 

from app.rag.persistence import restore_chroma_from_storage
from app.rag.vector_store import get_vector_store



@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Restore persistent Chroma data first
    restore_chroma_from_storage()

    # 2. Only then initialize Chroma
    get_vector_store()

    yield


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    lifespan=lifespan,
)

app.include_router(chat_router)
app.include_router(rag_sync_router)


@app.get("/")
async def root():
    return {
        "message": f"{APP_NAME} is running",
        "environment": ENVIRONMENT,
        "version": APP_VERSION,
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }