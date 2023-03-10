
from datetime import datetime, timedelta

import requests
import pandas as pd 

USER_ID="e700bcb7d1b74358b4cb2d3deebd25db"
TOKEN="BQDCNqHGllRv_scIcM4k1vqSNQzKMQDVaKDYq93v9cCV3idEvTbC6T3AeMwNvoBS8w_ttvor-X9S6yovqcW9B8RZiVjvIk3Kb-FfSYPzOMRnMycXzBU11pfx72jhyJsQKnnTQjUauo14dH6h2Y1j96m4h3SKGxOFkrEH8o5ugQnQsoLPpuT_ND3hgoteMVxrhatsDw"

def return_dataframe():
    input_variables = {
        "Accept" : "application/json",  
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
     
    today = datetime.now()
    yesterday = today - timedelta(days=10) #no of Days u want the data for)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix_timestamp), headers = input_variables)
    data = r.json()
    if not r.ok:
        raise Exception(r.status_code, data)
    # Extracting only the relevant bits of data from the json object
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])
        
    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }
    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    print(song_df)
    return song_df
