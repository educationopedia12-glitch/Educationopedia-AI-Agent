from langchain_core.messages import AIMessage, HumanMessage

from app.agent.system_prompt import get_system_message


def build_context(messages, current_message: str):
    context = [
        get_system_message()
    ]

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