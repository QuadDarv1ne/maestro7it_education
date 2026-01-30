#ifndef ADVANCED_AI_HPP
#define ADVANCED_AI_HPP

#include <vector>
#include <map>
#include <algorithm>
#include <climits>
#include <chrono>
#include <random>

/**
 * @brief Продвинутый искусственный интеллект для шахмат
 * 
 * Реализует алгоритмы минимакс с альфа-бета отсечением,
 * транспозиционные таблицы и улучшенное упорядочивание ходов.
 */
class AdvancedAI {
private:
    // Константы для оценки
    static const int PAWN_VALUE = 100;
    static const int KNIGHT_VALUE = 320;
    static const int BISHOP_VALUE = 330;
    static const int ROOK_VALUE = 500;
    static const int QUEEN_VALUE = 900;
    static const int KING_VALUE = 20000;
    
    // Позиционные бонусы
    static const int PAWN_POSITION_BONUS[64];
    static const int KNIGHT_POSITION_BONUS[64];
    static const int BISHOP_POSITION_BONUS[64];
    static const int ROOK_POSITION_BONUS[64];
    static const int QUEEN_POSITION_BONUS[64];
    static const int KING_POSITION_BONUS[64];
    
    // Настройки поиска
    int search_depth_;
    int time_limit_ms_;
    bool use_transposition_table_;
    
    // Транспозиционная таблица
    struct TTEntry {
        long long hash_key;
        int depth;
        int score;
        int flag; // 0 = exact, 1 = lower bound, 2 = upper bound
        int best_move_from;
        int best_move_to;
    };
    
    std::map<long long, TTEntry> transposition_table_;
    
    // Статистика поиска
    int nodes_searched_;
    int tt_hits_;
    std::chrono::steady_clock::time_point search_start_time_;
    
    // Генератор случайных чисел
    std::mt19937 rng_;
    
public:
    AdvancedAI(int depth = 4, int time_limit = 5000);
    
    // Основной интерфейс AI
    std::pair<int, int> getBestMove(const std::vector<std::vector<char>>& board, bool is_white);
    
    // Алгоритмы поиска
    int minimax(const std::vector<std::vector<char>>& board, int depth, bool is_maximizing, 
                int alpha, int beta, bool is_white);
    
    // Упорядочивание ходов
    std::vector<std::pair<int, int>> getOrderedMoves(const std::vector<std::vector<char>>& board, 
                                                     bool is_white);
    
    // Оценка позиции
    int evaluatePosition(const std::vector<std::vector<char>>& board, bool is_white);
    
    // Вспомогательные методы
    long long generateHashKey(const std::vector<std::vector<char>>& board, bool is_white);
    bool isGameOver(const std::vector<std::vector<char>>& board);
    int getMaterialScore(const std::vector<std::vector<char>>& board);
    int getPositionalScore(const std::vector<std::vector<char>>& board, bool is_white);
    
    // Транспозиционная таблица
    void storeTTEntry(long long hash_key, int depth, int score, int flag, 
                     int best_move_from, int best_move_to);
    TTEntry* probeTT(long long hash_key);
    
    // Получение статистики
    int getNodesSearched() const { return nodes_searched_; }
    int getTTHits() const { return tt_hits_; }
    void resetStatistics();
};

// Реализация позиционных бонусов
const int AdvancedAI::PAWN_POSITION_BONUS[64] = {
    0,  0,  0,  0,  0,  0,  0,  0,
   50, 50, 50, 50, 50, 50, 50, 50,
   10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
};

const int AdvancedAI::KNIGHT_POSITION_BONUS[64] = {
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50
};

const int AdvancedAI::BISHOP_POSITION_BONUS[64] = {
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20
};

const int AdvancedAI::ROOK_POSITION_BONUS[64] = {
  0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0
};

const int AdvancedAI::QUEEN_POSITION_BONUS[64] = {
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20
};

const int AdvancedAI::KING_POSITION_BONUS[64] = {
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
 20, 20,  0,  0,  0,  0, 20, 20,
 20, 30, 10,  0,  0, 10, 30, 20
};

#endif // ADVANCED_AI_HPP