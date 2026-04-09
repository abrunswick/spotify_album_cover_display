import os
import base64
import json
from dotenv import load_dotenv
import requests
import secrets
import string 
import hashlib
from dataclasses import dataclass
from typing import List

@dataclass
class SpotifyImage:
    url: str
    height: int
    width: int

@dataclass
class SpotifyTrack:
    name: str
    album_name: str
    artist: str
    spotify_track_id: str
    album_total_tracks: int
    track_number: int
    is_playing: bool
    progress_ms: int
    duration_ms: int
    images: List[SpotifyImage]

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_pkce_pair(length):
    possible = string.ascii_letters + string.digits
    verifier = ''.join(secrets.choice(possible) for _ in range(length))
    sha_hash = hashlib.sha256(verifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(sha_hash).decode('utf-8').rstrip('=')
    
    return verifier, challenge

def get_currently_playing(access_token):
    #https://developer.spotify.com/documentation/web-api/reference/get-the-users-currently-playing-track
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 204:
        return SpotifyTrack(
                name="",
                album_name="",
                artist="",
                spotify_track_id="",
                album_total_tracks=0,
                track_number=0,
                is_playing=False,
                progress_ms=0,
                duration_ms=0,
                images=None
            )
    
    if response.status_code == 200:
        data = response.json()
        item = data.get('item')

        if item:
            raw_images = item['album'].get('images', [])
            image_objects = [
                SpotifyImage(url=img['url'], height=img['height'], width=img['width']) 
                for img in raw_images
            ]

            return SpotifyTrack(
                name=item['name'],
                album_name=item['album']['name'],
                artist=item['artists'][0]['name'],
                spotify_track_id=item['id'],
                album_total_tracks=item['album']['total_tracks'],
                track_number=item['track_number'],
                is_playing=data['is_playing'],
                progress_ms=data['progress_ms'],
                duration_ms=item['duration_ms'],
                images=image_objects 
            )
    return None

def download_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
    except Exception as e:
        print(f"Download failed: {e}")
    
    return False
