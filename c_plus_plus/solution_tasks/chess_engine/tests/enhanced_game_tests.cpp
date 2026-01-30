#include "../include/board.hpp"
#include "../include/move_generator.hpp"
#include "../include/game_rules.hpp"
#include "../include/check_detection.hpp"
#include <iostream>
#include <cassert>
#include <vector>
#include <chrono>

class TestSuite {
private:
    int passed_tests = 0;
    int total_tests = 0;
    std::vector<std::string> failed_tests;

public:
    void runTest(const std::string& name, std::function<void()> test_func) {
        total_tests++;
        std::cout << "Running: " << name << " ... ";
        
        try {
            auto start = std::chrono::high_resolution_clock::now();
            test_func();
            auto end = std::chrono::high_resolution_clock::now();
            
            auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
            std::cout << "✓ PASSED (" << duration.count() << " μs)" << std::endl;
            passed_tests++;
        } catch (const std::exception& e) {
            std::cout << "✗ FAILED: " << e.what() << std::endl;
            failed_tests.push_back(name + ": " + e.what());
        } catch (...) {
            std::cout << "✗ FAILED: Unknown exception" << std::endl;
            failed_tests.push_back(name + ": Unknown exception");
        }
    }

    void printSummary() {
        std::cout << "\n" << std::string(50, '=') << std::endl;
        std::cout << "TEST SUITE SUMMARY" << std::endl;
        std::cout << std::string(50, '=') << std::endl;
        std::cout << "Passed: " << passed_tests << "/" << total_tests << std::endl;
        std::cout << "Success rate: " << (total_tests > 0 ? (passed_tests * 100.0 / total_tests) : 0) << "%" << std::endl;
        
        if (!failed_tests.empty()) {
            std::cout << "\nFailed tests:" << std::endl;
            for (const auto& test : failed_tests) {
                std::cout << "  - " << test << std::endl;
            }
        }
        
        std::cout << std::string(50, '=') << std::endl;
    }
};

void testBasicCheckDetection(TestSuite& suite) {
    suite.runTest("Basic Queen Check", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(4, 7), Piece(PieceType::QUEEN, Color::BLACK));
        board.setCurrentPlayer(Color::WHITE);
        
        assert(board.isCheck(Color::WHITE));
        assert(!board.isCheck(Color::BLACK));
    });
    
    suite.runTest("Knight Check Pattern", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 4), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(5, 6), Piece(PieceType::KNIGHT, Color::BLACK));
        
        assert(board.isCheck(Color::WHITE));
    });
    
    suite.runTest("Rook Check Pattern", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(4, 5), Piece(PieceType::ROOK, Color::BLACK));
        
        assert(board.isCheck(Color::WHITE));
    });
    
    suite.runTest("Bishop Check Pattern", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 4), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(7, 7), Piece(PieceType::BISHOP, Color::BLACK));
        
        assert(board.isCheck(Color::WHITE));
    });
    
    suite.runTest("Pawn Check Pattern", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 4), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(5, 5), Piece(PieceType::PAWN, Color::BLACK));
        
        assert(board.isCheck(Color::WHITE));
    });
    
    suite.runTest("No Check Scenario", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(4, 4), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(0, 0), Piece(PieceType::ROOK, Color::BLACK));
        
        assert(!board.isCheck(Color::WHITE));
    });
}

