import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tnc import config
from tnc.log_utils import log_message_details, log_event
from tnc.human_reply import get_human_reply
from tnc.voice_manager import text_to_voice
from tnc.reactions import send_reaction
from tnc.toggle import is_enabled, toggle
from tnc.afk_manager import handle_afk_mention, set_afk, remove_afk

app = Client(
    "TNC-Bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# -----------------------------
# Support Chat/Channel Logging
# -----------------------------
async def log_to_support(message):
    try:
        user = message.from_user
        username = f"@{user.username}" if user and user.username else "Unknown"
        user_id = user.id if user else "Unknown"
        chat_type = message.chat.type

        log_text = (
            f"📨 New Message Logged:\n"
            f"User: {username} ({user_id})\n"
            f"Chat: {message.chat.title or 'Private'} ({chat_type})\n"
            f"Message: {message.text or message.caption or '[Media/Other]'}"
        )

        await app.send_message(config.SUPPORT_CHAT_ID, log_text)
        await log_event("SUPPORT_LOGGED", message=message)
    except Exception as e:
        await log_event("SUPPORT_LOG_FAIL", message=message, extra=str(e))


# -----------------------------
# Start command with buttons
# -----------------------------
START_IMAGE_URL = "https://telegra.ph/file/your_image_here.png"
START_CAPTION = (
    "👋 Hello! I am TNC Bot 🤖\n\n"
    "I can chat in Hinglish, send voice replies, react with emojis, "
    "and handle AFK messages.\n\nOwner: @SemxyCarders"
)

START_BUTTONS = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("👤 Owner", url="https://t.me/SemxyCarders")],
        [InlineKeyboardButton("💬 Support Chat", url="https://t.me/YourSupportChat")],
        [InlineKeyboardButton("📢 Support Channel", url="https://t.me/YourSupportChannel")]
    ]
)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await log_message_details(message)
    await message.reply_photo(photo=START_IMAGE_URL, caption=START_CAPTION, reply_markup=START_BUTTONS)
    await log_event("START_COMMAND", message=message)


# -----------------------------
# /afk command
# -----------------------------
@app.on_message(filters.command("afk") & filters.private)
async def afk_command(client, message):
    reason = " ".join(message.command[1:]) if len(message.command) > 1 else ""
    await set_afk(message.from_user.id, reason)
    await message.reply_text(f"✅ You are now AFK.\nReason: {reason or 'No reason provided.'}")


# -----------------------------
# /back command
# -----------------------------
@app.on_message(filters.command("back") & filters.private)
async def back_command(client, message):
    await remove_afk(message.from_user.id)
    await message.reply_text("✅ Welcome back! AFK removed.")


# -----------------------------
# Main message handler
# -----------------------------
@app.on_message(filters.text & ~filters.edited)
async def handle_message(client, message):
    await log_message_details(message)
    await log_to_support(message)
    chat_id = message.chat.id

    if not is_enabled(chat_id, "chatbot_enabled"):
        await log_event("CHATBOT_DISABLED", message=message)
        return

    await handle_afk_mention(message)

    reply_text = await get_human_reply(message.text, message.from_user.id)
    if reply_text:
        await message.reply_text(reply_text)
        await log_event("CHATBOT_REPLY", message=message, extra=f"Reply: {reply_text[:50]}")

        voice_bytes = await text_to_voice(reply_text)
        if voice_bytes:
            await message.reply_voice(voice_bytes)
            await log_event("VOICE_SENT", message=message, extra=f"Voice length: {len(voice_bytes)} bytes")

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