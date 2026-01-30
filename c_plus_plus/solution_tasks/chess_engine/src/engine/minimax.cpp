#include "../include/minimax.hpp"
#include "../include/board.hpp"
#include <algorithm>
#include <climits>
#include <random>
#include <functional>
#include <iostream>

Minimax::Minimax(Board& board, int maxDepth) : board_(board), evaluator_(board), openingBook_(), maxDepth_(maxDepth), timeLimit_(std::chrono::seconds(10)), transpositionTable(HASH_TABLE_SIZE), killerMoves(MAX_PLY, std::vector<Move>(MAX_KILLER_MOVES)), historyTable(HISTORY_SIZE, 0) {
    initZobrist();
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
    int bestValue = (color == Color::WHITE) ? INT_MIN : INT_MAX;
    auto startTime = std::chrono::steady_clock::now();
    
    // Проверка книги дебютов
    // ... (код книги дебютов оставляем как есть) ...
    
    // Итеративное углубление
    for (int depth = 1; depth <= maxDepth_; depth++) {
        // Проверяем время перед новой глубиной
        if (isTimeUp(startTime)) {
            break;
        }

        std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
        if (moves.empty()) break;

        Move currentBestMove;
        int currentBestValue = (color == Color::WHITE) ? INT_MIN : INT_MAX;

        for (const Move& move : moves) {
            // Выполняем ход
            board_.makeMove(move.from, move.to);
            
            // Поиск (используем minimaxWithTT или PVS)
            int eval = minimaxWithTT(depth - 1, INT_MIN, INT_MAX, (color == Color::WHITE ? Color::BLACK : Color::WHITE));
            
            // Отменяем ход
            board_.undoMove();

            if (color == Color::WHITE) {
                if (eval > currentBestValue) {
                    currentBestValue = eval;
                    currentBestMove = move;
                }
            } else {
                if (eval < currentBestValue) {
                    currentBestValue = eval;
                    currentBestMove = move;
                }
            }
            
            // Проверка времени внутри цикла по ходам
            if (isTimeUp(startTime)) break;
        }

        if (!isTimeUp(startTime) || depth == 1) {
            bestMove = currentBestMove;
            bestValue = currentBestValue;
        }
    }
    
    return bestMove;
}

Move Minimax::findBestMoveWithTimeLimit(Color color, std::chrono::milliseconds timeLimit) {
    setTimeLimit(timeLimit);
    return findBestMove(color);
}

