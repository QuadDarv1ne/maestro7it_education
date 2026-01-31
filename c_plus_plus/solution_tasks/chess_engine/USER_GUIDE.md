# 🎓 Chess Engine User Guide

Welcome to the comprehensive user guide for the Professional Chess Engine! This guide will help you get started, master advanced features, and make the most of all available interfaces.

## 📋 Table of Contents
1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Gameplay Basics](#gameplay-basics)
4. [Advanced Features](#advanced-features)
5. [Multiplayer Guide](#multiplayer-guide)
6. [PGN System](#pgn-system)
7. [Analysis Tools](#analysis-tools)
8. [Troubleshooting](#troubleshooting)
9. [Keyboard Shortcuts](#keyboard-shortcuts)

---

## 🚀 Getting Started

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Python**: Version 3.8 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 500MB free disk space

### Installation Steps

1. **Clone or Download the Repository**
   ```bash
   git clone <repository-url>
   cd chess_engine
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements_fastapi.txt
   ```

3. **Launch the Application**
   ```bash
   python chess_launcher.py
   ```

### First Launch
Upon first launch, you'll see the main menu with 7 options:
1. 🖥️ Console version
2. 🎮 Graphical interface (pygame)
3. 🔧 Service utilities
4. ⚡ FastAPI web service
5. 🌐 Web interface (HTML5)
6. 🔗 WebSocket server (multiplayer)
7. 🚪 Exit

---

## 🎯 Interface Overview

### 1. Console Interface (`chess_launcher.py` → Option 1)
**Best for**: Quick games, terminal enthusiasts
- Text-based chess board using Unicode characters
- Arrow key navigation
- Simple and lightweight
- Works on all systems without additional dependencies

### 2. Pygame Interface (`chess_launcher.py` → Option 2)
**Best for**: Rich gaming experience
- Beautiful graphical interface
- Smooth animations and sound effects
- Mouse-controlled gameplay
- Requires pygame installation

### 3. Web Interface (`chess_launcher.py` → Option 5)
**Best for**: Accessibility and sharing
- Modern HTML5/JavaScript interface
- Responsive design (works on mobile/desktop)
- No installation required on client side
- Real-time multiplayer support

### 4. FastAPI Service (`chess_launcher.py` → Option 4)
**Best for**: Developers and integrators
- RESTful API for programmatic access
- WebSocket support for real-time features
- Professional-grade backend
- Swagger documentation at `/docs`

### 5. WebSocket Server (`chess_launcher.py` → Option 6)
**Best for**: Multiplayer gaming
- Real-time online chess
- Automatic player matching
- Concurrent game support
- Low-latency communication

---

## ♟️ Gameplay Basics

### Making Moves
**Console/Web Interface**:
- Click or select piece, then destination square
- Valid moves are highlighted
- Drag-and-drop support in web interface

**Keyboard Navigation** (Console):
- Arrow keys to move cursor
- Enter to select/deselect pieces
- Spacebar for special actions

### Special Moves

#### Castling
- Move king two squares toward a rook
- Rook jumps to square next to king
- Conditions: No pieces between, king/rook never moved, no check

#### En Passant
- Pawn captures diagonally after opponent's double pawn move
- Only available immediately after double move
- Appears as special capture option

#### Pawn Promotion
- Pawns reaching 8th rank promote to queen/rook/bishop/knight
- Choice presented when pawn reaches promotion square
- Queens are most common choice

### Game States
- **Check**: King under attack (must escape)
- **Checkmate**: No legal moves to escape check (game ends)
- **Stalemate**: No legal moves but not in check (draw)
- **Draw by Repetition**: Same position occurs 3 times
- **50-Move Rule**: 50 moves without capture/pawn move

---

## 🔧 Advanced Features

### Difficulty Levels
Available in most interfaces:
- **Beginner** (Depth 1): Very basic AI
- **Easy** (Depth 2): Simple tactics
- **Medium** (Depth 3): Balanced play
- **Hard** (Depth 4): Strong tactical play
- **Expert** (Depth 5): Advanced strategic play

### Move Validation
The engine validates all moves according to official chess rules:
- Piece movement patterns
- King safety checks
- Pin and skewer detection
- Discovered check prevention

### Position Evaluation
Advanced evaluation considers:
- Material balance
- Piece mobility
- King safety
- Pawn structure
- Center control
- Development advantage

---

## 🌐 Multiplayer Guide

### Setting Up Online Play

1. **Start WebSocket Server** (Option 6 in launcher)
   ```
   WebSocket server running at: ws://localhost:8765
   ```

2. **Connect Clients**
   - Open web interface in multiple browser tabs
   - Click "Multiplayer" button
   - Enter player names when prompted
   - System automatically pairs players

### Playing Online
- **Automatic Matching**: Players are paired automatically
- **Real-time Updates**: Moves appear instantly for both players
- **Connection Handling**: Graceful handling of disconnections
- **Game Persistence**: Games continue even if one player reconnects

### Best Practices
- Ensure stable internet connection
- Use compatible browsers (Chrome, Firefox, Edge)
- Keep browser tabs active during gameplay
- Refresh page if connection issues occur

---

## 📂 PGN System

### What is PGN?
PGN (Portable Game Notation) is the standard format for recording chess games, readable by all chess software.

### Exporting Games
1. Complete a game in any interface
2. Click "Export PGN" button
3. File downloads automatically with timestamp
4. Share with other chess programs or players

### Importing Games
1. Click "Import PGN" button
2. Select PGN file from your computer
3. Game replays automatically with 0.5s delays
4. Study famous games or your previous matches

### PGN Structure Example
```
[Event "Tournament Name"]
[Site "Location"]
[Date "2026.01.30"]
[Round "1"]
[White "Player Name"]
[Black "Opponent Name"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 1-0
```

---

## 📊 Analysis Tools

### Game Analysis
Click "Analyze Game" to get:
- **Move count**: Total moves played
- **Captures**: Number of pieces captured
- **Checks**: Times king was checked
- **Material balance**: Current piece value difference
- **Game phases**: Opening, middle game, endgame breakdown

### Statistics Dashboard
Click "Statistics" to view:
- **Games played**: Total games recorded
- **Win/loss record**: Your performance history
- **Win rate**: Percentage of games won
- **Average game length**: Typical game duration
- **Active pieces**: Which pieces you use most
- **Opening preferences**: Your favorite openings

### Position Evaluation
- **Material count**: Piece values (P=1, N/B=3, R=5, Q=9)
- **Mobility**: Legal moves available
- **King safety**: Distance from center, protection level
- **Pawn structure**: Doubled, isolated, passed pawns

---

## ❓ Troubleshooting

### Common Issues

#### "Module not found" errors
```bash
# Install missing dependencies
pip install pygame websockets fastapi uvicorn
```

#### Web interface not loading
- Check if server is running: `http://localhost:8080`
- Verify port isn't blocked by firewall
- Try refreshing the browser page

#### Multiplayer connection issues
- Ensure WebSocket server is running (port 8765)
- Check network connectivity
- Verify no firewall blocking WebSocket connections

#### Slow performance
- Close other applications
- Reduce AI difficulty level
- Ensure sufficient system resources

### Performance Tips
- Use Release mode for compiled versions
- Close unnecessary browser tabs
- Use wired connection for multiplayer
- Restart application if performance degrades

---

## ⌨️ Keyboard Shortcuts

### Web Interface
| Shortcut | Action |
|----------|--------|
| Ctrl + N | New Game |
| Ctrl + Z | Undo Move |
| Ctrl + F | Flip Board |
| Ctrl + H | Get Hint |
| Ctrl + S | Export PGN |
| Ctrl + O | Import PGN |
| Ctrl + A | Analyze Game |
| Ctrl + T | Show Statistics |

### Console Interface
| Key | Action |
|-----|--------|
| Arrow Keys | Navigate board |
| Enter | Select/Deselect |
| Space | Special actions |
| Q | Quit game |
| N | New game |
| U | Undo move |

### Pygame Interface
| Shortcut | Action |
|----------|--------|
| Ctrl + S | Save game |
| Ctrl + O | Load game |
| Ctrl + R | Start recording |
| Ctrl + T | Stop recording |
| Ctrl + E | Export PGN |
| Esc | Main menu |

---

## 🎓 Learning Resources

### Recommended Study Order
1. **Basics**: Learn piece movements and basic rules
2. **Tactics**: Practice common tactical patterns
3. **Openings**: Study fundamental opening principles
4. **Endgames**: Master basic checkmates and pawn endings
5. **Strategy**: Learn positional concepts and planning

### Practice Tips
- Play regularly against different difficulty levels
- Analyze your games to identify mistakes
- Study classic games via PGN import
- Focus on one aspect at a time
- Use hints sparingly to develop calculation skills

### Advanced Features to Explore
- **Engine Analysis**: Compare your moves with engine suggestions
- **Move Timers**: Practice under time pressure
- **Blindfold Mode**: Improve visualization skills
- **Custom Positions**: Set up specific training positions
- **Variant Chess**: Experiment with different rule sets

---

## 🆘 Support and Community

### Getting Help
- Check this guide first for common questions
- Review error messages carefully
- Search existing documentation in `notes/` folder
- Test with simple positions to isolate issues

### Contributing
- Report bugs with detailed reproduction steps
- Suggest features with clear use cases
- Share interesting PGN files for testing
- Contribute to documentation improvements

### Feedback
We welcome your suggestions for improving this chess engine! The project aims to be educational, accessible, and fun for players of all levels.

---

*Happy chess playing! May your calculations be deep and your victories numerous!* ♔ ♕ ♖ ♗ ♘ ♙