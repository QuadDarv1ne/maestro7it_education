#include "../include/board.hpp"
#include "../include/move_generator.hpp"
#include "../include/game_rules.hpp"
#include <iostream>
#include <cassert>
#include <vector>
#include <chrono>

class SpecialMoveTestSuite {
private:
    int passed = 0;
    int total = 0;
    std::vector<std::string> failures;

public:
    template<typename Func>
    void test(const std::string& name, Func func) {
        total++;
        std::cout << "🧪 " << name << " ... ";
        
        try {
            auto start = std::chrono::high_resolution_clock::now();
            func();
            auto end = std::chrono::high_resolution_clock::now();
            
            auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
            std::cout << "✅ PASSED (" << duration.count() << "μs)" << std::endl;
            passed++;
        } catch (const std::exception& e) {
            std::cout << "❌ FAILED: " << e.what() << std::endl;
            failures.push_back(name + ": " + e.what());
        }
    }

    void printResults() {
        std::cout << "\n" << std::string(60, '=') << std::endl;
        std::cout << "SPECIAL MOVES TEST RESULTS" << std::endl;
        std::cout << std::string(60, '=') << std::endl;
        std::cout << "✅ Passed: " << passed << "/" << total << std::endl;
        std::cout << "成功率: " << (total > 0 ? (passed * 100.0 / total) : 0) << "%" << std::endl;
        
        if (!failures.empty()) {
            std::cout << "\n❌ Failed tests:" << std::endl;
            for (const auto& failure : failures) {
                std::cout << "  • " << failure << std::endl;
            }
        }
        std::cout << std::string(60, '=') << std::endl;
    }
};

// CASTLING TESTS
void testCastlingScenarios(SpecialMoveTestSuite& suite) {
    suite.test("White Kingside Castling", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(7, 0), Piece(PieceType::ROOK, Color::WHITE));
        board.setCastlingRights(true, false, false, false);
        board.setCurrentPlayer(Color::WHITE);
        
        MoveGenerator mg(board);
        auto moves = mg.generateCastlingMoves();
        
        bool found = false;
        for (const auto& move : moves) {
            if (move.isCastling && board.file(move.to) == 6) {
                found = true;
                // Execute and verify
                board.makeMove(move);
                assert(board.getPiece(board.square(6, 0)).getType() == PieceType::KING);
                assert(board.getPiece(board.square(5, 0)).getType() == PieceType::ROOK);
                break;
            }
        }
        assert(found);
    });

    suite.test("White Queenside Castling", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(0, 0), Piece(PieceType::ROOK, Color::WHITE));
        board.setCastlingRights(false, true, false, false);
        board.setCurrentPlayer(Color::WHITE);
        
        MoveGenerator mg(board);
        auto moves = mg.generateCastlingMoves();
        
        bool found = false;
        for (const auto& move : moves) {
            if (move.isCastling && board.file(move.to) == 2) {
                found = true;
                board.makeMove(move);
                assert(board.getPiece(board.square(2, 0)).getType() == PieceType::KING);
                assert(board.getPiece(board.square(3, 0)).getType() == PieceType::ROOK);
                break;
            }
        }
        assert(found);
    });

    suite.test("Castling Rights Loss - King Move", []() {
        Board board;
        board.setupStartPosition();
        
        Move kingMove{{4, 0}, {4, 1}, false, false, PieceType::EMPTY};
        board.makeMove(kingMove);
        
        assert(!board.canCastleKingSide(Color::WHITE));
        assert(!board.canCastleQueenSide(Color::WHITE));
    });

    suite.test("Castling Rights Loss - Rook Move", []() {
        Board board;
        board.setupStartPosition();
        
        Move rookMove{{7, 0}, {6, 0}, false, false, PieceType::EMPTY};
        board.makeMove(rookMove);
        
        assert(!board.canCastleKingSide(Color::WHITE));
        assert(board.canCastleQueenSide(Color::WHITE));
    });

    suite.test("Castling Blocked by Pieces", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(7, 0), Piece(PieceType::ROOK, Color::WHITE));
        board.setPiece(board.square(5, 0), Piece(PieceType::BISHOP, Color::WHITE)); // Blocking piece
        board.setCastlingRights(true, false, false, false);
        board.setCurrentPlayer(Color::WHITE);
        
        MoveGenerator mg(board);
        auto moves = mg.generateCastlingMoves();
        
        // Should not find kingside castling due to blocker
        for (const auto& move : moves) {
            if (move.isCastling && board.file(move.to) == 6) {
                assert(false); // Should not reach here
            }
        }
    });

    suite.test("Castling Through Check", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(7, 0), Piece(PieceType::ROOK, Color::WHITE));
        board.setPiece(board.square(5, 7), Piece(PieceType::ROOK, Color::BLACK)); // Attacking square
        board.setCastlingRights(true, false, false, false);
        board.setCurrentPlayer(Color::WHITE);
        
        MoveGenerator mg(board);
        auto moves = mg.generateCastlingMoves();
        
        // Should not be able to castle through attacked square
        for (const auto& move : moves) {
            if (move.isCastling && board.file(move.to) == 6) {
                assert(false); // Should not be possible
            }
        }
    });
}

