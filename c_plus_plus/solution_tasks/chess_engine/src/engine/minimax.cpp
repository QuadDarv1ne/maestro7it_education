#include "../../include/minimax.hpp"
#include "../../include/board.hpp"
#include <algorithm>
#include <climits>
#include <random>
#include <functional>
#include <iostream>

Minimax::Minimax(Board& board, int maxDepth) 
    : board_(board), evaluator_(board), openingBook_(), maxDepth_(maxDepth), 
      timeLimit_(std::chrono::seconds(10)), interrupted_(false),
      transpositionTable(HASH_TABLE_SIZE), killerMoves(MAX_PLY, std::vector<Move>(MAX_KILLER_MOVES)), 
      historyTable(HISTORY_SIZE, 0) {
    initZobrist();
    // Инициализация таблицы транспозиций
    for(size_t i = 0; i < HASH_TABLE_SIZE; ++i) {
        transpositionTable[i] = TTEntry();
    }
    
    // Инициализация killer moves
    for (int ply = 0; ply < MAX_PLY; ply++) {
        for (int k = 0; k < MAX_KILLER_MOVES; k++) {
            killerMoves[ply][k] = Move();
        }
    }
    
    // Инициализация таблицы истории
    for (int i = 0; i < HISTORY_SIZE; i++) {
        historyTable[i] = 0;
    }
}

