import igraph as ig
import matplotlib.pyplot as plt
from handlers.db_handler import *
import sqlite3
import json
import matplotlib.pyplot as plt
import time


def calculate_time():
    """
    Create a graph of all artists and their relationships
    :param cursor: The cursor to the database
    """
    
    data = get_json('data/1000_random_artists_python.json')
    tot_python_time = 0
    for i in range(len(data)):
        tot_python_time += data[i]["time"]
        if data[i]["path_lengths"] == 0:
            break
    avg_python_time = round(tot_python_time / ((i+1)*60), 1)

    data = get_json('data/1000_random_artists_cpp.json')
    tot_cpp_time = 0
    for j in range(i+1):
        tot_cpp_time += data[j]["time"]
    avg_cpp_time = round(tot_cpp_time / ((j+1)*60), 1)

    print(f"Avg python time: {avg_python_time} minutes")
    print(f"Avg cpp time: {avg_cpp_time} minutes")


def create_graph(language="python"):

    json_data = get_json(f'data/1000_random_artists_{language}.json')

    # Set the figure to fullscreen
    mng = plt.get_current_fig_manager()
    try:
        mng.full_screen_toggle()  # Works on most backends
    except AttributeError:
        mng.window.state('zoomed') 
    


    x_data = []
    y_data = []

    totals = {}
    averages = {}


    for i in range(len(json_data)):
        if json_data[i]["path_lengths"] == 0:
            break
        if language == "cpp":
            hehe = sorted(json_data[i]["path_lengths"], key=lambda x: x[0])
            for pair in hehe:
                x_data.append(pair[0])
                y_data.append(pair[1])

                totals[pair[0]] = totals.get(pair[0], 0) + pair[1]
                averages[pair[0]] = totals[pair[0]] / (i+1)

        else:
            for key, value in json_data[i]["path_lengths"].items():
                x_data.append(key)
                y_data.append(value)

                totals[key] = totals.get(key, 0) + value
                averages[key] = totals[key] / (i+1)

        plt.clf()

        plt.plot(x_data, y_data, label=f'Data', linewidth=0.2)  # Use marker='o' to show points
        plt.plot(list(averages.keys()), list(averages.values()), label=f'Average', linewidth=5)
        # Add titles and labels
        plt.title(f'Basic Line Graph. Iteration: {i+1}')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')

        # Show the graph
        plt.pause(0.000001)
        #break

   

    
    # Add titles and labels
    plt.title('Artist Path Lengths')
    plt.xlabel('Path length')
    plt.ylabel('Number of artists')

    for key, value in averages.items():
        print(f"Path length: {key}, Average: {round(value, 0)}")

    # Show the graph
    plt.show()
    tot = 0

  

def get_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data
    
def main():
    #calculate_time()
    create_graph("cpp")



