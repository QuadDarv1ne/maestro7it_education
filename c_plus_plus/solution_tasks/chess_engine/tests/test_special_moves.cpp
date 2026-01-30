#include "../include/board.hpp"
#include "../include/move_generator.hpp"
#include "../include/game_rules.hpp"
#include <iostream>
#include <cassert>

void testCastling() {
    std::cout << "Testing castling moves..." << std::endl;
    
    // Test white kingside castling
    Board board;
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
    board.setPiece(board.square(7, 0), Piece(PieceType::ROOK, Color::WHITE));
    board.setCastlingRights(true, false, false, false);
    board.setCurrentPlayer(Color::WHITE);
    
    MoveGenerator moveGen(board);
    std::vector<Move> moves = moveGen.generateCastlingMoves();
    
    bool foundKingSideCastle = false;
    for (const Move& move : moves) {
        if (move.isCastling && board.file(move.to) == 6) {
            foundKingSideCastle = true;
            std::cout << "  ✓ White kingside castling detected" << std::endl;
            
            // Test execution
            board.makeMove(move);
            assert(board.getPiece(board.square(6, 0)).getType() == PieceType::KING);
            assert(board.getPiece(board.square(5, 0)).getType() == PieceType::ROOK);
            std::cout << "  ✓ White kingside castling executed correctly" << std::endl;
            board.undoMove();
            break;
        }
    }
    assert(foundKingSideCastle);
    
    // Test white queenside castling
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
    board.setPiece(board.square(0, 0), Piece(PieceType::ROOK, Color::WHITE));
    board.setCastlingRights(false, true, false, false);
    board.setCurrentPlayer(Color::WHITE);
    
    MoveGenerator moveGen2(board);
    moves = moveGen2.generateCastlingMoves();
    
    bool foundQueenSideCastle = false;
    for (const Move& move : moves) {
        if (move.isCastling && board.file(move.to) == 2) {
            foundQueenSideCastle = true;
            std::cout << "  ✓ White queenside castling detected" << std::endl;
            
            // Test execution
            board.makeMove(move);
            assert(board.getPiece(board.square(2, 0)).getType() == PieceType::KING);
            assert(board.getPiece(board.square(3, 0)).getType() == PieceType::ROOK);
            std::cout << "  ✓ White queenside castling executed correctly" << std::endl;
            board.undoMove();
            break;
        }
    }
    assert(foundQueenSideCastle);
    
    // Test black kingside castling
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 7), Piece(PieceType::KING, Color::BLACK));
    board.setPiece(board.square(7, 7), Piece(PieceType::ROOK, Color::BLACK));
    board.setCastlingRights(false, false, true, false);
    board.setCurrentPlayer(Color::BLACK);
    
    MoveGenerator moveGen3(board);
    moves = moveGen3.generateCastlingMoves();
    
    bool foundBlackKingSide = false;
    for (const Move& move : moves) {
        if (move.isCastling && board.file(move.to) == 6) {
            foundBlackKingSide = true;
            std::cout << "  ✓ Black kingside castling detected" << std::endl;
            
            // Test execution
            board.makeMove(move);
            assert(board.getPiece(board.square(6, 7)).getType() == PieceType::KING);
            assert(board.getPiece(board.square(5, 7)).getType() == PieceType::ROOK);
            std::cout << "  ✓ Black kingside castling executed correctly" << std::endl;
            board.undoMove();
            break;
        }
    }
    assert(foundBlackKingSide);
    
    // Test castling rights loss after king move
    board.setupStartPosition();
    Move kingMove;
    kingMove.from = board.square(4, 0);
    kingMove.to = board.square(4, 1);
    kingMove.isCastling = false;
    kingMove.isEnPassant = false;
    kingMove.promotion = PieceType::EMPTY;
    
    board.makeMove(kingMove);
    assert(!board.canCastleKingSide(Color::WHITE));
    assert(!board.canCastleQueenSide(Color::WHITE));
    std::cout << "  ✓ Castling rights removed after king move" << std::endl;
    
    std::cout << "✓ All castling tests passed!" << std::endl << std::endl;
}

