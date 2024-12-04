import igraph as ig
import matplotlib.pyplot as plt
from handlers.db_handler import *
import sqlite3
import time

def main():
    conn = sqlite3.connect("../artists.db")
    cursor = conn.cursor()
    start_time = time.time()
    artist_ids = get_all_artist_ids(cursor)
    counter = 0
    for artist_id in artist_ids:
        incoming = get_num_of_incoming_relationships(artist_id[0], cursor)
        counter += 1
        
        print("Counter: ", counter, " Time: ", time.time() - start_time, " Incoming: ", incoming)
        
    print("Counter: ", counter)
    print("Time: ", time.time() - start_time)

   
    conn.close()
 
