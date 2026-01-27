#ifndef MINIMAX_HPP
#define MINIMAX_HPP

#include "board.hpp"
#include "move_generator.hpp"
#include "position_evaluator.hpp"
#include <limits>
#include <chrono>
#include <unordered_map>
#include <cstdint>
#include <vector>

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
    
    // Transposition table for caching evaluations
    struct TTEntry {
        uint64_t hash;
        int depth;
        int score;
        Move bestMove;
        char flag; // 'EXACT', 'LOWER', 'UPPER'
        
        TTEntry() : hash(0), depth(0), score(0), flag(0) {}
        TTEntry(uint64_t h, int d, int s, Move bm, char f) : hash(h), depth(d), score(s), bestMove(bm), flag(f) {}
    };
    
    static const size_t HASH_TABLE_SIZE = 100000;  // Size of the hash table
    std::vector<TTEntry> transpositionTable;
    
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
    
    // Методы для оптимизации
    uint64_t hashPosition() const;                                         ///< Генерирует хеш позиции для транспозиционной таблицы
    void storeInTT(uint64_t hash, int depth, int score, Move bestMove, char flag);  ///< Сохраняет в транспозиционную таблицу
    TTEntry* probeTT(uint64_t hash);                                       ///< Ищет запись в транспозиционной таблице
    int minimaxWithTT(int depth, int alpha, int beta, Color maximizingPlayer);     ///< Минимакс с использованием транспозиционной таблицы
    int getMovePriority(const Move& move) const;                           ///< Определяет приоритет хода для упорядочивания
    bool isInCheck(Color color) const;                                     ///< Проверяет, находится ли король под шахом
};

// Константы для поиска
const int INF = std::numeric_limits<int>::max();  ///< Значение бесконечности для алгоритма
const int MATE_SCORE = 100000;                    ///< Оценка мата
const int MAX_QUIESCENCE_DEPTH = 4;               ///< Максимальная глубина для поиска в "тихих" позициях

#endif // MINIMAX_HPP