// EN PASSANT TESTS
void testEnPassantScenarios(SpecialMoveTestSuite& suite) {
    suite.test("Standard White En Passant", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 4), Piece(PieceType::PAWN, Color::WHITE));
        board.setPiece(board.square(5, 4), Piece(PieceType::PAWN, Color::BLACK));
        board.setEnPassantSquare(board.square(5, 5));
        board.setCurrentPlayer(Color::WHITE);
        
        MoveGenerator mg(board);
        auto moves = mg.generateEnPassantMoves();
        
        bool found = false;
        for (const auto& move : moves) {
            if (move.isEnPassant && move.to == board.square(5, 5)) {
                found = true;
                board.makeMove(move);
                // Verify capture
                assert(board.getPiece(board.square(5, 5)).getType() == PieceType::PAWN);
                assert(board.getPiece(board.square(5, 4)).isEmpty());
                assert(board.getPiece(board.square(4, 4)).isEmpty());
                break;
            }
        }
        assert(found);
    });

    suite.test("Standard Black En Passant", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(3, 3), Piece(PieceType::PAWN, Color::BLACK));
        board.setPiece(board.square(2, 3), Piece(PieceType::PAWN, Color::WHITE));
        board.setEnPassantSquare(board.square(2, 2));
        board.setCurrentPlayer(Color::BLACK);
        
        MoveGenerator mg(board);
        auto moves = mg.generateEnPassantMoves();
        
        bool found = false;
        for (const auto& move : moves) {
            if (move.isEnPassant && move.to == board.square(2, 2)) {
                found = true;
                board.makeMove(move);
                assert(board.getPiece(board.square(2, 2)).getType() == PieceType::PAWN);
                assert(board.getPiece(board.square(2, 3)).isEmpty());
                assert(board.getPiece(board.square(3, 3)).isEmpty());
                break;
            }
        }
        assert(found);
    });

    suite.test("En Passant Square Setting", []() {
        Board board;
        board.setupStartPosition();
        
        Move doubleMove{{4, 1}, {4, 3}, false, false, PieceType::EMPTY};
        board.makeMove(doubleMove);
        
        assert(board.getEnPassantSquare() == board.square(4, 2));
    });

    suite.test("En Passant Expired", []() {
        Board board;
        board.setupStartPosition();
        
        // Make pawn double move
        Move doubleMove{{4, 1}, {4, 3}, false, false, PieceType::EMPTY};
        board.makeMove(doubleMove);
        assert(board.getEnPassantSquare() == board.square(4, 2));
        
        // Make another move (should expire en passant)
        Move otherMove{{6, 0}, {5, 2}, false, false, PieceType::EMPTY};
        board.makeMove(otherMove);
        
        assert(board.getEnPassantSquare() == Board::NO_SQUARE);
    });

    suite.test("Invalid En Passant - Wrong Turn", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 4), Piece(PieceType::PAWN, Color::WHITE));
        board.setPiece(board.square(5, 4), Piece(PieceType::PAWN, Color::BLACK));
        board.setEnPassantSquare(board.square(5, 5));
        board.setCurrentPlayer(Color::BLACK); // Wrong player
        
        MoveGenerator mg(board);
        auto moves = mg.generateEnPassantMoves();
        
        // Should not generate en passant for wrong player
        for (const auto& move : moves) {
            if (move.isEnPassant) {
                assert(false); // Should not be generated
            }
        }
    });
}

