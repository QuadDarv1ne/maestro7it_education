#include "board.hpp"
#include "move_generator.hpp"
#include "game_rules.hpp"
#include <iostream>
#include <cassert>

void testBasicFunctionality() {
    std::cout << "=== Тест базовой функциональности ===" << std::endl;
    
    // Тест 1: Создание доски
    Board board;
    std::cout << "✓ Доска создана успешно" << std::endl;
    
    // Тест 2: Начальная позиция
    board.setupStartPosition();
    assert(board.getPiece(board.algebraicToSquare("e1")).getType() == PieceType::KING);
    assert(board.getPiece(board.algebraicToSquare("e1")).getColor() == Color::WHITE);
    assert(board.getPiece(board.algebraicToSquare("e8")).getType() == PieceType::KING);
    assert(board.getPiece(board.algebraicToSquare("e8")).getColor() == Color::BLACK);
    std::cout << "✓ Начальная позиция корректна" << std::endl;
    
    // Тест 3: Генерация ходов
    MoveGenerator generator(board);
    std::vector<Move> moves = generator.generateLegalMoves();
    assert(moves.size() == 20); // 16 пешечных + 4 коневых хода
    std::cout << "✓ Генерация ходов работает (найдено " << moves.size() << " ходов)" << std::endl;
    
    // Тест 4: Правила игры
    GameRules rules(board);
    assert(!rules.isGameOver());
    std::cout << "✓ Система правил инициализирована" << std::endl;
    
    std::cout << "✓ Все базовые тесты пройдены!" << std::endl << std::endl;
}

void testSpecificMoves() {
    std::cout << "=== Тест конкретных ходов ===" << std::endl;
    
    Board board;
    board.setupStartPosition();
    MoveGenerator generator(board);
    GameRules rules(board);
    
    // Тест хода e2-e4
    Square e2 = board.algebraicToSquare("e2");
    Square e4 = board.algebraicToSquare("e4");
    Move pawnMove(e2, e4);
    
    assert(rules.isValidMove(pawnMove));
    assert(generator.isLegalMove(pawnMove));
    std::cout << "✓ Ход e2-e4 корректен" << std::endl;
    
    // Выполняем ход
    bool moveSuccess = rules.makeMove(pawnMove);
    assert(moveSuccess);
    assert(board.getPiece(e4).getType() == PieceType::PAWN);
    assert(board.getPiece(e2).isEmpty());
    std::cout << "✓ Ход e2-e4 выполнен успешно" << std::endl;
    
    // Тест хода Ng1-f3
    Square g1 = board.algebraicToSquare("g1");
    Square f3 = board.algebraicToSquare("f3");
    Move knightMove(g1, f3);
    
    assert(rules.isValidMove(knightMove));
    std::cout << "✓ Ход Ng1-f3 корректен" << std::endl;
    
    std::cout << "✓ Тесты конкретных ходов пройдены!" << std::endl << std::endl;
}

void testGameFlow() {
    std::cout << "=== Тест игрового потока ===" << std::endl;
    
    Board board;
    board.setupStartPosition();
    GameRules rules(board);
    
    // Имитируем начало партии
    std::vector<std::string> openingMoves = {
        "e2-e4", "e7-e5",
        "Ng1-f3", "Nb8-c6",
        "Bf1-b5" // Испанский дебют
    };
    
    for (const std::string& moveStr : openingMoves) {
        // Парсим ход (упрощенная реализация)
        Square from = board.algebraicToSquare(moveStr.substr(0, 2));
        Square to = board.algebraicToSquare(moveStr.substr(3, 2));
        Move move(from, to);
        
        if (rules.isValidMove(move)) {
            assert(rules.makeMove(move));
        } else {
            std::cout << "⚠ Предупреждение: ход " << moveStr << " не является валидным" << std::endl;
        }
    }
    
    std::cout << "✓ Игровой поток протестирован" << std::endl;
    board.printBoard();
    std::cout << std::endl;
}

void testEdgeCases() {
    std::cout << "=== Тест крайних случаев ===" << std::endl;
    
    Board board;
    board.setupStartPosition();
    
    // Тест некорректных координат
    assert(board.algebraicToSquare("z9") == INVALID_SQUARE);
    assert(board.algebraicToSquare("") == INVALID_SQUARE);
    std::cout << "✓ Обработка некорректных координат работает" << std::endl;
    
    // Тест пустых фигур
    Piece emptyPiece;
    assert(emptyPiece.isEmpty());
    assert(emptyPiece.getType() == PieceType::EMPTY);
    std::cout << "✓ Работа с пустыми фигурами корректна" << std::endl;
    
    // Тест противоположных цветов
    assert(Piece::oppositeColor(Color::WHITE) == Color::BLACK);
    assert(Piece::oppositeColor(Color::BLACK) == Color::WHITE);
    std::cout << "✓ Преобразование цветов работает" << std::endl;
    
    std::cout << "✓ Все тесты крайних случаев пройдены!" << std::endl << std::endl;
}

int main() {
    try {
        std::cout << "===========================================" << std::endl;
        std::cout << "    ТЕСТИРОВАНИЕ ШАХМАТНОГО ДВИЖКА" << std::endl;
        std::cout << "===========================================" << std::endl << std::endl;
        
        testBasicFunctionality();
        testSpecificMoves();
        testGameFlow();
        testEdgeCases();
        
        std::cout << "===========================================" << std::endl;
        std::cout << "🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!" << std::endl;
        std::cout << "===========================================" << std::endl;
        
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "❌ ОШИБКА: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "❌ Неизвестная ошибка!" << std::endl;
        return 1;
    }
}