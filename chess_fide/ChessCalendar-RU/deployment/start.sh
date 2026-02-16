#!/bin/bash
# Startup script for ChessCalendar-RU

echo "Starting ChessCalendar-RU application..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d "env" ]; then
    echo "Activating virtual environment..."
    source env/bin/activate
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the application
echo "Starting application..."
python run.py