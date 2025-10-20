#!/usr/bin/env python3
"""
Check if all dependencies for the chess game are properly installed
"""

import sys
import os
import importlib

def check_python_packages():
    """Check if all required Python packages are installed."""
    required_packages = [
        'pygame',
        'stockfish',
        'chess'  # python-chess
    ]
    
    print("Checking Python packages...")
    all_good = True
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package} - {e}")
            all_good = False
    
    return all_good

def check_stockfish_executable():
    """Check if Stockfish executable is in PATH."""
    print("\nChecking Stockfish executable...")
    import shutil
    
    stockfish_path = shutil.which("stockfish")
    if stockfish_path:
        print(f"  ✅ Found Stockfish at: {stockfish_path}")
        return True
    else:
        print("  ❌ Stockfish executable not found in PATH")
        print("     Please download Stockfish from https://stockfishchess.org/download/")
        print("     and add it to your system PATH")
        return False

def main():
    """Main function to check installation."""
    print(" chess_stockfish - Installation Checker ")
    print("=" * 40)
    
    # Check Python packages
    packages_ok = check_python_packages()
    
    # Check Stockfish executable
    stockfish_ok = check_stockfish_executable()
    
    print("\n" + "=" * 40)
    if packages_ok and stockfish_ok:
        print("🎉 All checks passed! You're ready to play chess.")
        print("   Run 'python main.py' to start the game.")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()