import aiohttp
import asyncio
import logging
import config  # Load GEMINI_API_KEY from config

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Async client to communicate with Gemini API.
    """
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or config.GEMINI_API_KEY
        self.base_url = base_url or "https://api.gemini.example.com"
        self.headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    async def chat(self, message: str) -> str:
        """
        Send a message to Gemini API and return the reply text.
        """
        if not self.api_key:
            raise ValueError("Gemini API key not provided")

        payload = {"message": message}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(f"{self.base_url}/chat", json=payload, headers=self.headers, timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # Assume API returns {"reply": "text reply"}
                        return data.get("reply")
                    else:
                        logger.warning(f"[GEMINI] Error {resp.status}: {await resp.text()}")
                        return None
            except asyncio.TimeoutError:
                logger.warning("[GEMINI] Request timed out")
                return None
            except Exception as e:
                logger.error(f"[GEMINI] Unexpected error: {e}")
                return None
