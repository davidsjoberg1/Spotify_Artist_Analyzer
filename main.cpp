#include <iostream>
#include <string>

// Declare any additional functions here
void greetUser(const std::string &name);

int main() {
    // Variable to store the user's name
    std::string name;

    // Output a welcome message
    std::cout << "Welcome to the C++ Program!" << std::endl;

    // Prompt the user for their name
    std::cout << "Please enter your name: ";
    std::getline(std::cin, name);

    // Call a function to greet the user
    greetUser(name);

    // Main program logic here
    int choice;
    std::cout << "Choose an option:" << std::endl;
    std::cout << "1. Say Hello" << std::endl;
    std::cout << "2. Exit" << std::endl;
    std::cout << "Enter your choice: ";
    std::cin >> choice;

    // Simple decision-making
    if (choice == 1) {
        std::cout << "Hello, " << name << "! Nice to meet you!" << std::endl;
    } else {
        std::cout << "Goodbye!" << std::endl;
    }

    // End of program
    return 0;
}

// Function to greet the user
void greetUser(const std::string &name) {
    std::cout << "Hello, " << name << "! Welcome to the program!" << std::endl;
}
