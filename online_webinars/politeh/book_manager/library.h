// Подавление предупреждения MSVC о небезопасных функциях
#ifdef _MSC_VER
#define _CRT_SECURE_NO_WARNINGS
#pragma warning(disable: 4996)
#endif

#ifndef LIBRARY_H
#define LIBRARY_H

#include "book.h"
#include <fstream>
#include <deque>
#include <string>
#include <vector>

// Класс для управления библиотекой книг
class Library {
private:
    Book* books;        // Динамический массив книг
    int size;           // Текущее количество книг
    int capacity;       // Выделенная ёмкость
    
    // Стек для отмены операций удаления (динамический массив)
    struct DeletedBook* undoStack;
    int undoSize;
    int undoCapacity;
    int maxUndoOperations;  // Максимальное количество операций для отмены
    
    // История действий
    std::ofstream logFile;
    std::string logFileName;
    std::deque<std::string> actionHistory;  // Хранит последние действия
    int maxHistorySize;
    
    // Внутренние функции управления памятью
    void resize();      // Увеличение массива
    void shrink();      // Уменьшение массива
    
public:
    // Конструктор и деструктор
    Library();
    ~Library();
    
    // CRUD операции
    void addBook(const Book& book);
    void removeBook(const std::string& title);
    void updateBook(const std::string& title, const Book& newBook);
    void printLibrary() const;
    
    // Сортировка
    void sortByTitle(bool ascending = true);
    void sortByAuthor(bool ascending = true);
    void sortByYear(bool ascending = true);
    void sortByGenre(bool ascending = true);
    
    // Многопольная сортировка
    void sortByAuthorAndTitle(bool authorAsc = true, bool titleAsc = true);
    void sortByYearAndGenre(bool yearAsc = true, bool genreAsc = true);
    
    // Поиск
    void searchByTitle(const std::string& title) const;
    void searchByAuthor(const std::string& author) const;
    void searchByGenre(const std::string& genre) const;
    void searchByISBN(const std::string& isbn) const;
    
    // Работа с файлами
    void saveToFile(const std::string& filename) const;
    void loadFromFile(const std::string& filename);
    
    // Специальные функции (задание 5)
    void findBooksByAuthorAndGenre(const std::string& author, const std::string& genre) const;
    void findOldestBookAfterYear(int year) const;
    void findMostPopularGenre() const;
    void calculateYearStatistics() const;
    void findBooksWithExtremeTitles() const;
    
    // Дополнительные улучшения
    void printBooksByGenre() const;             // Группировка по жанрам
    void printRecentBooks(int years) const;     // Книги за последние N лет
    
    // Undo функциональность
    void setMaxUndoOperations(int maxOps);
    void undoLastOperations(int k);
    void clearUndoHistory();
    int getUndoStackSize() const;
    
    // История действий
    void enableActionLogging(const std::string& filename = "library_actions.log");
    void logAction(const std::string& action);
    void setMaxHistorySize(int maxSize);
    void printActionHistory() const;
    std::vector<std::string> getActionHistory() const;
    
    // Геттер
    int getSize() const { return size; }
    bool isEmpty() const { return size == 0; }
    
private:
    // Вспомогательные методы для undo
    void resizeUndoStack();
    void addToDeleteStack(const Book& book, int position);
    
    // Вспомогательные методы для истории действий
    void addToHistory(const std::string& action);
};

#endif