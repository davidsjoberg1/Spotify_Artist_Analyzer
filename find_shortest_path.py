from handlers.db_handler import *
import sqlite3
from handlers.spotify_api_handler import get_artist_spotify, get_token


def find_shortest_path(a1, a2, search_method, cursor, token):
    """
    Find the shortest path between two artists
    :param artist_1: The name of the first artist
    :param artist_2: The name of the second artist
    :param search_method: The search method to use
    :param cursor: The cursor to the database
    """
    try:
        a1 = get_artist_spotify(token, a1, limit=1)
        a2 = get_artist_spotify(token, a2, limit=1)
        if a1 is None or a2 is None:
            print("Artist not found")
            return
        
        if search_method == "BFS":
            path = bfs(a1[0]["id"], a2[0]["id"], cursor)
        elif search_method == "DFS":
            path = dfs(a1[0]["id"], a2[0]["id"], cursor)
        elif search_method == "Dijkstra":
            path = None
        elif search_method == "A*":
            path = None

        if path is None:
            print("No path found")
        else:
            print("Path found:")
            for artist_id in path:
                print(get_artist(artist_id, cursor)[1])
    except Exception as e:
        print("Error: ", e)
        return
    except KeyboardInterrupt as e:
        print("Error: ", e)
        return


if __name__ == "__main__":
    token = get_token()
    artist_1 = "ADAAM"#input("Enter name of first artist: ")
    artist_2 = "C3 Too Loose"#input("Enter name of second artist: ")

    search_methods = ["BFS", "DFS", "Dijkstra", "A*"]
    print("Search methods:")
    for i in range(len(search_methods)):
        print(f"{i}. {search_methods[i]}")
    search_method = 1#input("Enter index of method: ")

    conn = sqlite3.connect('data/artists.db')
    cursor = conn.cursor()

    find_shortest_path(artist_1, artist_2, search_methods[int(search_method)], cursor, token)

    conn.close()