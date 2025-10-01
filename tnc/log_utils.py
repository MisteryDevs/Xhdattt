import logging
from tnc import logger_setup

logger = logger_setup.logger

async def log_message_details(message):
    """
    Logs detailed info about who sent the message, in which chat,
    and a short preview of the message.
    """
    try:
        user = message.from_user
        chat = message.chat

        user_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        user_id = user.id
        chat_name = chat.title or chat.first_name or "Private Chat"
        chat_id = chat.id
        msg_preview = (message.text or "")[:50]  # Preview first 50 chars

        logger.info(
            f"[CHAT] '{chat_name}' ({chat_id}) | [USER] {user_name} ({user_id}) | [MSG] {msg_preview}"
        )
    except Exception as e:
        logger.warning(f"Failed to log message details: {e}")


async def log_event(event_name: str, message=None, extra=None):
    """
    Logs generic events such as AFK triggers, reactions, chatbot toggles, voice messages, etc.

    Args:
        event_name (str): Name of the event
        message (Optional[pyrogram.types.Message]): The message triggering the event
        extra (Optional[str]): Extra info for logging
    """
    try:
        details = ""
        if message:
            user = message.from_user
            chat = message.chat
            user_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
            chat_name = chat.title or chat.first_name or "Private Chat"
            details = f"[CHAT: {chat_name} | USER: {user_name} ({user.id})]"

        extra_info = f" | {extra}" if extra else ""
        logger.info(f"[EVENT: {event_name}] {details}{extra_info}")
    except Exception as e:
        logger.warning(f"Failed to log event '{event_name}': {e}")