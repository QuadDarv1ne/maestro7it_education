#!/usr/bin/env python3
"""
Main entry point for the chess game.
"""

from game.chess_game import ChessGame

def run_chess_game():
    """Запустить игру в шахматы."""
    try:
        print("Добро пожаловать в шахматы!")
        print("Выберите настройки игры:")
        
        # Выбор цвета
        while True:
            color_choice = input("Выберите цвет (w - белые, b - чёрные): ").lower().strip()
            if color_choice in ['w', 'b', 'white', 'black']:
                player_color = 'white' if color_choice.startswith('w') else 'black'
                break
            print("Пожалуйста, введите 'w' для белых или 'b' для чёрных.")
        
        # Выбор уровня сложности
        while True:
            try:
                skill_level = int(input("Выберите уровень сложности (0-20, по умолчанию 5): ") or "5")
                if 0 <= skill_level <= 20:
                    break
                print("Уровень должен быть от 0 до 20.")
            except ValueError:
                print("Пожалуйста, введите число от 0 до 20.")
        
        # Выбор темы
        themes = ['classic', 'dark', 'blue', 'green', 'contrast']
        print("Доступные темы:", ", ".join(themes))
        theme_choice = input("Выберите тему (по умолчанию classic): ").strip().lower()
        if theme_choice not in themes:
            theme_choice = 'classic'
        
        print(f"\nНастройки игры:")
        print(f"  Цвет: {player_color}")
        print(f"  Уровень сложности: {skill_level}")
        print(f"  Тема: {theme_choice}")
        print("\nГорячие клавиши:")
        print("  ЛКМ - выбрать/сделать ход")
        print("  ПКМ - снять выделение")
        print("  ←/→ - навигация по ходам")
        print("  R - новая игра")
        print("  T - подсказка")
        print("  A - анализ позиции")
        print("  S - сохранить партию")
        print("  L - загрузить партию")
        print("  G - резюме игры")
        print("  D - детальный анализ")
        print("  ESC - меню")
        print("\nНажмите Enter для начала игры...")
        input()
        
        # Создаем и запускаем игру
        game = ChessGame(player_color=player_color, skill_level=skill_level, theme=theme_choice)
        result = game.run()
        
        # Проверяем, нужно ли вернуться в главное меню
        if result == "main_menu":
            print("\nВозвращение в главное меню...\n")
            return  # Возвращаемся в главное меню
        
        # Если результат - статистика игры, показываем её
        if isinstance(result, dict):
            stats = result
        else:
            # Иначе получаем статистику из игры
            stats = game.get_game_stats()
            
        print("\n" + "="*50)
        print("Игра завершена. Статистика:")
        print("="*50)
        print(f"Всего ходов: {stats.get('total_moves', 0)}")
        print(f"Взятий игрока: {stats.get('player_captures', 0)}")
        print(f"Взятий компьютера: {stats.get('ai_captures', 0)}")
        print(f"Шахов: {stats.get('check_count', 0)}")
        print(f"Среднее время хода: {stats.get('avg_move_time', 0):.2f} сек")
        if stats.get('duration', 0) > 0:
            print(f"Длительность игры: {int(stats.get('duration', 0))} сек")
        print(f"Результат: {stats.get('result', 'ongoing')}")
        if stats.get('game_reason'):
            print(f"Причина окончания: {stats.get('game_reason')}")
        
    except KeyboardInterrupt:
        print("\n\nИгра прервана пользователем.")
    except Exception as e:
        print(f"\nОшибка при запуске игры: {e}")

if __name__ == "__main__":
    run_chess_game()
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
import shutil

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics

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
            menu_result: tuple = main_menu()  # Type annotation to help linter
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
import shutil

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics

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
            menu_result: tuple = main_menu()  # Type annotation to help linter
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
import shutil

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics

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
            menu_result: tuple = main_menu()  # Type annotation to help linter
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
import shutil

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics

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
            menu_result: tuple = main_menu()  # Type annotation to help linter
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
import shutil

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics

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
            menu_result: tuple = main_menu()  # Type annotation to help linter
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
import shutil

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics

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
            menu_result: tuple = main_menu()  # Type annotation to help linter
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
import shutil

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics

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
            menu_result: tuple = main_menu()  # Type annotation to help linter
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
import shutil

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics

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
            menu_result: tuple = main_menu()  # Type annotation to help linter
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
import shutil

# Import our game modules
from game.menu import main_menu
from game.chess_game import ChessGame
from utils.game_stats import GameStatistics

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
            menu_result: tuple = main_menu()  # Type annotation to help linter
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
    - utils/game_state.py: Сохранение и загрузка