#ifndef MINIMAX_HPP
#define MINIMAX_HPP

#include "board.hpp"
#include "move_generator.hpp"
#include "position_evaluator.hpp"
#include "opening_book.hpp"
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
    OpeningBook openingBook_;         ///< Книга дебютов
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
    
    // Killer moves for move ordering
    static const int MAX_KILLER_MOVES = 2;
    static const int MAX_PLY = 100;
    std::vector<std::vector<Move>> killerMoves;
    
    // History heuristic for move ordering
    static const int HISTORY_SIZE = 64 * 64; // From-To square combinations
    std::vector<int> historyTable;
    
public:
    Minimax(Board& board, int maxDepth = 4);
    
    // Основные методы поиска
    Move findBestMove(Color color);                                                    ///< Находит лучший ход для указанного цвета
    Move findBestMoveWithTimeLimit(Color color, std::chrono::milliseconds timeLimit);  ///< Находит лучший ход с ограничением времени
    
    // Поиск с альфа-бета отсечением
    int minimax(int depth, int alpha, int beta, Color maximizingPlayer);  ///< Алгоритм минимакс с альфа-бета отсечением
    int minimaxWithTimeLimit(int depth, int alpha, int beta, Color maximizingPlayer, 
                            std::chrono::steady_clock::time_point startTime);  ///< Минимакс с контролем времени
    
    // Настройки
    void setMaxDepth(int depth);                         ///< Устанавливает максимальную глубину поиска
    void setTimeLimit(std::chrono::milliseconds limit);  ///< Устанавливает ограничение времени
    int getMaxDepth() const;                             ///< Возвращает текущую максимальную глубину поиска
    
    // Упорядочивание ходов для лучшего отсечения
    std::vector<Move> orderMoves(const std::vector<Move>& moves) const;  ///< Упорядочивает ходы для повышения эффективности отсечения
    
private:
    // Вспомогательные методы
    int evaluatePosition() const;                                          ///< Оценивает текущую позицию на доске
    bool isTimeUp(std::chrono::steady_clock::time_point startTime) const;  ///< Проверяет, истекло ли отведенное время
    int quiescenceSearch(int alpha, int beta, int depth);                  ///< Выполняет поиск в "тихих" позициях для избежания горизонтального эффекта
    
    // Методы для оптимизации
    uint64_t hashPosition() const;                                         ///< Генерирует хеш позиции для транспозиционной таблицы
    void storeInTT(uint64_t hash, int depth, int score, Move bestMove, char flag);  ///< Сохраняет в транспозиционную таблицу
    TTEntry* probeTT(uint64_t hash);                                       ///< Ищет запись в транспозиционной таблице
    int minimaxWithTT(int depth, int alpha, int beta, Color maximizingPlayer);     ///< Минимакс с использованием транспозиционной таблицы
    int getMovePriority(const Move& move, int ply = 0) const;              ///< Определяет приоритет хода для упорядочивания
    bool isInCheck(Color color) const;                                     ///< Проверяет, находится ли король под шахом
    void addKillerMove(const Move& move, int ply);                         ///< Добавляет killer move
    bool isKillerMove(const Move& move, int ply) const;                    ///< Проверяет, является ли ход killer move
    int aspirationSearch(int depth, int previousScore, Color maximizingPlayer); ///< Поиск с aspiration windows
    void updateHistory(const Move& move, int depth);                           ///< Обновляет историю ходов
    int getHistoryScore(const Move& move) const;                               ///< Возвращает счет истории для хода
    bool isFutile(int depth, int alpha, int staticEval) const;                 ///< Проверяет, стоит ли применять futility pruning
    bool isRazoringApplicable(int depth, int beta, int staticEval) const;      ///< Проверяет, применимо ли razoring
    int multiCutPruning(int depth, int alpha, int beta, Color maximizingPlayer, int cutNumber = 1); ///< Multi-cut pruning
    int quiescenceSearch(int alpha, int beta, Color maximizingPlayer, int ply = 0);               ///< Улучшенный квизенс-поиск
    std::vector<Move> orderCaptures(const std::vector<Move>& captures) const;                     ///< Упорядочивание взятий для квизенса
    int principalVariationSearch(int depth, int alpha, int beta, Color maximizingPlayer, bool isPVNode = true); ///< Principal Variation Search
    int calculateExtension(const Move& move, Color maximizingPlayer, int depth) const;                          ///< Рассчитывает расширение для хода
    bool isCriticalPosition() const;                                                                            ///< Проверяет, является ли позиция критической
    bool probCut(int depth, int beta, Color maximizingPlayer, int threshold = 100);                            ///< ProbCut pruning technique
};

// Константы для поиска
const int INF = std::numeric_limits<int>::max();  ///< Значение бесконечности для алгоритма
const int MATE_SCORE = 100000;                    ///< Оценка мата
const int MAX_QUIESCENCE_DEPTH = 4;               ///< Максимальная глубина для поиска в "тихих" позициях

#endif // MINIMAX_HPP