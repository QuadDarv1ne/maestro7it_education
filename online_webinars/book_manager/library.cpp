// Подавление предупреждения MSVC о небезопасных функциях
#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#pragma warning(disable: 4996)
#endif

#include "library.h"
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <map>
#include <cmath>

// ==================== КОНСТРУКТОР И ДЕСТРУКТОР ====================

Library::Library() : books(nullptr), size(0), capacity(0) {}

Library::~Library() {
    delete[] books;
}

// ==================== УПРАВЛЕНИЕ ПАМЯТЬЮ ====================

void Library::resize() {
    int newCapacity = (capacity == 0) ? 4 : static_cast<int>(capacity * 1.5);
    Book* newBooks = new Book[newCapacity];
    
    for (int i = 0; i < size; i++) {
        newBooks[i] = books[i];
    }
    
    delete[] books;
    books = newBooks;
    capacity = newCapacity;
}

void Library::shrink() {
    if (size < capacity / 3 && capacity > 4) {
        int newCapacity = capacity / 2;
        Book* newBooks = new Book[newCapacity];
        
        for (int i = 0; i < size; i++) {
            newBooks[i] = books[i];
        }
        
        delete[] books;
        books = newBooks;
        capacity = newCapacity;
    }
}

// ==================== CRUD ОПЕРАЦИИ ====================

void Library::addBook(const Book& book) {
    if (size >= capacity) {
        resize();
    }
    books[size++] = book;
}

void Library::removeBook(const std::string& title) {
    int index = -1;
    for (int i = 0; i < size; i++) {
        if (books[i].title == title) {
            index = i;
            break;
        }
    }
    
    if (index == -1) {
        printf("Книга с названием \"%s\" не найдена.\n", title.c_str());
        return;
    }
    
    for (int i = index; i < size - 1; i++) {
        books[i] = books[i + 1];
    }
    size--;
    shrink();
    
    printf("Книга \"%s\" успешно удалена.\n", title.c_str());
}

void Library::updateBook(const std::string& title, const Book& newBook) {
    for (int i = 0; i < size; i++) {
        if (books[i].title == title) {
            books[i] = newBook;
            printf("Книга \"%s\" успешно обновлена.\n", title.c_str());
            return;
        }
    }
    printf("Книга с названием \"%s\" не найдена.\n", title.c_str());
}

void Library::printLibrary() const {
    if (size == 0) {
        printf("\n╔════════════════════════════════════════╗\n");
        printf("║       Библиотека пуста                 ║\n");
        printf("╚════════════════════════════════════════╝\n\n");
        return;
    }
    
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║         БИБЛИОТЕКА КНИГ                ║\n");
    printf("╠════════════════════════════════════════╣\n");
    printf("║  Всего книг: %-26d║\n", size);
    printf("╚════════════════════════════════════════╝\n\n");
    
    for (int i = 0; i < size; i++) {
        std::string genreStr = genreToString(books[i].genre);
        printf("┌─────────────────────────────────────────┐\n");
        printf("│ Книга #%-3d                              │\n", i + 1);
        printf("├─────────────────────────────────────────┤\n");
        printf("│ Название: %-30s│\n", books[i].title.c_str());
        printf("│ Автор:    %-30s│\n", books[i].author.c_str());
        printf("│ Год:      %-30d│\n", books[i].year);
        printf("│ Жанр:     %-30s│\n", genreStr.c_str());
        printf("│ ISBN:     %-30s│\n", books[i].isbn.empty() ? "Нет" : books[i].isbn.c_str());
        printf("│ Описание: %-30s│\n", books[i].description.substr(0, 30).c_str());
        if (books[i].description.length() > 30) {
            printf("│           %-30s│\n", books[i].description.substr(30, 30).c_str());
        }
        printf("└─────────────────────────────────────────┘\n\n");
    }
}

// ==================== СОРТИРОВКА ====================

