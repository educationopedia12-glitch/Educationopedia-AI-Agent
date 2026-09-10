from fastapi import APIRouter

from app.llm.service import llm
from app.schemas.chat import ChatRequest


router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):
    response = llm.invoke(request.message)

    return {
        "message": response.content
    }