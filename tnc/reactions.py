import random
from tnc import app, logger
from pyrogram.types import Message

# List of emoji reactions
EMOJI_REACTIONS = [
    "😏", "😉", "😂", "🥰", "😎", "😅", "🤭", "😍", "🤩", "🤔", "🙃"
]

async def send_reaction(message: Message):
    """
    Sends a random emoji reaction to a user message.
    """
    try:
        # 30% chance to react (optional)
        if random.random() < 0.3:
            emoji = random.choice(EMOJI_REACTIONS)
            await message.reply_text(emoji)
            logger.info(f"Sent reaction {emoji} to {message.from_user.id}")
    except Exception as e:
        logger.warning(f"Failed to send reaction: {e}")