void Library::sortByTitle(bool ascending) {
    // Пузырьковая сортировка (стабильная)
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            bool condition = ascending ? 
                (books[j].title > books[j + 1].title) :
                (books[j].title < books[j + 1].title);
            
            if (condition) {
                Book temp = books[j];
                books[j] = books[j + 1];
                books[j + 1] = temp;
            }
        }
    }
    printf("✓ Библиотека отсортирована по названию (%s).\n", 
           ascending ? "А→Я" : "Я→А");
}

void Library::sortByAuthor(bool ascending) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            bool condition = ascending ? 
                (books[j].author > books[j + 1].author) :
                (books[j].author < books[j + 1].author);
            
            if (condition) {
                Book temp = books[j];
                books[j] = books[j + 1];
                books[j + 1] = temp;
            }
        }
    }
    printf("✓ Библиотека отсортирована по автору (%s).\n", 
           ascending ? "А→Я" : "Я→А");
}

void Library::sortByYear(bool ascending) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            bool condition = ascending ? 
                (books[j].year > books[j + 1].year) :
                (books[j].year < books[j + 1].year);
            
            if (condition) {
                Book temp = books[j];
                books[j] = books[j + 1];
                books[j + 1] = temp;
            }
        }
    }
    printf("✓ Библиотека отсортирована по году (%s).\n", 
           ascending ? "старые→новые" : "новые→старые");
}

void Library::sortByGenre(bool ascending) {
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            bool condition = ascending ? 
                (books[j].genre > books[j + 1].genre) :
                (books[j].genre < books[j + 1].genre);
            
            if (condition) {
                Book temp = books[j];
                books[j] = books[j + 1];
                books[j + 1] = temp;
            }
        }
    }
    printf("✓ Библиотека отсортирована по жанру (%s).\n", 
           ascending ? "А→Я" : "Я→А");
}

// ==================== ПОИСК ====================

void Library::searchByTitle(const std::string& title) const {
    bool found = false;
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  ПОИСК ПО НАЗВАНИЮ: %-18s║\n", title.substr(0, 18).c_str());
    printf("╚════════════════════════════════════════╝\n");
    
    for (int i = 0; i < size; i++) {
        if (books[i].title.find(title) != std::string::npos) {
            std::string genreStr = genreToString(books[i].genre);
            printf("\n✓ Найдено:\n");
            printf("  Название: %s\n", books[i].title.c_str());
            printf("  Автор:    %s\n", books[i].author.c_str());
            printf("  Год:      %d\n", books[i].year);
            printf("  Жанр:     %s\n", genreStr.c_str());
            printf("  ISBN:     %s\n", books[i].isbn.empty() ? "Нет" : books[i].isbn.c_str());
            printf("  Описание: %s\n", books[i].description.c_str());
            found = true;
        }
    }
    
    if (!found) {
        printf("\n✗ Книги не найдены.\n");
    }
    printf("\n");
}

void Library::searchByAuthor(const std::string& author) const {
    bool found = false;
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  ПОИСК ПО АВТОРУ: %-20s║\n", author.substr(0, 20).c_str());
    printf("╚════════════════════════════════════════╝\n");
    
    for (int i = 0; i < size; i++) {
        if (books[i].author.find(author) != std::string::npos) {
            std::string genreStr = genreToString(books[i].genre);
            printf("\n✓ Найдено:\n");
            printf("  Название: %s\n", books[i].title.c_str());
            printf("  Автор:    %s\n", books[i].author.c_str());
            printf("  Год:      %d\n", books[i].year);
            printf("  Жанр:     %s\n", genreStr.c_str());
            printf("  ISBN:     %s\n", books[i].isbn.empty() ? "Нет" : books[i].isbn.c_str());
            found = true;
        }
    }
    
    if (!found) {
        printf("\n✗ Книги не найдены.\n");
    }
    printf("\n");
}

