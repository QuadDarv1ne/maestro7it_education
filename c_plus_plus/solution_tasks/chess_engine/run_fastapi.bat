@echo off
cls
echo ========================================
echo    FastAPI Chess Server Launcher
echo ========================================
echo.

REM Check if requirements are installed
echo Checking Python dependencies...
python -c "import fastapi, uvicorn, websockets" 2>nul
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements_fastapi.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies. Please install manually:
        echo pip install fastapi uvicorn[standard] websockets pydantic
        pause
        exit /b 1
    )
)

echo Dependencies OK!

REM Check if chess engine components exist
echo Checking chess engine components...
if not exist "chess_engine_wrapper.py" (
    echo Error: chess_engine_wrapper.py not found!
    pause
    exit /b 1
)

if not exist "optimized_move_generator.py" (
    echo Error: optimized_move_generator.py not found!
    pause
    exit /b 1
)

if not exist "enhanced_chess_ai.py" (
    echo Error: enhanced_chess_ai.py not found!
    pause
    exit /b 1
)

echo All components found!

REM Start the FastAPI server
echo.
echo Starting FastAPI Chess Server...
echo Server will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python fastapi_chess.py

pause