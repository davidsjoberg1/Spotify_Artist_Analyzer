#ifndef DBHANDLER_H
#define DBHANDLER_H

#include <sqlite3.h>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

// Declaration of the function you want to call
vector<string> getRelatedArtists(string artist_id, sqlite3* db);
int getNumOfIncomingRelationships(string artist_id, sqlite3* db);
unordered_map<string, vector<string>> getArtistRelationships(sqlite3* db);

#endif
