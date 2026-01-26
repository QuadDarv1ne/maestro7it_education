#ifndef POSITION_EVALUATOR_HPP
#define POSITION_EVALUATOR_HPP

#include "board.hpp"
#include "move_generator.hpp"
#include <map>

class PositionEvaluator {
private:
    const Board& board_;
    
    // Piece-square tables for positional evaluation
    static const int pawnTable[64];
    static const int knightTable[64];
    static const int bishopTable[64];
    static const int rookTable[64];
    static const int queenTable[64];
    static const int kingMiddleGameTable[64];
    static const int kingEndGameTable[64];
    
public:
    PositionEvaluator(const Board& board);
    
    // Main evaluation function
    int evaluate() const;
    
    // Component evaluations
    int materialEvaluation() const;
    int positionalEvaluation() const;
    int mobilityEvaluation() const;
    int kingSafetyEvaluation() const;
    int pawnStructureEvaluation() const;
    
    // Game phase detection
    bool isEndGame() const;
    int getGamePhase() const;
    
    // Piece-specific evaluations
    int evaluatePiece(PieceType type, Square square, Color color) const;
    int getPSTValue(PieceType type, Square square, Color color) const;
    
private:
    // Helper methods
    int getPieceMobility(Square square) const;
    int getKingSafety(Color color) const;
    int getPawnStructure(Color color) const;
    bool isPassedPawn(Square square) const;
    bool isIsolatedPawn(Square square) const;
    int flipSquare(Square square) const; // For black perspective
};

#endif // POSITION_EVALUATOR_HPP