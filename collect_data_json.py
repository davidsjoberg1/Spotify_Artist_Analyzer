from datetime import datetime
import time
from handlers.json_handler import get_json, write_json, delete_json
from handlers.spotify_api_handler import get_token, get_artist_spotify, get_related_artists_spotify
import requests

all_artists_json = "data/all_artists.json"
search_artists_json = "data/search_artists.json"
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
            all_artists = get_json(all_artists_json)
            search_artists = get_json(search_artists_json)
            print("All artists: ", len(all_artists))
            print("Search artists: ", len(search_artists))
        

            if len(search_artists) == 0:
                break

            # Get the artist to search for and remove it from the search file
            current_artist_id, current_artist_data = next(iter(search_artists.keys())), next(iter(search_artists.values()))
            delete_json(current_artist_id, search_artists_json)

            # maximum 180 requests per minute
            if counter == 90:
                time_diff = datetime.now().timestamp() - counter_time
                if time_diff < 30:
                    time.sleep(30 - time_diff)
                counter_time = datetime.now().timestamp()
                counter = 0

            # Get related artists, add them to the current artist and write to all_artists file
            related_artists = get_related_artists_spotify(token, current_artist_id)
            trimmed_related_artists = []
            for artist in related_artists:
                artist_id, artist_data = create_artist_data(artist)
                trimmed_related_artists.append({artist_id: artist_data})
            current_artist_data["related_artists"] = trimmed_related_artists
            write_json(current_artist_id, current_artist_data, all_artists_json)
            counter += 1

            # Every artist that has not been evaluated will be added to the search file
            for artist in related_artists:
                if artist["id"] not in all_artists:
                    artist_id, artist_data = create_artist_data(artist)
                    write_json(artist_id, artist_data, search_artists_json)
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)



def add_new_artist(token):
    artist_name = input("Enter artist name: ")
    artist= get_artist_spotify(token, artist_name)
    for a in artist:
        artist_id, artist_data = create_artist_data(a)
        write_json(artist_id, artist_data, search_artists_json)

def create_artist_data(artist):
    artist_id = artist["id"]
    artist_data = {
        "name": artist["name"],
        "genres": artist["genres"],
        "popularity": artist["popularity"],
        "followers": artist["followers"]["total"], 
        "related_artists": []
        }
    
    return artist_id, artist_data


    



if __name__ == '__main__':
    token = get_token()
    input_new = input("New artist?? y/n")
    if input_new == "y":
        add_new_artist(token)
    
    while True:
        token = get_token()
        start_time = datetime.now().timestamp()
        find_all_artists(token, start_time)



    


    
    


   


    
