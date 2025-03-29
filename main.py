import collect_data_sqlite
import data_analysis.find_shortest_path as find_shortest_path
import data_analysis.graph as graph
import data_analysis.community.leiden_graph as leiden


if __name__ == "__main__":
    actions_list = ["Collect data", "Analyze data", "Create graph", "Leiden", "Exit"]
    for i in actions_list:
        print(f"{actions_list.index(i) + 1}. {i}")
    action = int(input("Choose an action: "))
    if action == 1:
        print("Collecting data...")
        collect_data_sqlite.main()
    elif action == 2:
        print("Analyzing data...")
        find_shortest_path.main()
    elif action == 3:
        print("Creating graph...")
        graph.main()
    elif action == 4:
        print("Running Leiden algorithm...")
        leiden.main()
    elif action == 5:
        print("Exiting...")
        exit()


