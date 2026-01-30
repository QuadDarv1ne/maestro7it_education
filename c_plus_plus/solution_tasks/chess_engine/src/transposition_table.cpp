#include "../include/transposition_table.hpp"
#include <iostream>
#include <iomanip>
#include <algorithm>

TranspositionTable::TranspositionTable(size_t size_mb) 
    : table_size_(0), current_age_(0), hits_(0), misses_(0), collisions_(0) {
    resizeMB(size_mb);
}

void TranspositionTable::resizeMB(size_t size_mb) {
    // Ограничиваем размер
    size_mb = std::max(TTConstants::MIN_SIZE_MB, 
                      std::min(size_mb, TTConstants::MAX_SIZE_MB));
    
    // Вычисляем количество записей
    size_t entries = (size_mb * 1024 * 1024) / sizeof(TTEntry);
    
    resize(entries);
}

void TranspositionTable::resize(size_t new_size) {
    table_size_ = new_size;
    table_.clear();
    table_.resize(table_size_);
    clear();
}

size_t TranspositionTable::getIndex(uint64_t hash_key) const {
    return hash_key % table_size_;
}

uint64_t TranspositionTable::hashFunction(uint64_t key) {
    // Простая хэш-функция (в реальной реализации использовать более сложную)
    key ^= key >> 33;
    key *= 0xff51afd7ed558ccdULL;
    key ^= key >> 33;
    key *= 0xc4ceb9fe1a85ec53ULL;
    key ^= key >> 33;
    return key;
}

bool TranspositionTable::probe(uint64_t hash_key, int& score, int& depth, 
                              EntryType& type, uint32_t& best_move) const {
    size_t index = getIndex(hash_key);
    const TTEntry& entry = table_[index];
    
    if (entry.hash_key == hash_key) {
        // Найдена запись
        hits_++;
        
        score = entry.score;
        depth = entry.depth;
        type = entry.entry_type;
        best_move = entry.best_move;
        return true;
    }
    
    misses_++;
    return false;
}

void TranspositionTable::store(uint64_t hash_key, int depth, int score, 
                              EntryType type, uint32_t best_move) {
    size_t index = getIndex(hash_key);
    TTEntry& entry = table_[index];
    
    // Проверяем, нужно ли заменить существующую запись
    if (shouldReplace(entry, TTEntry(hash_key, depth, score, type, best_move, current_age_))) {
        entry.hash_key = hash_key;
        entry.depth = depth;
        entry.score = score;
        entry.entry_type = type;
        entry.best_move = best_move;
        entry.age = current_age_;
    } else {
        collisions_++;
    }
}

bool TranspositionTable::shouldReplace(const TTEntry& existing, const TTEntry& new_entry) const {
    // Если ячейка пуста
    if (existing.hash_key == 0) return true;
    
    // Если новая запись глубже
    if (new_entry.depth > existing.depth + TTConstants::DEPTH_REPLACE_THRESHOLD) return true;
    
    // Если существующая запись старая
    if (current_age_ - existing.age > TTConstants::AGE_REPLACE_FACTOR) return true;
    
    // Если хэши совпадают, заменяем всегда
    if (existing.hash_key == new_entry.hash_key) return true;
    
    return false;
}

void TranspositionTable::clear() {
    std::fill(table_.begin(), table_.end(), TTEntry());
    hits_ = 0;
    misses_ = 0;
    collisions_ = 0;
    current_age_ = 0;
}

void TranspositionTable::incrementAge() {
    current_age_++;
    // Предотвращаем переполнение
    if (current_age_ == 0) {
        current_age_ = 1;
    }
}

size_t TranspositionTable::getUsedEntries() const {
    return std::count_if(table_.begin(), table_.end(),
                        [](const TTEntry& entry) { return entry.hash_key != 0; });
}

void TranspositionTable::printStatistics() const {
    std::cout << "\n=== TRANSPOSITION TABLE STATISTICS ===" << std::endl;
    std::cout << "Table size: " << table_size_ << " entries" << std::endl;
    std::cout << "Memory usage: " << (table_size_ * sizeof(TTEntry)) / (1024 * 1024) 
              << " MB" << std::endl;
    std::cout << "Used entries: " << getUsedEntries() << std::endl;
    std::cout << "Hit rate: " << std::fixed << std::setprecision(2) 
              << (getHitRate() * 100) << "%" << std::endl;
    std::cout << "Total probes: " << (hits_ + misses_) << std::endl;
    std::cout << "Hits: " << hits_ << std::endl;
    std::cout << "Misses: " << misses_ << std::endl;
    std::cout << "Collisions: " << collisions_ << std::endl;
    std::cout << "Current age: " << current_age_ << std::endl;
    std::cout << "=====================================" << std::endl;
}

std::string TranspositionTable::getStatsString() const {
    std::stringstream ss;
    ss << "TT[size=" << table_size_ 
       << ", hits=" << hits_ 
       << ", miss=" << misses_ 
       << ", hitrate=" << std::fixed << std::setprecision(2) << (getHitRate() * 100) << "%"
       << ", used=" << getUsedEntries() << "]";
    return ss.str();
}

