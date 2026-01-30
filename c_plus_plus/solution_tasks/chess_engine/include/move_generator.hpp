#ifndef MOVE_GENERATOR_HPP
#define MOVE_GENERATOR_HPP

#include "board.hpp"
#include <vector>
#include <string>

struct Move {
    Square from;
    Square to;
    PieceType promotion;  // Для pawn promotion
    bool isCapture;
    bool isCheck;
    bool isCastling;      // Для рокировки
    bool isEnPassant;     // Для взятия на проходе
    
    Move() : from(INVALID_SQUARE), to(INVALID_SQUARE), 
             promotion(PieceType::EMPTY), isCapture(false), isCheck(false),
             isCastling(false), isEnPassant(false) {}
    
    Move(Square from, Square to) : from(from), to(to), 
                                   promotion(PieceType::EMPTY), 
                                   isCapture(false), isCheck(false),
                                   isCastling(false), isEnPassant(false) {}
    
    std::string toString() const;
};

// Реализация метода toString для Move
inline std::string Move::toString() const {
    if (from == INVALID_SQUARE || to == INVALID_SQUARE) {
        return "Invalid move";
    }
    
    // TODO: реализовать преобразование в алгебраическую нотацию
    return "Move from " + std::to_string(from) + " to " + std::to_string(to);
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
    bool isSquareAttackedOnBoard(const Board& board, Square square, Color byColor) const;
    bool isAttackedInDirection(const Board& board, Square square, int rankDelta, int fileDelta, Color byColor, bool diagonal) const;
    
private:
    // Helper methods
    std::vector<Move> addMovesInDirection(Square from, int fileDelta, int rankDelta) const;
    bool isValidSquare(Square square) const;
    bool isOpponentPiece(Square square) const;
    bool isEmptySquare(Square square) const;
    
    // Castling helpers
    bool canCastleKingside(Color color) const;
    bool canCastleQueenside(Color color) const;
    Square findKingSquare(Color color) const;
    Color oppositeColor(Color color) const;
};

#endif // MOVE_GENERATOR_HPP