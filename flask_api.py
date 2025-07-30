from flask import Flask, request, jsonify
import requests
from simple_salesforce import Salesforce
import openai
from livekit import send_audio_response  # Your own LiveKit function

app = Flask(__name__)

# Salesforce credentials
sf = Salesforce(
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD',
    security_token='YOUR_SECURITY_TOKEN',
    domain='login'
)

@app.route('/voice', methods=['POST'])
def voice_handler():
    # 1. Get transcripted voice (simulate)
    query = "What is the stage of Opportunity Oppo1?"

    # 2. Use Gemini/OpenAI to extract intent
    # Simulate using simple parsing
    if "opportunity" in query.lower():
        name = query.split("Opportunity ")[1].replace("?", "").strip()

        # 3. Query Salesforce
        opp = sf.query(f"SELECT StageName FROM Opportunity WHERE Name = '{name}'")
        stage = opp['records'][0]['StageName'] if opp['records'] else 'Not Found'

        # 4. Send voice back via LiveKit
        send_audio_response(f"The stage of opportunity {name} is {stage}")

        return jsonify({'stage': stage})

    return jsonify({'error': 'Invalid query'})
