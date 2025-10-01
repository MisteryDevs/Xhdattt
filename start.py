import asyncio
from pyrogram import Client
from tnc.bot import app  # your bot instance
from tnc.logger import logger
from tnc.config import BOT_NAME, BOT_OWNER

# Optional: send a start image in support chat & channel
WELCOME_IMAGE_URL = "https://example.com/welcome_image.jpg"  # Replace with your image URL

# Replace these with actual chat IDs or usernames
SUPPORT_CHAT_ID = "@YourSupportChat"    # Example: @TNC_Support
CHANNEL_ID = "@YourChannel"             # Example: @TNC_Updates

async def send_startup_messages():
    caption = f"{BOT_NAME} has started 💖\nOwner: {BOT_OWNER}"
    try:
        # Send to support chat
        await app.send_photo(
            chat_id=SUPPORT_CHAT_ID,
            photo=WELCOME_IMAGE_URL,
            caption=f"Support Chat Notification ✅\n{caption}"
        )
        logger.info("Startup image sent to support chat!")

        # Send to channel
        await app.send_photo(
            chat_id=CHANNEL_ID,
            photo=WELCOME_IMAGE_URL,
            caption=f"Channel Notification 📢\n{caption}"
        )
        logger.info("Startup image sent to channel!")

    except Exception as e:
        logger.warning(f"Failed to send startup images: {e}")

def main():
    logger.info(f"{BOT_NAME} starting... 💖")
    app.start()
    logger.info(f"{BOT_NAME} is now running!")

    # Send startup messages asynchronously
    asyncio.get_event_loop().run_until_complete(send_startup_messages())

    # Keep bot running
    app.idle()

if __name__ == "__main__":
    main()
