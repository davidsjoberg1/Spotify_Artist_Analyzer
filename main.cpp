#include <iostream>
#include <string>
#include <array>
#include "data_analysis/findShortestPath.h"

using namespace std;

int main() {
    // Variable to store the user's name
    string action;
    array <string, 2> actions = {"Search", "Exit"};

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
        cout << "Exit" << endl;
    }


    // End of program
    return 0;
}

