import json
import os
from tnc.log_utils import log_event

SETTINGS_FILE = "data/settings.json"

# Load chat settings
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"chats": {}}, f)
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

# Save chat settings
def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Check if chatbot is enabled in a chat
def is_chatbot_enabled(chat_id: int) -> bool:
    data = load_settings()
    return data.get("chats", {}).get(str(chat_id), {}).get("chatbot_enabled", True)

# Toggle chatbot in a chat
async def toggle_chatbot(chat_id: int, enabled: bool):
    data = load_settings()
    if str(chat_id) not in data["chats"]:
        data["chats"][str(chat_id)] = {}
    data["chats"][str(chat_id)]["chatbot_enabled"] = enabled
    save_settings(data)
    await log_event("TOGGLE_CHATBOT", extra=f"Chat {chat_id} chatbot_enabled={enabled}")