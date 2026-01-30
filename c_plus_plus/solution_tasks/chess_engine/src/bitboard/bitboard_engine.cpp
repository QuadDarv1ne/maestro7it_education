#include "../include/bitboard.hpp"
#include <iostream>
#include <cstring>

// Определение констант bitboard
namespace Bitboards {
    const Bitboard FILE_A = 0x0101010101010101ULL;
    const Bitboard FILE_H = 0x8080808080808080ULL;
    const Bitboard RANK_1 = 0x00000000000000FFULL;
    const Bitboard RANK_8 = 0xFF00000000000000ULL;
    const Bitboard CENTER_SQUARES = 0x0000001818000000ULL;
    const Bitboard LIGHT_SQUARES = 0x55AA55AA55AA55AAULL;
    const Bitboard DARK_SQUARES = 0xAA55AA55AA55AA55ULL;
    
    // Предварительно вычисленные маски атак
    Bitboard KNIGHT_ATTACKS[64];
    Bitboard KING_ATTACKS[64];
    Bitboard PAWN_ATTACKS[2][64];
    
    // Инициализация масок атак
    void initAttackTables() {
        // Атаки коня
        for (int sq = 0; sq < 64; sq++) {
            Bitboard attacks = 0;
            int rank = sq / 8;
            int file = sq % 8;
            
            int knightMoves[8][2] = {
                {-2, -1}, {-2, 1}, {-1, -2}, {-1, 2},
                {1, -2}, {1, 2}, {2, -1}, {2, 1}
            };
            
            for (int i = 0; i < 8; i++) {
                int newRank = rank + knightMoves[i][0];
                int newFile = file + knightMoves[i][1];
                if (newRank >= 0 && newRank < 8 && newFile >= 0 && newFile < 8) {
                    attacks |= (1ULL << (newRank * 8 + newFile));
                }
            }
            KNIGHT_ATTACKS[sq] = attacks;
        }
        
        // Атаки короля
        for (int sq = 0; sq < 64; sq++) {
            Bitboard attacks = 0;
            int rank = sq / 8;
            int file = sq % 8;
            
            for (int dr = -1; dr <= 1; dr++) {
                for (int df = -1; df <= 1; df++) {
                    if (dr == 0 && df == 0) continue;
                    int newRank = rank + dr;
                    int newFile = file + df;
                    if (newRank >= 0 && newRank < 8 && newFile >= 0 && newFile < 8) {
                        attacks |= (1ULL << (newRank * 8 + newFile));
                    }
                }
            }
            KING_ATTACKS[sq] = attacks;
        }
        
        // Атаки пешек
        for (int color = 0; color < 2; color++) {
            for (int sq = 0; sq < 64; sq++) {
                Bitboard attacks = 0;
                int rank = sq / 8;
                int file = sq % 8;
                
                int direction = (color == 0) ? 1 : -1; // 0 - white, 1 - black
                
                if (file > 0) {
                    int newRank = rank + direction;
                    int newFile = file - 1;
                    if (newRank >= 0 && newRank < 8) {
                        attacks |= (1ULL << (newRank * 8 + newFile));
                    }
                }
                
                if (file < 7) {
                    int newRank = rank + direction;
                    int newFile = file + 1;
                    if (newRank >= 0 && newRank < 8) {
                        attacks |= (1ULL << (newRank * 8 + newFile));
                    }
                }
                PAWN_ATTACKS[color][sq] = attacks;
            }
        }
    }
    
    // Глобальная инициализация при первом использовании
    bool isInitialized = false;
    void initialize() {
        if (!isInitialized) {
            initAttackTables();
            isInitialized = true;
        }
    }
}

BitboardEngine::BitboardEngine() {
    Bitboards::initialize();
    clear();
}

void BitboardEngine::clear() {
    // Очистка всех bitboards
    memset(pieces, 0, sizeof(pieces));
    memset(allPieces, 0, sizeof(allPieces));
    occupancy = 0;
    sideToMove = 0;
    enPassantSquare = INVALID_SQUARE;
    
    // Сброс прав рокировки
    castlingRights[0][0] = castlingRights[0][1] = true; // white king/queen side
    castlingRights[1][0] = castlingRights[1][1] = true; // black king/queen side
}

void BitboardEngine::setupStartPosition() {
    clear();
    
    // Расстановка фигур для начальной позиции
    // Белые фигуры
    setPiece(A1, 3, 0); setPiece(B1, 4, 0); setPiece(C1, 2, 0); setPiece(D1, 1, 0);
    setPiece(E1, 0, 0); setPiece(F1, 2, 0); setPiece(G1, 4, 0); setPiece(H1, 3, 0);
    for (int i = 0; i < 8; i++) setPiece(i + 8, 5, 0); // Белые пешки
    
    // Черные фигуры
    setPiece(A8, 3, 1); setPiece(B8, 4, 1); setPiece(C8, 2, 1); setPiece(D8, 1, 1);
    setPiece(E8, 0, 1); setPiece(F8, 2, 1); setPiece(G8, 4, 1); setPiece(H8, 3, 1);
    for (int i = 0; i < 8; i++) setPiece(i + 48, 5, 1); // Черные пешки
    
    sideToMove = 0; // Белые начинают
}

void BitboardEngine::setPiece(int square, int pieceType, int color) {
    if (square < 0 || square >= 64) return;
    
    // Удаляем фигуру с этой клетки, если она там была
    removePiece(square);
    
    // Добавляем новую фигуру
    Bitboard mask = 1ULL << square;
    pieces[color][pieceType] |= mask;
    allPieces[color] |= mask;
    occupancy |= mask;
}

