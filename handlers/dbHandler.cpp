#include <iostream>
#include "sqlite3.h"
#include <vector>
#include <string>


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