// Подавление предупреждения MSVC о небезопасных функциях
#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#pragma warning(disable: 4996)
#endif

#ifndef BOOK_H
#define BOOK_H

#include <string>

// Перечисление жанров книг
enum class Genre {
    ROMAN,              // Роман
    POVEST,             // Повесть
    ROMAN_EPOPEYA,      // Роман-эпопея
    ROMAN_V_STIHAH,     // Роман в стихах
    FANTASTIKA,         // Фантастика
    DETEKTIV,           // Детектив
    DRAMA,              // Драма
    KOMEDIYA,           // Комедия
    POEZIYA,            // Поэзия
    PROZA,              // Проза
    OTHER               // Другое
};

// Структура для хранения информации о книге
struct Book {
    std::string title;          // Название
    std::string author;         // Автор
    int year;                   // Год издания
    Genre genre;                // Жанр
    std::string description;    // Описание
    std::string isbn;           // ISBN
};

// Функции для работы с жанрами
std::string genreToString(Genre genre);
Genre stringToGenre(const std::string& str);
void printAllGenres();

#endif