void BitboardEngine::removePiece(int square) {
    if (square < 0 || square >= 64) return;
    
    Bitboard mask = ~(1ULL << square);
    
    // Удаляем из всех bitboards
    for (int color = 0; color < 2; color++) {
        for (int piece = 0; piece < 6; piece++) {
            pieces[color][piece] &= mask;
        }
        allPieces[color] &= mask;
    }
    occupancy &= mask;
}

int BitboardEngine::getPieceType(int square) const {
    if (square < 0 || square >= 64) return -1;
    
    Bitboard mask = 1ULL << square;
    
    for (int piece = 0; piece < 6; piece++) {
        if (pieces[0][piece] & mask) return piece;
        if (pieces[1][piece] & mask) return piece;
    }
    return -1; // Пустая клетка
}

int BitboardEngine::getPieceColor(int square) const {
    if (square < 0 || square >= 64) return -1;
    
    Bitboard mask = 1ULL << square;
    
    if (allPieces[0] & mask) return 0; // Белые
    if (allPieces[1] & mask) return 1; // Черные
    return -1; // Пустая клетка
}

bool BitboardEngine::isEmpty(int square) const {
    if (square < 0 || square >= 64) return true;
    return !(occupancy & (1ULL << square));
}

Bitboard BitboardEngine::generatePawnAttacks(int square, int color) const {
    if (square < 0 || square >= 64) return 0;
    return Bitboards::PAWN_ATTACKS[color][square];
}

Bitboard BitboardEngine::generateKnightAttacks(int square) const {
    if (square < 0 || square >= 64) return 0;
    return Bitboards::KNIGHT_ATTACKS[square];
}

Bitboard BitboardEngine::generateKingAttacks(int square) const {
    if (square < 0 || square >= 64) return 0;
    return Bitboards::KING_ATTACKS[square];
}

Bitboard BitboardEngine::generateSlidingAttacks(int square, Bitboard occupied, Bitboard mask) const {
    Bitboard attacks = 0;
    Bitboard squareBB = 1ULL << square;
    
    // Для ладьи (горизонтали и вертикали)
    // Для слона (диагонали)
    // Здесь упрощенная реализация
    
    // Север
    Bitboard ray = squareBB;
    while (ray) {
        ray <<= 8;
        if (ray & mask) attacks |= ray;
        if (ray & occupied) break;
        if (ray & Bitboards::RANK_8) break;
    }
    
    // Юг
    ray = squareBB;
    while (ray) {
        ray >>= 8;
        if (ray & mask) attacks |= ray;
        if (ray & occupied) break;
        if (ray & Bitboards::RANK_1) break;
    }
    
    // Восток
    ray = squareBB;
    while (ray && !(ray & Bitboards::FILE_H)) {
        ray <<= 1;
        if (ray & mask) attacks |= ray;
        if (ray & occupied) break;
    }
    
    // Запад
    ray = squareBB;
    while (ray && !(ray & Bitboards::FILE_A)) {
        ray >>= 1;
        if (ray & mask) attacks |= ray;
        if (ray & occupied) break;
    }
    
    return attacks;
}

void BitboardEngine::updateOccupancy() {
    occupancy = allPieces[0] | allPieces[1];
}

// Статические утилиты bitboard
Bitboard BitboardEngine::squareToBitboard(int square) {
    return (square >= 0 && square < 64) ? (1ULL << square) : 0;
}

int BitboardEngine::bitboardToSquare(Bitboard bb) {
    if (bb == 0) return INVALID_SQUARE;
    return __builtin_ctzll(bb); // Подсчет замыкающих нулей
}

int BitboardEngine::popcount(Bitboard bb) {
    return __builtin_popcountll(bb); // Подсчет количества единиц
}

int BitboardEngine::lsb(Bitboard bb) {
    return bb ? __builtin_ctzll(bb) : INVALID_SQUARE;
}

int BitboardEngine::msb(Bitboard bb) {
    return bb ? (63 - __builtin_clzll(bb)) : INVALID_SQUARE;
}

void BitboardEngine::printBitboard(Bitboard bb) const {
    std::cout << "  a b c d e f g h" << std::endl;
    for (int rank = 7; rank >= 0; rank--) {
        std::cout << (rank + 1) << " ";
        for (int file = 0; file < 8; file++) {
            int square = rank * 8 + file;
            if (bb & (1ULL << square)) {
                std::cout << "1 ";
            } else {
                std::cout << ". ";
            }
        }
        std::cout << (rank + 1) << std::endl;
    }
    std::cout << "  a b c d e f g h" << std::endl;
    std::cout << "Bitboard value: 0x" << std::hex << bb << std::dec << std::endl;
}

void BitboardEngine::printBoard() const {
    std::cout << "  a b c d e f g h" << std::endl;
    for (int rank = 7; rank >= 0; rank--) {
        std::cout << (rank + 1) << " ";
        for (int file = 0; file < 8; file++) {
            int square = rank * 8 + file;
            int pieceType = getPieceType(square);
            int color = getPieceColor(square);
            
            if (pieceType == -1) {
                std::cout << ". ";
            } else {
                char pieceChars[] = {'K', 'Q', 'B', 'R', 'N', 'P'};
                char piece = pieceChars[pieceType];
                if (color == 1) piece = piece + 32; // lowercase for black
                std::cout << piece << " ";
            }
        }
        std::cout << (rank + 1) << std::endl;
    }
    std::cout << "  a b c d e f g h" << std::endl;
    std::cout << "Side to move: " << (sideToMove == 0 ? "White" : "Black") << std::endl;
}