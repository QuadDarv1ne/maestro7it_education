#ifndef BITBOARD_HPP
#define BITBOARD_HPP

#include <cstdint>
#include <iostream>
#include <vector>
#include <string>

/**
 * @brief Bitboard представление шахматной доски
 * 
 * Использует 64-битные целые числа для представления позиций фигур
 * на доске, что обеспечивает высокую производительность операций.
 */
class Bitboard {
public:
    // Типы для bitboard представления
    using BitboardType = uint64_t;
    
    // Константы для фигур
    enum PieceType {
        PAWN = 0, KNIGHT, BISHOP, ROOK, QUEEN, KING, PIECE_TYPE_COUNT
    };
    
    // Константы для цветов
    enum Color {
        WHITE = 0, BLACK, COLOR_COUNT
    };
    
private:
    // Bitboards для каждой фигуры каждого цвета
    BitboardType pieces_[COLOR_COUNT][PIECE_TYPE_COUNT];
    
    // Bitboards для всех фигур каждого цвета
    BitboardType occupancy_[COLOR_COUNT];
    
    // Bitboard для всех фигур на доске
    BitboardType all_pieces_;
    
    // Цвет игрока, который делает следующий ход
    Color side_to_move_;
    
    // Рокировки
    bool castling_rights_[COLOR_COUNT][2]; // [color][king_side, queen_side]
    
    // Проходная пешка (en passant)
    int en_passant_square_;
    
    // Номер хода
    int half_move_clock_;
    int full_move_number_;
    
    // Вспомогательные функции
    static constexpr int squareToIndex(int rank, int file) {
        return rank * 8 + file;
    }
    
    static constexpr int indexToRank(int index) {
        return index / 8;
    }
    
    static constexpr int indexToFile(int index) {
        return index % 8;
    }
    
public:
    // Конструкторы
    Bitboard();
    
    // Основные операции
    void clear();
    void setupStartPosition();
    
    // Получение информации о доске
    bool isEmpty(int square) const;
    bool isOccupied(int square) const;
    PieceType getPieceType(int square) const;
    Color getPieceColor(int square) const;
    Color getSideToMove() const { return side_to_move_; }
    
    // Установка и удаление фигур
    void setPiece(int square, PieceType piece, Color color);
    void removePiece(int square);
    PieceType movePiece(int from_square, int to_square);
    
    // Bitboard операции
    BitboardType getPieces(Color color, PieceType piece) const { return pieces_[color][piece]; }
    BitboardType getOccupancy(Color color) const { return occupancy_[color]; }
    BitboardType getAllPieces() const { return all_pieces_; }
    
    // Атаки и движения
    BitboardType getPawnAttacks(int square, Color color) const;
    BitboardType getKnightAttacks(int square) const;
    BitboardType getKingAttacks(int square) const;
    BitboardType getBishopAttacks(int square, BitboardType occupied = 0) const;
    BitboardType getRookAttacks(int square, BitboardType occupied = 0) const;
    BitboardType getQueenAttacks(int square, BitboardType occupied = 0) const;
    
    // Генерация всех легальных ходов
    std::vector<std::pair<int, int>> generateLegalMoves() const;
    
    // Проверка шаха
    bool isInCheck(Color color) const;
    
    // Magic bitboards для слонов и ладей (заглушка)
    static void initMagicBitboards();
    
    // Отладочные функции
    void printBoard() const;
    std::string toFen() const;
    
    // Операторы
    bool operator==(const Bitboard& other) const;
    bool operator!=(const Bitboard& other) const { return !(*this == other); }
};

// Вспомогательные функции
namespace BitboardUtils {
    // Битовые операции
    inline Bitboard::BitboardType setBit(Bitboard::BitboardType bb, int square) {
        return bb | (1ULL << square);
    }
    
    inline Bitboard::BitboardType clearBit(Bitboard::BitboardType bb, int square) {
        return bb & ~(1ULL << square);
    }
    
    inline bool getBit(Bitboard::BitboardType bb, int square) {
        return (bb >> square) & 1ULL;
    }
    
    inline int popCount(Bitboard::BitboardType bb) {
        return __builtin_popcountll(bb);
    }
    
    inline int lsb(Bitboard::BitboardType bb) {
        return __builtin_ctzll(bb);
    }
    
    // Направления для генерации атак
    extern const int KNIGHT_DELTAS[8];
    extern const int KING_DELTAS[8];
    extern const int BISHOP_DELTAS[4];
    extern const int ROOK_DELTAS[4];
    
    // Magic numbers (заглушки)
    extern Bitboard::BitboardType BISHOP_MAGICS[64];
    extern Bitboard::BitboardType ROOK_MAGICS[64];
}

#endif // BITBOARD_HPP