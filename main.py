import collect_data_sqlite
import data_analysis.find_shortest_path as find_shortest_path

if __name__ == "__main__":
    actions_list = ["Collect data", "Analyze data", "Exit"]
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
        print("Exiting...")
        exit()


