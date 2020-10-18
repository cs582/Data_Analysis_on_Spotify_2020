import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'

# Authenticating client user id and secret key.
client_id = "71907f2aa045448d8b803606a292c16f"
client_secret = "d7628c0393a945429fd5ec709526fc10"

happy_song = "1EN91xJtYSDCJtjn9t0iww"

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id, client_secret= client_secret))

results = spotify.artist_albums(birdy_uri, album_type="album")
albums = results['items']

while results['next']:
	results = spotify.next(results)
	albums.extend(results['items'])


for album in albums:
	print(album['name'])

