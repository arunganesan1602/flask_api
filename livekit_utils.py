import jwt
import time
import os

# Load LiveKit credentials from environment
LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET')

def generate_token(identity: str, room_name: str) -> str:
    now = int(time.time())
    payload = {
        "iss": LIVEKIT_API_KEY,
        "sub": identity,
        "aud": "livekit",
        "nbf": now,
        "exp": now + 3600,
        "room": room_name,
        "video": False,
        "audio": True,
    }

    token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm="HS256")
    return token


def send_audio_response(text: str):
    print(f"[LiveKit] Voice Response: {text}")
    # Optional: Use gTTS or other TTS to convert to speech
