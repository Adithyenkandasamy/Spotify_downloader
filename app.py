import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

# ===== YOUR SPOTIFY API CREDENTIALS =====
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# ===== Authenticate with Spotify API =====
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# ===== Create folder for previews =====
SAVE_FOLDER = "spotify_previews"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# ===== Function to download a preview =====
def download_preview(track):
    track_name = track["name"].replace("/", "-")
    artist_name = track["artists"][0]["name"].replace("/", "-")
    preview_url = track["preview_url"]

    if preview_url:
        file_path = os.path.join(SAVE_FOLDER, f"{track_name} - {artist_name}.mp3")
        r = requests.get(preview_url)
        with open(file_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Downloaded preview: {track_name} - {artist_name}")
    else:
        print(f"❌ No preview available for: {track_name} - {artist_name}")

# ===== Main function to process a playlist =====
def download_playlist_previews(playlist_url):
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"]

    while results["next"]:  # Handle playlists with more than 100 tracks
        results = sp.next(results)
        tracks.extend(results["items"])

    print(f"🎵 Found {len(tracks)} tracks in playlist.\n")

    for item in tracks:
        track = item["track"]
        download_preview(track)

# ===== Example usage =====
if __name__ == "__main__":
    playlist_link = input("Enter Spotify playlist URL: ").strip()
    download_playlist_previews(playlist_link)
    print("\n✅ All previews processed!")
