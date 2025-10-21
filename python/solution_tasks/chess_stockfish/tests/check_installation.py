#!/usr/bin/env python3
"""
Check if all dependencies for the chess game are properly installed
"""

import sys
import os
import importlib
import shutil

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
        
        # Try to get version info
        try:
            import subprocess
            result = subprocess.run([stockfish_path, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"  📄 Version info: {result.stdout.strip()}")
            else:
                print(f"  ⚠️  Could not get version info")
        except Exception as e:
            print(f"  ⚠️  Could not get version info: {e}")
            
        return True
    else:
        print("  ❌ Stockfish executable not found in PATH")
        print("     Please download Stockfish from https://stockfishchess.org/download/")
        print("     and add it to your system PATH")
        return False

def check_system_info():
    """Display system information for troubleshooting."""
    print("\nSystem Information:")
    print(f"  Platform: {sys.platform}")
    print(f"  Python version: {sys.version}")
    print(f"  Python executable: {sys.executable}")
    
    # Check PATH
    path_dirs = os.environ.get('PATH', '').split(os.pathsep)
    print(f"  PATH directories: {len(path_dirs)} found")
    
    # Check common Stockfish locations
    common_locations = [
        "C:\\Program Files\\stockfish",
        "C:\\Program Files (x86)\\stockfish",
        "C:\\stockfish",
        "/usr/local/bin",
        "/usr/bin"
    ]
    
    print("\nChecking common Stockfish locations:")
    found_locations = []
    for location in common_locations:
        if os.path.exists(location):
            files = [f for f in os.listdir(location) if 'stockfish' in f.lower()]
            if files:
                found_locations.append((location, files))
                print(f"  📁 {location}: {files}")
    
    if not found_locations:
        print("  ❌ No Stockfish installations found in common locations")

def main():
    """Main function to check installation."""
    print(" chess_stockfish - Installation Checker ")
    print("=" * 40)
    
    # Show system info
    check_system_info()
    
    # Check Python packages
    packages_ok = check_python_packages()
    
    # Check Stockfish executable
    stockfish_ok = check_stockfish_executable()
    
    print("\n" + "=" * 40)
    if packages_ok and stockfish_ok:
        print("🎉 All checks passed! You're ready to play chess.")
        print("   Run 'python main.py' to start the game.")
        return 0
    elif packages_ok:
        print("⚠️  Python packages are OK, but Stockfish executable is missing.")
        print("   You can play in limited mode, but AI opponent won't work.")
        print("   To fix this, install Stockfish and add it to PATH.")
        print("\nSuggested actions:")
        print("  1. Run install_stockfish.bat for automated installation")
        print("  2. Or manually download from https://stockfishchess.org/download/")
        print("  3. Run this script again after installation")
        return 0  # Don't exit with error, allow limited mode
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())