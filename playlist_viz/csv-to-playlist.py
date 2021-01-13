import json
import pandas as pd
import requests
from secrets import token, user_id


class CreatePlaylist:

    def __init__(self):
        self.user_id = user_id
        self.token = token
        self.csv = "/Users/isacmlee/Desktop/Projects/csv-to-playlist/recommendations.csv"
        self.tuples = self.get_song_names()

    # Step 1: Get list of tuples containing song and artist names from csv file.
    def get_song_names(self):
        df = pd.read_csv(self.csv)
        df = df.sample(frac=1) # shuffle the dataframe so songs are not ordered based on genre
        tuple_list = list(zip(df.track, df.artist))
        return tuple_list

    # Step 2: Create playlist in Spotify.
    def create_playlist(self):
        request_body = json.dumps({
            "name": "CSV_to_Spotify pt 2",
            "description": "Python script that converts CSV file generated by recommender into a Spotify Playlist.",
            "public": True
        })
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data=request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.token)
            }
        )
        response_json = response.json()

        # playlist id
        return response_json["id"]

    # Step 3: Get each song's Spotify uri
    def get_spotify_uri(self, song, artist):
        query = "https://api.spotify.com/v1/search?query=track%3A{}&type=track&offset=0&limit=1".format(song, artist)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )
        response_json = response.json()
        songs = response_json["tracks"]["items"]

        # URI
        uri = songs[0]["uri"]
        return uri

    # Step 4: Add songs to Spotify Playlist
    def add_to_playlist(self):
        uris = []

        # Loop through tuples and get URIs
        for i, j in self.tuples[:40]:
            uris.append(self.get_spotify_uri(i, j))

        # Create new playlist
        playlist_id = self.create_playlist()

        # Populate playlist
        request_data = json.dumps(uris)
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            query,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.token)
            }
        )

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    cp = CreatePlaylist()
    cp.add_to_playlist()