void testAdvancedCheckmateScenarios(TestSuite& suite) {
    suite.runTest("Back Rank Mate", []() {
        Board board;
        board.initializeEmptyBoard();
        // White king trapped on back rank
        board.setPiece(board.square(0, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(1, 0), Piece(PieceType::ROOK, Color::BLACK));
        board.setPiece(board.square(0, 1), Piece(PieceType::ROOK, Color::BLACK));
        board.setCurrentPlayer(Color::WHITE);
        
        assert(board.isCheck(Color::WHITE));
        assert(board.isCheckmate(Color::WHITE));
    });
    
    suite.run("Anastasia's Mate", []() {
        Board board;
        board.initializeEmptyBoard();
        // Classic Anastasia's mate pattern
        board.setPiece(board.square(7, 1), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(5, 0), Piece(PieceType::KNIGHT, Color::BLACK));
        board.setPiece(board.square(7, 0), Piece(PieceType::ROOK, Color::BLACK));
        board.setPiece(board.square(6, 2), Piece(PieceType::PAWN, Color::WHITE));
        board.setCurrentPlayer(Color::WHITE);
        
        assert(board.isCheck(Color::WHITE));
        assert(board.isCheckmate(Color::WHITE));
    });
    
    suite.runTest("Smothered Mate", []() {
        Board board;
        board.initializeEmptyBoard();
        // Smothered mate with knight
        board.setPiece(board.square(7, 7), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(6, 5), Piece(PieceType::KNIGHT, Color::BLACK));
        board.setPiece(board.square(6, 7), Piece(PieceType::PAWN, Color::WHITE));
        board.setPiece(board.square(7, 6), Piece(PieceType::PAWN, Color::WHITE));
        board.setCurrentPlayer(Color::WHITE);
        
        assert(board.isCheck(Color::WHITE));
        assert(board.isCheckmate(Color::WHITE));
    });
    
    suite.runTest("Double Check Mate", []() {
        Board board;
        board.initializeEmptyBoard();
        // Double check leading to mate
        board.setPiece(board.square(4, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(3, 2), Piece(PieceType::KNIGHT, Color::BLACK));
        board.setPiece(board.square(5, 2), Piece(PieceType::BISHOP, Color::BLACK));
        board.setPiece(board.square(4, 1), Piece(PieceType::PAWN, Color::WHITE)); // Blocking escape
        board.setCurrentPlayer(Color::WHITE);
        
        assert(board.isCheck(Color::WHITE));
        assert(board.isCheckmate(Color::WHITE));
    });
}

void testStalemateScenarios(TestSuite& suite) {
    suite.runTest("Classic King vs King+Queen Stalemate", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(7, 7), Piece(PieceType::KING, Color::BLACK));
        board.setPiece(board.square(5, 6), Piece(PieceType::QUEEN, Color::WHITE));
        board.setPiece(board.square(5, 5), Piece(PieceType::KING, Color::WHITE));
        board.setCurrentPlayer(Color::BLACK);
        
        assert(!board.isCheck(Color::BLACK));
        assert(board.isStalemate(Color::BLACK));
    });
    
    suite.runTest("Pawn Blocking Stalemate", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(0, 7), Piece(PieceType::KING, Color::BLACK));
        board.setPiece(board.square(1, 5), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(0, 6), Piece(PieceType::PAWN, Color::WHITE));
        board.setCurrentPlayer(Color::BLACK);
        
        assert(!board.isCheck(Color::BLACK));
        assert(board.isStalemate(Color::BLACK));
    });
    
    suite.runTest("Not Stalemate - Has Legal Moves", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(7, 7), Piece(PieceType::KING, Color::BLACK));
        board.setPiece(board.square(4, 4), Piece(PieceType::QUEEN, Color::WHITE));
        board.setPiece(board.square(0, 0), Piece(PieceType::KING, Color::WHITE));
        board.setCurrentPlayer(Color::BLACK);
        
        assert(!board.isStalemate(Color::BLACK));
    });
}

void testDrawConditions(TestSuite& suite) {
    suite.runTest("Threefold Repetition", []() {
        Board board;
        board.setupStartPosition();
        
        // Execute knight dance pattern 3 times
        for (int cycle = 0; cycle < 3; cycle++) {
            Move moves[] = {
                {{6, 0}, {5, 2}, false, false, PieceType::EMPTY},
                {{6, 7}, {5, 5}, false, false, PieceType::EMPTY},
                {{5, 2}, {6, 0}, false, false, PieceType::EMPTY},
                {{5, 5}, {6, 7}, false, false, PieceType::EMPTY}
            };
            
            for (const auto& move : moves) {
                board.makeMove(move);
            }
        }
        
        assert(board.isRepetition());
    });
    
    suite.runTest("50-Move Rule", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(0, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(7, 7), Piece(PieceType::KING, Color::BLACK));
        board.setCurrentPlayer(Color::WHITE);
        board.setHalfMoveClock(100);
        
        assert(board.isFiftyMoveDraw());
    });
    
    suite.runTest("Insufficient Material - King vs King", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(0, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(7, 7), Piece(PieceType::KING, Color::BLACK));
        board.setCurrentPlayer(Color::WHITE);
        
        assert(board.isInsufficientMaterial());
    });
    
    suite.runTest("Insufficient Material - King+Bishop vs King", []() {
        Board board;
        board.initializeEmptyBoard();
        board.setPiece(board.square(0, 0), Piece(PieceType::KING, Color::WHITE));
        board.setPiece(board.square(7, 7), Piece(PieceType::KING, Color::BLACK));
        board.setPiece(board.square(1, 1), Piece(PieceType::BISHOP, Color::WHITE));
        board.setCurrentPlayer(Color::WHITE);
        
        assert(board.isInsufficientMaterial());
    });
}

void testPerformance(TestSuite& suite) {
    suite.runTest("Move Generation Performance", []() {
        Board board;
        board.setupStartPosition();
        
        const int iterations = 1000;
        auto start = std::chrono::high_resolution_clock::now();
        
        for (int i = 0; i < iterations; i++) {
            MoveGenerator gen(board);
            auto moves = gen.generateLegalMoves();
            // Reset board to avoid game end
            if (i < iterations - 1) {
                board.setupStartPosition();
            }
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        
        double avg_ms = static_cast<double>(duration.count()) / iterations;
        std::cout << "Average move generation time: " << avg_ms << " ms per position" << std::endl;
        
        // Performance threshold: should be under 10ms average
        assert(avg_ms < 10.0);
    });
}

int main() {
    std::cout << "♔ ♕ ♖ ♗ ♘ ♙ ENHANCED GAME STATE TEST SUITE ♟ ♞ ♝ ♜ ♛ ♚" << std::endl;
    std::cout << std::string(60, '=') << std::endl;
    
    TestSuite suite;
    
    // Run all test categories
    testBasicCheckDetection(suite);
    testAdvancedCheckmateScenarios(suite);
    testStalemateScenarios(suite);
    testDrawConditions(suite);
    testPerformance(suite);
    
    suite.printSummary();
    
    return suite.total_tests == suite.passed_tests ? 0 : 1;
}