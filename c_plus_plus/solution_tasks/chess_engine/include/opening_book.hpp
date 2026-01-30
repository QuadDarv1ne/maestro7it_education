#ifndef OPENING_BOOK_HPP
#define OPENING_BOOK_HPP

#include <vector>
#include <string>
#include <unordered_map>
#include <random>
#include <fstream>

/**
 * @brief Шахматная книга дебютов
 * 
 * Предоставляет доступ к заранее подготовленным дебютным линиям
 * для улучшения игры в начале партии.
 */
class OpeningBook {
private:
    // Карта позиций -> возможные ходы с весами
    std::unordered_map<std::string, std::vector<std::pair<std::string, int>>> book_;
    
    // Генератор случайных чисел
    mutable std::mt19937 rng_;
    
    /**
     * @brief Загрузить книгу из файла
     * @param filename Путь к файлу книги
     */
    void loadFromFile(const std::string& filename);
    
    /**
     * @brief Добавить стандартные дебюты
     */
    void addStandardOpenings();
    
public:
    OpeningBook();
    
    /**
     * @brief Получить случайный ход из книги для заданной позиции
     * @param fen Позиция в формате FEN
     * @return Ход или пустая строка, если позиция не найдена
     */
    std::string getMove(const std::string& fen) const;
    
    /**
     * @brief Проверить, есть ли позиция в книге
     * @param fen Позиция в формате FEN
     * @return true если позиция найдена
     */
    bool hasPosition(const std::string& fen) const;
    
    /**
     * @brief Получить все возможные ходы для позиции
     * @param fen Позиция в формате FEN
     * @return Вектор пар (ход, вес)
     */
    std::vector<std::pair<std::string, int>> getMoves(const std::string& fen) const;
    
    /**
     * @brief Размер книги
     * @return Количество позиций в книге
     */
    size_t size() const;
};

#endif // OPENING_BOOK_HPP