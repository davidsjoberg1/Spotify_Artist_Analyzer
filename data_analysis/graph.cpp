#include <iostream>
#include <string>
#include <array>
#include "sqlite3.h"
#include "../handlers/dbHandler.h"
#include <fstream>




using namespace std;

int findNum(){
    sqlite3* db;
    if (sqlite3_open("../artists.db", &db) != SQLITE_OK) {
        cerr << "Error opening database: " << sqlite3_errmsg(db) << endl;
        return 1;
    }
    string artistID = "7zLm9op6LgPqKL62d1FzhO";
    cout << "Database opened successfully!" << endl;
    getArtistRelationships(db);
    cout << "HEj" << endl;

    
    sqlite3_close(db); 
    return 0;

}

