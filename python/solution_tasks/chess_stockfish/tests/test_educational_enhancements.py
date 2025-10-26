#!/usr/bin/env python3
"""
Тесты для улучшенных образовательных функций chess_stockfish.
"""

import sys
import os
import unittest

# Добавляем путь к модулям игры
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.educational import ChessEducator
from utils.opening_book import OpeningBook

class TestEducationalEnhancements(unittest.TestCase):
    """Тесты для улучшенных образовательных функций."""
    
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.educator = ChessEducator()
        self.opening_book = OpeningBook()
    
    def test_get_random_tip(self):
        """Тест получения случайного стратегического совета."""
        tip = self.educator.get_random_tip()
        self.assertIsInstance(tip, str)
        self.assertGreater(len(tip), 0)
        print(f"💡 Совет: {tip}")
    
    def test_get_piece_hint(self):
        """Тест получения подсказки по фигуре."""
        pieces = ["пешка", "ладья", "конь", "слон", "ферзь", "король"]
        for piece in pieces:
            hint = self.educator.get_piece_hint(piece)
            self.assertIsInstance(hint, str)
            self.assertGreater(len(hint), 0)
            print(f"♟️ {piece.capitalize()}: {hint}")
    
    def test_get_term_explanation(self):
        """Тест получения объяснения термина."""
        terms = ["шах", "мат", "рокировка", "форк", "пин"]
        for term in terms:
            explanation = self.educator.get_term_explanation(term)
            self.assertIsInstance(explanation, str)
            self.assertGreater(len(explanation), 0)
            print(f"📖 {term.capitalize()}: {explanation}")
    
    def test_get_historical_fact(self):
        """Тест получения исторического факта."""
        fact = self.educator.get_historical_fact()
        self.assertIsInstance(fact, str)
        self.assertGreater(len(fact), 0)
        print(f"📚 Факт: {fact}")
    
    def test_get_tactical_motiv(self):
        """Тест получения тактического мотива."""
        motiv = self.educator.get_tactical_motiv()
        self.assertIsInstance(motiv, str)
        self.assertGreater(len(motiv), 0)
        print(f"⚔️ Тактика: {motiv}")
    
    def test_get_random_puzzle(self):
        """Тест получения случайной головоломки."""
        puzzle = self.educator.get_random_puzzle()
        self.assertIsInstance(puzzle, dict)
        self.assertIn("name", puzzle)
        self.assertIn("fen", puzzle)
        self.assertIn("solution", puzzle)
        self.assertIn("description", puzzle)
        print(f"🧩 Головоломка: {puzzle['name']}")
        print(f"   Описание: {puzzle['description']}")
        print(f"   Решение: {puzzle['solution']}")
    
    def test_check_puzzle_solution(self):
        """Тест проверки решения головоломки."""
        # Создаем тестовую головоломку
        test_puzzle = {
            "name": "Тестовая головоломка",
            "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 1",
            "solution": "f3g5",
            "description": "Тестовая головоломка"
        }
        
        # Проверяем правильное решение
        is_correct = self.educator.check_puzzle_solution(test_puzzle, "f3g5")
        self.assertTrue(is_correct)
        
        # Проверяем неправильное решение
        is_correct = self.educator.check_puzzle_solution(test_puzzle, "e2e4")
        self.assertFalse(is_correct)
        
        print("✅ Проверка решения головоломки работает корректно")
    
    def test_get_opening_info(self):
        """Тест получения информации о дебюте."""
        openings = ["Испанская партия", "Сицилианская защита", "Итальянская партия"]
        for opening in openings:
            info = self.opening_book.get_opening_info(opening)
            self.assertIsInstance(info, dict)
            if info:  # Проверяем, что info не None
                self.assertIn("description", info)
                self.assertIn("strategy", info)
                self.assertIn("difficulty", info)
                print(f"🎯 {opening}:")
                print(f"   Описание: {info['description']}")
                print(f"   Стратегия: {info['strategy']}")
                print(f"   Сложность: {info['difficulty']}")
    
    def test_get_educational_tip(self):
        """Тест получения образовательного совета по дебюту."""
        opening_name = "Испанская партия"
        tip = self.opening_book.get_educational_tip(opening_name)
        if tip:
            self.assertIsInstance(tip, str)
            self.assertGreater(len(tip), 0)
            print(f"💡 Совет по {opening_name}: {tip}")
    
    def test_get_opening_lesson(self):
        """Тест получения интерактивного урока по дебюту."""
        # Проверяем существующий урок
        lesson = self.opening_book.get_opening_lesson("Испанская партия")
        if lesson:
            self.assertIsInstance(lesson, dict)
            self.assertIn("title", lesson)
            self.assertIn("content", lesson)
            self.assertIn("key_moves", lesson)
            self.assertIn("practice_position", lesson)
            self.assertIn("objectives", lesson)
            print(f"📘 Урок: {lesson['title']}")
            print(f"   {lesson['content']}")
    
    def test_learning_progress(self):
        """Тест системы прогресса обучения."""
        # Проверяем начальный прогресс
        progress = self.educator.get_learning_progress()
        self.assertIsInstance(progress, dict)
        self.assertIn("tactics", progress)
        self.assertIn("openings", progress)
        self.assertIn("endgames", progress)
        self.assertIn("strategy", progress)
        
        # Симулируем решение головоломки
        initial_tactics = progress["tactics"]
        puzzle = self.educator.get_random_puzzle()
        self.educator.check_puzzle_solution(puzzle, puzzle["solution"])
        new_progress = self.educator.get_learning_progress()
        self.assertEqual(new_progress["tactics"], initial_tactics + 1)
        
        print("📈 Система прогресса обучения работает корректно")
    
    def test_achievements(self):
        """Тест системы достижений."""
        # Проверяем начальные достижения
        achievements = self.educator.get_unlocked_achievements()
        self.assertIsInstance(achievements, list)
        
        # Симулируем изучение дебютов
        self.educator.add_learned_opening("Испанская партия")
        self.educator.add_learned_opening("Сицилианская защита")
        self.educator.add_learned_opening("Итальянская партия")
        self.educator.add_learned_opening("Французская защита")
        self.educator.add_learned_opening("Каро-Каннская защита")
        
        # Симулируем решение головоломок
        for i in range(10):
            puzzle = self.educator.get_random_puzzle()
            self.educator.check_puzzle_solution(puzzle, puzzle["solution"])
        
        # Проверяем разблокированные достижения
        new_achievements = self.educator.get_unlocked_achievements()
        self.assertGreater(len(new_achievements), len(achievements))
        
        print("🏅 Система достижений работает корректно")
        for achievement in new_achievements:
            info = self.educator.get_achievement_info(achievement)
            if info:
                print(f"   {info['name']}: {info['description']}")

def run_tests():
    """Запуск тестов."""
    print("🎓 Тестирование улучшенных образовательных функций")
    print("=" * 60)
    
    # Создаем тестовый набор
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEducationalEnhancements)
    
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Выводим результаты
    print("\n" + "=" * 60)
    print(f"✅ Тестов пройдено: {result.testsRun}")
    print(f"❌ Ошибок: {len(result.errors)}")
    print(f"⚠️  Провалов: {len(result.failures)}")
    
    if result.wasSuccessful():
        print("🎉 Все тесты пройдены успешно!")
    else:
        print("❌ Некоторые тесты провалены.")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)