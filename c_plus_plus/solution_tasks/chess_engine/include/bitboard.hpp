#ifndef BITBOARD_HPP
#define BITBOARD_HPP

#include <cstdint>
#include <array>
#include <iostream>

// Тип для bitboard - 64-битное целое
typedef uint64_t Bitboard;

// Константы для квадратов доски
enum Square : int {
    A1, B1, C1, D1, E1, F1, G1, H1,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A8, B8, C8, D8, E8, F8, G8, H8,
    INVALID_SQUARE = 64
};

// Направления для генерации ходов
enum Direction : int {
    NORTH = 8, SOUTH = -8, EAST = 1, WEST = -1,
    NORTH_EAST = 9, NORTH_WEST = 7, SOUTH_EAST = -7, SOUTH_WEST = -9
};

class BitboardEngine {
private:
    // Bitboards для каждой фигуры и цвета
    Bitboard pieces[2][6]; // [color][piece_type]
    
    // Объединенные bitboards
    Bitboard allPieces[2]; // [color] - все фигуры каждого цвета
    Bitboard occupancy;    // все занятые клетки
    
    // Текущий игрок
    int sideToMove;
    
    // Права рокировки
    bool castlingRights[2][2]; // [color][side] - [white/black][king/queen side]
    
    // Клетка для взятия на проходе
    int enPassantSquare;
    
public:
    BitboardEngine();
    
    // Базовые операции с bitboards
    void clear();
    void setupStartPosition();
    
    // Манипуляции с фигурами
    void setPiece(int square, int pieceType, int color);
    void removePiece(int square);
    int getPieceType(int square) const;
    int getPieceColor(int square) const;
    bool isEmpty(int square) const;
    
    // Генерация ходов
    Bitboard generatePawnAttacks(int square, int color) const;
    Bitboard generateKnightAttacks(int square) const;
    Bitboard generateKingAttacks(int square) const;
    Bitboard generateSlidingAttacks(int square, Bitboard occupied, Bitboard mask) const;
    
    // Утилиты bitboard
    static Bitboard squareToBitboard(int square);
    static int bitboardToSquare(Bitboard bb);
    static int popcount(Bitboard bb);
    static int lsb(Bitboard bb); // least significant bit
    static int msb(Bitboard bb); // most significant bit
    
    // Отладка
    void printBitboard(Bitboard bb) const;
    void printBoard() const;
    
    // Геттеры
    int getSideToMove() const { return sideToMove; }
    void setSideToMove(int color) { sideToMove = color; }
    Bitboard getOccupancy() const { return occupancy; }
    Bitboard getColorOccupancy(int color) const { return allPieces[color]; }
    
private:
    // Вспомогательные функции
    void updateOccupancy();
    Bitboard getRookAttacks(int square, Bitboard occupied) const;
    Bitboard getBishopAttacks(int square, Bitboard occupied) const;
};

// Константы bitboard
namespace Bitboards {
    extern const Bitboard FILE_A;
    extern const Bitboard FILE_H;
    extern const Bitboard RANK_1;
    extern const Bitboard RANK_8;
    extern const Bitboard CENTER_SQUARES;
    extern const Bitboard LIGHT_SQUARES;
    extern const Bitboard DARK_SQUARES;
    
    // Маски для генерации атак
    extern const Bitboard KNIGHT_ATTACKS[64];
    extern const Bitboard KING_ATTACKS[64];
    extern const Bitboard PAWN_ATTACKS[2][64]; // [color][square]
}

#endif // BITBOARD_HPP