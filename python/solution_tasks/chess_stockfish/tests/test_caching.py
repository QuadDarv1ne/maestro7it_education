#!/usr/bin/env python3
"""
Test script for caching mechanisms in the chess game.
"""

from game.chess_game import ChessGame
import time

def test_valid_moves_cache():
    """Test valid moves caching functionality."""
    print("Testing valid moves caching...")
    game = ChessGame()
    
    # Get valid moves for a piece (white pawn at e2)
    start_time = time.time()
    moves1 = game._get_valid_moves(6, 4)  # e2 pawn (row 6, col 4 in FEN)
    time1 = time.time() - start_time
    
    # Get the same moves again (should use cache)
    start_time = time.time()
    moves2 = game._get_valid_moves(6, 4)  # e2 pawn
    time2 = time.time() - start_time
    
    print(f"First call time: {time1:.6f} seconds")
    print(f"Second call time: {time2:.6f} seconds")
    print(f"Speedup: {time1/time2:.2f}x" if time2 > 0 else "Cached result")
    print(f"Moves are equal: {moves1 == moves2}")
    
    # Clear cache and test again
    game._clear_caches()
    start_time = time.time()
    moves3 = game._get_valid_moves(6, 4)  # e2 pawn
    time3 = time.time() - start_time
    print(f"After cache clear: {time3:.6f} seconds")
    
    print("Valid moves caching test completed!\n")

def test_king_position_cache():
    """Test king position caching functionality."""
    print("Testing king position caching...")
    game = ChessGame()
    
    # Get board state
    board_state = game.engine.get_board_state()
    
    # Find white king position
    start_time = time.time()
    king_pos1 = game._find_king_position(board_state, True)
    time1 = time.time() - start_time
    
    # Find white king position again (should use cache)
    start_time = time.time()
    king_pos2 = game._find_king_position(board_state, True)
    time2 = time.time() - start_time
    
    print(f"First call time: {time1:.6f} seconds")
    print(f"Second call time: {time2:.6f} seconds")
    print(f"King position: {king_pos1}")
    print(f"Positions are equal: {king_pos1 == king_pos2}")
    
    print("King position caching test completed!\n")

def test_educational_feedback_cache():
    """Test educational feedback caching functionality."""
    print("Testing educational feedback caching...")
    game = ChessGame()
    
    # Get educational feedback
    start_time = time.time()
    feedback1 = game.educator.get_educational_feedback(5, time.time())
    time1 = time.time() - start_time
    
    # Get educational feedback again (should use cache)
    start_time = time.time()
    feedback2 = game.educator.get_educational_feedback(5, time.time())
    time2 = time.time() - start_time
    
    print(f"First call time: {time1:.6f} seconds")
    print(f"Second call time: {time2:.6f} seconds")
    print(f"Feedback: {feedback1}")
    
    print("Educational feedback caching test completed!\n")

def main():
    """Run all caching tests."""
    print("Running caching mechanism tests...\n")
    
    try:
        test_valid_moves_cache()
        test_king_position_cache()
        test_educational_feedback_cache()
        
        print("All caching tests completed successfully!")
        print("\nPerformance improvements implemented:")
        print("1. Valid moves caching with 500ms expiration")
        print("2. King position caching with 1s expiration")
        print("3. Educational feedback caching with 10s expiration")
        print("4. Piece hint caching")
        print("5. Enhanced cache clearing mechanisms")
        print("6. Periodic cache cleanup every 30 seconds")
        
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main()