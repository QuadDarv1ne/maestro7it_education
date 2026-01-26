#ifndef MINIMAX_HPP
#define MINIMAX_HPP

#include "board.hpp"
#include "move_generator.hpp"
#include "position_evaluator.hpp"
#include <limits>
#include <chrono>

/**
 * @brief Класс, реализующий алгоритм минимакс с альфа-бета отсечением
 * 
 * Использует алгоритм минимакс с альфа-бета отсечением для поиска оптимальных ходов в шахматах,
 * с поддержкой ограничения по времени и улучшенным упорядочиванием ходов
 */
class Minimax {
private:
    Board& board_;                    ///< Ссылка на текущую игровую доску
    PositionEvaluator evaluator_;     ///< Оценщик позиции
    int maxDepth_;                    ///< Максимальная глубина поиска
    std::chrono::milliseconds timeLimit_;  ///< Ограничение времени на поиск
    
public:
    Minimax(Board& board, int maxDepth = 4);
    
    // Основные методы поиска
    Move findBestMove(Color color);                                                    ///< Находит лучший ход для указанного цвета
    Move findBestMoveWithTimeLimit(Color color, std::chrono::milliseconds timeLimit);  ///< Находит лучший ход с ограничением времени
    
    // Поиск с альфа-бета отсечением
    int minimax(int depth, int alpha, int beta, Color maximizingPlayer);  ///< Алгоритм минимакс с альфа-бета отсечением
    int minimaxWithTimeLimit(int depth, int alpha, int beta, Color maximizingPlayer, 
                            std::chrono::steady_clock::time_start startTime);  ///< Минимакс с контролем времени
    
    // Настройки
    void setMaxDepth(int depth);                         ///< Устанавливает максимальную глубину поиска
    void setTimeLimit(std::chrono::milliseconds limit);  ///< Устанавливает ограничение времени
    int getMaxDepth() const;                             ///< Возвращает текущую максимальную глубину поиска
    
    // Упорядочивание ходов для лучшего отсечения
    std::vector<Move> orderMoves(const std::vector<Move>& moves) const;  ///< Упорядочивает ходы для повышения эффективности отсечения
    
private:
    // Вспомогательные методы
    int evaluatePosition() const;                                          ///< Оценивает текущую позицию на доске
    bool isTimeUp(std::chrono::steady_clock::time_start startTime) const;  ///< Проверяет, истекло ли отведенное время
    int quiescenceSearch(int alpha, int beta, int depth);                  ///< Выполняет поиск в "тихих" позициях для избежания горизонтального эффекта
};

// Константы для поиска
const int INF = std::numeric_limits<int>::max();  ///< Значение бесконечности для алгоритма
const int MATE_SCORE = 100000;                    ///< Оценка мата
const int MAX_QUIESCENCE_DEPTH = 4;               ///< Максимальная глубина для поиска в "тихих" позициях

#endif // MINIMAX_HPP