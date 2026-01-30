#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Debug script for checkmate detection"""

import sys
sys.path.append('core')

from chess_engine_wrapper import ChessEngineWrapper

def print_board(board_state):
    """Print the board"""
    print("\n   a b c d e f g h")
    print("  +----------------+")
    for i, row in enumerate(board_state):
        print(f"{8-i} |", end="")
        for piece in row:
            print(f"{piece} ", end="")
        print(f"| {8-i}")
    print("  +----------------+")
    print("   a b c d e f g h\n")

def notation_to_pos(notation):
    """Convert algebraic notation to position"""
    col = ord(notation[0]) - ord('a')
    row = 8 - int(notation[1])
    return (row, col)

def check_all_legal_moves(engine, is_white):
    """Find all legal moves for a color"""
    print(f"\nChecking all legal moves for {'White' if is_white else 'Black'}:")
    legal_moves = []
    
    for from_row in range(8):
        for from_col in range(8):
            piece = engine.board_state[from_row][from_col]
            if piece == '.':
                continue
            
            piece_is_white = piece.isupper()
            if piece_is_white != is_white:
                continue
            
            for to_row in range(8):
                for to_col in range(8):
                    if (from_row, from_col) == (to_row, to_col):
                        continue
                    
                    # Check if move is valid
                    if engine.is_valid_move_python((from_row, from_col), (to_row, to_col)):
                        # Check if king would still be in check
                        would_be_check = engine.would_still_be_in_check(
                            (from_row, from_col), (to_row, to_col), is_white
                        )
                        
                        if not would_be_check:
                            from_notation = chr(ord('a') + from_col) + str(8 - from_row)
                            to_notation = chr(ord('a') + to_col) + str(8 - to_row)
                            legal_moves.append(f"{piece}{from_notation}-{to_notation}")
                            print(f"  Legal: {piece}{from_notation}-{to_notation}")
    
    if not legal_moves:
        print("  NO LEGAL MOVES FOUND!")
    
    return legal_moves

# Test Back Rank Mate
print("="*50)
print("Testing Back Rank Mate Position")
print("="*50)

engine = ChessEngineWrapper()

position = [
    ['.', '.', '.', 'R', 'k', '.', '.', '.'],  # 8th rank
    ['.', '.', '.', '.', '.', 'p', 'p', 'p'],  # 7th rank
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', 'P', 'P', 'P'],  # 2nd rank
    ['.', '.', '.', '.', 'K', '.', '.', '.']   # 1st rank
]

engine.set_position(position, current_turn=False)  # Black to move

print_board(engine.board_state)

# Find black king position
king_pos = None
for row in range(8):
    for col in range(8):
        if engine.board_state[row][col] == 'k':
            king_pos = (row, col)
            break

print(f"Black king position: {king_pos}")

# Check if king is in check
is_check = engine.is_king_in_check(False)
print(f"\nBlack king in check: {is_check}")

# Check what squares attack the king
if is_check:
    print("\nSquares attacking the king:")
    for row in range(8):
        for col in range(8):
            piece = engine.board_state[row][col]
            if piece != '.' and piece.isupper():  # White pieces
                if engine.is_valid_move_python((row, col), king_pos):
                    notation = chr(ord('a') + col) + str(8 - row)
                    print(f"  {piece} on {notation} attacks king")

# Find all legal moves
legal_moves = check_all_legal_moves(engine, False)

# Check if it's checkmate
is_mate = engine.is_checkmate(False)
print(f"\nCheckmate: {is_mate}")
print(f"Number of legal moves: {len(legal_moves)}")

if not is_mate and is_check:
    print("\n⚠️ King is in check but not in checkmate!")
    print("This means there's at least one escape move.")