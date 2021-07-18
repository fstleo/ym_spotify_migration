import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from yandex_music import Client
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
scope = os.getenv('SCOPE')

print("Enter Y.Music login")
login = input()
print("Enter Y.Music password")
password = input()

ym = Client.from_credentials(login, password)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

saved_tracks = ym.users_likes_tracks()
playlist = sp.current_user_playlists(limit=20)["items"][0]

not_found = open("not_found.txt", "a", encoding="utf-8")

skip_until_album_id = None
skip_until_id = None
add = False
print("Found " + str(len(saved_tracks)) + " saved tracks")
for track in saved_tracks:
    print(track)
    track_ym_id = track["id"]
    album_id = track["album_id"]
    print(track_ym_id)
    print(album_id)
    if (track_ym_id == skip_until_id) and (album_id == skip_until_album_id):
        add = True
        print("Start from next")
        continue
    if not add:
        print("Skip")
        continue
    track_info = track.fetch_track()

    print(track_info)

    title = track_info["title"]
    if title is None:
        continue
    artists = track_info["artists"]
    if len(artists) == 0:
        not_found.write(title + " no artist? \n")
        continue

    artist = artists[0]["name"]
    search = title + " " + artist

    print(search)

    search_results = sp.search(search, type="track")["tracks"]["items"]
    if len(search_results) > 0:
        search_result = search_results[0]
        print(search_result)
        track_id = search_result["uri"]
        print(track_id)
        tracks = [track_id]
        sp.current_user_saved_tracks_add(tracks)
    else:
        not_found.write(search + "\n")

not_found.close()
