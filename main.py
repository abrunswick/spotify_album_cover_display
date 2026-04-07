import time
import json
import os
from realthing import get_currently_playing, SpotifyTrack, download_image

def main():
    if not os.path.exists('credentials.json'):
        print("Error: credentials.json not found. Run app.py first!")
        return

    current_track_id = None

    while True:
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
        
        access_token = creds.get('access_token')

        track = get_currently_playing(access_token)

        if track and track.is_playing and track.spotify_track_id != current_track_id:
            current_track_id = track.spotify_track_id
        
            if track.images:
                img_url = track.images[1].url
                #print(f"Downloading new art: {track.name}...")
                
                download_image(img_url, "current_album_art.jpg")

        os.system('clear')

        
        print("ipod display with imagination <3")
        
        if isinstance(track, SpotifyTrack):
            progress = (track.progress_ms / track.duration_ms) * 100
            print(f"Song:   {track.name}")
            print(f"Artist: {track.artist}")
            print(f"Album:  {track.album_name}\n")
            print(f"Track {track.track_number} of {track.album_total_tracks}\n")
            print(f"[{'#' * int(progress/5)}{'-' * (20 - int(progress/5))}] {progress:.1f}%")
            for img in track.images:
                print(f"Found {img.width}x{img.height} image at {img.url}")
        elif isinstance(track, str):
            print(f"Status: {track}")
        
        time.sleep(1)

if __name__ == "__main__":
    main()