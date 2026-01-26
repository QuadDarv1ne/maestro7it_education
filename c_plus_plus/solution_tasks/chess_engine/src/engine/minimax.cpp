#include "../include/minimax.hpp"
#include <algorithm>
#include <climits>

Minimax::Minimax(Board& board, int maxDepth) : board_(board), evaluator_(board), maxDepth_(maxDepth), timeLimit_(std::chrono::seconds(10)) {}

Move Minimax::findBestMove(Color color) {
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    
    if (moves.empty()) {
        return Move(); // Нет доступных ходов
    }
    
    Move bestMove = moves[0];
    int bestValue = (color == Color::WHITE) ? INT_MIN : INT_MAX;
    
    for (const Move& move : moves) {
        // Выполнить ход на временной доске
        // TODO: реализовать выполнение хода и откат
        
        int value = minimax(maxDepth_, INT_MIN, INT_MAX, color);
        
        if ((color == Color::WHITE && value > bestValue) || 
            (color == Color::BLACK && value < bestValue)) {
            bestValue = value;
            bestMove = move;
        }
    }
    
    return bestMove;
}

Move Minimax::findBestMoveWithTimeLimit(Color color, std::chrono::milliseconds timeLimit) {
    // TODO: реализовать поиск с ограничением по времени
    return findBestMove(color);
}

int Minimax::minimax(int depth, int alpha, int beta, Color maximizingPlayer) {
    if (depth == 0) {
        return evaluatePosition();
    }
    
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    
    if (maximizingPlayer == Color::WHITE) {
        int maxValue = INT_MIN;
        for (const Move& move : moves) {
            // TODO: выполнить ход
            int eval = minimax(depth - 1, alpha, beta, Color::BLACK);
            // TODO: откатить ход
            
            maxValue = std::max(maxValue, eval);
            alpha = std::max(alpha, eval);
            if (beta <= alpha) {
                break; // Альфа-бета отсечение
            }
        }
        return maxValue;
    } else {
        int minValue = INT_MAX;
        for (const Move& move : moves) {
            // TODO: выполнить ход
            int eval = minimax(depth - 1, alpha, beta, Color::WHITE);
            // TODO: откатить ход
            
            minValue = std::min(minValue, eval);
            beta = std::min(beta, eval);
            if (beta <= alpha) {
                break; // Альфа-бета отсечение
            }
        }
        return minValue;
    }
}

int Minimax::minimaxWithTimeLimit(int depth, int alpha, int beta, Color maximizingPlayer, 
                                 std::chrono::steady_clock::time_point startTime) {
    // TODO: реализовать минимакс с учетом времени
    return minimax(depth, alpha, beta, maximizingPlayer);
}

void Minimax::setMaxDepth(int depth) {
    maxDepth_ = depth;
}

void Minimax::setTimeLimit(std::chrono::milliseconds limit) {
    timeLimit_ = limit;
}

int Minimax::getMaxDepth() const {
    return maxDepth_;
}

std::vector<Move> Minimax::orderMoves(const std::vector<Move>& moves) const {
    // TODO: реализовать упорядочивание ходов для лучшего альфа-бета отсечения
    // Например: сначала взятия, затем остальные
    return moves; // Пока возвращаем без изменений
}

int Minimax::evaluatePosition() const {
    return evaluator_.evaluate();
}

bool Minimax::isTimeUp(std::chrono::steady_clock::time_point startTime) const {
    auto now = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(now - startTime);
    return elapsed >= timeLimit_;
}

int Minimax::quiescenceSearch(int alpha, int beta, int depth) {
    // TODO: реализовать тихий поиск (quiescence search)
    int standPat = evaluatePosition();
    
    if (standPat >= beta) {
        return beta;
    }
    
    if (alpha < standPat) {
        alpha = standPat;
    }
    
    // Рассмотреть только шахи и взятия
    return standPat;
}