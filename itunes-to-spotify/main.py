import os
import logging
from typing import Tuple, List, Dict
from fuzzywuzzy import fuzz
import xml.etree.ElementTree as et
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
from utils import clean_artist, clean_track

load_dotenv()

logging.basicConfig(level=logging.INFO)

def find_best_track_match(tracks: List[Dict], query: str) -> Dict:
    # Finds the best track match from a list of track dictionaries based on a query string.
    # Takes a tracks, a list of dictionaries that each containing track information,
    # and the search query, a string used for matching.

    # Initialize variables for the best match and its score
    best_match, best_score = None, 0

    # Loop through each track in the provided list
    for track in tracks:
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        popularity = track['popularity']

        # Use fuzzy string matching to compare the query with each track's artist and name
        match_score = fuzz.partial_ratio(query.lower(), f"{artist_name} {track_name}".lower())

        # Update best match if this track has a higher score or the same score but higher popularity
        if match_score > best_score or (match_score == best_score and popularity > best_match['popularity']):
            best_match = track
            best_score = match_score

    # Returns a dictionary containing the best matching track.
    return best_match

def process_track(track: et.Element) -> Tuple[int, str, str, str, int]:
    # Initializes variables to hold the track's ID, name, artist, album, and track number.
    # Sets them to None initially.
    track_id, name, artist, album, track_number = None, None, None, None, None

    # Converts the XML track element's children to a list for easy traversal.
    children = list(track)

    # Iterates through the list of children, checking each 'key' element for specific data.
    for i in range(len(children) - 1):
        child = children[i]
        next_child = children[i + 1]

        # Checks if the current element is a 'key' element.
        if child.tag == "key":
            # Extracts the 'Track ID' if the following element is an integer.
            if child.text == "Track ID" and next_child.tag == "integer":
                track_id = int(next_child.text)
            # Extracts the 'Name' if the following element is a string.
            elif child.text == "Name" and next_child.tag == "string":
                name = next_child.text
            # Extracts the 'Artist' if the following element is a string.
            elif child.text == "Artist" and next_child.tag == "string":
                artist = next_child.text
            # Extracts the 'Album' if the following element is a string.
            elif child.text == "Album" and next_child.tag == "string":
                album = next_child.text
            # Extracts the 'Track Number' if the following element is an integer.
            elif child.text == "Track Number" and next_child.tag == "integer":
                track_number = int(next_child.text)

    # Returns a tuple containing the extracted track information.
    return track_id, name, artist, album, track_number

def track_getter(sp, user_id: str, playlist_id: str, playlist_order: List[int], tracks_info: Dict[int, Tuple[str, str, str, int]]):
    # Initialize a set to keep track of the URIs that have been added to the playlist.
    added_uris = set()

    # Iterate through each track_id in the playlist order.
    for track_id in playlist_order:
        # Retrieve track information using track_id.
        name, artist, album, track_number = tracks_info[track_id]

        # Proceed as long as name and artist fields are not None.
        if name and artist:
            # Clean the name and album fields.
            cleaned_name = clean_track(name)
            cleaned_album = clean_track(album)
     
            # Perform initial Spotify search using cleaned track name, artist, and album.
            results = sp.search(q=f"track:{cleaned_name} artist:{artist} album:{cleaned_album}", type='track')
            tracks = results['tracks']['items']

            # If no matches found, clean artist name and perform the search again.
            if not tracks:
                cleaned_artist = clean_artist(artist)
                results = sp.search(q=f"track:{cleaned_name} artist:{cleaned_artist}", type='track')
                tracks = results['tracks']['items']

            # If still no matches found, search using artist and album name, and find the track based on track number.
            # This can be helpful when the song title is in another language and isn't translated on Spotify.
            if not tracks:
                album_results = sp.search(q=f"artist:{artist} album:{cleaned_album}", type='album')
                albums = album_results['albums']['items']
                if albums:
                    album_id = albums[0]['id']
                    track_results = sp.album_tracks(album_id)
                    if track_number <= len(track_results['items']):
                        track_uri = track_results['items'][track_number - 1]['uri']
                        if track_uri not in added_uris:
                            sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])
                            added_uris.add(track_uri)
                            print(f"Added {artist} - {name} to playlist, but it may have a different name.")
                            continue

            # Find the best matching track from the search results.
            best_track = find_best_track_match(tracks, f"{artist} {cleaned_name}")

            # Add the track to the playlist if it's not a duplicate.
            if best_track:
                track_uri = best_track['uri']
                if track_uri not in added_uris:
                    sp.user_playlist_add_tracks(user_id, playlist_id, [track_uri])
                    added_uris.add(track_uri)
                    print(f"Added {artist} - {name} to playlist.")
                else:
                    print(f"Skipped duplicate track: {artist} - {name}")
            # If no track could be found, print a warning message.
            else:
                print(f"*** {artist} - {name} could not be found. ***")

