#include <iostream>
#include "sqlite3.h"
#include <vector>
#include <string>
#include <unordered_map>



using namespace std;

vector<string> getRelatedArtists(string artist_id, sqlite3* db){
    vector<string> artist_ids;
    int rc;
    sqlite3_stmt* stmt;

    // Prepare SQL Query
    const char* sqlQuery = "SELECT related_artist_id FROM artist_relationships WHERE artist_id = ?";
    rc = sqlite3_prepare_v2(db, sqlQuery, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << endl;
        return artist_ids;
    }

    // Bind the artist_id parameter
    rc = sqlite3_bind_text(stmt, 1, artist_id.c_str(), -1, SQLITE_STATIC);
    if (rc != SQLITE_OK) {
        cerr << "Failed to bind parameter: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return artist_ids;
    }

    // Execute and fetch rows
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        // Get the first column as a C-string
        const char* releated_artist = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
        if (releated_artist){
            artist_ids.push_back(string(releated_artist));
        }
    }
    
    if (rc != SQLITE_DONE) {
        cerr << "Failed to execute statement: " << sqlite3_errmsg(db) << endl;
    }
    
    sqlite3_finalize(stmt);
    return artist_ids;

}


int getNumOfIncomingRelationships(string artist_id, sqlite3* db){
    auto startTime = chrono::high_resolution_clock::now();
    int numOfIncoming = 0;
    int rc;
    sqlite3_stmt* stmt;

    // Prepare SQL Query
    const char* sqlQuery = "SELECT COUNT(*) FROM artist_relationships WHERE related_artist_id = ?";
    rc = sqlite3_prepare_v2(db, sqlQuery, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << endl;
        return numOfIncoming;
    }

    // Bind the artist_id parameter
    rc = sqlite3_bind_text(stmt, 1, artist_id.c_str(), -1, SQLITE_STATIC);
    if (rc != SQLITE_OK) {
        cerr << "Failed to bind parameter: " << sqlite3_errmsg(db) << endl;
        sqlite3_finalize(stmt);
        return numOfIncoming;
    }

    // Execute and fetch rows
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        // Get the first column as a C-string
        const char* numOfIncoming_ = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
        if (numOfIncoming_){
            numOfIncoming = stoi(string(numOfIncoming_));
        }
    }
    
    if (rc != SQLITE_DONE) {
        cerr << "Failed to execute statement: " << sqlite3_errmsg(db) << endl;
    }
    
    sqlite3_finalize(stmt);
    auto end = chrono::high_resolution_clock::now();
    auto execTime = chrono::duration_cast<chrono::seconds>(end - startTime);
    cout << "Execution time: " << execTime.count() << " seconds" << endl;
    return numOfIncoming;

}

unordered_map<string, vector<string>> getArtistRelationships(sqlite3* db){
    auto startTime = chrono::high_resolution_clock::now();
    unordered_map<string, vector<string>> artistRelationships;
    int rc;
    sqlite3_stmt* stmt;

    // Prepare SQL Query
    const char* sqlQuery = "SELECT * FROM artist_relationships";
    rc = sqlite3_prepare_v2(db, sqlQuery, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        cerr << "Failed to prepare statement: " << sqlite3_errmsg(db) << endl;
        return artistRelationships;
    }
    int counter = 0;
    // Execute and fetch rows
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        counter ++;
        // Get the first column as a C-string
        const char* artist_id = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
        const char* related_id = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 1));

        if (artist_id && related_id){
            artistRelationships[string(artist_id)].push_back(string(related_id));
            //cout << "counter:" << counter << "artist: " << string(artist_id) << " related: " << string(related_id) << endl;
            
        }
    }
    cout << "Number of relationships: " << counter << endl;
    if (rc != SQLITE_DONE) {
        cerr << "Failed to execute statement: " << sqlite3_errmsg(db) << endl;
    }

    
    sqlite3_finalize(stmt);
    auto end = chrono::high_resolution_clock::now();
    auto execTime = chrono::duration_cast<chrono::seconds>(end - startTime);
    cout << "Execution time: " << execTime.count() << " seconds" << endl;
    return artistRelationships;

}