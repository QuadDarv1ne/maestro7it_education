/**
 * @file test_game_states.cpp
 * @brief Тесты базовых состояний игры (шах, мат, пат)
 */

#include "../include/board.hpp"
#include "../include/game_rules.hpp"
#include "../include/move_generator.hpp"
#include <iostream>
#include <cassert>
#include <string>

void printTestHeader(const std::string& testName) {
    std::cout << "\n=== " << testName << " ===" << std::endl;
}

void testBasicCheckDetection() {
    printTestHeader("Basic Check Detection");
    
    Board board;
    GameRules rules(board);
    
    // Позиция: белый король на e1, черная ладья на e8
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));  // Ke1
    board.setPiece(board.square(4, 7), Piece(PieceType::ROOK, Color::BLACK));  // Re8
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isCheck(Color::WHITE) == true);
    std::cout << "✓ White king is in check" << std::endl;
    
    // Позиция: белый король на e1, черная ладья на a1 (не атакует)
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));  // Ke1
    board.setPiece(board.square(0, 0), Piece(PieceType::ROOK, Color::BLACK));  // Ra1
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isCheck(Color::WHITE) == false);
    std::cout << "✓ White king is not in check" << std::endl;
}

void testCheckmateDetection() {
    printTestHeader("Checkmate Detection");
    
    Board board;
    GameRules rules(board);
    
    // Классический мат ладьей: Kg1, Rg2, Kh1
    board.initializeEmptyBoard();
    board.setPiece(board.square(6, 0), Piece(PieceType::KING, Color::WHITE));  // Kg1
    board.setPiece(board.square(6, 1), Piece(PieceType::ROOK, Color::BLACK));  // Rg2
    board.setPiece(board.square(7, 0), Piece(PieceType::KING, Color::BLACK));  // Kh1
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isCheck(Color::WHITE) == true);
    assert(rules.isCheckmate(Color::WHITE) == true);
    std::cout << "✓ Classic back rank mate detected" << std::endl;
    
    // Позиция без мата (король может уйти)
    board.initializeEmptyBoard();
    board.setPiece(board.square(6, 0), Piece(PieceType::KING, Color::WHITE));  // Kg1
    board.setPiece(board.square(7, 2), Piece(PieceType::ROOK, Color::BLACK));  // Rh3
    board.setPiece(board.square(7, 0), Piece(PieceType::KING, Color::BLACK));  // Kh1
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isCheck(Color::WHITE) == true);
    assert(rules.isCheckmate(Color::WHITE) == false);
    std::cout << "✓ Check without mate detected" << std::endl;
}

void testStalemateDetection() {
    printTestHeader("Stalemate Detection");
    
    Board board;
    GameRules rules(board);
    
    // Классический пат: Kb1, Qa2, Ka1
    board.initializeEmptyBoard();
    board.setPiece(board.square(1, 0), Piece(PieceType::KING, Color::WHITE));  // Kb1
    board.setPiece(board.square(0, 1), Piece(PieceType::QUEEN, Color::BLACK)); // Qa2
    board.setPiece(board.square(0, 0), Piece(PieceType::KING, Color::BLACK));  // Ka1
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isCheck(Color::WHITE) == false);
    assert(rules.isStalemate(Color::WHITE) == true);
    std::cout << "✓ Classic stalemate detected" << std::endl;
    
    // Позиция без пата (есть легальные ходы)
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));  // Ke1
    board.setPiece(board.square(0, 1), Piece(PieceType::QUEEN, Color::BLACK)); // Qa2
    board.setPiece(board.square(0, 0), Piece(PieceType::KING, Color::BLACK));  // Ka1
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isCheck(Color::WHITE) == false);
    assert(rules.isStalemate(Color::WHITE) == false);
    std::cout << "✓ Not stalemate when moves available" << std::endl;
}

void testInsufficientMaterial() {
    printTestHeader("Insufficient Material Detection");
    
    Board board;
    GameRules rules(board);
    
    // Только короли
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
    board.setPiece(board.square(4, 7), Piece(PieceType::KING, Color::BLACK));
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isInsufficientMaterial() == true);
    std::cout << "✓ King vs King - insufficient material" << std::endl;
    
    // Король + слон против короля
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
    board.setPiece(board.square(4, 7), Piece(PieceType::KING, Color::BLACK));
    board.setPiece(board.square(3, 3), Piece(PieceType::BISHOP, Color::WHITE));
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isInsufficientMaterial() == true);
    std::cout << "✓ King + Bishop vs King - insufficient material" << std::endl;
    
    // Король + слон против короля + слон (одноцветные)
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
    board.setPiece(board.square(4, 7), Piece(PieceType::KING, Color::BLACK));
    board.setPiece(board.square(2, 2), Piece(PieceType::BISHOP, Color::WHITE));  // Чернопольный
    board.setPiece(board.square(5, 5), Piece(PieceType::BISHOP, Color::BLACK));  // Чернопольный
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isInsufficientMaterial() == true);
    std::cout << "✓ Same-colored bishops - insufficient material" << std::endl;
    
    // Достаточный материал (ферзь)
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
    board.setPiece(board.square(4, 7), Piece(PieceType::KING, Color::BLACK));
    board.setPiece(board.square(3, 3), Piece(PieceType::QUEEN, Color::WHITE));
    board.setCurrentPlayer(Color::WHITE);
    
    assert(rules.isInsufficientMaterial() == false);
    std::cout << "✓ Queen present - sufficient material" << std::endl;
}

void testDrawByRepetition() {
    printTestHeader("Draw by Repetition");
    
    Board board;
    GameRules rules(board);
    
    // Начальная позиция - должна быть 0 повторений
    board.setupStartPosition();
    assert(rules.isDrawByRepetition() == false);
    std::cout << "✓ Starting position - no repetition" << std::endl;
    
    // TODO: Добавить тест с реальным повторением позиции
    // Это требует реализации нескольких ходов туда-обратно
}

void testDrawByFiftyMoveRule() {
    printTestHeader("Draw by Fifty Move Rule");
    
    Board board;
    GameRules rules(board);
    
    // Новая доска - счетчик 0
    board.initializeEmptyBoard();
    board.setupStartPosition();
    assert(rules.isDrawByFiftyMoveRule() == false);
    std::cout << "✓ Fresh game - not 50 moves yet" << std::endl;
    
    // Установим счетчик на 99 (еще не 50 ходов)
    board.setHalfMoveClock(99);
    assert(rules.isDrawByFiftyMoveRule() == false);
    std::cout << "✓ 99 half-moves - not yet 50 moves" << std::endl;
    
    // Установим счетчик на 100 (50 полных ходов)
    board.setHalfMoveClock(100);
    assert(rules.isDrawByFiftyMoveRule() == true);
    std::cout << "✓ 100 half-moves - 50 move rule triggered" << std::endl;
}

void runAllTests() {
    std::cout << "Running Game States Tests..." << std::endl;
    
    try {
        testBasicCheckDetection();
        testCheckmateDetection();
        testStalemateDetection();
        testInsufficientMaterial();
        testDrawByRepetition();
        testDrawByFiftyMoveRule();
        
        std::cout << "\n🎉 All Game States tests passed!" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "❌ Test failed: " << e.what() << std::endl;
        exit(1);
    }
}

int main() {
    runAllTests();
    return 0;
}