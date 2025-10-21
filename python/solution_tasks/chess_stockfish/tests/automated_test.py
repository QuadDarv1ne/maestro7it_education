#!/usr/bin/env python3
"""
Automated test script to verify chess_stockfish components without user interaction
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pygame

def test_pygame():
    """Test Pygame initialization."""
    print("Testing Pygame initialization...")
    try:
        pygame.init()
        print("✅ Pygame initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Pygame initialization failed: {e}")
        return False

def test_imports():
    """Test importing all modules."""
    print("\nTesting module imports...")
    modules = {
        'Chess Game': 'game.chess_game',
        'Stockfish Wrapper': 'engine.stockfish_wrapper',
        'Board Renderer': 'ui.board_renderer',
        'Game Stats': 'utils.game_stats',
        'Menu': 'game.menu'
    }
    
    all_passed = True
    for name, module in modules.items():
        try:
            __import__(module)
            print(f"✅ {name} module imported successfully")
        except Exception as e:
            print(f"❌ {name} module import failed: {e}")
            all_passed = False
    
    return all_passed

def test_stockfish_library():
    """Test Stockfish library import."""
    print("\nTesting Stockfish library...")
    try:
        from stockfish import Stockfish
        print("✅ Stockfish library imported successfully")
        return True
    except Exception as e:
        print(f"❌ Stockfish library import failed: {e}")
        return False

def test_chess_library():
    """Test python-chess library import."""
    print("\nTesting python-chess library...")
    try:
        import chess
        print("✅ python-chess library imported successfully")
        return True
    except Exception as e:
        print(f"❌ python-chess library import failed: {e}")
        return False

def main():
    """Run all tests."""
    print(" chess_stockfish - Automated Tests ")
    print("=" * 35)
    
    # Run all tests
    tests = [
        test_pygame,
        test_imports,
        test_stockfish_library,
        test_chess_library
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Summary
    print("\n" + "=" * 35)
    if all(results):
        print("🎉 All automated tests passed!")
        print("The core components are working correctly.")
        return 0
    else:
        print("❌ Some tests failed.")
        print("Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())