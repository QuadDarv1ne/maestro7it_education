#include "../include/minimax.hpp"
#include <algorithm>
#include <climits>
#include <random>
#include <functional>

Minimax::Minimax(Board& board, int maxDepth) : board_(board), evaluator_(board), maxDepth_(maxDepth), timeLimit_(std::chrono::seconds(10)), transpositionTable(HASH_TABLE_SIZE) {
    // Initialize the transposition table
    for(size_t i = 0; i < HASH_TABLE_SIZE; ++i) {
        transpositionTable[i] = TTEntry();
    }
}

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
    return minimaxWithTT(depth, alpha, beta, maximizingPlayer);
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
    std::vector<Move> orderedMoves = moves;
    
    // Упорядочиваем ходы по приоритетам:
    // 1. Ходы с прошлого лучшего варианта (killer moves)
    // 2. Взятия фигур
    // 3. Ходы пешек (продвижение)
    // 4. Прочие ходы
    
    std::sort(orderedMoves.begin(), orderedMoves.end(), [this](const Move& a, const Move& b) {
        // Оценка приоритета для первого хода
        int priorityA = getMovePriority(a);
        int priorityB = getMovePriority(b);
        
        // Сортировка по убыванию приоритета
        return priorityA > priorityB;
    });
    
    return orderedMoves;
}

int Minimax::getMovePriority(const Move& move) const {
    Piece capturedPiece = board_.getPiece(move.to);
    Piece movingPiece = board_.getPiece(move.from);
    
    // Приоритет для взятий - MVV (Most Valuable Victim) / LVA (Least Valuable Attacker)
    if (!capturedPiece.isEmpty()) {
        // Взятие с высокой стоимостью жертвы и низкой стоимостью атакующей фигуры
        int mvvLva = capturedPiece.getValue() - movingPiece.getValue() / 10;
        return 1000 + mvvLva;
    }
    
    // Приоритет для ходов пешки вперед
    if (movingPiece.getType() == PieceType::PAWN) {
        // Продвижение пешки
        int rankDiff = (movingPiece.getColor() == Color::WHITE) ? 
                      (board_.rank(move.to) - board_.rank(move.from)) : 
                      (board_.rank(move.from) - board_.rank(move.to));
        if (rankDiff > 0) {
            return 500 + rankDiff * 10;
        }
    }
    
    // Приоритет для ходов королевской пары (ферзь, король)
    if (movingPiece.getType() == PieceType::QUEEN) {
        return 400;
    }
    
    if (movingPiece.getType() == PieceType::KING) {
        return 300;
    }
    
    // Приоритет для других фигур
    return movingPiece.getValue();
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

// Simple hash function for board positions
uint64_t Minimax::hashPosition() const {
    // Simple XOR-based hashing - in a real implementation, you'd want Zobrist hashing
    uint64_t hash = 0;
    
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (!piece.isEmpty()) {
            // Combine piece type, color, and position
            uint64_t pieceHash = (piece.getType() * 16 + piece.getColor()) * 64 + square;
            hash ^= pieceHash;
        }
    }
    
    // Include whose turn it is
    hash ^= static_cast<int>(board_.getCurrentPlayer()) * 10000;
    
    return hash;
}

void Minimax::storeInTT(uint64_t hash, int depth, int score, Move bestMove, char flag) {
    size_t index = hash % HASH_TABLE_SIZE;
    
    transpositionTable[index] = TTEntry(hash, depth, score, bestMove, flag);
}

Minimax::TTEntry* Minimax::probeTT(uint64_t hash) {
    size_t index = hash % HASH_TABLE_SIZE;
    
    if (transpositionTable[index].hash == hash) {
        return &transpositionTable[index];
    }
    
    return nullptr;
}

int Minimax::minimaxWithTT(int depth, int alpha, int beta, Color maximizingPlayer) {
    // Check transposition table
    uint64_t hash = hashPosition();
    TTEntry* entry = probeTT(hash);
    
    if (entry && entry->depth >= depth) {
        if (entry->flag == 'E') { // Exact
            return entry->score;
        } else if (entry->flag == 'L' && entry->score >= beta) { // Lower bound
            return entry->score;
        } else if (entry->flag == 'U' && entry->score <= alpha) { // Upper bound
            return entry->score;
        }
    }
    
    if (depth == 0) {
        int score = evaluatePosition();
        
        if (!entry) {
            storeInTT(hash, depth, score, Move(), 'E');
        }
        
        return score;
    }
    
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    
    int bestScore;
    Move bestMove;
    bool hasBestMove = false;
    
    if (maximizingPlayer == Color::WHITE) {
        int maxValue = INT_MIN;
        for (const Move& move : moves) {
            // TODO: выполнить ход
            int eval = minimaxWithTT(depth - 1, alpha, beta, Color::BLACK);
            // TODO: откатить ход
            
            if (eval > maxValue) {
                maxValue = eval;
                bestMove = move;
                hasBestMove = true;
            }
            
            alpha = std::max(alpha, eval);
            if (beta <= alpha) {
                break; // Альфа-бета отсечение
            }
        }
        bestScore = maxValue;
    } else {
        int minValue = INT_MAX;
        for (const Move& move : moves) {
            // TODO: выполнить ход
            int eval = minimaxWithTT(depth - 1, alpha, beta, Color::WHITE);
            // TODO: откатить ход
            
            if (eval < minValue) {
                minValue = eval;
                bestMove = move;
                hasBestMove = true;
            }
            
            beta = std::min(beta, eval);
            if (beta <= alpha) {
                break; // Альфа-бета отсечение
            }
        }
        bestScore = minValue;
    }
    
    // Store result in transposition table
    char flag;
    if (bestScore <= alpha) {
        flag = 'U'; // Upper bound
    } else if (bestScore >= beta) {
        flag = 'L'; // Lower bound
    } else {
        flag = 'E'; // Exact
    }
    
    storeInTT(hash, depth, bestScore, hasBestMove ? bestMove : Move(), flag);
    
    return bestScore;
}