import asyncio
from pyrogram import Client, filters
from tnc import config, logger_setup
from tnc.utils import log_message_details, log_event
from tnc.human_reply import get_human_reply
from tnc.voice_manager import text_to_voice
from tnc.reactions import send_reaction
from tnc.toggle import is_chatbot_enabled
from tnc.afk_manager import check_afk, handle_afk_mention

app = Client(
    "TNC-Bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# -----------------------------
# Start command with welcome image
# -----------------------------
START_IMAGE_URL = "https://telegra.ph/file/your_image_here.png"  # Replace with your image
START_CAPTION = (
    "👋 Hello! I am TNC Bot 🤖\n\n"
    "I can chat in Hinglish, send voice replies, react with emojis, "
    "and handle AFK messages.\n\n"
    "Owner: @SemxyCarders"
)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await log_message_details(message)
    await message.reply_photo(
        photo=START_IMAGE_URL,
        caption=START_CAPTION
    )
    await log_event("START_COMMAND", message=message)

# -----------------------------
# Main message handler
# -----------------------------
@app.on_message(filters.text & ~filters.edited)
async def handle_message(client, message):
    # Log message details
    await log_message_details(message)

    chat_id = message.chat.id

    # Check chatbot toggle
    if not is_chatbot_enabled(chat_id):
        return

    # Check for AFK mentions
    await handle_afk_mention(message)

    # Generate human-like Hinglish reply
    reply_text = await get_human_reply(message.text, message.from_user.id)
    if reply_text:
        # Send text reply
        await message.reply_text(reply_text)
        await log_event("CHATBOT_REPLY", message=message, extra=f"Reply: {reply_text[:50]}")

        # Send voice reply
        voice_bytes = await text_to_voice(reply_text)
        if voice_bytes:
            await message.reply_voice(voice_bytes)
            await log_event("VOICE_SENT", message=message, extra=f"Voice length: {len(voice_bytes)} bytes")

    # Send emoji reactions
    await send_reaction(message)
    await log_event("REACTION_SENT", message=message)

# -----------------------------
# Startup
# -----------------------------
async def main():
    logger_setup.logger.info("Starting TNC Bot...")
    await app.start()
    logger_setup.logger.info("TNC Bot started and listening for messages...")
    await asyncio.Event().wait()  # Keep running

if __name__ == "__main__":
    asyncio.run(main())