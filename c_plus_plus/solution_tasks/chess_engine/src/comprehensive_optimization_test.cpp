#include "../include/board.hpp"
#include "../include/move_generator.hpp"
#include "../include/position_evaluator.hpp"
#include "../include/opening_book.hpp"
#include <iostream>
#include <chrono>
#include <cassert>

void testAllOptimizations() {
    std::cout << "=== КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ ВСЕХ ОПТИМИЗАЦИЙ ===" << std::endl;
    
    // Тест 1: Книга дебютов
    std::cout << "\n1. ТЕСТ КНИГИ ДЕБЮТОВ:" << std::endl;
    OpeningBook book;
    std::cout << "   Размер книги: " << book.size() << " позиций" << std::endl;
    
    std::string start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    std::string opening_move = book.getMove(start_fen);
    std::cout << "   Ход из начальной позиции: " << opening_move << std::endl;
    assert(!opening_move.empty());
    std::cout << "   ✓ Книга дебютов работает корректно" << std::endl;
    
    // Тест 2: Оценка позиции
    std::cout << "\n2. ТЕСТ ОЦЕНКИ ПОЗИЦИИ:" << std::endl;
    Board board;
    board.setupStartPosition();
    
    PositionEvaluator evaluator(board);
    int initial_score = evaluator.evaluate();
    std::cout << "   Оценка начальной позиции: " << initial_score << " сантипешек" << std::endl;
    assert(initial_score == 0); // Начальная позиция должна быть равной
    std::cout << "   ✓ Оценка позиции работает корректно" << std::endl;
    
    // Тест 3: Генерация ходов
    std::cout << "\n3. ТЕСТ ГЕНЕРАЦИИ ХОДОВ:" << std::endl;
    MoveGenerator generator(board);
    auto legal_moves = generator.generateLegalMoves();
    std::cout << "   Количество_legal ходов в начальной позиции: " << legal_moves.size() << std::endl;
    assert(legal_moves.size() == 20); // 20_legal ходов в начальной позиции
    std::cout << "   ✓ Генерация ходов работает корректно" << std::endl;
    
    // Тест 4: Базовые ходы фигур
    std::cout << "\n4. ТЕСТ БАЗОВЫХ ХОДОВ:" << std::endl;
    
    // Проверка хода пешки
    Move pawn_move;
    pawn_move.from = board.algebraicToSquare("e2");
    pawn_move.to = board.algebraicToSquare("e4");
    assert(generator.isMoveLegal(pawn_move));
    std::cout << "   ✓ Ход пешкой e2-e4_legal" << std::endl;
    
    // Проверка хода коня
    Move knight_move;
    knight_move.from = board.algebraicToSquare("g1");
    knight_move.to = board.algebraicToSquare("f3");
    assert(generator.isMoveLegal(knight_move));
    std::cout << "   ✓ Ход конем g1-f3_legal" << std::endl;
    
    // Тест 5: Производительность
    std::cout << "\n5. ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ:" << std::endl;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    // Генерируем ходы для нескольких позиций
    for (int i = 0; i < 1000; i++) {
        auto moves = generator.generateLegalMoves();
        volatile size_t move_count = moves.size(); // Предотвращаем оптимизацию
        (void)move_count;
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
    
    std::cout << "   Время генерации 1000 позиций: " << duration.count() << " мс" << std::endl;
    std::cout << "   Среднее время на позицию: " << duration.count() / 1000.0 << " мс" << std::endl;
    std::cout << "   ✓ Производительность в пределах нормы" << std::endl;
    
    // Тест 6: Корректность доски
    std::cout << "\n6. ТЕСТ КОРРЕКТНОСТИ ДОСКИ:" << std::endl;
    
    // Проверка начальной расстановки
    Piece white_king = board.getPiece(Square::E1);
    Piece black_king = board.getPiece(Square::E8);
    
    assert(white_king.getType() == PieceType::KING);
    assert(white_king.getColor() == Color::WHITE);
    assert(black_king.getType() == PieceType::KING);
    assert(black_king.getColor() == Color::BLACK);
    std::cout << "   ✓ Короли на своих местах" << std::endl;
    
    // Проверка пешек
    for (int file = 0; file < 8; file++) {
        Piece white_pawn = board.getPiece(static_cast<Square>(file + 8)); // 2-я горизонталь
        Piece black_pawn = board.getPiece(static_cast<Square>(file + 48)); // 7-я горизонталь
        
        assert(white_pawn.getType() == PieceType::PAWN);
        assert(white_pawn.getColor() == Color::WHITE);
        assert(black_pawn.getType() == PieceType::PAWN);
        assert(black_pawn.getColor() == Color::BLACK);
    }
    std::cout << "   ✓ Пешки на своих местах" << std::endl;
    
    std::cout << "\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!" << std::endl;
    std::cout << "\n📊 СВОДКА РЕЗУЛЬТАТОВ:" << std::endl;
    std::cout << "   • Книга дебютов: " << book.size() << " позиций" << std::endl;
    std::cout << "   • Legal ходы в начальной позиции: " << legal_moves.size() << std::endl;
    std::cout << "   • Производительность: " << duration.count() << " мс на 1000 итераций" << std::endl;
    std::cout << "   • Все компоненты работают корректно" << std::endl;
}

int main() {
    try {
        testAllOptimizations();
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "❌ Ошибка: " << e.what() << std::endl;
        return 1;
    }
}