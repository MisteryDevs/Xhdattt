from pyrogram import filters
from tnc import app, logger
from tnc.afk_manager import check_afk, afk_auto_reply
from tnc.human_reply import get_human_reply
from tnc.reactions import send_reaction
from tnc.toggle import is_chatbot_enabled
from tnc.config import BOT_OWNER, FAKE_TYPING_DELAY
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
        reply_text = await get_human_reply(text, user_id)
        await message.reply_text(reply_text)
        logger.info(f"Replied to {user_id} with human-like message")
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
    # Placeholder: Convert voice → text → AI reply → voice response
    logger.info(f"Received voice message from {message.from_user.id}")
    await message.reply_text("Voice reply feature coming soon 😎")