int Minimax::minimaxWithTimeLimit(int depth, int alpha, int beta, Color maximizingPlayer, 
                                 std::chrono::steady_clock::time_point startTime) {
    if (isTimeUp(startTime)) return evaluatePosition();
    return minimaxWithTT(depth, alpha, beta, maximizingPlayer);
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

int Minimax::getMovePriority(const Move& move, int ply) const {
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

bool Minimax::isRazoringApplicable(int depth, int beta, int staticEval) const {
    // Razoring constants (in centipawns)
    static const int RAZOR_MARGIN[] = {0, 300, 400, 600, 800};
    
    if (depth >= 4) return false; // Only apply for shallow depths
    if (depth <= 0 || depth >= 5) return false;
    
    // Check if the static evaluation minus margin is still above beta
    int margin = (depth < 5) ? RAZOR_MARGIN[depth] : 800;
    return (staticEval - margin) >= beta;
}

int Minimax::multiCutPruning(int depth, int alpha, int beta, Color maximizingPlayer, int cutNumber) {
    // Multi-cut pruning - try to prove multiple cuts in one search
    if (depth <= 2 || cutNumber <= 0) {
        return minimaxWithTT(depth, alpha, beta, maximizingPlayer);
    }
    
    // Try to find multiple good moves that would cause beta cutoffs
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    if (moves.empty()) {
        return evaluatePosition();
    }
    
    int bestValue = (maximizingPlayer == Color::WHITE) ? INT_MIN : INT_MAX;
    int cutsFound = 0;
    const int CUT_THRESHOLD = 2; // Number of cuts needed to trigger multi-cut
    
    for (size_t i = 0; i < moves.size() && cutsFound < CUT_THRESHOLD; i++) {
        const Move& move = moves[i];
        
        // Execute move
        Piece capturedPiece = board_.getPiece(move.to);
        Piece movingPiece = board_.getPiece(move.from);
        board_.setPiece(move.to, movingPiece);
        board_.setPiece(move.from, Piece());
        
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        board_.setCurrentPlayer(opponent);
        
        // Reduced depth search to test for cuts
        int reducedDepth = depth - 2;
        int eval = -minimaxWithTT(reducedDepth, -beta, -alpha, opponent);
        
        // Restore board
        board_.setPiece(move.from, movingPiece);
        board_.setPiece(move.to, capturedPiece);
        board_.setCurrentPlayer(maximizingPlayer);
        
        // Check if this move causes a cut
        if ((maximizingPlayer == Color::WHITE && eval >= beta) ||
            (maximizingPlayer == Color::BLACK && eval <= alpha)) {
            cutsFound++;
        }
        
        // Update best value
        if (maximizingPlayer == Color::WHITE) {
            bestValue = std::max(bestValue, eval);
            alpha = std::max(alpha, eval);
        } else {
            bestValue = std::min(bestValue, eval);
            beta = std::min(beta, eval);
        }
        
        // Early termination if we found enough cuts
        if (cutsFound >= CUT_THRESHOLD) {
            return bestValue;
        }
    }
    
    // If we didn't find enough cuts, do normal search
    return minimaxWithTT(depth, alpha, beta, maximizingPlayer);
}

int Minimax::evaluatePosition() const {
    return evaluator_.evaluate();
}

std::vector<Move> Minimax::orderCaptures(const std::vector<Move>& captures) const {
    std::vector<Move> orderedCaptures = captures;
    
    // Order captures by MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
    std::sort(orderedCaptures.begin(), orderedCaptures.end(), [this](const Move& a, const Move& b) {
        Piece victimA = board_.getPiece(a.to);
        Piece attackerA = board_.getPiece(a.from);
        Piece victimB = board_.getPiece(b.to);
        Piece attackerB = board_.getPiece(b.from);
        
        // MVV-LVA scoring: higher value for more valuable victims and less valuable attackers
        int scoreA = victimA.getValue() * 10 - attackerA.getValue();
        int scoreB = victimB.getValue() * 10 - attackerB.getValue();
        
        return scoreA > scoreB;
    });
    
    return orderedCaptures;
}

int Minimax::quiescenceSearch(int alpha, int beta, Color maximizingPlayer, int ply) {
    // Stand pat evaluation
    int standPat = evaluatePosition();
    
    // Beta cutoff
    if (standPat >= beta) {
        return beta;
    }
    
    // Alpha update
    if (standPat > alpha) {
        alpha = standPat;
    }
    
    // Generate only captures and legal moves (simplified - generate all legal moves and filter captures)
    MoveGenerator generator(board_);
    std::vector<Move> allMoves = generator.generateLegalMoves();
    
    // Filter only captures
    std::vector<Move> tacticalMoves;
    for (const Move& move : allMoves) {
        if (move.isCapture || isInCheck(maximizingPlayer)) {
            tacticalMoves.push_back(move);
        }
    }
    
    // Order tactical moves
    tacticalMoves = orderCaptures(tacticalMoves);
    
    // Limit quiescence depth to prevent explosion
    const int MAX_QUIESCENCE_DEPTH = 8;
    if (ply >= MAX_QUIESCENCE_DEPTH) {
        return standPat;
    }
    
    int bestValue = standPat;
    
    for (const Move& move : tacticalMoves) {
        // Delta pruning - if capture gain + positional bonus doesn't beat alpha, skip
        Piece captured = board_.getPiece(move.to);
        if (!captured.isEmpty()) {
            int delta = captured.getValue() + 200; // Positional bonus
            if (standPat + delta < alpha) {
                continue; // Skip this capture
            }
        }
        
        // Execute move
        Piece capturedPiece = board_.getPiece(move.to);
        Piece movingPiece = board_.getPiece(move.from);
        board_.setPiece(move.to, movingPiece);
        board_.setPiece(move.from, Piece());
        
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        board_.setCurrentPlayer(opponent);
        
        // Recursive quiescence search
        int score = -quiescenceSearch(-beta, -alpha, opponent, ply + 1);
        
        // Restore board
        board_.setPiece(move.from, movingPiece);
        board_.setPiece(move.to, capturedPiece);
        board_.setCurrentPlayer(maximizingPlayer);
        
        // Update best value and bounds
        if (score > bestValue) {
            bestValue = score;
            if (score > alpha) {
                alpha = score;
                if (score >= beta) {
                    break; // Beta cutoff
                }
            }
        }
    }
    
    return bestValue;
}

bool Minimax::probCut(int depth, int beta, Color maximizingPlayer, int threshold) {
    // ProbCut - probabilistic cutoff based on shallow search
    if (depth < 3) return false; // Only apply for sufficient depth
    
    // Perform a shallow search with reduced depth
    int shallowDepth = depth - 2;
    int shallowBeta = beta - threshold;
    
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    if (moves.empty()) return false;
    
    // Test the top few moves with shallow search
    int testMoves = std::min(3, static_cast<int>(moves.size()));
    
    for (int i = 0; i < testMoves; i++) {
        const Move& move = moves[i];
        
        // Execute move
        Piece capturedPiece = board_.getPiece(move.to);
        Piece movingPiece = board_.getPiece(move.from);
        board_.setPiece(move.to, movingPiece);
        board_.setPiece(move.from, Piece());
        
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        board_.setCurrentPlayer(opponent);
        
        // Shallow search
        int shallowScore = -minimaxWithTT(shallowDepth, -shallowBeta - 1, -shallowBeta, opponent);
        
        // Restore board
        board_.setPiece(move.from, movingPiece);
        board_.setPiece(move.to, capturedPiece);
        board_.setCurrentPlayer(maximizingPlayer);
        
        // If shallow search exceeds threshold, likely to cause cutoff
        if (shallowScore >= shallowBeta) {
            // Do a verification search at full depth
            int verifyScore = -minimaxWithTT(depth - 1, -beta - 1, -beta, opponent);
            
            if (verifyScore >= beta) {
                return true; // Probabilistic cutoff confirmed
            }
        }
    }
    
    return false; // No cutoff predicted
}

int Minimax::calculateExtension(const Move& move, Color maximizingPlayer, int depth) const {
    int extension = 0;
    
    // Check extensions
    if (isInCheck(maximizingPlayer)) {
        extension += 1; // One ply extension for check positions
    }
    
    // Capture extensions
    Piece capturedPiece = board_.getPiece(move.to);
    if (!capturedPiece.isEmpty()) {
        // Extend for capture of valuable pieces
        if (capturedPiece.getValue() >= 500) { // Queen or rook
            extension += 1;
        } else if (capturedPiece.getValue() >= 300) { // Bishop or knight
            extension += 0; // No extension for minor pieces
        }
    }
    
    // Promotion extensions
    if (move.promotion != PieceType::EMPTY) {
        extension += 1; // Extend for promotions
    }
    
    // Pawn push extensions near promotion
    Piece movingPiece = board_.getPiece(move.from);
    if (movingPiece.getType() == PieceType::PAWN) {
        int toRank = board_.rank(move.to);
        if ((movingPiece.getColor() == Color::WHITE && toRank >= 6) ||
            (movingPiece.getColor() == Color::BLACK && toRank <= 1)) {
            extension += 1; // Extend pawn pushes to 7th/2nd rank
        }
    }
    
    // Limit total extension
    return std::min(extension, 2); // Maximum 2 ply extension
}

bool Minimax::isCriticalPosition() const {
    // A position is critical if:
    // 1. King is in check
    // 2. Material balance is close (within 200 centipawns)
    // 3. Position has tactical threats
    
    Color currentPlayer = board_.getCurrentPlayer();
    if (isInCheck(currentPlayer)) {
        return true;
    }
    
    // Check material balance
    int materialEval = evaluatePosition(); // Use the general evaluation function
    if (std::abs(materialEval) <= 200) {
        return true; // Close game
    }
    
    // TODO: Add more sophisticated critical position detection
    // - Look for hanging pieces
    // - Check for tactical motifs
    // - Analyze pawn structure tension
    
    return false;
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
void Minimax::initZobrist() {
    std::mt19937_64 rng(123456789); // Fixed seed for reproducibility
    std::uniform_int_distribution<uint64_t> dist(0, std::numeric_limits<uint64_t>::max());
    
    for (int i = 0; i < 64; i++) {
        for (int j = 0; j < 12; j++) {
            zobristTable[i][j] = dist(rng);
        }
    }
    
    zobristBlackToMove = dist(rng);
    
    for (int i = 0; i < 16; i++) {
        zobristCastling[i] = dist(rng);
    }
    
    for (int i = 0; i < 8; i++) {
        zobristEnPassant[i] = dist(rng);
    }
}

uint64_t Minimax::hashPosition() const {
    uint64_t hash = 0;
    
    // Pieces
    for (int square = 0; square < 64; square++) {
        Piece piece = board_.getPiece(square);
        if (!piece.isEmpty()) {
            int pieceIdx = static_cast<int>(piece.getType());
            if (piece.getColor() == Color::BLACK) pieceIdx += 6;
            hash ^= zobristTable[square][pieceIdx];
        }
    }
    
    // Turn
    if (board_.getCurrentPlayer() == Color::BLACK) {
        hash ^= zobristBlackToMove;
    }
    
    // Castling
    int castlingIdx = 0;
    if (board_.canCastleKingSide(Color::WHITE)) castlingIdx |= 1;
    if (board_.canCastleQueenSide(Color::WHITE)) castlingIdx |= 2;
    if (board_.canCastleKingSide(Color::BLACK)) castlingIdx |= 4;
    if (board_.canCastleQueenSide(Color::BLACK)) castlingIdx |= 8;
    hash ^= zobristCastling[castlingIdx];
    
    // En passant
    Square ep = board_.getEnPassantSquare();
    if (ep != INVALID_SQUARE) {
        hash ^= zobristEnPassant[board_.file(ep)];
    }
    
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
            
            // Выполняем ход
            board_.makeMove(move.from, move.to);
            
            int reduction = (i >= 4 && depth >= 3) ? 1 : 0; // Late move reduction
            int eval = minimaxWithTT(depth - 1 - reduction, alpha, beta, Color::BLACK);
            
            // Отменяем ход
            board_.undoMove();
            
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
            
            // Выполняем ход
            board_.makeMove(move.from, move.to);
            
            int reduction = (i >= 4 && depth >= 3) ? 1 : 0; // Late move reduction
            int eval = minimaxWithTT(depth - 1 - reduction, alpha, beta, Color::WHITE);
            
            // Отменяем ход
            board_.undoMove();
            
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

int Minimax::principalVariationSearch(int depth, int alpha, int beta, Color maximizingPlayer, bool isPVNode) {
    // Base case: leaf node
    if (depth <= 0) {
        return quiescenceSearch(alpha, beta, maximizingPlayer);
    }
    
    // Check transposition table
    uint64_t hash = hashPosition();
    TTEntry* entry = probeTT(hash);
    
    if (entry && entry->depth >= depth) {
        if (entry->flag == 'E') return entry->score; // Exact score
        if (entry->flag == 'L' && entry->score >= beta) return beta; // Lower bound
        if (entry->flag == 'U' && entry->score <= alpha) return alpha; // Upper bound
    }
    
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    if (moves.empty()) {
        return evaluatePosition();
    }
    
    int bestValue = (maximizingPlayer == Color::WHITE) ? INT_MIN : INT_MAX;
    Move bestMove;
    bool firstMove = true;
    
    for (const Move& move : moves) {
        // Execute move
        Piece capturedPiece = board_.getPiece(move.to);
        Piece movingPiece = board_.getPiece(move.from);
        board_.setPiece(move.to, movingPiece);
        board_.setPiece(move.from, Piece());
        
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        board_.setCurrentPlayer(opponent);
        
        int eval;
        if (firstMove) {
            // First move gets full window search
            eval = -principalVariationSearch(depth - 1, -beta, -alpha, opponent, isPVNode);
            firstMove = false;
        } else {
            // Subsequent moves get null-window search
            eval = -principalVariationSearch(depth - 1, -alpha - 1, -alpha, opponent, false);
            
            // If the null-window search suggests improvement, do full re-search
            if (eval > alpha && eval < beta) {
                eval = -principalVariationSearch(depth - 1, -beta, -alpha, opponent, isPVNode);
            }
        }
        
        // Restore board
        board_.setPiece(move.from, movingPiece);
        board_.setPiece(move.to, capturedPiece);
        board_.setCurrentPlayer(maximizingPlayer);
        
        // Update best value and bounds
        if (maximizingPlayer == Color::WHITE) {
            if (eval > bestValue) {
                bestValue = eval;
                bestMove = move;
                if (eval > alpha) {
                    alpha = eval;
                    if (eval >= beta) {
                        // Beta cutoff - add killer move
                        addKillerMove(move, depth);
                        break;
                    }
                }
            }
        } else {
            if (eval < bestValue) {
                bestValue = eval;
                bestMove = move;
                if (eval < beta) {
                    beta = eval;
                    if (eval <= alpha) {
                        // Alpha cutoff - add killer move
                        addKillerMove(move, depth);
                        break;
                    }
                }
            }
        }
    }
    
    // Store in transposition table
    char flag = 'E'; // Exact
    if (bestValue <= alpha) flag = 'U'; // Upper bound
    if (bestValue >= beta) flag = 'L';  // Lower bound
    
    storeInTT(hash, depth, bestValue, bestMove, flag);
    
    return bestValue;
}