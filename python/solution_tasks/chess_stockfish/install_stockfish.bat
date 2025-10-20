@echo off
echo Installing Stockfish for Windows...
echo.

REM Check if Stockfish is already installed
where stockfish >nul 2>&1
if %errorlevel% == 0 (
    echo Stockfish is already installed!
    stockfish --version
    goto end
)

echo Downloading Stockfish...
echo Please download Stockfish manually from https://stockfishchess.org/download/
echo and follow the instructions in README.md
echo.
echo After downloading:
echo 1. Extract the stockfish executable to a folder
echo 2. Add that folder to your PATH environment variable
echo 3. Run this script again to verify installation

:end
echo.
echo Press any key to exit...
pause >nul