#ifndef MOVE_ORDERING_HPP
#define MOVE_ORDERING_HPP

#include <vector>
#include <algorithm>
#include <unordered_map>

/**
 * @brief Система упорядочивания ходов для улучшения поиска
 * 
 * Реализует различные эвристики для упорядочивания ходов
 * с целью ускорения альфа-бета отсечений.
 */
class MoveOrdering {
private:
    // История хороших ходов
    std::unordered_map<uint64_t, int> history_table_;
    
    // Killer ходы (хорошие ходы на определенной глубине)
    std::vector<std::vector<std::string>> killer_moves_;
    
    // MVV/LVA таблица (Most Valuable Victim / Least Valuable Attacker)
    std::unordered_map<std::string, int> mvv_lva_scores_;
    
    void initializeMVVLVA() {
        // Базовые значения для MVV/LVA
        mvv_lva_scores_["PxP"] = 100;  // Пешка берет пешку
        mvv_lva_scores_["NxP"] = 200;  // Конь берет пешку
        mvv_lva_scores_["BxP"] = 300;  // Слон берет пешку
        mvv_lva_scores_["RxP"] = 400;  // Ладья берет пешку
        mvv_lva_scores_["QxP"] = 500;  // Ферзь берет пешку
        mvv_lva_scores_["KxP"] = 600;  // Король берет пешку
        
        mvv_lva_scores_["PxN"] = 150;  // Пешка берет коня
        mvv_lva_scores_["NxN"] = 250;  // Конь берет коня
        // ... и так далее для всех комбинаций
    }
    
public:
    MoveOrdering(int max_depth = 64) : killer_moves_(max_depth) {
        initializeMVVLVA();
    }
    
    /**
     * @brief Оценить ход для упорядочивания
     * @param move Ход в алгебраической нотации
     * @param depth Текущая глубина поиска
     * @param is_capture Признак взятия
     * @param is_promotion Признак превращения
     * @return Оценка хода (чем выше, тем лучше)
     */
    int scoreMove(const std::string& move, int depth, 
                  bool is_capture = false, bool is_promotion = false) const {
        int score = 0;
        
        // 1. Ходы превращения пешек (очень хорошие)
        if (is_promotion) {
            score += 10000;
        }
        
        // 2. Взятия (MVV/LVA)
        if (is_capture) {
            auto it = mvv_lva_scores_.find(move);
            if (it != mvv_lva_scores_.end()) {
                score += it->second;
            } else {
                score += 500; // Базовая оценка взятия
            }
        }
        
        // 3. Killer ходы
        if (depth < static_cast<int>(killer_moves_.size())) {
            const auto& killers = killer_moves_[depth];
            if (std::find(killers.begin(), killers.end(), move) != killers.end()) {
                score += 8000;
            }
        }
        
        // 4. История ходов
        uint64_t move_hash = std::hash<std::string>{}(move);
        auto hist_it = history_table_.find(move_hash);
        if (hist_it != history_table_.end()) {
            score += hist_it->second;
        }
        
        // 5. Центральные ходы пешками (в начале игры)
        if (move.length() >= 4) {
            char from_file = move[0];
            char from_rank = move[1];
            char to_file = move[2];
            char to_rank = move[3];
            
            // Ходы в центр доски получают бонус
            if ((to_file >= 'c' && to_file <= 'f') && 
                (to_rank >= '3' && to_rank <= '6')) {
                score += 100;
            }
            
            // Ходы пешками вперед получают небольшой бонус
            if (from_file == to_file && 
                ((to_rank - from_rank == 1) || (from_rank - to_rank == 1))) {
                score += 50;
            }
        }
        
        return score;
    }
    
    /**
     * @brief Упорядочить ходы по убыванию оценки
     * @param moves Вектор ходов
     * @param depth Текущая глубина
     * @return Упорядоченный вектор ходов
     */
    std::vector<std::string> orderMoves(const std::vector<std::string>& moves, 
                                       int depth) const {
        std::vector<std::pair<int, std::string>> scored_moves;
        
        for (const auto& move : moves) {
            bool is_capture = (move.find('x') != std::string::npos);
            bool is_promotion = (move.find('=') != std::string::npos);
            int score = scoreMove(move, depth, is_capture, is_promotion);
            scored_moves.emplace_back(score, move);
        }
        
        // Сортировка по убыванию оценки
        std::sort(scored_moves.begin(), scored_moves.end(),
                 [](const auto& a, const auto& b) {
                     return a.first > b.first;
                 });
        
        // Извлечение ходов
        std::vector<std::string> ordered_moves;
        ordered_moves.reserve(moves.size());
        for (const auto& pair : scored_moves) {
            ordered_moves.push_back(pair.second);
        }
        
        return ordered_moves;
    }
    
    /**
     * @brief Добавить хороший ход в историю
     * @param move Ход
     * @param depth Глубина
     * @param bonus Бонус к истории
     */
    void addGoodMove(const std::string& move, int depth, int bonus = 1) {
        uint64_t move_hash = std::hash<std::string>{}(move);
        history_table_[move_hash] += bonus;
        
        // Ограничиваем значения истории
        if (history_table_[move_hash] > 10000) {
            history_table_[move_hash] = 10000;
        }
    }
    
    /**
     * @brief Добавить killer ход
     * @param move Ход
     * @param depth Глубина
     */
    void addKillerMove(const std::string& move, int depth) {
        if (depth >= static_cast<int>(killer_moves_.size())) {
            return;
        }
        
        auto& killers = killer_moves_[depth];
        if (std::find(killers.begin(), killers.end(), move) == killers.end()) {
            if (killers.size() < 2) {
                killers.push_back(move);
            } else {
                // Заменяем самый старый killer ход
                killers[0] = move;
            }
        }
    }
    
    /**
     * @brief Очистить таблицы истории
     */
    void clearHistory() {
        history_table_.clear();
        for (auto& killers : killer_moves_) {
            killers.clear();
        }
    }
    
    /**
     * @brief Получить размер таблицы истории
     * @return Количество записей в истории
     */
    size_t getHistorySize() const {
        return history_table_.size();
    }
};

#endif // MOVE_ORDERING_HPP