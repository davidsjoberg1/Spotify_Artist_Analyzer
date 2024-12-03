#ifndef FIND_SHORTEST_PATH_H
#define FIND_SHORTEST_PATH_H

#include <sqlite3.h>
#include <string>
#include <unordered_map>


using namespace std;

// Declaration of the function you want to call
int findShortestPath();
int getLenghts(string artist_id, sqlite3* db);
string getUnsearchedArtist();
void writeToJSON(string artist_id, unordered_map<int, int> pathLengths, int execTime);

#endif
