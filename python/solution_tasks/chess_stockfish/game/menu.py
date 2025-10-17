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
    
Возможности:
    - Валидация ввода
    - Подробная справка по уровням сложности
    - Красивое оформление консоли
"""


def show_difficulty_guide():
    """
    Показать справку по уровням сложности Stockfish.
    
    Объясняет, что означают разные уровни сложности.
    """
    print("\n📚 Уровни сложности Stockfish:")
    print("   0-5   : Любитель (начинающий может победить)")
    print("   6-10  : Средний (опытный любитель)")
    print("   11-15 : Сильный (мастер)")
    print("   16-20 : Гроссмейстер (чемпион)")
    print()


def main_menu() -> Tuple[str, int]:
    """
    Главное меню выбора параметров игры.
    
    Выводит приветствие, справку и запрашивает параметры игры.
    
    Возвращает:
        Tuple[str, int]: Кортеж (color, skill_level)
            - color: 'white' или 'black'
            - skill_level: уровень сложности (0-20)
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
    print("   ✓ Оптимизированная производительность\n")
    
    show_difficulty_guide()
    
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
    
    # Подтверждение
    print(f"\n✅ Игра начинается:")
    print(f"   Вы: {player_color.upper()}")
    print(f"   ПК: {('BLACK' if player_color == 'white' else 'WHITE')}")
    print(f"   Уровень: {level}/20")
    print(f"\n{'='*70}\n")
    
    return player_color, level