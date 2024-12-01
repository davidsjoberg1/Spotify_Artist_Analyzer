# Define the compiler
CXX = g++

# Compiler flags
CXXFLAGS = -Wall -std=c++11

LDFLAGS = -lsqlite3

# Target executable
TARGET = main

# Source files
SRCS = main.cpp data_analysis/findShortestPath.cpp 

# Object files
OBJS = $(SRCS:.cpp=.o)

# Rule to build the target executable
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) $(LDFLAGS) -o $(TARGET)

# Rule to build object files from source files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean rule to remove object files and the executable
clean:
	rm -f $(OBJS) $(TARGET)