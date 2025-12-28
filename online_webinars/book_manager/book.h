#ifndef BOOK_H
#define BOOK_H

#include <string>

/**
 * @brief Структура, представляющая книгу в библиотеке.
 */
struct Book {
    std::string title;      ///< Название книги
    std::string author;     ///< Автор книги
    int year;               ///< Год издания
    std::string genre;      ///< Жанр книги
    std::string description;///< Описание книги
    std::string isbn;       ///< ISBN книги (новое поле)
};

#endif