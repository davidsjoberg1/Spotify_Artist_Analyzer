// FILE: dotenv.cpp
#include "dotenv.h"
#include <fstream>
#include <sstream>
#include <cstdlib>

namespace dotenv {
    void init() {
        std::ifstream file(".env");
        if (!file.is_open()) {
            return;
        }

        std::string line;
        while (std::getline(file, line)) {
            std::istringstream is_line(line);
            std::string key;
            if (std::getline(is_line, key, '=')) {
                std::string value;
                if (std::getline(is_line, value)) {
                    setenv(key.c_str(), value.c_str(), 1);
                }
            }
        }
    }
}