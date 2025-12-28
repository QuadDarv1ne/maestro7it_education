#include "ui.h"
#include <cstdio>
#include <limits>
#include <cstring>

UI::UI(Library& lib) : library(lib) {}

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
            if (value > 0) {  // Базовая валидация для года
                return value;
            } else {
                printf("Ошибка: значение должно быть положительным.\n");
            }
        } else {
            printf("Ошибка: введите корректное число.\n");
            clearInputBuffer();
        }
    }
}

std::string UI::getStringInput(const char* prompt) {
    char buffer[1024];
    printf("%s", prompt);
    if (fgets(buffer, sizeof(buffer), stdin)) {
        buffer[strcspn(buffer, "\n")] = 0;
        return std::string(buffer);
    }
    return "";
}

void UI::addBookMenu() {
    printf("\n=== ДОБАВЛЕНИЕ НОВОЙ КНИГИ ===\n");
    
    Book book;
    book.title = getStringInput("Название книги: ");
    book.author = getStringInput("Автор: ");
    book.year = getIntInput("Год издания: ");
    book.genre = getStringInput("Жанр: ");
    book.description = getStringInput("Краткое описание: ");
    book.isbn = getStringInput("ISBN: ");
    
    library.addBook(book);
    printf("\nКнига успешно добавлена!\n\n");
}

void UI::removeBookMenu() {
    printf("\n=== УДАЛЕНИЕ КНИГИ ===\n");
    std::string title = getStringInput("Введите название книги для удаления: ");
    library.removeBook(title);
}

void UI::updateBookMenu() {
    printf("\n=== ИЗМЕНЕНИЕ ИНФОРМАЦИИ О КНИГЕ ===\n");
    std::string oldTitle = getStringInput("Введите название книги для изменения: ");
    
    printf("\nВведите новые данные:\n");
    Book newBook;
    newBook.title = getStringInput("Новое название: ");
    newBook.author = getStringInput("Новый автор: ");
    newBook.year = getIntInput("Новый год издания: ");
    newBook.genre = getStringInput("Новый жанр: ");
    newBook.description = getStringInput("Новое описание: ");
    newBook.isbn = getStringInput("Новый ISBN: ");
    
    library.updateBook(oldTitle, newBook);
}

void UI::sortMenu() {
    printf("\n=== СОРТИРОВКА БИБЛИОТЕКИ ===\n");
    printf("1. По названию\n");
    printf("2. По автору\n");
    printf("3. По году издания\n");
    printf("4. По жанру\n");
    printf("0. Назад\n");
    
    int choice = getIntInput("\nВыберите поле для сортировки: ");
    
    if (choice < 1 || choice > 4) {
        if (choice != 0) printf("Неверный выбор.\n");
        return;
    }
    
    printf("\n1. По возрастанию\n");
    printf("2. По убыванию\n");
    int order = getIntInput("Выберите порядок: ");
    
    bool ascending = (order == 1);
    
    switch (choice) {
        case 1: library.sortByTitle(ascending); break;
        case 2: library.sortByAuthor(ascending); break;
        case 3: library.sortByYear(ascending); break;
        case 4: library.sortByGenre(ascending); break;
    }
}

void UI::searchMenu() {
    printf("\n=== ПОИСК КНИГ ===\n");
    printf("1. По названию\n");
    printf("2. По автору\n");
    printf("3. По жанру\n");
    printf("0. Назад\n");
    
    int choice = getIntInput("\nВыберите критерий поиска: ");
    
    std::string query;
    switch (choice) {
        case 1:
            query = getStringInput("Введите название (или часть): ");
            library.searchByTitle(query);
            break;
        case 2:
            query = getStringInput("Введите автора (или часть): ");
            library.searchByAuthor(query);
            break;
        case 3:
            query = getStringInput("Введите жанр (или часть): ");
            library.searchByGenre(query);
            break;
        case 0:
            break;
        default:
            printf("Неверный выбор.\n");
    }
}

void UI::fileMenu() {
    printf("\n=== РАБОТА С ФАЙЛАМИ ===\n");
    printf("1. Сохранить библиотеку в файл\n");
    printf("2. Загрузить библиотеку из файла\n");
    printf("0. Назад\n");
    
    int choice = getIntInput("\nВыберите действие: ");
    
    std::string filename;
    switch (choice) {
        case 1:
            filename = getStringInput("Введите имя файла для сохранения: ");
            library.saveToFile(filename);
            break;
        case 2:
            filename = getStringInput("Введите имя файла для загрузки: ");
            library.loadFromFile(filename);
            break;
        case 0:
            break;
        default:
            printf("Неверный выбор.\n");
    }
}

void UI::specialFunctionsMenu() {
    printf("\n=== СПЕЦИАЛЬНЫЕ ФУНКЦИИ ===\n");
    printf("1. Найти книги по автору и/или жанру\n");
    printf("2. Найти самую старую книгу после заданного года\n");
    printf("3. Найти самый популярный жанр\n");
    printf("4. Статистика по годам издания\n");
    printf("5. Книги с самым длинным и коротким названием\n");
    printf("0. Назад\n");
    
    int choice = getIntInput("\nВыберите функцию: ");
    
    switch (choice) {
        case 1: {
            std::string author = getStringInput("Введите автора (Enter для пропуска): ");
            std::string genre = getStringInput("Введите жанр (Enter для пропуска): ");
            library.findBooksByAuthorAndGenre(author, genre);
            break;
        }
        case 2: {
            int year = getIntInput("Введите год: ");
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
        case 0:
            break;
        default:
            printf("Неверный выбор.\n");
    }
}

void UI::run() {
    printf("╔═══════════════════════════════════════════╗\n");
    printf("║   СИСТЕМА УПРАВЛЕНИЯ БИБЛИОТЕКОЙ КНИГ    ║\n");
    printf("╚═══════════════════════════════════════════╝\n\n");
    
    bool running = true;
    while (running) {
        printf("═══════════════════════════════════════════\n");
        printf("          ГЛАВНОЕ МЕНЮ\n");
        printf("═══════════════════════════════════════════\n");
        printf("1. Распечатать библиотеку\n");
        printf("2. Добавить книгу\n");
        printf("3. Удалить книгу\n");
        printf("4. Изменить информацию о книге\n");
        printf("5. Сортировка\n");
        printf("6. Поиск книг\n");
        printf("7. Работа с файлами\n");
        printf("8. Специальные функции\n");
        printf("0. Выход из программы\n");
        printf("═══════════════════════════════════════════\n");
        
        int choice = getIntInput("\nВаше действие: ");
        
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
                printf("\nСпасибо за использование программы!\n");
                printf("До свидания!\n\n");
                running = false;
                break;
            default:
                printf("\nОшибка: неверный выбор. Попробуйте снова.\n\n");
        }
    }
}