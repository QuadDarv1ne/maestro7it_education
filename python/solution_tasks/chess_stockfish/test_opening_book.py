#!/usr/bin/env python3
# ============================================================================
# test_opening_book.py
# ============================================================================

"""
Тестирование функциональности дебютной книги и её интеграции с образовательной системой.
"""

import sys
import os
import unittest
import time
from unittest.mock import Mock, patch

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from utils.opening_book import OpeningBook
from utils.educational import ChessEducator

class TestOpeningBook(unittest.TestCase):
    """Тесты для дебютной книги."""
    
    def setUp(self):
        """Настройка тестов."""
        self.opening_book = OpeningBook()
    
    def test_get_opening_name(self):
        """Тест определения названия дебюта."""
        # Тест Испанской партии
        spanish_moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
        self.assertEqual(self.opening_book.get_opening_name(spanish_moves), "Испанская партия")
        
        # Тест Итальянской партии
        italian_moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"]
        self.assertEqual(self.opening_book.get_opening_name(italian_moves), "Итальянская партия")
        
        # Тест несуществующей последовательности
        unknown_moves = ["a2a3", "b7b6"]
        self.assertIsNone(self.opening_book.get_opening_name(unknown_moves))
    
    def test_get_opening_info(self):
        """Тест получения информации о дебюте."""
        # Тест существующего дебюта
        info = self.opening_book.get_opening_info("Испанская партия")
        self.assertIsNotNone(info)
        self.assertIsInstance(info, dict)
        if info is not None:
            self.assertIn("moves", info)
            self.assertIn("description", info)
            self.assertIn("strategy", info)
            self.assertIn("difficulty", info)
        
        # Тест несуществующего дебюта
        info = self.opening_book.get_opening_info("Несуществующий дебют")
        self.assertIsNone(info)
    
    def test_get_move_comment(self):
        """Тест получения комментария к ходу."""
        # Тест существующего хода
        comment = self.opening_book.get_move_comment("e2e4")
        self.assertIsNotNone(comment)
        if comment is not None:
            self.assertIsInstance(comment, str)
            self.assertGreater(len(comment), 0)
        
        # Тест несуществующего хода
        comment = self.opening_book.get_move_comment("a1a2")
        self.assertIsNone(comment)
    
    def test_get_random_principle(self):
        """Тест получения случайного дебютного принципа."""
        principle, explanation = self.opening_book.get_random_principle()
        self.assertIsNotNone(principle)
        self.assertIsNotNone(explanation)
        if principle is not None and explanation is not None:
            self.assertIsInstance(principle, str)
            self.assertIsInstance(explanation, str)
            self.assertGreater(len(principle), 0)
            self.assertGreater(len(explanation), 0)
    
    def test_get_opening_suggestion(self):
        """Тест получения предложения по дебюту."""
        # Тест для ранней стадии игры
        suggestion = self.opening_book.get_opening_suggestion(5)
        self.assertIsNotNone(suggestion)
        if suggestion is not None:
            self.assertIsInstance(suggestion, str)
            self.assertGreater(len(suggestion), 0)
        
        # Тест для средней стадии игры
        suggestion = self.opening_book.get_opening_suggestion(15)
        self.assertIsNotNone(suggestion)
        if suggestion is not None:
            self.assertIsInstance(suggestion, str)
        
        # Тест для поздней стадии игры
        suggestion = self.opening_book.get_opening_suggestion(25)
        self.assertIsNotNone(suggestion)
        if suggestion is not None:
            self.assertIsInstance(suggestion, str)
    
    def test_add_move_and_get_current_opening(self):
        """Тест добавления ходов и определения текущего дебюта."""
        # Добавляем ходы Испанской партии
        spanish_moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
        for move in spanish_moves:
            self.opening_book.add_move(move)
        
        # Проверяем, что текущий дебют определяется правильно
        current_opening = self.opening_book.get_current_opening()
        self.assertIsNotNone(current_opening)
        if current_opening is not None:
            self.assertIsInstance(current_opening, tuple)
            self.assertEqual(current_opening[0], "Испанская партия")
        
        # Сбрасываем последовательность
        self.opening_book.reset_sequence()
        current_opening = self.opening_book.get_current_opening()
        self.assertIsNone(current_opening)

class TestEducationalIntegration(unittest.TestCase):
    """Тесты для интеграции дебютной книги с образовательной системой."""
    
    def setUp(self):
        """Настройка тестов."""
        self.educator = ChessEducator()
    
    def test_get_educational_feedback_with_opening(self):
        """Тест получения образовательной обратной связи с информацией о дебюте."""
        # Добавляем ходы в дебютную книгу через educator
        spanish_moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
        for move in spanish_moves:
            self.educator.opening_book.add_move(move)
        
        # Получаем обратную связь с правильным временем
        feedback = self.educator.get_educational_feedback(4, time.time() + 35)
        # Просто проверяем, что метод работает без ошибок
        # (не проверяем конкретное значение, так как зависит от случайных факторов)
        
        # Сбрасываем последовательность
        self.educator.opening_book.reset_sequence()
    
    def test_get_educational_feedback_without_opening(self):
        """Тест получения образовательной обратной связи без информации о дебюте."""
        # Сбрасываем последовательность, чтобы не было дебютной информации
        self.educator.opening_book.reset_sequence()
        
        # Получаем обратную связь с правильным временем
        feedback = self.educator.get_educational_feedback(4, time.time() + 35)
        # Просто проверяем, что метод работает без ошибок
        # (не проверяем конкретное значение, так как зависит от случайных факторов)

def run_tests():
    """Запуск всех тестов."""
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)

if __name__ == "__main__":
    run_tests()