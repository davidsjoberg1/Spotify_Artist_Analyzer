from datetime import datetime
import time
from spotify_api_handler import get_token, get_artist, get_related_artists
import requests
import sqlite3
from db_handler import *



def find_all_artists(token, start_time):
    """
    Searches through all related artists of the artists in the search file, 
    and continues to search until all artists have been evaluated
    """
    counter = 0
    counter_time = datetime.now().timestamp()
    try:
        while True:
            # Token will be expired after 3600 seconds
            if datetime.now().timestamp() - start_time > 3000:
                break
            
            # Accessing all_artists.json and search_artists
            #all_artists = get_json("all_artists.json")
            #search_artists = get_json("search_artists.json")
            #print("All artists: ", len(all_artists))
            #print("Search artists: ", len(search_artists))
        

            if get_table_length("search_artists") == 0:
                break

            current_artist = get_first_artist("search_artists")
            print(current_artist[0])
            exit(0)


            # Get the artist to search for and remove it from the search file
            #current_artist_id, current_artist_data = next(iter(search_artists.keys())), next(iter(search_artists.values()))
            delete_json(current_artist_id, "search_artists.json")

            # maximum 180 requests per minute
            if counter == 90:
                time_diff = datetime.now().timestamp() - counter_time
                if time_diff < 30:
                    time.sleep(30 - time_diff)
                counter_time = datetime.now().timestamp()
                counter = 0

            # Get related artists, add them to the current artist and write to all_artists file
            related_artists = get_related_artists(token, current_artist_id)
            trimmed_related_artists = []
            for artist in related_artists:
                artist_id, artist_data = create_artist_data(artist)
                trimmed_related_artists.append({artist_id: artist_data})
            current_artist_data["related_artists"] = trimmed_related_artists
            write_json(current_artist_id, current_artist_data, "all_artists.json")
            counter += 1

            # Every artist that has not been evaluated will be added to the search file
            for artist in related_artists:
                if artist["id"] not in all_artists:
                    artist_id, artist_data = create_artist_data(artist)
                    write_json(artist_id, artist_data, "search_artists.json")
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)



def add_new_artist(token):
    artist_name = input("Enter artist name: ")
    artist= get_artist(token, artist_name)
    artists = []
    for a in artist:
        artists.append(create_artist_data(a))
        insert_artist_data(artists, "search_artists")
        #write_json(artist_id, artist_data, "search_artists.json")


def create_artist_data(artist):
    artist_data = {
        "id": artist["id"],
        "name": artist["name"],
        "genres": artist["genres"],
        "popularity": artist["popularity"],
        "followers": artist["followers"]["total"], 
        "related_artists": []
        }
    
    return artist_data


    




if __name__ == '__main__':
    token = get_token()

    if input("Delete tables? y/n") == "y":
        delete_table("search_artists")
        delete_table("all_artists")
        delete_table("artist_relationships")
        delete_table("genre_relationships")
    create_tables()
 
    

    
    

    input_new = input("New artist?? y/n")
    if input_new == "y":
        add_new_artist(token)
    
    while True:
        token = get_token()
        start_time = datetime.now().timestamp()
        find_all_artists(token, start_time)



    


    
    


   


    

