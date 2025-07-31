# livekit_utils.py
import os
from gtts import gTTS

AUDIO_DIR = os.path.join("static", "audio")
AUDIO_FILENAME = "last_response.mp3"

def send_audio_response(text):
    """
    Converts the given text to speech using gTTS and saves it as an MP3 file
    """
    os.makedirs(AUDIO_DIR, exist_ok=True)
    file_path = os.path.join(AUDIO_DIR, AUDIO_FILENAME)

    try:
        tts = gTTS(text=text)
        tts.save(file_path)
        print(f"[✅] Audio response saved to: {file_path}")
    except Exception as e:
        print(f"[❌] Error generating audio: {e}")
