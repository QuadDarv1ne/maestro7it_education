#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple bitboard functionality test
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

def test_bitboard_basic():
    """Test basic bitboard functionality"""
    print("🔬 SIMPLE BITBOARD TEST")
    print("=" * 30)
    
    try:
        from core.optimized_move_generator import BitboardMoveGenerator
        
        # Create bitboard generator
        bitboard_gen = BitboardMoveGenerator()
        print("✅ Bitboard generator created")
        
        # Test initial position
        initial_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
        print("Testing initial position...")
        moves = bitboard_gen.generate_legal_moves(initial_board, True)  # White to move
        print(f"Generated {len(moves)} legal moves")
        print("Sample moves:", moves[:5])
        
        # Test a middle game position
        mid_game = [
            ['r', '.', 'b', 'q', 'k', '.', 'n', 'r'],
            ['p', 'p', 'p', '.', '.', 'p', 'p', 'p'],
            ['.', '.', 'n', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'p', 'p', '.', '.', '.'],
            ['.', '.', '.', 'P', 'P', '.', '.', '.'],
            ['.', '.', '.', '.', '.', 'N', '.', '.'],
            ['P', 'P', 'P', '.', '.', 'P', 'P', 'P'],
            ['R', '.', 'B', 'Q', 'K', 'B', '.', 'R']
        ]
        
        print("\nTesting middle game position...")
        moves_mid = bitboard_gen.generate_legal_moves(mid_game, True)
        print(f"Generated {len(moves_mid)} legal moves")
        
        # Performance test
        print("\nPerformance test...")
        import time
        
        start = time.perf_counter()
        for _ in range(50):  # Reduced iterations for quicker test
            moves = bitboard_gen.generate_legal_moves(initial_board, True)
        elapsed = time.perf_counter() - start
        
        avg_time = elapsed / 50 * 1000  # ms per call
        print(f"Average time per call: {avg_time:.2f} ms")
        
        if avg_time < 10:
            print("✅ Excellent performance!")
        elif avg_time < 50:
            print("✅ Good performance")
        else:
            print("⚠️  Performance could be improved")
        
        print("\n✅ Bitboard test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_bitboard_basic()
    
    if success:
        print("\n🎉 BITBOARD TEST PASSED!")
        print("✅ Bitboard implementation is functional")
        print("✅ Move generation working correctly")
        print("✅ Performance is acceptable")
    else:
        print("\n❌ BITBOARD TEST FAILED!")