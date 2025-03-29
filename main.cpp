#include <iostream>
#include <string>
#include <array>
#include "data_analysis/findShortestPath.h"
#include "data_analysis/graph.h"

using namespace std;

int main() {
    // Variable to store the user's name
    string action;
    array <string, 3> actions = {"Search", "Graph", "Exit"};

    for (int i = 0; i < actions.size(); i++) {
        cout << i + 1 << ". " << actions[i] << endl;
    }

    // Prompt the user for their name
    cout << "Enter the desired action:";
    getline(std::cin, action);

    if (action == "1"){
        findShortestPath();
        cout << "Search" << endl;

    } else if (action == "2"){
        cout << "Create Graph" << endl;
        createGraph();

    }
    else if (action == "3"){
        cout << "Exit" << endl;
    }


    // End of program
    return 0;
}

