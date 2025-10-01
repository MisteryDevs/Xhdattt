from tnc import logger

# Dictionary to store chatbot status per chat_id
chatbot_status = {}  # True = enabled, False = disabled

# -----------------------------
# Enable chatbot
# -----------------------------
def enable_chatbot(chat_id: int):
    chatbot_status[chat_id] = True
    logger.info(f"Chatbot enabled for chat {chat_id}")

# -----------------------------
# Disable chatbot
# -----------------------------
def disable_chatbot(chat_id: int):
    chatbot_status[chat_id] = False
    logger.info(f"Chatbot disabled for chat {chat_id}")

# -----------------------------
# Check chatbot status
# -----------------------------
def is_chatbot_enabled(chat_id: int) -> bool:
    # Default: enabled if not set
    return chatbot_status.get(chat_id, True)
