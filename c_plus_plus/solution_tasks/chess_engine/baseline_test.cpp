#include "include/board.hpp"
#include "include/piece.hpp"
#include <iostream>
#include <chrono>

int main() {
    std::cout << "=== BASELINE PERFORMANCE TEST ===" << std::endl;
    
    // Test 1: Board initialization performance
    auto start = std::chrono::high_resolution_clock::now();
    
    const int iterations = 10000;
    for (int i = 0; i < iterations; i++) {
        Board board;
        board.setupStartPosition();
        volatile int dummy = board.getMoveCount(); // Prevent optimization
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Board initialization test (" << iterations << " iterations): " 
              << duration.count() << " ms" << std::endl;
    std::cout << "Average time per initialization: " 
              << (double)duration.count() / iterations * 1000 << " μs" << std::endl;
    
    // Test 2: Basic piece operations
    Board board;
    board.setupStartPosition();
    
    start = std::chrono::high_resolution_clock::now();
    
    for (int i = 0; i < iterations * 10; i++) {
        Piece piece = board.getPiece(0);
        volatile PieceType type = piece.getType(); // Prevent optimization
        volatile Color color = piece.getColor();
    }
    
    end = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Piece access test (" << iterations * 10 << " iterations): " 
              << duration.count() << " ms" << std::endl;
    std::cout << "Average time per access: " 
              << (double)duration.count() / (iterations * 10) * 1000 << " μs" << std::endl;
    
    // Test 3: Simple evaluation
    start = std::chrono::high_resolution_clock::now();
    
    int totalScore = 0;
    for (int i = 0; i < iterations / 10; i++) {
        // Simple material counting
        int whiteMaterial = 0, blackMaterial = 0;
        for (int square = 0; square < 64; square++) {
            Piece piece = board.getPiece(square);
            if (!piece.isEmpty()) {
                int value = piece.getValue();
                if (piece.getColor() == Color::WHITE) {
                    whiteMaterial += value;
                } else {
                    blackMaterial += value;
                }
            }
        }
        totalScore += (whiteMaterial - blackMaterial);
    }
    
    end = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
    
    std::cout << "Simple evaluation test (" << iterations / 10 << " iterations): " 
              << duration.count() << " ms" << std::endl;
    std::cout << "Average time per evaluation: " 
              << (double)duration.count() / (iterations / 10) * 1000 << " μs" << std::endl;
    std::cout << "Total score accumulated: " << totalScore << std::endl;
    
    std::cout << "\n=== BASELINE ESTABLISHED ===" << std::endl;
    std::cout << "These measurements will serve as reference points for future optimizations." << std::endl;
    
    return 0;
}