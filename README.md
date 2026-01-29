# GitHub Webhook Receiver (Flask)

This app receives GitHub webhook events (push, pull request, merge),
stores them in MongoDB, and shows recent activity on a simple UI.

## How to run

1. Create & activate virtual env  
   `python -m venv venv`  
   `venv\Scripts\activate` (Windows) / `source venv/bin/activate`

2. Install deps  
   `pip install -r requirements.txt`

3. Create `.env` and copy env from `.env.local`

4. Compile UI  
   `tsc .\app\static\app.ts `

5. Run app  
   `python run.py`

## Webhook

Expose locally using ngrok:
`ngrok http 5000`

Use this URL in GitHub webhook:
`/webhook/receiver`
