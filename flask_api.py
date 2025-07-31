from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from simple_salesforce import Salesforce
from livekit_utils import send_audio_response
import re
from dotenv import load_dotenv

# Load environment variables from .env (for local testing)
load_dotenv()

app = Flask(__name__)
CORS(app)

# Salesforce connection
try:
    sf = Salesforce(
        username=os.getenv('SF_USERNAME'),
        password=os.getenv('SF_PASSWORD'),
        security_token=os.getenv('SF_SECURITY_TOKEN'),
        domain=os.getenv('SF_DOMAIN')  # 'login' for production or 'test' for sandbox
    )
except Exception as e:
    print("Salesforce connection error:", str(e))
    sf = None

@app.route('/')
def index():
    return "✅ Flask Voice API is running!"

@app.route('/voice', methods=['POST'])
def voice_handler():
    if sf is None:
        return jsonify({'error': 'Salesforce connection not established'}), 500

    data = request.get_json()
    query = data.get("query", "").strip()

    if not query:
        return jsonify({'error': 'Query is empty'}), 400

    if "opportunity" in query.lower():
        try:
            # Extract Opportunity Name using regex (e.g., "opportunity Test Oppo")
            match = re.search(r"opportunity\s+([A-Za-z0-9_\- ]+)", query, re.IGNORECASE)
            name = match.group(1).strip() if match else None

            if not name:
                return jsonify({'error': 'Opportunity name not found in query'}), 400

            # Query Salesforce for Opportunity
            opp_result = sf.query(f"SELECT Id, Name, StageName FROM Opportunity WHERE Name = '{name}' LIMIT 1")

            if opp_result['records']:
                stage = opp_result['records'][0]['StageName']
                response_text = f"The stage of opportunity {name} is {stage}."
                send_audio_response(response_text)
                return jsonify({'stage': stage})
            else:
                error_msg = f'Opportunity "{name}" not found in Salesforce.'
                send_audio_response(error_msg)
                return jsonify({'error': error_msg}), 404

        except Exception as e:
            error_msg = f'Processing error: {str(e)}'
            send_audio_response(error_msg)
            return jsonify({'error': error_msg}), 500

    return jsonify({'error': 'Only Opportunity queries are supported'}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
