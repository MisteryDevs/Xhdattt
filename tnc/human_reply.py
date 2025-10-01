import asyncio
import random
import logging
from tnc.voice_manager import text_to_voice
from tnc.log_utils import log_message
from apis import samnova, gemini, openai_api
import config  # Import API keys and settings

# -----------------------------
# Logger configuration
# -----------------------------
logger = logging.getLogger(__name__)

# Initialize API clients with keys from config
samnova_client = samnova.SamnovaClient(api_key=config.SAMNOVA_API_KEY)
gemini_client = gemini.GeminiClient(api_key=config.GEMINI_API_KEY)
openai_api_key = config.OPENAI_API_KEY

# -----------------------------
# Fake typing simulation
# -----------------------------
async def fake_typing(user_id: int, message_text: str, min_delay: float = 0.5, max_delay: float = 1.5):
    """
    Simulate human typing delay based on message length.
    """
    delay = random.uniform(min_delay, max_delay) + len(message_text) * 0.05
    await asyncio.sleep(delay)

# -----------------------------
# Multi-API reply router
# -----------------------------
async def get_mixed_reply(user_id: int, message_text: str) -> str:
    """
    Try Samnova → Gemini → OpenAI and return first successful reply.
    """
    # 1️⃣ Try Samnova
    try:
        reply = await samnova_client.get_reply(message_text)
        if reply:
            return reply
    except Exception as e:
        logger.warning(f"[API_ROUTER] Samnova failed: {e}")

    # 2️⃣ Try Gemini
    try:
        reply = await gemini_client.chat(message_text)
        if reply:
            return reply
    except Exception as e:
        logger.warning(f"[API_ROUTER] Gemini failed: {e}")

    # 3️⃣ Try OpenAI
    try:
        import openai
        openai.api_key = openai_api_key
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message_text}],
            temperature=0.7,
            max_tokens=200
        )
        reply = completion.choices[0].message.content
        if reply:
            return reply
    except Exception as e:
        logger.warning(f"[API_ROUTER] OpenAI failed: {e}")

    # 4️⃣ Fallback reply
    fallback = random.choice([
        "Hmm… mujhe samajh nahi aaya 😅",
        "Arey yaar, thoda confuse ho gaya 🤔",
        "Oops! Something went wrong 😶"
    ])
    return fallback

# -----------------------------
# Main function: human-like reply
# -----------------------------
async def get_human_reply(user_id: int, message_text: str):
    """
    Returns text + voice reply using multi-API routing with Hinglish output.
    """
    try:
        # 1️⃣ Fake typing simulation
        await fake_typing(user_id, message_text)

        # 2️⃣ Get reply from multi-API router
        reply_text = await get_mixed_reply(user_id, message_text)

        # 3️⃣ Log the conversation
        log_message(user_id=user_id, user_message=message_text, bot_reply=reply_text)

        # 4️⃣ Generate voice using ElevenLabs
        audio_bytes = await text_to_voice(reply_text)

        return reply_text, audio_bytes

    except Exception as e:
        logger.error(f"[HUMAN_REPLY] Failed to generate reply: {e}")
        fallback_reply = "Hmm… mujhe samajh nahi aaya 😅"
        return fallback_reply, None

# -----------------------------
# Optional: Quick test
# -----------------------------
if __name__ == "__main__":
    import asyncio

    async def test():
        user_id = 12345
        message = "Hey, kya haal hai?"
        text, audio = await get_human_reply(user_id, message)
        print("Text Reply:", text)
        print("Voice Bytes Length:", len(audio) if audio else 0)

    asyncio.run(test())