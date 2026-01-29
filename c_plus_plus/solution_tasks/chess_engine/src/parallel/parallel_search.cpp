#include "../include/parallel_search.hpp"
#include <iostream>
#include <algorithm>
#include <numeric>

// Определение констант
namespace ParallelConstants {
    const int MIN_SPLIT_DEPTH = 3;
    const int MAX_THREADS = 64;
    const int THREAD_STACK_SIZE = 8192 * 1024; // 8MB
    const int ASPIRATION_WINDOW = 50;
}

ParallelChessEngine::ParallelChessEngine(int numThreads) 
    : evaluator_(board_), maxDepth_(6), numThreads_(numThreads), 
      timeLimit_(std::chrono::milliseconds(10000)),
      stopSearch_(false), bestScore_(0), searchDepth_(0) {
    
    // Инициализация транспозиционной таблицы
    transpositionTable_.resize(TRANSPOSITION_TABLE_SIZE);
    std::fill(transpositionTable_.begin(), transpositionTable_.end(), TranspositionEntry());
    
    // Инициализация таблицы истории
    historyTable_.resize(HISTORY_SIZE, 0);
    
    // Установка начальной позиции
    board_.setupStartPosition();
}

ParallelChessEngine::~ParallelChessEngine() {
    stopAllThreads();
}

Move ParallelChessEngine::findBestMove(Color color, std::chrono::milliseconds timeLimit) {
    setTimeLimit(timeLimit);
    
    // Сброс состояния поиска
    stopSearch_.store(false);
    bestScore_.store(0);
    searchDepth_.store(0);
    
    std::cout << "Начало параллельного поиска с " << numThreads_ << " потоками" << std::endl;
    
    // Создание потоков
    std::vector<std::thread> threads;
    std::vector<std::promise<Move>> promises(numThreads_);
    
    auto startTime = std::chrono::steady_clock::now();
    
    // Запуск рабочих потоков
    for (int i = 0; i < numThreads_; i++) {
        threads.emplace_back([this, i, color, &promises]() {
            try {
                workerThread(i, color);
                promises[i].set_value(bestMove_.load());
            } catch (const std::exception& e) {
                promises[i].set_exception(std::current_exception());
            }
        });
    }
    
    // Ожидание завершения или истечения времени
    std::future_status status;
    do {
        status = std::async(std::launch::async, [this, startTime]() {
            auto elapsed = std::chrono::steady_clock::now() - startTime;
            return elapsed >= timeLimit_;
        }).wait_for(std::chrono::milliseconds(100));
        
        if (status == std::future_status::ready) {
            stopSearch_.store(true);
            break;
        }
    } while (status != std::future_status::ready);
    
    // Сбор результатов
    Move bestMove;
    int bestThread = -1;
    int bestThreadScore = INT_MIN;
    
    for (int i = 0; i < numThreads_; i++) {
        try {
            Move threadMove = promises[i].get_future().get();
            if (i == 0) { // Основной поток
                bestMove = threadMove;
                bestThread = 0;
                bestThreadScore = bestScore_.load();
            }
        } catch (const std::exception& e) {
            std::cerr << "Ошибка в потоке " << i << ": " << e.what() << std::endl;
        }
    }
    
    // Остановка всех потоков
    stopAllThreads();
    
    // Ожидание завершения потоков
    for (auto& thread : threads) {
        if (thread.joinable()) {
            thread.join();
        }
    }
    
    auto endTime = std::chrono::steady_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime);
    
    std::cout << "Параллельный поиск завершен за " << duration.count() << " мс" << std::endl;
    std::cout << "Лучший ход: " << board_.squareToAlgebraic(bestMove.from) 
              << "-" << board_.squareToAlgebraic(bestMove.to) << std::endl;
    std::cout << "Оценка позиции: " << bestScore_.load() << std::endl;
    
    return bestMove;
}

