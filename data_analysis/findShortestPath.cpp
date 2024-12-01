#include <iostream>
#include <string>
#include <array>
#include "sqlite3.h"
#include <chrono>
#include <unordered_map>
#include <vector>


using namespace std;

vector<string> getRelatedArtists(string artist_id, sqlite3* db){
    vector<string> artist_ids;
    int rc;
    sqlite3_stmt* stmt;

    // Prepare SQL Query
    string sqlQueryString = "SELECT related_artist_id FROM artist_relationships WHERE artist_id = '" + artist_id + "'";
    const char* sqlQuery = sqlQueryString.c_str();
    rc = sqlite3_prepare_v2(db, sqlQuery, -1, &stmt, nullptr);
   

    // Execute and fetch rows
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        // Get the first column as a C-string
        const char* releated_artist = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
        artist_ids.push_back(string(releated_artist));
    }

    sqlite3_finalize(stmt);
    return artist_ids;

}

int getLenghts(string artist_id, sqlite3* db){
    auto startTime = std::chrono::high_resolution_clock::now();

    unordered_map<string, int> explored;
    unordered_map<string, int> found;
    unordered_map<int, int> pathLengths;
    vector<vector<string>> queue;
    vector<string> path;
    string node;
    int maxLength = 0;

    found[artist_id] = 1;
    queue.push_back({artist_id});

    while (queue.size() > 0){

        path = queue.back();
        queue.pop_back();
        node = path.back();
        

        for (string relatedArtist: getRelatedArtists(node, db)){
            if(found.find(relatedArtist) == found.end()){
                found[relatedArtist] = 1;
                vector<string> newPath = path;
                newPath.push_back(relatedArtist);
                queue.push_back(newPath);
            }
        }
        explored[node] = 0;

        int pathLen = path.size();
        pathLengths[pathLen - 1] = pathLengths[pathLen -1 ] + 1;
        
    }

    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::seconds>(end - startTime);
    cout << "Execution time: " << duration.count() << " seconds" << endl;


    return 0;
}

int _findShortestPath(){
    string artist_id = "7zLm9op6LgPqKL62d1FzhO";

    sqlite3* db;
    char* errMsg = nullptr;

    if (sqlite3_open("../artists.db", &db) != SQLITE_OK) {
        cerr << "Error opening database: " << sqlite3_errmsg(db) << endl;
        return 1;
    }
    cout << "Database opened successfully!" << endl;

    getRelatedArtists(artist_id, db);

    getLenghts(artist_id, db);

    sqlite3_close(db); 






    return 0;

}

