@echo off
title Stockfish Installer for chess_stockfish
echo ======================================================
echo    Stockfish Installer for chess_stockfish Project
echo ======================================================
echo.

REM Check if Stockfish is already installed
echo Checking if Stockfish is already installed...
where stockfish >nul 2>&1
if %errorlevel% == 0 (
    echo.
    echo ✅ Stockfish is already installed!
    for /f "tokens=*" %%i in ('where stockfish') do set STOCKFISH_PATH=%%i
    echo Path: %STOCKFISH_PATH%
    stockfish --version
    goto end
)

echo.
echo ❌ Stockfish not found. Let's install it.
echo.

echo Please select installation method:
echo 1. Download precompiled Stockfish (recommended)
echo 2. Compile from source code (requires development tools)
echo 3. Exit
echo.

choice /c 123 /m "Select option"
if errorlevel 3 goto end
if errorlevel 2 goto compile
if errorlevel 1 goto download

:download
echo.
echo Downloading precompiled Stockfish...
echo.
echo Please follow these steps:
echo 1. Visit: https://stockfishchess.org/download/windows/
echo 2. Download the latest Windows version
echo 3. Extract the archive to a folder (e.g., C:\Program Files\stockfish\)
echo 4. Add that folder to your system PATH
echo.
echo Instructions for adding to PATH:
echo 1. Press Win+R, type "sysdm.cpl" and press Enter
echo 2. Go to "Advanced" tab
echo 3. Click "Environment Variables"
echo 4. Under "System Variables", find and select "Path", then click "Edit"
echo 5. Click "New" and add the path to your Stockfish folder
echo 6. Click "OK" to close all dialogs
echo 7. Restart your command prompt
echo.
goto manual_steps

:compile
echo.
echo Compiling Stockfish from source...
echo.
echo Requirements:
echo - MinGW-w64 or Visual Studio
echo - Git (optional, for latest source)
echo.
echo Steps:
echo 1. Install MinGW-w64 from https://www.mingw-w64.org/downloads/
echo 2. Add MinGW-w64 bin directory to PATH
echo 3. Open this directory in command prompt:
echo    cd "c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\stockfish\src"
echo 4. Run: make -j4 build
echo 5. The executable will be created in the src directory
echo 6. Copy it to a folder and add that folder to PATH
echo.
goto manual_steps

:manual_steps
echo.
echo After installation, please:
echo 1. Restart your command prompt
echo 2. Run this script again to verify installation
echo 3. Or run: python check_installation.py
echo.

:end
echo.
echo Press any key to exit...
pause >nul