void ParallelChessEngine::workerThread(int threadId, Color color) {
    std::cout << "Поток " << threadId << " запущен" << std::endl;
    
    // Генерация ходов
    std::vector<Move> moves = generateLegalMoves();
    if (moves.empty()) return;
    
    // Упорядочивание ходов для лучшего распределения
    moves = orderMoves(moves, 0);
    
    int alpha = INT_MIN;
    int beta = INT_MAX;
    int localBestScore = INT_MIN;
    Move localBestMove = moves[0];
    
    // Итеративное углубление
    for (int depth = 1; depth <= maxDepth_ && !shouldStop(); depth++) {
        searchDepth_.store(depth);
        
        for (size_t i = 0; i < moves.size() && !shouldStop(); i++) {
            const Move& move = moves[i];
            
            // Выполнение хода
            Piece capturedPiece = board_.getPiece(move.to);
            Piece movingPiece = board_.getPiece(move.from);
            board_.setPiece(move.to, movingPiece);
            board_.setPiece(move.from, Piece());
            
            Color opponent = (color == Color::WHITE) ? Color::BLACK : Color::WHITE;
            board_.setSideToMove(opponent);
            
            // Поиск минимаксом
            int score = -parallelMinimax(depth - 1, -beta, -alpha, opponent, threadId);
            
            // Восстановление позиции
            board_.setPiece(move.from, movingPiece);
            board_.setPiece(move.to, capturedPiece);
            board_.setSideToMove(color);
            
            // Обновление лучшего результата
            if (score > localBestScore) {
                localBestScore = score;
                localBestMove = move;
                
                if (score > alpha) {
                    alpha = score;
                }
                
                // Обновление глобального лучшего результата
                if (threadId == 0) { // Только основной поток обновляет глобальные значения
                    int currentBest = bestScore_.load();
                    if (score > currentBest) {
                        bestScore_.store(score);
                        bestMove_.store(move);
                    }
                }
            }
            
            if (shouldStop()) break;
        }
    }
    
    std::cout << "Поток " << threadId << " завершен. Лучший результат: " << localBestScore << std::endl;
}

int ParallelChessEngine::parallelMinimax(int depth, int alpha, int beta, Color maximizingPlayer, int threadId) {
    if (depth == 0 || shouldStop()) {
        return evaluatePosition();
    }
    
    // Проверка транспозиционной таблицы
    uint64_t hash = hashPosition();
    TranspositionEntry* entry = probeTT(hash, threadId);
    
    if (entry && entry->depth >= depth) {
        if (entry->flag == 'E') return entry->score;
        if (entry->flag == 'L' && entry->score >= beta) return beta;
        if (entry->flag == 'U' && entry->score <= alpha) return alpha;
    }
    
    std::vector<Move> moves = generateLegalMoves();
    if (moves.empty()) {
        return evaluatePosition();
    }
    
    moves = orderMoves(moves, maxDepth_ - depth);
    
    int bestValue = (maximizingPlayer == Color::WHITE) ? INT_MIN : INT_MAX;
    Move bestMove;
    
    for (const Move& move : moves) {
        if (shouldStop()) break;
        
        // Выполнение хода
        Piece capturedPiece = board_.getPiece(move.to);
        Piece movingPiece = board_.getPiece(move.from);
        board_.setPiece(move.to, movingPiece);
        board_.setPiece(move.from, Piece());
        
        Color opponent = (maximizingPlayer == Color::WHITE) ? Color::BLACK : Color::WHITE;
        board_.setSideToMove(opponent);
        
        int value = -parallelMinimax(depth - 1, -beta, -alpha, opponent, threadId);
        
        // Восстановление позиции
        board_.setPiece(move.from, movingPiece);
        board_.setPiece(move.to, capturedPiece);
        board_.setSideToMove(maximizingPlayer);
        
        if (maximizingPlayer == Color::WHITE) {
            if (value > bestValue) {
                bestValue = value;
                bestMove = move;
                alpha = std::max(alpha, value);
                if (alpha >= beta) break;
            }
        } else {
            if (value < bestValue) {
                bestValue = value;
                bestMove = move;
                beta = std::min(beta, value);
                if (beta <= alpha) break;
            }
        }
    }
    
    // Сохранение в транспозиционную таблицу
    char flag = 'E';
    if (bestValue <= alpha) flag = 'U';
    if (bestValue >= beta) flag = 'L';
    
    storeInTT(hash, depth, bestValue, bestMove, flag, threadId);
    
    return bestValue;
}