def process_playlist(playlist: et.Element) -> List[int]:
    # Initialize an empty list to hold track IDs.
    track_ids = []

    # Convert the XML playlist element's children to a list for easy traversal.
    children = list(playlist)

    # Loop through the children of the playlist element.
    for i, child in enumerate(children):

        # Look for the 'key' element with the text "Playlist Items".
        if child.tag == "key" and child.text == "Playlist Items":

            # Make sure the next element exists and is an 'array' element.
            if i + 1 < len(children) and children[i + 1].tag == "array":

                # Get the array element that contains the playlist items.
                array = children[i + 1]

                # Loop through all the 'dict' elements in the array.
                for item in array.findall("./dict"):

                    # Initialize a variable to hold the track ID.
                    track_id = None

                    # Loop through the keys within each 'dict' element.
                    for j, key in enumerate(item):

                        # Look for the 'key' element with the text "Track ID".
                        if key.tag == "key" and key.text == "Track ID":

                            # Make sure the next element exists and is an 'integer' element.
                            if j + 1 < len(item) and item[j + 1].tag == "integer":

                                # Get the track ID from the next element.
                                track_id = int(item[j + 1].text)

                    # If a track ID was found, append it to the list.
                    if track_id is not None:
                        track_ids.append(track_id)

    # Return the list of track IDs.
    return track_ids

def authenticate_spotify() -> spotipy.Spotify:
    # Retrieve Spotify API credentials from .env.
    scope = os.getenv("SPOTIPY_SCOPE")
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

    if not all([scope, client_id, client_secret, redirect_uri]):
        raise ValueError("Spotify API credentials are missing in .env file.")

    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope))

def create_spotify_playlist(sp: spotipy.Spotify, user_id: str, playlist_name: str) -> str:
    """ Creates a Spotify playlist and returns its ID. """
    return sp.user_playlist_create(user_id, playlist_name)['id']

def main():
    # Prompt the user for an iTunes XML playlist file name and attempt to parse it.
    xml_file = input("Name of the iTunes playlist XML file: ")
    try:
        tree = et.parse(xml_file)
        root = tree.getroot()
    except et.ParseError:
        print("Error parsing the XML file. Please ensure the file is a valid XML.")
        return
    except FileNotFoundError:
        print("The specified XML file was not found.")
        return

    # Attempt to authenticate with Spotify API using provided credentials.
    try:
        sp = authenticate_spotify()
    except Exception as e:
        logging.error(f"Failed to authenticate with Spotify: {e}")
        return

    # Create a Spotify playlist using the name of the iTunes playlist.
    user_id = sp.current_user()['id']
    playlist_name = os.path.splitext(xml_file)[0]
    playlist_id = create_spotify_playlist(sp, user_id, playlist_name)

    # Process the iTunes playlist to obtain the track IDs.
    playlist_order = []
    for playlist in root.findall("./dict/array/dict"):
        playlist_order = process_playlist(playlist)

    # Process each track in the iTunes XML to collect its info.
    tracks_info = {}
    for track in root.findall("./dict/dict/dict"):
        track_id, name, artist, album, track_number = process_track(track)
        if track_id is not None:
            tracks_info[track_id] = (name, artist, album, track_number)

    # Populate the Spotify playlist with the tracks found in the iTunes playlist.
    track_getter(sp, user_id, playlist_id, playlist_order, tracks_info)

if __name__ == "__main__":
    main()

# TODO: Error log that tracks duplicates and songs that can't be found