void Library::searchByGenre(const std::string& genre) const {
    bool found = false;
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  ПОИСК ПО ЖАНРУ: %-21s║\n", genre.substr(0, 21).c_str());
    printf("╚════════════════════════════════════════╝\n");
    
    Genre searchGenre = stringToGenre(genre);
    
    for (int i = 0; i < size; i++) {
        std::string genreStr = genreToString(books[i].genre);
        if (books[i].genre == searchGenre || genreStr.find(genre) != std::string::npos) {
            printf("\n✓ Найдено:\n");
            printf("  Название: %s\n", books[i].title.c_str());
            printf("  Автор:    %s\n", books[i].author.c_str());
            printf("  Год:      %d\n", books[i].year);
            printf("  Жанр:     %s\n", genreStr.c_str());
            found = true;
        }
    }
    
    if (!found) {
        printf("\n✗ Книги не найдены.\n");
    }
    printf("\n");
}

void Library::searchByISBN(const std::string& isbn) const {
    bool found = false;
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  ПОИСК ПО ISBN: %-22s║\n", isbn.substr(0, 22).c_str());
    printf("╚════════════════════════════════════════╝\n");
    
    for (int i = 0; i < size; i++) {
        if (books[i].isbn.find(isbn) != std::string::npos) {
            std::string genreStr = genreToString(books[i].genre);
            printf("\n✓ Найдено:\n");
            printf("  Название: %s\n", books[i].title.c_str());
            printf("  Автор:    %s\n", books[i].author.c_str());
            printf("  Год:      %d\n", books[i].year);
            printf("  Жанр:     %s\n", genreStr.c_str());
            printf("  ISBN:     %s\n", books[i].isbn.c_str());
            found = true;
        }
    }
    
    if (!found) {
        printf("\n✗ Книги не найдены.\n");
    }
    printf("\n");
}

// ==================== РАБОТА С ФАЙЛАМИ ====================

void Library::saveToFile(const std::string& filename) const {
    FILE* file = fopen(filename.c_str(), "w");
    if (!file) {
        printf("✗ Ошибка: не удалось открыть файл \"%s\" для записи.\n", filename.c_str());
        return;
    }
    
    fprintf(file, "%d\n", size);
    for (int i = 0; i < size; i++) {
        std::string genreStr = genreToString(books[i].genre);
        fprintf(file, "%s\n", books[i].title.c_str());
        fprintf(file, "%s\n", books[i].author.c_str());
        fprintf(file, "%d\n", books[i].year);
        fprintf(file, "%s\n", genreStr.c_str());
        fprintf(file, "%s\n", books[i].isbn.c_str());
        fprintf(file, "%s\n", books[i].description.c_str());
    }
    
    fclose(file);
    printf("✓ Библиотека успешно сохранена в файл \"%s\" (%d книг).\n", filename.c_str(), size);
}

void Library::loadFromFile(const std::string& filename) {
    FILE* file = fopen(filename.c_str(), "r");
    if (!file) {
        printf("✗ Ошибка: не удалось открыть файл \"%s\" для чтения.\n", filename.c_str());
        return;
    }
    
    delete[] books;
    books = nullptr;
    size = 0;
    capacity = 0;
    
    int newSize;
    if (fscanf(file, "%d\n", &newSize) != 1) {
        printf("✗ Ошибка: неверный формат файла.\n");
        fclose(file);
        return;
    }
    
    char buffer[1024];
    for (int i = 0; i < newSize; i++) {
        Book book;
        
        if (fgets(buffer, sizeof(buffer), file)) {
            buffer[strcspn(buffer, "\n")] = 0;
            book.title = buffer;
        }
        
        if (fgets(buffer, sizeof(buffer), file)) {
            buffer[strcspn(buffer, "\n")] = 0;
            book.author = buffer;
        }
        
        if (fscanf(file, "%d\n", &book.year) != 1) {
            printf("✗ Ошибка чтения года издания.\n");
            break;
        }
        
        if (fgets(buffer, sizeof(buffer), file)) {
            buffer[strcspn(buffer, "\n")] = 0;
            book.genre = stringToGenre(buffer);
        }
        
        if (fgets(buffer, sizeof(buffer), file)) {
            buffer[strcspn(buffer, "\n")] = 0;
            book.isbn = buffer;
        }
        
        if (fgets(buffer, sizeof(buffer), file)) {
            buffer[strcspn(buffer, "\n")] = 0;
            book.description = buffer;
        }
        
        addBook(book);
    }
    
    fclose(file);
    printf("✓ Библиотека успешно загружена из файла \"%s\" (%d книг).\n", filename.c_str(), size);
}

