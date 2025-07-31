from flask import Flask, request, jsonify
from simple_salesforce import Salesforce
from livekit_utils import send_audio_response
from gtts import gTTS
import os

app = Flask(__name__)

sf = Salesforce(
    username=os.getenv('SF_USERNAME'),
    password=os.getenv('SF_PASSWORD'),
    security_token=os.getenv('SF_SECURITY_TOKEN')
)

@app.route('/voice-query', methods=['POST'])
def handle_voice_query():
    data = request.json
    transcript = data.get('text')  # e.g. "What is the status of Opportunity Test Oppo"

    if not transcript:
        return jsonify({'error': 'No text found'}), 400

    # Basic extraction of Opportunity name
    trigger_phrase = "opportunity"
    opp_name = transcript.lower().split(trigger_phrase)[-1].strip().title()

    query = f"SELECT Name, StageName FROM Opportunity WHERE Name = '{opp_name}' LIMIT 1"
    results = sf.query(query)

    if results['totalSize'] > 0:
        stage = results['records'][0]['StageName']
        voice_text = f"The stage of opportunity {opp_name} is {stage}."
    else:
        voice_text = f"I couldn't find any opportunity with the name {opp_name}."

    # Use gTTS to convert to audio and send via LiveKit
    send_audio_response(voice_text)
    return jsonify({'message': voice_text}), 200
