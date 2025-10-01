import logging
import os
from pyrogram import Client

# -------------------------
# Relative import of config
# -------------------------
from .config import BOT_NAME, API_ID, API_HASH, BOT_TOKEN, LOG_FILE, LOG_LEVEL

# -------------------------
# Logging configuration
# -------------------------
logger = logging.getLogger(BOT_NAME)
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

# Console handler (stdout)
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# File handler (optional: Heroku dyno storage is ephemeral)
log_dir = "tnc/logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
fh = logging.FileHandler(LOG_FILE)
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.info(f"{BOT_NAME} logging initialized!")

# -------------------------
# Pyrogram client setup
# -------------------------
app = Client(
    name=BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode="html",
    in_memory=True  # keeps session in memory for ephemeral dynos
)

logger.info(f"{BOT_NAME} Pyrogram client initialized successfully!")