import os
import logging
import json

# -------------------------
# Telegram Bot Configuration
# -------------------------
API_ID = int(os.getenv("API_ID", "22657083"))          # Telegram API ID
API_HASH = os.getenv("API_HASH", "d6186691704bd901bdab275ceaab88f3")  # Telegram API Hash
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_NAME = "WaifuxGraber_bot"  # WRITE WITHOUT @
BOT_OWNER = os.getenv("BOT_OWNER", "@SemxyCarders")  # Owner username

# -------------------------
# Support & Channel
# -------------------------
SUPPORT_CHAT_ID = os.getenv("SUPPORT_CHAT_ID", "TechNodeCoders")  # Support chat
CHANNEL_ID = os.getenv("CHANNEL_ID", "TNCmeetup")                 # Channel for updates

# -------------------------
# Voice & ElevenLabs
# -------------------------
TNC_VOICE_ID = os.getenv("TNC_VOICE_ID", "DnThIAnAgyB5NKBqPQmh")  # ElevenLabs voice ID

# Corrected JSON parsing of multiple keys
ELEVENLABS_API_KEYS = []
elevenlabs_env = os.getenv(
    "ELEVENLABS_API_KEYS",
    '["sk_79ce62df7f5c28cf7c65f297d531c41b33429708ec0c6b72"]'
)
try:
    ELEVENLABS_API_KEYS = json.loads(elevenlabs_env)
except json.JSONDecodeError:
    ELEVENLABS_API_KEYS = []

# -------------------------
# AI APIs
# -------------------------
SAMBANOVA_API_KEY = os.getenv("SAMBANOVA_API_KEY", "41c87b5d-4a4d-4a8f-9544-48d9bfc9b06a")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCYvLrKc9tduBl_sQZpN9yEd5YQ1waDlMs")
OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    "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"
)

# -------------------------
# Logging Configuration
# -------------------------
LOG_FILE = "tnc/logs/bot.log"
LOG_LEVEL = logging.INFO  # INFO / WARNING / ERROR

handlers = [logging.StreamHandler()]  # Always log to console (Heroku-friendly)

# Try to also log to file (works locally, may not work on Heroku)
try:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    handlers.append(logging.FileHandler(LOG_FILE))
except Exception:
    pass  # Ignore if folder cannot be created (Heroku ephemeral FS)

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=handlers,
)

logger = logging.getLogger(__name__)

# -------------------------
# Optional Settings
# -------------------------
FAKE_TYPING_DELAY = float(os.getenv("FAKE_TYPING_DELAY", "1.5"))