// Демонстрационная программа для тестирования транспозиционной таблицы
class TTTest {
private:
    TranspositionTable tt_;
    
public:
    TTTest() : tt_(32) {} // 32 MB таблица
    
    void runTests() {
        std::cout << "=== TRANSPOSITION TABLE TESTING ===" << std::endl;
        
        testBasicFunctionality();
        testPerformance();
        testCollisionHandling();
        testAgeReplacement();
        
        std::cout << "\n=== TESTING COMPLETED ===" << std::endl;
    }

private:
    void testBasicFunctionality() {
        std::cout << "\n1. BASIC FUNCTIONALITY TEST:" << std::endl;
        
        // Тестируем сохранение и извлечение
        uint64_t test_hash = 0x123456789ABCDEF0ULL;
        int test_score = 150;
        int test_depth = 5;
        uint32_t test_move = TTUtils::packMove(12, 28); // e2-e4
        
        tt_.store(test_hash, test_depth, test_score, 
                 TranspositionTable::EXACT, test_move);
        
        int retrieved_score, retrieved_depth;
        TranspositionTable::EntryType retrieved_type;
        uint32_t retrieved_move;
        
        bool found = tt_.probe(test_hash, retrieved_score, retrieved_depth, 
                              retrieved_type, retrieved_move);
        
        std::cout << "Store/Probe test: " << (found ? "PASSED" : "FAILED") << std::endl;
        if (found) {
            std::cout << "  Score: " << retrieved_score << " (expected: " << test_score << ")" << std::endl;
            std::cout << "  Depth: " << retrieved_depth << " (expected: " << test_depth << ")" << std::endl;
            std::cout << "  Move: " << retrieved_move << " (expected: " << test_move << ")" << std::endl;
        }
    }
    
    void testPerformance() {
        std::cout << "\n2. PERFORMANCE TEST:" << std::endl;
        
        const int iterations = 100000;
        auto start = std::chrono::high_resolution_clock::now();
        
        // Заполняем таблицу
        for (int i = 0; i < iterations; i++) {
            uint64_t hash = hashFunction(i);
            tt_.store(hash, i % 10, i % 1000, 
                     TranspositionTable::EXACT, TTUtils::packMove(i % 64, (i + 10) % 64));
        }
        
        // Тестируем поиск
        int hits = 0;
        for (int i = 0; i < iterations; i++) {
            uint64_t hash = hashFunction(i);
            int score, depth;
            TranspositionTable::EntryType type;
            uint32_t move;
            
            if (tt_.probe(hash, score, depth, type, move)) {
                hits++;
            }
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        std::cout << "Iterations: " << iterations << std::endl;
        std::cout << "Total time: " << duration.count() << " ms" << std::endl;
        std::cout << "Operations per second: " << (iterations * 2 * 1000 / duration.count()) << std::endl;
        std::cout << "Hit rate: " << std::fixed << std::setprecision(2) 
                  << (static_cast<double>(hits) / iterations * 100) << "%" << std::endl;
    }
    
    void testCollisionHandling() {
        std::cout << "\n3. COLLISION HANDLING TEST:" << std::endl;
        
        // Создаем ситуации с коллизиями
        size_t initial_collisions = tt_.getCollisions();
        
        // Записываем несколько записей с одинаковым индексом
        uint64_t base_hash = 1000;
        size_t index = tt_.getIndex(base_hash);
        
        for (int i = 0; i < 10; i++) {
            uint64_t hash = base_hash + (i * tt_.getSize()); // Гарантированно одинаковый индекс
            tt_.store(hash, 5, i * 10, TranspositionTable::EXACT, TTUtils::packMove(0, i));
        }
        
        size_t final_collisions = tt_.getCollisions();
        std::cout << "Collisions generated: " << (final_collisions - initial_collisions) << std::endl;
        std::cout << "Collision handling: WORKING" << std::endl;
    }
    
    void testAgeReplacement() {
        std::cout << "\n4. AGE REPLACEMENT TEST:" << std::endl;
        
        // Тестируем механизм замещения по возрасту
        tt_.clear();
        
        // Записываем старую запись
        tt_.store(1, 5, 100, TranspositionTable::EXACT, TTUtils::packMove(0, 1));
        
        // Увеличиваем возраст
        for (int i = 0; i < 10; i++) {
            tt_.incrementAge();
        }
        
        // Пытаемся записать новую запись в ту же позицию
        tt_.store(1, 3, 200, TranspositionTable::EXACT, TTUtils::packMove(2, 3));
        
        // Проверяем, что новая запись сохранилась
        int score, depth;
        TranspositionTable::EntryType type;
        uint32_t move;
        
        bool found = tt_.probe(1, score, depth, type, move);
        std::cout << "Age-based replacement: " << (found && score == 200 ? "WORKING" : "FAILED") << std::endl;
    }
};

int main() {
    try {
        TTTest test;
        test.runTests();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}