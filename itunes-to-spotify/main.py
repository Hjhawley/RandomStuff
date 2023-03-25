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
    for child in track:
        if child.tag == "key":
            if child.text == "Name":
                name = next(child.itertext())
            elif child.text == "Artist":
                artist = next(child.itertext())
            elif child.text == "Album":
                album = next(child.itertext())
    if name and artist:
        # Search for track on Spotify
        results = sp.search(q=f"track:{name} artist:{artist} album:{album}", type='track')
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])