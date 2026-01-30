#include "../include/opening_book.hpp"
#include <iostream>
#include <cassert>

void testOpeningBook() {
    std::cout << "=== ТЕСТ КНИГИ ДЕБЮТОВ ===" << std::endl;
    
    OpeningBook book;
    
    // Тест 1: Проверка размера книги
    std::cout << "Размер книги: " << book.size() << " позиций" << std::endl;
    assert(book.size() > 0);
    std::cout << "✓ Размер книги корректный" << std::endl;
    
    // Тест 2: Проверка начальной позиции
    std::string start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    bool has_start = book.hasPosition(start_fen);
    std::cout << "Начальная позиция найдена: " << (has_start ? "ДА" : "НЕТ") << std::endl;
    assert(has_start);
    std::cout << "✓ Начальная позиция присутствует" << std::endl;
    
    // Тест 3: Получение хода из начальной позиции
    std::string move = book.getMove(start_fen);
    std::cout << "Ход из начальной позиции: " << move << std::endl;
    assert(!move.empty());
    std::cout << "✓ Ход успешно получен" << std::endl;
    
    // Тест 4: Получение всех ходов
    auto moves = book.getMoves(start_fen);
    std::cout << "Все возможные ходы из начальной позиции:" << std::endl;
    for (const auto& pair : moves) {
        std::cout << "  " << pair.first << " (вес: " << pair.second << ")" << std::endl;
    }
    assert(!moves.empty());
    std::cout << "✓ Все ходы успешно получены" << std::endl;
    
    // Тест 5: Проверка несуществующей позиции
    std::string fake_fen = "invalid_position";
    bool has_fake = book.hasPosition(fake_fen);
    std::cout << "Несуществующая позиция найдена: " << (has_fake ? "ДА" : "НЕТ") << std::endl;
    assert(!has_fake);
    std::cout << "✓ Корректная обработка несуществующих позиций" << std::endl;
    
    std::string fake_move = book.getMove(fake_fen);
    assert(fake_move.empty());
    std::cout << "✓ Корректная обработка хода из несуществующей позиции" << std::endl;
    
    std::cout << "\n✓ Все тесты книги дебютов пройдены успешно!" << std::endl << std::endl;
}

int main() {
    try {
        testOpeningBook();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Ошибка: " << e.what() << std::endl;
        return 1;
    }
}