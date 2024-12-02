from handlers.db_handler import *
import sqlite3
from handlers.spotify_api_handler import get_artist_spotify, get_token
from data_analysis.search_methods import bfs, dfs, get_all_lengths
from datetime import datetime
import json



def get_all_lengths(a1, cursor):
    """
    Find the path length from one artist to all others in the database using breadth-first search
    ##Write to a json file
    :param a1: The id of the artist
    :param cursor: The cursor to the database
    :return: Dict of paths lengths
    """
    start_time = datetime.now().timestamp()
    
    explored = {}
    found = {a1: None}
    # Key = path length, Value = number of artists with that path length
    path_lengths = {}
    queue = [[a1]]
    while queue:
        path = queue.pop(0)
        node = path[-1]

        for related_artist in get_related_artists(node, cursor):
            if related_artist[0] not in found:
                found[related_artist[0]] = None
                new_path = list(path)
                new_path.append(related_artist[0])
                queue.append(new_path)

        explored[node] = None
        path_lengths[len(path)-1] = path_lengths.get(len(path) -1, 0) + 1
        #print("Path lengths: ", path_lengths, " Queue length: ", len(queue), end="\r")
    artists_found = 0
    for i in range(len(path_lengths)):
        artists_found += path_lengths[i]
    if artists_found == len(get_all("all_artists", cursor)):
        print("\nAll artists found")
    else:
        print("\nFound: ", artists_found, " artists of ", len(get_all("all_artists", cursor)))
    exec_time = datetime.now().timestamp() - start_time
    print("Time: ", exec_time)
    return path_lengths, round(exec_time, 2)


def create_1000_random_artists_file(cursor):
    """
    ONLY RUN ONCE
    """
    json_list = []
    artists_list = get_1000_random_artists(cursor)
    for artist in artists_list:
        json_list.append({"artist_id": artist[0], "path_lengths": 0, "time": 0})
    with open('data/1000_random_artists_python.json', 'w') as f:
        json.dump(json_list, f, indent=4)
    with open('data/1000_random_artists_cpp.json', 'w') as f:
        json.dump(json_list, f, indent=4)


def write_to_json_file(artist_id, path_lengths, exec_time):
    with open("data/1000_random_artists_python.json", 'r') as f:
        data = json.load(f)
    for artist in data:
        if artist["artist_id"] == artist_id:
            artist["path_lengths"] = path_lengths
            artist["time"] = exec_time
            break
    with open("data/1000_random_artists_python.json", 'w') as f:
        json.dump(data, f, indent=4)


def get_unsearched_artist():
    with open("data/1000_random_artists_python.json", 'r') as f:
        data = json.load(f)
    for artist in data:
        if artist["path_lengths"] == 0:
            return artist["artist_id"]
    return None

        





        

def main():
    conn = sqlite3.connect('../artists.db')
    cursor = conn.cursor()
    start_time = datetime.now().timestamp()

    while True:
        artist_id = get_unsearched_artist()
        if artist_id is None:
            break
        path_lengths, exec_time = get_all_lengths(artist_id, cursor)
        write_to_json_file(artist_id, path_lengths, exec_time)
        print("Time: ", datetime.now().timestamp() - start_time)

    

    conn.close()