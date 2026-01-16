import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()

# ENV VARS (set in Clever Cloud)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "")

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"

SCOPES = "https://www.googleapis.com/auth/drive.readonly"

@app.get("/")
def root():
    return {
        "status": "running",
        "google_redirect_uri": REDIRECT_URI
    }

# 🔗 Open this to start OAuth
@app.get("/login/google")
def login_google():
    return RedirectResponse(
        f"{AUTH_URL}"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPES}"
        f"&access_type=offline"
        f"&prompt=consent"
    )

# 🔁 Google redirects here
@app.get("/oauth/google/callback")
def google_callback(request: Request):
    code = request.query_params.get("code")

    if not code:
        return HTMLResponse("<h3>❌ Authorization failed</h3>")

    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI
    }

    token_res = requests.post(TOKEN_URL, data=token_data).json()

    return HTMLResponse(f"""
        <h2>✅ Google OAuth Success</h2>
        <pre>{token_res}</pre>
        <p>You can close this window.</p>
    """)
