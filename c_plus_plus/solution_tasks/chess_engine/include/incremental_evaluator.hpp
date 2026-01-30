#ifndef INCREMENTAL_EVALUATOR_HPP
#define INCREMENTAL_EVALUATOR_HPP

#include "bitboard.hpp"
#include <array>

/**
 * @brief Инкрементальный оценщик позиции
 * 
 * Обновляет оценку позиции инкрементально при каждом ходе,
 * вместо полного пересчета всей позиции.
 */
class IncrementalEvaluator {
private:
    const Bitboard& board_;
    
    // Текущая оценка позиции
    int material_score_;
    int positional_score_;
    int mobility_score_;
    int pawn_structure_score_;
    int king_safety_score_;
    
    // Кэшированные значения для быстрого доступа
    std::array<int, 64> square_values_;
    std::array<int, 64> pawn_shield_bonus_;
    
    // Веса для разных компонентов оценки
    static const int MATERIAL_WEIGHTS[Bitboard::PIECE_TYPE_COUNT];
    static const int POSITIONAL_BONUSES[64];
    static const int MOBILITY_BONUSES[Bitboard::PIECE_TYPE_COUNT];
    
    // Инициализация таблиц значений
    void initializeSquareValues();
    void initializePawnShieldBonuses();
    
    // Расчет компонентов оценки
    int calculateMaterialScore() const;
    int calculatePositionalScore() const;
    int calculateMobilityScore() const;
    int calculatePawnStructureScore() const;
    int calculateKingSafetyScore() const;
    
    // Инкрементальные обновления
    void updateMaterialOnMove(int from_square, int to_square, 
                             Bitboard::PieceType captured_piece = Bitboard::PIECE_TYPE_COUNT);
    void updatePositionalOnMove(int from_square, int to_square);
    void updateMobilityOnMove(int square, Bitboard::PieceType piece_type);
    void updatePawnStructureOnMove(int from_square, int to_square);
    void updateKingSafetyOnMove(int square);
    
public:
    IncrementalEvaluator(const Bitboard& board);
    
    // Основной метод оценки
    int evaluate() const;
    
    // Инкрементальное обновление после хода
    void updateOnMove(int from_square, int to_square, 
                     Bitboard::PieceType captured_piece = Bitboard::PIECE_TYPE_COUNT);
    
    // Сброс и полный пересчет
    void reset();
    void fullRecalculate();
    
    // Получение компонентов оценки
    int getMaterialScore() const { return material_score_; }
    int getPositionalScore() const { return positional_score_; }
    int getMobilityScore() const { return mobility_score_; }
    int getPawnStructureScore() const { return pawn_structure_score_; }
    int getKingSafetyScore() const { return king_safety_score_; }
    
    // Отладочные методы
    void printEvaluationBreakdown() const;
    std::string getEvaluationDetails() const;
};

// Константы для оценки
namespace EvaluationConstants {
    // Материальные значения фигур (в сантипешках)
    const int PAWN_VALUE = 100;
    const int KNIGHT_VALUE = 320;
    const int BISHOP_VALUE = 330;
    const int ROOK_VALUE = 500;
    const int QUEEN_VALUE = 900;
    const int KING_VALUE = 20000; // Очень большое значение для короля
    
    // Позиционные бонусы
    const int CENTER_BONUS = 10;
    const int DEVELOPMENT_BONUS = 5;
    const int KING_SAFETY_BONUS = 15;
    
    // Мобильность
    const int MOBILITY_BONUS_PER_MOVE = 2;
    
    // Структура пешек
    const int DOUBLED_PAWN_PENALTY = -15;
    const int ISOLATED_PAWN_PENALTY = -20;
    const int PASSED_PAWN_BONUS = 25;
    
    // Безопасность короля
    const int KING_SHIELD_BONUS = 10;
    const int KING_EXPOSURE_PENALTY = -30;
}

#endif // INCREMENTAL_EVALUATOR_HPP