// ==================== СПЕЦИАЛЬНЫЕ ФУНКЦИИ ====================

void Library::findBooksByAuthorAndGenre(const std::string& author, const std::string& genre) const {
    bool found = false;
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  КОМБИНИРОВАННЫЙ ПОИСК                 ║\n");
    printf("╚════════════════════════════════════════╝\n");
    printf("  Автор: %s\n", author.empty() ? "(любой)" : author.c_str());
    printf("  Жанр:  %s\n", genre.empty() ? "(любой)" : genre.c_str());
    
    Genre searchGenre = genre.empty() ? Genre::OTHER : stringToGenre(genre);
    
    for (int i = 0; i < size; i++) {
        bool matchAuthor = author.empty() || books[i].author.find(author) != std::string::npos;
        std::string genreStr = genreToString(books[i].genre);
        bool matchGenre = genre.empty() || books[i].genre == searchGenre || 
                         genreStr.find(genre) != std::string::npos;
        
        if (matchAuthor && matchGenre) {
            printf("\n✓ Найдено:\n");
            printf("  Название: %s\n", books[i].title.c_str());
            printf("  Автор:    %s\n", books[i].author.c_str());
            printf("  Год:      %d\n", books[i].year);
            printf("  Жанр:     %s\n", genreStr.c_str());
            found = true;
        }
    }
    
    if (!found) {
        printf("\n✗ Книги не найдены.\n");
    }
    printf("\n");
}

void Library::findOldestBookAfterYear(int year) const {
    int minYear = -1;
    int minIndex = -1;
    
    for (int i = 0; i < size; i++) {
        if (books[i].year > year) {
            if (minYear == -1 || books[i].year < minYear) {
                minYear = books[i].year;
                minIndex = i;
            }
        }
    }
    
    if (minIndex == -1) {
        printf("\n✗ Нет книг с годом издания после %d.\n\n", year);
        return;
    }
    
    std::string genreStr = genreToString(books[minIndex].genre);
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  СТАРЕЙШАЯ КНИГА ПОСЛЕ %d г.         ║\n", year);
    printf("╚════════════════════════════════════════╝\n");
    printf("  Название: %s\n", books[minIndex].title.c_str());
    printf("  Автор:    %s\n", books[minIndex].author.c_str());
    printf("  Год:      %d\n", books[minIndex].year);
    printf("  Жанр:     %s\n\n", genreStr.c_str());
}

void Library::findMostPopularGenre() const {
    if (size == 0) {
        printf("\n✗ Библиотека пуста.\n\n");
        return;
    }
    
    std::map<Genre, int> genreCount;
    for (int i = 0; i < size; i++) {
        genreCount[books[i].genre]++;
    }
    
    Genre mostPopular = Genre::OTHER;
    int maxCount = 0;
    
    for (const auto& pair : genreCount) {
        if (pair.second > maxCount) {
            maxCount = pair.second;
            mostPopular = pair.first;
        }
    }
    
    std::string genreStr = genreToString(mostPopular);
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  САМЫЙ ПОПУЛЯРНЫЙ ЖАНР                 ║\n");
    printf("╚════════════════════════════════════════╝\n");
    printf("  Жанр:           %s\n", genreStr.c_str());
    printf("  Количество книг: %d\n", maxCount);
    printf("  Процент:        %.1f%%\n\n", (maxCount * 100.0) / size);
}

