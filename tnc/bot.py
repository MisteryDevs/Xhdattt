from pyrogram import filters
from tnc import app, logger
from tnc.afk_manager import afk_auto_reply
from tnc.human_reply import get_human_reply
from tnc.reactions import send_reaction
from tnc.toggle import is_chatbot_enabled
from tnc.config import FAKE_TYPING_DELAY

import asyncio

# -----------------------------
# Message Handler
# -----------------------------
@app.on_message(filters.private | filters.group)
async def handle_message(client, message):
    user_id = message.from_user.id if message.from_user else None
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
    # Chatbot toggle
    # -----------------------------
    if not is_chatbot_enabled(message.chat.id):
        return

    # -----------------------------
    # Fake typing simulation
    # -----------------------------
    await message.chat.send_action("typing")
    await asyncio.sleep(FAKE_TYPING_DELAY)

    # -----------------------------
    # Get human-like reply
    # -----------------------------
    try:
        reply_text, audio_bytes = await get_human_reply(user_id, text)

        # Send text reply
        if reply_text:
            await message.reply_text(reply_text)
            logger.info(f"Replied to {user_id} with human-like message")

        # Send voice reply if available
        if audio_bytes:
            await message.reply_voice(audio_bytes)
            logger.info(f"Sent voice reply to {user_id}")

    except Exception as e:
        logger.warning(f"Failed to generate reply: {e}")

    # -----------------------------
    # Send reactions (optional)
    # -----------------------------
    await send_reaction(message)


# -----------------------------
# Voice Handler (Optional)
# -----------------------------
@app.on_message(filters.voice | filters.audio)
async def handle_voice(client, message):
    # Convert voice → text → AI reply → voice response
    user_id = message.from_user.id if message.from_user else None
    logger.info(f"Received voice message from {user_id}")

    # Placeholder for future voice-to-text + reply
    await message.reply_text("Voice reply feature coming soon 😎")