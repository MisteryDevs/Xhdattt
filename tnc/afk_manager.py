import json
import os
from tnc.logger import logger
from tnc.config import BOT_OWNER

AFK_FILE = "data/afk.json"

# Ensure AFK file exists
if not os.path.exists(AFK_FILE):
    with open(AFK_FILE, "w") as f:
        json.dump({}, f)

def set_afk(user_id: int, reason: str = None):
    """Mark a user as AFK with optional reason."""
    with open(AFK_FILE, "r") as f:
        afk_data = json.load(f)

    afk_data[str(user_id)] = reason or "AFK"
    with open(AFK_FILE, "w") as f:
        json.dump(afk_data, f)
    
    logger.info(f"User {user_id} is now AFK. Reason: {reason}")

def remove_afk(user_id: int):
    """Remove AFK status for a user."""
    with open(AFK_FILE, "r") as f:
        afk_data = json.load(f)

    if str(user_id) in afk_data:
        del afk_data[str(user_id)]
        with open(AFK_FILE, "w") as f:
            json.dump(afk_data, f)
        logger.info(f"User {user_id} is no longer AFK.")

def check_afk(user_id: int) -> str | None:
    """Check if user is AFK, return reason or None."""
    with open(AFK_FILE, "r") as f:
        afk_data = json.load(f)
    
    return afk_data.get(str(user_id))

def afk_auto_reply(sender_id: int) -> str:
    """Return an auto-reply message if sender is messaging AFK user."""
    reason = check_afk(sender_id)
    if reason:
        return f"I'm currently AFK 😴. Reason: {reason}"
    return None
