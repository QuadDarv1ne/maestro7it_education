#ifndef ADVANCED_CHESS_ENGINE_HPP
#define ADVANCED_CHESS_ENGINE_HPP

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <random>
#include <chrono>

/**
 * @brief Продвинутый шахматный движок с оптимизациями
 * 
 * Реализует современные алгоритмы поиска и оценки позиции
 */
class AdvancedChessEngine {
private:
    // Таблица транспозиций для кэширования
    struct TTEntry {
        uint64_t hash_key;
        int score;
        int depth;
        int flag; // 0=exact, 1=lowerbound, 2=upperbound
        std::string best_move;
    };
    
    std::unordered_map<uint64_t, TTEntry> transposition_table_;
    
    // История хороших ходов
    std::unordered_map<std::string, int> history_table_;
    
    // Killer ходы
    std::vector<std::vector<std::string>> killer_moves_;
    
    // Генератор случайных чисел
    std::mt19937 rng_;
    
    // Параметры поиска
    int max_depth_;
    bool use_null_move_;
    int nodes_searched_;
    
public:
    AdvancedChessEngine() 
        : max_depth_(6)
        , use_null_move_(true)
        , nodes_searched_(0)
        , rng_(std::chrono::steady_clock::now().time_since_epoch().count()) {
        
        killer_moves_.resize(100); // Максимальная глубина 100
    }
    
    /**
     * @brief Поиск лучшего хода с помощью минимакса с альфа-бета отсечением
     * @param fen_position Текущая позиция в формате FEN
     * @param search_depth Глубина поиска
     * @return Лучший ход в шахматной нотации
     */
    std::string findBestMove(const std::string& fen_position, int search_depth = 6) {
        max_depth_ = search_depth;
        nodes_searched_ = 0;
        
        // Парсинг FEN позиции
        auto board_state = parseFEN(fen_position);
        
        // Итеративное углубление
        std::string best_move;
        int alpha = -1000000;
        int beta = 1000000;
        
        for (int depth = 1; depth <= max_depth_; ++depth) {
            int score = minimax(board_state, depth, alpha, beta, true);
            
            // Получение лучшего хода для этой глубины
            auto moves = generateLegalMoves(board_state);
            if (!moves.empty()) {
                best_move = orderMoves(moves)[0];
            }
            
            // Адаптивное окно поиска
            if (score <= alpha || score >= beta) {
                alpha = -1000000;
                beta = 1000000;
                score = minimax(board_state, depth, alpha, beta, true);
            } else {
                alpha = score - 50;
                beta = score + 50;
            }
        }
        
        return best_move;
    }
    
    /**
     * @brief Минимакс с альфа-бета отсечением
     */
    int minimax(const std::vector<std::string>& board_state, int depth, 
                int alpha, int beta, bool maximizing_player) {
        
        nodes_searched_++;
        
        // Проверка терминальных состояний
        if (depth == 0 || isGameOver(board_state)) {
            return evaluatePosition(board_state);
        }
        
        // Проверка таблицы транспозиций
        uint64_t hash_key = computeHash(board_state);
        auto it = transposition_table_.find(hash_key);
        if (it != transposition_table_.end() && it->second.depth >= depth) {
            if (it->second.flag == 0) return it->second.score; // exact
            if (it->second.flag == 1 && it->second.score >= beta) return beta; // lowerbound
            if (it->second.flag == 2 && it->second.score <= alpha) return alpha; // upperbound
        }
        
        // Null-move pruning
        if (use_null_move_ && depth >= 3 && !maximizing_player && 
            staticEvaluation(board_state) >= beta) {
            int null_score = -minimax(board_state, depth - 3, -beta, -beta + 1, !maximizing_player);
            if (null_score >= beta) {
                return beta;
            }
        }
        
        auto moves = generateLegalMoves(board_state);
        if (moves.empty()) {
            return isCheckmate(board_state, maximizing_player) ? -100000 : 0;
        }
        
        // Упорядочивание ходов
        moves = orderMoves(moves);
        
        std::string best_move;
        int best_score = maximizing_player ? -1000000 : 1000000;
        
        for (size_t i = 0; i < moves.size() && i < 40; ++i) { // Ограничение на 40 ходов
            auto new_state = makeMove(board_state, moves[i]);
            
            int score;
            if (i == 0) {
                // Полное окно для лучшего хода
                score = minimax(new_state, depth - 1, alpha, beta, !maximizing_player);
            } else {
                // NMP и LMR для остальных ходов
                int reduction = (i > 3 && depth > 2) ? 1 : 0;
                score = -minimax(new_state, depth - 1 - reduction, -alpha - 1, -alpha, !maximizing_player);
                
                if (score > alpha && score < beta) {
                    score = -minimax(new_state, depth - 1, -beta, -alpha, !maximizing_player);
                }
            }
            
            if (maximizing_player) {
                if (score > best_score) {
                    best_score = score;
                    best_move = moves[i];
                    if (score > alpha) alpha = score;
                }
            } else {
                if (score < best_score) {
                    best_score = score;
                    best_move = moves[i];
                    if (score < beta) beta = score;
                }
            }
            
            if (alpha >= beta) {
                // Обновление killer ходов и истории
                if (std::find(killer_moves_[depth].begin(), killer_moves_[depth].end(), moves[i]) 
                    == killer_moves_[depth].end()) {
                    killer_moves_[depth].push_back(moves[i]);
                    if (killer_moves_[depth].size() > 2) {
                        killer_moves_[depth].erase(killer_moves_[depth].begin());
                    }
                }
                history_table_[moves[i]] += depth * depth;
                break; // Beta cutoff
            }
        }
        
        // Сохранение в таблицу транспозиций
        int flag = 0; // exact
        if (best_score <= alpha) flag = 2; // upperbound
        if (best_score >= beta) flag = 1; // lowerbound
        
        transposition_table_[hash_key] = {hash_key, best_score, depth, flag, best_move};
        
        return best_score;
    }
    
