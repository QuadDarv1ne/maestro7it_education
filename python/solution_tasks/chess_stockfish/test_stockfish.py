#!/usr/bin/env python3
"""
Test script to verify Stockfish installation
"""

import sys
import os

def test_stockfish():
    """Test if Stockfish is properly installed and accessible."""
    try:
        from stockfish import Stockfish
        print("✅ Stockfish Python library imported successfully")
        
        # Try to create a Stockfish instance
        try:
            engine = Stockfish()
            print("✅ Stockfish engine created successfully")
            
            # Test basic functionality
            fen = engine.get_fen_position()
            print(f"✅ Initial FEN position: {fen}")
            
            # Test making a move
            engine.make_moves_from_current_position(["e2e4"])
            new_fen = engine.get_fen_position()
            print(f"✅ After e4 move: {new_fen}")
            
            # engine.quit()  # Not all versions have this method
            return True
            
        except Exception as e:
            print(f"❌ Error creating Stockfish engine: {e}")
            print("💡 This usually means Stockfish executable is not found in PATH")
            print("💡 Please download Stockfish from https://stockfishchess.org/download/")
            print("💡 and add it to your system PATH")
            return False
            
    except ImportError as e:
        print(f"❌ Stockfish library not installed: {e}")
        print("💡 Install it with: pip install stockfish")
        return False

if __name__ == "__main__":
    print("Testing Stockfish installation...")
    success = test_stockfish()
    if success:
        print("\n🎉 All tests passed! Stockfish is ready to use.")
    else:
        print("\n❌ Tests failed. Please check the installation instructions in README.md")
        sys.exit(1)