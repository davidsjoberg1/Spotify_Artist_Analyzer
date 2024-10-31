from datetime import datetime
import time
from spotify_api_handler import get_token, get_artist_spotify, get_related_artists_spotify
import requests
import sqlite3
from db_handler import *
from json_handler import write_json



def find_all_artists(token, start_time):
    """
    Searches through all related artists of the artists in the search file, 
    and continues to search until all artists have been evaluated
    """
    counter = 0
    counter_time = datetime.now().timestamp()
    thousand_time = datetime.now().timestamp()

    try:
        while True:
            conn = sqlite3.connect('artists.db')
            cursor = conn.cursor()

            all_searched = len(get_all_searched(1, cursor))
            if all_searched % 1000 == 0:
                write_json(all_searched, str(round((datetime.now().timestamp() - thousand_time)/60, 2)) + " minutes", "time.json")
                thousand_time = datetime.now().timestamp()
            

            # Token will be expired after 3600 seconds
            if datetime.now().timestamp() - start_time > 3000:
                break
             # maximum 180 requests per minute
            if counter == 45:
                time_diff = datetime.now().timestamp() - counter_time
                if time_diff < 15:
                    print("Sleeping for: ", 15 - time_diff, " seconds")
                    time.sleep(15 - time_diff)
                counter_time = datetime.now().timestamp()
                counter = 0
        

            if len(get_all_searched(0, cursor)) == 0:
                break

            current_artist = get_first_not_searched_artist(cursor)
            if all_searched % 10 == 0:
                print("Current artist: ", current_artist, " All searched: ", all_searched)
            related_artists = get_related_artists_spotify(token, current_artist[0])
            trimmed_related_artists = []
            for related_artist in related_artists:
                if not get_artist(related_artist["id"], cursor):
                    trimmed_related_artists.append(create_artist_data(related_artist))
            
            insert_artist_data(trimmed_related_artists, "all_artists", conn, cursor)
            insert_related_artists(current_artist[0], trimmed_related_artists, conn, cursor)
            
            set_is_searched(current_artist[0], True, conn, cursor)
            counter += 1
            conn.close()



    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)



def add_new_artist(token):
    artist_name = input("Enter artist name: ")
    artist = get_artist_spotify(token, artist_name)
    artists = []
    for a in artist:
        artists.append(create_artist_data(a))
    conn = sqlite3.connect('artists.db')
    cursor = conn.cursor()
    insert_artist_data(artists, "all_artists", conn, cursor)
    conn.close()
    



def create_artist_data(artist):
    artist_data = {
        "id": artist["id"],
        "name": artist["name"],
        "genres": artist["genres"],
        "popularity": artist["popularity"],
        "followers": artist["followers"]["total"], 
        "related_artists": [],
        "is_searched": False
        }
    
    return artist_data


    




if __name__ == '__main__':
    token = get_token()
    


    if input("Delete tables? y/n") == "y":
        delete_table("genre_relationships")
        delete_table("artist_relationships")
        delete_table("all_artists")
 

    create_tables()
 
    

    
    

    input_new = input("New artist?? y/n")
    if input_new == "y":
        add_new_artist(token)
    
    
    while True:
        token = get_token()
        start_time = datetime.now().timestamp()
        find_all_artists(token, start_time)



    


    
    


   


    

