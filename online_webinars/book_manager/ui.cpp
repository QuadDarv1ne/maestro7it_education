// Подавление предупреждения MSVC о небезопасных функциях
#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#pragma warning(disable: 4996)
#endif

#include "ui.h"
#include <cstdio>
#include <limits>
#include <cstring>

UI::UI(Library& lib) : library(lib) {}

// ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ====================

void UI::clearInputBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

int UI::getIntInput(const char* prompt) {
    int value;
    while (true) {
        printf("%s", prompt);
        if (scanf("%d", &value) == 1) {
            clearInputBuffer();
            return value;
        } else {
            printf("✗ Ошибка: введите корректное число.\n");
            clearInputBuffer();
        }
    }
}

std::string UI::getStringInput(const char* prompt) {
    char buffer[1024];
    printf("%s", prompt);
    fflush(stdout);
    
    if (fgets(buffer, sizeof(buffer), stdin)) {
        size_t len = strlen(buffer);
        if (len > 0 && buffer[len - 1] == '\n') {
            buffer[len - 1] = '\0';
        }
        return std::string(buffer);
    }
    return "";
}

// ==================== МЕНЮ ОПЕРАЦИЙ ====================

void UI::addBookMenu() {
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║     ДОБАВЛЕНИЕ НОВОЙ КНИГИ             ║\n");
    printf("╚════════════════════════════════════════╝\n\n");
    
    Book book;
    
    // Название
    book.title = getStringInput("📖 Название книги: ");
    if (book.title.empty()) {
        printf("✗ Ошибка: название не может быть пустым.\n");
        return;
    }
    
    // Автор
    book.author = getStringInput("✍️  Автор: ");
    if (book.author.empty()) {
        printf("✗ Ошибка: автор не может быть пустым.\n");
        return;
    }
    
    // Год
    book.year = getIntInput("📅 Год издания: ");
    if (book.year < 1000 || book.year > 2025) {
        printf("⚠️  Предупреждение: необычный год издания.\n");
    }
    
    // Жанр
    printAllGenres();
    int genreChoice = getIntInput("\n🎭 Выберите жанр (1-11): ");
    switch (genreChoice) {
        case 1: book.genre = Genre::ROMAN; break;
        case 2: book.genre = Genre::POVEST; break;
        case 3: book.genre = Genre::ROMAN_EPOPEYA; break;
        case 4: book.genre = Genre::ROMAN_V_STIHAH; break;
        case 5: book.genre = Genre::FANTASTIKA; break;
        case 6: book.genre = Genre::DETEKTIV; break;
        case 7: book.genre = Genre::DRAMA; break;
        case 8: book.genre = Genre::KOMEDIYA; break;
        case 9: book.genre = Genre::POEZIYA; break;
        case 10: book.genre = Genre::PROZA; break;
        default: book.genre = Genre::OTHER; break;
    }
    
    // ISBN (опционально)
    book.isbn = getStringInput("🔢 ISBN (Enter для пропуска): ");
    
    // Описание
    book.description = getStringInput("📝 Краткое описание: ");
    
    library.addBook(book);
    printf("\n✓ Книга \"%s\" успешно добавлена!\n\n", book.title.c_str());
}

void UI::removeBookMenu() {
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║        УДАЛЕНИЕ КНИГИ                  ║\n");
    printf("╚════════════════════════════════════════╝\n\n");
    
    if (library.isEmpty()) {
        printf("✗ Библиотека пуста.\n\n");
        return;
    }
    
    std::string title = getStringInput("📖 Введите название книги для удаления: ");
    library.removeBook(title);
    printf("\n");
}

