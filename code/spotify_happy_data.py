import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd


# birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'

# Authenticating client user id and secret key.
client_id = "71907f2aa045448d8b803606a292c16f"
client_secret = "d7628c0393a945429fd5ec709526fc10"

happy_song = "1EN91xJtYSDCJtjn9t0iww"

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id, client_secret= client_secret))


# playlist = spotify.user_playlist_tracks("Best Playlists Ever", happy_song)

# for part in playlist["items"]:
# 	print(part)


# Taken from a Medium article https://towardsdatascience.com/how-to-create-large-music-datasets-using-spotipy-40e7242cc6a6
def create_playlist_df(creator, playlist_id):

	playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness",
	"mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]

	playlist_df = pd.DataFrame(columns=playlist_features_list)

	playlist = spotify.user_playlist_tracks(creator, playlist_id)["items"]

	for track in playlist:

	    playlist_features = {}
	    # Get metadata
	    playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
	    playlist_features["album"] = track["track"]["album"]["name"]
	    playlist_features["track_name"] = track["track"]["name"]
	    playlist_features["track_id"] = track["track"]["id"]
	    
	    # Get audio features
	    audio_features = spotify.audio_features(playlist_features["track_id"])[0]
	    
	    for feature in playlist_features_list[4:]:
	        playlist_features[feature] = audio_features[feature]
	    
	    # Concat the dfs
	    track_df = pd.DataFrame(playlist_features, index = [0])
	    playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
    
	return playlist_df



# happy_playlist_df = create_playlist_df("Best Playlists Ever", happy_song)

# happy_playlist_df.to_csv("Happy_song_playlist.csv")

sad_song_id = "7LxpjJGV6XQ3b5jkPpzLk5"

sad_playlist_df = create_playlist_df("Theawesomevocals", sad_song_id)
sad_playlist_df.to_csv("Sad_song_playlist.csv")
