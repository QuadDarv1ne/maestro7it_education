# In-Game Menu Features

## Overview
This document describes the in-game menu system that has been implemented to enhance the chess game experience. The menu can be accessed during gameplay by pressing the ESC key and provides various options for controlling the game.

## Features Implemented

### 1. Main Menu Access
- Press ESC during gameplay to open the in-game menu
- Semi-transparent overlay for better visibility
- Intuitive navigation with keyboard arrows or mouse

### 2. Menu Options
The in-game menu provides the following options:

1. **Продолжить игру** (Resume Game)
   - Closes the menu and returns to the game

2. **Новая игра** (New Game)
   - Resets the current game to start a new match

3. **Изменить параметры** (Change Settings)
   - Allows changing game parameters (side, difficulty, theme)

4. **Переключить музыку** (Toggle Music)
   - Turns background music on/off

5. **Переключить звуки** (Toggle Sounds)
   - Turns sound effects on/off

6. **Главное меню** (Main Menu)
   - Returns to the main menu screen

7. **Выход из игры** (Quit Game)
   - Exits the application

### 3. Navigation
- **Keyboard**: Use UP/DOWN arrow keys to navigate, ENTER to select, ESC to close
- **Mouse**: Click directly on menu items to select them

### 4. Visual Design
- Semi-transparent dark blue background
- Highlighted selection for current menu item
- Clear visual indication of disabled options
- Consistent with the game's overall aesthetic

## Technical Implementation

### Integration Points
- Integrated with `ChessGame` class in [game/chess_game.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\chess_game.py)
- Uses `SoundManager` for audio feedback
- Handles all Pygame events when active

### File Structure
- Main implementation in [game/in_game_menu.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\in_game_menu.py)
- Integrated into game loop in [game/chess_game.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\chess_game.py)
- Main menu loop updated in [main.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\main.py)

## Testing
A test script is available at [demos/test_in_game_menu.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\demos\test_in_game_menu.py) to verify menu functionality.

## Future Enhancements
Planned improvements for the in-game menu:
1. Full settings menu implementation for changing side, difficulty, and theme
2. Save/Load game options
3. Game statistics display
4. Tutorial access