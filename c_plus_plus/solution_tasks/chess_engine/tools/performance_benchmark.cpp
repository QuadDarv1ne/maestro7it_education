#include <chrono>
#include <iostream>
#include <vector>
#include <iomanip>
#include <string>
#include <algorithm>
#include <random>
#include <numeric>
#include <exception>

#include "../include/board.hpp"
#include "../include/move_generator.hpp"
#include "../include/game_rules.hpp"

using namespace std;
using namespace std::chrono;

class PerformanceBenchmark {
private:
    vector<string> test_positions_;
    
public:
    PerformanceBenchmark() {
        // Standard test positions
        test_positions_ = {
            // Starting position
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            
            // Mid-game position
            "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1",
            
            // Complex tactical position
            "r1bq1rk1/pp2ppbp/2np1np1/8/2PNP3/2N1BP2/PP2B1PP/R2QK2R w KQ - 0 1",
            
            // Endgame position
            "8/2k5/8/8/8/5K2/8/8 w - - 0 1",
            
            // Queen + King vs King endgame
            "8/8/8/4k3/8/8/2K5/3Q4 w - - 0 1"
        };
    }
    
    void runAllBenchmarks() {
        cout << "♔ ♕ ♖ ♗ ♘ ♙ CHESS ENGINE PERFORMANCE BENCHMARK ♟ ♞ ♝ ♜ ♛ ♚\n";
        cout << string(60, '=') << "\n\n";
        
        benchmarkMoveGeneration();
        benchmarkPositionEvaluation();
        benchmarkSearchPerformance();
        benchmarkMemoryUsage();
        
        cout << "\n" << string(60, '=') << "\n";
        cout << "✅ All benchmarks completed!\n";
    }
    
private:
    void benchmarkMoveGeneration() {
        cout << "🏃 MOVE GENERATION BENCHMARK\n";
        cout << string(40, '-') << "\n";
        
        vector<double> times;
        vector<size_t> move_counts;
        
        for (const auto& fen : test_positions_) {
            Board board;
            board.setupFromFEN(fen);
            MoveGenerator moveGen(board);
            
            // Warm up
            for (int i = 0; i < 100; ++i) {
                auto moves = moveGen.generateLegalMoves();
            }
            
            // Benchmark
            auto start = high_resolution_clock::now();
            const int iterations = 10000;
            
            size_t total_moves = 0;
            for (int i = 0; i < iterations; ++i) {
                auto moves = moveGen.generateLegalMoves();
                total_moves += moves.size();
            }
            
            auto end = high_resolution_clock::now();
            auto duration = duration_cast<nanoseconds>(end - start);
            
            double avg_time = static_cast<double>(duration.count()) / iterations;
            double moves_per_second = 1e9 / avg_time;
            
            times.push_back(avg_time);
            move_counts.push_back(total_moves / iterations);
            
            cout << "FEN: " << fen.substr(0, min(static_cast<size_t>(30), fen.length())) << "...\n";
            cout << "  Avg time: " << fixed << setprecision(2) << avg_time << " ns\n";
            cout << "  Moves/sec: " << fixed << setprecision(0) << moves_per_second << "\n";
            cout << "  Avg moves: " << move_counts.back() << "\n\n";
        }
        
        // Summary
        double avg_time = accumulate(times.begin(), times.end(), 0.0) / times.size();
        double avg_moves = accumulate(move_counts.begin(), move_counts.end(), 0.0) / move_counts.size();
        double moves_per_second = 1e9 / avg_time;
        
        cout << "📊 MOVE GENERATION SUMMARY:\n";
        cout << "  Average time per position: " << fixed << setprecision(2) << avg_time << " ns\n";
        cout << "  Overall moves/sec: " << fixed << setprecision(0) << moves_per_second << "\n";
        cout << "  Average legal moves: " << fixed << setprecision(1) << avg_moves << "\n\n";
    }
    
