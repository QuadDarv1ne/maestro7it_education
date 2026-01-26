@echo off
echo Building Chess Engine...
echo ======================

REM Create build directory
if not exist build mkdir build
cd build

REM Generate build files with CMake
cmake .. -G "MinGW Makefiles"

REM Build the project
mingw32-make

if %ERRORLEVEL% == 0 (
    echo.
    echo Build successful!
    echo Executable created: chess_engine.exe
    echo.
    echo To run the chess engine:
    echo   cd build
    echo   chess_engine.exe
) else (
    echo.
    echo Build failed!
    echo Please check for compilation errors above.
)

pause