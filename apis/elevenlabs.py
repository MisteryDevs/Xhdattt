# apis/elevenlabs.py

import logging
from elevenlabs.client import AsyncElevenLabs
import config
import asyncio

logger = logging.getLogger(__name__)

class ElevenLabsClient:
    def __init__(self):
        self.api_keys = config.ELEVENLABS_API_KEYS
        self.current_key_index = 0
        self.voice_id = config.TNC_VOICE_ID

    async def text_to_voice(self, text: str) -> bytes | None:
        if not self.api_keys:
            logger.warning("ELEVENLABS_API_KEYS not configured. Skipping voice generation.")
            return None

        for _ in range(len(self.api_keys)):
            try:
                current_key = self.api_keys[self.current_key_index]
                logger.info(f"Attempting ElevenLabs call with key index {self.current_key_index}")

                eleven_client = AsyncElevenLabs(api_key=current_key)

                audio_stream = await eleven_client.text_to_speech.convert(
                    voice_id=self.voice_id,
                    text=text,
                )

                audio_bytes = b""
                async for chunk in audio_stream:
                    audio_bytes += chunk

                if not audio_bytes:
                    raise ValueError("Received empty audio stream from ElevenLabs.")

                logger.info(f"Successfully generated voice for text: '{text[:30]}...'")
                return audio_bytes

            except Exception as e:
                logger.warning(
                    f"ElevenLabs API key at index {self.current_key_index} failed ({type(e).__name__}: {e}). Rotating to next key."
                )
                self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)

        logger.critical("All ElevenLabs API keys exhausted or failing. Please check your quotas.")
        return None