// PAWN PROMOTION TESTS
void testPromotionScenarios(SpecialMoveTestSuite& suite) {
    suite.test("White Pawn Promotion to Queen", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 6), Piece(PieceType::PAWN, Color::WHITE));
        board.setCurrentPlayer(Color::WHITE);
        
        Move promoMove{{4, 6}, {4, 7}, false, false, PieceType::QUEEN};
        board.makeMove(promoMove);
        
        assert(board.getPiece(board.square(4, 7)).getType() == PieceType::QUEEN);
        assert(board.getPiece(board.square(4, 7)).getColor() == Color::WHITE);
    });

    suite.test("White Pawn Promotion to Knight", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(3, 6), Piece(PieceType::PAWN, Color::WHITE));
        board.setCurrentPlayer(Color::WHITE);
        
        Move promoMove{{3, 6}, {3, 7}, false, false, PieceType::KNIGHT};
        board.makeMove(promoMove);
        
        assert(board.getPiece(board.square(3, 7)).getType() == PieceType::KNIGHT);
    });

    suite.test("Black Pawn Promotion", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(2, 1), Piece(PieceType::PAWN, Color::BLACK));
        board.setCurrentPlayer(Color::BLACK);
        
        Move promoMove{{2, 1}, {2, 0}, false, false, PieceType::QUEEN};
        board.makeMove(promoMove);
        
        assert(board.getPiece(board.square(2, 0)).getType() == PieceType::QUEEN);
        assert(board.getPiece(board.square(2, 0)).getColor() == Color::BLACK);
    });

    suite.test("Promotion with Capture", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 6), Piece(PieceType::PAWN, Color::WHITE));
        board.setPiece(board.square(5, 7), Piece(PieceType::ROOK, Color::BLACK));
        board.setCurrentPlayer(Color::WHITE);
        
        Move promoCapture{{4, 6}, {5, 7}, false, false, PieceType::QUEEN};
        board.makeMove(promoCapture);
        
        assert(board.getPiece(board.square(5, 7)).getType() == PieceType::QUEEN);
        assert(board.getPiece(board.square(5, 7)).getColor() == Color::WHITE);
    });

    suite.test("Multiple Promotion Options Generation", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(0, 6), Piece(PieceType::PAWN, Color::WHITE));
        board.setCurrentPlayer(Color::WHITE);
        
        MoveGenerator mg(board);
        auto moves = mg.generateLegalMoves();
        
        int promotionCount = 0;
        for (const auto& move : moves) {
            if (move.promotion != PieceType::EMPTY) {
                promotionCount++;
                // Should be promoting to Q, R, B, N
                assert(move.promotion == PieceType::QUEEN || 
                       move.promotion == PieceType::ROOK ||
                       move.promotion == PieceType::BISHOP ||
                       move.promotion == PieceType::KNIGHT);
            }
        }
        
        // Should have 4 promotion options (one for each piece type)
        assert(promotionCount >= 4);
    });
}

// EDGE CASE TESTS
void testEdgeCases(SpecialMoveTestSuite& suite) {
    suite.test("Castling Into Check", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(7, 0), Piece(PieceType::ROOK, Color::WHITE));
        board.setPiece(board.square(6, 7), Piece(PieceType::BISHOP, Color::BLACK)); // Attacks castling square
        board.setCastlingRights(true, false, false, false);
        board.setCurrentPlayer(Color::WHITE);
        
        MoveGenerator mg(board);
        auto moves = mg.generateCastlingMoves();
        
        // Should not be able to castle into check
        for (const auto& move : moves) {
            if (move.isCastling) {
                // Try to make the move and see if it results in check
                Board tempBoard = board;
                tempBoard.makeMove(move);
                assert(!tempBoard.isCheck(Color::WHITE)); // Should not be in check after castling
            }
        }
    });

    suite.test("En Passant Captures En Passant Square", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 4), Piece(PieceType::PAWN, Color::WHITE));
        board.setPiece(board.square(5, 4), Piece(PieceType::PAWN, Color::BLACK));
        board.setEnPassantSquare(board.square(5, 5));
        board.setCurrentPlayer(Color::WHITE);
        
        MoveGenerator mg(board);
        auto moves = mg.generateEnPassantMoves();
        
        bool found = false;
        for (const auto& move : moves) {
            if (move.isEnPassant) {
                found = true;
                board.makeMove(move);
                // The en passant square should no longer be set
                assert(board.getEnPassantSquare() == Board::NO_SQUARE);
                break;
            }
        }
        assert(found);
    });

    suite.test("Illegal Castling Through Pieces", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(7, 0), Piece(PieceType::ROOK, Color::WHITE));
        board.setPiece(board.square(6, 0), Piece(PieceType::KNIGHT, Color::WHITE)); // Blocking piece
        board.setCastlingRights(true, false, false, false);
        board.setCurrentPlayer(Color::WHITE);
        
        MoveGenerator mg(board);
        auto moves = mg.generateCastlingMoves();
        
        // Should not generate castling move due to blocker
        for (const auto& move : moves) {
            if (move.isCastling) {
                assert(false); // Should not be generated
            }
        }
    });
}

int main() {
    std::cout << "👑 SPECIAL MOVES COMPREHENSIVE TEST SUITE 👑" << std::endl;
    std::cout << std::string(60, '=') << std::endl;
    
    SpecialMoveTestSuite suite;
    
    std::cout << "\n🏰 CASTLING TESTS" << std::endl;
    std::cout << std::string(30, '-') << std::endl;
    testCastlingScenarios(suite);
    
    std::cout << "\n🎯 EN PASSANT TESTS" << std::endl;
    std::cout << std::string(30, '-') << std::endl;
    testEnPassantScenarios(suite);
    
    std::cout << "\n⭐ PAWN PROMOTION TESTS" << std::endl;
    std::cout << std::string(30, '-') << std::endl;
    testPromotionScenarios(suite);
    
    std::cout << "\n⚠️ EDGE CASE TESTS" << std::endl;
    std::cout << std::string(30, '-') << std::endl;
    testEdgeCases(suite);
    
    suite.printResults();
    
    return suite.total == suite.passed ? 0 : 1;
}