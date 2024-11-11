#include <iostream>
#include <string>
#include <array>

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
        cout << "Search" << endl;
    } else if (action == "2"){
        cout << "Exit" << endl;
    }


    // End of program
    return 0;
}

// Function to greet the user
void greetUser(const std::string &name) {
    std::cout << "Hello, " << name << "! Welcome to the program!" << std::endl;
}
