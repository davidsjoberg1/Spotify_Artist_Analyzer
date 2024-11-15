#include <iostream>
#include <string>
#include <cstdlib>
#include "../dotenv.h"  // Include the dotenv-cpp header

using namespace std;

string getToken() {
    // Load environment variables from the .env file
    dotenv::init();
    

    // Retrieve environment variables
    const char* client_id = std::getenv("CLIENT_ID1");
    const char* client_secret = std::getenv("CLIENT_SECRET1");

    if (client_id && client_secret) {
        cout << "CLIENT_ID1: " << client_id << endl;
        cout << "CLIENT_SECRET1: " << client_secret << endl;
        
    } else {
        cerr << "Environment variables not found" << endl;
    }

    return "";
}