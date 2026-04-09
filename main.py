import time
import json
import os
from spotify_api import get_currently_playing, SpotifyTrack, download_image
from pathlib import Path

last_played_track = None
def main():
    img_dir = Path("imgs")
    img_dir.mkdir(exist_ok=True)
    
    if not os.path.exists('credentials.json'):
        print("Error: credentials.json not found. run app.py first")
        return

    current_track_id = None

    while True:
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
        
        access_token = creds.get('access_token')

        track = get_currently_playing(access_token)

        if isinstance(track, SpotifyTrack): 
            if track.is_playing:
                last_played_track = track
                if track.spotify_track_id != current_track_id:
                        current_track_id = track.spotify_track_id
                        if track.images:
                            img_url = track.images[1].url
                            temp_path = img_dir / "temp_art.jpg"
                            final_path = img_dir / "current_album_art.jpg"
                            
                            download_image(img_url, str(temp_path))
                            os.replace(temp_path, final_path)
            else:
                track = last_played_track
                track.is_playing = False

            progress_pct = track.progress_ms / track.duration_ms
            state = {
                "name": track.name,
                "artist": track.artist,
                "image_filename": "current_album_art.jpg",
                "progress": progress_pct,
                "is_playing": track.is_playing
            }

            with open('shared_state.json.tmp', 'w') as f:
                json.dump(state, f)
            os.replace('shared_state.json.tmp', 'shared_state.json')    

        time.sleep(1)

if __name__ == "__main__":
    main()


"""
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
            """