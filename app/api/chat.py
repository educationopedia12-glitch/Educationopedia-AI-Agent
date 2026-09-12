from fastapi import APIRouter

from app.llm.service import llm
from app.memory.context import build_context
from app.memory.store import add_message, get_messages
from app.schemas.chat import ChatRequest


router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):
    history = get_messages(request.conversationId)

    context = build_context(
        history,
        request.message,
    )

    response = llm.invoke(context)

    add_message(
        request.conversationId,
        "user",
        request.message,
    )

    add_message(
        request.conversationId,
        "assistant",
        response.content,
    )

    return {
        "message": response.content,
        "conversationId": request.conversationId,
    }