import os
import logging
import json

# -------------------------
# Telegram Bot Configuration
# -------------------------
API_ID = int(os.getenv("API_ID", "123456"))          # Telegram API ID
API_HASH = os.getenv("API_HASH", "your_api_hash")   # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
BOT_NAME = "TNC-Bot"
BOT_OWNER = os.getenv("BOT_OWNER", "@SemxyCarders") # Owner username

# -------------------------
# Support & Channel
# -------------------------
SUPPORT_CHAT_ID = os.getenv("SUPPORT_CHAT_ID", "@YourSupportChat")  # Support chat
CHANNEL_ID = os.getenv("CHANNEL_ID", "@YourChannel")                # Channel for updates

# -------------------------
# Voice & ElevenLabs
# -------------------------
TNC_VOICE_ID = os.getenv("TNC_VOICE_ID", "your_voice_id")   # ElevenLabs voice ID
ELEVENLABS_API_KEYS = json.loads(os.getenv("ELEVENLABS_API_KEYS", '[]'))  # JSON array of keys

# -------------------------
# AI APIs
# -------------------------
SAMNOVA_API_KEY = os.getenv("SAMNOVA_API_KEY", "your_samnova_key")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_key")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_key")

# -------------------------
# Logging Configuration
# -------------------------
LOG_FILE = "tnc/logs/bot.log"
LOG_LEVEL = logging.INFO  # INFO / WARNING / ERROR

# Setup logger
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# -------------------------
# Optional Settings
# -------------------------
# Fake typing delay in seconds
FAKE_TYPING_DELAY = float(os.getenv("FAKE_TYPING_DELAY", "1.5"))