void UI::updateBookMenu() {
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║     ИЗМЕНЕНИЕ ИНФОРМАЦИИ О КНИГЕ       ║\n");
    printf("╚════════════════════════════════════════╝\n\n");
    
    if (library.isEmpty()) {
        printf("✗ Библиотека пуста.\n\n");
        return;
    }
    
    std::string oldTitle = getStringInput("📖 Введите название книги для изменения: ");
    
    printf("\n--- Введите новые данные ---\n\n");
    Book newBook;
    
    newBook.title = getStringInput("📖 Новое название: ");
    newBook.author = getStringInput("✍️  Новый автор: ");
    newBook.year = getIntInput("📅 Новый год издания: ");
    
    printAllGenres();
    int genreChoice = getIntInput("\n🎭 Выберите новый жанр (1-11): ");
    switch (genreChoice) {
        case 1: newBook.genre = Genre::ROMAN; break;
        case 2: newBook.genre = Genre::POVEST; break;
        case 3: newBook.genre = Genre::ROMAN_EPOPEYA; break;
        case 4: newBook.genre = Genre::ROMAN_V_STIHAH; break;
        case 5: newBook.genre = Genre::FANTASTIKA; break;
        case 6: newBook.genre = Genre::DETEKTIV; break;
        case 7: newBook.genre = Genre::DRAMA; break;
        case 8: newBook.genre = Genre::KOMEDIYA; break;
        case 9: newBook.genre = Genre::POEZIYA; break;
        case 10: newBook.genre = Genre::PROZA; break;
        default: newBook.genre = Genre::OTHER; break;
    }
    
    newBook.isbn = getStringInput("🔢 Новый ISBN: ");
    newBook.description = getStringInput("📝 Новое описание: ");
    
    library.updateBook(oldTitle, newBook);
    printf("\n");
}

void UI::sortMenu() {
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║       СОРТИРОВКА БИБЛИОТЕКИ            ║\n");
    printf("╚════════════════════════════════════════╝\n");
    printf("  1. По названию\n");
    printf("  2. По автору\n");
    printf("  3. По году издания\n");
    printf("  4. По жанру\n");
    printf("  0. ← Назад\n");
    
    int choice = getIntInput("\n📊 Выберите поле для сортировки: ");
    
    if (choice < 1 || choice > 4) {
        if (choice != 0) printf("✗ Неверный выбор.\n");
        return;
    }
    
    printf("\n  1. По возрастанию (A→Z, 0→9)\n");
    printf("  2. По убыванию (Z→A, 9→0)\n");
    int order = getIntInput("Выберите порядок: ");
    
    bool ascending = (order == 1);
    
    printf("\n");
    switch (choice) {
        case 1: library.sortByTitle(ascending); break;
        case 2: library.sortByAuthor(ascending); break;
        case 3: library.sortByYear(ascending); break;
        case 4: library.sortByGenre(ascending); break;
    }
    printf("\n");
}

void UI::searchMenu() {
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║          ПОИСК КНИГ                    ║\n");
    printf("╚════════════════════════════════════════╝\n");
    printf("  1. По названию\n");
    printf("  2. По автору\n");
    printf("  3. По жанру\n");
    printf("  4. По ISBN\n");
    printf("  0. ← Назад\n");
    
    int choice = getIntInput("\n🔍 Выберите критерий поиска: ");
    
    std::string query;
    switch (choice) {
        case 1:
            query = getStringInput("\n📖 Введите название (или часть): ");
            library.searchByTitle(query);
            break;
        case 2:
            query = getStringInput("\n✍️  Введите автора (или часть): ");
            library.searchByAuthor(query);
            break;
        case 3:
            query = getStringInput("\n🎭 Введите жанр (или часть): ");
            library.searchByGenre(query);
            break;
        case 4:
            query = getStringInput("\n🔢 Введите ISBN (или часть): ");
            library.searchByISBN(query);
            break;
        case 0:
            break;
        default:
            printf("✗ Неверный выбор.\n");
    }
}

void UI::fileMenu() {
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║       РАБОТА С ФАЙЛАМИ                 ║\n");
    printf("╚════════════════════════════════════════╝\n");
    printf("  1. 💾 Сохранить библиотеку в файл\n");
    printf("  2. 📂 Загрузить библиотеку из файла\n");
    printf("  0. ← Назад\n");
    
    int choice = getIntInput("\n📁 Выберите действие: ");
    
    std::string filename;
    switch (choice) {
        case 1:
            filename = getStringInput("\n💾 Введите имя файла для сохранения: ");
            if (filename.empty()) {
                filename = "library.txt";
                printf("   Используется имя по умолчанию: %s\n", filename.c_str());
            }
            library.saveToFile(filename);
            break;
        case 2:
            filename = getStringInput("\n📂 Введите имя файла для загрузки: ");
            if (filename.empty()) {
                printf("✗ Имя файла не может быть пустым.\n");
                break;
            }
            library.loadFromFile(filename);
            break;
        case 0:
            break;
        default:
            printf("✗ Неверный выбор.\n");
    }
    printf("\n");
}

