#include "../include/minimax.hpp"
#include <algorithm>
#include <climits>
#include <random>
#include <functional>

Minimax::Minimax(Board& board, int maxDepth) : board_(board), evaluator_(board), maxDepth_(maxDepth), timeLimit_(std::chrono::seconds(10)), transpositionTable(HASH_TABLE_SIZE), killerMoves(MAX_PLY, std::vector<Move>(MAX_KILLER_MOVES)), historyTable(HISTORY_SIZE, 0) {
    // Initialize the transposition table
    for(size_t i = 0; i < HASH_TABLE_SIZE; ++i) {
        transpositionTable[i] = TTEntry();
    }
    
    // Initialize killer moves
    for (int ply = 0; ply < MAX_PLY; ply++) {
        for (int k = 0; k < MAX_KILLER_MOVES; k++) {
            killerMoves[ply][k] = Move();
        }
    }
    
    // Initialize history table
    for (int i = 0; i < HISTORY_SIZE; i++) {
        historyTable[i] = 0;
    }
}

Move Minimax::findBestMove(Color color) {
    Move bestMove;
    int bestValue = 0;
    bool firstIteration = true;
    
    // Итеративное углубление с aspiration search
    for (int depth = 1; depth <= maxDepth_; depth++) {
        std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
        
        if (moves.empty()) {
            return Move(); // Нет доступных ходов
        }
        
        Move currentBestMove = moves[0];
        int currentValue;
        
        if (firstIteration) {
            // First iteration - use full window search
            currentValue = minimax(depth, INT_MIN, INT_MAX, color);
            firstIteration = false;
        } else {
            // Subsequent iterations - use aspiration search
            currentValue = aspirationSearch(depth, bestValue, color);
        }
        
        // Find the move that gives this value
        for (const Move& move : moves) {
            // TODO: Actually execute moves and find which one gives currentValue
            // For now, we'll use a simplified approach
            if ((color == Color::WHITE && currentValue > bestValue) || 
                (color == Color::BLACK && currentValue < bestValue)) {
                currentBestMove = move;
                break;
            }
        }
        
        // Обновляем лучший ход и значение
        bestMove = currentBestMove;
        bestValue = currentValue;
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

int Minimax::getMovePriority(const Move& move, int ply = 0) const {
    Piece capturedPiece = board_.getPiece(move.to);
    Piece movingPiece = board_.getPiece(move.from);
    
    // Приоритет для killer moves
    if (isKillerMove(move, ply)) {
        return 2000; // Высокий приоритет для killer moves
    }
    
    // Приоритет для взятий - MVV (Most Valuable Victim) / LVA (Least Valuable Attacker)
    if (!capturedPiece.isEmpty()) {
        // Взятие с высокой стоимостью жертвы и низкой стоимостью атакующей фигуры
        int mvvLva = capturedPiece.getValue() - movingPiece.getValue() / 10;
        return 1000 + mvvLva;
    }
    
    // Приоритет для истории ходов
    int historyScore = getHistoryScore(move);
    if (historyScore > 0) {
        return 800 + historyScore / 100; // Масштабируем для согласования
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

bool Minimax::isInCheck(Color color) const {
    // Найдем короля нужного цвета
    Square kingSquare = INVALID_SQUARE;
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(static_cast<Square>(square));
        if (piece.getType() == PieceType::KING && piece.getColor() == color) {
            kingSquare = static_cast<Square>(square);
            break;
        }
    }
    
    if (kingSquare == INVALID_SQUARE) {
        return false; // Король не найден (теоретически невозможно)
    }
    
    // Проверим, атакован ли король
    MoveGenerator generator(board_);
    Color opponentColor = (color == Color::WHITE) ? Color::BLACK : Color::WHITE;
    return generator.isSquareAttacked(kingSquare, opponentColor);
}

void Minimax::addKillerMove(const Move& move, int ply) {
    if (ply >= MAX_PLY) return;
    
    // Не добавляем ходы взятия как killer moves
    Piece capturedPiece = board_.getPiece(move.to);
    if (!capturedPiece.isEmpty()) {
        return;
    }
    
    // Сдвигаем существующие killer moves
    for (int i = MAX_KILLER_MOVES - 1; i > 0; i--) {
        killerMoves[ply][i] = killerMoves[ply][i-1];
    }
    
    // Добавляем новый killer move
    killerMoves[ply][0] = move;
}

bool Minimax::isKillerMove(const Move& move, int ply) const {
    if (ply >= MAX_PLY) return false;
    
    for (int i = 0; i < MAX_KILLER_MOVES; i++) {
        if (killerMoves[ply][i].from == move.from && 
            killerMoves[ply][i].to == move.to) {
            return true;
        }
    }
    return false;
}

int Minimax::aspirationSearch(int depth, int previousScore, Color maximizingPlayer) {
    const int ASPIRATION_WINDOW = 50; // Window size around previous score
    
    int alpha = previousScore - ASPIRATION_WINDOW;
    int beta = previousScore + ASPIRATION_WINDOW;
    
    int score = minimaxWithTT(depth, alpha, beta, maximizingPlayer);
    
    // If we failed high or low, search with full window
    if (score <= alpha || score >= beta) {
        score = minimaxWithTT(depth, INT_MIN, INT_MAX, maximizingPlayer);
    }
    
    return score;
}

void Minimax::updateHistory(const Move& move, int depth) {
    // Don't update history for captures or promotions
    Piece capturedPiece = board_.getPiece(move.to);
    if (!capturedPiece.isEmpty() || move.promotion != PieceType::EMPTY) {
        return;
    }
    
    // Calculate index in history table
    int index = move.from * 64 + move.to;
    if (index >= 0 && index < HISTORY_SIZE) {
        // Increase history score, but prevent overflow
        historyTable[index] += depth * depth;
        if (historyTable[index] > 10000) {
            // Scale down all history scores to prevent overflow
            for (int i = 0; i < HISTORY_SIZE; i++) {
                historyTable[i] /= 2;
            }
        }
    }
}

int Minimax::getHistoryScore(const Move& move) const {
    int index = move.from * 64 + move.to;
    if (index >= 0 && index < HISTORY_SIZE) {
        return historyTable[index];
    }
    return 0;
}

bool Minimax::isFutile(int depth, int alpha, int staticEval) const {
    // Futility pruning constants (in centipawns)
    static const int FUTILITY_MARGIN[] = {0, 100, 300, 500, 900};
    
    if (depth >= 4) return false; // Only apply for shallow depths
    if (depth <= 0 || depth >= 5) return false;
    
    // Check if the static evaluation plus margin is still below alpha
    int margin = (depth < 5) ? FUTILITY_MARGIN[depth] : 900;
    return (staticEval + margin) <= alpha;
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
    
    // Null-move pruning
    if (depth >= 3 && !isInCheck(maximizingPlayer)) {
        // Make null move (pass the turn)
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        board_.setCurrentPlayer(opponent);
        
        int nullScore = -minimaxWithTT(depth - 1 - 2, -beta, -beta + 1, opponent);
        
        // Restore player
        board_.setCurrentPlayer(maximizingPlayer);
        
        if (nullScore >= beta) {
            return beta; // Prune the subtree
        }
    }
    
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    
    int bestScore;
    Move bestMove;
    bool hasBestMove = false;
    
    if (maximizingPlayer == Color::WHITE) {
        int maxValue = INT_MIN;
        for (size_t i = 0; i < moves.size(); i++) {
            const Move& move = moves[i];
            // TODO: выполнить ход
            int reduction = (i >= 4 && depth >= 3) ? 1 : 0; // Late move reduction
            int eval = minimaxWithTT(depth - 1 - reduction, alpha, beta, Color::BLACK);
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
        for (size_t i = 0; i < moves.size(); i++) {
            const Move& move = moves[i];
            // TODO: выполнить ход
            int reduction = (i >= 4 && depth >= 3) ? 1 : 0; // Late move reduction
            int eval = minimaxWithTT(depth - 1 - reduction, alpha, beta, Color::WHITE);
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