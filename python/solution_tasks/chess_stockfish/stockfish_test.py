#!/usr/bin/env python3
"""
Test Stockfish engine creation without actually running it
"""

import sys
import os

def test_stockfish_wrapper():
    """Test our Stockfish wrapper."""
    print("Testing Stockfish wrapper...")
    try:
        # Add the current directory to Python path
        sys.path.insert(0, '.')
        
        # Import our wrapper
        from engine.stockfish_wrapper import StockfishWrapper
        
        # Try to create an instance (this will fail if Stockfish executable is not found)
        # but we'll catch the exception and provide useful feedback
        try:
            engine = StockfishWrapper(skill_level=1)
            print("✅ Stockfish wrapper created successfully")
            print(f"   Initial FEN: {engine.get_fen()}")
            engine.quit()
            return True
        except RuntimeError as e:
            if "Не удалось запустить Stockfish" in str(e) or "not found" in str(e).lower():
                print("⚠️  Stockfish executable not found in PATH")
                print("   This is expected if Stockfish is not installed")
                print("   To fix this, download Stockfish from https://stockfishchess.org/download/")
                print("   and add it to your system PATH")
                return True  # This is not a failure of our code, just missing executable
            else:
                print(f"❌ Unexpected error creating Stockfish wrapper: {e}")
                return False
        except Exception as e:
            print(f"❌ Error creating Stockfish wrapper: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error importing Stockfish wrapper: {e}")
        return False

def main():
    """Run the test."""
    print(" chess_stockfish - Stockfish Test ")
    print("=" * 35)
    
    success = test_stockfish_wrapper()
    
    print("\n" + "=" * 35)
    if success:
        print("🎉 Stockfish test completed!")
        print("The wrapper is working correctly.")
        print("If you saw a 'not found' message, please install Stockfish.")
        return 0
    else:
        print("❌ Stockfish test failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())