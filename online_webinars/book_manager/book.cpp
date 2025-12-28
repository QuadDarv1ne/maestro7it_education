#include "book.h"

/**
 * @brief Преобразует enum Genre в строку.
 * @param genre Жанр.
 * @return Строковое представление.
 */
std::string genreToString(Genre genre) {
    switch (genre) {
        case Genre::FICTION: return "Художественная литература";
        case Genre::NON_FICTION: return "Нон-фикшн";
        case Genre::SCIENCE: return "Наука";
        case Genre::HISTORY: return "История";
        case Genre::OTHER: return "Другое";
        default: return "Неизвестно";
    }
}

/**
 * @brief Преобразует строку в enum Genre.
 * @param str Строка.
 * @return Жанр или OTHER если не распознано.
 */
Genre stringToGenre(const std::string& str) {
    if (str == "Художественная литература") return Genre::FICTION;
    if (str == "Нон-фикшн") return Genre::NON_FICTION;
    if (str == "Наука") return Genre::SCIENCE;
    if (str == "История") return Genre::HISTORY;
    return Genre::OTHER;
}