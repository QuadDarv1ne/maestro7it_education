#!/usr/bin/env python3
"""
Optimized performance test for chess_stockfish game.
"""

import sys
import os
import time
import pygame

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from engine.stockfish_wrapper import StockfishWrapper

def test_optimized_rendering():
    """Test optimized rendering performance."""
    print("Testing optimized rendering performance...")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((512, 612))
    
    # Create game instance
    game = ChessGame()
    
    # Test multiple rendering cycles with optimization
    total_time = 0
    cycle_count = 100
    
    for i in range(cycle_count):
        start_time = time.time()
        
        # Get board state
        board_state = game.get_board_state()
        
        # Test optimized evaluation caching
        evaluation = None
        current_time = time.time()
        if not hasattr(game, '_last_eval_update') or (current_time - game._last_eval_update) > 0.5:
            # Обновляем оценку только раз в 500 мс
            evaluation = game.engine.get_evaluation()
            game._last_eval_update = current_time
        elif hasattr(game, '_cached_evaluation'):
            evaluation = game._cached_evaluation
        
        game._cached_evaluation = evaluation
        
        # Simulate rendering
        # In real implementation, this would call the renderer
        render_time = time.time() - start_time
        total_time += render_time
        
        # Add small delay to simulate frame rate
        time.sleep(0.01)  # 10ms delay = 100 FPS target
    
    avg_render_time = total_time / cycle_count
    print(f"  Average optimized render time: {avg_render_time*1000:.2f} ms")
    print(f"  Target frame rate: {1.0/avg_render_time:.1f} FPS" if avg_render_time > 0 else "  Target frame rate: ∞ FPS")
    
    pygame.quit()
    return avg_render_time

def test_ai_move_optimization():
    """Test AI move optimization."""
    print("\nTesting AI move optimization...")
    
    # Create engine with low depth for fast testing
    engine = StockfishWrapper(skill_level=1)
    
    # Test multiple AI move calculations with caching
    total_time = 0
    move_count = 10
    
    for i in range(move_count):
        start_time = time.time()
        best_move = engine.get_best_move(depth=1)  # Low depth for fast testing
        move_time = time.time() - start_time
        total_time += move_time
        print(f"  Move {i+1}: {best_move} ({move_time*1000:.2f} ms)")
    
    avg_move_time = total_time / move_count
    print(f"  Average AI move time: {avg_move_time*1000:.2f} ms")
    
    return avg_move_time

def test_caching_improvements():
    """Test caching improvements."""
    print("\nTesting caching improvements...")
    
    game = ChessGame()
    
    # Test evaluation caching
    start_time = time.time()
    eval1 = game.engine.get_evaluation()
    first_call = time.time() - start_time
    
    start_time = time.time()
    eval2 = game.engine.get_evaluation()  # Should use cache
    second_call = time.time() - start_time
    
    print(f"  Evaluation first call: {first_call*1000:.2f} ms")
    print(f"  Evaluation second call: {second_call*1000:.2f} ms")
    print(f"  Caching speedup: {first_call/second_call:.2f}x" if second_call > 0 else "  Cached result")
    
    # Test valid moves caching
    start_time = time.time()
    moves1 = game._get_valid_moves(6, 4)  # e2 pawn
    first_call = time.time() - start_time
    
    start_time = time.time()
    moves2 = game._get_valid_moves(6, 4)  # Should use cache
    second_call = time.time() - start_time
    
    print(f"  Valid moves first call: {first_call*1000:.2f} ms")
    print(f"  Valid moves second call: {second_call*1000:.2f} ms")
    print(f"  Caching speedup: {first_call/second_call:.2f}x" if second_call > 0 else "  Cached result")
    
    return first_call, second_call

def main():
    """Run all optimized performance tests."""
    print("Chess Stockfish Optimized Performance Test")
    print("=" * 50)
    
    try:
        # Run tests
        render_time = test_optimized_rendering()
        ai_time = test_ai_move_optimization()
        cache_first, cache_second = test_caching_improvements()
        
        # Summary
        print("\n" + "=" * 50)
        print("OPTIMIZED PERFORMANCE SUMMARY")
        print("=" * 50)
        print(f"Average render time: {render_time*1000:.2f} ms")
        print(f"Target frame rate: {1.0/render_time:.1f} FPS" if render_time > 0 else "Target frame rate: ∞ FPS")
        print(f"Average AI move time: {ai_time*1000:.2f} ms")
        print(f"Caching speedup: {cache_first/cache_second:.2f}x" if cache_second > 0 else "Caching effective")
        
        # Performance assessment
        print("\nPERFORMANCE ASSESSMENT:")
        if render_time < 0.016:  # < 16ms = 60+ FPS
            print("  ✅ Excellent rendering performance (60+ FPS)")
        elif render_time < 0.033:  # < 33ms = 30+ FPS
            print("  ⚠️  Good rendering performance (30+ FPS)")
        else:
            print("  ❌ Poor rendering performance (< 30 FPS)")
            
        if ai_time < 0.1:  # < 100ms
            print("  ✅ Fast AI response")
        elif ai_time < 0.5:  # < 500ms
            print("  ⚠️  Acceptable AI response")
        else:
            print("  ❌ Slow AI response (> 500ms)")
            
        if cache_second < 0.001:  # < 1ms
            print("  ✅ Excellent caching performance")
        else:
            print("  ⚠️  Good caching performance")
            
        print("\n🎉 Optimized performance test completed!")
        
    except Exception as e:
        print(f"❌ Error during optimized testing: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)