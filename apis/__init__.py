# apis/__init__.py
"""
Initialize all external API clients here:
- Samnova API
- Gemini API
- ElevenLabs API
- Any other custom APIs
"""

from .samnova import SamnovaClient
from .gemini import GeminiClient
from .elevenlabs import ElevenLabsClient

# Optional: create global instances
samnova_client = SamnovaClient(api_key="YOUR_SAMNOVA_KEY")
gemini_client = GeminiClient(api_key="YOUR_GEMINI_KEY")
# ElevenLabs will be used via voice_manager.py

__all__ = ["samnova_client", "gemini_client"]
