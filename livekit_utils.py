import os
import jwt  # PyJWT library

LIVEKIT_API_KEY = os.getenv('LIVEKIT_API_KEY')
LIVEKIT_API_SECRET = os.getenv('LIVEKIT_API_SECRET')

def generate_livekit_token(identity, room_name):
    payload = {
        "iss": LIVEKIT_API_KEY,
        "sub": "voice-assistant",
        "aud": "livekit",
        "exp": int(time.time()) + 3600,
        "room": room_name,
        "identity": identity
    }

    token = jwt.encode(payload, LIVEKIT_API_SECRET, algorithm='HS256')
    return token
