// Подавление предупреждения MSVC о небезопасных функциях
#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#pragma warning(disable: 4996)
#endif

#include "book.h"
#include <algorithm>
#include <cctype>
#include <cstdio>

// Преобразование жанра из enum в строку
std::string genreToString(Genre genre) {
    switch (genre) {
        case Genre::ROMAN: return "Роман";
        case Genre::POVEST: return "Повесть";
        case Genre::ROMAN_EPOPEYA: return "Роман-эпопея";
        case Genre::ROMAN_V_STIHAH: return "Роман в стихах";
        case Genre::FANTASTIKA: return "Фантастика";
        case Genre::DETEKTIV: return "Детектив";
        case Genre::DRAMA: return "Драма";
        case Genre::KOMEDIYA: return "Комедия";
        case Genre::POEZIYA: return "Поэзия";
        case Genre::PROZA: return "Проза";
        case Genre::OTHER: 
        default: return "Другое";
    }
}

// Преобразование строки в жанр (умный парсинг)
Genre stringToGenre(const std::string& str) {
    std::string lower = str;
    std::transform(lower.begin(), lower.end(), lower.begin(), 
                   [](unsigned char c){ return std::tolower(c); });
    
    // Проверяем в порядке от более специфичных к общим
    if (lower.find("роман-эпопея") != std::string::npos || 
        lower.find("роман эпопея") != std::string::npos) return Genre::ROMAN_EPOPEYA;
    if (lower.find("роман в стихах") != std::string::npos) return Genre::ROMAN_V_STIHAH;
    if (lower.find("роман") != std::string::npos) return Genre::ROMAN;
    if (lower.find("повесть") != std::string::npos) return Genre::POVEST;
    if (lower.find("фантастика") != std::string::npos || 
        lower.find("sci-fi") != std::string::npos) return Genre::FANTASTIKA;
    if (lower.find("детектив") != std::string::npos) return Genre::DETEKTIV;
    if (lower.find("драма") != std::string::npos) return Genre::DRAMA;
    if (lower.find("комедия") != std::string::npos) return Genre::KOMEDIYA;
    if (lower.find("поэзия") != std::string::npos || 
        lower.find("стих") != std::string::npos) return Genre::POEZIYA;
    if (lower.find("проза") != std::string::npos) return Genre::PROZA;
    
    return Genre::OTHER;
}

// Вывод всех доступных жанров
void printAllGenres() {
    printf("\nДоступные жанры:\n");
    printf("1.  Роман\n");
    printf("2.  Повесть\n");
    printf("3.  Роман-эпопея\n");
    printf("4.  Роман в стихах\n");
    printf("5.  Фантастика\n");
    printf("6.  Детектив\n");
    printf("7.  Драма\n");
    printf("8.  Комедия\n");
    printf("9.  Поэзия\n");
    printf("10. Проза\n");
    printf("11. Другое\n");
}