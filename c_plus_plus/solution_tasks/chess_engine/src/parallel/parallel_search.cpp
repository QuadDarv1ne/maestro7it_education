#include "../../include/parallel_search.hpp"
#include <iostream>
#include <algorithm>
#include <climits>
#include <chrono>

ParallelSearch::ParallelSearch(const Bitboard& board, IncrementalEvaluator& evaluator, 
                              int max_depth, int num_threads)
    : board_(board), evaluator_(evaluator), max_depth_(max_depth), 
      num_threads_(num_threads), time_limit_(std::chrono::milliseconds(10000)),
      stop_search_(false), best_score_(INT_MIN), nodes_searched_(0) {
    
    transposition_table_.resize(TT_SIZE);
}

void ParallelSearch::resetStats() {
    nodes_searched_ = 0;
}

void ParallelSearch::stop() {
    stop_search_ = true;
}

bool ParallelSearch::isTimeUp() const {
    auto now = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(now - start_time_);
    return elapsed >= time_limit_;
}

std::pair<int, int> ParallelSearch::findBestMove(Bitboard::Color color) {
    resetStats();
    stop_search_ = false;
    start_time_ = std::chrono::steady_clock::now();
    best_score_ = (color == Bitboard::Color::WHITE) ? INT_MIN : INT_MAX;
    best_move_ = {-1, -1};

    auto moves = board_.generateLegalMoves();
    if (moves.empty()) return {-1, -1};

    int moves_per_thread = (moves.size() + num_threads_ - 1) / num_threads_;
    std::vector<std::thread> threads;

    for (int i = 0; i < num_threads_; ++i) {
        int start = i * moves_per_thread;
        int end = std::min(static_cast<int>(moves.size()), (i + 1) * moves_per_thread);
        if (start < end) {
            threads.emplace_back(&ParallelSearch::workerThread, this, i, moves, start, end, color);
        }
    }

    for (auto& t : threads) {
        if (t.joinable()) t.join();
    }

    return best_move_;
}

void ParallelSearch::workerThread(int thread_id, std::vector<std::pair<int, int>> moves, 
                                 int start_idx, int end_idx, Bitboard::Color color) {
    int local_best_score = (color == Bitboard::Color::WHITE) ? INT_MIN : INT_MAX;
    std::pair<int, int> local_best_move = {-1, -1};

    for (int i = start_idx; i < end_idx; ++i) {
        if (stop_search_ || isTimeUp()) {
            stop_search_ = true;
            break;
        }

        Bitboard local_board = board_;
        auto move = moves[i];
        local_board.movePiece(move.first, move.second);
        
        IncrementalEvaluator local_eval(local_board);
        int score = alphabeta(local_board, local_eval, max_depth_ - 1, INT_MIN + 1, INT_MAX - 1, 
                             (color == Bitboard::Color::WHITE ? Bitboard::Color::BLACK : Bitboard::Color::WHITE));

        if (color == Bitboard::Color::WHITE) {
            if (score > local_best_score) {
                local_best_score = score;
                local_best_move = move;
            }
        } else {
            if (score < local_best_score) {
                local_best_score = score;
                local_best_move = move;
            }
        }
    }

    std::lock_guard<std::mutex> lock(mutex_);
    if (color == Bitboard::Color::WHITE) {
        if (local_best_score > best_score_) {
            best_score_ = local_best_score;
            best_move_ = local_best_move;
        }
    } else {
        if (local_best_score < best_score_) {
            best_score_ = local_best_score;
            best_move_ = local_best_move;
        }
    }
}

int ParallelSearch::alphabeta(Bitboard& b, IncrementalEvaluator& eval, int depth, int alpha, int beta, Bitboard::Color color) {
    nodes_searched_++;
    
    if (depth == 0) {
        return eval.evaluate();
    }

    if (nodes_searched_ % 1000 == 0 && isTimeUp()) {
        stop_search_ = true;
        return eval.evaluate();
    }

    auto moves = b.generateLegalMoves();
    if (moves.empty()) {
        if (b.isInCheck(color)) return (color == Bitboard::Color::WHITE) ? -20000 : 20000;
        return 0;
    }

    if (color == Bitboard::Color::WHITE) {
        int max_eval = INT_MIN + 1;
        for (const auto& move : moves) {
            Bitboard next_board = b;
            next_board.movePiece(move.first, move.second);
            IncrementalEvaluator next_eval(next_board);
            int eval_score = alphabeta(next_board, next_eval, depth - 1, alpha, beta, Bitboard::Color::BLACK);
            max_eval = std::max(max_eval, eval_score);
            alpha = std::max(alpha, eval_score);
            if (beta <= alpha) break;
            if (stop_search_) break;
        }
        return max_eval;
    } else {
        int min_eval = INT_MAX - 1;
        for (const auto& move : moves) {
            Bitboard next_board = b;
            next_board.movePiece(move.first, move.second);
            IncrementalEvaluator next_eval(next_board);
            int eval_score = alphabeta(next_board, next_eval, depth - 1, alpha, beta, Bitboard::Color::WHITE);
            min_eval = std::min(min_eval, eval_score);
            beta = std::min(beta, eval_score);
            if (beta <= alpha) break;
            if (stop_search_) break;
        }
        return min_eval;
    }
}

uint64_t ParallelSearch::hashPosition(const Bitboard& b) const {
    // Упрощенная реализация хеширования, если Bitboard не поддерживает Zobrist
    return 0; 
}

void ParallelSearch::storeInTT(uint64_t hash, int depth, int score, std::pair<int, int> move, char flag) {
    // Временно не используем ТТ для упрощения и во избежание проблем с многопоточностью
}

ParallelSearch::TTEntry* ParallelSearch::probeTT(uint64_t hash) {
    return nullptr;
}

void ParallelSearch::setMaxDepth(int depth) {
    max_depth_ = depth;
}

void ParallelSearch::setNumThreads(int threads) {
    num_threads_ = threads;
}

void ParallelSearch::setTimeLimit(std::chrono::milliseconds limit) {
    time_limit_ = limit;
}

void ParallelSearch::printSearchStats() const {
    std::cout << "Узлов исследовано: " << nodes_searched_.load() << std::endl;
}

