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
    string sqlQueryString = "SELECT related_artist_id FROM artist_relationships WHERE artist_id = '" + artist_id + "'";
    const char* sqlQuery = sqlQueryString.c_str();
    rc = sqlite3_prepare_v2(db, sqlQuery, -1, &stmt, nullptr);
   

    // Execute and fetch rows
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW) {
        // Get the first column as a C-string
        const char* releated_artist = reinterpret_cast<const char*>(sqlite3_column_text(stmt, 0));
        artist_ids.push_back(string(releated_artist));
    }

    for (string artist_id : artist_ids){
        cout << artist_id << endl;
    }

    sqlite3_finalize(stmt);
    return artist_ids;

}