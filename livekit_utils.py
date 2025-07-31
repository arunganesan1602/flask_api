import jwt
import time
import os
from gtts import gTTS
from playsound import playsound
import tempfile

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
    try:
        print(f"[LiveKit] Speaking: {text}")

        # Generate speech from text
        tts = gTTS(text=text, lang='en')

        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            audio_path = tmp_file.name

        # Play the audio
        playsound(audio_path)

        # Optional: Delete file after playing
        os.remove(audio_path)

    except Exception as e:
        print(f"Error generating voice response: {str(e)}")
