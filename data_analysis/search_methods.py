from line_profiler import profile
from handlers.db_handler import *
from datetime import datetime
from handlers.json_handler import write_json



def bfs(a1, a2, cursor):
    """
    Find the shortest path between two artists using breadth-first search
    :param a1: The id of the first artist
    :param a2: The id of the second artist
    :param cursor: The cursor to the database
    :return: The path between the two artists
    """
    explored = {a1: None}
    queue = [[a1]]
    while queue:        
        path = queue.pop(0)
        node = path[-1]
        if node == a2:
            print("\n")
            return path
        for related_artist in get_related_artists(node, cursor):
            if related_artist[0] not in explored:
                explored[related_artist[0]] = None
                new_path = list(path)
                new_path.append(related_artist[0])
                queue.append(new_path)
        print("len path: ", len(path), " len queue: ", len(queue), "len explored: ", len(explored), end="\r")
    return None


def dfs(a1, a2, cursor):
    """
    Find a path between two artists using depth-first search
    This method is not guaranteed to find the shortest path
    :param a1: The id of the first artist
    :param a2: The id of the second artist
    :param cursor: The cursor to the database
    :return: The path between the two artists
    """
    explored = {a1: None}
    stack = [[a1]]
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == a2:
            print("Explored: ", len(explored))
            return path
        for related_artist in get_related_artists(node, cursor):
            if related_artist[0] not in explored:
                explored[related_artist[0]] = None
                new_path = list(path)
                new_path.append(related_artist[0])
                stack.append(new_path)
    return None


def get_all_lengths(a1, cursor):
    """
    Find the path length from one artist to all others in the database using breadth-first search
    Write to a json file
    :param a1: The id of the artist
    :param cursor: The cursor to the database
    :return: Dict of paths lengths
    """
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
        print("Path lengths: ", path_lengths, " Queue length: ", len(queue), end="\r")
    artists_found = 0
    for i in range(len(path_lengths)):
        artists_found += path_lengths[i]
    if artists_found == len(get_all("all_artists", cursor)):
        print("\nAll artists found")
    else:
        print("\nFound: ", artists_found, " artists of ", len(get_all("all_artists", cursor)))
    return path_lengths
