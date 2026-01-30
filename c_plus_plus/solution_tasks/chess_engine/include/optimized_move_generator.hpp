#ifndef OPTIMIZED_MOVE_GENERATOR_HPP
#define OPTIMIZED_MOVE_GENERATOR_HPP

#include "bitboard.hpp"
#include <vector>
#include <array>

/**
 * @brief Оптимизированный генератор ходов с использованием bitboard
 * 
 * Реализует высокопроизводительную генерацию ходов с использованием
 * bitboard представления и magic bitboards для слайдеров.
 */
class OptimizedMoveGenerator {
public:
    // Тип для хода: упакованный from(6 бит) | to(6 бит) | флаги(4 бита)
    using MoveType = uint16_t;
    
    // Флаги ходов
    static const MoveType CAPTURE_FLAG = 1 << 12;
    static const MoveType PROMOTION_FLAG = 1 << 13;
    static const MoveType CASTLING_FLAG = 1 << 14;
    static const MoveType EN_PASSANT_FLAG = 1 << 15;
    
private:
    const Bitboard& board_;
    
    // Magic bitboards для быстрых вычислений атак
    static std::array<Bitboard::BitboardType, 64> bishop_magics_;
    static std::array<Bitboard::BitboardType, 64> rook_magics_;
    static std::array<Bitboard::BitboardType, 64> bishop_masks_;
    static std::array<Bitboard::BitboardType, 64> rook_masks_;
    
    // Таблицы атак (заглушки)
    static std::array<std::array<Bitboard::BitboardType, 512>, 64> bishop_attacks_;
    static std::array<std::array<Bitboard::BitboardType, 4096>, 64> rook_attacks_;
    
    // Предвычисленные таблицы для пешек
    static std::array<Bitboard::BitboardType, 64> pawn_attacks_white_;
    static std::array<Bitboard::BitboardType, 64> pawn_attacks_black_;
    static std::array<Bitboard::BitboardType, 64> pawn_pushes_white_;
    static std::array<Bitboard::BitboardType, 64> pawn_pushes_black_;
    
    // Инициализация таблиц
    static void initializeTables();
    static void initializePawnTables();
    static void initializeMagicBitboards();
    
    // Вспомогательные функции
    static constexpr int packMove(int from, int to, MoveType flags = 0) {
        return (from & 0x3F) | ((to & 0x3F) << 6) | (flags & 0xF000);
    }
    
    static constexpr int unpackFrom(MoveType move) {
        return move & 0x3F;
    }
    
    static constexpr int unpackTo(MoveType move) {
        return (move >> 6) & 0x3F;
    }
    
    static constexpr MoveType unpackFlags(MoveType move) {
        return move & 0xF000;
    }
    
public:
    OptimizedMoveGenerator(const Bitboard& board);
    
    // Основные методы генерации ходов
    std::vector<MoveType> generateLegalMoves() const;
    std::vector<MoveType> generatePseudoLegalMoves() const;
    
    // Специализированные генераторы для фигур
    std::vector<MoveType> generatePawnMoves(Bitboard::Color color) const;
    std::vector<MoveType> generateKnightMoves(Bitboard::Color color) const;
    std::vector<MoveType> generateBishopMoves(Bitboard::Color color) const;
    std::vector<MoveType> generateRookMoves(Bitboard::Color color) const;
    std::vector<MoveType> generateQueenMoves(Bitboard::Color color) const;
    std::vector<MoveType> generateKingMoves(Bitboard::Color color) const;
    
    // Специальные ходы
    std::vector<MoveType> generateCastlingMoves(Bitboard::Color color) const;
    std::vector<MoveType> generateEnPassantMoves(Bitboard::Color color) const;
    std::vector<MoveType> generatePromotionMoves(Bitboard::Color color) const;
    
    // Проверки легальности
    bool isLegalMove(MoveType move) const;
    bool wouldLeaveKingInCheck(MoveType move) const;
    bool isSquareAttacked(int square, Bitboard::Color by_color) const;
    
    // Атаки фигур (используют magic bitboards)
    static Bitboard::BitboardType getBishopAttacks(int square, Bitboard::BitboardType occupied);
    static Bitboard::BitboardType getRookAttacks(int square, Bitboard::BitboardType occupied);
    static Bitboard::BitboardType getQueenAttacks(int square, Bitboard::BitboardType occupied);
    static Bitboard::BitboardType getKnightAttacks(int square);
    static Bitboard::BitboardType getKingAttacks(int square);
    static Bitboard::BitboardType getPawnAttacks(int square, Bitboard::Color color);
    
    // Утилиты
    static void init();
    static std::string moveToAlgebraic(MoveType move);
    static MoveType algebraicToMove(const std::string& alg);
    
private:
    // Внутренние вспомогательные методы
    std::vector<MoveType> addSlidingMoves(int square, Bitboard::BitboardType attacks, 
                                         Bitboard::BitboardType own_pieces, 
                                         Bitboard::BitboardType enemy_pieces) const;
    
    std::vector<MoveType> addNonSlidingMoves(int square, Bitboard::BitboardType attacks,
                                            Bitboard::BitboardType own_pieces,
                                            Bitboard::BitboardType enemy_pieces) const;
    
    bool isValidSquare(int square) const;
};

// Глобальная инициализация
namespace MoveGenInit {
    void initialize();
    bool isInitialized();
}

#endif // OPTIMIZED_MOVE_GENERATOR_HPP