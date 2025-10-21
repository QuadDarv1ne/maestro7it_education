# Save/Load Game Features

## Overview
This document describes the file-based save/load system that has been implemented to allow players to save their chess games and continue them later. The system provides persistent storage of game states and comprehensive management of saved games.

## Features Implemented

### 1. Save Game Functionality
- Save current game state to JSON files
- Automatic timestamp-based filename generation
- Storage of complete game state including:
  - Player color and AI settings
  - Move history
  - Current board position (FEN notation)
  - Game statistics
  - Timestamp and version information
- Automatic creation of saves directory

### 2. Load Game Functionality
- Load previously saved games from JSON files
- Version compatibility checking
- Complete restoration of game state
- Error handling for missing or corrupted files

### 3. Game Management
- List all saved games
- Delete unwanted saved games
- Detailed game information in load menu (player color, move count, date)

### 4. File Storage
- JSON format for human-readable save files
- Automatic saves directory management
- Cross-platform file path handling
- Unicode support for internationalization

## Technical Implementation

### Core Methods
The save/load functionality is implemented in the `ChessGame` class:

1. **_save_game_to_file(filename=None)**
   - Saves current game state to a JSON file
   - Generates timestamp-based filename if none provided
   - Creates saves directory if it doesn't exist
   - Stores comprehensive game state information

2. **_load_game_from_file(filename)**
   - Loads game state from a JSON file
   - Performs version compatibility checking
   - Restores complete game state
   - Handles missing or corrupted files gracefully

3. **_list_saved_games()**
   - Returns list of all saved game files
   - Filters for .json files only
   - Handles missing saves directory

4. **_delete_saved_game(filename)**
   - Deletes a saved game file
   - Handles missing files gracefully
   - Provides user feedback on operation result

### Menu Integration
The functionality is integrated into the in-game menu system:

1. **Save Game Menu Item**
   - Accessible from main in-game menu
   - Calls _save_game_to_file() with automatic filename

2. **Load Game Menu**
   - Opens submenu with list of saved games
   - Shows detailed information about each saved game
   - Allows selection of game to load

3. **Delete Game Menu**
   - Opens submenu with list of saved games
   - Allows selection of game to delete

### Data Format
Saved games use JSON format with the following structure:
```json
{
  "player_color": "white",
  "skill_level": 5,
  "theme": "classic",
  "move_history": ["e2e4", "e7e5", "g1f3"],
  "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",
  "timestamp": 1700000000.0,
  "stats": { /* game statistics */ },
  "version": "1.0"
}
```

## File Structure
- Save methods implemented in [game/chess_game.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\chess_game.py)
- Menu integration in [game/in_game_menu.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\in_game_menu.py)
- Save files stored in `saves/` directory
- Tests in [tests/test_save_load.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\tests\test_save_load.py)
- Delete tests in [tests/test_delete_saved_games.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\tests\test_delete_saved_games.py)
- Demos in [demos/demonstrate_save_load.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\demos\demonstrate_save_load.py) and [demos/demonstrate_delete_games.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\demos\demonstrate_delete_games.py)

## Testing
Comprehensive tests ensure the reliability of the save/load system:

1. **Basic Save/Load Tests**
   - Creation and loading of save files
   - Verification of game state preservation
   - Error handling for missing files

2. **Edge Case Tests**
   - Handling of non-existent files
   - Automatic filename generation
   - Version compatibility checking

3. **Delete Functionality Tests**
   - Successful deletion of existing files
   - Handling of non-existent files
   - Integration with list functionality

## Usage Instructions

### Saving a Game
1. During gameplay, press ESC to open the in-game menu
2. Select "Сохранить игру" (Save Game)
3. Game will be saved to a file in the saves directory with a timestamp name

### Loading a Game
1. During gameplay, press ESC to open the in-game menu
2. Select "Загрузить игру" (Load Game)
3. Choose a saved game from the list
4. Game state will be restored completely

### Deleting a Game
1. During gameplay, press ESC to open the in-game menu
2. Select "Удалить игру" (Delete Game)
3. Choose a saved game to delete from the list
4. Confirm deletion

## Future Enhancements
Planned improvements for the save/load system:
1. Cloud synchronization of saved games
2. Export/Import functionality for sharing games
3. Game preview thumbnails
4. Search and filter functionality for saved games
5. Automatic cloud backup
6. Game tags and categories