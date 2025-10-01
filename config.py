import os
import logging
import json

# -------------------------
# Telegram Bot Configuration
# -------------------------
API_ID = int(os.getenv("API_ID", "22657083"))          # Telegram API ID
API_HASH = os.getenv("API_HASH", "d6186691704bd901bdab275ceaab88f3")         # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_NAME = "WaifuxGraber_bot"  # WRITE WITHOUT @
BOT_OWNER = os.getenv("BOT_OWNER", "@SemxyCarders")  # Owner username

# -------------------------
# Support & Channel
# -------------------------
SUPPORT_CHAT_ID = os.getenv("SUPPORT_CHAT_ID", "TechNodeCoders")  # Support chat
CHANNEL_ID = os.getenv("CHANNEL_ID", "TNCmeetup")            # Channel for updates

# -------------------------
# Voice & ElevenLabs
# -------------------------
TNC_VOICE_ID = os.getenv("TNC_VOICE_ID", "")  # ElevenLabs voice ID

# Corrected JSON parsing of multiple keys
ELEVENLABS_API_KEYS = []
elevenlabs_env = os.getenv("ELEVENLABS_API_KEYS", '[""]')
try:
    ELEVENLABS_API_KEYS = json.loads(elevenlabs_env)
except json.JSONDecodeError:
    ELEVENLABS_API_KEYS = []

# -------------------------
# AI APIs
# -------------------------
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY", "")  # updated
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