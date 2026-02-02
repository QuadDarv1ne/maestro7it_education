#ifndef ADVANCED_AI_HPP
#define ADVANCED_AI_HPP

#include "board.hpp"
#include "minimax.hpp"
#include "position_evaluator.hpp"
#include <vector>
#include <map>
#include <memory>
#include <chrono>
#include <cstdint>
#include <unordered_map>

/**
 * @brief Класс, реализующий продвинутый искусственный интеллект для шахмат
 * 
 * Включает в себя:
 * - Многопоточный поиск
 * - Современные эвристики
 * - Открытую библиотеку дебютов
 * - Эндшпильные таблицы
 */
class AdvancedAI {
private:
    Board& board_;
    int searchDepth_;
    PositionEvaluator evaluator_;
    
    // Таблица транспозиций для оптимизации поиска
    struct TTEntry {
        uint64_t zobristHash;
        int score;
        int depth;
        Move bestMove;
        char flag; // 'EXACT', 'LOWER', 'UPPER'
        
        TTEntry() : zobristHash(0), score(0), depth(0), flag(0) {}
    };
    
    static const size_t TTBucketSize = 1000000; // 1 миллион позиций
    std::vector<TTEntry> transpositionTable;
    
    // Открытая библиотека дебютов
    std::vector<std::vector<Move>> openingBook;
    
    // Статистика поиска
    struct SearchStats {
        uint64_t nodesSearched;
        uint64_t ttHits;
        uint64_t ttMisses;
        double searchTime;
        
        SearchStats() : nodesSearched(0), ttHits(0), ttMisses(0), searchTime(0.0) {}
    } stats_;
    
public:
    /**
     * @brief Конструктор продвинутого ИИ
     * @param board Ссылка на игровую доску
     * @param searchDepth Глубина поиска
     */
    AdvancedAI(Board& board, int searchDepth = 6);
    
    /**
     * @brief Найти лучший ход для текущего игрока
     * @param playerColor Цвет игрока, для которого ищется ход
     * @return Лучший ход
     */
    Move findBestMove(Color playerColor);
    
    /**
     * @brief Найти лучший ход с ограничением по времени
     * @param playerColor Цвет игрока
     * @param timeLimitMs Ограничение по времени в миллисекундах
     * @return Лучший ход
     */
    Move findBestMoveWithTimeLimit(Color playerColor, int timeLimitMs);
    
    /**
     * @brief Оценить текущую позицию
     * @param board Доска для оценки
     * @param maximizingPlayer Цвет игрока, максимизирующего оценку
     * @return Оценка позиции (в сантипешках)
     */
    int evaluatePosition(const Board& board, bool maximizingPlayer) const;
    
    /**
     * @brief Получить статистику поиска
     * @return Статистика последнего поиска
     */
    const SearchStats& getSearchStats() const { return stats_; }
    
    /**
     * @brief Сбросить статистику поиска
     */
    void resetStats();
    
    /**
     * @brief Проверить, есть ли позиция в таблице транспозиций
     * @param zobristHash Хэш позиции
     * @param depth Глубина поиска
     * @param alpha Альфа-значение
     * @param beta Бета-значение
     * @return true, если позиция найдена и результат может быть использован
     */
    bool probeTranspositionTable(uint64_t zobristHash, int depth, int alpha, int beta, int& score, Move& bestMove) const;
    
    /**
     * @brief Сохранить позицию в таблицу транспозиций
     * @param zobristHash Хэш позиции
     * @param depth Глубина поиска
     * @param score Оценка позиции
     * @param bestMove Лучший ход
     * @param flag Флаг типа оценки
     */
    void storeInTranspositionTable(uint64_t zobristHash, int depth, int score, Move bestMove, char flag);
    
    /**
     * @brief Очистить таблицу транспозиций
     */
    void clearTranspositionTable();
    
    /**
     * @brief Проверить, есть ли ход в дебютной книге
     * @param board Текущая доска
     * @return Ход из дебютной книги или невалидный ход
     */
    Move getOpeningBookMove(const Board& board) const;
    
    /**
     * @brief Добавить ход в дебютную книгу
     * @param moves Последовательность ходов
     * @param weight Вес хода (чем больше, тем чаще выбирается)
     */
    void addToOpeningBook(const std::vector<Move>& moves, int weight = 1);
    
    /**
     * @brief Установить глубину поиска
     * @param depth Новая глубина поиска
     */
    void setSearchDepth(int depth) { searchDepth_ = depth; }
    
    /**
     * @brief Получить текущую глубину поиска
     * @return Глубина поиска
     */
    int getSearchDepth() const { return searchDepth_; }
};

#endif // ADVANCED_AI_HPP