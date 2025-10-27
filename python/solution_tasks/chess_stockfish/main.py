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
# Import new game modes
from game.puzzle_mode import PuzzleMode
from game.timed_mode import TimedMode
from game.adaptive_mode import AdaptiveMode

from utils.game_stats import GameStatistics
from utils.performance_monitor import get_performance_monitor  # Добавляем импорт

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
        print("   pip install pygame stockfish python-chess psutil")
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


def cleanup_game(game):
    """Безопасная очистка ресурсов игры."""
    try:
        if game and hasattr(game, 'cleanup'):
            game.cleanup()
        elif game and hasattr(game, 'engine') and game.engine:
            if hasattr(game.engine, 'quit'):
                game.engine.quit()
    except Exception as e:
        # Игнорируем ошибки при очистке
        pass


def run_classic_game(player_color, skill_level, theme):
    """Запустить классическую игру."""
    game = ChessGame(player_color=player_color, skill_level=skill_level, theme=theme)
    result = game.run()
    return result


def run_puzzle_mode(theme):
    """Запустить режим головоломок."""
    pygame.init()
    screen = pygame.display.set_mode((512, 612))  # Дополнительное пространство для UI
    pygame.display.set_caption("♟️  Шахматные головоломки — Maestro7IT")
    
    puzzle_mode = PuzzleMode(screen, theme)
    result = puzzle_mode.run()
    puzzle_mode.cleanup()
    return result


def run_timed_mode(player_color, theme):
    """Запустить режим игры на время."""
    pygame.init()
    screen = pygame.display.set_mode((512, 612))  # Дополнительное пространство для UI
    pygame.display.set_caption("⏱️  Игра на время — Maestro7IT")
    
    timed_mode = TimedMode(screen, player_color, 'blitz_3_0')  # По умолчанию блиц 3+0
    result = timed_mode.run()
    timed_mode.cleanup()
    return result


def run_adaptive_mode(player_color, theme):
    """Запустить адаптивный режим."""
    pygame.init()
    screen = pygame.display.set_mode((512, 612))  # Дополнительное пространство для UI
    pygame.display.set_caption("🧠  Адаптивная сложность — Maestro7IT")
    
    adaptive_mode = AdaptiveMode(screen, player_color, theme)
    result = adaptive_mode.run()
    adaptive_mode.cleanup()
    return result


def main():
    """
    Главная функция - точка входа в приложение.
    
    Инициализирует Pygame, показывает меню и запускает игру.
    Обрабатывает исключения и выводит полезные сообщения об ошибках.
    """
    # Инициализируем монитор производительности
    performance_monitor = get_performance_monitor()
    performance_monitor.start_monitoring(1.0)  # Мониторим каждую секунду
    print("✅ Монитор производительности запущен")
    
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
    
    game = None
    try:
        while True:  # Цикл для возвращения в главное меню
            menu_result = main_menu()
            # Handle menu return type (color, skill_level, theme, game_mode)
            if len(menu_result) == 4:
                player_color, skill_level, theme, game_mode = menu_result
            else:
                # Fallback to classic mode for older menu versions
                player_color, skill_level = menu_result
                theme = 'classic'
                game_mode = 'classic'
            
            # Запуск соответствующего режима игры
            if game_mode == 'classic':
                result = run_classic_game(player_color, skill_level, theme)
            elif game_mode == 'puzzle':
                result = run_puzzle_mode(theme)
            elif game_mode == 'timed':
                result = run_timed_mode(player_color, theme)
            elif game_mode == 'adaptive':
                result = run_adaptive_mode(player_color, theme)
            else:
                # По умолчанию классический режим
                result = run_classic_game(player_color, skill_level, theme)
            
            # Проверяем, нужно ли вернуться в главное меню
            if result == "main_menu":
                print("\nВозвращение в главное меню...\n")
                # Очищаем ресурсы перед возвратом в меню
                cleanup_game(game)
                game = None
                continue  # Возвращаемся к началу цикла (в главное меню)
            
            # Сохранить статистику игры (если это не режим головоломок)
            if game_mode != 'puzzle':
                try:
                    stats = GameStatistics()
                    # Если результат - статистика игры, сохраняем её
                    if isinstance(result, dict):
                        game_stats = result
                    else:
                        # Иначе получаем статистику из игры
                        game_stats = game.get_game_stats() if game else {}
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
            
            # Очищаем ресурсы игры
            cleanup_game(game)
            game = None
            
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
        # Очищаем ресурсы игры, если они еще не были очищены
        if game:
            cleanup_game(game)
        pygame.quit()
        
        # Останавливаем монитор производительности
        performance_monitor.stop_monitoring()
        performance_summary = performance_monitor.get_performance_summary()
        if performance_summary:
            print(f"\n📊 Сводка производительности:")
            print(f"   Время работы: {performance_summary.get('uptime_seconds', 0):.2f} сек")
            cpu_usage = performance_summary.get('cpu_usage', {})
            print(f"   CPU: среднее {cpu_usage.get('average', 0)}%")
            memory_usage = performance_summary.get('memory_usage', {})
            print(f"   Память: {memory_usage.get('process_memory_mb', {}).get('average', 0)} MB")
        
        performance_monitor.save_log()
        print("✅ Приложение закрыто\n")


if __name__ == "__main__":
    main()