#include "../include/board.hpp"
#include "../include/move_generator.hpp"
#include <iostream>

int main() {
    try {
        std::cout << "=== CHESS ENGINE TESTING ===" << std::endl;
        
        // Создаем доску
        Board board;
        std::cout << "Starting position:" << std::endl;
        board.printBoard();
        
        // Создаем генератор ходов
        MoveGenerator generator(board);
        
        // Генерируем легальные ходы
        std::vector<Move> legalMoves = generator.generateLegalMoves();
        std::cout << "\nNumber of legal moves from starting position: " 
                  << legalMoves.size() << std::endl;
        
        // Показываем первые 10 ходов
        std::cout << "\nFirst 10 legal moves:" << std::endl;
        for (size_t i = 0; i < std::min(legalMoves.size(), size_t(10)); i++) {
            const Move& move = legalMoves[i];
            std::cout << i + 1 << ". " << move.toString() << std::endl;
        }
        
        // Тестируем конкретные ходы
        std::cout << "\n=== TESTING SPECIFIC MOVES ===" << std::endl;
        
        // Проверяем ход пешки e2-e4
        Square e2 = board.algebraicToSquare("e2");
        Square e4 = board.algebraicToSquare("e4");
        
        if (e2 != INVALID_SQUARE && e4 != INVALID_SQUARE) {
            Move pawnMove(e2, e4);
            bool isLegal = generator.isLegalMove(pawnMove);
            std::cout << "Move e2-e4 is legal: " << (isLegal ? "Yes" : "No") << std::endl;
        }
        
        // Проверяем ход коня Ng1-f3
        Square g1 = board.algebraicToSquare("g1");
        Square f3 = board.algebraicToSquare("f3");
        
        if (g1 != INVALID_SQUARE && f3 != INVALID_SQUARE) {
            Move knightMove(g1, f3);
            bool isLegal = generator.isLegalMove(knightMove);
            std::cout << "Move Ng1-f3 is legal: " << (isLegal ? "Yes" : "No") << std::endl;
        }
        
        std::cout << "\n=== TEST COMPLETED SUCCESSFULLY ===" << std::endl;
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "Unknown error!" << std::endl;
        return 1;
    }
}