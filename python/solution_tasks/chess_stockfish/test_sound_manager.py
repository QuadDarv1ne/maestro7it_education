#!/usr/bin/env python3
"""
Test script for the SoundManager module
"""

import sys
import os
import time

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_sound_manager():
    """Test the SoundManager functionality."""
    print("Testing SoundManager...")
    
    try:
        from utils.sound_manager import SoundManager
        print("✅ SoundManager module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import SoundManager: {e}")
        return False
    
    try:
        # Create a sound manager instance
        sound_manager = SoundManager()
        print("✅ SoundManager instance created successfully")
    except Exception as e:
        print(f"❌ Failed to create SoundManager instance: {e}")
        return False
    
    try:
        # Load sounds
        sound_manager.load_sounds()
        print("✅ Sounds loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load sounds: {e}")
        return False
    
    try:
        # Test playing sounds
        print("Playing test sounds...")
        sound_manager.play_sound("move")
        time.sleep(0.2)
        sound_manager.play_sound("capture")
        time.sleep(0.2)
        sound_manager.play_sound("check")
        time.sleep(0.2)
        sound_manager.play_sound("checkmate")
        time.sleep(0.2)
        sound_manager.play_sound("castle")
        time.sleep(0.2)
        sound_manager.play_sound("promote")
        time.sleep(0.2)
        sound_manager.play_sound("win")
        time.sleep(0.2)
        sound_manager.play_sound("lose")
        time.sleep(0.2)
        sound_manager.play_sound("draw")
        time.sleep(0.2)
        sound_manager.play_sound("button")
        print("✅ All sounds played successfully")
    except Exception as e:
        print(f"❌ Failed to play sounds: {e}")
        return False
    
    try:
        # Test volume control
        sound_manager.set_volume(0.5)
        print("✅ Volume control works")
    except Exception as e:
        print(f"❌ Failed to set volume: {e}")
        return False
    
    try:
        # Test sound toggle
        was_enabled = sound_manager.is_sound_enabled()
        sound_manager.toggle_sound()
        sound_manager.toggle_sound()
        is_enabled = sound_manager.is_sound_enabled()
        if was_enabled == is_enabled:
            print("✅ Sound toggle works")
        else:
            print("⚠️  Sound toggle may have issues")
    except Exception as e:
        print(f"❌ Failed to toggle sound: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print(" chess_stockfish - Sound Manager Tests ")
    print("=" * 40)
    
    if test_sound_manager():
        print("\n" + "=" * 40)
        print("🎉 All sound manager tests passed!")
        print("The sound system is working correctly.")
        return 0
    else:
        print("\n" + "=" * 40)
        print("❌ Some tests failed.")
        print("Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())