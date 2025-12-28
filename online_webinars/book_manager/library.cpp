#include "library.h"
#include <cstdio>
#include <cstring>
#include <algorithm>
#include <map>
#include <cmath>
#include <vector>  // Добавлено для std::vector

/**
 * @brief Конструктор по умолчанию.
 * Инициализирует пустую библиотеку.
 */
Library::Library() {}

/**
 * @brief Добавляет книгу в библиотеку.
 * @param book Книга для добавления.
 */
void Library::addBook(const Book& book) {
    books.push_back(book);
    printf("Книга \"%s\" успешно добавлена.\n", book.title.c_str());
}

/**
 * @brief Удаляет книгу по названию.
 * @param title Название книги для удаления.
 */
void Library::removeBook(const std::string& title) {
    auto it = std::find_if(books.begin(), books.end(), 
                           [&title](const Book& b) { return b.title == title; });
    
    if (it == books.end()) {
        printf("Книга с названием \"%s\" не найдена.\n", title.c_str());
        return;
    }
    
    books.erase(it);
    printf("Книга \"%s\" успешно удалена.\n", title.c_str());
}

/**
 * @brief Обновляет книгу по названию.
 * @param title Название книги для обновления.
 * @param newBook Новые данные книги.
 */
void Library::updateBook(const std::string& title, const Book& newBook) {
    for (auto& book : books) {
        if (book.title == title) {
            book = newBook;
            printf("Книга \"%s\" успешно обновлена.\n", title.c_str());
            return;
        }
    }
    printf("Книга с названием \"%s\" не найдена.\n", title.c_str());
}

/**
 * @brief Выводит все книги в библиотеке.
 */
void Library::printLibrary() const {
    if (books.empty()) {
        printf("\nБиблиотека пуста.\n\n");
        return;
    }
    
    printf("\n========== БИБЛИОТЕКА ==========\n");
    printf("Всего книг: %zu\n\n", books.size());
    
    int i = 1;
    for (const auto& book : books) {
        printf("--- Книга %d ---\n", i++);
        printf("Название: %s\n", book.title.c_str());
        printf("Автор: %s\n", book.author.c_str());
        printf("Год: %d\n", book.year);
        printf("Жанр: %s\n", genreToString(book.genre).c_str());
        printf("Описание: %s\n", book.description.c_str());
        printf("ISBN: %s\n\n", book.isbn.c_str());
    }
    printf("================================\n\n");
}

/**
 * @brief Сортирует книги по названию.
 * @param ascending true для сортировки по возрастанию, false - по убыванию.
 */
void Library::sortByTitle(bool ascending) {
    if (ascending) {
        std::sort(books.begin(), books.end(), 
                  [](const Book& a, const Book& b) { return a.title < b.title; });
    } else {
        std::sort(books.begin(), books.end(), 
                  [](const Book& a, const Book& b) { return a.title > b.title; });
    }
    printf("Библиотека отсортирована по названию (%s).\n", 
           ascending ? "по возрастанию" : "по убыванию");
}

/**
 * @brief Сортирует книги по автору.
 * @param ascending true для сортировки по возрастанию, false - по убыванию.
 */
void Library::sortByAuthor(bool ascending) {
    if (ascending) {
        std::sort(books.begin(), books.end(), 
                  [](const Book& a, const Book& b) { return a.author < b.author; });
    } else {
        std::sort(books.begin(), books.end(), 
                  [](const Book& a, const Book& b) { return a.author > b.author; });
    }
    printf("Библиотека отсортирована по автору (%s).\n", 
           ascending ? "по возрастанию" : "по убыванию");
}

/**
 * @brief Сортирует книги по году.
 * @param ascending true для сортировки по возрастанию, false - по убыванию.
 */
void Library::sortByYear(bool ascending) {
    if (ascending) {
        std::sort(books.begin(), books.end(), 
                  [](const Book& a, const Book& b) { return a.year < b.year; });
    } else {
        std::sort(books.begin(), books.end(), 
                  [](const Book& a, const Book& b) { return a.year > b.year; });
    }
    printf("Библиотека отсортирована по году (%s).\n", 
           ascending ? "по возрастанию" : "по убыванию");
}

/**
 * @brief Сортирует книги по жанру.
 * @param ascending true для сортировки по возрастанию, false - по убыванию.
 */
void Library::sortByGenre(bool ascending) {
    if (ascending) {
        std::sort(books.begin(), books.end(), 
                  [](const Book& a, const Book& b) { return a.genre < b.genre; });
    } else {
        std::sort(books.begin(), books.end(), 
                  [](const Book& a, const Book& b) { return a.genre > b.genre; });
    }
    printf("Библиотека отсортирована по жанру (%s).\n", 
           ascending ? "по возрастанию" : "по убыванию");
}

/**
 * @brief Ищет книги по названию (с частичным совпадением).
 * @param title Строка для поиска.
 */
