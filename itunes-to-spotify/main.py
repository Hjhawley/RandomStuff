import xml.etree.ElementTree as et
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load iTunes playlist XML
tree = et.parse('iTunesPlaylist.xml')
root = tree.getroot()

# Authenticate with Spotify API
scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Create a new Spotify playlist
playlist_name = 'My New Playlist'
user_id = sp.current_user()['id']
playlist_id = sp.user_playlist_create(user_id, playlist_name)['id']

# Iterate through iTunes playlist and add tracks to Spotify playlist
for track in root.findall("./dict/dict/dict"):
    name = None
    artist = None
    for child in track:
        if child.tag == "key":
            if child.text == "Name":
                name = next(child.itertext())
            elif child.text == "Artist":
                artist = next(child.itertext())
    if name and artist:
        # Search for track on Spotify
        results = sp.search(q=f"track:{name} artist:{artist}", type='track')
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])
