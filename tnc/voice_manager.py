"""
Manages all interactions with the ElevenLabs Text-to-Speech API,
including voice conversion and async key rotation.
"""

import logging
from elevenlabs.client import AsyncElevenLabs
import config
import asyncio

logger = logging.getLogger(__name__)

# -----------------------------
# Configure voice ID
# -----------------------------
TNC_VOICE_ID = "DnThIAnAgyB5NKBqPQmh"  # Replace with your ElevenLabs voice ID

# -----------------------------
# Text-to-voice function
# -----------------------------
async def text_to_voice(text: str) -> bytes | None:
    """
    Converts Hinglish text to voice using ElevenLabs, with API key rotation on failure.

    Args:
        text: The text to convert.

    Returns:
        The audio data as bytes if successful, otherwise None.
    """
    if not config.ELEVENLABS_API_KEYS:
        logger.warning("ELEVENLABS_API_KEYS not configured. Skipping voice generation.")
        return None

    # Rotate through all API keys
    for attempt in range(len(config.ELEVENLABS_API_KEYS)):
        try:
            current_key = config.ELEVENLABS_API_KEYS[config.CURRENT_ELEVEN_KEY_INDEX]
            logger.info(f"Attempting ElevenLabs call with key index {config.CURRENT_ELEVEN_KEY_INDEX}")

            eleven_client = AsyncElevenLabs(api_key=current_key)

            # Convert text to voice
            audio_stream = eleven_client.text_to_speech.convert(
                voice_id=TNC_VOICE_ID,
                model_id="eleven_v3",
                text=text,
                output_format="mp3_44100_128"
            )

            # Assemble audio bytes
            audio_bytes = b""
            async for chunk in audio_stream:
                audio_bytes += chunk

            if not audio_bytes:
                raise ValueError("Received empty audio stream from ElevenLabs.")

            logger.info(f"Successfully generated voice for text: '{text[:30]}...'")
            return audio_bytes

        except Exception as e:
            logger.warning(
                f"ElevenLabs API key at index {config.CURRENT_ELEVEN_KEY_INDEX} failed ({type(e).__name__}: {e}). Rotating to next key."
            )
            # Rotate key
            config.CURRENT_ELEVEN_KEY_INDEX = (config.CURRENT_ELEVEN_KEY_INDEX + 1) % len(config.ELEVENLABS_API_KEYS)

    logger.critical("All ElevenLabs API keys exhausted or failing. Please check your quotas.")
    return None
