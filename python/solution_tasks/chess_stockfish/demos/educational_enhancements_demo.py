#!/usr/bin/env python3
"""
Educational enhancements demo for chess_stockfish.

This script demonstrates the educational features and improvements added to the chess game.
"""

import time
import sys
import os

# Add project path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.educational import ChessEducator
from utils.opening_book import OpeningBook


def demonstrate_educational_features():
    """Demonstrate educational features of the chess game."""
    print("🎓 EDUCATIONAL FEATURES DEMO")
    print("=" * 50)
    
    # Create educator
    educator = ChessEducator()
    
    print("1. Piece Movement Hints:")
    piece_hints = [
        ('pawn', 'пешка'),
        ('knight', 'конь'),
        ('bishop', 'слон'),
        ('rook', 'ладья'),
        ('queen', 'ферзь'),
        ('king', 'король')
    ]
    
    for piece_en, piece_ru in piece_hints:
        hint = educator.get_piece_hint(piece_ru)
        print(f"   {piece_ru.capitalize()}: {hint}")
    
    print()
    
    print("2. Educational Feedback:")
    feedback_examples = [
        (1, time.time()),
        (5, time.time()),
        (10, time.time()),
        (20, time.time()),
        (50, time.time())
    ]
    
    for move_count, current_time in feedback_examples:
        feedback = educator.get_educational_feedback(move_count, current_time)
        if feedback:
            print(f"   After {move_count} moves: {feedback}")
    
    print()
    
    print("3. Chess Principles:")
    # Get principles from opening book
    opening_book = OpeningBook()
    for i in range(5):
        principle, explanation = opening_book.get_random_principle()
        print(f"   {i+1}. {principle}")
    
    print()


def demonstrate_opening_book():
    """Demonstrate opening book functionality."""
    print("📚 OPENING BOOK DEMO")
    print("=" * 50)
    
    # Create opening book
    opening_book = OpeningBook()
    
    print("1. Popular Openings:")
    # Show some openings from the book
    opening_names = list(opening_book.__class__.__dict__.get('OPENING_BOOK', {}))[:5]
    for i, name in enumerate(opening_names, 1):
        info = opening_book.get_opening_info(name)
        if info:
            print(f"   {i}. {name}: {info['description']}")
    
    print()
    
    print("2. Opening Tracking:")
    # Simulate some moves
    test_moves = ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1b5']
    
    for move in test_moves:
        opening_book.add_move(move)
        current_opening = opening_book.get_current_opening()
        if current_opening:
            name, info = current_opening
            print(f"   Move {move}: {name}")
        else:
            print(f"   Move {move}: Not in opening book")
    
    print()
    
    print("3. Opening Statistics:")
    learned = opening_book.get_learned_openings()
    print(f"   Total moves tracked: {len(opening_book.move_sequence)}")
    print(f"   Learned openings: {len(learned)}")
    
    print()


def demonstrate_advanced_tips():
    """Demonstrate advanced educational tips."""
    print("🧠 ADVANCED EDUCATIONAL TIPS")
    print("=" * 50)
    
    educator = ChessEducator()
    
    print("1. Tactical Patterns:")
    tactics = [
        "fork",
        "pin",
        "skewer",
        "discovery",
        "deflection"
    ]
    
    for tactic in tactics:
        motiv = educator.get_tactical_motiv()
        print(f"   {tactic.capitalize()}: {motiv}")
    
    print()
    
    print("2. Endgame Principles:")
    for i in range(5):
        tip = educator.get_endgame_tip()
        print(f"   {i+1}. {tip}")
    
    print()
    
    print("3. Common Mistakes:")
    for i in range(5):
        fact = educator.get_historical_fact()
        print(f"   {i+1}. {fact}")
    
    print()


def demonstrate_interactive_learning():
    """Demonstrate interactive learning features."""
    print("🎮 INTERACTIVE LEARNING DEMO")
    print("=" * 50)
    
    educator = ChessEducator()
    
    print("1. Move Quality Assessment:")
    # Simulate different types of moves
    moves = [
        ("e2e4", "Good opening move, controls center"),
        ("f2f3", "Weak move, weakens king position"),
        ("d1h5", "Developing queen early, potentially risky"),
        ("g1f3", "Good developing move, controls center")
    ]
    
    for move, description in moves:
        tip = educator.get_random_tip()
        print(f"   Move {move}: {tip}")
        print(f"      Explanation: {description}")
    
    print()
    
    print("2. Positional Evaluation:")
    positions = [
        "start",  # Starting position
        "center_control",  # Center control
        "king_exposed",  # Exposed king
        "piece_development"  # Piece development
    ]
    
    for position_type in positions:
        fact = educator.get_historical_fact()
        print(f"   Position {position_type}: {fact}")
    
    print()


def main():
    """Main demo function."""
    print("🎓 EDUCATIONAL ENHANCEMENTS DEMO")
    print("Chess Stockfish - Maestro7IT Education")
    print("=" * 60)
    print()
    
    # Demonstrate all educational features
    demonstrate_educational_features()
    demonstrate_opening_book()
    demonstrate_advanced_tips()
    demonstrate_interactive_learning()
    
    print("=" * 60)
    print("🎉 EDUCATIONAL DEMO COMPLETED")
    print("=" * 60)
    print()
    print("Key Educational Improvements:")
    print("• Enhanced piece movement hints")
    print("• Advanced tactical pattern recognition")
    print("• Opening book with popular openings")
    print("• Interactive move quality assessment")
    print("• Positional evaluation guidance")
    print("• Endgame principles and tips")
    print("• Common mistake prevention")
    print()
    print("Run 'python main_optimized.py' to experience these features in the game!")


if __name__ == "__main__":
    main()