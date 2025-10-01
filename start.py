import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tnc import config
from tnc.log_utils import log_message_details, log_event
from tnc.human_reply import get_human_reply
from tnc.voice_manager import text_to_voice

app = Client(
    "TNC-Bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# -----------------------------
# Start & Help Images and Captions
# -----------------------------
START_IMAGE_URL = "https://telegra.ph/file/your_start_image_here.png"
HELP_IMAGE_URL = "https://telegra.ph/file/your_help_image_here.png"

START_CAPTION = (
    "👋 Hello! I am TNC Bot 🤖\n\n"
    "I can chat in Hinglish, send voice replies, react with emojis, "
    "and handle AFK messages.\n\nOwner: {}".format(config.BOT_OWNER)
)

HELP_CAPTION = (
    "🆘 **TNC Bot Help**\n\n"
    "I can:\n"
    "• Chat in Hinglish 💬\n"
    "• Reply in voice 🎙️\n"
    "• React with emojis 😎\n"
    "• Handle AFK messages 💤\n\n"
    "Owner: {}".format(config.BOT_OWNER)
)

# -----------------------------
# Inline Buttons
# -----------------------------
BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("👤 Owner", url=f"https://t.me/{config.BOT_OWNER.lstrip('@')}")],
    [InlineKeyboardButton("💬 Support Chat", url=f"https://t.me/{config.SUPPORT_CHAT_ID.lstrip('@')}")],
    [InlineKeyboardButton("📢 Channel", url=f"https://t.me/{config.CHANNEL_ID.lstrip('@')}")]
])

# -----------------------------
# Fake typing helper
# -----------------------------
async def fake_typing(chat, delay: float = config.FAKE_TYPING_DELAY):
    await chat.send_action("typing")
    await asyncio.sleep(delay)

# -----------------------------
# /start command
# -----------------------------
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await log_message_details(message)
    await fake_typing(message.chat)
    await message.reply_photo(
        photo=START_IMAGE_URL,
        caption=START_CAPTION,
        reply_markup=BUTTONS
    )
    await log_event("START_COMMAND", message=message)

# -----------------------------
# /help command
# -----------------------------
@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    await log_message_details(message)
    await fake_typing(message.chat)
    await message.reply_photo(
        photo=HELP_IMAGE_URL,
        caption=HELP_CAPTION,
        reply_markup=BUTTONS
    )
    await log_event("HELP_COMMAND", message=message)

# -----------------------------
# Chat handler for human-like Hinglish replies
# -----------------------------
@app.on_message(filters.text & ~filters.edited)
async def chat_handler(client, message):
    await log_message_details(message)

    # Fake typing
    await fake_typing(message.chat)

    # Generate human-like reply
    reply_text, voice_bytes = await get_human_reply(message.from_user.id, message.text)

    if reply_text:
        await message.reply_text(reply_text)
        await log_event("CHATBOT_REPLY", message=message, extra=f"Reply: {reply_text[:50]}")

    # Send voice reply if available
    if voice_bytes:
        await message.reply_voice(voice_bytes)
        await log_event("VOICE_REPLY_SENT", message=message, extra=f"Voice length: {len(voice_bytes)} bytes")

# -----------------------------
# Startup
# -----------------------------
async def main():
    await app.start()
    await log_event("BOT_STARTED")
    print("✅ TNC Bot is running with fake typing & voice replies...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())