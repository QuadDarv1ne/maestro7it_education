#ifndef LIBRARY_H
#define LIBRARY_H

#include "book.h"
#include <vector>

/**
 * @brief Класс для управления библиотекой книг.
 * Поддерживает добавление, удаление, обновление, сортировку, поиск и сохранение книг.
 */
class Library {
private:
    std::vector<Book> books;  ///< Вектор книг (замена на std::vector для автоматического управления памятью)
    
public:
    Library();
    ~Library() = default;  // Деструктор по умолчанию, так как vector сам управляет памятью
    
    /**
     * @brief Добавляет книгу в библиотеку.
     * @param book Книга для добавления.
     */
    void addBook(const Book& book);
    
    /**
     * @brief Удаляет книгу по названию.
     * @param title Название книги для удаления.
     */
    void removeBook(const std::string& title);
    
    /**
     * @brief Обновляет книгу по названию.
     * @param title Название книги для обновления.
     * @param newBook Новые данные книги.
     */
    void updateBook(const std::string& title, const Book& newBook);
    
    /**
     * @brief Выводит все книги в библиотеке.
     */
    void printLibrary() const;
    
    /**
     * @brief Сортирует книги по названию.
     * @param ascending true для сортировки по возрастанию, false - по убыванию.
     */
    void sortByTitle(bool ascending = true);
    
    /**
     * @brief Сортирует книги по автору.
     * @param ascending true для сортировки по возрастанию, false - по убыванию.
     */
    void sortByAuthor(bool ascending = true);
    
    /**
     * @brief Сортирует книги по году.
     * @param ascending true для сортировки по возрастанию, false - по убыванию.
     */
    void sortByYear(bool ascending = true);
    
    /**
     * @brief Сортирует книги по жанру.
     * @param ascending true для сортировки по возрастанию, false - по убыванию.
     */
    void sortByGenre(bool ascending = true);
    
    /**
     * @brief Ищет книги по названию (с частичным совпадением).
     * @param title Строка для поиска.
     */
    void searchByTitle(const std::string& title) const;
    
    /**
     * @brief Ищет книги по автору (с частичным совпадением).
     * @param author Строка для поиска.
     */
    void searchByAuthor(const std::string& author) const;
    
    /**
     * @brief Ищет книги по жанру (с частичным совпадением строкового представления).
     * @param genre Строка для поиска.
     */
    void searchByGenre(const std::string& genre) const;
    
    /**
     * @brief Сохраняет библиотеку в файл.
     * @param filename Имя файла.
     */
    void saveToFile(const std::string& filename) const;
    
    /**
     * @brief Загружает библиотеку из файла.
     * @param filename Имя файла.
     */
    void loadFromFile(const std::string& filename);
    
    // Дополнительные функции (задание 5)
    /**
     * @brief Находит книги по автору и жанру.
     * @param author Автор.
     * @param genre Жанр (строка).
     */
    void findBooksByAuthorAndGenre(const std::string& author, const std::string& genre) const;
    
    /**
     * @brief Находит самую старую книгу после заданного года.
     * @param year Год.
     */
    void findOldestBookAfterYear(int year) const;
    
    /**
     * @brief Находит самый популярный жанр.
     */
    void findMostPopularGenre() const;
    
    /**
     * @brief Вычисляет статистику по годам.
     */
    void calculateYearStatistics() const;
    
    /**
     * @brief Находит книги с экстремальными названиями (самое длинное/короткое).
     */
    void findBooksWithExtremeTitles() const;
    
    /**
     * @brief Возвращает количество книг в библиотеке.
     * @return Размер библиотеки.
     */
    int getSize() const { return static_cast<int>(books.size()); }
};

#endif