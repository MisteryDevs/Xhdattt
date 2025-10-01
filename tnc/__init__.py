from pyrogram import Client
from tnc.config import BOT_NAME, API_ID, API_HASH, BOT_TOKEN, LOG_FILE, LOG_LEVEL
import logging
import os

# -------------------------
# Logging configuration
# -------------------------
logger = logging.getLogger(BOT_NAME)
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

# Console handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# Optional: log to file (Heroku free dyno storage is ephemeral, so use stdout primarily)
if not os.path.exists("tnc/logs"):
    os.makedirs("tnc/logs")
fh = logging.FileHandler(LOG_FILE)
fh.setFormatter(formatter)
logger.addHandler(fh)

# -------------------------
# Pyrogram client setup
# -------------------------
app = Client(
    name=BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode="html",
    in_memory=True  # Optional: keeps session in memory for free dynos
)

logger.info(f"{BOT_NAME} Pyrogram client initialized successfully!")
