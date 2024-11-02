from handlers.db_handler import *


def bfs(a1, a2, cursor):
    """
    Find the shortest path between two artists using breadth-first search
    :param a1: The id of the first artist
    :param a2: The id of the second artist
    :param cursor: The cursor to the database
    :return: The path between the two artists
    """
    explored = [a1]
    queue = [[a1]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == a2:
            return path
        for related_artist in get_related_artists(node, cursor):
            if related_artist[0] not in explored:
                explored.append(related_artist[0])
                new_path = list(path)
                new_path.append(related_artist[0])
                queue.append(new_path)
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
    explored = [a1]
    stack = [[a1]]
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == a2:
            print("Explored: ", len(explored))
            return path
        for related_artist in get_related_artists(node, cursor):
            if related_artist[0] not in explored:
                explored.append(related_artist[0])
                new_path = list(path)
                new_path.append(related_artist[0])
                stack.append(new_path)
    return None