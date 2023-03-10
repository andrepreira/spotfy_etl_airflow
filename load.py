# from flask import session
import extract as Extract
import transform as Transform
import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
# import requests
# import json
# from datetime import datetime
# import datetime
# import sqlite3

DATABASE_URL = "postgresql://postgres:password@db:5432/my_played_tracks"

if __name__ == "__main__":

#Importing the songs_df from the Extract.py
    load_df=Extract.return_dataframe()
    if(Transform.Data_Quality(load_df) == False):
        raise Exception("Failed at Data Validation")
    Transformed_df=Transform.Transform_df(load_df)
    #The Two Data Frame that need to be Loaded in to the DataBase

#Loading into Database
    engine = sqlalchemy.create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    # conn = sqlite3.connect('my_played_tracks.sqlite')
    # cursor = conn.cursor()
    conn = engine.connect()
    # SQL Query to Create Played Songs
    sql_query_1 = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
    song_name VARCHAR(200),
    artist_name VARCHAR(200),
    played_at TIMESTAMP,
    CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    # SQL Query to Create Most Listened Artist
    sql_query_2 = """
    CREATE TABLE IF NOT EXISTS fav_artist(
    ID SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    artist_name VARCHAR(200),
    count INTEGER
    )
    """

    conn.execute(sql_query_1)
    conn.execute(sql_query_2)

    print("Opened database successfully")

    #We need to only Append New Data to avoid duplicates
    try:
        load_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")
    try:
        Transformed_df.to_sql("fav_artist", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database2")

    #cursor.execute('DROP TABLE my_played_tracks')
    #cursor.execute('DROP TABLE fav_artist')

    conn.close()
    print("Close database successfully")