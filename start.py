import asyncio
from pyrogram import Client, filters
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
# Start command with image
# -----------------------------
START_IMAGE_URL = "https://telegra.ph/file/your_image_here.png"
START_CAPTION = (
    "👋 Hello! I am TNC Bot 🤖\n\n"
    "I can chat in Hinglish, send voice replies, react with emojis, "
    "and handle AFK messages.\n\nOwner: @SemxyCarders"
)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await log_message_details(message)
    await message.reply_photo(photo=START_IMAGE_URL, caption=START_CAPTION)
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
    chat_id = message.chat.id

    # Check if chatbot is enabled
    if not is_enabled(chat_id, "chatbot_enabled"):
        await log_event("CHATBOT_DISABLED", message=message)
        return

    # Handle AFK mentions
    await handle_afk_mention(message)

    # Generate human-like Hinglish reply
    reply_text = await get_human_reply(message.text, message.from_user.id)
    if reply_text:
        await message.reply_text(reply_text)
        await log_event("CHATBOT_REPLY", message=message, extra=f"Reply: {reply_text[:50]}")

        # Voice reply
        voice_bytes = await text_to_voice(reply_text)
        if voice_bytes:
            await message.reply_voice(voice_bytes)
            await log_event("VOICE_SENT", message=message, extra=f"Voice length: {len(voice_bytes)} bytes")

    # Emoji reactions
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