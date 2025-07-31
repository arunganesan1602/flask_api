from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from simple_salesforce import Salesforce
from livekit_utils import send_audio_response
import os

app = Flask(__name__)
CORS(app)

# Load environment variables (replace with actual values or use dotenv)
sf = Salesforce(
    username=os.getenv("SF_USERNAME"),
    password=os.getenv("SF_PASSWORD"),
    security_token=os.getenv("SF_SECURITY_TOKEN"),
    domain='login'
)

@app.route('/voice', methods=['POST'])
def voice_query():
    try:
        data = request.get_json()
        query = data.get("query", "")
        print("Received query:", query)

        # Extract Opportunity name from query using simple logic
        if "opportunity" in query.lower():
            opp_name = query.split("opportunity")[-1].strip().replace("?", "")
        else:
            return jsonify({"error": "No Opportunity name found."})

        # Query Salesforce
        result = sf.query(f"SELECT StageName FROM Opportunity WHERE Name = '{opp_name}'")
        records = result.get("records", [])

        if not records:
            return jsonify({"error": f"No Opportunity found with name '{opp_name}'"})

        stage = records[0]["StageName"]
        response_text = f"The stage of opportunity {opp_name} is {stage}."

        # Convert to voice and return file path
        audio_path = send_audio_response(response_text)

        return jsonify({
            "stage": stage,
            "audio_url": audio_path
        })

    except Exception as e:
        return jsonify({"error": str(e)})

# Serve audio files
@app.route('/static/audio/<filename>')
def serve_audio(filename):
    return send_from_directory('static/audio', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
