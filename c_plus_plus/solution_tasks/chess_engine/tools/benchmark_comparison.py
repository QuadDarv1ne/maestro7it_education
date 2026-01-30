#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Performance Benchmark: Original vs Optimized Move Generation
"""

import time
from typing import List, Tuple
import matplotlib.pyplot as plt
import numpy as np

def original_move_generation(board: List[List[str]], color: bool) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Оригинальная генерация ходов (используемая в текущей реализации)"""
    moves = []
    
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != '.':
                is_white = piece.isupper()
                if (color and is_white) or (not color and not is_white):
                    # Generate moves for this piece
                    for to_row in range(8):
                        for to_col in range(8):
                            if is_valid_move_original(board, (row, col), (to_row, to_col), color):
                                moves.append(((row, col), (to_row, to_col)))
    return moves

def is_valid_move_original(board: List[List[str]], from_pos: Tuple[int, int], to_pos: Tuple[int, int], is_white_turn: bool) -> bool:
    """Оригинальная логика валидации ходов"""
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    
    piece = board[from_row][from_col]
    target = board[to_row][to_col]
    
    # Basic validation
    if not (0 <= to_row < 8 and 0 <= to_col < 8):
        return False
    
    if from_pos == to_pos:
        return False
    
    # Color validation
    is_white_piece = piece.isupper()
    if (is_white_piece and not is_white_turn) or (not is_white_piece and is_white_turn):
        return False
    
    # Cannot capture own pieces or king
    if target != '.':
        if (target.isupper() and is_white_piece) or (target.islower() and not is_white_piece):
            return False
        if target.lower() == 'k':
            return False
    
    # Piece-specific movement rules (simplified)
    piece_type = piece.lower()
    
    if piece_type == 'p':  # Pawn
        direction = -1 if is_white_piece else 1
        start_row = 6 if is_white_piece else 1
        
        # Forward move
        if from_col == to_col and to_row == from_row + direction and target == '.':
            return True
        # Double move from start
        if (from_row == start_row and from_col == to_col and 
            to_row == from_row + 2 * direction and 
            target == '.' and board[from_row + direction][from_col] == '.'):
            return True
        # Capture
        if (abs(from_col - to_col) == 1 and to_row == from_row + direction and 
            target != '.' and target.isupper() != is_white_piece):
            return True
            
    elif piece_type == 'r':  # Rook
        return is_straight_move(from_pos, to_pos, board)
    elif piece_type == 'b':  # Bishop
        return is_diagonal_move(from_pos, to_pos, board)
    elif piece_type == 'q':  # Queen
        return is_straight_move(from_pos, to_pos, board) or is_diagonal_move(from_pos, to_pos, board)
    elif piece_type == 'k':  # King
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        return row_diff <= 1 and col_diff <= 1
    elif piece_type == 'n':  # Knight
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    return False

def is_straight_move(from_pos: Tuple[int, int], to_pos: Tuple[int, int], board: List[List[str]]) -> bool:
    """Check if move is straight (horizontal/vertical)"""
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    
    if from_row != to_row and from_col != to_col:
        return False
    
    # Check path is clear
    if from_row == to_row:  # Horizontal
        step = 1 if from_col < to_col else -1
        for col in range(from_col + step, to_col, step):
            if board[from_row][col] != '.':
                return False
    else:  # Vertical
        step = 1 if from_row < to_row else -1
        for row in range(from_row + step, to_row, step):
            if board[row][from_col] != '.':
                return False
    
    return True

def is_diagonal_move(from_pos: Tuple[int, int], to_pos: Tuple[int, int], board: List[List[str]]) -> bool:
    """Check if move is diagonal"""
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    
    if abs(from_row - to_row) != abs(from_col - to_col):
        return False
    
    row_step = 1 if to_row > from_row else -1
    col_step = 1 if to_col > from_col else -1
    
    row, col = from_row + row_step, from_col + col_step
    while row != to_row and col != to_col:
        if board[row][col] != '.':
            return False
        row += row_step
        col += col_step
    
    return True

