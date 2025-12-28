#include "library.h"
#include <cassert>
#include <iostream>

/**
 * @brief Простые юнит-тесты для класса Library.
 * Запускаются вручную для проверки функциональности.
 */
void testLibrary() {
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