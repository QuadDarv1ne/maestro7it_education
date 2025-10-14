#!/usr/bin/env python3
"""
Точка входа в приложение chess_stockfish
"""

from game.menu import main_menu
from game.chess_game import ChessGame
import pygame
import sys

def main():
    player_color, skill_level = main_menu()
    
    try:
        game = ChessGame(player_color=player_color, skill_level=skill_level)
        game.run()
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()