void testEnPassant() {
    std::cout << "Testing en passant moves..." << std::endl;
    
    // Test white en passant
    Board board;
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 4), Piece(PieceType::PAWN, Color::WHITE));
    board.setPiece(board.square(5, 4), Piece(PieceType::PAWN, Color::BLACK));
    board.setEnPassantSquare(board.square(5, 5)); // Black pawn just moved from 5,6 to 5,4
    board.setCurrentPlayer(Color::WHITE);
    
    MoveGenerator moveGen(board);
    std::vector<Move> moves = moveGen.generateEnPassantMoves();
    
    bool foundEnPassant = false;
    for (const Move& move : moves) {
        if (move.isEnPassant && move.from == board.square(4, 4) && move.to == board.square(5, 5)) {
            foundEnPassant = true;
            std::cout << "  ✓ White en passant move detected" << std::endl;
            
            // Test execution
            board.makeMove(move);
            assert(board.getPiece(board.square(5, 5)).getType() == PieceType::PAWN);
            assert(board.getPiece(board.square(5, 4)).isEmpty());
            assert(board.getPiece(board.square(4, 4)).isEmpty());
            std::cout << "  ✓ White en passant executed correctly (captured pawn removed)" << std::endl;
            board.undoMove();
            break;
        }
    }
    assert(foundEnPassant);
    
    // Test black en passant
    board.initializeEmptyBoard();
    board.setPiece(board.square(3, 3), Piece(PieceType::PAWN, Color::BLACK));
    board.setPiece(board.square(2, 3), Piece(PieceType::PAWN, Color::WHITE));
    board.setEnPassantSquare(board.square(2, 2)); // White pawn just moved from 2,1 to 2,3
    board.setCurrentPlayer(Color::BLACK);
    
    MoveGenerator moveGen2(board);
    moves = moveGen2.generateEnPassantMoves();
    
    bool foundBlackEnPassant = false;
    for (const Move& move : moves) {
        if (move.isEnPassant && move.from == board.square(3, 3) && move.to == board.square(2, 2)) {
            foundBlackEnPassant = true;
            std::cout << "  ✓ Black en passant move detected" << std::endl;
            
            // Test execution
            board.makeMove(move);
            assert(board.getPiece(board.square(2, 2)).getType() == PieceType::PAWN);
            assert(board.getPiece(board.square(2, 3)).isEmpty());
            assert(board.getPiece(board.square(3, 3)).isEmpty());
            std::cout << "  ✓ Black en passant executed correctly (captured pawn removed)" << std::endl;
            board.undoMove();
            break;
        }
    }
    assert(foundBlackEnPassant);
    
    // Test en passant square setting after pawn double move
    board.setupStartPosition();
    Move pawnDoubleMove;
    pawnDoubleMove.from = board.square(4, 1);
    pawnDoubleMove.to = board.square(4, 3);
    pawnDoubleMove.isCastling = false;
    pawnDoubleMove.isEnPassant = false;
    pawnDoubleMove.promotion = PieceType::EMPTY;
    
    board.makeMove(pawnDoubleMove);
    assert(board.getEnPassantSquare() == board.square(4, 2));
    std::cout << "  ✓ En passant square set correctly after pawn double move" << std::endl;
    
    std::cout << "✓ All en passant tests passed!" << std::endl << std::endl;
}

void testPawnPromotion() {
    std::cout << "Testing pawn promotion..." << std::endl;
    
    // Test white pawn promotion to queen
    Board board;
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 6), Piece(PieceType::PAWN, Color::WHITE));
    board.setCurrentPlayer(Color::WHITE);
    
    Move promoteToQueen;
    promoteToQueen.from = board.square(4, 6);
    promoteToQueen.to = board.square(4, 7);
    promoteToQueen.isCastling = false;
    promoteToQueen.isEnPassant = false;
    promoteToQueen.promotion = PieceType::QUEEN;
    
    board.makeMove(promoteToQueen);
    assert(board.getPiece(board.square(4, 7)).getType() == PieceType::QUEEN);
    assert(board.getPiece(board.square(4, 7)).getColor() == Color::WHITE);
    std::cout << "  ✓ White pawn promoted to queen" << std::endl;
    board.undoMove();
    
    // Test white pawn promotion to knight
    Move promoteToKnight;
    promoteToKnight.from = board.square(4, 6);
    promoteToKnight.to = board.square(4, 7);
    promoteToKnight.isCastling = false;
    promoteToKnight.isEnPassant = false;
    promoteToKnight.promotion = PieceType::KNIGHT;
    
    board.makeMove(promoteToKnight);
    assert(board.getPiece(board.square(4, 7)).getType() == PieceType::KNIGHT);
    std::cout << "  ✓ White pawn promoted to knight" << std::endl;
    board.undoMove();
    
    // Test black pawn promotion
    board.initializeEmptyBoard();
    board.setPiece(board.square(3, 1), Piece(PieceType::PAWN, Color::BLACK));
    board.setCurrentPlayer(Color::BLACK);
    
    Move blackPromoteToQueen;
    blackPromoteToQueen.from = board.square(3, 1);
    blackPromoteToQueen.to = board.square(3, 0);
    blackPromoteToQueen.isCastling = false;
    blackPromoteToQueen.isEnPassant = false;
    blackPromoteToQueen.promotion = PieceType::QUEEN;
    
    board.makeMove(blackPromoteToQueen);
    assert(board.getPiece(board.square(3, 0)).getType() == PieceType::QUEEN);
    assert(board.getPiece(board.square(3, 0)).getColor() == Color::BLACK);
    std::cout << "  ✓ Black pawn promoted to queen" << std::endl;
    board.undoMove();
    
    // Test promotion with capture
    board.initializeEmptyBoard();
    board.setPiece(board.square(4, 6), Piece(PieceType::PAWN, Color::WHITE));
    board.setPiece(board.square(5, 7), Piece(PieceType::ROOK, Color::BLACK));
    board.setCurrentPlayer(Color::WHITE);
    
    Move promoteWithCapture;
    promoteWithCapture.from = board.square(4, 6);
    promoteWithCapture.to = board.square(5, 7);
    promoteWithCapture.isCastling = false;
    promoteWithCapture.isEnPassant = false;
    promoteWithCapture.promotion = PieceType::QUEEN;
    
    board.makeMove(promoteWithCapture);
    assert(board.getPiece(board.square(5, 7)).getType() == PieceType::QUEEN);
    assert(board.getPiece(board.square(5, 7)).getColor() == Color::WHITE);
    std::cout << "  ✓ Pawn promotion with capture works correctly" << std::endl;
    
    std::cout << "✓ All pawn promotion tests passed!" << std::endl << std::endl;
}

int main() {
    std::cout << "=== Special Moves Test Suite ===" << std::endl << std::endl;
    
    try {
        testCastling();
        testEnPassant();
        testPawnPromotion();
        
        std::cout << "=== All special move tests passed! ===" << std::endl;
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "Test failed with exception: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "Test failed with unknown exception" << std::endl;
        return 1;
    }
}
