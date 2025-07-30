from flask import Flask, request, jsonify
from simple_salesforce import Salesforce
import google.generativeai as genai
import os

app = Flask(__name__)

# Config for Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

# Salesforce credentials (use Render's environment variables)
sf = Salesforce(
    username=os.environ.get('SF_USERNAME'),
    password=os.environ.get('SF_PASSWORD'),
    security_token=os.environ.get('SF_TOKEN')
)

@app.route("/process", methods=["POST"])
def process_transcript():
    transcript = request.json.get("transcript", "")

    # Gemini: Extract Opportunity Name
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Extract only the Opportunity name from this question: '{transcript}'"
    response = model.generate_content(prompt)
    opp_name = response.text.strip().replace("'", "")

    # Salesforce: Query Opportunity Stage
    try:
        result = sf.query(f"SELECT StageName FROM Opportunity WHERE Name = '{opp_name}' LIMIT 1")
        if not result['records']:
            return jsonify({"reply": f"No opportunity found with name '{opp_name}'"})

        stage = result['records'][0]['StageName']
        return jsonify({"reply": f"The stage of Opportunity '{opp_name}' is {stage}."})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/", methods=["GET"])
def home():
    return "LiveKit + Gemini + Salesforce API is running."

if __name__ == "__main__":
    app.run(debug=True)