def benchmark_comparison():
    """Compare original vs optimized move generation performance"""
    
    # Test positions
    test_positions = [
        # Starting position
        ('Start Position', [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]),
        # Mid-game position
        ('Mid-game', [
            ['r', '.', 'b', 'q', 'k', '.', 'n', 'r'],
            ['p', 'p', 'p', '.', '.', 'p', 'p', 'p'],
            ['.', '.', 'n', '.', '.', '.', '.', '.'],
            ['.', '.', '.', 'p', 'p', '.', '.', '.'],
            ['.', '.', '.', 'P', 'P', '.', '.', '.'],
            ['.', '.', '.', '.', '.', 'N', '.', '.'],
            ['P', 'P', 'P', '.', '.', 'P', 'P', 'P'],
            ['R', '.', 'B', 'Q', 'K', 'B', '.', 'R']
        ]),
        # Endgame position
        ('Endgame', [
            ['.', '.', '.', '.', 'k', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', 'K', '.', '.', '.']
        ])
    ]
    
    # Import optimized generator
    from optimized_move_generator import BitboardMoveGenerator
    optimized_generator = BitboardMoveGenerator()
    
    results = {
        'positions': [],
        'original_times': [],
        'optimized_times': [],
        'speedup_ratios': [],
        'original_moves': [],
        'optimized_moves': []
    }
    
    print("♔ ♕ ♖ ♗ ♘ ♙ MOVE GENERATION BENCHMARK ♟ ♞ ♝ ♜ ♛ ♚")
    print("=" * 60)
    print(f"{'Position':<15} {'Original (ms)':<15} {'Optimized (ms)':<15} {'Speedup':<10} {'Moves'}")
    print("-" * 60)
    
    for pos_name, board in test_positions:
        # Warm up
        for _ in range(10):
            original_move_generation(board, True)
            optimized_generator.generate_legal_moves(board, True)
        
        # Benchmark original
        start_time = time.perf_counter()
        for _ in range(100):
            original_moves = original_move_generation(board, True)
        original_time = (time.perf_counter() - start_time) / 100
        
        # Benchmark optimized
        start_time = time.perf_counter()
        for _ in range(100):
            optimized_moves = optimized_generator.generate_legal_moves(board, True)
        optimized_time = (time.perf_counter() - start_time) / 100
        
        # Calculate speedup
        speedup = original_time / optimized_time if optimized_time > 0 else float('inf')
        
        # Store results
        results['positions'].append(pos_name)
        results['original_times'].append(original_time * 1000)
        results['optimized_times'].append(optimized_time * 1000)
        results['speedup_ratios'].append(speedup)
        results['original_moves'].append(len(original_moves))
        results['optimized_moves'].append(len(optimized_moves))
        
        print(f"{pos_name:<15} {original_time*1000:<15.4f} {optimized_time*1000:<15.4f} {speedup:<10.2f}x {len(original_moves)}")
    
    # Summary statistics
    avg_speedup = sum(results['speedup_ratios']) / len(results['speedup_ratios'])
    total_original_time = sum(results['original_times'])
    total_optimized_time = sum(results['optimized_times'])
    
    print("-" * 60)
    print(f"{'AVERAGE':<15} {total_original_time/len(test_positions):<15.4f} {total_optimized_time/len(test_positions):<15.4f} {avg_speedup:<10.2f}x")
    print("=" * 60)
    print(f"Overall performance improvement: {avg_speedup:.2f}x faster")
    
    # Create visualization
    create_performance_chart(results)
    
    return results

def create_performance_chart(results):
    """Create performance comparison chart"""
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        positions = results['positions']
        x_pos = range(len(positions))
        
        # Time comparison chart
        width = 0.35
        ax1.bar([x - width/2 for x in x_pos], results['original_times'], 
                width, label='Original', color='red', alpha=0.7)
        ax1.bar([x + width/2 for x in x_pos], results['optimized_times'], 
                width, label='Optimized', color='green', alpha=0.7)
        
        ax1.set_xlabel('Position Type')
        ax1.set_ylabel('Time (milliseconds)')
        ax1.set_title('Move Generation Time Comparison')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(positions)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Speedup chart
        bars = ax2.bar(positions, results['speedup_ratios'], 
                      color=['blue' if s < 10 else 'orange' for s in results['speedup_ratios']])
        ax2.set_xlabel('Position Type')
        ax2.set_ylabel('Speedup Ratio (times faster)')
        ax2.set_title('Performance Improvement')
        ax2.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, speedup in zip(bars, results['speedup_ratios']):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{speedup:.1f}x', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('move_generation_benchmark.png', dpi=300, bbox_inches='tight')
        print(f"\n📊 Chart saved as: move_generation_benchmark.png")
        
    except ImportError:
        print("\n⚠️  Matplotlib not available - skipping chart generation")
        print("Install with: pip install matplotlib")

def main():
    """Run the benchmark"""
    results = benchmark_comparison()
    
    # Save detailed results
    import json
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: benchmark_results.json")
    print("✅ Benchmark complete!")

if __name__ == "__main__":
    main()