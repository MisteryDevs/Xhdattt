# tnc/voice_manager.py

from apis import elevenlabs_client

async def text_to_voice(text: str) -> bytes | None:
    """
    Converts Hinglish text to voice using the ElevenLabs client.
    """
    return await elevenlabs_client.text_to_voice(text)
