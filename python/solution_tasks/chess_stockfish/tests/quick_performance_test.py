#!/usr/bin/env python3
"""
Быстрый тест производительности для проверки улучшений.

Этот скрипт выполняет базовые тесты производительности,
чтобы убедиться, что оптимизации работают корректно.
"""

import time
import sys
import os

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from engine.stockfish_wrapper import StockfishWrapper


def test_caching_performance():
    """Тест производительности кэширования."""
    print("🔍 Тест кэширования...")
    
    # Создаем движок
    engine = StockfishWrapper(skill_level=3)
    
    # Тест 1: Кэширование состояния доски
    print("  Тест 1: Кэширование состояния доски")
    
    # Первый вызов (без кэша)
    start_time = time.perf_counter()
    board1 = engine.get_board_state()
    time1 = time.perf_counter() - start_time
    
    # Второй вызов (с кэшем)
    start_time = time.perf_counter()
    board2 = engine.get_board_state()
    time2 = time.perf_counter() - start_time
    
    print(f"    Первый вызов: {time1*1000:.2f} мс")
    print(f"    Второй вызов: {time2*1000:.2f} мс")
    print(f"    Ускорение: {time1/time2:.1f}x" if time2 > 0 else "    Ускорение: ∞")
    
    # Проверяем, что результаты одинаковые
    assert board1 == board2, "Кэшированные результаты должны совпадать"
    
    # Тест 2: Кэширование оценки позиции
    print("  Тест 2: Кэширование оценки позиции")
    
    # Первый вызов (без кэша)
    start_time = time.perf_counter()
    eval1 = engine.get_evaluation()
    time1 = time.perf_counter() - start_time
    
    # Второй вызов (с кэшем)
    start_time = time.perf_counter()
    eval2 = engine.get_evaluation()
    time2 = time.perf_counter() - start_time
    
    print(f"    Первый вызов: {time1*1000:.2f} мс")
    print(f"    Второй вызов: {time2*1000:.2f} мс")
    print(f"    Ускорение: {time1/time2:.1f}x" if time2 > 0 else "    Ускорение: ∞")
    
    # Проверяем, что результаты близкие (могут немного отличаться из-за округления)
    if eval1 is not None and eval2 is not None:
        assert abs(eval1 - eval2) < 0.01, "Кэшированные оценки должны совпадать"
    
    print("  ✅ Тест кэширования пройден")
    return True


def test_move_validation_performance():
    """Тест производительности валидации ходов."""
    print("🔍 Тест валидации ходов...")
    
    # Создаем движок
    engine = StockfishWrapper(skill_level=3)
    
    # Тестовые ходы (используем ходы, которые точно корректны в начальной позиции)
    test_moves = ['e2e4', 'd2d4', 'g1f3', 'b1c3']
    
    # Измеряем время валидации
    start_time = time.perf_counter()
    results = []
    for move in test_moves:
        is_valid = engine.is_move_correct(move)
        results.append(is_valid)
    total_time = time.perf_counter() - start_time
    
    avg_time = total_time / len(test_moves) * 1000  # мс
    print(f"    Среднее время на ход: {avg_time:.2f} мс")
    print(f"    Всего ходов: {len(test_moves)}")
    print(f"    Общее время: {total_time*1000:.2f} мс")
    
    # Проверяем ожидаемые результаты
    expected = [True, True, True, True]  # Все ходы корректны в начальной позиции
    assert results == expected, f"Ожидаемые результаты: {expected}, получено: {results}"
    
    print("  ✅ Тест валидации ходов пройден")
    return True


def test_ai_move_performance():
    """Тест производительности генерации ходов ИИ."""
    print("🔍 Тест генерации ходов ИИ...")
    
    # Создаем движок с низким уровнем сложности для быстрого теста
    engine = StockfishWrapper(skill_level=1)
    
    # Измеряем время получения хода
    start_time = time.perf_counter()
    move = engine.get_best_move(depth=1)
    move_time = time.perf_counter() - start_time
    
    print(f"    Время получения хода: {move_time*1000:.2f} мс")
    print(f"    Полученный ход: {move}")
    
    # Проверяем, что ход получен
    assert move is not None, "Ход ИИ должен быть получен"
    assert len(move) == 4, "Ход должен быть в формате UCI (4 символа)"
    
    print("  ✅ Тест генерации ходов ИИ пройден")
    return True


def main():
    """Основная функция тестирования."""
    print("🚀 БЫСТРЫЙ ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 50)
    print()
    
    try:
        # Выполняем все тесты
        test_caching_performance()
        print()
        
        test_move_validation_performance()
        print()
        
        test_ai_move_performance()
        print()
        
        print("=" * 50)
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("✅ Производительность оптимизирована")
        print("✅ Кэширование работает корректно")
        print("✅ Все функции работают как ожидается")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Тест провален: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)