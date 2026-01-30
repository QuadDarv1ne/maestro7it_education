#ifndef CHECK_DETECTION_HPP
#define CHECK_DETECTION_HPP

#include <vector>
#include <utility>
#include <string>

/**
 * Система обнаружения шаха и мата
 * Реализует полную проверку шахматных правил
 */

class CheckDetection {
public:
    // Типы результатов
    enum class GameState {
        NORMAL,         // Нормальная игра
        CHECK,          // Шах
        CHECKMATE,      // Мат
        STALEMATE,      // Пат
        INSUFFICIENT_MATERIAL, // Недостаточно фигур для мата
        THREEFOLD_REPETITION,  // Трехкратное повторение
        FIFTY_MOVE_RULE        // Правило 50 ходов
    };
    
    struct CheckInfo {
        bool in_check;                    // Под шахом ли король
        std::vector<int> attacking_pieces; // Индексы атакующих фигур
        std::vector<int> attack_squares;   // Клетки атаки
        GameState game_state;             // Текущее состояние игры
    };
    
    CheckDetection() = default;
    ~CheckDetection() = default;
    
    /**
     * Проверяет, находится ли король под шахом
     */
    CheckInfo detect_check(const std::vector<std::string>& board, bool white_to_move) const;
    
    /**
     * Проверяет, является ли позиция матом
     */
    bool is_checkmate(const std::vector<std::string>& board, bool white_to_move) const;
    
    /**
     * Проверяет, является ли позиция патом
     */
    bool is_stalemate(const std::vector<std::string>& board, bool white_to_move) const;
    
    /**
     * Проверяет недостаток материала для мата
     */
    bool is_insufficient_material(const std::vector<std::string>& board) const;
    
    /**
     * Проверяет трехкратное повторение позиции
     */
    bool is_threefold_repetition(const std::vector<std::vector<std::string>>& position_history) const;
    
    /**
     * Проверяет правило 50 ходов
     */
    bool is_fifty_move_rule(int halfmove_clock) const;
    
    /**
     * Получает все легальные ходы короля
     */
    std::vector<std::pair<int, int>> get_king_legal_moves(
        const std::vector<std::string>& board, 
        int king_pos, 
        bool white_king
    ) const;
    
    /**
     * Проверяет, защищает ли фигура короля от шаха
     */
    bool does_piece_block_check(
        const std::vector<std::string>& board,
        int piece_pos,
        int king_pos,
        const std::vector<int>& attack_directions
    ) const;
    
    /**
     * Проверяет, может ли фигура взять атакующую фигуру
     */
    bool can_capture_attacker(
        const std::vector<std::string>& board,
        int piece_pos,
        const std::vector<int>& attackers
    ) const;
    
private:
    /**
     * Находит позицию короля заданного цвета
     */
    int find_king(const std::vector<std::string>& board, bool white_king) const;
    
    /**
     * Проверяет, атакует ли фигура конкретную клетку
     */
    bool is_square_attacked(
        const std::vector<std::string>& board,
        int attacker_pos,
        int target_pos
    ) const;
    
    /**
     * Получает направления атаки для фигуры
     */
    std::vector<int> get_attack_directions(
        const std::string& piece,
        int from_pos,
        int to_pos
    ) const;
    
    /**
     * Проверяет путь между двумя клетками
     */
    bool is_path_clear(
        const std::vector<std::string>& board,
        int from_pos,
        int to_pos,
        const std::vector<int>& directions
    ) const;
    
    /**
     * Преобразует координаты в позицию (0-63)
     */
    int coords_to_pos(int row, int col) const;
    
    /**
     * Преобразует позицию в координаты
     */
    std::pair<int, int> pos_to_coords(int pos) const;
    
    /**
     * Проверяет, находится ли позиция в пределах доски
     */
    bool is_valid_position(int pos) const;
    bool is_valid_coords(int row, int col) const;
    
    /**
     * Получает тип фигуры без учета регистра
     */
    char get_piece_type(char piece) const;
};

// Глобальный экземпляр
extern CheckDetection g_check_detector;

#endif // CHECK_DETECTION_HPP