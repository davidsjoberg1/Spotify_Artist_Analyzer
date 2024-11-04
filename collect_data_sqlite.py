from datetime import datetime
import time
from handlers.spotify_api_handler import get_token, get_artist_spotify, get_related_artists_spotify
import sqlite3
from handlers.db_handler import *
from handlers.json_handler import write_json

DB_PATH = '../../../../media/davidsjoberg/RB_DB/spotify_data/artists.db'
#DB_PATH = 'data/artists.db'
NO_APPS = 3


def find_all_artists():
    """
    Searches through all related artists of the artists in the search file, 
    and continues to search until all artists have been evaluated
    """

    thousand_time = datetime.now().timestamp()
    start_time = datetime.now().timestamp()
    counter_time = datetime.now().timestamp()
    token_counter = 2
    token = get_token(token_counter)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        while True:

            num_all_searched = len(get_all_searched(1, cursor))
            current_artist = get_first_not_searched_artist(cursor)
           

            if current_artist is None:
                print("All artists searched")
                print("Total number of artists found: ", get_table_length("all_artists", cursor))
                print("Total number of genres found: ", get_table_length("genre_relationships", cursor))
                print("Total number of artist relationships found: ", get_table_length("artist_relationships", cursor))
                conn.close()
                return True

            
            if datetime.now().timestamp() - start_time >= 3000:
                start_time = datetime.now().timestamp()
                token = get_token()

            if num_all_searched % 1000 == 0:
                write_json(num_all_searched, str(round((datetime.now().timestamp() - thousand_time)/60, 2)) + " minutes", "data/time.json")
                thousand_time = datetime.now().timestamp()

            if num_all_searched % 100 == 0:
                conn.close()
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                token = get_token(token_counter)
                token_counter += 1
                if token_counter > NO_APPS:
                    token_counter = 1
                print("Current artist: ", current_artist, " All searched: ", num_all_searched)

            # 9600 requests per day 
            time_diff = datetime.now().timestamp() - counter_time
            if time_diff < 9:
                print("Sleeping for: ", 9 - time_diff, " seconds")
                time.sleep(9 - time_diff)
            counter_time = datetime.now().timestamp()
                
                
        

            related_artists = get_related_artists_spotify(token, current_artist[0])
            new_artists = []
            # TODO: maybe not efficient with that many get_artist calls
            # might be more effiecient to just create data for all with a list maker
            # and then insert all at once ??
            for related_artist in related_artists:
                if not get_artist(related_artist["id"], cursor) :
                    new_artists.append(create_artist_data(related_artist))
            
            insert_artist_data(new_artists, "all_artists", conn, cursor)
            insert_related_artists(current_artist[0], related_artists, conn, cursor)
            
            set_is_searched(current_artist[0], True, conn, cursor)

    except KeyboardInterrupt:
        conn.close()
        print("Exiting...")
        exit(0)

def add_new_artist(token):
    artist_name = input("Enter artist name: ")
    artist = get_artist_spotify(token, artist_name)
    artists = []
    for a in artist:
        artists.append(create_artist_data(a))
    conn = sqlite3.connect(DB_PATH)
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if input("Delete tables? y/n") == "y":
        delete_table("genre_relationships", conn, cursor)
        delete_table("artist_relationships", conn, cursor)
        delete_table("all_artists", conn, cursor)
    create_tables(conn, cursor)

    token = get_token()
    input_new = input("New artist?? y/n")
    if input_new == "y":
        
        add_new_artist(token)
    conn.close()
    while True:
        stop = find_all_artists()
        if stop:
            break



    


    
    


   


    