void Library::calculateYearStatistics() const {
    if (size == 0) {
        printf("\n✗ Библиотека пуста.\n\n");
        return;
    }
    
    int minYear = books[0].year;
    int maxYear = books[0].year;
    long long sum = 0;
    
    int* years = new int[size];
    for (int i = 0; i < size; i++) {
        years[i] = books[i].year;
        if (books[i].year < minYear) minYear = books[i].year;
        if (books[i].year > maxYear) maxYear = books[i].year;
        sum += books[i].year;
    }
    
    double average = static_cast<double>(sum) / size;
    
    // Сортировка для медианы
    for (int i = 0; i < size - 1; i++) {
        for (int j = 0; j < size - i - 1; j++) {
            if (years[j] > years[j + 1]) {
                int temp = years[j];
                years[j] = years[j + 1];
                years[j + 1] = temp;
            }
        }
    }
    
    double median;
    if (size % 2 == 0) {
        median = (years[size / 2 - 1] + years[size / 2]) / 2.0;
    } else {
        median = years[size / 2];
    }
    
    delete[] years;
    
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  СТАТИСТИКА ПО ГОДАМ ИЗДАНИЯ           ║\n");
    printf("╚════════════════════════════════════════╝\n");
    printf("  Минимальный год:         %d\n", minYear);
    printf("  Максимальный год:        %d\n", maxYear);
    printf("  Диапазон:                %d лет\n", maxYear - minYear);
    printf("  Среднее (арифметическое): %.2f\n", average);
    printf("  Медиана:                 %.2f\n\n", median);
}

void Library::findBooksWithExtremeTitles() const {
    if (size == 0) {
        printf("\n✗ Библиотека пуста.\n\n");
        return;
    }
    
    int shortestIndex = 0;
    int longestIndex = 0;
    
    for (int i = 1; i < size; i++) {
        if (books[i].title.length() < books[shortestIndex].title.length()) {
            shortestIndex = i;
        }
        if (books[i].title.length() > books[longestIndex].title.length()) {
            longestIndex = i;
        }
    }
    
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  ЭКСТРЕМАЛЬНЫЕ НАЗВАНИЯ                ║\n");
    printf("╚════════════════════════════════════════╝\n\n");
    
    printf("📖 Самое короткое название (%zu символов):\n", books[shortestIndex].title.length());
    printf("   \"%s\"\n", books[shortestIndex].title.c_str());
    printf("   Автор: %s (%d)\n\n", books[shortestIndex].author.c_str(), books[shortestIndex].year);
    
    printf("📚 Самое длинное название (%zu символов):\n", books[longestIndex].title.length());
    printf("   \"%s\"\n", books[longestIndex].title.c_str());
    printf("   Автор: %s (%d)\n\n", books[longestIndex].author.c_str(), books[longestIndex].year);
}

// ==================== ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ====================

void Library::printBooksByGenre() const {
    if (size == 0) {
        printf("\n✗ Библиотека пуста.\n\n");
        return;
    }
    
    std::map<Genre, int> genreCount;
    for (int i = 0; i < size; i++) {
        genreCount[books[i].genre]++;
    }
    
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  РАСПРЕДЕЛЕНИЕ ПО ЖАНРАМ               ║\n");
    printf("╚════════════════════════════════════════╝\n\n");
    
    for (const auto& pair : genreCount) {
        std::string genreStr = genreToString(pair.first);
        double percentage = (pair.second * 100.0) / size;
        printf("  %-20s : %2d книг (%.1f%%)\n", genreStr.c_str(), pair.second, percentage);
    }
    printf("\n");
}

void Library::printRecentBooks(int years) const {
    if (size == 0) {
        printf("\n✗ Библиотека пуста.\n\n");
        return;
    }
    
    int currentYear = 2024; // Можно получить системное время
    int minYear = currentYear - years;
    int count = 0;
    
    printf("\n╔════════════════════════════════════════╗\n");
    printf("║  КНИГИ ЗА ПОСЛЕДНИЕ %d ЛЕТ            ║\n", years);
    printf("╚════════════════════════════════════════╝\n");
    
    for (int i = 0; i < size; i++) {
        if (books[i].year >= minYear) {
            std::string genreStr = genreToString(books[i].genre);
            printf("\n  • %s\n", books[i].title.c_str());
            printf("    %s (%d, %s)\n", books[i].author.c_str(), books[i].year, genreStr.c_str());
            count++;
        }
    }
    
    if (count == 0) {
        printf("\n✗ Нет книг за последние %d лет.\n", years);
    } else {
        printf("\n  Всего найдено: %d книг\n", count);
    }
    printf("\n");
}