void Library::searchByTitle(const std::string& title) const {
    bool found = false;
    printf("\n=== Результаты поиска по названию: \"%s\" ===\n", title.c_str());
    
    for (const auto& book : books) {
        if (book.title.find(title) != std::string::npos) {
            printf("\n--- Найдена книга ---\n");
            printf("Название: %s\n", book.title.c_str());
            printf("Автор: %s\n", book.author.c_str());
            printf("Год: %d\n", book.year);
            printf("Жанр: %s\n", book.genre.c_str());
            printf("Описание: %s\n", book.description.c_str());
            printf("ISBN: %s\n", book.isbn.c_str());
            found = true;
        }
    }
    
    if (!found) {
        printf("Книги не найдены.\n");
    }
    printf("\n");
}

/**
 * @brief Ищет книги по автору (с частичным совпадением).
 * @param author Строка для поиска.
 */
void Library::searchByAuthor(const std::string& author) const {
    bool found = false;
    printf("\n=== Результаты поиска по автору: \"%s\" ===\n", author.c_str());
    
    for (const auto& book : books) {
        if (book.author.find(author) != std::string::npos) {
            printf("\n--- Найдена книга ---\n");
            printf("Название: %s\n", book.title.c_str());
            printf("Автор: %s\n", book.author.c_str());
            printf("Год: %d\n", book.year);
            printf("Жанр: %s\n", book.genre.c_str());
            printf("Описание: %s\n", book.description.c_str());
            printf("ISBN: %s\n", book.isbn.c_str());
            found = true;
        }
    }
    
    if (!found) {
        printf("Книги не найдены.\n");
    }
    printf("\n");
}

/**
 * @brief Ищет книги по жанру (с частичным совпадением).
 * @param genre Строка для поиска.
 */
void Library::searchByGenre(const std::string& genre) const {
    bool found = false;
    printf("\n=== Результаты поиска по жанру: \"%s\" ===\n", genre.c_str());
    
    for (const auto& book : books) {
        if (genreToString(book.genre).find(genre) != std::string::npos) {
            printf("\n--- Найдена книга ---\n");
            printf("Название: %s\n", book.title.c_str());
            printf("Автор: %s\n", book.author.c_str());
            printf("Год: %d\n", book.year);
            printf("Жанр: %s\n", genreToString(book.genre).c_str());
            printf("Описание: %s\n", book.description.c_str());
            printf("ISBN: %s\n", book.isbn.c_str());
            found = true;
        }
    }
    
    if (!found) {
        printf("Книги не найдены.\n");
    }
    printf("\n");
}

/**
 * @brief Сохраняет библиотеку в файл.
 * @param filename Имя файла.
 */
void Library::saveToFile(const std::string& filename) const {
    FILE* file = fopen(filename.c_str(), "w");
    if (!file) {
        printf("Ошибка: не удалось открыть файл \"%s\" для записи.\n", filename.c_str());
        return;
    }
    
    fprintf(file, "%zu\n", books.size());
    for (const auto& book : books) {
        fprintf(file, "%s\n", book.title.c_str());
        fprintf(file, "%s\n", book.author.c_str());
        fprintf(file, "%d\n", book.year);
        fprintf(file, "%s\n", genreToString(book.genre).c_str());
        fprintf(file, "%s\n", book.description.c_str());
        fprintf(file, "%s\n", book.isbn.c_str());
    }
    
    fclose(file);
    printf("Библиотека успешно сохранена в файл \"%s\".\n", filename.c_str());
}

/**
 * @brief Загружает библиотеку из файла.
 * @param filename Имя файла.
 */
void Library::loadFromFile(const std::string& filename) {
    FILE* file = fopen(filename.c_str(), "r");
    if (!file) {
        printf("Ошибка: не удалось открыть файл \"%s\" для чтения.\n", filename.c_str());
        return;
    }
    
    books.clear();  // Очищаем текущую библиотеку
    
    size_t newSize;
    if (fscanf(file, "%zu\n", &newSize) != 1) {
        printf("Ошибка: неверный формат файла.\n");
        fclose(file);
        return;
    }
    
    char buffer[1024];
    for (size_t i = 0; i < newSize; i++) {
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
            printf("Ошибка чтения года издания.\n");
            break;
        }
        
        if (fgets(buffer, sizeof(buffer), file)) {
            buffer[strcspn(buffer, "\n")] = 0;
            book.genre = stringToGenre(buffer);
        }
        
        if (fgets(buffer, sizeof(buffer), file)) {
            buffer[strcspn(buffer, "\n")] = 0;
            book.description = buffer;
        }
        
        if (fgets(buffer, sizeof(buffer), file)) {
            buffer[strcspn(buffer, "\n")] = 0;
            book.isbn = buffer;
        }
        
        books.push_back(book);
    }
    
    fclose(file);
    printf("Библиотека успешно загружена из файла \"%s\" (%zu книг).\n", filename.c_str(), books.size());
}

