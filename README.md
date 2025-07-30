# Voice Assistant Backend (Salesforce + LiveKit)

This Flask app connects Salesforce with LiveKit to handle voice queries like:
> "What is the stage of Opportunity Oppo1?"

## Technologies
- Python (Flask)
- Salesforce (via simple-salesforce)
- LiveKit (Voice Communication)
- JWT (for LiveKit token)
- Render.com (Deployment)

## API Endpoint
- `POST /voice`: Triggers Opportunity voice lookup

## Deployment
Auto-deployed on Render via `.render.yaml`.
