from flask import Flask, request, jsonify
import os
from simple_salesforce import Salesforce
from livekit_utils import send_audio_response
import re

app = Flask(__name__)

sf = Salesforce(
    username=os.getenv('SF_USERNAME'),
    password=os.getenv('SF_PASSWORD'),
    security_token=os.getenv('SF_SECURITY_TOKEN'),
    domain=os.environ.get('SF_DOMAIN')
)

@app.route('/voice', methods=['POST'])
def voice_handler():
    data = request.get_json()
    query = data.get("query", "")

    if "opportunity" in query.lower():
        try:
            # Extract Opportunity Name using regex
            match = re.search(r"Opportunity\s+([A-Za-z0-9_\- ]+)", query, re.IGNORECASE)
            name = match.group(1).strip() if match else None

            if not name:
                return jsonify({'error': 'Opportunity name not found in query'}), 400

            opp = sf.query(f"SELECT StageName FROM Opportunity WHERE Name = '{name}'")
            if opp['records']:
                stage = opp['records'][0]['StageName']
                send_audio_response(f"The stage of opportunity {name} is {stage}")
                return jsonify({'stage': stage})
            else:
                return jsonify({'error': 'Opportunity not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid query'}), 400
