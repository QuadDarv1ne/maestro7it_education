# ============================================================================
# game/menu.py
# ============================================================================

"""
Модуль: game/menu.py

Описание:
    Содержит функции для интерактивного меню выбора параметров игры.
    Позволяет игроку выбрать:
    - Сторону (белые/чёрные)
    - Уровень сложности Stockfish (0-20)
    - Режим игры (классический, головоломки, на время, адаптивный)
    
Возможности:
    - Валидация ввода
    - Подробная справка по уровням сложности
    - Красивое оформление консоли
"""

from typing import Tuple
from utils.game_stats import GameStatistics


def show_difficulty_guide():
    """
    Показать справку по уровням сложности Stockfish.
    
    Объясняет, что означают разные уровни сложности.
    """
    print("\n📚 Уровни сложности Stockfish:")
    print("   0-3   : Новичок (очень лёгкий)")
    print("   4-7   : Любитель (лёгкий)")
    print("   8-11  : Средний (умеренный)")
    print("   12-15 : Сильный (сложный)")
    print("   16-20 : Эксперт (очень сложный)")
    print()


def show_game_modes():
    """
    Показать справку по режимам игры.
    
    Объясняет, что представляют собой различные режимы игры.
    """
    print("\n🎮 Режимы игры:")
    print("   classic     : Классическая игра против Stockfish")
    print("   puzzle      : Решение шахматных головоломок")
    print("   timed       : Игра на время (блиц, рапид, пуля)")
    print("   adaptive    : Адаптивная сложность под ваш уровень")
    print()


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
        
        # Показать статистику по уровням
        level_stats = stats.get_level_performance()
        if level_stats:
            print("📈 Статистика по уровням сложности:")
            for level in sorted(level_stats.keys()):
                ls = level_stats[level]
                print(f"   Уровень {level}: {ls['wins']}/{ls['total']} побед ({ls['win_rate']:.1f}%)")
            print()
    except Exception as e:
        print(f"⚠️  Не удалось загрузить статистику: {e}")


def main_menu() -> Tuple[str, int, str, str]:
    """
    Главное меню выбора параметров игры.
    
    Выводит приветствие, справку и запрашивает параметры игры.
    
    Возвращает:
        Tuple[str, int, str, str]: Кортеж (color, skill_level, theme, game_mode)
            - color: 'white' или 'black'
            - skill_level: уровень сложности (0-20)
            - theme: цветовая тема
            - game_mode: режим игры ('classic', 'puzzle', 'timed', 'adaptive')
    """
    print("\n" + "="*70)
    print("♟️  chess_stockfish — УЛУЧШЕННАЯ ВЕРСИЯ — Maestro7IT Education")
    print("="*70)
    print("\n🎯 Добро пожаловать в шахматный тренер со Stockfish!\n")
    print("✨ Новые возможности улучшенной версии:")
    print("   ✓ Оценка позиции в реальном времени")
    print("   ✓ Выделение последних ходов")
    print("   ✓ Информационная панель с подробной статистикой")
    print("   ✓ Поддержка обеих сторон (белые/чёрные)")
    print("   ✓ Разные уровни сложности (0-20)")
    print("   ✓ История ходов и позиций")
    print("   ✓ Оптимизированная производительность")
    print("   ✓ Новые режимы игры: головоломки, на время, адаптивный")
    print()
    
    # Показать статистику
    show_stats()
    
    show_difficulty_guide()
    show_game_modes()
    
    # Инициализация значений по умолчанию
    player_color = 'white'
    level = 5
    theme = 'classic'
    game_mode = 'classic'
    
    # Выбор режима игры
    while True:
        mode_input = input("Выберите режим игры (classic/puzzle/timed/adaptive): ").strip().lower()
        if mode_input in ('classic', 'puzzle', 'timed', 'adaptive'):
            game_mode = mode_input
            break
        else:
            print("❌ Неверный ввод! Введите 'classic', 'puzzle', 'timed' или 'adaptive'")
    
    # Для режима головоломок и уровня
    if game_mode == 'puzzle':
        # Выбор темы
        print("\n🎨 Доступные темы: classic, dark, blue, green, contrast, purple, wood, sunset")
        theme_input = input("Выберите тему (по умолчанию classic): ").strip().lower()
        if theme_input in ('classic', 'dark', 'blue', 'green', 'contrast', 'purple', 'wood', 'sunset'):
            theme = theme_input
        else:
            theme = 'classic'
            
        print(f"\n✅ Режим головоломок запускается с темой: {theme}")
        print(f"\n{'='*70}\n")
        return 'white', 10, theme, 'puzzle'  # Для головоломок используем стандартные значения
    
    # Для классического режима и адаптивного режима требуются все параметры
    if game_mode in ('classic', 'adaptive'):
        # Выбор стороны
        while True:
            side_input = input("Выберите сторону (white/w, black/b): ").strip().lower()
            if side_input in ('white', 'w'):
                player_color = 'white'
                break
            elif side_input in ('black', 'b'):
                player_color = 'black'
                break
            else:
                print("❌ Неверный ввод! Введите 'white' (или 'w') или 'black' (или 'b')")
        
        # Выбор уровня сложности
        while True:
            try:
                level_input = input("\nУровень Stockfish (0-20, рекомендуется 5-10): ").strip()
                if level_input == '':
                    level = 5  # По умолчанию средний уровень
                    break
                level = int(level_input)
                if 0 <= level <= 20:
                    break
                else:
                    print("❌ Уровень должен быть от 0 до 20")
            except ValueError:
                print("❌ Пожалуйста, введите число от 0 до 20")
    
    # Для режима на время используются предопределенные настройки
    elif game_mode == 'timed':
        # Выбор стороны
        while True:
            side_input = input("Выберите сторону (white/w, black/b): ").strip().lower()
            if side_input in ('white', 'w'):
                player_color = 'white'
                break
            elif side_input in ('black', 'b'):
                player_color = 'black'
                break
            else:
                print("❌ Неверный ввод! Введите 'white' (или 'w') или 'black' (или 'b')")
        
        # Для режима на время уровень сложности фиксирован
        level = 10  # Средний уровень для режима на время
    
    # Выбор темы
    print("\n🎨 Доступные темы: classic, dark, blue, green, contrast, purple, wood, sunset")
    theme_input = input("Выберите тему (по умолчанию classic): ").strip().lower()
    if theme_input in ('classic', 'dark', 'blue', 'green', 'contrast', 'purple', 'wood', 'sunset'):
        theme = theme_input
    else:
        theme = 'classic'
    
    # Подтверждение
    print(f"\n✅ Игра начинается:")
    print(f"   Режим: {game_mode}")
    print(f"   Вы: {player_color.upper()}")
    print(f"   ПК: {('BLACK' if player_color == 'white' else 'WHITE')}")
    print(f"   Уровень: {level}/20")
    print(f"   Тема: {theme}")
    print(f"\n{'='*70}\n")
    
    return player_color, level, theme, game_mode