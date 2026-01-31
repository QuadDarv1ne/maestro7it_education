#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Test script for chess engine optimizations"""

from core.enhanced_chess_ai import EnhancedChessAI
import time

def test_performance():
    print("♔ ♕ ♖ ♗ ♘ ♙ TESTING CHESS ENGINE OPTIMIZATIONS ♟ ♞ ♝ ♜ ♛ ♚")
    print("=" * 60)
    
    # Create AI instance
    ai = EnhancedChessAI(search_depth=4)
    
    # Test board (starting position)
    test_board = [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    ]
    
    print("Testing AI performance with optimizations...")
    print(f"Search depth: {ai.search_depth}")
    print("-" * 40)
    
    # Run test
    start_time = time.perf_counter()
    try:
        move = ai.get_best_move(test_board, True, time_limit=2.0)
        duration = time.perf_counter() - start_time
        
        print(f"✅ Test completed successfully!")
        print(f"⏱️  Time taken: {duration:.2f} seconds")
        print(f"🔢 Nodes searched: {ai.nodes_searched:,}")
        print(f"⚡ Nodes per second: {ai.nodes_searched/duration:,.0f}")
        print(f"🎯 Transposition table hits: {ai.tt_hits:,}")
        print(f"🧠 Best move found: {move}")
        
        # Performance metrics
        print("\n📈 PERFORMANCE METRICS:")
        print("-" * 25)
        if duration > 0:
            nps = ai.nodes_searched / duration
            hit_rate = (ai.tt_hits / ai.nodes_searched * 100) if ai.nodes_searched > 0 else 0
            
            print(f"Nodes/sec: {nps:,.0f}")
            print(f"TT Hit rate: {hit_rate:.1f}%")
            
            # Compare with baseline expectations
            if nps > 5000:
                print("🏆 Excellent performance!")
            elif nps > 2000:
                print("✅ Good performance")
            else:
                print("⚠️  Performance could be improved")
                
            if hit_rate > 20:
                print("🎯 High TT efficiency")
            elif hit_rate > 10:
                print("👍 Decent TT usage")
            else:
                print("🔧 Low TT utilization")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_performance()
    print("\n🎉 Optimization testing complete!")