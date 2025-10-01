"""
Initialize all external API clients here:
- Samnova API
- Gemini API
- ElevenLabs API
- OpenAI API
"""

import openai
from .samnova import SamnovaClient
from .gemini import GeminiClient
from .elevenlabs import ElevenLabsClient

# -------------------------
# API Keys (replace with your actual keys)
# -------------------------
SAMNOVA_KEY = "YOUR_SAMNOVA_KEY"
GEMINI_KEY = "YOUR_GEMINI_KEY"
OPENAI_KEY = "YOUR_OPENAI_KEY"

# -------------------------
# Initialize clients
# -------------------------
samnova_client = SamnovaClient(api_key=SAMNOVA_KEY)
gemini_client = GeminiClient(api_key=GEMINI_KEY)
elevenlabs_client = ElevenLabsClient()  # Use via voice_manager.py

# OpenAI setup
openai.api_key = OPENAI_KEY

__all__ = [
    "samnova_client",
    "gemini_client",
    "elevenlabs_client",
    "openai"
]