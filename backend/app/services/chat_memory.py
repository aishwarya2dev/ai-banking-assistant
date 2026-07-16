conversation_history = []

def get_history():
    return conversation_history

def add_message(user: str, assistant: str):
    conversation_history.append(
        {
            "user": user,
            "assistant": assistant
        }
    )

    # Keep only the last 5 conversation turns
    if len(conversation_history) > 5:
        conversation_history.pop(0)


def clear_history():
    conversation_history.clear()