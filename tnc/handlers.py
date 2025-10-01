from pyrogram import filters
from tnc import app, logger
from tnc.afk_manager import set_afk, remove_afk
from tnc.toggle import enable_chatbot, disable_chatbot
from tnc.config import BOT_OWNER

# -----------------------------
# /start command
# -----------------------------
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply_text(
        f"Hello {message.from_user.first_name} 😎\n"
        f"I'm your TNC-Bot! Owner: {BOT_OWNER}\n"
        "You can chat with me here."
    )
    logger.info(f"/start command used by {message.from_user.id}")

# -----------------------------
# /afk command
# -----------------------------
@app.on_message(filters.command("afk") & filters.private)
async def afk_command(client, message):
    reason = " ".join(message.command[1:]) if len(message.command) > 1 else None
    set_afk(message.from_user.id, reason)
    await message.reply_text(f"You are now AFK 😴\nReason: {reason or 'AFK'}")

# -----------------------------
# /back command
# -----------------------------
@app.on_message(filters.command("back") & filters.private)
async def back_command(client, message):
    remove_afk(message.from_user.id)
    await message.reply_text("Welcome back! You're no longer AFK ✅")

# -----------------------------
# Chatbot Toggle Commands
# -----------------------------
@app.on_message(filters.command("chatbot_on") & filters.user(BOT_OWNER))
async def chatbot_on(client, message):
    enable_chatbot(message.chat.id)
    await message.reply_text("Chatbot enabled in this chat ✅")
    logger.info(f"Chatbot enabled in chat {message.chat.id}")

@app.on_message(filters.command("chatbot_off") & filters.user(BOT_OWNER))
async def chatbot_off(client, message):
    disable_chatbot(message.chat.id)
    await message.reply_text("Chatbot disabled in this chat ❌")
    logger.info(f"Chatbot disabled in chat {message.chat.id}")

# -----------------------------
# /owner command
# -----------------------------
@app.on_message(filters.command("owner") & filters.private)
async def owner_command(client, message):
    await message.reply_text(f"My owner is: {BOT_OWNER} 💖")