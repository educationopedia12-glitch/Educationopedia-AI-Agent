import os
from dotenv import load_dotenv

load_dotenv()


APP_NAME = os.getenv("APP_NAME", "Educationopedia AI Agent")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

MAX_HISTORY_MESSAGES = 10
RAG_INGESTION_BATCH_SIZE = 50