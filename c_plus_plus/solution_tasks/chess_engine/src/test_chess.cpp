#include "../include/board.hpp"
#include "../include/move_generator.hpp"
#include <iostream>

int main() {
    try {
        std::cout << "=== Тестирование шахматного движка ===" << std::endl;
        
        // Создаем доску
        Board board;
        std::cout << "Начальная позиция:" << std::endl;
        board.printBoard();
        
        // Создаем генератор ходов
        MoveGenerator generator(board);
        
        // Генерируем легальные ходы
        std::vector<Move> legalMoves = generator.generateLegalMoves();
        std::cout << "\nКоличество легальных ходов из начальной позиции: " 
                  << legalMoves.size() << std::endl;
        
        // Показываем первые 10 ходов
        std::cout << "\nПервые 10 легальных ходов:" << std::endl;
        for (size_t i = 0; i < std::min(legalMoves.size(), size_t(10)); i++) {
            const Move& move = legalMoves[i];
            std::cout << i + 1 << ". " << move.toString() << std::endl;
        }
        
        // Тестируем конкретные ходы
        std::cout << "\n=== Тестирование конкретных ходов ===" << std::endl;
        
        // Проверяем ход пешки e2-e4
        Square e2 = board.algebraicToSquare("e2");
        Square e4 = board.algebraicToSquare("e4");
        
        if (e2 != INVALID_SQUARE && e4 != INVALID_SQUARE) {
            Move pawnMove(e2, e4);
            bool isLegal = generator.isLegalMove(pawnMove);
            std::cout << "Ход e2-e4 легален: " << (isLegal ? "Да" : "Нет") << std::endl;
        }
        
        // Проверяем ход коня Ng1-f3
        Square g1 = board.algebraicToSquare("g1");
        Square f3 = board.algebraicToSquare("f3");
        
        if (g1 != INVALID_SQUARE && f3 != INVALID_SQUARE) {
            Move knightMove(g1, f3);
            bool isLegal = generator.isLegalMove(knightMove);
            std::cout << "Ход Ng1-f3 легален: " << (isLegal ? "Да" : "Нет") << std::endl;
        }
        
        std::cout << "\n=== Тест завершен успешно ===" << std::endl;
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Ошибка: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "Неизвестная ошибка!" << std::endl;
        return 1;
    }
}