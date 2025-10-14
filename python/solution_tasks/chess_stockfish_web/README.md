# Chess Stockfish Web Application

A web-based chess game powered by the Stockfish engine.

## Prerequisites

1. Python 3.7+
2. Stockfish chess engine

## Installation

### 1. Install Stockfish Engine

#### Windows:
- Download Stockfish from [https://stockfishchess.org/download/](https://stockfishchess.org/download/)
- Extract the executable (e.g., `stockfish-windows-x86-64.exe`)
- Add the path to the executable to your system PATH or set the `STOCKFISH_PATH` environment variable

#### macOS:
```bash
brew install stockfish
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install stockfish
```

### 2. Set up Python Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows (PowerShell):
```bash
venv\Scripts\Activate.ps1
```

Windows (Command Prompt):
```bash
venv\Scripts\activate.bat
```

macOS/Linux:
```bash
source venv/bin/activate
```

### 4. Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at http://127.0.0.1:5001/

## Usage

1. Select your side (white or black)
2. Choose difficulty level (0-20)
3. Click "Start Game"
4. Play by dragging pieces on the board