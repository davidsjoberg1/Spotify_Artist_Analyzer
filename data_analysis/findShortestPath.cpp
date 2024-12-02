#include <iostream>
#include <string>
#include <array>
#include "sqlite3.h"
#include <chrono>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <queue>
#include <deque>
#include "../handlers/dbHandler.h"

using namespace std;


int bfs(string a1, string a2, sqlite3* db){
    auto startTime = std::chrono::high_resolution_clock::now();
    unordered_set<string> explored;
    deque<vector<string>> queue;
    vector<string> path;


    queue.push_back({a1});
    explored.insert(a1);


    while (queue.size() > 0){

        path = queue.front();
        queue.pop_front();
        string node = path.back();

        if (node == a2){
            break;
        }
        vector<string> relatedArtists = getRelatedArtists(node, db);
        for (string relatedArtist: relatedArtists){
            if(explored.find(relatedArtist) == explored.end()){
                explored.insert(relatedArtist);
                vector<string> newPath = path;
                newPath.push_back(relatedArtist);
                queue.push_back(newPath);
            }
        }
        //cout << "\rPath size: " << path.size() << " Queue size: " << queue.size() << " Explored size: " << explored.size() << flush;
    }

    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::seconds>(end - startTime);
    cout << "Execution time: " << duration.count() << " seconds" << endl;

    return 0;
}

int getLenghts(string artist_id, sqlite3* db){
    auto startTime = chrono::high_resolution_clock::now();
    unordered_set<string> explored;
    unordered_map<int, int> pathLengths;
    deque<vector<string>> queue;
    vector<string> path;


    queue.push_back({artist_id});
    explored.insert(artist_id);
    
    int counter = 0;
    while (queue.size() > 0){
        counter++;

        path = queue.front();
        queue.pop_front();
        string node = path.back(); 
        

        vector<string> relatedArtists = getRelatedArtists(node, db);
        for (string relatedArtist: relatedArtists){
            if(explored.find(relatedArtist) == explored.end()){
                explored.insert(relatedArtist);
                vector<string> newPath = path;
                newPath.push_back(relatedArtist);
                queue.push_back(newPath);
            }
        }
        pathLengths[path.size()-1] = pathLengths[path.size()-1] + 1;

        //cout << "\rPath size: " << path.size() << " Queue size: " << queue.size() << " Explored size: " << explored.size() << flush;
    }

    auto end = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::seconds>(end - startTime);
    cout << "Execution time: " << duration.count() << " seconds" << endl;

    return 0;
}

int _findShortestPath(){
    string artist_id = "7zLm9op6LgPqKL62d1FzhO";
    string find_id = "2vpNYYY6ysRzg1H95E9QgG";

    sqlite3* db;
    char* errMsg = nullptr;

    if (sqlite3_open("../artists.db", &db) != SQLITE_OK) {
        cerr << "Error opening database: " << sqlite3_errmsg(db) << endl;
        return 1;
    }
    cout << "Database opened successfully!" << endl;


    getLenghts(artist_id, db);
    
    
    sqlite3_close(db); 






    return 0;

}

