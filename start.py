import sys
import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Add current directory to path for Heroku
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import config and bot utilities
from config import BOT_NAME, API_ID, API_HASH, BOT_TOKEN, BOT_OWNER, SUPPORT_CHAT_ID, CHANNEL_ID, FAKE_TYPING_DELAY
from tnc.log_utils import log_message_details, log_event
from tnc.human_reply import get_human_reply
from tnc.voice_manager import text_to_voice

# -----------------------------
# Pyrogram client
# -----------------------------
app = Client(
    BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# -----------------------------
# Start & Help Images & Captions
# -----------------------------
START_IMAGE_URL = "https://files.catbox.moe/ytmqz3.jpg"
HELP_IMAGE_URL = "https://files.catbox.moe/4dtfwd.jpg"

START_CAPTION = (
    f"ʜᴇʟʟᴏ! I am a chat bot of TNC.\n\nOwner: {BOT_OWNER}"
)
HELP_CAPTION = (
    f"I can chat in Hinglish 💬\nReply in voice 🎙️\nReact with emojis 😎\nHandle AFK messages 💤\n\nOwner: {BOT_OWNER}"
)

# -----------------------------
# Inline buttons
# -----------------------------
BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("ʙᴀʙʏ 👀", url=f"https://t.me/{BOT_OWNER.lstrip('@')}")],
    [InlineKeyboardButton("💬 Support Chat", url=f"https://t.me/{SUPPORT_CHAT_ID.lstrip('@')}")],
    [InlineKeyboardButton("📢 Channel", url=f"https://t.me/{CHANNEL_ID.lstrip('@')}")]
])

# -----------------------------
# Fake typing helper
# -----------------------------
async def fake_typing(client, chat_id, delay=FAKE_TYPING_DELAY):
    await client.send_chat_action(chat_id, "typing")
    await asyncio.sleep(delay)

# -----------------------------
# /start command
# -----------------------------
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await log_message_details(message)
    await fake_typing(client, message.chat.id)
    await message.reply_photo(photo=START_IMAGE_URL, caption=START_CAPTION, reply_markup=BUTTONS)
    await log_event("START_COMMAND", message=message)

# -----------------------------
# /help command
# -----------------------------
@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    await log_message_details(message)
    await fake_typing(client, message.chat.id)
    await message.reply_photo(photo=HELP_IMAGE_URL, caption=HELP_CAPTION, reply_markup=BUTTONS)
    await log_event("HELP_COMMAND", message=message)

# -----------------------------
# Chat handler for human-like replies
# -----------------------------
@app.on_message(filters.text)
async def chat_handler(client, message):
    await log_message_details(message)
    await fake_typing(client, message.chat.id)

    reply_text, voice_bytes = await get_human_reply(message.from_user.id, message.text)

    if reply_text:
        await message.reply_text(reply_text)
        await log_event("CHATBOT_REPLY", message=message, extra=f"Reply: {reply_text[:50]}")

    if voice_bytes:
        await message.reply_voice(voice_bytes)
        await log_event("VOICE_REPLY_SENT", message=message, extra=f"Voice length: {len(voice_bytes)} bytes")

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
