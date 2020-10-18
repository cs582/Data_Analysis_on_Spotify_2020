import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from tensorflow.keras.models import save_model, load_model
from sklearn.preprocessing import StandardScaler
import numpy as np

client_id = "71907f2aa045448d8b803606a292c16f"
client_secret = "d7628c0393a945429fd5ec709526fc10"


# take song track id from user


spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id, client_secret= client_secret))

# track_list = spotify.tracks(track_id_list)

# print(track)

def create_playlist_df(track_id_list):

	playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness",
	"mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]

	playlist_df = pd.DataFrame(columns=playlist_features_list)

	# playlist = spotify.user_playlist_tracks(creator, playlist_id)["items"]
	track_list = spotify.tracks(track_id_list)

	for track in track_list['tracks']:

	    playlist_features = {}
	    # Get metadata
	    playlist_features["artist"] = track["album"]["artists"][0]["name"]
	    playlist_features["album"] = track["album"]["name"]
	    playlist_features["track_name"] = track["name"]
	    playlist_features["track_id"] = track["id"]
	    
	    # Get audio features
	    # print(track)
	    # print("Hello")
	    audio_features = spotify.audio_features(playlist_features["track_id"])[0]
	    
	    for feature in playlist_features_list[4:]:
	        playlist_features[feature] = audio_features[feature]
	    
	#     # Concat the dfs
	    track_df = pd.DataFrame(playlist_features, index = [0])
	    playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)
    
	return playlist_df



# Sad one
track_id_list = ["4T6p9mFEP9J1HbQWfdIP6F","2obZ7JPb1t7Fr5qFPxt3Tx", "4j42o0WCmTIpymSY0Llerv"]

###### TAKE INPUT FROM USER (something not working here)
# number = int(input("Enter number of tracks you would like to enter: "))
# track_id_list = []
# for i in range(number):
# 	ele = input()
# 	track_id_list.append(ele)


# Happy one
# track_id_list = ["05wIrZSwuaVWhcv5FfqeH0","1Je1IMUlBXcx1Fz0WE7oPT","3cfOd4CMv2snFaKAnMdnvK"]


track_df = create_playlist_df(track_id_list)


# convert track_df into test_data for the model abd some cleaning, pre-processing
print(track_df)
test_data = track_df.drop(["artist", "album", "track_name","track_id","duration_ms", "speechiness", "key"], axis=1)
sc = StandardScaler()
test_data = sc.fit_transform(test_data)



# load model
filepath = './saved_model'
model = load_model(filepath, compile=True)

prediction = model.predict(test_data)

# prediction = (prediction>0.5)

# print(prediction)

# count = 0
# total = len(prediction)
# for value in prediction:
# 	if value:
# 		count += 1

# mood_index = count/total

mood_index = np.mean(prediction)

print(mood_index)

if mood_index >= 0.6:
	print("Your partner/friend is in a Happy Mood")

elif mood_index <= 0.4:
	print("Cheer up your partner/friend, they are in a melancholy mood")

else:
	print("Relax! They are just enjoying music.")

print("Bye")
