#ifndef PARALLEL_SEARCH_HPP
#define PARALLEL_SEARCH_HPP

#include "bitboard.hpp"
#include "incremental_evaluator.hpp"
#include <thread>
#include <mutex>
#include <atomic>
#include <condition_variable>
#include <vector>
#include <future>

/**
 * @brief Многопоточный шахматный движок
 * 
 * Реализует параллельный поиск с использованием нескольких потоков CPU.
 * Обеспечивает 2-4x ускорение на многоядерных системах за счет Lazy SMP подхода.
 */
class ParallelChessEngine {
private:
    // Основные компоненты
    BitboardEngine board_;
    IncrementalEvaluator evaluator_;
    
    // Настройки поиска
    int maxDepth_;
    int numThreads_;
    std::chrono::milliseconds timeLimit_;
    
    // Потокобезопасные данные для совместного использования
    mutable std::mutex sharedMutex_;
    std::condition_variable searchFinished_;
    
    // Разделяемые данные между потоками
    std::atomic<bool> stopSearch_;
    std::atomic<int> bestScore_;
    std::atomic<Move> bestMove_;
    std::atomic<int> searchDepth_;
    
    // Транспозиционная таблица (совместно используемая)
    static const size_t TRANSPOSITION_TABLE_SIZE = 1000000;
    std::vector<TranspositionEntry> transpositionTable_;
    
    // История ходов для упорядочивания
    static const int HISTORY_SIZE = 64 * 64;
    std::vector<int> historyTable_;
    
public:
    ParallelChessEngine(int numThreads = 4);
    ~ParallelChessEngine();
    
    // Основной интерфейс
    Move findBestMove(Color color, std::chrono::milliseconds timeLimit = std::chrono::milliseconds(10000));
    void setMaxDepth(int depth);
    void setNumThreads(int threads);
    void setTimeLimit(std::chrono::milliseconds limit);
    
    // Получение информации
    int getNodesSearched() const;
    int getSearchDepth() const { return searchDepth_.load(); }
    int getNumThreads() const { return numThreads_; }
    
private:
    // Рабочие функции потоков
    void workerThread(int threadId, Color color);
    int parallelMinimax(int depth, int alpha, int beta, Color maximizingPlayer, int threadId);
    
    // Синхронизация и координация
    void startSearch(Color color);
    void stopAllThreads();
    bool shouldStop() const { return stopSearch_.load(); }
    
    // Улучшенные алгоритмы поиска
    int principalVariationSearch(int depth, int alpha, int beta, Color maximizingPlayer, int threadId, bool isPVNode = true);
    int quiescenceSearch(int alpha, int beta, Color maximizingPlayer, int ply, int threadId);
    
    // Упорядочивание ходов
    std::vector<Move> orderMoves(const std::vector<Move>& moves, int ply) const;
    int getMovePriority(const Move& move, int ply) const;
    
    // Транспозиционная таблица
    struct TranspositionEntry {
        uint64_t hash;
        int depth;
        int score;
        Move bestMove;
        char flag; // 'E' = exact, 'L' = lower bound, 'U' = upper bound
        
        TranspositionEntry() : hash(0), depth(0), score(0), flag(0) {}
        TranspositionEntry(uint64_t h, int d, int s, Move bm, char f) 
            : hash(h), depth(d), score(s), bestMove(bm), flag(f) {}
    };
    
    void storeInTT(uint64_t hash, int depth, int score, Move bestMove, char flag, int threadId);
    TranspositionEntry* probeTT(uint64_t hash, int threadId);
    
    // Эвристики оптимизации
    bool isFutile(int depth, int alpha, int staticEval) const;
    bool isRazoringApplicable(int depth, int beta, int staticEval) const;
    void updateHistory(const Move& move, int depth);
    int getHistoryScore(const Move& move) const;
    
    // Вспомогательные функции
    uint64_t hashPosition() const;
    bool isInCheck(Color color) const;
    int evaluatePosition() const;
};

// Утилиты для многопоточности
namespace ParallelUtils {
    // Определение оптимального числа потоков
    int getOptimalThreadCount();
    
    // Балансировка нагрузки
    void distributeWork(const std::vector<Move>& moves, int numThreads, 
                       std::vector<std::vector<Move>>& threadWork);
    
    // Сбор результатов
    Move aggregateResults(const std::vector<std::future<Move>>& futures);
}

// Константы для многопоточного поиска
namespace ParallelConstants {
    extern const int MIN_SPLIT_DEPTH;     // Минимальная глубина для разделения
    extern const int MAX_THREADS;         // Максимальное число потоков
    extern const int THREAD_STACK_SIZE;   // Размер стека потока
    extern const int ASPIRATION_WINDOW;   // Размер окна aspiration search
}

#endif // PARALLEL_SEARCH_HPP