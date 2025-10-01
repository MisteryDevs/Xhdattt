import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tnc import config
from tnc.log_utils import log_message_details, log_event

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
# Start command image and buttons
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
# Startup
# -----------------------------
async def main():
    await app.start()
    await log_event("BOT_STARTED")
    print("✅ TNC Bot is running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())