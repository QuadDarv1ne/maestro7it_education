#ifndef CONSOLE_UI_HPP
#define CONSOLE_UI_HPP

#include "board.hpp"
#include "game_rules.hpp"
#include "minimax.hpp"
#include <string>
#include <vector>

enum class GameMode {
    HUMAN_VS_HUMAN,
    HUMAN_VS_AI,
    AI_VS_AI
};

enum class PlayerType {
    HUMAN,
    AI
};

class ConsoleUI {
private:
    Board board_;
    GameRules rules_;
    Minimax aiEngine_;
    
    GameMode gameMode_;
    PlayerType whitePlayer_;
    PlayerType blackPlayer_;
    
    int aiDifficulty_; // Depth level for AI
    
public:
    ConsoleUI();
    
    // Main game loop
    void run();
    
    // Menu system
    void showMainMenu();
    void showGameSettings();
    void startNewGame();
    
    // Game play
    void playGame();
    Move getPlayerMove(Color playerColor);
    Move getAIMove(Color playerColor);
    
    // Input handling
    Move parseMoveInput(const std::string& input) const;
    bool isValidMoveFormat(const std::string& input) const;
    
    // Display methods
    void showBoard() const;
    void showGameStatus() const;
    void showAvailableMoves(const std::vector<Move>& moves) const;
    void showMessage(const std::string& message) const;
    
    // Settings
    void configureGameSettings();
    void setGameMode(GameMode mode);
    void setPlayerTypes(PlayerType white, PlayerType black);
    void setAIDifficulty(int difficulty);
    
    // Utility methods
    std::string getColorName(Color color) const;
    std::string getMoveString(const Move& move) const;
    void clearScreen() const;
    
private:
    // Helper methods
    void initializeGame();
    bool handleSpecialCommands(const std::string& input);
    void showHelp() const;
};

#endif // CONSOLE_UI_HPP