    /**
     * @brief Упорядочивание ходов по приоритету
     */
    std::vector<std::string> orderMoves(const std::vector<std::string>& moves) {
        std::vector<std::pair<int, std::string>> scored_moves;
        
        for (const auto& move : moves) {
            int score = 0;
            
            // MVV/LVA эвристика (Most Valuable Victim / Least Valuable Attacker)
            if (isCapture(move)) {
                int victim_value = getPieceValue(getCapturedPiece(move));
                int attacker_value = getPieceValue(getMovingPiece(move));
                score += 10000 + victim_value - attacker_value;
            }
            
            // Killer ходы
            for (const auto& killers : killer_moves_) {
                if (std::find(killers.begin(), killers.end(), move) != killers.end()) {
                    score += 9000;
                }
            }
            
            // История ходов
            auto hist_it = history_table_.find(move);
            if (hist_it != history_table_.end()) {
                score += hist_it->second;
            }
            
            // Центральные ходы
            if (isCentralMove(move)) {
                score += 100;
            }
            
            scored_moves.push_back({score, move});
        }
        
        // Сортировка по убыванию
        std::sort(scored_moves.begin(), scored_moves.end(), 
                  [](const auto& a, const auto& b) { return a.first > b.first; });
        
        std::vector<std::string> ordered_moves;
        for (const auto& pair : scored_moves) {
            ordered_moves.push_back(pair.second);
        }
        
        return ordered_moves;
    }
    
    // Вспомогательные методы (заглушки для демонстрации)
    std::vector<std::string> parseFEN(const std::string& fen) {
        // Реализация парсинга FEN
        return {"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"};
    }
    
    std::vector<std::string> generateLegalMoves(const std::vector<std::string>& board_state) {
        // Реализация генерации_legalных ходов
        return {"e2e4", "d2d4", "g1f3", "b1c3"};
    }
    
    std::vector<std::string> makeMove(const std::vector<std::string>& board_state, 
                                      const std::string& move) {
        // Реализация выполнения хода
        return board_state;
    }
    
    int evaluatePosition(const std::vector<std::string>& board_state) {
        // Реализация оценки позиции
        return staticEvaluation(board_state) + positionalEvaluation(board_state);
    }
    
    int staticEvaluation(const std::vector<std::string>& board_state) {
        // Материальная оценка
        return 0;
    }
    
    int positionalEvaluation(const std::vector<std::string>& board_state) {
        // Позиционная оценка
        return 0;
    }
    
    bool isGameOver(const std::vector<std::string>& board_state) {
        return false;
    }
    
    bool isCheckmate(const std::vector<std::string>& board_state, bool white_to_move) {
        return false;
    }
    
    bool isCapture(const std::string& move) { return false; }
    char getCapturedPiece(const std::string& move) { return ' '; }
    char getMovingPiece(const std::string& move) { return ' '; }
    int getPieceValue(char piece) { return 0; }
    bool isCentralMove(const std::string& move) { return false; }
    
    uint64_t computeHash(const std::vector<std::string>& board_state) {
        // Zobrist хэширование
        return std::hash<std::string>{}(board_state[0]);
    }
    
    // Геттеры для статистики
    int getNodesSearched() const { return nodes_searched_; }
    size_t getTTSize() const { return transposition_table_.size(); }
    size_t getHistorySize() const { return history_table_.size(); }
};

#endif // ADVANCED_CHESS_ENGINE_HPP