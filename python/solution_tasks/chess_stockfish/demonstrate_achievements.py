#!/usr/bin/env python3
# ============================================================================
# demonstrate_achievements.py
# ============================================================================

"""
Демонстрация функциональности системы достижений.
"""

import sys
import os
import tempfile

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from utils.achievements import AchievementSystem

def demonstrate_achievement_system():
    """Демонстрация работы системы достижений."""
    print("=== Демонстрация системы достижений ===\n")
    
    # Создаем временную систему достижений
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    temp_file.close()
    
    try:
        # Создаем экземпляр системы достижений
        achievement_system = AchievementSystem(temp_file.name)
        
        # Показываем все достижения
        print("Все достижения:")
        all_achievements = achievement_system.get_all_achievements()
        categories = {}
        
        # Группируем достижения по категориям
        for achievement_id, info in all_achievements.items():
            category = info["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append((achievement_id, info))
        
        # Показываем достижения по категориям
        for category, achievements in categories.items():
            print(f"\nКатегория: {category.capitalize()}")
            for i, (achievement_id, info) in enumerate(achievements[:3], 1):  # Показываем первые 3
                print(f"  {i}. {info['icon']} {info['name']} ({info['points']} очков)")
                print(f"     {info['description']}")
            if len(achievements) > 3:
                print(f"     ... и еще {len(achievements) - 3} достижений")
        print()
        
        # Показываем уровни
        print("Система уровней:")
        from utils.achievements import LEVELS
        for level_num, level_info in LEVELS.items():
            print(f"  {level_num}. {level_info['icon']} {level_info['name']} (от {level_info['points_required']} очков)")
        print()
        
        # Демонстрируем получение достижений
        print("Получение достижений:")
        
        # Получаем первое образовательное достижение
        achievement_system.add_educational_hint()
        new_achievements = achievement_system.check_achievements()
        print(f"  Получено образовательных подсказок: {achievement_system.stats['educational_hints']}")
        
        # Проверяем новые достижения
        new_achievements = achievement_system.get_new_achievements()
        if new_achievements:
            print("  Новые достижения:")
            for achievement in new_achievements:
                if "info" in achievement:
                    info = achievement["info"]
                    print(f"    {info['icon']} {info['name']} ({info['points']} очков)")
        else:
            print("  Новых достижений нет")
        achievement_system.clear_new_achievements()
        print()
        
        # Демонстрируем систему уровней
        print("Система уровней:")
        print(f"  Текущий уровень: {achievement_system.level}")
        level_info = achievement_system.get_level_info()
        if level_info:
            print(f"  Звание: {level_info['icon']} {level_info['name']}")
        
        # Показываем прогресс до следующего уровня
        progress = achievement_system.get_progress_to_next_level()
        current_points, points_needed, percent = progress
        if points_needed > 0:
            print(f"  Прогресс до следующего уровня: {current_points}/{points_needed} ({percent}%)")
        else:
            print("  Максимальный уровень достигнут!")
        print()
        
        # Демонстрируем статистику
        print("Статистика:")
        stats = achievement_system.stats
        print(f"  Образовательных подсказок: {stats['educational_hints']}")
        print(f"  Изучено дебютов: {len(stats['openings_learned'])}")
        print(f"  Завершено эндшпилей: {stats['endgames_completed']}")
        print(f"  Сыграно партий: {stats['games_played']}")
        print(f"  Выиграно партий: {stats['games_won']}")
        print(f"  Поставлено матов: {stats['checkmates']}")
        print(f"  Всего очков: {achievement_system.total_points}")
        print()
        
        # Получаем список полученных достижений
        print("Полученные достижения:")
        unlocked = achievement_system.get_unlocked_achievements()
        if unlocked:
            for achievement in unlocked[:5]:  # Показываем первые 5
                info = achievement["info"]
                print(f"  {info['icon']} {info['name']} ({info['points']} очков)")
            if len(unlocked) > 5:
                print(f"  ... и еще {len(unlocked) - 5} достижений")
        else:
            print("  Пока нет полученных достижений")
        print()
        
        # Получаем список неполученных достижений
        print("Неполученные достижения:")
        locked = achievement_system.get_locked_achievements()
        if locked:
            for achievement in locked[:5]:  # Показываем первые 5
                info = achievement["info"]
                print(f"  {info['icon']} {info['name']} ({info['points']} очков)")
            if len(locked) > 5:
                print(f"  ... и еще {len(locked) - 5} достижений")
        else:
            print("  Все достижения получены!")
        print()
        
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

def demonstrate_achievement_progression():
    """Демонстрация прогрессии достижений."""
    print("=== Демонстрация прогрессии достижений ===\n")
    
    # Создаем временную систему достижений
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    temp_file.close()
    
    try:
        achievement_system = AchievementSystem(temp_file.name)
        
        # Имитируем прогресс игрока
        print("Имитация прогресса игрока:")
        
        # Добавляем различные статистики
        for i in range(5):
            achievement_system.add_educational_hint()
            achievement_system.add_opening_learned(f"Дебют {i+1}")
        
        for i in range(3):
            achievement_system.add_endgame_completed()
        
        for i in range(2):
            achievement_system.add_game_played()
            achievement_system.add_game_won()
        
        achievement_system.add_checkmate()
        achievement_system.add_moves(100)
        achievement_system.add_captures(10)
        achievement_system.add_play_time(7200)  # 2 часа
        
        # Проверяем достижения
        new_achievements = achievement_system.check_achievements()
        
        print(f"  Образовательных подсказок: {achievement_system.stats['educational_hints']}")
        print(f"  Изучено дебютов: {len(achievement_system.stats['openings_learned'])}")
        print(f"  Завершено эндшпилей: {achievement_system.stats['endgames_completed']}")
        print(f"  Сыграно партий: {achievement_system.stats['games_played']}")
        print(f"  Выиграно партий: {achievement_system.stats['games_won']}")
        print(f"  Сделано ходов: {achievement_system.stats['moves_made']}")
        print(f"  Время игры: {achievement_system.stats['time_played']} секунд")
        print(f"  Всего очков: {achievement_system.total_points}")
        print()
        
        # Проверяем уровень
        level_info = achievement_system.get_level_info()
        if level_info:
            print(f"  Текущий уровень: {level_info['icon']} {level_info['name']}")
        
        # Показываем новые достижения
        new_achievements = achievement_system.get_new_achievements()
        if new_achievements:
            print("  Полученные достижения:")
            for achievement in new_achievements:
                if "info" in achievement:
                    info = achievement["info"]
                    print(f"    {info['icon']} {info['name']}")
        achievement_system.clear_new_achievements()
        print()
        
        # Показываем прогресс
        progress = achievement_system.get_progress_to_next_level()
        current_points, points_needed, percent = progress
        if points_needed > 0:
            print(f"  Прогресс до следующего уровня: {percent}%")
        print()
        
    finally:
        # Удаляем временный файл
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)

def main():
    """Основная функция демонстрации."""
    print("Демонстрация функциональности системы достижений\n")
    print("=" * 50)
    
    demonstrate_achievement_system()
    demonstrate_achievement_progression()
    
    print("Демонстрация завершена!")

if __name__ == "__main__":
    main()