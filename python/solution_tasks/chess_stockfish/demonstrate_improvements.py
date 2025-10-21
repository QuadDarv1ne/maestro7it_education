#!/usr/bin/env python3
"""
Demonstration script for the new improvements in chess_stockfish
"""

import sys
import os
import time

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def demonstrate_sound_system():
    """Demonstrate the new sound system."""
    print("🎵 Demonstrating Sound System...")
    
    try:
        from utils.sound_manager import SoundManager
        sound_manager = SoundManager()
        sound_manager.load_sounds()
        
        print("Playing various game sounds:")
        sounds = [
            ("move", "♙ Фигура перемещена"),
            ("capture", "✓ Фигура взята"),
            ("check", "⚠ Шах королю"),
            ("checkmate", "♚ Мат! Игра окончена"),
            ("castle", "♖ Рокировка"),
            ("promote", "♛ Пешка превращена"),
            ("win", "🏆 Победа!"),
            ("lose", "💀 Поражение"),
            ("draw", "🤝 Ничья"),
            ("button", "🖱 Клик по кнопке")
        ]
        
        for sound_name, description in sounds:
            print(f"  {description}")
            sound_manager.play_sound(sound_name)
            time.sleep(0.5)
            
        print("✅ Sound system demonstration completed!")
        return True
    except Exception as e:
        print(f"❌ Sound system demonstration failed: {e}")
        return False

def demonstrate_move_timers():
    """Demonstrate the move timer functionality."""
    print("\n⏱ Demonstrating Move Timer System...")
    
    try:
        # Import the ChessGame class
        from game.chess_game import ChessGame
        
        # Create a game instance (this will initialize the move timers)
        print("Creating chess game instance...")
        game = ChessGame(player_color='white', skill_level=1)
        
        # Show initial timer state
        print(f"Initial player time: {game.move_timers['player']:.2f} seconds")
        print(f"Initial AI time: {game.move_timers['ai']:.2f} seconds")
        
        # Simulate some time passing
        print("Simulating game play...")
        time.sleep(1)
        
        # Show timer state after some time
        print(f"Player time after 1 second: {game.move_timers['player']:.2f} seconds")
        print(f"AI time after 1 second: {game.move_timers['ai']:.2f} seconds")
        
        print("✅ Move timer demonstration completed!")
        return True
    except Exception as e:
        print(f"❌ Move timer demonstration failed: {e}")
        return False

def main():
    """Run all demonstrations."""
    print(" chess_stockfish - New Improvements Demonstration ")
    print("=" * 50)
    
    success = True
    
    # Demonstrate sound system
    if not demonstrate_sound_system():
        success = False
    
    # Demonstrate move timers
    if not demonstrate_move_timers():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All demonstrations completed successfully!")
        print("\nNew features in chess_stockfish:")
        print("  🎵 Sound System - Audio feedback for game events")
        print("  ⏱ Move Timers - Track thinking time for players")
        print("  🛠 Improved Stability - Fixed duplicate methods and type issues")
        print("\nThese improvements enhance the gaming experience and provide")
        print("better educational value for chess students.")
    else:
        print("❌ Some demonstrations failed.")
        print("Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())