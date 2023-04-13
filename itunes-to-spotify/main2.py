import os
import re
from fuzzywuzzy import fuzz
import xml.etree.ElementTree as et
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def clean_track_title(title):
    # Remove or replace special characters
    cleaned_title = re.sub(r'[\/\-]', '', title)
    # Remove text within parentheses
    cleaned_title = re.sub(r'\(.*\)', '', cleaned_title).strip()
    return cleaned_title

def find_best_track_match(tracks, query):
    best_match = None
    best_match_score = 0
    for track in tracks:
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        popularity = track['popularity']
        # Calculate the fuzzy string match score for the track
        match_score = fuzz.partial_ratio(query.lower(), f"{artist_name} {track_name}".lower())
        # Prioritize tracks with higher match scores and popularity
        if match_score > best_match_score or (match_score == best_match_score and popularity > best_match['popularity']):
            best_match = track
            best_match_score = match_score
    return best_match

def main():
    # Prompt user for name of iTunes playlist XML file
    xml_file = input("Name of the iTunes playlist XML file: ")

    # Load iTunes playlist XML
    tree = et.parse(xml_file)
    root = tree.getroot()

    # Authenticate with Spotify API
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='d2b73b9ffc8b40c79aef4890db82237a', client_secret='818c0389ed9648f289235ef7e0fcc946', redirect_uri='http://localhost:8888/callback', scope=scope))

    # Create a new Spotify playlist with the same name as the XML file
    playlist_name = os.path.splitext(xml_file)[0]
    user_id = sp.current_user()['id']
    playlist_id = sp.user_playlist_create(user_id, playlist_name)['id']

    # Iterate through iTunes playlist and add tracks to Spotify playlist
    for track in root.findall("./dict/dict/dict"):
        name = None
        artist = None
        album = None
        children = list(track)
        for i, child in enumerate(children):
            if child.tag == "key":
                if child.text == "Name" and i + 1 < len(children) and children[i + 1].tag == "string":
                    name = children[i + 1].text
                elif child.text == "Artist" and i + 1 < len(children) and children[i + 1].tag == "string":
                    artist = children[i + 1].text
                elif child.text == "Album" and i + 1 < len(children) and children[i + 1].tag == "string":
                    album = children[i + 1].text
        if name and artist:
            # Clean the track title
            cleaned_name = clean_track_title(name)
            # Search for the track on Spotify
            results = sp.search(q=f"track:{cleaned_name} artist:{artist} album:{album}", type='track')
            tracks = results['tracks']['items']
            if not tracks: # Search without the album information
                results = sp.search(q=f"track:{cleaned_name} artist:{artist}", type='track')
                tracks = results['tracks']['items']
            if tracks:
                # Find the best matching track
                best_track = find_best_track_match(tracks, f"{artist} {cleaned_name}")
                if best_track:
                    track_uri = best_track['uri']
                    sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])
                    print("Added", artist, "-", name, "to", xml_file)
                else:
                    print("***", artist, "-", name, "could not be found. ***")
            else:
                print("***", artist, "-", name, "could not be found. ***")

main()