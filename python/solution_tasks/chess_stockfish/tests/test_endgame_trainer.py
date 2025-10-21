#!/usr/bin/env python3
# ============================================================================
# test_endgame_trainer.py
# ============================================================================

"""
Тестирование функциональности тренажера эндшпилей.
"""

import sys
import os
import unittest

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from utils.endgame_trainer import EndgameTrainer

class TestEndgameTrainer(unittest.TestCase):
    """Тесты для тренажера эндшпилей."""
    
    def setUp(self):
        """Настройка тестов."""
        self.trainer = EndgameTrainer()
    
    def test_get_available_scenarios(self):
        """Тест получения списка доступных сценариев."""
        scenarios = self.trainer.get_available_scenarios()
        self.assertIsNotNone(scenarios)
        self.assertIsInstance(scenarios, list)
        self.assertGreater(len(scenarios), 0)
        
        # Проверяем структуру первого сценария
        first_scenario = scenarios[0]
        self.assertIn("id", first_scenario)
        self.assertIn("name", first_scenario)
        self.assertIn("description", first_scenario)
        self.assertIn("difficulty", first_scenario)
    
    def test_select_scenario(self):
        """Тест выбора сценария."""
        # Тест существующего сценария
        scenario = self.trainer.select_scenario("ферзь_против_пешки")
        self.assertIsNotNone(scenario)
        self.assertIsInstance(scenario, dict)
        if scenario is not None:
            self.assertIn("name", scenario)
            self.assertIn("fen", scenario)
        
        # Проверяем, что сценарий установлен как текущий
        current = self.trainer.get_current_scenario()
        self.assertIsNotNone(current)
        if current is not None:
            self.assertEqual(current["name"], "Ферзь против пешки")
        
        # Тест несуществующего сценария
        scenario = self.trainer.select_scenario("несуществующий_сценарий")
        self.assertIsNone(scenario)
    
    def test_get_scenario_fen(self):
        """Тест получения FEN позиции сценария."""
        # Без выбора сценария
        fen = self.trainer.get_scenario_fen()
        self.assertIsNone(fen)
        
        # С выбором сценария
        self.trainer.select_scenario("ладья_против_пешки")
        fen = self.trainer.get_scenario_fen()
        self.assertIsNotNone(fen)
        self.assertIsInstance(fen, str)
        if fen is not None:
            self.assertGreater(len(fen), 0)
    
    def test_get_random_tip(self):
        """Тест получения случайного совета."""
        # Без выбора сценария
        tip = self.trainer.get_random_tip()
        self.assertIsNone(tip)
        
        # С выбором сценария
        self.trainer.select_scenario("ферзь_против_пешки")
        tip = self.trainer.get_random_tip()
        self.assertIsNotNone(tip)
        self.assertIsInstance(tip, str)
        if tip is not None:
            self.assertGreater(len(tip), 0)
    
    def test_complete_scenario(self):
        """Тест завершения сценария."""
        # Выбираем сценарий
        self.trainer.select_scenario("ферзь_против_пешки")
        
        # Получаем начальную статистику
        initial_stats = self.trainer.get_stats()
        
        # Завершаем сценарий успешно
        self.trainer.complete_scenario(success=True)
        
        # Проверяем обновление статистики
        updated_stats = self.trainer.get_stats()
        self.assertEqual(updated_stats["total_attempts"], initial_stats["total_attempts"] + 1)
        self.assertEqual(updated_stats["successful_attempts"], initial_stats["successful_attempts"] + 1)
        self.assertEqual(updated_stats["scenarios_completed"], initial_stats["scenarios_completed"] + 1)
        
        # Проверяем, что текущий сценарий сброшен
        self.assertIsNone(self.trainer.get_current_scenario())
    
    def test_get_stats(self):
        """Тест получения статистики."""
        stats = self.trainer.get_stats()
        self.assertIsNotNone(stats)
        self.assertIsInstance(stats, dict)
        self.assertIn("scenarios_completed", stats)
        self.assertIn("total_attempts", stats)
        self.assertIn("successful_attempts", stats)
        self.assertIn("time_spent", stats)
    
    def test_get_success_rate(self):
        """Тест получения процента успешных попыток."""
        # Без попыток
        rate = self.trainer.get_success_rate()
        self.assertEqual(rate, 0.0)
        
        # С одним успешным завершением
        self.trainer.select_scenario("ферзь_против_пешки")
        self.trainer.complete_scenario(success=True)
        rate = self.trainer.get_success_rate()
        self.assertEqual(rate, 100.0)
        
        # С одним неуспешным завершением
        self.trainer.select_scenario("ладья_против_пешки")
        self.trainer.complete_scenario(success=False)
        rate = self.trainer.get_success_rate()
        self.assertEqual(rate, 50.0)
    
    def test_get_recommendation(self):
        """Тест получения рекомендации."""
        # Без статистики
        recommendation = self.trainer.get_recommendation()
        self.assertIsNotNone(recommendation)
        self.assertIsInstance(recommendation, str)
        
        # С низкой успешностью
        # Имитируем несколько неуспешных попыток
        for i in range(5):
            self.trainer.select_scenario("ферзь_против_пешки")
            self.trainer.complete_scenario(success=False)
        
        recommendation = self.trainer.get_recommendation()
        self.assertIsNotNone(recommendation)
        
        # С высокой успешностью
        # Имитируем несколько успешных попыток
        for i in range(10):
            self.trainer.select_scenario("ферзь_против_пешки")
            self.trainer.complete_scenario(success=True)
        
        recommendation = self.trainer.get_recommendation()
        self.assertIsNotNone(recommendation)

def run_tests():
    """Запуск всех тестов."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)

if __name__ == "__main__":
    run_tests()