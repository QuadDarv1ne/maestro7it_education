#ifndef BOOK_H
#define BOOK_H

#include <string>

/**
 * @brief Перечисление жанров книг.
 */
enum class Genre {
    FICTION,      ///< Художественная литература
    NON_FICTION,  ///< Нон-фикшн
    SCIENCE,      ///< Наука
    HISTORY,      ///< История
    OTHER         ///< Другое
};

/**
 * @brief Преобразует enum Genre в строку.
 * @param genre Жанр.
 * @return Строковое представление.
 */
std::string genreToString(Genre genre);

/**
 * @brief Преобразует строку в enum Genre.
 * @param str Строка.
 * @return Жанр или OTHER если не распознано.
 */
Genre stringToGenre(const std::string& str);

/**
 * @brief Структура, представляющая книгу в библиотеке.
 */
struct Book {
    std::string title;      ///< Название книги
    std::string author;     ///< Автор книги
    int year;               ///< Год издания
    Genre genre;            ///< Жанр книги (enum)
    std::string description;///< Описание книги
    std::string isbn;       ///< ISBN книги (новое поле)
};

#endif