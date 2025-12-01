@echo off
REM Script for building PCMetrics project
REM This script automates the CMake build process

echo ========================================
echo PCMetrics Build Script
echo ========================================

REM Check if build directory exists, if so, remove it
if exist build (
    echo Removing existing build directory...
    rmdir /s /q build
)

REM Create build directory
echo Creating build directory...
mkdir build

REM Change to build directory
cd build

REM Generate build files with CMake
echo Generating build files with CMake...
cmake .. -G "MinGW Makefiles"

REM Check if CMake generation was successful
if %ERRORLEVEL% NEQ 0 (
    echo Error: CMake generation failed!
    cd ..
    pause
    exit /b %ERRORLEVEL%
)

REM Build the project
echo Building project...
cmake --build .

REM Check if build was successful
if %ERRORLEVEL% NEQ 0 (
    echo Error: Build failed!
    cd ..
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo Executables created:
echo   - pcmetrics.exe (main application)
echo   - bin/pcmetrics_test.exe (test application)
echo.
echo To run the main application:
echo   pcmetrics.exe
echo.
echo To run the test application:
echo   bin/pcmetrics_test.exe
echo ========================================

REM Return to project root
cd ..

pause