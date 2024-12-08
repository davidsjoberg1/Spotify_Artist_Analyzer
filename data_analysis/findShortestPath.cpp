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
#include <nlohmann/json.hpp>
#include <fstream>
#include "findShortestPath.h"



using namespace std;


void writeToJSON(string artist_id, unordered_map<int, int> pathLengths, int execTime){
    try{
        const string fileName = "data/1000_random_artists_cpp.json";
    
        ifstream inFile(fileName);
        if (!inFile.is_open()) {
            throw std::runtime_error("Could not open input file.");
        }
        nlohmann::json jsonData;
        inFile >> jsonData; // Parse JSON file content into jsonData
        inFile.close();

        for (int i = 0; i < jsonData.size(); i++){
            if (jsonData[i]["artist_id"] == artist_id) {
                jsonData[i]["path_lengths"] = pathLengths;
                jsonData[i]["time"] = execTime;
                break;
            }
        }

        ofstream outFile(fileName);
        if (!outFile.is_open()) {
            throw std::runtime_error("Could not open output file.");
        }
        outFile << jsonData.dump(4); // Write jsonData to output file
        outFile.close();
    }
    catch (const exception& e) {
        cerr << "Error: " << e.what() << std::endl;

    }
}

string getUnsearchedArtist(){
    try{
        const string fileName = "data/1000_random_artists_cpp.json";
    
        ifstream inFile(fileName);
        if (!inFile.is_open()) {
            throw std::runtime_error("Could not open input file.");
        }
        nlohmann::json jsonData;
        inFile >> jsonData; // Parse JSON file content into jsonData
        inFile.close();

        for (int i = 0; i < jsonData.size(); i++){
            if (jsonData[i]["path_lengths"] == 0) {
                cout << "Num of searched: " << i << endl;
                return jsonData[i]["artist_id"];
            }
        }
        cout << "none" << endl;
        return "";

    }
    catch (const exception& e) {
        cerr << "Error: " << e.what() << std::endl;
        return "";
    }
    return "";
}

 int getLenghts(string artist_id, sqlite3* db, unordered_map<int, int>& pathLengths){
    auto startTime = chrono::high_resolution_clock::now();
    unordered_set<string> explored;
    deque<vector<string>> queue;
    vector<string> path;
    vector<string> newPath;
    string node;
    vector<string> relatedArtists;

    queue.push_back({artist_id});
    explored.insert(artist_id);
    
    while (queue.size() > 0){
        
        path = queue.front();
        queue.pop_front();
        node = path.back(); 

        relatedArtists = getRelatedArtists(node, db);
        for (string relatedArtist: relatedArtists){
            if(explored.find(relatedArtist) == explored.end()){
                explored.insert(relatedArtist);
                newPath = path;
                newPath.push_back(relatedArtist);
                queue.push_back(newPath);
            }
        }
        
        pathLengths[path.size()-1] = pathLengths[path.size()-1] + 1;

    }

    auto end = chrono::high_resolution_clock::now();
    auto execTime = chrono::duration_cast<chrono::seconds>(end - startTime);
    cout << "Execution time: " << execTime.count() << " seconds" << endl;

    return execTime.count();
}

int findShortestPath(){
    sqlite3* db;
    if (sqlite3_open("../artists.db", &db) != SQLITE_OK) {
        cerr << "Error opening database: " << sqlite3_errmsg(db) << endl;
        return 1;
    }
    cout << "Database opened successfully!" << endl;
    while (true){
        string artist_id = getUnsearchedArtist();
        if (artist_id == ""){
            break;
        }
        // Key: Length of a path, Value: Number of paths with that length
        unordered_map<int, int> pathLengths;
        int execTime = getLenghts(artist_id, db, pathLengths);
        writeToJSON(artist_id, pathLengths, execTime);

    }    
    sqlite3_close(db); 
    return 0;

}

