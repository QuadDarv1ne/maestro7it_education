#ifndef MOVE_GENERATOR_HPP
#define MOVE_GENERATOR_HPP

#include "board.hpp"
#include <vector>
#include <string>

struct Move {
    Square from;
    Square to;
    PieceType promotion;  // For pawn promotion
    bool isCapture;
    bool isCheck;
    
    Move() : from(INVALID_SQUARE), to(INVALID_SQUARE), 
             promotion(PieceType::EMPTY), isCapture(false), isCheck(false) {}
    
    Move(Square from, Square to) : from(from), to(to), 
                                   promotion(PieceType::EMPTY), 
                                   isCapture(false), isCheck(false) {}
    
    std::string toString() const;
};

class MoveGenerator {
private:
    const Board& board_;
    
public:
    MoveGenerator(const Board& board);
    
    // Generate all legal moves for current player
    std::vector<Move> generateLegalMoves() const;
    
    // Generate pseudo-legal moves (may include moves that leave king in check)
    std::vector<Move> generatePseudoLegalMoves() const;
    
    // Check if a move is legal
    bool isLegalMove(const Move& move) const;
    
    // Specific piece move generators
    std::vector<Move> generatePawnMoves(Square from) const;
    std::vector<Move> generateKnightMoves(Square from) const;
    std::vector<Move> generateBishopMoves(Square from) const;
    std::vector<Move> generateRookMoves(Square from) const;
    std::vector<Move> generateQueenMoves(Square from) const;
    std::vector<Move> generateKingMoves(Square from) const;
    
    // Special moves
    std::vector<Move> generateCastlingMoves() const;
    std::vector<Move> generateEnPassantMoves() const;
    
    // Validation helpers
    bool wouldBeInCheck(Square from, Square to) const;
    bool isSquareAttacked(Square square, Color byColor) const;
    
private:
    // Helper methods
    std::vector<Move> addMovesInDirection(Square from, int fileDelta, int rankDelta) const;
    bool isValidSquare(Square square) const;
    bool isOpponentPiece(Square square) const;
    bool isEmptySquare(Square square) const;
};

#endif // MOVE_GENERATOR_HPP