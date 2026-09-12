from app.config import MAX_HISTORY_MESSAGES

conversations = {}

def add_message(conversation_id: str, role: str, content: str):
    if conversation_id not in conversations:
        conversations[conversation_id] = []

    conversations[conversation_id].append(
        {
            "role": role,
            "content": content,
        }
    )

def get_messages(conversation_id: str):
    messages = conversations.get(conversation_id, [])

    return messages[-MAX_HISTORY_MESSAGES:]
