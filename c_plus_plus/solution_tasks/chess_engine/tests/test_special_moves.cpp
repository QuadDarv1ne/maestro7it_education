/**
 * @file test_special_moves.cpp
 * @brief Тесты специальных ходов (рокировка, взятие на проходе, превращение)
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

void testBasicCastling() {
    printTestHeader("Basic Castling");
    
    Board board;
    GameRules rules(board);
    
    // Начальная позиция - короткая рокировка должна быть возможна
    board.setupStartPosition();
    board.setCurrentPlayer(Color::WHITE);
    
    // Проверяем, что рокировка возможна
    MoveGenerator moveGen(board);
    std::vector<Move> moves = moveGen.generateLegalMoves();
    
    bool kingsideCastleAvailable = false;
    bool queensideCastleAvailable = false;
    
    for (const Move& move : moves) {
        if (move.from == board.square(4, 0) && move.to == board.square(6, 0)) {
            kingsideCastleAvailable = move.isCastling;
        }
        if (move.from == board.square(4, 0) && move.to == board.square(2, 0)) {
            queensideCastleAvailable = move.isCastling;
        }
    }
    
    assert(kingsideCastleAvailable == true);
    assert(queensideCastleAvailable == true);
    std::cout << "✓ Both castling options available in starting position" << std::endl;
}

void testCastlingBlockedByPieces() {
    printTestHeader("Castling Blocked by Pieces");
    
    Board board;
    GameRules rules(board);
    
    // Белый король на e1, ладьи на a1 и h1, но между ними фигуры
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));  // Ke1
    board.setPiece(board.square(0, 0), Piece(PieceType::ROOK, Color::WHITE));  // Ra1
    board.setPiece(board.square(7, 0), Piece(PieceType::ROOK, Color::WHITE));  // Rh1
    board.setPiece(board.square(1, 0), Piece(PieceType::KNIGHT, Color::WHITE)); // Nb1
    board.setPiece(board.square(5, 0), Piece(PieceType::BISHOP, Color::WHITE)); // Bf1
    board.setCurrentPlayer(Color::WHITE);
    
    MoveGenerator moveGen(board);
    std::vector<Move> moves = moveGen.generateLegalMoves();
    
    bool kingsideCastleAvailable = false;
    bool queensideCastleAvailable = false;
    
    for (const Move& move : moves) {
        if (move.from == board.square(4, 0) && move.to == board.square(6, 0)) {
            kingsideCastleAvailable = move.isCastling;
        }
        if (move.from == board.square(4, 0) && move.to == board.square(2, 0)) {
            queensideCastleAvailable = move.isCastling;
        }
    }
    
    assert(kingsideCastleAvailable == false);
    assert(queensideCastleAvailable == false);
    std::cout << "✓ Castling blocked by pieces between king and rook" << std::endl;
}

void testCastlingAfterKingMoved() {
    printTestHeader("Castling After King Moved");
    
    Board board;
    GameRules rules(board);
    
    // Король уже ходил, потом вернулся
    board.setupStartPosition();
    board.setCurrentPlayer(Color::WHITE);
    
    // Сделаем ход королем и обратно
    rules.makeMove("e1e2");  // Ke1-e2
    rules.makeMove("e7e5");  // черные ходят
    rules.makeMove("e2e1");  // Ke2-e1
    
    MoveGenerator moveGen(board);
    std::vector<Move> moves = moveGen.generateLegalMoves();
    
    bool kingsideCastleAvailable = false;
    bool queensideCastleAvailable = false;
    
    for (const Move& move : moves) {
        if (move.from == board.square(4, 0) && move.to == board.square(6, 0)) {
            kingsideCastleAvailable = move.isCastling;
        }
        if (move.from == board.square(4, 0) && move.to == board.square(2, 0)) {
            queensideCastleAvailable = move.isCastling;
        }
    }
    
    assert(kingsideCastleAvailable == false);
    assert(queensideCastleAvailable == false);
    std::cout << "✓ No castling after king has moved" << std::endl;
}

void testEnPassantCapture() {
    printTestHeader("En Passant Capture");
    
    Board board;
    GameRules rules(board);
    
    // Позиция для взятия на проходе: белая пешка на e5, черная пешка на d7
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 4), Piece(PieceType::PAWN, Color::WHITE));  // Pe5
    board.setPiece(board.square(3, 6), Piece(PieceType::PAWN, Color::BLACK));  // Pd7
    board.setCurrentPlayer(Color::BLACK);
    
    // Черные делают двойной ход пешкой
    rules.makeMove("d7d5");
    
    // Теперь белые могут взять на проходе
    MoveGenerator moveGen(board);
    std::vector<Move> moves = moveGen.generateLegalMoves();
    
    bool enPassantAvailable = false;
    for (const Move& move : moves) {
        if (move.from == board.square(4, 4) && move.to == board.square(3, 5)) {
            enPassantAvailable = move.isEnPassant;
        }
    }
    
    assert(enPassantAvailable == true);
    std::cout << "✓ En passant capture available after double pawn move" << std::endl;
    
    // Выполним взятие на проходе
    bool moveSuccess = rules.makeMove("e5d6");  // exd6 en passant
    assert(moveSuccess == true);
    
    // Проверим, что пешка исчезла
    assert(board.getPiece(board.square(3, 5)).isEmpty() == true);  // d6 пусто
    assert(board.getPiece(board.square(3, 4)).isEmpty() == true);  // d5 пусто (взятая пешка)
    assert(board.getPiece(board.square(3, 6)).isEmpty() == true);  // d7 пусто (ушла)
    std::cout << "✓ En passant capture executed correctly" << std::endl;
}

void testPawnPromotion() {
    printTestHeader("Pawn Promotion");
    
    Board board;
    GameRules rules(board);
    
    // Белая пешка на 7-й горизонтали
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 6), Piece(PieceType::PAWN, Color::WHITE));  // Pe7
    board.setPiece(board.square(4, 7), Piece(PieceType::KING, Color::BLACK));  // Ke8
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));  // Ke1
    board.setCurrentPlayer(Color::WHITE);
    
    // Сделаем ход пешкой на последнюю горизонталь
    bool moveSuccess = rules.makeMove("e7e8q");  // Pe7-e8=Q
    assert(moveSuccess == true);
    
    // Проверим, что пешка превратилась в ферзя
    Piece piece = board.getPiece(board.square(4, 7));
    assert(piece.getType() == PieceType::QUEEN);
    assert(piece.getColor() == Color::WHITE);
    std::cout << "✓ Pawn promoted to queen successfully" << std::endl;
    
    // Проверим другие варианты превращения
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 6), Piece(PieceType::PAWN, Color::WHITE));
    board.setPiece(board.square(4, 7), Piece(PieceType::KING, Color::BLACK));
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
    board.setCurrentPlayer(Color::WHITE);
    
    // Превращение в ладью
    moveSuccess = rules.makeMove("e7e8r");
    assert(moveSuccess == true);
    piece = board.getPiece(board.square(4, 7));
    assert(piece.getType() == PieceType::ROOK);
    std::cout << "✓ Pawn promoted to rook successfully" << std::endl;
}

void testInvalidPromotion() {
    printTestHeader("Invalid Promotion");
    
    Board board;
    GameRules rules(board);
    
    // Пешка не на последней горизонтали
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 5), Piece(PieceType::PAWN, Color::WHITE));  // Pe6
    board.setPiece(board.square(4, 7), Piece(PieceType::KING, Color::BLACK));
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
    board.setCurrentPlayer(Color::WHITE);
    
    // Попытка превращения не на последней горизонтали
    bool moveSuccess = rules.makeMove("e6e7q");
    assert(moveSuccess == false);
    std::cout << "✓ Invalid promotion rejected" << std::endl;
}

void runAllTests() {
    std::cout << "Running Special Moves Tests..." << std::endl;
    
    try {
        testBasicCastling();
        testCastlingBlockedByPieces();
        testCastlingAfterKingMoved();
        testEnPassantCapture();
        testPawnPromotion();
        testInvalidPromotion();
        
        std::cout << "\n🎉 All Special Moves tests passed!" << std::endl;
    } catch (const std::exception& e) {
        std::cerr << "❌ Test failed: " << e.what() << std::endl;
        exit(1);
    }
}

int main() {
    runAllTests();
    return 0;
}