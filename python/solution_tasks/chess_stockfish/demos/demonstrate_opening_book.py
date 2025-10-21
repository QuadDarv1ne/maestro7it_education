#!/usr/bin/env python3
# ============================================================================
# demonstrate_opening_book.py
# ============================================================================

"""
Демонстрация функциональности дебютной книги и её интеграции с образовательной системой.
"""

import sys
import os
import time

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from utils.opening_book import OpeningBook
from utils.educational import ChessEducator

def demonstrate_opening_book():
    """Демонстрация работы дебютной книги."""
    print("=== Демонстрация дебютной книги ===\n")
    
    # Создаем экземпляр дебютной книги
    opening_book = OpeningBook()
    
    # Показываем доступные дебюты
    print("Доступные дебюты:")
    from utils.opening_book import OPENING_BOOK
    for i, (name, info) in enumerate(OPENING_BOOK.items(), 1):
        print(f"{i:2d}. {name} ({info['difficulty']})")
        if i >= 10:  # Показываем только первые 10 для краткости
            print("    ...")
            break
    print()
    
    # Демонстрируем определение дебютов
    print("Определение дебютов по ходам:")
    
    # Испанская партия
    spanish_moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
    print(f"Ходы: {spanish_moves}")
    opening_name = opening_book.get_opening_name(spanish_moves)
    if opening_name:
        info = opening_book.get_opening_info(opening_name)
        print(f"Определен дебют: {opening_name}")
        if info:
            print(f"  Описание: {info['description']}")
            print(f"  Стратегия: {info['strategy']}")
            print(f"  Сложность: {info['difficulty']}")
    print()
    
    # Итальянская партия
    italian_moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"]
    print(f"Ходы: {italian_moves}")
    opening_name = opening_book.get_opening_name(italian_moves)
    if opening_name:
        info = opening_book.get_opening_info(opening_name)
        print(f"Определен дебют: {opening_name}")
        if info:
            print(f"  Описание: {info['description']}")
    print()
    
    # Демонстрируем комментарии к ходам
    print("Комментарии к популярным ходам:")
    sample_moves = ["e2e4", "e7e5", "g1f3", "c7c5"]
    for move in sample_moves:
        comment = opening_book.get_move_comment(move)
        if comment:
            print(f"  {move}: {comment}")
    print()
    
    # Демонстрируем дебютные принципы
    print("Дебютные принципы:")
    for i in range(3):  # Показываем 3 случайных принципа
        principle, explanation = opening_book.get_random_principle()
        print(f"  {principle}")
        print(f"    {explanation}")
        print()

def demonstrate_educational_integration():
    """Демонстрация интеграции дебютной книги с образовательной системой."""
    print("=== Демонстрация интеграции с образовательной системой ===\n")
    
    # Создаем экземпляр образовательной системы
    educator = ChessEducator()
    
    # Добавляем ходы в дебютную книгу
    spanish_moves = ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"]
    for move in spanish_moves:
        educator.opening_book.add_move(move)
    
    # Получаем образовательную обратную связь
    print("Образовательная обратная связь с информацией о дебюте:")
    # Используем время в будущем, чтобы гарантировать показ подсказки
    feedback = educator.get_educational_feedback(4, time.time() + 35)
    if feedback:
        print(f"  {feedback}")
    else:
        # Пробуем другой тип контента
        feedback = educator.get_educational_feedback(3, time.time() + 35)
        if feedback:
            print(f"  {feedback}")
    
    print()
    
    # Сбрасываем последовательность и показываем обычную обратную связь
    educator.opening_book.reset_sequence()
    print("Образовательная обратная связь без информации о дебюте:")
    feedback = educator.get_educational_feedback(4, time.time() + 35)
    if feedback:
        print(f"  {feedback}")
    print()

def demonstrate_suggestions():
    """Демонстрация предложений по дебютам."""
    print("=== Демонстрация предложений по дебютам ===\n")
    
    opening_book = OpeningBook()
    
    print("Предложения по дебютам для разных стадий игры:")
    stages = [(5, "Ранняя стадия"), (15, "Средняя стадия"), (25, "Поздняя стадия")]
    
    for move_count, description in stages:
        suggestion = opening_book.get_opening_suggestion(move_count)
        print(f"  {description} (ход {move_count}): {suggestion}")
    print()

def main():
    """Основная функция демонстрации."""
    print("Демонстрация функциональности дебютной книги\n")
    print("=" * 50)
    
    demonstrate_opening_book()
    demonstrate_educational_integration()
    demonstrate_suggestions()
    
    print("Демонстрация завершена!")

if __name__ == "__main__":
    main()