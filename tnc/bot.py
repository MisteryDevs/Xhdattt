from pyrogram import filters
from tnc import app, logger
from tnc.afk_manager import afk_auto_reply
from tnc.human_reply import get_human_reply
from tnc.reactions import send_reaction
from tnc.toggle import is_chatbot_enabled
from tnc.config import BOT_OWNER, FAKE_TYPING_DELAY
import asyncio

# -----------------------------
# Message Handler (Private & Group)
# -----------------------------
@app.on_message(filters.private | filters.group)
async def handle_message(client, message):
    user_id = message.from_user.id if message.from_user else None
    chat_id = message.chat.id
    text = message.text or message.caption or ""

    # Skip messages without text
    if not text:
        return

    # -----------------------------
    # AFK Auto-reply
    # -----------------------------
    afk_reply = afk_auto_reply(user_id)
    if afk_reply:
        await message.reply_text(afk_reply)
        logger.info(f"Sent AFK auto-reply to {user_id}")
        return

    # -----------------------------
    # Chatbot toggle check
    # -----------------------------
    if not is_chatbot_enabled(chat_id):
        return

    # -----------------------------
    # Fake typing simulation
    # -----------------------------
    try:
        await message.chat.send_action("typing")
        await asyncio.sleep(FAKE_TYPING_DELAY)
    except Exception as e:
        logger.warning(f"Failed to send typing action: {e}")

    # -----------------------------
    # Get human-like reply
    # -----------------------------
    try:
        reply_text, _ = await get_human_reply(user_id, text)
        if reply_text:
            await message.reply_text(reply_text)
            logger.info(f"Replied to {user_id} with human-like message")
    except Exception as e:
        logger.warning(f"Failed to generate reply: {e}")

    # -----------------------------
    # Send reactions (optional)
    # -----------------------------
    try:
        await send_reaction(message)
    except Exception as e:
        logger.warning(f"Failed to send reaction: {e}")

# -----------------------------
# Voice Handler (Optional)
# -----------------------------
@app.on_message(filters.voice | filters.audio)
async def handle_voice(client, message):
    user_id = message.from_user.id if message.from_user else None
    logger.info(f"Received voice message from {user_id}")

    # Placeholder for future implementation:
    # Convert voice → text → AI reply → voice response
    try:
        await message.reply_text("Voice reply feature coming soon 😎")
    except Exception as e:
        logger.warning(f"Failed to send placeholder voice reply: {e}")