// Вспомогательные функции
std::vector<Move> ParallelChessEngine::orderMoves(const std::vector<Move>& moves, int ply) const {
    std::vector<Move> orderedMoves = moves;
    
    std::sort(orderedMoves.begin(), orderedMoves.end(), 
              [this, ply](const Move& a, const Move& b) {
                  return getMovePriority(a, ply) > getMovePriority(b, ply);
              });
    
    return orderedMoves;
}

int ParallelChessEngine::getMovePriority(const Move& move, int ply) const {
    Piece capturedPiece = board_.getPiece(move.to);
    Piece movingPiece = board_.getPiece(move.from);
    
    // Приоритет взятий (MVV-LVA)
    if (!capturedPiece.isEmpty()) {
        return 10000 + capturedPiece.getValue() * 10 - movingPiece.getValue();
    }
    
    // Приоритет истории
    int historyScore = getHistoryScore(move);
    if (historyScore > 0) {
        return 1000 + historyScore;
    }
    
    // Приоритет продвижения пешек
    if (movingPiece.getType() == PieceType::PAWN) {
        int rankDiff = (movingPiece.getColor() == Color::WHITE) ? 
                      (board_.rank(move.to) - board_.rank(move.from)) : 
                      (board_.rank(move.from) - board_.rank(move.to));
        if (rankDiff > 0) {
            return 500 + rankDiff * 50;
        }
    }
    
    return movingPiece.getValue();
}

void ParallelChessEngine::storeInTT(uint64_t hash, int depth, int score, Move bestMove, char flag, int threadId) {
    // Простая реализация без блокировок для демонстрации
    size_t index = hash % TRANSPOSITION_TABLE_SIZE;
    transpositionTable_[index] = TranspositionEntry(hash, depth, score, bestMove, flag);
}

ParallelChessEngine::TranspositionEntry* ParallelChessEngine::probeTT(uint64_t hash, int threadId) {
    size_t index = hash % TRANSPOSITION_TABLE_SIZE;
    if (transpositionTable_[index].hash == hash) {
        return &transpositionTable_[index];
    }
    return nullptr;
}

// Геттеры и сеттеры
void ParallelChessEngine::setMaxDepth(int depth) {
    maxDepth_ = depth;
}

void ParallelChessEngine::setNumThreads(int threads) {
    numThreads_ = std::min(threads, ParallelConstants::MAX_THREADS);
}

void ParallelChessEngine::setTimeLimit(std::chrono::milliseconds limit) {
    timeLimit_ = limit;
}

void ParallelChessEngine::stopAllThreads() {
    stopSearch_.store(true);
}

// Утилиты
namespace ParallelUtils {
    int getOptimalThreadCount() {
        unsigned int hwThreads = std::thread::hardware_concurrency();
        return hwThreads > 0 ? std::min(hwThreads, static_cast<unsigned int>(ParallelConstants::MAX_THREADS)) : 4;
    }
    
    void distributeWork(const std::vector<Move>& moves, int numThreads, 
                       std::vector<std::vector<Move>>& threadWork) {
        threadWork.resize(numThreads);
        int movesPerThread = moves.size() / numThreads;
        int remainder = moves.size() % numThreads;
        
        int moveIndex = 0;
        for (int i = 0; i < numThreads; i++) {
            int threadMoves = movesPerThread + (i < remainder ? 1 : 0);
            threadWork[i].reserve(threadMoves);
            
            for (int j = 0; j < threadMoves && moveIndex < static_cast<int>(moves.size()); j++) {
                threadWork[i].push_back(moves[moveIndex++]);
            }
        }
    }
}