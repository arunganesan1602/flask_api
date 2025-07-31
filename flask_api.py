# flask_api.py
from flask import Flask, request, jsonify, send_from_directory
from simple_salesforce import Salesforce
from livekit_utils import send_audio_response
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Salesforce connection
sf = Salesforce(
    username=os.getenv('SF_USERNAME'),
    password=os.getenv('SF_PASSWORD'),
    security_token=os.getenv('SF_SECURITY_TOKEN')
)

@app.route('/voice-query', methods=['POST'])
def handle_voice_query():
    data = request.json
    transcript = data.get('text')

    if not transcript:
        return jsonify({'error': 'No input text provided'}), 400

    try:
        # Extract opportunity name from voice text
        if "opportunity" in transcript.lower():
            opp_name = transcript.lower().split("opportunity")[-1].strip().title()
        else:
            opp_name = transcript.strip().title()

        query = f"SELECT Name, StageName FROM Opportunity WHERE Name = '{opp_name}' LIMIT 1"
        result = sf.query(query)

        if result['totalSize'] > 0:
            stage = result['records'][0]['StageName']
            response_text = f"The status of Opportunity {opp_name} is {stage}"
        else:
            response_text = f"No Opportunity named {opp_name} was found in Salesforce."

        send_audio_response(response_text)
        return jsonify({'message': response_text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve the audio response
@app.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    return send_from_directory('static/audio', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
