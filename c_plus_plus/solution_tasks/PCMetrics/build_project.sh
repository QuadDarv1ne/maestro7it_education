#!/bin/bash

# Script for building PCMetrics project
# This script automates the CMake build process

echo "========================================"
echo "PCMetrics Build Script"
echo "========================================"

# Check if build directory exists, if so, remove it
if [ -d "build" ]; then
    echo "Removing existing build directory..."
    rm -rf build
fi

# Create build directory
echo "Creating build directory..."
mkdir build

# Change to build directory
cd build

# Generate build files with CMake
echo "Generating build files with CMake..."
cmake ..

# Check if CMake generation was successful
if [ $? -ne 0 ]; then
    echo "Error: CMake generation failed!"
    cd ..
    exit 1
fi

# Build the project
echo "Building project..."
cmake --build .

# Check if build was successful
if [ $? -ne 0 ]; then
    echo "Error: Build failed!"
    cd ..
    exit 1
fi

echo ""
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo "Executables created:"
echo "  - pcmetrics (main application)"
echo "  - bin/pcmetrics_test (test application)"
echo ""
echo "To run the main application:"
echo "  ./pcmetrics"
echo ""
echo "To run the test application:"
echo "  ./bin/pcmetrics_test"
echo "========================================"

# Return to project root
cd ..