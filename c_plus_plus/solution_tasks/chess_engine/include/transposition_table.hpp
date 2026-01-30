#ifndef TRANSPOSITION_TABLE_HPP
#define TRANSPOSITION_TABLE_HPP

#include <unordered_map>
#include <vector>
#include <cstdint>
#include <memory>

/**
 * @brief Транспозиционная таблица для кэширования позиций
 * 
 * Реализует эффективное кэширование уже вычисленных позиций
 * для избежания повторных вычислений в поиске.
 */
class TranspositionTable {
public:
    enum EntryType {
        EXACT,      // Точное значение
        LOWERBOUND, // Нижняя граница (альфа)
        UPPERBOUND  // Верхняя граница (бета)
    };
    
    struct TTEntry {
        uint64_t hash_key;      // Хэш позиции
        int depth;              // Глубина поиска
        int score;              // Оценка позиции
        EntryType entry_type;   // Тип записи
        uint32_t best_move;     // Лучший ход (упакованный)
        uint32_t age;           // Возраст записи
        
        TTEntry() : hash_key(0), depth(0), score(0), entry_type(EXACT), best_move(0), age(0) {}
        
        TTEntry(uint64_t key, int d, int s, EntryType type, uint32_t move, uint32_t a)
            : hash_key(key), depth(d), score(s), entry_type(type), best_move(move), age(a) {}
    };

private:
    std::vector<TTEntry> table_;
    size_t table_size_;
    uint32_t current_age_;
    mutable size_t hits_;
    mutable size_t misses_;
    mutable size_t collisions_;
    
    // Хэш-функция
    static uint64_t hashFunction(uint64_t key);
    
    // Управление размером таблицы
    void resize(size_t new_size);
    size_t getIndex(uint64_t hash_key) const;
    
    // Замещение записей
    bool shouldReplace(const TTEntry& existing, const TTEntry& new_entry) const;
    
public:
    // Конструкторы
    explicit TranspositionTable(size_t size_mb = 64);
    ~TranspositionTable() = default;
    
    // Основной функционал
    bool probe(uint64_t hash_key, int& score, int& depth, EntryType& type, uint32_t& best_move) const;
    void store(uint64_t hash_key, int depth, int score, EntryType type, uint32_t best_move);
    
    // Управление таблицей
    void clear();
    void incrementAge();
    void resizeMB(size_t size_mb);
    
    // Статистика
    size_t getHits() const { return hits_; }
    size_t getMisses() const { return misses_; }
    size_t getCollisions() const { return collisions_; }
    double getHitRate() const { return hits_ + misses_ > 0 ? static_cast<double>(hits_) / (hits_ + misses_) : 0.0; }
    size_t getSize() const { return table_size_; }
    size_t getUsedEntries() const;
    
    // Информация о таблице
    void printStatistics() const;
    std::string getStatsString() const;
};

// Утилиты для работы с ходами
namespace TTUtils {
    // Упаковка хода в 32 бита
    inline uint32_t packMove(int from, int to, int promotion = 0) {
        return (static_cast<uint32_t>(from) << 16) | 
               (static_cast<uint32_t>(to) << 8) | 
               static_cast<uint32_t>(promotion);
    }
    
    // Распаковка хода
    inline void unpackMove(uint32_t packed, int& from, int& to, int& promotion) {
        from = (packed >> 16) & 0xFF;
        to = (packed >> 8) & 0xFF;
        promotion = packed & 0xFF;
    }
    
    // Конвертация оценки в формат таблицы
    inline int16_t scoreToTT(int score, int ply) {
        if (score >= 90000) return static_cast<int16_t>(score + ply);
        if (score <= -90000) return static_cast<int16_t>(score - ply);
        return static_cast<int16_t>(score);
    }
    
    // Конвертация оценки из формата таблицы
    inline int scoreFromTT(int16_t score, int ply) {
        if (score >= 90000) return score - ply;
        if (score <= -90000) return score + ply;
        return score;
    }
}

// Константы для транспозиционной таблицы
namespace TTConstants {
    const size_t DEFAULT_SIZE_MB = 64;
    const size_t MIN_SIZE_MB = 1;
    const size_t MAX_SIZE_MB = 1024;
    const size_t ENTRY_SIZE = sizeof(TranspositionTable::TTEntry);
    
    // Размеры таблицы в зависимости от доступной памяти
    const size_t SMALL_TABLE_MB = 32;
    const size_t MEDIUM_TABLE_MB = 128;
    const size_t LARGE_TABLE_MB = 512;
    const size_t XLARGE_TABLE_MB = 1024;
    
    // Параметры замещения
    const int DEPTH_REPLACE_THRESHOLD = 2;
    const int AGE_REPLACE_FACTOR = 4;
}

#endif // TRANSPOSITION_TABLE_HPP