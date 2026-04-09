from flask import Flask, request, redirect
from urllib.parse import urlencode
import requests
from spotify_api import get_pkce_pair, get_currently_playing
import json

app = Flask(__name__)

store = {
    "client_id": "532289ccf4d5427fae80eae839a8319c",
    "redirect_uri": "http://127.0.0.1:8080/callback",
    "code_verifier": None
}

@app.route('/')
def login():
    verifier, challenge = get_pkce_pair(64)
    store["code_verifier"] = verifier
    
    params = {
        'response_type': 'code',
        'client_id': store["client_id"],
        'scope': 'user-read-private user-read-email user-read-currently-playing',
        'code_challenge_method': 'S256',
        'code_challenge': challenge,
        'redirect_uri': store["redirect_uri"],
    }
    
    auth_url = f"https://accounts.spotify.com/authorize?{urlencode(params)}"
    return f'Click to Authorize: <a href="{auth_url}">{auth_url}</a>'

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        'client_id': store["client_id"],
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': store["redirect_uri"],
        'code_verifier': store["code_verifier"],
    }

    response = requests.post(token_url, data=payload)
    res_data = response.json()

    if response.status_code == 200:
        with open('credentials.json', 'w') as f:
            json.dump(res_data, f)
            
        res_data['code_verifier'] = store["code_verifier"]
        with open('credentials.json', 'w') as f:
            json.dump(res_data, f)

        return "<h1>Token Saved! You can close this tab and check your terminal.</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)