// Демонстрационная программа для тестирования новых функций
// 1. Многопольная сортировка
// 2. Отмена операций удаления

#include "library.h"
#include "book.h"
#include <iostream>

int main() {
    Library lib;
    
    // Создаем тестовые книги
    Book book1 = {"Война и мир", "Лев Толстой", 1869, Genre::ROMAN, "Эпическая повесть", "978-5-17-081998-7"};
    Book book2 = {"Преступление и наказание", "Фёдор Достоевский", 1866, Genre::ROMAN, "Психологический роман", "978-5-17-079754-0"};
    Book book3 = {"Анна Каренина", "Лев Толстой", 1877, Genre::ROMAN, "Роман о любви и обществе", "978-5-17-082000-6"};
    Book book4 = {"Мастер и Маргарита", "Михаил Булгаков", 1967, Genre::FANTASTIKA, "Фантастический роман", "978-5-17-081999-4"};
    Book book5 = {"Собачье сердце", "Михаил Булгаков", 1968, Genre::ROMAN, "Сатирический роман", "978-5-17-082001-3"};
    
    // Добавляем книги в библиотеку
    lib.addBook(book1);
    lib.addBook(book2);
    lib.addBook(book3);
    lib.addBook(book4);
    lib.addBook(book5);
    
    std::cout << "\n=== ДЕМОНСТРАЦИЯ МНОГОПОЛЬНОЙ СОРТИРОВКИ ===\n";
    std::cout << "\nИсходная библиотека:\n";
    lib.printLibrary();
    
    std::cout << "\n1. Сортировка по автору (A-Z), затем по названию (A-Z):\n";
    lib.sortByAuthorAndTitle(true, true);
    lib.printLibrary();
    
    std::cout << "\n2. Сортировка по году (старые->новые), затем по жанру (A-Z):\n";
    lib.sortByYearAndGenre(true, true);
    lib.printLibrary();
    
    std::cout << "\n=== ДЕМОНСТРАЦИЯ ОТМЕНЫ ОПЕРАЦИЙ ===\n";
    std::cout << "\nТекущий размер истории отмен: " << lib.getUndoStackSize() << "\n";
    
    std::cout << "\nУдаляем книгу 'Собачье сердце':\n";
    lib.removeBook("Собачье сердце");
    lib.printLibrary();
    std::cout << "Размер истории отмен: " << lib.getUndoStackSize() << "\n";
    
    std::cout << "\nУдаляем книгу 'Анна Каренина':\n";
    lib.removeBook("Анна Каренина");
    lib.printLibrary();
    std::cout << "Размер истории отмен: " << lib.getUndoStackSize() << "\n";
    
    std::cout << "\nОтменяем последнюю операцию (удаление 'Анна Каренина'):\n";
    lib.undoLastOperations(1);
    lib.printLibrary();
    std::cout << "Размер истории отмен: " << lib.getUndoStackSize() << "\n";
    
    std::cout << "\nОтменяем все оставшиеся операции:\n";
    lib.undoLastOperations(10); // Отменяем больше, чем есть
    lib.printLibrary();
    std::cout << "Размер истории отмен: " << lib.getUndoStackSize() << "\n";
    
    std::cout << "\n=== ДЕМОНСТРАЦИЯ ОГРАНИЧЕНИЯ ИСТОРИИ ===\n";
    std::cout << "\nУстанавливаем максимальный размер истории отмен = 2:\n";
    lib.setMaxUndoOperations(2);
    
    // Добавим книги заново для теста
    lib.addBook(book3); // Анна Каренина
    lib.addBook(book5); // Собачье сердце
    
    std::cout << "\nУдаляем 3 книги подряд:\n";
    lib.removeBook("Война и мир");
    lib.removeBook("Преступление и наказание");
    lib.removeBook("Мастер и Маргарита");
    
    std::cout << "Размер истории отмен: " << lib.getUndoStackSize() << " (должно быть 2)\n";
    
    std::cout << "\nПытаемся отменить 3 операции (хотя доступно только 2):\n";
    lib.undoLastOperations(3);
    std::cout << "Размер истории отмен: " << lib.getUndoStackSize() << "\n";
    
    std::cout << "\n=== ЗАВЕРШЕНИЕ ДЕМОНСТРАЦИИ ===\n";
    std::cout << "\nФинальная библиотека:\n";
    lib.printLibrary();
    
    return 0;
}