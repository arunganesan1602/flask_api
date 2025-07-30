import jwt
import time
import os

# ✅ Load LiveKit credentials from Render environment variables
LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET')

def generate_token(identity: str, room_name: str) -> str:
    """
    Generates a LiveKit access token using JWT.
    Args:
        identity (str): Unique participant ID (e.g., user ID)
        room_name (str): Room name in LiveKit (e.g., "support-room")

    Returns:
        str: LiveKit JWT token
    """
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
    """
    Placeholder function to simulate sending audio response back via LiveKit.
    You can replace this with actual TTS + audio streaming code.
    Args:
        text (str): Text to convert and send as voice
    """
    print(f"[LiveKit] Voice Response: {text}")

    # Optional: integrate Google TTS or any speech engine here
    # Example:
    # from gtts import gTTS
    # tts = gTTS(text)
    # tts.save("response.mp3")
    # then stream to LiveKit using SDK/WebRTC
