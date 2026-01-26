#ifndef GAME_RULES_HPP
#define GAME_RULES_HPP

#include "board.hpp"
#include "move_generator.hpp"
#include <string>

class GameRules {
private:
    Board& board_;
    
public:
    GameRules(Board& board);
    
    // Move validation
    bool isValidMove(const Move& move) const;
    bool isValidMove(const std::string& algebraicNotation) const;
    
    // Game state checks
    bool isCheck(Color color) const;
    bool isCheckmate(Color color) const;
    bool isStalemate(Color color) const;
    bool isDrawByRepetition() const;
    bool isDrawByFiftyMoveRule() const;
    bool isInsufficientMaterial() const;
    
    // Move execution
    bool makeMove(const Move& move);
    bool makeMove(const std::string& algebraicNotation);
    
    // Game termination
    bool isGameOver() const;
    std::string getGameResult() const;
    
    // Utility methods
    Color getWinner() const;
    bool isDraw() const;
    
private:
    // Helper methods
    bool wouldLeaveKingInCheck(const Move& move) const;
    void updateGameStateAfterMove(const Move& move);
    bool hasLegalMoves(Color color) const;
    int countPieces(Color color) const;
    bool onlyKingsRemain() const;
};

#endif // GAME_RULES_HPP