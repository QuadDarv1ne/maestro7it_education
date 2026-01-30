#ifndef ENDGAME_TABLEBASE_HPP
#define ENDGAME_TABLEBASE_HPP

#include <unordered_map>
#include <array>
#include <bitset>
#include <cstdint>
#include <string>
#include <functional>

/**
 * Система эндшпильных таблиц (Endgame Tablebases)
 * Предоставляет идеальную игру для позиций с малым количеством фигур
 * Поддерживает до 6 фигур (Syzygy tablebases совместимость)
 */

class EndgameTablebase {
private:
    // Типы результатов
    enum class Result {
        WIN,        // Победа для стороны на ходу
        LOSS,       // Поражение для стороны на ходу  
        DRAW,       // Ничья
        UNKNOWN     // Результат неизвестен
    };
    
    // Типы позиций
    enum class PositionType {
        KPK,        // Король + пешка против короля
        KRK,        // Король + ладья против короля
        KBK,        // Король + слон против короля
        KNK,        // Король + конь против короля
        KQK,        // Король + ферзь против короля
        KBBK,       // Король + 2 слона против короля
        KBNK,       // Король + слон + конь против короля
        MULTI_PIECE // Позиции с 4-6 фигурами
    };
    
    // Ключ для хэширования позиции
    struct PositionKey {
        uint64_t white_pieces;  // Битборд белых фигур
        uint64_t black_pieces;  // Битборд черных фигур
        uint8_t piece_types;    // Типы фигур (компактное представление)
        bool white_to_move;     // Очередь хода
        
        bool operator==(const PositionKey& other) const {
            return white_pieces == other.white_pieces &&
                   black_pieces == other.black_pieces &&
                   piece_types == other.piece_types &&
                   white_to_move == other.white_to_move;
        }
    };
    
    // Хэш-функция для PositionKey
    struct PositionKeyHash {
        std::size_t operator()(const PositionKey& key) const {
            return std::hash<uint64_t>{}(key.white_pieces) ^
                   (std::hash<uint64_t>{}(key.black_pieces) << 1) ^
                   (std::hash<uint8_t>{}(key.piece_types) << 2) ^
                   (std::hash<bool>{}(key.white_to_move) << 3);
        }
    };
    
    // Данные для каждой позиции
    struct TablebaseEntry {
        Result result;
        int distance_to_conversion;  // Расстояние до превращения/мата
        uint16_t best_move;          // Лучший ход (кодированный)
        uint16_t dtz;               // Distance To Zero (Syzygy формат)
    };
    
    // Кэш таблиц
    std::unordered_map<PositionKey, TablebaseEntry, PositionKeyHash> tablebase_cache_;
    
    // Предвычисленные таблицы для базовых эндшпилей
    std::array<std::array<Result, 64>, 64> kpk_table_;  // KPK таблица
    std::array<std::array<Result, 64>, 64> krk_table_;  // KRK таблица
    
    // Статистика
    mutable size_t cache_hits_;
    mutable size_t cache_misses_;
    mutable size_t positions_computed_;

public:
    EndgameTablebase();
    ~EndgameTablebase() = default;
    
    /**
     * Проверяет, можно ли использовать tablebase для данной позиции
     */
    bool is_applicable(const std::string& fen) const;
    
    /**
     * Получает идеальный результат для позиции
     */
    Result get_result(const std::string& fen) const;
    
    /**
     * Получает лучший ход из tablebase
     */
    std::string get_best_move(const std::string& fen) const;
    
    /**
     * Получает расстояние до мата/ничьей
     */
    int get_distance(const std::string& fen) const;
    
    /**
     * Проверяет позицию KPK (король + пешка против короля)
     */
    Result evaluate_kpk(uint8_t wk_sq, uint8_t bk_sq, uint8_t pawn_sq, bool white_to_move) const;
    
    /**
     * Проверяет позицию KRK (король + ладья против короля)
     */
    Result evaluate_krk(uint8_t wk_sq, uint8_t wr_sq, uint8_t bk_sq, bool white_to_move) const;
    
    /**
     * Генерирует все базовые эндшпили
     */
    void generate_basic_endgames();
    
    /**
     * Загружает внешние tablebase файлы (Syzygy формат)
     */
    bool load_syzygy_tablebases(const std::string& path);
    
    /**
     * Получает статистику использования
     */
    void get_statistics(size_t& hits, size_t& misses, size_t& computed) const;
    
    /**
     * Очищает кэш
     */
    void clear_cache();
    
private:
    /**
     * Преобразует FEN в ключ позиции
     */
    PositionKey fen_to_key(const std::string& fen) const;
    
    /**
     * Вычисляет результат для KPK позиции
     */
    Result compute_kpk_result(uint8_t wk_sq, uint8_t bk_sq, uint8_t pawn_sq, bool white_to_move) const;
    
    /**
     * Вычисляет результат для KRK позиции
     */
    Result compute_krk_result(uint8_t wk_sq, uint8_t wr_sq, uint8_t bk_sq, bool white_to_move) const;
    
    /**
     * Проверяет, является ли ход выигрышным
     */
    bool is_winning_move(uint8_t from, uint8_t to, const std::string& fen) const;
    
    /**
     * Кодирует ход в 16-битное число
     */
    uint16_t encode_move(uint8_t from, uint8_t to) const;
    
    /**
     * Декодирует ход из 16-битного числа
     */
    std::pair<uint8_t, uint8_t> decode_move(uint16_t move) const;
};

// Глобальный экземпляр tablebase
extern EndgameTablebase g_endgame_tablebase;

#endif // ENDGAME_TABLEBASE_HPP