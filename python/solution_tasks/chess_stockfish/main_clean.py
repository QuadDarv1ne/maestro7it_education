#!/usr/bin/env python3
"""
Main entry point for the chess game.
"""

import pygame
import sys
import shutil
from typing import Tuple, Union

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics


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
        print(f"   Ничьих: {summary['total_draws']}")
        if summary['total_games'] > 0:
            print(f"   Процент побед: {summary['win_rate']:.1f}%")
        print()
    except Exception as e:
        print(f"⚠️  Не удалось загрузить статистику: {e}")


def check_stockfish_installed():
    """Проверяет, установлен ли Stockfish в системе."""
    return shutil.which("stockfish") is not None


def suggest_stockfish_installation():
    """Предлагает пользователю варианты установки Stockfish."""
    print("\n💡 ВНИМАНИЕ: Stockfish не найден в системе!")
    print("\nДля полноценной работы игры необходимо установить Stockfish.")
    print("\nВарианты установки:")
    print("  1. Автоматическая установка:")
    print("     Запустите install_stockfish.bat")
    print("\n  2. Ручная установка:")
    print("     - Скачайте с https://stockfishchess.org/download/")
    print("     - Распакуйте в папку (например, C:\\Program Files\\stockfish)")
    print("     - Добавьте путь к папке в переменные среды PATH")
    print("\n  3. Проверка установки:")
    print("     Запустите: python check_installation.py")
    print("\nБез Stockfish игра будет работать в ограниченном режиме.")


def main():
    """
    Главная функция - точка входа в приложение.
    
    Инициализирует Pygame, показывает меню и запускает игру.
    Обрабатывает исключения и выводит полезные сообщения об ошибках.
    """
    # Проверка зависимостей
    if not check_dependencies():
        sys.exit(1)
    
    # Проверка наличия Stockfish
    if not check_stockfish_installed():
        suggest_stockfish_installation()
        # Спросить пользователя, хочет ли он продолжить в ограниченном режиме
        choice = input("\nПродолжить в ограниченном режиме? (y/n): ").strip().lower()
        if choice not in ('y', 'yes', 'д', 'да'):
            print("Выход из программы. Установите Stockfish для полноценной работы.")
            sys.exit(1)
    
    # Показать статистику перед началом игры
    show_stats()
    
    pygame.init()
    
    try:
        while True:  # Цикл для возвращения в главное меню
            menu_result: Union[Tuple[str, int], Tuple[str, int, str]] = main_menu()
            # Handle both old and new menu return types
            if len(menu_result) == 3:
                player_color, skill_level, theme = menu_result
            else:
                player_color, skill_level = menu_result
                theme = 'classic'
            
            game = ChessGame(player_color=player_color, skill_level=skill_level, theme=theme)
            result = game.run()
            
            # Проверяем, нужно ли вернуться в главное меню
            if result == "main_menu":
                print("\nВозвращение в главное меню...\n")
                continue  # Возвращаемся к началу цикла (в главное меню)
            
            # Сохранить статистику игры
            try:
                stats = GameStatistics()
                # Если результат - статистика игры, сохраняем её
                if isinstance(result, dict):
                    game_stats = result
                else:
                    # Иначе получаем статистику из игры
                    game_stats = game.get_game_stats()
                stats.save_game(game_stats)
                print("📊 Статистика игры сохранена")
                
                # Показать обновленную статистику
                summary = stats.get_summary()
                print(f"\n📈 Обновленная статистика:")
                print(f"   Всего игр: {summary['total_games']}")
                print(f"   Побед: {summary['total_wins']}")
                print(f"   Поражений: {summary['total_losses']}")
                print(f"   Ничьих: {summary['total_draws']}")
                if summary['total_games'] > 0:
                    print(f"   Процент побед: {summary['win_rate']:.1f}%")
                print()
            except Exception as e:
                print(f"⚠️  Не удалось сохранить статистику: {e}")
            
            # Спросить, хочет ли игрок сыграть еще раз
            play_again = input("Хотите сыграть еще раз? (y/n): ").strip().lower()
            if play_again not in ('y', 'yes', 'д', 'да'):
                break  # Выход из цикла и завершение программы
        
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