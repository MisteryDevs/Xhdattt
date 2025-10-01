import os
import json
import logging

# -------------------------
# Telegram Bot Configuration
# -------------------------
API_ID = int(os.getenv("API_ID", "123456"))             # Telegram API ID
API_HASH = os.getenv("API_HASH", "your_api_hash")      # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")  # Bot token
BOT_NAME = os.getenv("BOT_NAME", "TNC-Bot")           # Bot display name
BOT_OWNER = os.getenv("BOT_OWNER", "@SemxyCarders")   # Owner username

# -------------------------
# Support & Channel
# -------------------------
SUPPORT_CHAT = os.getenv("SUPPORT_CHAT_ID", "@YourSupportChat")  # Support chat
CHANNEL = os.getenv("CHANNEL_ID", "@YourChannel")                 # Channel for updates

# -------------------------
# Voice & ElevenLabs
# -------------------------
TNC_VOICE_ID = os.getenv("TNC_VOICE_ID", "your_voice_id")        # ElevenLabs voice ID

# Parse ElevenLabs API keys from JSON array string
elevenlabs_keys = os.getenv("ELEVENLABS_API_KEYS", "[]")
try:
    ELEVENLABS_API_KEYS = json.loads(elevenlabs_keys)
except Exception:
    ELEVENLABS_API_KEYS = []
    print("⚠️ Failed to parse ELEVENLABS_API_KEYS. Using empty list.")

# -------------------------
# AI APIs
# -------------------------
SAMNOVA_API_KEY = os.getenv("SAMNOVA_API_KEY", "your_samnova_key")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_key")

# -------------------------
# Logging Configuration
# -------------------------
LOG_FILE = os.getenv("LOG_FILE", "tnc/logs/bot.log")
LOG_LEVEL = getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO)

# -------------------------
# Optional Settings
# -------------------------
FAKE_TYPING_DELAY = float(os.getenv("FAKE_TYPING_DELAY", "1.5"))  # seconds