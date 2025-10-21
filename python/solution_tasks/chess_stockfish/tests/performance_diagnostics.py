#!/usr/bin/env python3
"""
Performance diagnostics for chess_stockfish game.
"""

import sys
import os
import time
import psutil
import pygame

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from engine.stockfish_wrapper import StockfishWrapper

def test_cpu_performance():
    """Test CPU performance."""
    print("Testing CPU performance...")
    start_time = time.time()
    
    # CPU intensive test
    result = sum(i * i for i in range(1000000))
    
    cpu_time = time.time() - start_time
    print(f"  CPU computation time: {cpu_time:.4f} seconds")
    print(f"  Result: {result}")
    
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"  Current CPU usage: {cpu_percent}%")
    
    return cpu_time

def test_memory_usage():
    """Test memory usage."""
    print("\nTesting memory usage...")
    
    # Initial memory
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    print(f"  Initial memory usage: {initial_memory:.2f} MB")
    
    # Create game instance
    start_time = time.time()
    game = ChessGame()
    game_creation_time = time.time() - start_time
    
    game_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = game_memory - initial_memory
    
    print(f"  Game creation time: {game_creation_time:.4f} seconds")
    print(f"  Memory after game creation: {game_memory:.2f} MB")
    print(f"  Memory increase: {memory_increase:.2f} MB")
    
    return game_memory, memory_increase

def test_rendering_performance():
    """Test rendering performance."""
    print("\nTesting rendering performance...")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((512, 612))
    
    # Create game instance
    game = ChessGame()
    
    # Test board state retrieval
    start_time = time.time()
    board_state = game.get_board_state()
    board_state_time = time.time() - start_time
    print(f"  Board state retrieval: {board_state_time:.6f} seconds")
    
    # Test rendering
    start_time = time.time()
    evaluation = game.engine.get_evaluation()
    rendering_time = time.time() - start_time
    print(f"  Rendering preparation: {rendering_time:.6f} seconds")
    
    # Test valid moves calculation
    start_time = time.time()
    valid_moves = game._get_valid_moves(6, 4)  # e2 pawn
    valid_moves_time = time.time() - start_time
    print(f"  Valid moves calculation: {valid_moves_time:.6f} seconds")
    print(f"  Number of valid moves: {len(valid_moves)}")
    
    pygame.quit()
    return board_state_time, rendering_time, valid_moves_time

def test_ai_performance():
    """Test AI performance."""
    print("\nTesting AI performance...")
    
    # Create engine instance
    start_time = time.time()
    engine = StockfishWrapper(skill_level=5)
    engine_creation_time = time.time() - start_time
    print(f"  Engine creation time: {engine_creation_time:.4f} seconds")
    
    # Test best move calculation
    start_time = time.time()
    best_move = engine.get_best_move(depth=1)
    best_move_time = time.time() - start_time
    print(f"  Best move calculation (depth 1): {best_move_time:.4f} seconds")
    print(f"  Best move: {best_move}")
    
    # Test board state retrieval
    start_time = time.time()
    board_state = engine.get_board_state()
    board_state_time = time.time() - start_time
    print(f"  Board state retrieval: {board_state_time:.6f} seconds")
    
    return engine_creation_time, best_move_time, board_state_time

def test_caching_efficiency():
    """Test caching efficiency."""
    print("\nTesting caching efficiency...")
    
    game = ChessGame()
    
    # Test valid moves caching
    start_time = time.time()
    moves1 = game._get_valid_moves(6, 4)
    first_call_time = time.time() - start_time
    
    start_time = time.time()
    moves2 = game._get_valid_moves(6, 4)
    second_call_time = time.time() - start_time
    
    print(f"  Valid moves first call: {first_call_time:.6f} seconds")
    print(f"  Valid moves second call: {second_call_time:.6f} seconds")
    print(f"  Speedup: {first_call_time/second_call_time:.2f}x" if second_call_time > 0 else "  Cached result")
    
    # Test board state caching
    start_time = time.time()
    board1 = game.get_board_state()
    first_call_time = time.time() - start_time
    
    start_time = time.time()
    board2 = game.get_board_state()
    second_call_time = time.time() - start_time
    
    print(f"  Board state first call: {first_call_time:.6f} seconds")
    print(f"  Board state second call: {second_call_time:.6f} seconds")
    print(f"  Speedup: {first_call_time/second_call_time:.2f}x" if second_call_time > 0 else "  Cached result")
    
    return first_call_time, second_call_time

def main():
    """Run all performance diagnostics."""
    print("Chess Stockfish Performance Diagnostics")
    print("=" * 50)
    
    try:
        # System information
        print(f"System: {psutil.cpu_count()} CPU cores")
        print(f"Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB RAM")
        print(f"Python version: {sys.version}")
        
        # Run tests
        cpu_time = test_cpu_performance()
        game_memory, memory_increase = test_memory_usage()
        board_time, render_time, moves_time = test_rendering_performance()
        engine_time, move_time, engine_board_time = test_ai_performance()
        cache_first, cache_second = test_caching_efficiency()
        
        # Summary
        print("\n" + "=" * 50)
        print("PERFORMANCE SUMMARY")
        print("=" * 50)
        print(f"CPU performance: {cpu_time:.4f} seconds")
        print(f"Memory usage: {game_memory:.2f} MB (+{memory_increase:.2f} MB)")
        print(f"Board state retrieval: {board_time:.6f} seconds")
        print(f"Rendering preparation: {render_time:.6f} seconds")
        print(f"Valid moves calculation: {moves_time:.6f} seconds")
        print(f"AI move calculation: {move_time:.4f} seconds")
        print(f"Caching speedup: {cache_first/cache_second:.2f}x" if cache_second > 0 else "Caching effective")
        
        # Performance recommendations
        print("\nRECOMMENDATIONS:")
        if cpu_time > 0.2:
            print("  ⚠️  High CPU usage detected - consider CPU upgrade")
        if memory_increase > 100:
            print("  ⚠️  High memory usage - optimize memory management")
        if moves_time > 0.01:
            print("  ⚠️  Slow move calculation - optimize algorithms")
        if move_time > 1.0:
            print("  ⚠️  Slow AI response - reduce AI depth or optimize engine")
        if cache_second > 0.001:
            print("  ⚠️  Caching not optimal - increase cache duration")
            
        print("\n🎉 Diagnostics completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during diagnostics: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)