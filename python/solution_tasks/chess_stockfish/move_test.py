#!/usr/bin/env python3
"""
Test script for move validation
"""

# Simple test without Stockfish to check basic logic
def test_basic_chess_rules():
    """Test basic chess rules for pawn movement"""
    print("=== Тестирование базовых шахматных правил ===")
    
    # In chess, a pawn can move:
    # 1. One square forward from any position
    # 2. Two squares forward ONLY from its starting position (rank 2 for white, rank 7 for black)
    
    print("Правила движения пешки:")
    print("1. Пешка может двигаться на одну клетку вперед из любой позиции")
    print("2. Пешка может двигаться на две клетки вперед ТОЛЬКО из начальной позиции")
    print("   - Белые пешки: начальная позиция на горизонтали 2 (ранг 2)")
    print("   - Черные пешки: начальная позиция на горизонтали 7 (ранг 7)")
    print()
    
    # Examples of valid moves from starting position
    print("Примеры корректных ходов пешки из начальной позиции:")
    print("e2e4 - белая пешка e2 -> e4 (2 клетки вперед) ✓")
    print("e2e3 - белая пешка e2 -> e3 (1 клетка вперед) ✓")
    print("e7e5 - черная пешка e7 -> e5 (2 клетки вперед) ✓")
    print("e7e6 - черная пешка e7 -> e6 (1 клетка вперед) ✓")
    print()
    
    # Examples of valid moves from non-starting position
    print("Примеры корректных ходов пешки НЕ из начальной позиции:")
    print("e3e4 - белая пешка e3 -> e4 (1 клетка вперед) ✓")
    print("e3e5 - белая пешка e3 -> e5 (2 клетки вперед) ✗ (некорректно)")
    print()

if __name__ == "__main__":
    test_basic_chess_rules()
    print("\n=== Тестирование завершено ===")