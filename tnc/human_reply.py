import random
import asyncio
from tnc.config import SAMNOVA_API_KEY, GEMINI_API_KEY, OPENAI_API_KEY, logger
import aiohttp
import json

# -----------------------------
# Samnova API (Hinglish)
# -----------------------------
async def samnova_reply(prompt: str, user_id: int) -> str:
    prompt = f"Reply in friendly Hinglish: {prompt}"
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {SAMNOVA_API_KEY}"}
            payload = {"prompt": prompt, "user_id": user_id}
            async with session.post("https://api.samnova.ai/chat", json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("reply", "")
    except Exception as e:
        logger.warning(f"Samnova API error: {e}")
    return None

# -----------------------------
# Gemini API (Hinglish)
# -----------------------------
async def gemini_reply(prompt: str, user_id: int) -> str:
    prompt = f"Reply in friendly Hinglish: {prompt}"
    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {GEMINI_API_KEY}"}
            payload = {"prompt": prompt, "user_id": user_id}
            async with session.post("https://api.gemini.ai/v1/chat", json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("reply", "")
    except Exception as e:
        logger.warning(f"Gemini API error: {e}")
    return None

# -----------------------------
# OpenAI API (Hinglish)
# -----------------------------
async def openai_reply(prompt: str, user_id: int) -> str:
    prompt = f"Reply in friendly Hinglish: {prompt}"
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            user=str(user_id)
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning(f"OpenAI API error: {e}")
    return None

# -----------------------------
# Main human-like reply
# -----------------------------
async def get_human_reply(prompt: str, user_id: int) -> str:
    """
    Tries Samnova → Gemini → OpenAI → fallback.
    Returns a Hinglish string reply for the user.
    """
    reply = await samnova_reply(prompt, user_id)
    if reply:
        return reply

    reply = await gemini_reply(prompt, user_id)
    if reply:
        return reply

    reply = await openai_reply(prompt, user_id)
    if reply:
        return reply

    # Fallback generic Hinglish replies
    fallback_replies = [
        "Arey wah 😏, ye toh interesting hai!",
        "Accha? Batao aur 😜",
        "Hmm, samajh gaya 😅, aur bolo",
        "Haha really? Batao thoda aur 💖",
        "Kya baat hai! 😎"
    ]
    return random.choice(fallback_replies)
