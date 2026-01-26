#ifndef MINIMAX_HPP
#define MINIMAX_HPP

#include "board.hpp"
#include "move_generator.hpp"
#include "position_evaluator.hpp"
#include <limits>
#include <chrono>

class Minimax {
private:
    Board& board_;
    PositionEvaluator evaluator_;
    int maxDepth_;
    std::chrono::milliseconds timeLimit_;
    
public:
    Minimax(Board& board, int maxDepth = 4);
    
    // Main search methods
    Move findBestMove(Color color);
    Move findBestMoveWithTimeLimit(Color color, std::chrono::milliseconds timeLimit);
    
    // Search with alpha-beta pruning
    int minimax(int depth, int alpha, int beta, Color maximizingPlayer);
    int minimaxWithTimeLimit(int depth, int alpha, int beta, Color maximizingPlayer, 
                            std::chrono::steady_clock::time_point startTime);
    
    // Settings
    void setMaxDepth(int depth);
    void setTimeLimit(std::chrono::milliseconds limit);
    int getMaxDepth() const;
    
    // Move ordering for better pruning
    std::vector<Move> orderMoves(const std::vector<Move>& moves) const;
    
private:
    // Helper methods
    int evaluatePosition() const;
    bool isTimeUp(std::chrono::steady_clock::time_point startTime) const;
    int quiescenceSearch(int alpha, int beta, int depth);
};

// Constants for search
const int INF = std::numeric_limits<int>::max();
const int MATE_SCORE = 100000;
const int MAX_QUIESCENCE_DEPTH = 4;

#endif // MINIMAX_HPP