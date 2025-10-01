"""
Initialize all external API clients here:
- Sambanova API
- Gemini API
- ElevenLabs API
- OpenAI API
"""

import openai
from .sambanova import SambanovaClient  # replaced samnova -> sambanova
from .gemini import GeminiClient
from .elevenlabs import ElevenLabsClient

# -------------------------
# API Keys (replace with your actual keys)
# -------------------------
SAMBANOVA_KEY = "YOUR_SAMBANOVA_KEY"  # updated
GEMINI_KEY = "YOUR_GEMINI_KEY"
OPENAI_KEY = "YOUR_OPENAI_KEY"

# -------------------------
# Initialize clients
# -------------------------
sambanova_client = SambanovaClient(api_key=SAMBANOVA_KEY)  # updated
gemini_client = GeminiClient(api_key=GEMINI_KEY)
elevenlabs_client = ElevenLabsClient()  # Use via voice_manager.py

# OpenAI setup
openai.api_key = OPENAI_KEY

__all__ = [
    "sambanova_client",  # updated
    "gemini_client",
    "elevenlabs_client",
    "openai"
]