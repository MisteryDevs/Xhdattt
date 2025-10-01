import asyncio
import logging
from tnc.voice_manager import text_to_voice
from tnc.config import (
    SAMNOVA_API_KEY,
    GEMINI_API_KEY,
    OPENAI_API_KEY,
    FAKE_TYPING_DELAY
)
from tnc.apis import samnova, gemini, openai_api

logger = logging.getLogger(__name__)

# -----------------------------
# Multi-API Human Reply
# -----------------------------
async def get_human_reply(user_id: int, text: str):
    """
    Returns a human-like response for the user text.
    Tries Samnova first, then Gemini, then OpenAI.
    Also generates voice bytes if ElevenLabs API is configured.
    Simulates fake typing delay before sending reply.
    """

    reply_text = None
    audio_bytes = None

    # -----------------------------
    # Fake typing delay
    # -----------------------------
    await asyncio.sleep(FAKE_TYPING_DELAY)

    # -----------------------------
    # 1️⃣ Try Samnova API
    # -----------------------------
    try:
        reply_text = await samnova.chat(text, user_id, api_key=SAMNOVA_API_KEY)
        if reply_text:
            logger.info(f"[Samnova] Reply generated for user {user_id}")
    except Exception as e:
        logger.warning(f"[Samnova] Failed: {e}")

    # -----------------------------
    # 2️⃣ Fallback to Gemini API
    # -----------------------------
    if not reply_text:
        try:
            gem_client = gemini.GeminiClient(api_key=GEMINI_API_KEY)
            reply_text = await gem_client.chat(text)
            if reply_text:
                logger.info(f"[Gemini] Reply generated for user {user_id}")
        except Exception as e:
            logger.warning(f"[Gemini] Failed: {e}")

    # -----------------------------
    # 3️⃣ Fallback to OpenAI API
    # -----------------------------
    if not reply_text:
        try:
            reply_text = await openai_api.chat_with_openai(text, api_key=OPENAI_API_KEY)
            if reply_text:
                logger.info(f"[OpenAI] Reply generated for user {user_id}")
        except Exception as e:
            logger.warning(f"[OpenAI] Failed: {e}")

    # -----------------------------
    # 4️⃣ Generate Voice if available
    # -----------------------------
    try:
        if reply_text:
            audio_bytes = await text_to_voice(reply_text)
    except Exception as e:
        logger.warning(f"[Voice] Failed to generate voice: {e}")

    # Return tuple: (text reply, voice bytes)
    return reply_text, audio_bytes