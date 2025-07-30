from flask import Flask, request, jsonify
import os
from simple_salesforce import Salesforce
from livekit_utils import send_audio_response
import re
from dotenv import load_dotenv

# Load environment variables from .env (for local testing)
load_dotenv()

app = Flask(__name__)

# Salesforce connection
try:
    sf = Salesforce(
        username=os.getenv('SF_USERNAME'),
        password=os.getenv('SF_PASSWORD'),
        security_token=os.getenv('SF_SECURITY_TOKEN'),
        domain=os.getenv('SF_DOMAIN')  # Use 'login' for production or 'test' for sandbox
    )
except Exception as e:
    print("Salesforce connection error:", str(e))
    sf = None

# Basic root check route (optional but good for debugging Render deployments)
@app.route('/')
def index():
    return "✅ Flask Voice API is running!"

# Main voice query endpoint
@app.route('/voice', methods=['POST'])
def voice_handler():
    if sf is None:
        return jsonify({'error': 'Salesforce connection not established'}), 500

    data = request.get_json()
    query = data.get("query", "")

    if "opportunity" in query.lower():
        try:
            # Extract Opportunity Name using regex (e.g., "opportunity Oppo1")
            match = re.search(r"opportunity\s+([A-Za-z0-9_\- ]+)", query, re.IGNORECASE)
            name = match.group(1).strip() if match else None

            if not name:
                return jsonify({'error': 'Opportunity name not found in query'}), 400

            # Query Salesforce
            opp_result = sf.query(f"SELECT Id, Name, StageName FROM Opportunity WHERE Name = '{name}' LIMIT 1")

            if opp_result['records']:
                stage = opp_result['records'][0]['StageName']
                # Send voice response
                send_audio_response(f"The stage of opportunity {name} is {stage}")
                return jsonify({'stage': stage})
            else:
                return jsonify({'error': f'Opportunity "{name}" not found'}), 404

        except Exception as e:
            return jsonify({'error': f'Processing error: {str(e)}'}), 500

    return jsonify({'error': 'Invalid query: only opportunity queries are supported'}), 400

# Run locally or on Render
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
