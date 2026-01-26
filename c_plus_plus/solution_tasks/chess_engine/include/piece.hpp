#ifndef PIECE_HPP
#define PIECE_HPP

#include <iostream>
#include <string>

/**
 * Типы шахматных фигур
 */
enum class PieceType {
    EMPTY = 0,   ///< Пустая клетка
    PAWN = 1,    ///< Пешка
    KNIGHT = 2,  ///< Конь
    BISHOP = 3,  ///< Слон
    ROOK = 4,    ///< Ладья
    QUEEN = 5,   ///< Ферзь
    KING = 6     ///< Король
};

/**
 * Цвет фигур
 */
enum class Color {
    WHITE = 0,  ///< Белые
    BLACK = 1   ///< Черные
};

/**
 * @brief Класс, представляющий шахматную фигуру
 * 
 * Хранит тип и цвет фигуры, предоставляет методы для получения
 * символа, названия и стоимости фигуры
 */
class Piece {
private:
    PieceType type_;  ///< Тип фигуры
    Color color_;     ///< Цвет фигуры

public:
    // Конструкторы
    Piece();
    Piece(PieceType type, Color color);
    
    // Геттеры
    PieceType getType() const;  ///< Возвращает тип фигуры
    Color getColor() const;     ///< Возвращает цвет фигуры
    bool isEmpty() const;       ///< Проверяет, является ли клетка пустой
    
    // Сеттеры
    void setType(PieceType type);  ///< Устанавливает тип фигуры
    void setColor(Color color);    ///< Устанавливает цвет фигуры
    
    // Вспомогательные методы
    char getSymbol() const;        ///< Возвращает символ фигуры (например, 'K' для короля)
    std::string getName() const;   ///< Возвращает полное название фигуры на русском
    int getValue() const;          ///< Возвращает оценочную стоимость фигуры
    
    // Операторы
    bool operator==(const Piece& other) const;  ///< Сравнение двух фигур на равенство
    bool operator!=(const Piece& other) const;  ///< Сравнение двух фигур на неравенство
    
    // Статические методы
    static Piece createPiece(char symbol);              ///< Создает фигуру по символу
    static Color oppositeColor(Color color);           ///< Возвращает противоположный цвет
};

// Вспомогательные функции
std::ostream& operator<<(std::ostream& os, const Piece& piece);  ///< Вывод фигуры в поток

#endif // PIECE_HPP