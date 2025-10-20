#!/usr/bin/env python3
# ============================================================================
# test_achievements.py
# ============================================================================

"""
Тестирование функциональности системы достижений.
"""

import sys
import os
import unittest
import tempfile
import json

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from utils.achievements import AchievementSystem

class TestAchievementSystem(unittest.TestCase):
    """Тесты для системы достижений."""
    
    def setUp(self):
        """Настройка тестов."""
        # Создаем временный файл для сохранения достижений
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.achievement_system = AchievementSystem(self.temp_file.name)
    
    def tearDown(self):
        """Очистка после тестов."""
        # Удаляем временный файл
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_get_achievement_info(self):
        """Тест получения информации о достижении."""
        # Тест существующего достижения
        info = self.achievement_system.get_achievement_info("first_lesson")
        self.assertIsNotNone(info)
        self.assertIsInstance(info, dict)
        self.assertIn("name", info)
        self.assertIn("description", info)
        self.assertIn("category", info)
        self.assertIn("points", info)
        self.assertIn("icon", info)
        
        # Тест несуществующего достижения
        info = self.achievement_system.get_achievement_info("nonexistent")
        self.assertIsNone(info)
    
    def test_get_all_achievements(self):
        """Тест получения всех достижений."""
        achievements = self.achievement_system.get_all_achievements()
        self.assertIsNotNone(achievements)
        self.assertIsInstance(achievements, dict)
        self.assertGreater(len(achievements), 0)
    
    def test_get_unlocked_and_locked_achievements(self):
        """Тест получения полученных и неполученных достижений."""
        # Изначально нет полученных достижений
        unlocked = self.achievement_system.get_unlocked_achievements()
        self.assertIsInstance(unlocked, list)
        self.assertEqual(len(unlocked), 0)
        
        locked = self.achievement_system.get_locked_achievements()
        self.assertIsInstance(locked, list)
        self.assertGreater(len(locked), 0)
    
    def test_educational_achievements(self):
        """Тест образовательных достижений."""
        # Проверяем достижение "first_lesson"
        self.achievement_system.add_educational_hint()
        new_achievements = self.achievement_system.check_achievements()
        self.assertIn("first_lesson", new_achievements)
        
        # Проверяем, что достижение теперь в списке полученных
        unlocked = self.achievement_system.get_unlocked_achievements()
        unlocked_ids = [a["id"] for a in unlocked]
        self.assertIn("first_lesson", unlocked_ids)
        
        # Проверяем, что достижение больше не в списке неполученных
        locked = self.achievement_system.get_locked_achievements()
        locked_ids = [a["id"] for a in locked]
        self.assertNotIn("first_lesson", locked_ids)
    
    def test_level_system(self):
        """Тест системы уровней."""
        # Изначально уровень 1
        self.assertEqual(self.achievement_system.level, 1)
        
        # Получаем достижение с 10 очками
        self.achievement_system.achievements["test_achievement"] = 1
        self.achievement_system.unlocked_achievements.add("test_achievement")
        self.achievement_system.total_points = 10
        self.achievement_system.level = self.achievement_system.calculate_level()
        
        # Уровень должен остаться 1 (нужно 100 для уровня 2)
        self.assertEqual(self.achievement_system.level, 1)
        
        # Получаем больше очков
        self.achievement_system.total_points = 150
        self.achievement_system.level = self.achievement_system.calculate_level()
        
        # Проверяем информацию об уровне
        level_info = self.achievement_system.get_level_info(2)
        self.assertIsNotNone(level_info)
        self.assertIn("name", level_info)
        self.assertIn("points_required", level_info)
        self.assertIn("icon", level_info)
    
    def test_progress_to_next_level(self):
        """Тест прогресса до следующего уровня."""
        # Устанавливаем очки между уровнями
        self.achievement_system.total_points = 150  # Между 100 (уровень 2) и 300 (уровень 3)
        self.achievement_system.level = self.achievement_system.calculate_level()
        
        progress = self.achievement_system.get_progress_to_next_level()
        self.assertIsInstance(progress, tuple)
        self.assertEqual(len(progress), 3)
        
        current_points, points_needed, percent = progress
        self.assertIsInstance(current_points, int)
        self.assertIsInstance(points_needed, int)
        self.assertIsInstance(percent, int)
        self.assertGreaterEqual(percent, 0)
        self.assertLessEqual(percent, 100)
    
    def test_new_achievements(self):
        """Тест недавно полученных достижений."""
        # Изначально нет новых достижений
        new_achievements = self.achievement_system.get_new_achievements()
        self.assertIsInstance(new_achievements, list)
        self.assertEqual(len(new_achievements), 0)
        
        # Получаем достижение
        self.achievement_system.add_educational_hint()
        self.achievement_system.check_achievements()
        
        # Проверяем новые достижения
        new_achievements = self.achievement_system.get_new_achievements()
        self.assertIsInstance(new_achievements, list)
        self.assertGreater(len(new_achievements), 0)
        
        # Очищаем список новых достижений
        self.achievement_system.clear_new_achievements()
        new_achievements = self.achievement_system.get_new_achievements()
        self.assertEqual(len(new_achievements), 0)
    
    def test_statistics_updates(self):
        """Тест обновления статистики."""
        # Проверяем начальную статистику
        initial_stats = self.achievement_system.stats.copy()
        
        # Обновляем различные статистики
        self.achievement_system.add_educational_hint()
        self.achievement_system.add_opening_learned("Испанская партия")
        self.achievement_system.add_endgame_completed()
        self.achievement_system.add_game_played()
        self.achievement_system.add_game_won()
        self.achievement_system.add_checkmate()
        self.achievement_system.add_draw()
        self.achievement_system.add_moves(5)
        self.achievement_system.add_captures(3)
        self.achievement_system.add_play_time(3600)  # 1 час
        self.achievement_system.add_perfect_game()
        self.achievement_system.add_comeback_win()
        self.achievement_system.add_short_game()
        self.achievement_system.add_long_game()
        
        # Проверяем, что статистика обновилась
        self.assertGreater(self.achievement_system.stats["educational_hints"], 
                          initial_stats["educational_hints"])
        self.assertGreater(len(self.achievement_system.stats["openings_learned"]), 
                          len(initial_stats["openings_learned"]))
        self.assertGreater(self.achievement_system.stats["endgames_completed"], 
                          initial_stats["endgames_completed"])
    
    def test_save_and_load_achievements(self):
        """Тест сохранения и загрузки достижений."""
        # Получаем достижение
        self.achievement_system.add_educational_hint()
        self.achievement_system.check_achievements()
        
        # Сохраняем достижения
        self.achievement_system.save_achievements()
        
        # Создаем новую систему достижений с тем же файлом
        new_system = AchievementSystem(self.temp_file.name)
        
        # Проверяем, что достижения загрузились
        self.assertGreater(len(new_system.unlocked_achievements), 0)
        self.assertGreater(new_system.total_points, 0)
        
        # Проверяем конкретное достижение
        self.assertIn("first_lesson", new_system.unlocked_achievements)

def run_tests():
    """Запуск всех тестов."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)

if __name__ == "__main__":
    run_tests()