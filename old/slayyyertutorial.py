import os
import base64
import json
from dotenv import load_dotenv
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    result = post(url, headers=headers, data=data)
    json_result = result.json()
    return json_result.get("access_token")

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    # CORRECT URL
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {"q": artist_name, "type": "artist", "limit": 1}

    result = get(url, headers=headers, params=params)
    json_result = result.json().get("artists", {}).get("items", [])
    
    if not json_result:
        print("No artists found.")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, artist_name):
    # We use the search endpoint to find tracks by the artist name
    # query format: 'artist:Artist Name'
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    params = {
        "q": f"artist:{artist_name}",
        "type": "track",
        "limit": 10
    }
    
    result = get(url, headers=headers, params=params)
    
    if result.status_code != 200:
        print(f"Error fetching tracks: {result.status_code}")
        return []
        
    return result.json().get("tracks", {}).get("items", [])

# Execution
token = get_token()
if token:
    artist_name = "Slayyyter"
    artist = search_for_artist(token, artist_name)
    
    if artist:
        print(f"Found Artist ID: {artist['id']}")
        # Use the search-based song fetcher
        songs = get_songs_by_artist(token, artist_name)
        
        if songs:
            for idx, song in enumerate(songs):
                print(f"{idx + 1}. {song['name']}")
        else:
            print("No songs found.")
else:
    print("Failed to retrieve token.")