# In-Game Menu Features

## Overview
This document describes the in-game menu system that has been implemented to enhance the chess game experience. The menu can be accessed during gameplay by pressing the ESC key and provides various options for controlling the game.

## Features Implemented

### 1. Main Menu Access
- Press ESC during gameplay to open the in-game menu
- Semi-transparent overlay for better visibility
- Intuitive navigation with keyboard arrows or mouse
- Smooth animations for opening/closing

### 2. Menu Options
The in-game menu provides the following options:

1. **Продолжить игру** (Resume Game)
   - Closes the menu and returns to the game

2. **Сдаться** (Resign)
   - Surrender the current game

3. **Новая игра** (New Game)
   - Resets the current game to start a new match

4. **Сохранить игру** (Save Game)
   - Saves the current game state to a file with timestamp

5. **Загрузить игру** (Load Game)
   - Opens a submenu to load a previously saved game
   - Shows detailed information about saved games (player color, move count, date)

6. **Удалить игру** (Delete Game)
   - Opens a submenu to delete saved games

7. **Настройки** (Settings)
   - Allows changing game parameters (side, difficulty, theme)

8. **Переключить музыку** (Toggle Music)
   - Turns background music on/off

9. **Переключить звуки** (Toggle Sounds)
   - Turns sound effects on/off

10. **Главное меню** (Main Menu)
    - Returns to the main menu screen

11. **Выход из игры** (Quit Game)
    - Exits the application

### 3. Submenus
The menu system includes several submenus:

1. **Settings Menu**
   - Toggle player side (white/black)
   - Change difficulty level (1-20)
   - Switch themes (classic, dark, blue, green, contrast)

2. **Load Game Menu**
   - Displays list of saved games with detailed information
   - Shows player color, move count, and save date
   - Select a game to load

3. **Delete Game Menu**
   - Displays list of saved games
   - Select a game to delete

### 4. Navigation
- **Keyboard**: Use UP/DOWN arrow keys to navigate, ENTER to select, ESC to close or go back
- **Mouse**: Click directly on menu items to select them
- **Back Navigation**: ESC key or "Назад" option to return to previous menu

### 5. Visual Design
- Semi-transparent dark blue background
- Highlighted selection for current menu item
- Clear visual indication of disabled options
- Hover effects for mouse navigation
- Smooth animations and transitions
- Icons for each menu item
- Consistent with the game's overall aesthetic

## Technical Implementation

### Integration Points
- Integrated with `ChessGame` class in [game/chess_game.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\chess_game.py)
- Uses `SoundManager` for audio feedback
- Handles all Pygame events when active
- File-based save/load system in [game/chess_game.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\chess_game.py)

### File Structure
- Main implementation in [game/in_game_menu.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\in_game_menu.py)
- Integrated into game loop in [game/chess_game.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\chess_game.py)
- Main menu loop updated in [main.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\main.py)

## Testing
Test scripts are available to verify menu functionality:
- Basic menu functionality: [demos/test_in_game_menu.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\demos\test_in_game_menu.py)
- Save/load functionality: [tests/test_save_load.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\tests\test_save_load.py)
- Delete functionality: [tests/test_delete_saved_games.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\tests\test_delete_saved_games.py)

## Future Enhancements
Planned improvements for the in-game menu:
1. Game statistics display within the menu
2. Tutorial access
3. Export/Import functionality for saved games
4. Cloud synchronization of saved games