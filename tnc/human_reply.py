import asyncio
import logging
from tnc.voice_manager import text_to_voice
from config import (
    SAMBANOVA_API_KEY,  # updated
    GEMINI_API_KEY,
    OPENAI_API_KEY,
    FAKE_TYPING_DELAY
)
# from tnc.apis import sambanova_client, gemini, openai  # updated imports
from apis import sambanova_client, gemini, openai
logger = logging.getLogger(__name__)

async def get_human_reply(user_id: int, text: str):
    """
    Returns a human-like Hinglish response for the user text.
    Tries Sambanova first, then Gemini, then OpenAI.
    Also generates voice bytes using ElevenLabs (if configured).
    Simulates fake typing delay before sending reply.

    Args:
        user_id (int): Unique user ID for session/context.
        text (str): User's message.

    Returns:
        tuple: (reply_text:str, audio_bytes:bytes or None)
    """
    reply_text = None
    audio_bytes = None

    # -----------------------------
    # Fake typing delay
    # -----------------------------
    await asyncio.sleep(FAKE_TYPING_DELAY)

    # -----------------------------
    # 1️⃣ Try Sambanova API
    # -----------------------------
    try:
        reply_text = await sambanova_client.get_reply(text, user_id, api_key=SAMBANOVA_API_KEY, lang="hinglish")
        if reply_text:
            logger.info(f"[Sambanova] Reply generated for user {user_id}")
    except Exception as e:
        logger.warning(f"[Sambanova] Failed: {e}")

    # -----------------------------
    # 2️⃣ Fallback to Gemini API
    # -----------------------------
    if not reply_text:
        try:
            gem_client = gemini.GeminiClient(api_key=GEMINI_API_KEY)
            reply_text = await gem_client.chat(text, lang="hinglish")
            if reply_text:
                logger.info(f"[Gemini] Reply generated for user {user_id}")
        except Exception as e:
            logger.warning(f"[Gemini] Failed: {e}")

    # -----------------------------
    # 3️⃣ Fallback to OpenAI API
    # -----------------------------
    if not reply_text:
        try:
            reply_text = await openai.chat_with_openai(text, api_key=OPENAI_API_KEY, lang="hinglish")
            if reply_text:
                logger.info(f"[OpenAI] Reply generated for user {user_id}")
        except Exception as e:
            logger.warning(f"[OpenAI] Failed: {e}")

    # -----------------------------
    # 4️⃣ Generate Voice if available
    # -----------------------------
    if reply_text:
        try:
            audio_bytes = await text_to_voice(reply_text)
        except Exception as e:
            logger.warning(f"[Voice] Failed to generate voice: {e}")

    # -----------------------------
    # Return tuple: (text reply, voice bytes)
    # -----------------------------
    return reply_text, audio_bytes
