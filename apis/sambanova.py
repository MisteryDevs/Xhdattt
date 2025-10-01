# apis/sambanova.py

import aiohttp
import asyncio
import config
from tnc.log_utils import logger

class SambanovaClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.samnova.ai/v1/chat" # Using the URL from the original file

    async def get_reply(self, message_text: str, user_id: int = None) -> str:
        """
        Sends a message to Samnova API and gets a reply.
        """
        if not self.api_key:
            logger.error("Sambanova API key is not set.")
            return "Sorry, I am having trouble replying right now 😓"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "message": message_text,
            "user_id": str(user_id) if user_id else "anonymous",
            "lang": "en"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload, headers=headers, timeout=30) as resp:
                    if resp.status != 200:
                        logger.warning(f"Sambanova API failed: {resp.status}")
                        return "Sorry, I am having trouble replying right now 😓"
                    data = await resp.json()
                    return data.get("reply") or data.get("message") or "Hmm..."
        except asyncio.TimeoutError:
            logger.warning("Sambanova API timeout")
            return "Sorry, I took too long to think 😅"
        except Exception as e:
            logger.warning(f"Sambanova API error: {e}")
            return "Oops! Something went wrong 🤔"
