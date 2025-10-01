import os
import logging
import json

# -------------------------
# Telegram Bot Configuration
# -------------------------
API_ID = int(os.getenv("API_ID", ""))          # Telegram API ID
API_HASH = os.getenv("API_HASH", "")   # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_NAME = "" # WRITE WITHOUT @
BOT_OWNER = os.getenv("BOT_OWNER", "@SemxyCarders") # Owner username

# -------------------------
# Support & Channel
# -------------------------
SUPPORT_CHAT_ID = os.getenv("SUPPORT_CHAT_ID", "")  # Support chat
CHANNEL_ID = os.getenv("CHANNEL_ID", "")                # Channel for updates

# -------------------------
# Voice & ElevenLabs
# -------------------------
TNC_VOICE_ID = os.getenv("TNC_VOICE_ID", "")   # ElevenLabs voice ID
ELEVENLABS_API_KEYS = json.loads(os.getenv("ELEVENLABS_API_KEYS, "", ""))  # JSON array of keys

# -------------------------
# AI APIs
# -------------------------
SAMNOVA_API_KEY = os.getenv("SAMNOVA_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

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