import json
import os
from tnc.log_utils import log_event

SETTINGS_FILE = "data/settings.json"

# Load settings from JSON
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"chats": {}}, f, indent=4)
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

# Save settings to JSON
def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Check if a toggle is enabled in a chat
def is_enabled(chat_id: int, toggle_name: str) -> bool:
    data = load_settings()
    return data.get("chats", {}).get(str(chat_id), {}).get(toggle_name, True)

# Toggle a setting for a chat
async def toggle(chat_id: int, toggle_name: str, value: bool):
    data = load_settings()
    if str(chat_id) not in data["chats"]:
        data["chats"][str(chat_id)] = {}
    data["chats"][str(chat_id)][toggle_name] = value
    save_settings(data)
    await log_event("TOGGLE_SETTING", extra=f"Chat {chat_id}: {toggle_name}={value}")