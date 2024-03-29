# iTunes XML to Spotify Playlist

Reads an iTunes playlist in XML format and uses it to create a
Spotify playlist.

## Dependencies

- spotipy
- fuzzywuzzy
- python-dotenv
- python-Levenshtein

## Setup

1. Obtain your `client_id`, `client_secret`, and `redirect_uri`. You can do this by going to https://developer.spotify.com/dashboard and creating an app (this is free).

2. Create an `.env` file in the root of your project directory and add your Spotify credentials like this:

    ```
    SPOTIPY_SCOPE='your_scope_here'
    SPOTIPY_CLIENT_ID='your_client_id_here'
    SPOTIPY_CLIENT_SECRET='your_client_secret_here'
    SPOTIPY_REDIRECT_URI='your_redirect_uri_here'
    ```

## Usage

1. Export your iTunes playlist as an XML file and save it in the root directory.

2. Run main.py and enter the name of your file (ex: Playlist.xml)