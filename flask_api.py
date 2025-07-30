from flask import Flask, request, jsonify
import os
from simple_salesforce import Salesforce
from livekit_utils import send_audio_response

app = Flask(__name__)

# Salesforce credentials from Render environment variables
sf = Salesforce(
    username=os.getenv('SF_USERNAME'),
    password=os.getenv('SF_PASSWORD'),
    security_token=os.getenv('SF_TOKEN'),
    domain='login'
)

@app.route('/voice', methods=['POST'])
def voice_handler():
    # Simulated voice query (replace with actual transcript later)
    query = "What is the stage of Opportunity Oppo1?"

    if "opportunity" in query.lower():
        try:
            name = query.split("Opportunity ")[1].replace("?", "").strip()
            opp = sf.query(f"SELECT StageName FROM Opportunity WHERE Name = '{name}'")
            stage = opp['records'][0]['StageName'] if opp['records'] else 'Not Found'

            send_audio_response(f"The stage of opportunity {name} is {stage}")
            return jsonify({'stage': stage})
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'error': 'Invalid query'})
