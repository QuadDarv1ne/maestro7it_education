#ifndef PARALLEL_SEARCH_HPP
#define PARALLEL_SEARCH_HPP

#include "bitboard.hpp"
#include "incremental_evaluator.hpp"
#include <thread>
#include <mutex>
#include <atomic>
#include <vector>
#include <future>
#include <condition_variable>

/**
 * @brief Многопоточный поиск лучших ходов
 * 
 * Реализует параллельный алгоритм минимакс с альфа-бета отсечением
 * с использованием нескольких потоков для ускорения поиска.
 */
class ParallelSearch {
private:
    const Bitboard& board_;
    IncrementalEvaluator& evaluator_;
    
    // Параметры поиска
    int max_depth_;
    int num_threads_;
    std::chrono::milliseconds time_limit_;
    
    // Синхронизация
    std::mutex mutex_;
    std::condition_variable cv_;
    std::atomic<bool> stop_search_;
    std::atomic<int> best_score_;
    std::atomic<int> nodes_searched_;
    
    // Результаты поиска
    std::pair<int, int> best_move_;
    std::vector<std::future<void>> futures_;
    
    // Таблица транспозиций
    struct TTEntry {
        uint64_t hash;
        int depth;
        int score;
        std::pair<int, int> best_move;
        char flag; // 'E', 'L', 'U'
    };
    
    static const size_t TT_SIZE = 1000000;
    std::vector<TTEntry> transposition_table_;
    
    // Вспомогательные методы
    uint64_t hashPosition() const;
    void storeInTT(uint64_t hash, int depth, int score, std::pair<int, int> move, char flag);
    TTEntry* probeTT(uint64_t hash);
    
    // Алгоритмы поиска
    int minimax(int depth, int alpha, int beta, Bitboard::Color color, int thread_id = 0);
    int alphabeta(int depth, int alpha, int beta, Bitboard::Color color, int thread_id);
    
    // Параллельные методы
    void workerThread(int thread_id, std::vector<std::pair<int, int>> moves, 
                     int start_idx, int end_idx, Bitboard::Color color);
    
    bool isTimeUp() const;
    
public:
    ParallelSearch(const Bitboard& board, IncrementalEvaluator& evaluator, 
                  int max_depth = 6, int num_threads = 4);
    
    // Основной метод поиска
    std::pair<int, int> findBestMove(Bitboard::Color color);
    
    // Настройки
    void setMaxDepth(int depth);
    void setNumThreads(int threads);
    void setTimeLimit(std::chrono::milliseconds limit);
    
    // Статистика
    int getNodesSearched() const { return nodes_searched_.load(); }
    void resetStats();
    
    // Управление поиском
    void stop();
    
    // Отладочные методы
    void printSearchStats() const;
};

// Константы для параллельного поиска
namespace ParallelConstants {
    const int MIN_SPLIT_DEPTH = 3;  // Минимальная глубина для разделения работы
    const int SPLIT_THRESHOLD = 5;  // Минимальное количество ходов для разделения
    const int NODES_BETWEEN_CHECKS = 1000; // Проверка остановки каждые N узлов
}

#endif // PARALLEL_SEARCH_HPP