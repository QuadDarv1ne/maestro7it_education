#ifndef POSITION_EVALUATOR_HPP
#define POSITION_EVALUATOR_HPP

#include "board.hpp"
#include "move_generator.hpp"
#include <map>

/**
 * @brief Класс, реализующий оценку позиции в шахматах
 * 
 * Оценивает текущую позицию на доске, учитывая материальный баланс,
 * позиционное расположение фигур, мобильность, безопасность короля
 * и структуру пешек
 */
class PositionEvaluator {
private:
    const Board& board_;  ///< Ссылка на текущую игровую доску
    
    // Таблицы позиционной оценки для каждой фигуры
    static const int pawnTable[64];                ///< Таблица оценки пешек
    static const int knightTable[64];              ///< Таблица оценки коней
    static const int bishopTable[64];              ///< Таблица оценки слонов
    static const int rookTable[64];                ///< Таблица оценки ладей
    static const int queenTable[64];               ///< Таблица оценки ферзей
    static const int kingMiddleGameTable[64];      ///< Таблица оценки короля в миттельшпиле
    static const int kingEndGameTable[64];         ///< Таблица оценки короля в эндшпиле
    
public:
    PositionEvaluator(const Board& board);
    
    // Основная функция оценки
    int evaluate() const;  ///< Основная функция оценки позиции
    
    // Компоненты оценки
    int materialEvaluation() const;      ///< Оценка материального баланса
    int positionalEvaluation() const;    ///< Оценка позиционного расположения фигур
    int mobilityEvaluation() const;      ///< Оценка мобильности фигур
    int kingSafetyEvaluation() const;    ///< Оценка безопасности короля
    int pawnStructureEvaluation() const; ///< Оценка структуры пешек
    
    // Определение фазы игры
    bool isEndGame() const;  ///< Проверяет, является ли позиция эндшпилем
    int getGamePhase() const;  ///< Определяет фазу игры (начало, миттельшпиль, эндшпиль)
    
    // Оценка конкретных фигур
    int evaluatePiece(PieceType type, Square square, Color color) const;  ///< Оценивает конкретную фигуру
    int getPSTValue(PieceType type, Square square, Color color) const;    ///< Получает значение из таблицы позиционной оценки
    
private:
    // Вспомогательные методы
    int getPieceMobility(Square square) const;  ///< Рассчитывает мобильность фигуры на заданной клетке
    int getKingSafety(Color color) const;       ///< Оценивает безопасность короля заданного цвета
    int getPawnStructure(Color color) const;    ///< Анализирует структуру пешек заданного цвета
    bool isPassedPawn(Square square) const;     ///< Проверяет, является ли пешка проходной
    bool isIsolatedPawn(Square square) const;   ///< Проверяет, является ли пешка изолированной
    int flipSquare(Square square) const;        ///< Переворачивает квадрат для черных фигур
    
    // Новые вспомогательные методы
    int evaluateKingSafety(Square kingSquare, Color color) const;  ///< Оценивает безопасность короля
    int evaluatePawnStructure(Color color) const;                  ///< Оценивает структуру пешек
    int countDefenders(Square square, Color color) const;          ///< Подсчитывает защитников
    int countAttackers(Square square, Color color) const;          ///< Подсчитывает атакующих
    int getDistanceToCenter(Square square) const;                  ///< Расстояние до центра
    bool isConnectedPawn(Square square) const;                     ///< Проверяет связанные пешки
    bool isProtectedPawn(Square square) const;                     ///< Проверяет защищенные пешки
};

#endif // POSITION_EVALUATOR_HPP