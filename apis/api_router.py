import random
from apis import samnova_client, gemini_client, openai

async def get_mixed_reply(user_id: int, message: str) -> str:
    """
    Routes a message to multiple APIs (Samnova, Gemini, OpenAI)
    and returns a combined human-like reply in Hinglish.

    Priority/Fallback:
    1. Samnova
    2. Gemini
    3. OpenAI
    """

    # Try Samnova first
    try:
        samnova_reply = await samnova_client.get_reply(message)
        if samnova_reply:
            return samnova_reply
    except Exception as e:
        print(f"[API_ROUTER] Samnova failed: {e}")

    # Fallback to Gemini
    try:
        gemini_reply = await gemini_client.chat(message)
        if gemini_reply:
            return gemini_reply
    except Exception as e:
        print(f"[API_ROUTER] Gemini failed: {e}")

    # Fallback to OpenAI GPT
    try:
        import openai
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}],
            temperature=0.7,
            max_tokens=200
        )
        openai_reply = completion.choices[0].message.content
        if openai_reply:
            return openai_reply
    except Exception as e:
        print(f"[API_ROUTER] OpenAI failed: {e}")

    # If all fail, return a generic fallback
    fallback_replies = [
        "Hmm… mujhe samajh nahi aaya 😅",
        "Arey yaar, thoda confuse ho gaya 🤔",
        "Oops! Something went wrong 😶"
    ]
    return random.choice(fallback_replies)
