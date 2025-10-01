 import aiohttp
import asyncio
from tnc import config
from tnc.log_utils import logger

SAMNOVA_API_URL = "https://api.samnova.ai/v1/chat"  # Replace with correct endpoint
API_KEY = config.SAMNOVA_API_KEY  # Make sure this is set in your config

async def get_samnova_reply(message_text: str, user_id: int = None) -> str:
    """
    Sends a message to Samnova API and gets a reply.
    
    Args:
        message_text (str): User message text.
        user_id (int, optional): Unique ID for the user (for context/session).
    
    Returns:
        str: Samnova AI response.
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": message_text,
        "user_id": str(user_id) if user_id else "anonymous",
        "lang": "en"  # Use "hinglish" if supported by API
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(SAMNOVA_API_URL, json=payload, headers=headers, timeout=30) as resp:
                if resp.status != 200:
                    logger.warning(f"Samnova API failed: {resp.status}")
                    return "Sorry, I am having trouble replying right now 😓"
                data = await resp.json()
                reply = data.get("reply") or data.get("message") or "Hmm..."
                return reply
    except asyncio.TimeoutError:
        logger.warning("Samnova API timeout")
        return "Sorry, I took too long to think 😅"
    except Exception as e:
        logger.warning(f"Samnova API error: {e}")
        return "Oops! Something went wrong 🤔"