Move Minimax::findBestMove(Color color) {
    Move bestMove;
    int bestValue = (color == Color::WHITE) ? INT_MIN : INT_MAX;
    startTime_ = std::chrono::steady_clock::now();
    resetInterrupt();
    
    // Проверка книги дебютов
    // ... (код книги дебютов оставляем как есть) ...
    
    // Итеративное углубление
    for (int depth = 1; depth <= maxDepth_; depth++) {
        // Проверяем время и флаг прерывания перед новой глубиной
        if (shouldStop()) {
            break;
        }

        std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
        if (moves.empty()) break;

        Move currentBestMove;
        int currentBestValue = (color == Color::WHITE) ? INT_MIN : INT_MAX;

        for (const Move& move : moves) {
            // Проверка времени и флага прерывания внутри цикла по ходам
            if (shouldStop()) break;

            // Выполняем ход
            board_.makeMove(move);
            
            // Поиск (используем PVS для лучшей производительности)
            int eval = -principalVariationSearch(depth - 1, -1000000, 1000000, (color == Color::WHITE ? Color::BLACK : Color::WHITE), true);
            
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
        }

        if (!shouldStop() || depth == 1) {
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
    startTime_ = startTime;
    resetInterrupt();
    if (shouldStop()) return evaluatePosition();
    return minimaxWithTT(depth, alpha, beta, maximizingPlayer);
}

void Minimax::setMaxDepth(int depth) {
    maxDepth_ = depth;
}

void Minimax::setTimeLimit(std::chrono::milliseconds limit) {
    timeLimit_ = limit;
}

void Minimax::interrupt() {
    interrupted_ = true;
}

void Minimax::resetInterrupt() {
    interrupted_ = false;
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
    int priority = 0;
    
    // 1. Превращение пешки (наивысший приоритет)
    if (move.promotion != PieceType::EMPTY) {
        priority += 10000;
        if (move.promotion == PieceType::QUEEN) {
            priority += 1000; // Бонус за превращение в ферзя
        }
    }
    
    // 2. MVV-LVA для взятий (Most Valuable Victim / Least Valuable Attacker)
    if (!capturedPiece.isEmpty()) {
        int victimValue = capturedPiece.getValue();
        int attackerValue = movingPiece.getValue();
        // MVV-LVA: взятие ценной фигуры дешевой фигурой получает высокий приоритет
        priority += 9000 + (victimValue * 10 - attackerValue);
    }
    
    // 3. Killer moves (тихие ходы, вызвавшие отсечение на этой глубине)
    if (isKillerMove(move, ply)) {
        priority += 8000;
    }
    
    // 4. История ходов (успешные ходы из других веток)
    int historyScore = getHistoryScore(move);
    if (historyScore > 0) {
        priority += 100 + std::min(historyScore / 10, 500); // Ограничиваем влияние истории
    }
    
    // 5. Позиционные эвристики
    // Развитие фигур в центр
    int toFile = board_.file(move.to);
    int toRank = board_.rank(move.to);
    bool isCentral = (toFile >= 2 && toFile <= 5) && (toRank >= 2 && toRank <= 5);
    bool isExtendedCenter = (toFile >= 1 && toFile <= 6) && (toRank >= 1 && toRank <= 6);
    
    if (movingPiece.getType() == PieceType::KNIGHT || 
        movingPiece.getType() == PieceType::BISHOP) {
        if (isCentral) {
            priority += 80;
        } else if (isExtendedCenter) {
            priority += 40;
        }
    }
    
    // 6. Продвижение пешек
    if (movingPiece.getType() == PieceType::PAWN) {
        int forwardDirection = (movingPiece.getColor() == Color::WHITE) ? 1 : -1;
        int rankProgress = (toRank - board_.rank(move.from)) * forwardDirection;
        if (rankProgress > 0) {
            priority += 50 + rankProgress * 20; // Бонус за продвижение
            // Дополнительный бонус для проходных пешек
            if (toRank == 6 || toRank == 1) {
                priority += 100; // Пешка близка к превращению
            }
        }
    }
    
    // 7. Рокировка (развитие короля в безопасность)
    if (move.isCastling) {
        priority += 60;
    }
    
    return priority;
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
    const int ASPIRATION_WINDOW = 50; // Размер окна вокруг предыдущей оценки
    
    int alpha = previousScore - ASPIRATION_WINDOW;
    int beta = previousScore + ASPIRATION_WINDOW;
    
    int score = minimaxWithTT(depth, alpha, beta, maximizingPlayer);
    
    // Если провал в верхнем или нижнем диапазоне, ищем с полным окном
    if (score <= alpha || score >= beta) {
        score = minimaxWithTT(depth, INT_MIN, INT_MAX, maximizingPlayer);
    }
    
    return score;
}

void Minimax::updateHistory(const Move& move, int depth) {
    // Не обновляем историю для взятий и превращений
    Piece capturedPiece = board_.getPiece(move.to);
    if (!capturedPiece.isEmpty() || move.promotion != PieceType::EMPTY) {
        return;
    }
    
    // Вычисляем индекс в таблице истории
    int index = move.from * 64 + move.to;
    if (index >= 0 && index < HISTORY_SIZE) {
        // Увеличиваем оценку истории, но предотвращаем переполнение
        historyTable[index] += depth * depth;
        if (historyTable[index] > 10000) {
            // Масштабируем все оценки истории, чтобы предотвратить переполнение
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
    // Константы futility pruning (в сотых пешки)
    static const int FUTILITY_MARGIN[] = {0, 100, 300, 500, 900};
    
    if (depth >= 4) return false; // Применяем только на малых глубинах
    if (depth <= 0 || depth >= 5) return false;
    
    // Проверяем, находится ли статическая оценка плюс маржа ниже alpha
    int margin = (depth < 5) ? FUTILITY_MARGIN[depth] : 900;
    return (staticEval + margin) <= alpha;
}

bool Minimax::isRazoringApplicable(int depth, int beta, int staticEval) const {
    // Константы razoring (в сотых пешки)
    static const int RAZOR_MARGIN[] = {0, 300, 400, 600, 800};
    
    if (depth >= 4) return false; // Применяем только на малых глубинах
    if (depth <= 0 || depth >= 5) return false;
    
    // Проверяем, находится ли статическая оценка минус маржа выше beta
    int margin = (depth < 5) ? RAZOR_MARGIN[depth] : 800;
    return (staticEval - margin) >= beta;
}

int Minimax::multiCutPruning(int depth, int alpha, int beta, Color maximizingPlayer, int cutNumber) {
    // Multi-cut pruning - попытка доказать несколько отсечений за один поиск
    if (depth <= 2 || cutNumber <= 0) {
        return minimaxWithTT(depth, alpha, beta, maximizingPlayer);
    }
    
    // Пытаемся найти несколько хороших ходов, которые вызовут beta cutoff
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    if (moves.empty()) {
        return evaluatePosition();
    }
    
    int bestValue = (maximizingPlayer == Color::WHITE) ? INT_MIN : INT_MAX;
    int cutsFound = 0;
    const int CUT_THRESHOLD = 2; // Количество отсечений для запуска multi-cut
    
    for (size_t i = 0; i < moves.size() && cutsFound < CUT_THRESHOLD; i++) {
        const Move& move = moves[i];
        
        // Выполняем ход
        Piece capturedPiece = board_.getPiece(move.to);
        Piece movingPiece = board_.getPiece(move.from);
        board_.setPiece(move.to, movingPiece);
        board_.setPiece(move.from, Piece());
        
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        board_.setCurrentPlayer(opponent);
        
        // Поиск с уменьшенной глубиной для проверки отсечений
        int reducedDepth = depth - 2;
        int eval = -minimaxWithTT(reducedDepth, -beta, -alpha, opponent);
        
        // Восстанавливаем доску
        board_.setPiece(move.from, movingPiece);
        board_.setPiece(move.to, capturedPiece);
        board_.setCurrentPlayer(maximizingPlayer);
        
        // Проверяем, вызывает ли этот ход отсечение
        if ((maximizingPlayer == Color::WHITE && eval >= beta) ||
            (maximizingPlayer == Color::BLACK && eval <= alpha)) {
            cutsFound++;
        }
        
        // Обновляем лучшее значение
        if (maximizingPlayer == Color::WHITE) {
            bestValue = std::max(bestValue, eval);
            alpha = std::max(alpha, eval);
        } else {
            bestValue = std::min(bestValue, eval);
            beta = std::min(beta, eval);
        }
        
        // Досрочное завершение, если нашли достаточно отсечений
        if (cutsFound >= CUT_THRESHOLD) {
            return bestValue;
        }
    }
    
    // Если не нашли достаточно отсечений, делаем обычный поиск
    return minimaxWithTT(depth, alpha, beta, maximizingPlayer);
}

int Minimax::evaluatePosition() const {
    return evaluator_.evaluate();
}

std::vector<Move> Minimax::orderCaptures(const std::vector<Move>& captures) const {
    std::vector<Move> orderedCaptures = captures;
    
    // Сортируем взятия по MVV-LVA (Наиболее ценная жертва - Наименее ценный атакующий)
    std::sort(orderedCaptures.begin(), orderedCaptures.end(), [this](const Move& a, const Move& b) {
        Piece victimA = board_.getPiece(a.to);
        Piece attackerA = board_.getPiece(a.from);
        Piece victimB = board_.getPiece(b.to);
        Piece attackerB = board_.getPiece(b.from);
        
        // MVV-LVA оценка: большее значение для более ценных жертв и менее ценных атакующих
        int scoreA = victimA.getValue() * 10 - attackerA.getValue();
        int scoreB = victimB.getValue() * 10 - attackerB.getValue();
        
        return scoreA > scoreB;
    });
    
    return orderedCaptures;
}

int Minimax::quiescenceSearch(int alpha, int beta, Color maximizingPlayer, int ply) {
    // Статическая оценка позиции
    int standPat = evaluatePosition();
    
    // Beta отсечение
    if (standPat >= beta) {
        return beta;
    }
    
    // Обновление alpha
    if (standPat > alpha) {
        alpha = standPat;
    }
    
    // Генерируем только взятия и легальные ходы (упрощенно - генерируем все легальные ходы и фильтруем взятия)
    MoveGenerator generator(board_);
    std::vector<Move> allMoves = generator.generateLegalMoves();
    
    // Фильтруем только взятия
    std::vector<Move> tacticalMoves;
    for (const Move& move : allMoves) {
        if (move.isCapture || isInCheck(maximizingPlayer)) {
            tacticalMoves.push_back(move);
        }
    }
    
    // Упорядочиваем тактические ходы
    tacticalMoves = orderCaptures(tacticalMoves);
    
    // Ограничиваем глубину quiescence search для предотвращения взрыва
    const int MAX_QUIESCENCE_DEPTH = 8;
    if (ply >= MAX_QUIESCENCE_DEPTH) {
        return standPat;
    }
    
    int bestValue = standPat;
    
    for (const Move& move : tacticalMoves) {
        // Delta pruning - если выгода от взятия + позиционный бонус не превосходит alpha, пропускаем
        Piece captured = board_.getPiece(move.to);
        if (!captured.isEmpty()) {
            int delta = captured.getValue() + 200; // Позиционный бонус
            if (standPat + delta < alpha) {
                continue; // Пропускаем это взятие
            }
        }
        
        // Выполняем ход
        board_.makeMove(move);
        
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        
        // Рекурсивный quiescence search
        int score = -quiescenceSearch(-beta, -alpha, opponent, ply + 1);
        
        // Восстанавливаем доску
        board_.undoMove();
        
        // Обновляем лучшее значение и границы
        if (score > bestValue) {
            bestValue = score;
            if (score > alpha) {
                alpha = score;
                if (score >= beta) {
                    break; // Beta отсечение
                }
            }
        }
    }
    
    return bestValue;
}

bool Minimax::probCut(int depth, int beta, Color maximizingPlayer, int threshold) {
    // ProbCut - вероятностное отсечение на основе поверхностного поиска
    if (depth < 3) return false; // Применяем только при достаточной глубине
    
    // Выполняем поверхностный поиск с уменьшенной глубиной
    int shallowDepth = depth - 2;
    int shallowBeta = beta - threshold;
    
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    if (moves.empty()) return false;
    
    // Тестируем несколько лучших ходов с поверхностным поиском
    int testMoves = std::min(3, static_cast<int>(moves.size()));
    
    for (int i = 0; i < testMoves; i++) {
        const Move& move = moves[i];
        
        // Выполняем ход
        board_.makeMove(move);
        
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        
        // Поверхностный поиск
        int shallowScore = -minimaxWithTT(shallowDepth, -shallowBeta - 1, -shallowBeta, opponent);
        
        // Восстанавливаем доску
        board_.undoMove();
        
        // Если поверхностный поиск превышает порог, вероятно вызовет отсечение
        if (shallowScore >= shallowBeta) {
            // Выполняем проверочный поиск на полной глубине
            int verifyScore = -minimaxWithTT(depth - 1, -beta - 1, -beta, opponent);
            
            if (verifyScore >= beta) {
                return true; // Вероятностное отсечение подтверждено
            }
        }
    }
    
    return false; // Не удалось предсказать отсечение
}

int Minimax::calculateExtension(const Move& move, Color maximizingPlayer, int depth) const {
    int extension = 0;
    
    // Расширения для шахов
    if (isInCheck(maximizingPlayer)) {
        extension += 1; // Расширение на 1 полуход для позиций с шахом
    }
    
    // Расширения для взятий
    Piece capturedPiece = board_.getPiece(move.to);
    if (!capturedPiece.isEmpty()) {
        // Расширяем для взятия ценных фигур
        if (capturedPiece.getValue() >= 500) { // Ферзь или ладья
            extension += 1;
        } else if (capturedPiece.getValue() >= 300) { // Слон или конь
            extension += 0; // Нет расширения для легких фигур
        }
    }
    
    // Расширения для превращений
    if (move.promotion != PieceType::EMPTY) {
        extension += 1; // Расширяем для превращений
    }
    
    // Расширения для продвижения пешек близко к превращению
    Piece movingPiece = board_.getPiece(move.from);
    if (movingPiece.getType() == PieceType::PAWN) {
        int toRank = board_.rank(move.to);
        if ((movingPiece.getColor() == Color::WHITE && toRank >= 6) ||
            (movingPiece.getColor() == Color::BLACK && toRank <= 1)) {
            extension += 1; // Расширяем продвижение пешек на 7-ю/2-ю горизонталь
        }
    }
    
    // Ограничиваем общее расширение
    return std::min(extension, 2); // Максимум 2 полухода расширения
}

bool Minimax::isCriticalPosition() const {
    // Позиция является критической, если:
    // 1. Король под шахом
    // 2. Материальный баланс близок (в пределах 200 сотых пешки)
    // 3. Позиция имеет тактические угрозы
    
    Color currentPlayer = board_.getCurrentPlayer();
    if (isInCheck(currentPlayer)) {
        return true;
    }
    
    // Проверяем материальный баланс
    int materialEval = evaluatePosition(); // Используем общую функцию оценки
    if (std::abs(materialEval) <= 200) {
        return true; // Близкая игра
    }
    
    // TODO: Добавить более сложное определение критических позиций
    // - Поиск висящих фигур
    // - Проверка тактических мотивов
    // - Анализ напряжения пешечной структуры
    
    return false;
}

bool Minimax::isTimeUp() const {
    auto now = std::chrono::steady_clock::now();
    auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(now - startTime_);
    return elapsed >= timeLimit_;
}

bool Minimax::shouldStop() const {
    return interrupted_ || isTimeUp();
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

// Простая хеш-функция для позиций на доске
void Minimax::initZobrist() {
    std::mt19937_64 rng(123456789); // Фиксированное зерно для воспроизводимости
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
    return board_.getZobristHash();
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
    if (shouldStop()) return evaluatePosition();
    
    // Проверка на ничью (повторение или правило 50 ходов)
    if (board_.getHalfMoveClock() >= 100 || board_.isRepetition()) {
        return 0;
    }

    // Проверяем таблицу транспозиций
    uint64_t hash = hashPosition();
    TTEntry* entry = probeTT(hash);
    
    if (entry && entry->depth >= depth) {
        if (entry->flag == 'E') { // Точное значение
            return entry->score;
        } else if (entry->flag == 'L' && entry->score >= beta) { // Нижняя граница
            return entry->score;
        } else if (entry->flag == 'U' && entry->score <= alpha) { // Верхняя граница
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
        // Делаем пустой ход (передаем ход)
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        board_.setCurrentPlayer(opponent);
        
        int nullScore = -minimaxWithTT(depth - 1 - 2, -beta, -beta + 1, opponent);
        
        // Восстанавливаем сторону
        board_.setCurrentPlayer(maximizingPlayer);
        
        if (nullScore >= beta) {
            return beta; // Отсекаем поддерево
        }
    }
    
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    
    if (moves.empty()) {
        if (isInCheck(maximizingPlayer)) {
            return (maximizingPlayer == Color::WHITE) ? (-20000 - depth) : (20000 + depth);
        } else {
            return 0; // Пат
        }
    }
    
    int bestScore;
    Move bestMove;
    bool hasBestMove = false;
    
    if (maximizingPlayer == Color::WHITE) {
        int maxValue = INT_MIN;
        for (size_t i = 0; i < moves.size(); i++) {
            if (shouldStop()) break;
            const Move& move = moves[i];
            
            // Выполняем ход
            board_.makeMove(move);
            
            int reduction = (i >= 4 && depth >= 3) ? 1 : 0; // Редукция поздних ходов
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
            if (shouldStop()) break;
            const Move& move = moves[i];
            
            // Выполняем ход
            board_.makeMove(move);
            
            int reduction = (i >= 4 && depth >= 3) ? 1 : 0; // Редукция поздних ходов
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
    
    // Сохраняем результат в таблице транспозиций
    char flag;
    if (bestScore <= alpha) {
        flag = 'U'; // Верхняя граница
    } else if (bestScore >= beta) {
        flag = 'L'; // Нижняя граница
    } else {
        flag = 'E'; // Точное значение
    }
    
    storeInTT(hash, depth, bestScore, hasBestMove ? bestMove : Move(), flag);
    
    return bestScore;
}

int Minimax::principalVariationSearch(int depth, int alpha, int beta, Color maximizingPlayer, bool isPVNode) {
    if (shouldStop()) return evaluatePosition();
    
    // Проверка на ничью
    if (board_.getHalfMoveClock() >= 100 || board_.isRepetition()) {
        return 0;
    }

    // Базовый случай: листовой узел
    if (depth <= 0) {
        return quiescenceSearch(alpha, beta, maximizingPlayer);
    }
    
    // Проверяем таблицу транспозиций
    uint64_t hash = hashPosition();
    TTEntry* entry = probeTT(hash);
    
    if (entry && entry->depth >= depth) {
        if (entry->flag == 'E') return entry->score; // Точная оценка
        if (entry->flag == 'L' && entry->score >= beta) return beta; // Нижняя граница
        if (entry->flag == 'U' && entry->score <= alpha) return alpha; // Верхняя граница
    }
    
    std::vector<Move> moves = orderMoves(MoveGenerator(board_).generateLegalMoves());
    if (moves.empty()) {
        return evaluatePosition();
    }
    
    int bestValue = (maximizingPlayer == Color::WHITE) ? INT_MIN : INT_MAX;
    Move bestMove;
    bool firstMove = true;
    
    for (const Move& move : moves) {
        if (shouldStop()) break;
        // Выполняем ход
        board_.makeMove(move);
        
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        
        int eval;
        if (firstMove) {
            // Первый ход получает поиск с полным окном
            eval = -principalVariationSearch(depth - 1, -beta, -alpha, opponent, isPVNode);
            firstMove = false;
        } else {
            // Последующие ходы получают поиск с нулевым окном
            eval = -principalVariationSearch(depth - 1, -alpha - 1, -alpha, opponent, false);
            
            // Если поиск с нулевым окном указывает на улучшение, делаем полный перепоиск
            if (eval > alpha && eval < beta) {
                eval = -principalVariationSearch(depth - 1, -beta, -alpha, opponent, isPVNode);
            }
        }
        
        // Восстанавливаем доску
        board_.undoMove();
        
        // Обновляем лучшее значение и границы
        if (maximizingPlayer == Color::WHITE) {
            if (eval > bestValue) {
                bestValue = eval;
                bestMove = move;
                if (eval > alpha) {
                    alpha = eval;
                    if (eval >= beta) {
                        // Beta отсечение - добавляем killer move
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
                        // Alpha отсечение - добавляем killer move
                        addKillerMove(move, depth);
                        break;
                    }
                }
            }
        }
    }
    
    // Сохраняем в таблице транспозиций
    char flag = 'E'; // Точное значение
    if (bestValue <= alpha) flag = 'U'; // Верхняя граница
    if (bestValue >= beta) flag = 'L';  // Нижняя граница
    
    storeInTT(hash, depth, bestValue, bestMove, flag);
    
    return bestValue;
}