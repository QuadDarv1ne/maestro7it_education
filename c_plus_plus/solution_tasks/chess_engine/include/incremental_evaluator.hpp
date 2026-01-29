#ifndef INCREMENTAL_EVALUATOR_HPP
#define INCREMENTAL_EVALUATOR_HPP

#include "bitboard.hpp"
#include <array>

/**
 * @brief Инкрементальный оценщик позиции
 * 
 * Система оценки, которая отслеживает изменения в позиции и обновляет 
 * только те компоненты оценки, которые действительно изменились.
 * Обеспечивает 2-3x ускорение по сравнению с полным пересчетом.
 */
class IncrementalEvaluator {
private:
    const BitboardEngine& board_;
    
    // Кэшированные значения компонентов оценки
    int material_[2];        // Материал для каждого цвета
    int mobility_[2];        // Мобильность для каждого цвета
    int pawnStructure_[2];   // Пешечная структура
    int kingSafety_[2];      // Безопасность короля
    int centerControl_[2];   // Контроль центра
    
    // Флаги изменений
    bool materialChanged_;
    bool mobilityChanged_;
    bool pawnStructureChanged_;
    bool kingSafetyChanged_;
    bool centerControlChanged_;
    
    // Таблицы для быстрой оценки
    static const int PIECE_VALUES[6];
    static const int PSQT[6][64]; // Piece-Square Tables
    
public:
    IncrementalEvaluator(const BitboardEngine& board);
    
    // Основной интерфейс
    int evaluate();
    void updateAfterMove(int fromSquare, int toSquare, int pieceType, int color, int capturedPiece = -1);
    void fullRecalculation();
    
    // Геттеры для компонентов
    int getMaterialScore() const { return material_[0] - material_[1]; }
    int getMobilityScore() const { return mobility_[0] - mobility_[1]; }
    int getPawnStructureScore() const { return pawnStructure_[0] - pawnStructure_[1]; }
    int getKingSafetyScore() const { return kingSafety_[0] - kingSafety_[1]; }
    int getCenterControlScore() const { return centerControl_[0] - centerControl_[1]; }
    
private:
    // Инкрементальные обновления
    void updateMaterial(int pieceType, int color, int capturedPiece = -1);
    void updateMobility(int square, int pieceType, int color);
    void updatePawnStructure(int fromSquare, int toSquare, int color);
    void updateKingSafety(int kingSquare, int color);
    void updateCenterControl(int square, int pieceType, int color);
    
    // Вспомогательные функции
    int calculatePieceMobility(Bitboard attacks, Bitboard opponentPieces) const;
    int calculatePawnStructure(int color) const;
    int calculateKingSafety(int kingSquare, int color) const;
    int calculateCenterControl(int color) const;
    Bitboard getPieceAttacks(int square, int pieceType, int color) const;
};

// Константы для оценки
namespace EvaluationConstants {
    // Значения фигур в сантипешках
    extern const int PAWN_VALUE;
    extern const int KNIGHT_VALUE;
    extern const int BISHOP_VALUE;
    extern const int ROOK_VALUE;
    extern const int QUEEN_VALUE;
    extern const int KING_VALUE;
    
    // Бонусы и штрафы
    extern const int CENTER_BONUS;
    extern const int MOBILITY_BONUS;
    extern const int KING_SAFETY_BONUS;
    extern const int DOUBLED_PAWN_PENALTY;
    extern const int ISOLATED_PAWN_PENALTY;
    extern const int PASSED_PAWN_BONUS;
}

#endif // INCREMENTAL_EVALUATOR_HPP