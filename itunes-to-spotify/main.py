import os
import re
from fuzzywuzzy import fuzz
import xml.etree.ElementTree as et
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def clean_track_title(title):
    cleaned_title = re.sub(r'[\/\-]', ' ', title)  # Replace \-/ with spaces
    cleaned_title = re.sub(r"[\'’]", '', cleaned_title)  # Delete both kinds of apostrophes
    cleaned_title = re.sub(r'\(.*\)', '', cleaned_title).strip()
    return cleaned_title

def find_best_track_match(tracks, query):
    best_match = None
    best_match_score = 0
    for track in tracks:
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        popularity = track['popularity']
        match_score = fuzz.partial_ratio(query.lower(), f"{artist_name} {track_name}".lower())
        if match_score > best_match_score or (match_score == best_match_score and popularity > best_match['popularity']):
            best_match = track
            best_match_score = match_score
    return best_match

def process_track(track):
    name, artist, album = None, None, None
    children = list(track)
    for i, child in enumerate(children):
        if child.tag == "key":
            if child.text == "Name" and i + 1 < len(children) and children[i + 1].tag == "string":
                name = children[i + 1].text
            elif child.text == "Artist" and i + 1 < len(children) and children[i + 1].tag == "string":
                artist = children[i + 1].text
            elif child.text == "Album" and i + 1 < len(children) and children[i + 1].tag == "string":
                album = children[i + 1].text
    return name, artist, album

def main():
    xml_file = input("Name of the iTunes playlist XML file: ")
    tree = et.parse(xml_file)
    root = tree.getroot()

    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='d2b73b9ffc8b40c79aef4890db82237a', client_secret='818c0389ed9648f289235ef7e0fcc946', redirect_uri='http://localhost:8888/callback', scope=scope))

    playlist_name = os.path.splitext(xml_file)[0]
    user_id = sp.current_user()['id']
    playlist_id = sp.user_playlist_create(user_id, playlist_name)['id']

    for track in root.findall("./dict/dict/dict"):
        name, artist, album = process_track(track)
        if name and artist:
            cleaned_name = clean_track_title(name)
            cleaned_album = clean_track_title(album)
            results = sp.search(q=f"track:{cleaned_name} artist:{artist} album:{cleaned_album}", type='track')
            tracks = results['tracks']['items']
            if not tracks:
                results = sp.search(q=f"track:{cleaned_name} artist:{artist}", type='track')
                tracks = results['tracks']['items']
                print(f"Search results for {artist} - {cleaned_name}: {tracks}") ### TODO delete
                best_track = find_best_track_match(tracks, f"{artist} {cleaned_name}")
                if best_track:
                    track_uri = best_track['uri']
                    sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])
                    print("Added", artist, "-", name, "to playlist.")
                else:
                    print("***", artist, "-", name, "could not be found. ***")
            if tracks:
                print(f"Search results for {artist} - {cleaned_name}: {tracks}") ### TODO delete
                best_track = find_best_track_match(tracks, f"{artist} {cleaned_name}")
                if best_track:
                    track_uri = best_track['uri']
                    sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])
                    print("Added", artist, "-", name, "to playlist.")
                else:
                    print("***", artist, "-", name, "could not be found. ***")

if __name__ == "__main__":
    main()