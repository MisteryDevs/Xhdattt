# apis/__init__.py

import openai
from .sambanova import SambanovaClient
from .gemini import GeminiClient
from .elevenlabs import ElevenLabsClient
import config

# Initialize clients
sambanova_client = SambanovaClient(api_key=config.SAMBANOVA_API_KEY)
gemini_client = GeminiClient(api_key=config.GEMINI_API_KEY)
elevenlabs_client = ElevenLabsClient()

# OpenAI setup
openai.api_key = config.OPENAI_API_KEY

__all__ = [
    "sambanova_client",
    "gemini_client",
    "elevenlabs_client",
    "openai"
]
