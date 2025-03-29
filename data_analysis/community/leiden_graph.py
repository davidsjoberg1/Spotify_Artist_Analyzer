import igraph as ig
import leidenalg as la
import sqlite3
import handlers.db_handler as db_handler
from datetime import datetime
import time

# Create a graph with 3 nodes and 2 edges
#g = ig.Graph(edges=[(0, 1), (1, 2), (2,0)], directed=True)

# Set labels
#g.vs["label"] = ["Alice", "Bob", "Charlie"]

# Visualize
#ig.plot(g, target="leiden_graph.png", bbox=(0, 0, 300, 300))

DB_PATH = '../artists.db'

def test_artist():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("before db get")
    time =datetime.now().timestamp()
    artists = db_handler.get_first_100_artist_relationships(cursor)
    print("after db get, time: ", datetime.now().timestamp() - time)
    conn.close()
    print(artists[0])

    g = ig.Graph(edges=create_edges(artists), directed=False)

    deg = g.degree()

    node_sizes = [(50/max(deg))*d for d in deg]  # scaling factor + offset

    # Run the partition
    partition = la.find_partition(
        graph=g,
        partition_type=la.ModularityVertexPartition
    )

    print(f"Number of communities found: {len(partition)}")

    # --- Generate distinct colors for each community ---
    num_communities = len(set(partition.membership))
    # Create a coloring palette with the same number of colors as communities
    palette = ig.drawing.colors.ClusterColoringPalette(num_communities)

    # Assign a color to each vertex based on community membership
    vertex_colors = [palette[m] for m in partition.membership]

    # --- Plot with igraph ---
    # Use the Fruchterman-Reingold layout
    layout = g.layout_fruchterman_reingold(
        niter=1000,
    )  
    ig.plot(
        g,
        layout=layout,
        vertex_color=vertex_colors,
        vertex_size=node_sizes,
        bbox=(400, 400),
        margin=20,
        target="leiden_graph.png",
        edge_width=0.5,
    )

def create_edges(artists):
    artist_dict = {}
    i = 0
    edges = []
    for relationship in artists:
        for artist in relationship:
            if artist not in artist_dict:
                artist_dict[artist] = i
                i += 1
        edges.append((artist_dict[relationship[0]], artist_dict[relationship[1]]))
    return edges
    




    



def main():
    test_artist()
