#include "library.h"
#include <cassert>
#include <iostream>
#include <locale.h>
#include <clocale>

#ifdef _WIN32
    #include <windows.h>
#endif

/**
 * @brief Простые юнит-тесты для класса Library.
 * Запускаются вручную для проверки функциональности.
 */
void testLibrary() {
    // Установка локали для поддержки кириллицы
    setlocale(LC_ALL, "ru_RU.UTF-8");
    
    #ifdef _WIN32
    // Для Windows: установка кодовой страницы UTF-8
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);
    #endif
    
    Library lib;

    // Тест добавления книги
    Book book1 = {"Война и мир", "Толстой", 1869, Genre::FICTION, "Эпический роман", "978-5-17-087121-1"};
    lib.addBook(book1);
    assert(lib.getSize() == 1);

    // Тест поиска
    lib.searchByTitle("Война");
    // (Вручную проверить вывод)

    // Тест удаления
    lib.removeBook("Война и мир");
    assert(lib.getSize() == 0);

    std::cout << "Все тесты пройдены!" << std::endl;
}

int main() {
    testLibrary();
    return 0;
}