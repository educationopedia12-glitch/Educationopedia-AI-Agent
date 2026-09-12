from fastapi import FastAPI

from app.config import APP_NAME, APP_VERSION, ENVIRONMENT
from app.api.chat import router as chat_router


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
)

app.include_router(chat_router)

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

