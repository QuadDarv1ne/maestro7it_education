#ifndef OPENING_BOOK_HPP
#define OPENING_BOOK_HPP

#include <unordered_map>
#include <string>
#include <vector>
#include <random>

/**
 * @brief Книга дебютов для шахматного движка
 * 
 * Содержит заранее подготовленные последовательности ходов
 * для популярных шахматных дебютов.
 */
class OpeningBook {
private:
    // Карта дебютов: позиция -> список возможных ходов
    std::unordered_map<std::string, std::vector<std::string>> book_;
    std::mt19937 rng_;
    
    void initializeBook() {
        // Итальянская партия
        book_["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"] = 
            {"e2e4", "Nf3", "Bc4"};
            
        book_["rnbqkbnr/pppp1ppp/8/4p3/2B1P3/8/PPPP1PPP/RNBQK1NR b KQkq - 0 1"] = 
            {"Nf6", "Bc5", "d6"};
            
        // Испанская партия  
        book_["rnbqkb1r/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 0 1"] = 
            {"a6", "Nf6", "Bc5"};
            
        // Сицилианская защита
        book_["rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"] = 
            {"Nf3", "d4", "c3"};
            
        // Французская защита
        book_["rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"] = 
            {"d4", "Nf3", "Nc3"};
            
        // Каро-Каннская защита
        book_["rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1"] = 
            {"d4", "Nf3", "Nc3"};
            
        // Дебют английского
        book_["rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq - 0 1"] = 
            {"e5", "Nf6", "c5"};
            
        // Дебют королевского пешечника
        book_["rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1"] = 
            {"d5", "Nf6", "e6"};
    }
    
public:
    OpeningBook() : rng_(std::random_device{}()) {
        initializeBook();
    }
    
    /**
     * @brief Получить случайный ход из книги дебютов
     * @param fen_position Текущая позиция в нотации FEN
     * @return Ход или пустая строка, если позиция не найдена
     */
    std::string getRandomMove(const std::string& fen_position) const {
        auto it = book_.find(fen_position);
        if (it != book_.end() && !it->second.empty()) {
            std::uniform_int_distribution<size_t> dist(0, it->second.size() - 1);
            return it->second[dist(rng_)];
        }
        return "";
    }
    
    /**
     * @brief Получить все возможные ходы для позиции
     * @param fen_position Текущая позиция в нотации FEN
     * @return Вектор ходов или пустой вектор
     */
    std::vector<std::string> getAllMoves(const std::string& fen_position) const {
        auto it = book_.find(fen_position);
        if (it != book_.end()) {
            return it->second;
        }
        return {};
    }
    
    /**
     * @brief Проверить, есть ли позиция в книге дебютов
     * @param fen_position Позиция в нотации FEN
     * @return true если позиция найдена
     */
    bool hasPosition(const std::string& fen_position) const {
        return book_.find(fen_position) != book_.end();
    }
    
    /**
     * @brief Добавить новую позицию в книгу
     * @param fen_position Позиция в нотации FEN
     * @param moves Вектор возможных ходов
     */
    void addPosition(const std::string& fen_position, 
                    const std::vector<std::string>& moves) {
        book_[fen_position] = moves;
    }
    
    /**
     * @brief Получить размер книги
     * @return Количество позиций в книге
     */
    size_t size() const {
        return book_.size();
    }
};

#endif // OPENING_BOOK_HPP