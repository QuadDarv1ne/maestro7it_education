# In-Game Menu Usage Guide

## Overview
This guide explains how to use the new in-game menu feature that has been added to the chess_stockfish application. The menu provides convenient access to various game functions during gameplay.

## Accessing the Menu

### How to Open
- Press the **ESC** key at any time during gameplay to open the in-game menu
- The menu will appear as a semi-transparent overlay on top of the game board

### How to Close
- Press **ESC** again to close the menu and return to the game
- Select the "Продолжить игру" (Resume Game) option
- Click outside the menu area (if implemented)

## Menu Navigation

### Keyboard Navigation
- Use the **UP** and **DOWN** arrow keys to navigate between menu items
- Press **ENTER** or **SPACE** to select the highlighted item
- Press **ESC** to close the menu without making a selection

### Mouse Navigation
- Move your mouse cursor over menu items to highlight them
- Click on any menu item to select it
- Click outside the menu area to close it (if implemented)

## Menu Options

### 1. Продолжить игру (Resume Game)
- Closes the menu and returns to the game
- No changes are made to the current game state

### 2. Новая игра (New Game)
- Resets the current game and starts a new match
- All game statistics and history are cleared
- The same player settings (side, difficulty, theme) are maintained

### 3. Изменить параметры (Change Settings)
- Opens the settings submenu to modify game parameters
- Allows changing:
  - Player side (white/black)
  - Difficulty level (0-20)
  - Visual theme (classic, dark, blue, green, contrast)
- *Note: Full settings implementation is planned for future versions*

### 4. Переключить музыку (Toggle Music)
- Turns background music on or off
- Only available if a sound manager is present
- The change takes effect immediately

### 5. Переключить звуки (Toggle Sounds)
- Turns sound effects on or off
- Only available if a sound manager is present
- The change takes effect immediately

### 6. Главное меню (Main Menu)
- Exits the current game and returns to the main menu
- Allows selecting new game parameters
- Current game progress will be lost

### 7. Выход из игры (Quit Game)
- Exits the application completely
- Current game progress will be lost
- All resources are properly cleaned up

## Visual Design

### Menu Appearance
- Semi-transparent dark blue background for better visibility
- White text with blue highlighting for the selected item
- Disabled items are shown in gray with "(недоступно)" indicator
- Clean, modern design with rounded corners

### Layout
- Centered on the screen for easy access
- Sufficient spacing between menu items
- Clear visual hierarchy with a prominent title
- Navigation hints at the bottom of the menu

## Technical Details

### Integration Points
- The menu is integrated into the main game loop in [game/chess_game.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\game\chess_game.py)
- Event handling is processed when the menu is visible
- The menu has access to the sound manager for audio feedback
- Visual rendering uses the same Pygame surface as the main game

### Performance Considerations
- The menu only renders when visible, minimizing performance impact
- Efficient event handling prevents input lag
- No additional game logic is processed while the menu is active
- Memory usage is minimal with lightweight UI elements

## Troubleshooting

### Menu Not Appearing
- Ensure you're pressing the **ESC** key during gameplay
- Check that the game window has focus
- Verify that the menu feature is properly integrated (check for errors during game startup)

### Navigation Issues
- Make sure to use the **UP** and **DOWN** arrow keys for navigation
- If mouse navigation isn't working, ensure your mouse cursor is positioned correctly
- Disabled items cannot be selected and will be skipped during keyboard navigation

### Sound Problems
- If music/sound toggle options are grayed out, check that the sound manager is properly initialized
- Verify that audio files are present in the soundtrack directory
- Check system audio settings and volume levels

## Future Enhancements

### Planned Features
1. **Full Settings Implementation**: Complete the settings submenu to allow changing game parameters during gameplay
2. **Save/Load Integration**: Add save and load game options to the menu
3. **Statistics Display**: Show game statistics and performance metrics
4. **Tutorial Access**: Provide access to tutorials and help documentation
5. **Customization Options**: Allow customization of menu appearance and behavior

## Testing

### Verification Tests
- [demos/simple_menu_test.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\demos\simple_menu_test.py) - Automated tests for menu functionality
- [demos/integration_test.py](file://c:\Users\maksi\OneDrive\Documents\GitHub\maestro7it_education\python\solution_tasks\chess_stockfish\demos\integration_test.py) - Integration tests with the complete game system

### Manual Testing
1. Start a game and press ESC to open the menu
2. Navigate through all menu items using both keyboard and mouse
3. Test all functional menu options (new game, toggle music/sound, etc.)
4. Verify that the menu appears and disappears correctly
5. Check visual appearance and layout on different screen sizes