void UI::specialFunctionsMenu() {
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║       СПЕЦИАЛЬНЫЕ ФУНКЦИИ              ║\n");
    printf("╚════════════════════════════════════════╝\n");
    printf("  1. 🔎 Найти книги по автору и/или жанру\n");
    printf("  2. 📅 Найти самую старую книгу после года\n");
    printf("  3. 🏆 Найти самый популярный жанр\n");
    printf("  4. 📊 Статистика по годам издания\n");
    printf("  5. 📏 Книги с экстремальной длиной названия\n");
    printf("  6. 📚 Распределение по жанрам\n");
    printf("  7. 🆕 Недавно изданные книги\n");
    printf("  0. ← Назад\n");
    
    int choice = getIntInput("\n⚡ Выберите функцию: ");
    
    switch (choice) {
        case 1: {
            printf("\n");
            std::string author = getStringInput("✍️  Введите автора (Enter для пропуска): ");
            std::string genre = getStringInput("🎭 Введите жанр (Enter для пропуска): ");
            library.findBooksByAuthorAndGenre(author, genre);
            break;
        }
        case 2: {
            int year = getIntInput("\n📅 Введите год: ");
            library.findOldestBookAfterYear(year);
            break;
        }
        case 3:
            library.findMostPopularGenre();
            break;
        case 4:
            library.calculateYearStatistics();
            break;
        case 5:
            library.findBooksWithExtremeTitles();
            break;
        case 6:
            library.printBooksByGenre();
            break;
        case 7: {
            int years = getIntInput("\n📅 Показать книги за последние N лет: ");
            library.printRecentBooks(years);
            break;
        }
        case 0:
            break;
        default:
            printf("✗ Неверный выбор.\n");
    }
}

// ==================== ГЛАВНЫЙ ЦИКЛ ====================

void UI::run() {
    printf("\n");
    printf("╔═══════════════════════════════════════════════════╗\n");
    printf("║                                                   ║\n");
    printf("║      📚 СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ 📚        ║\n");
    printf("║                                                   ║\n");
    printf("║            Добро пожаловать                       ║\n");
    printf("║                                                   ║\n");
    printf("╚═══════════════════════════════════════════════════╝\n\n");
    
    bool running = true;
    while (running) {
        printf("╔═══════════════════════════════════════════════════╗\n");
        printf("║                  ГЛАВНОЕ МЕНЮ                     ║\n");
        printf("╠═══════════════════════════════════════════════════╣\n");
        printf("║  1. 📋 Распечатать библиотеку                     ║\n");
        printf("║  2. ➕ Добавить книгу                              ║\n");
        printf("║  3. ➖ Удалить книгу                               ║\n");
        printf("║  4. ✏️  Изменить информацию о книге                ║\n");
        printf("║  5. 📊 Сортировка                                 ║\n");
        printf("║  6. 🔍 Поиск книг                                 ║\n");
        printf("║  7. 💾 Работа с файлами                           ║\n");
        printf("║  8. ⚡ Специальные функции                        ║\n");
        printf("║  0. 🚪 Выход из программы                         ║\n");
        printf("╚═══════════════════════════════════════════════════╝\n");
        
        int choice = getIntInput("\n🎯 Ваше действие: ");
        
        switch (choice) {
            case 1:
                library.printLibrary();
                break;
            case 2:
                addBookMenu();
                break;
            case 3:
                removeBookMenu();
                break;
            case 4:
                updateBookMenu();
                break;
            case 5:
                sortMenu();
                break;
            case 6:
                searchMenu();
                break;
            case 7:
                fileMenu();
                break;
            case 8:
                specialFunctionsMenu();
                break;
            case 0:
                printf("\n╔═══════════════════════════════════════════════════╗\n");
                printf("║                                                   ║\n");
                printf("║     Спасибо за использование программы            ║\n");
                printf("║              До свидания  👋                      ║\n");
                printf("║                                                   ║\n");
                printf("╚═══════════════════════════════════════════════════╝\n\n");
                running = false;
                break;
            default:
                printf("\n✗ Ошибка: неверный выбор. Попробуйте снова.\n\n");
        }
    }
}