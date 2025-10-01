import json
import os
from datetime import datetime
from tnc import config
from tnc.log_utils import log_event

AFK_FILE = "data/afk.json"

# Load AFK data
def load_afk():
    if not os.path.exists(AFK_FILE):
        with open(AFK_FILE, "w") as f:
            json.dump({"users": {}, "chats": {}}, f)
    with open(AFK_FILE, "r") as f:
        return json.load(f)

# Save AFK data
def save_afk(data):
    with open(AFK_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Set user AFK
async def set_afk(user_id: int, reason: str = ""):
    data = load_afk()
    data["users"][str(user_id)] = {
        "is_afk": True,
        "reason": reason,
        "since": datetime.utcnow().isoformat()
    }
    save_afk(data)
    await log_event("SET_AFK", extra=f"User {user_id} set AFK. Reason: {reason}")

# Remove user AFK
async def remove_afk(user_id: int):
    data = load_afk()
    if str(user_id) in data["users"]:
        data["users"][str(user_id)]["is_afk"] = False
        data["users"][str(user_id)]["reason"] = ""
        data["users"][str(user_id)]["since"] = ""
        save_afk(data)
        await log_event("REMOVE_AFK", extra=f"User {user_id} is no longer AFK")

# Handle mentions of AFK users
async def handle_afk_mention(message):
    data = load_afk()
    if not data.get("chats", {}).get(str(message.chat.id), {}).get("afk_enabled", True):
        return  # AFK disabled in this chat

    mentioned_users = [u.id for u in message.entities if hasattr(u, "user") and u.user]
    for user_id in mentioned_users:
        user_afk = data["users"].get(str(user_id))
        if user_afk and user_afk.get("is_afk"):
            reason = user_afk.get("reason", "AFK")
            since = user_afk.get("since", "")
            reply = f"⚠️ User is AFK since {since}.\nReason: {reason}"
            await message.reply_text(reply)
            await log_event("AFK_MENTION", message=message, extra=f"User {user_id} mentioned")