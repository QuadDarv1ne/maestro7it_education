#!/usr/bin/env python3
"""
chess_stockfish — Полнофункциональная шахматная игра со Stockfish

Описание:
    Интерактивная шахматная игра с использованием движка Stockfish.
    Игрок может выбрать сторону (белые/чёрные) и уровень сложности (0-20).
    
Основные компоненты:
    - engine/stockfish_wrapper.py: Обёртка для работы со Stockfish
    - ui/board_renderer.py: Отображение шахматной доски в Pygame
    - game/chess_game.py: Основная логика игры
    - game/menu.py: Консольное меню выбора параметров
    - utils/game_state.py: Сохранение и загрузка игр (PGN)
    - utils/game_stats.py: Статистика игр
    
Требования:
    - pygame: Визуализация и UI
    - stockfish: Шахматный движок
    - python-chess: Работа с позициями и ходами
    
Запуск:
    python main.py

Автор: Maestro7IT Education
Лицензия: MIT
"""

import pygame
from typing import Optional, Tuple, List
import time
import os
import sys

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utills.game_stats import GameStatistics

# ============================================================================
# main.py
# ============================================================================

"""
Модуль: main.py

Описание:
    Точка входа в приложение chess_stockfish.
    Инициализирует Pygame, запускает меню и начинает игру.
    
Возможности:
    - Проверка наличия зависимостей
    - Обработка ошибок при запуске
    - Красивый вывод ошибок с подсказками
"""


def check_dependencies():
    """
    Проверяет наличие необходимых зависимостей.
    
    Возвращает:
        bool: True если все зависимости установлены, False иначе
    """
    try:
        import pygame
        import stockfish
        return True
    except ImportError as e:
        print(f"\n❌ Ошибка импорта: {e}")
        print("\n💡 РЕШЕНИЕ: Установите необходимые зависимости:")
        print("   pip install pygame stockfish python-chess")
        return False


def show_stats():
    """Показать статистику игр."""
    try:
        stats = GameStatistics()
        summary = stats.get_summary()
        print(f"\n📊 Статистика игр:")
        print(f"   Всего игр: {summary['total_games']}")
        print(f"   Побед: {summary['total_wins']}")
        print(f"   Поражений: {summary['total_losses']}")
        if summary['total_games'] > 0:
            print(f"   Процент побед: {summary['win_rate']:.1f}%")
        print()
    except Exception as e:
        print(f"⚠️  Не удалось загрузить статистику: {e}")


def main():
    """
    Главная функция - точка входа в приложение.
    
    Инициализирует Pygame, показывает меню и запускает игру.
    Обрабатывает исключения и выводит полезные сообщения об ошибках.
    """
    # Проверка зависимостей
    if not check_dependencies():
        sys.exit(1)
    
    # Показать статистику перед началом игры
    show_stats()
    
    pygame.init()
    
    try:
        player_color, skill_level = main_menu()
        game = ChessGame(player_color=player_color, skill_level=skill_level)
        game.run()
        
        # Сохранить статистику игры
        try:
            stats = GameStatistics()
            game_stats = game.get_game_stats()
            stats.save_game(game_stats)
            print("📊 Статистика игры сохранена")
            
            # Показать обновленную статистику
            summary = stats.get_summary()
            print(f"\n📈 Обновленная статистика:")
            print(f"   Всего игр: {summary['total_games']}")
            print(f"   Побед: {summary['total_wins']}")
            print(f"   Поражений: {summary['total_losses']}")
            if summary['total_games'] > 0:
                print(f"   Процент побед: {summary['win_rate']:.1f}%")
            print()
        except Exception as e:
            print(f"⚠️  Не удалось сохранить статистику: {e}")
        
    except RuntimeError as e:
        print(f"\n❌ Ошибка: {e}")
        print("\n💡 РЕШЕНИЕ: Убедитесь, что Stockfish установлен на вашу систему:")
        print("\n   Windows:")
        print("      1. Скачайте с https://stockfishchess.org/download/")
        print("      2. Разархивируйте stockfish.exe в C:\\Program Files\\stockfish\\")
        print("      3. Добавьте в PATH или укажите полный путь в коде\n")
        print("   Linux/macOS:")
        print("      Linux:  sudo apt-get install stockfish")
        print("      macOS:  brew install stockfish\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Игра прервана пользователем")
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        pygame.quit()
        print("✅ Приложение закрыто\n")


if __name__ == "__main__":
    main()