#ifndef MOVE_GENERATOR_HPP
#define MOVE_GENERATOR_HPP

#include "board.hpp"
#include <vector>
#include <string>
#include <utility>  // for std::move

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
    std::string toAlgebraic() const;
};

// Реализация методов для Move
inline std::string Move::toAlgebraic() const {
    if (from == INVALID_SQUARE || to == INVALID_SQUARE) return "0000";
    
    std::string result = "";
    result += (char)('a' + (from % 8));
    result += (char)('1' + (from / 8));
    result += (char)('a' + (to % 8));
    result += (char)('1' + (to / 8));
    
    if (promotion != PieceType::EMPTY) {
        if (promotion == PieceType::QUEEN) result += 'q';
        else if (promotion == PieceType::ROOK) result += 'r';
        else if (promotion == PieceType::BISHOP) result += 'b';
        else if (promotion == PieceType::KNIGHT) result += 'n';
    }
    
    return result;
}

inline std::string Move::toString() const {
    return toAlgebraic();
};

class MoveGenerator {
private:
    const Board& board_;
    
public:
    explicit MoveGenerator(const Board& board) noexcept;
    
    // Генерация всех легальных ходов для текущего игрока
    [[nodiscard]] std::vector<Move> generateLegalMoves() const;
    
    // Генерация псевдо-легальных ходов (может включать ходы, оставляющие короля под шахом)
    [[nodiscard]] std::vector<Move> generatePseudoLegalMoves() const;
    
    // Проверка, является ли ход легальным
    [[nodiscard]] bool isLegalMove(const Move& move) const noexcept;
    
    // Генераторы ходов для конкретных фигур
    [[nodiscard]] std::vector<Move> generatePawnMoves(Square from) const;
    [[nodiscard]] std::vector<Move> generateKnightMoves(Square from) const;
    [[nodiscard]] std::vector<Move> generateBishopMoves(Square from) const;
    [[nodiscard]] std::vector<Move> generateRookMoves(Square from) const;
    [[nodiscard]] std::vector<Move> generateQueenMoves(Square from) const;
    [[nodiscard]] std::vector<Move> generateKingMoves(Square from) const;
    
    // Специальные ходы
    [[nodiscard]] std::vector<Move> generateCastlingMoves() const;
    [[nodiscard]] std::vector<Move> generateEnPassantMoves() const;
    
    // Вспомогательные методы валидации
    [[nodiscard]] bool wouldBeInCheck(const Move& move) const;
    [[nodiscard]] bool isSquareAttacked(Square square, Color byColor) const noexcept;
    [[nodiscard]] bool isSquareAttackedOnBoard(const Board& board, Square square, Color byColor) const noexcept;
    [[nodiscard]] bool isAttackedInDirection(const Board& board, Square square, int rankDelta, int fileDelta, Color byColor, bool diagonal) const noexcept;
    
private:
    // Вспомогательные методы
    [[nodiscard]] std::vector<Move> addMovesInDirection(Square from, int fileDelta, int rankDelta) const;
    [[nodiscard]] bool isValidSquare(Square square) const noexcept;
    [[nodiscard]] bool isOpponentPiece(Square square) const noexcept;
    [[nodiscard]] bool isEmptySquare(Square square) const noexcept;
    
    // Вспомогательные методы для рокировки
    [[nodiscard]] bool canCastleKingside(Color color) const noexcept;
    [[nodiscard]] bool canCastleQueenside(Color color) const noexcept;
    [[nodiscard]] Square findKingSquare(Color color) const noexcept;
    [[nodiscard]] Color oppositeColor(Color color) const noexcept;
};

#endif // MOVE_GENERATOR_HPP