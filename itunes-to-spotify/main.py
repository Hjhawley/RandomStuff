import os
import xml.etree.ElementTree as et
import spotipy
from spotipy.oauth2 import SpotifyOAuth

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
        # Search for track on Spotify
        results = sp.search(q=f"track:{name} artist:{artist} album:{album}", type='track')
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])
            print("Added", artist, "-", name, "to", xml_file)
        else: # Grab an alternate version of the track if necessary
            results = sp.search(q=f"track:{name} artist:{artist}", type='track')
            if results['tracks']['items']:
                track_uri = results['tracks']['items'][0]['uri']
                sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])
                print("Added", artist, "-", name, "to", xml_file)
            else:
                print("***", artist, "-", name, "could not be found. ***")