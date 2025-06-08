import os
import json
import base64
import hashlib
import secrets
import requests
import webbrowser
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
load_dotenv()


# Spotify App Configuration
CLIENT_ID = os.getenv("CLIENT_ID1")
REDIRECT_URI = os.getenv("REDIRECT_URL")
SCOPE = "user-modify-playback-state user-read-playback-state user-library-modify"

def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)
    code_verifier = code_verifier[:128]  # Max 128 chars

    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode('utf-8')

    return code_verifier, code_challenge

def authenticate():
    code_verifier, code_challenge = generate_pkce_pair()

    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE.replace(' ', '%20')}"
        f"&code_challenge_method=S256"
        f"&code_challenge={code_challenge}"
    )

    print("🔗 Open this URL in your browser to authorize Spotify:")
    print(auth_url)
    webbrowser.open(auth_url)

    redirect_response = input("\n📋 Paste the FULL redirect URL here:\n")
    parsed = urlparse(redirect_response)
    code = parse_qs(parsed.query).get("code", [None])[0]

    if not code:
        print("❌ Failed to extract code from URL.")
        return

    # Exchange code for tokens
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": code_verifier
    }

    response = requests.post(token_url, data=data)

    if response.status_code == 200:
        token_info = response.json()
        with open("token_info.json", "w") as f:
            json.dump(token_info, f, indent=2)
        print("✅ Authentication successful! token_info.json saved.")
    else:
        print("❌ Token request failed:")
        print(response.text)

if __name__ == "__main__":
    authenticate()
