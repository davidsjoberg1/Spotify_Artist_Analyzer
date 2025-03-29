# Define the compiler
CXX = g++

# Compiler flags
CXXFLAGS = -Wall -std=c++11 -I/opt/homebrew/Cellar/nlohmann-json/3.11.3/include

# Linker flags
LDFLAGS = -lsqlite3

# Target executable
TARGET = main

# Source files
SRCS = $(wildcard *.cpp) $(wildcard data_analysis/*.cpp) $(wildcard handlers/*.cpp)

# Object files
OBJS = $(SRCS:.cpp=.o)

# Rule to build the target executable
$(TARGET): $(OBJS)
	$(info Building target: $(TARGET))
	$(CXX) $(CXXFLAGS) $(OBJS) $(LDFLAGS) -o $(TARGET)

# Rule to build object files from source files
%.o: %.cpp
	$(info Building object: $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean rule to remove object files and the executable
clean:
	$(info Cleaning up...)
	$(RM) $(OBJS) $(TARGET)
