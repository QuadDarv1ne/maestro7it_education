#!/bin/bash

echo "Building Chess Engine..."
echo "======================"

# Create build directory
mkdir -p build
cd build

# Generate build files with CMake
cmake ..

# Build the project
make

if [ $? -eq 0 ]; then
    echo ""
    echo "Build successful!"
    echo "Executable created: chess_engine"
    echo ""
    echo "To run the chess engine:"
    echo "  cd build"
    echo "  ./chess_engine"
else
    echo ""
    echo "Build failed!"
    echo "Please check for compilation errors above."
fi