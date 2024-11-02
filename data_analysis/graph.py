import igraph as ig
import matplotlib.pyplot as plt
from handlers.db_handler import *
import sqlite3

def create_graph(cursor):
    """
    Create a graph of all artists and their relationships
    :param cursor: The cursor to the database
    """
    g = ig.Graph(directed=True)
    g.add_vertices(get_all("all_artists", cursor))
    
    return g

if __name__ == "__main__":
    conn = sqlite3.connect('data/artists.db')
    cursor = conn.cursor()
