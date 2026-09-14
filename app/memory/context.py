from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)

from app.agent.system_prompt import get_system_message
from app.rag.context import format_retrieved_context
from app.rag.retriever import retrieve_documents


def build_context(messages, current_message: str):
    context = [
        get_system_message()
    ]

    retrieved_documents = retrieve_documents(current_message)

    if retrieved_documents:
        retrieved_context = format_retrieved_context(retrieved_documents)

        context.append(
            SystemMessage(
                content=(
                    "The following is verified Educationopedia knowledge retrieved "
                    "for the current user question. Use it when relevant. Do not "
                    "invent information that is not present in the retrieved "
                    "knowledge.\n\n"
                    f"{retrieved_context}"
                )
            )
        )

    for message in messages:
        if message["role"] == "user":
            context.append(
                HumanMessage(content=message["content"])
            )

        elif message["role"] == "assistant":
            context.append(
                AIMessage(content=message["content"])
            )

    context.append(
        HumanMessage(content=current_message)
    )

    return context