void Library::findBooksByAuthorAndGenre(const std::string& author, const std::string& genre) const {
    bool found = false;
    printf("\n=== Поиск книг (автор: \"%s\", жанр: \"%s\") ===\n", author.c_str(), genre.c_str());
    
    for (const auto& book : books) {
        bool matchAuthor = author.empty() || book.author.find(author) != std::string::npos;
        bool matchGenre = genre.empty() || book.genre.find(genre) != std::string::npos;
        
        if (matchAuthor && matchGenre) {
            printf("\n--- Найдена книга ---\n");
            printf("Название: %s\n", book.title.c_str());
            printf("Автор: %s\n", book.author.c_str());
            printf("Год: %d\n", book.year);
            printf("Жанр: %s\n", book.genre.c_str());
            printf("Описание: %s\n", book.description.c_str());
            printf("ISBN: %s\n", book.isbn.c_str());
            found = true;
        }
    }
    
    if (!found) {
        printf("Книги не найдены.\n");
    }
    printf("\n");
}

void Library::findOldestBookAfterYear(int year) const {
    const Book* oldest = nullptr;
    
    for (const auto& book : books) {
        if (book.year > year) {
            if (!oldest || book.year < oldest->year) {
                oldest = &book;
            }
        }
    }
    
    if (!oldest) {
        printf("\nНет книг с годом издания после %d.\n\n", year);
        return;
    }
    
    printf("\n=== Самая старая книга после %d года ===\n", year);
    printf("Название: %s\n", oldest->title.c_str());
    printf("Автор: %s\n", oldest->author.c_str());
    printf("Год: %d\n", oldest->year);
    printf("Жанр: %s\n", oldest->genre.c_str());
    printf("Описание: %s\n", oldest->description.c_str());
    printf("ISBN: %s\n\n", oldest->isbn.c_str());
}

void Library::findMostPopularGenre() const {
    if (books.empty()) {
        printf("\nБиблиотека пуста.\n\n");
        return;
    }
    
    std::map<std::string, int> genreCount;
    for (const auto& book : books) {
        genreCount[book.genre]++;
    }
    
    std::string mostPopular;
    int maxCount = 0;
    
    for (const auto& pair : genreCount) {
        if (pair.second > maxCount) {
            maxCount = pair.second;
            mostPopular = pair.first;
        }
    }
    
    printf("\n=== Самый популярный жанр ===\n");
    printf("Жанр: %s\n", mostPopular.c_str());
    printf("Количество книг: %d\n\n", maxCount);
}

void Library::calculateYearStatistics() const {
    if (books.empty()) {
        printf("\nБиблиотека пуста.\n\n");
        return;
    }
    
    int minYear = books[0].year;
    int maxYear = books[0].year;
    long long sum = 0;
    
    std::vector<int> years;
    for (const auto& book : books) {
        years.push_back(book.year);
        if (book.year < minYear) minYear = book.year;
        if (book.year > maxYear) maxYear = book.year;
        sum += book.year;
    }
    
    double average = static_cast<double>(sum) / books.size();
    
    std::sort(years.begin(), years.end());
    
    double median;
    size_t n = years.size();
    if (n % 2 == 0) {
        median = (years[n / 2 - 1] + years[n / 2]) / 2.0;
    } else {
        median = years[n / 2];
    }
    
    printf("\n=== Статистика по годам издания ===\n");
    printf("Минимальный год: %d\n", minYear);
    printf("Максимальный год: %d\n", maxYear);
    printf("Средний год (арифметически): %.2f\n", average);
    printf("Медиана года: %.2f\n\n", median);
}

void Library::findBooksWithExtremeTitles() const {
    if (books.empty()) {
        printf("\nБиблиотека пуста.\n\n");
        return;
    }
    
    const Book* shortest = &books[0];
    const Book* longest = &books[0];
    
    for (const auto& book : books) {
        if (book.title.length() < shortest->title.length()) {
            shortest = &book;
        }
        if (book.title.length() > longest->title.length()) {
            longest = &book;
        }
    }
    
    printf("\n=== Книга с самым коротким названием ===\n");
    printf("Название: %s (длина: %zu символов)\n", shortest->title.c_str(), shortest->title.length());
    printf("Автор: %s\n", shortest->author.c_str());
    printf("Год: %d\n", shortest->year);
    printf("ISBN: %s\n\n", shortest->isbn.c_str());
    
    printf("=== Книга с самым длинным названием ===\n");
    printf("Название: %s (длина: %zu символов)\n", longest->title.c_str(), longest->title.length());
    printf("Автор: %s\n", longest->author.c_str());
    printf("Год: %d\n", longest->year);
    printf("ISBN: %s\n\n", longest->isbn.c_str());
}