    void benchmarkPositionEvaluation() {
        cout << "🎯 POSITION EVALUATION BENCHMARK\n";
        cout << string(40, '-') << "\n";
        
        vector<double> times;
        
        for (const auto& fen : test_positions_) {
            Board board;
            board.setupFromFEN(fen);
            
            // Warm up
            for (int i = 0; i < 1000; ++i) {
                auto hash = board.getZobristHash();
            }
            
            // Benchmark
            auto start = high_resolution_clock::now();
            const int iterations = 100000;
            
            for (int i = 0; i < iterations; ++i) {
                auto hash = board.getZobristHash();
            }
            
            auto end = high_resolution_clock::now();
            auto duration = duration_cast<nanoseconds>(end - start);
            
            double avg_time = static_cast<double>(duration.count()) / iterations;
            double hashes_per_second = 1e9 / avg_time;
            
            times.push_back(avg_time);
            
            cout << "FEN: " << fen.substr(0, min(static_cast<size_t>(30), fen.length())) << "...\n";
            cout << "  Avg hash time: " << fixed << setprecision(2) << avg_time << " ns\n";
            cout << "  Hashes/sec: " << fixed << setprecision(0) << hashes_per_second << "\n\n";
        }
        
        // Summary
        double avg_time = accumulate(times.begin(), times.end(), 0.0) / times.size();
        double hashes_per_second = 1e9 / avg_time;
        
        cout << "📊 EVALUATION SUMMARY:\n";
        cout << "  Average hash time: " << fixed << setprecision(2) << avg_time << " ns\n";
        cout << "  Overall hashes/sec: " << fixed << setprecision(0) << hashes_per_second << "\n\n";
    }
    
    void benchmarkSearchPerformance() {
        cout << "🔍 SEARCH PERFORMANCE BENCHMARK\n";
        cout << string(40, '-') << "\n";
        
        // Test position with moderate complexity
        string test_fen = "r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1";
        
        Board board;
        board.setupFromFEN(test_fen);
        
        cout << "Testing position: " << test_fen.substr(0, 30) << "...\n\n";
        
        // Depth 1-4 search benchmark
        for (int depth = 1; depth <= 4; ++depth) {
            auto start = high_resolution_clock::now();
            
            // Simple perft-like calculation
            size_t nodes = perft(board, depth);
            
            auto end = high_resolution_clock::now();
            auto duration = duration_cast<milliseconds>(end - start);
            
            double seconds = duration.count() / 1000.0;
            double nps = nodes / seconds;
            
            cout << "Depth " << depth << ":\n";
            cout << "  Nodes: " << nodes << "\n";
            cout << "  Time: " << fixed << setprecision(3) << seconds << " s\n";
            cout << "  NPS: " << fixed << setprecision(0) << nps << "\n\n";
        }
    }
    
    void benchmarkMemoryUsage() {
        cout << "💾 MEMORY USAGE BENCHMARK\n";
        cout << string(40, '-') << "\n";
        
        // Measure size of key classes
        cout << "Object sizes:\n";
        cout << "  Board: " << sizeof(Board) << " bytes\n";
        cout << "  Move: " << sizeof(Move) << " bytes\n";
        cout << "  Piece: " << sizeof(Piece) << " bytes\n";
        cout << "  Square: " << sizeof(Square) << " bytes\n\n";
        
        // Memory allocation test
        const size_t num_boards = 10000;
        vector<Board> boards;
        
        auto start = high_resolution_clock::now();
        boards.reserve(num_boards);
        
        for (size_t i = 0; i < num_boards; ++i) {
            boards.emplace_back();
            boards.back().setupStartPosition();
        }
        
        auto end = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(end - start);
        
        size_t total_size = num_boards * sizeof(Board);
        double mb_used = static_cast<double>(total_size) / (1024 * 1024);
        
        cout << "Allocated " << num_boards << " Board objects:\n";
        cout << "  Total size: " << fixed << setprecision(2) << mb_used << " MB\n";
        cout << "  Time taken: " << duration.count() << " ms\n";
        cout << "  Avg time per board: " << fixed << setprecision(3) << 
                static_cast<double>(duration.count()) / num_boards << " ms\n\n";
    }
    
    // Simple perft implementation for benchmarking
    size_t perft(Board& board, int depth) {
        if (depth == 0) return 1;
        
        MoveGenerator moveGen(board);
        auto moves = moveGen.generateLegalMoves();
        
        if (depth == 1) return moves.size();
        
        size_t nodes = 0;
        GameRules rules(board);
        
        for (const auto& move : moves) {
            board.makeMove(move);
            nodes += perft(board, depth - 1);
            board.undoMove();
        }
        
        return nodes;
    }
};

int main() {
    try {
        PerformanceBenchmark benchmark;
        benchmark.runAllBenchmarks();
        return 0;
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }
}