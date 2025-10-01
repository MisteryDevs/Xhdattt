import openai
import logging
from .config import OPENAI_API_KEY

logger = logging.getLogger(__name__)
openai.api_key = OPENAI_API_KEY

async def chat_with_openai(prompt: str) -> str:
    """
    Sends a message to OpenAI API and returns the response text.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning(f"[OpenAI] Failed to get reply: {e}")
        return None
