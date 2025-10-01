import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tnc import config
from tnc.log_utils import log_message_details, log_event, logger
from tnc.human_reply import get_human_reply
from tnc.voice_manager import text_to_voice
from tnc.reactions import send_reaction
from tnc.toggle import is_enabled
from tnc.afk_manager import set_afk, remove_afk, handle_afk_mention

# -----------------------------
# Initialize bot
# -----------------------------
app = Client(
    "TNC-Bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# -----------------------------
# Start command with image + buttons
# -----------------------------
START_IMAGE_URL = "https://telegra.ph/file/your_image_here.png"
START_CAPTION = (
    "👋 Hello! I am TNC Bot 🤖\n\n"
    "I can chat in Hinglish, send voice replies, react with emojis, "
    "and handle AFK messages.\n\nOwner: @SemxyCarders"
)

START_BUTTONS = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("👤 Owner", url=f"https://t.me/{config.BOT_OWNER}")],
        [InlineKeyboardButton("💬 Support Chat", url=config.SUPPORT_CHAT)],
        [InlineKeyboardButton("📢 Channel", url=config.CHANNEL)]
    ]
)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await log_message_details(message)
    await message.reply_photo(
        photo=START_IMAGE_URL,
        caption=START_CAPTION,
        reply_markup=START_BUTTONS
    )
    await log_event("START_COMMAND", message=message)
    print(f"✅ /start triggered by {message.from_user.id}")

# -----------------------------
# AFK Commands
# -----------------------------
@app.on_message(filters.command("afk") & filters.private)
async def afk_command(client, message):
    reason = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    await set_afk(message.from_user.id, reason)
    await message.reply_text(f"✅ You are now AFK.\nReason: {reason or 'No reason provided.'}")
    await log_event("AFK_SET", message=message, extra=reason)

@app.on_message(filters.command("back") & filters.private)
async def back_command(client, message):
    await remove_afk(message.from_user.id)
    await message.reply_text("✅ Welcome back! AFK removed.")
    await log_event("AFK_REMOVED", message=message)

# -----------------------------
# Main message handler
# -----------------------------
@app.on_message(filters.text & ~filters.edited)
async def handle_message(client, message):
    await log_message_details(message)
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text or message.caption

    if not text:
        return

    # -----------------------------
    # Handle AFK mentions
    # -----------------------------
    await handle_afk_mention(message)

    # -----------------------------
    # Check chatbot toggle
    # -----------------------------
    if not is_enabled(chat_id, "chatbot_enabled"):
        await log_event("CHATBOT_DISABLED", message=message)
        return

    # -----------------------------
    # Simulate fake typing
    # -----------------------------
    await message.chat.send_action("typing")
    await asyncio.sleep(config.FAKE_TYPING_DELAY)

    # -----------------------------
    # Generate human-like Hinglish reply
    # -----------------------------
    try:
        reply_text, voice_bytes = await get_human_reply(user_id, text)
        if reply_text:
            await message.reply_text(reply_text)
            await log_event("CHATBOT_REPLY", message=message, extra=f"Reply: {reply_text[:50]}")
            
            # -----------------------------
            # Send voice reply if available
            # -----------------------------
            if voice_bytes:
                await message.reply_voice(voice_bytes)
                await log_event("VOICE_SENT", message=message, extra=f"Voice length: {len(voice_bytes)} bytes")
    except Exception as e:
        logger.warning(f"[CHATBOT] Failed to generate reply: {e}")

    # -----------------------------
    # Send emoji reactions
    # -----------------------------
    if is_enabled(chat_id, "reactions_enabled"):
        await send_reaction(message)
        await log_event("REACTION_SENT", message=message)

# -----------------------------
# Startup
# -----------------------------
async def main():
    await app.start()
    await log_event("BOT_STARTED")
    print("✅ TNC Bot is running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())