#ifndef OPTIMIZED_MOVE_GENERATOR_HPP
#define OPTIMIZED_MOVE_GENERATOR_HPP

#include "board.hpp"
#include <vector>
#include <array>
#include <bitset>

/**
 * @brief Оптимизированный генератор ходов
 * 
 * Реализует высокопроизводительную генерацию легальных ходов
 * с использованием битбордов и оптимизированных алгоритмов.
 */
class OptimizedMoveGenerator {
private:
    const Board& board_;
    
    // Предвычисленные данные для ускорения
    mutable std::array<uint64_t, 64> knight_attacks_;
    mutable std::array<uint64_t, 64> king_attacks_;
    mutable std::array<std::array<uint64_t, 64>, 2> pawn_attacks_; // [color][square]
    
    // Кэширование для производительности
    mutable bool attack_tables_initialized_;
    mutable uint64_t occupancy_cache_;
    mutable std::array<uint64_t, 64> bishop_attacks_cache_;
    mutable std::array<uint64_t, 64> rook_attacks_cache_;
    
    // Инициализация таблиц атак
    void initializeAttackTables() const;
    void initializeKnightAttacks() const;
    void initializeKingAttacks() const;
    void initializePawnAttacks() const;
    
    // Оптимизированные функции генерации атак
    uint64_t getBishopAttacks(int square, uint64_t occupancy) const;
    uint64_t getRookAttacks(int square, uint64_t occupancy) const;
    uint64_t getQueenAttacks(int square, uint64_t occupancy) const;
    
    // Генерация ходов для конкретных фигур
    void generatePawnMoves(std::vector<Move>& moves, Color color) const;
    void generateKnightMoves(std::vector<Move>& moves, Color color) const;
    void generateBishopMoves(std::vector<Move>& moves, Color color) const;
    void generateRookMoves(std::vector<Move>& moves, Color color) const;
    void generateQueenMoves(std::vector<Move>& moves, Color color) const;
    void generateKingMoves(std::vector<Move>& moves, Color color) const;
    
    // Специализированные генераторы
    void generateCastlingMoves(std::vector<Move>& moves, Color color) const;
    void generateEnPassantMoves(std::vector<Move>& moves, Color color) const;
    void generatePromotionMoves(std::vector<Move>& moves, Color color) const;
    
    // Вспомогательные функции
    bool isSquareAttacked(int square, Color by_color) const;
    bool wouldBeInCheck(int from, int to, Color color) const;
    uint64_t getPiecesAttackingSquare(int square, Color attacker_color) const;
    
    // Оптимизированные проверки легальности
    bool isValidMove(const Move& move) const;
    bool isPseudoLegal(const Move& move) const;
    
public:
    explicit OptimizedMoveGenerator(const Board& board);
    
    // Основной интерфейс
    std::vector<Move> generateLegalMoves(Color color = Color::WHITE) const;
    std::vector<Move> generateCaptureMoves(Color color = Color::WHITE) const;
    std::vector<Move> generateQuietMoves(Color color = Color::WHITE) const;
    
    // Специализированные генераторы
    std::vector<Move> generateCheckMoves(Color color = Color::WHITE) const;
    std::vector<Move> generateTacticalMoves(Color color = Color::WHITE) const;
    std::vector<Move> generateEvasionMoves(Color color = Color::WHITE) const;
    
    // Быстрые проверки
    bool isInCheck(Color color) const;
    bool isCheckmate(Color color) const;
    bool isStalemate(Color color) const;
    bool hasLegalMoves(Color color) const;
    
    // Производительность
    size_t countLegalMoves(Color color = Color::WHITE) const;
    size_t countCaptureMoves(Color color = Color::WHITE) const;
    
    // Отладка и анализ
    void printMoveStatistics(Color color = Color::WHITE) const;
    std::string getMoveGenerationStats(Color color = Color::WHITE) const;
    
    // Настройки оптимизации
    void enableAggressivePruning(bool enable);
    void setDepthLimit(int max_depth);
};

// Константы для оптимизации
namespace MoveGenConstants {
    const int MAX_MOVES_PER_POSITION = 218;  // Максимум возможных ходов
    const int ATTACK_TABLE_SIZE = 64;        // Размер таблиц атак
    const uint64_t FULL_BOARD = 0xFFFFFFFFFFFFFFFFULL;
    
    // Направления для слайдеров
    const int BISHOP_DIRECTIONS[4] = { -9, -7, 7, 9 };
    const int ROOK_DIRECTIONS[4] = { -8, -1, 1, 8 };
    const int KING_DIRECTIONS[8] = { -9, -8, -7, -1, 1, 7, 8, 9 };
    
    // Бонусы для упорядочивания ходов
    const int CAPTURE_BONUS = 10000;
    const int PROMOTION_BONUS = 8000;
    const int CASTLING_BONUS = 6000;
    const int CHECK_BONUS = 4000;
}

#endif // OPTIMIZED_MOVE_GENERATOR_HPP