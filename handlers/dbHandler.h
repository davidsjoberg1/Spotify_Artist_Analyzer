#ifndef DBHANDLER_H
#define DBHANDLER_H

#include <sqlite3.h>
#include <vector>
#include <string>

using namespace std;

// Declaration of the function you want to call
vector<string> getRelatedArtists(string artist_id, sqlite3* db);

#endif
