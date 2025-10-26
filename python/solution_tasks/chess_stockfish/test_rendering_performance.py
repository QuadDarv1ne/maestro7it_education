#!/usr/bin/env python3
"""
Тест производительности рендеринга для оптимизации FPS.
"""

import time
import sys
import os
import pygame

# Добавляем путь к проекту
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game.chess_game import ChessGame
from engine.stockfish_wrapper import StockfishWrapper


def test_rendering_performance():
    """Тест производительности рендеринга."""
    print("Тест производительности рендеринга")
    print("=" * 40)
    
    # Создаем игру
    game = ChessGame(player_color='white', skill_level=5)
    
    # Получаем состояние доски
    board_state = game.get_board_state()
    
    # Тест 1: Измеряем время отрисовки доски
    print("Тест 1: Время отрисовки доски")
    start_time = time.perf_counter()
    
    for i in range(100):
        # Имитируем отрисовку доски
        game.renderer.draw(
            board_state,
            evaluation=0.5,
            thinking=False,
            mouse_pos=(256, 256),
            move_count=10,
            capture_count=(3, 2),
            check_count=1
        )
    
    render_time = time.perf_counter() - start_time
    avg_render_time = render_time / 100 * 1000  # мс
    
    print(f"  Общее время: {render_time:.4f} сек")
    print(f"  Среднее время на кадр: {avg_render_time:.2f} мс")
    print(f"  Приблизительный FPS: {1000/avg_render_time:.1f}")
    
    # Тест 2: Измеряем время обновления состояния доски
    print("\nТест 2: Время обновления состояния доски")
    start_time = time.perf_counter()
    
    for i in range(1000):
        board = game.get_board_state()
    
    update_time = time.perf_counter() - start_time
    avg_update_time = update_time / 1000 * 1000  # мс
    
    print(f"  Общее время: {update_time:.4f} сек")
    print(f"  Среднее время на обновление: {avg_update_time:.4f} мс")
    
    # Тест 3: Измеряем время кэширования
    print("\nТест 3: Эффективность кэширования")
    start_time = time.perf_counter()
    
    # Первый вызов (без кэша)
    game.board_state_cache = None
    board1 = game.get_board_state()
    first_call_time = time.perf_counter() - start_time
    
    # Второй вызов (с кэшем)
    start_time = time.perf_counter()
    board2 = game.get_board_state()
    second_call_time = time.perf_counter() - start_time
    
    print(f"  Первый вызов (без кэша): {first_call_time*1000:.4f} мс")
    print(f"  Второй вызов (с кэшем): {second_call_time*1000:.4f} мс")
    print(f"  Ускорение: {first_call_time/second_call_time:.2f}x")
    
    # Очистка
    game.renderer.cleanup()
    
    return {
        'avg_render_time_ms': avg_render_time,
        'fps': 1000/avg_render_time,
        'avg_update_time_ms': avg_update_time,
        'caching_speedup': first_call_time/second_call_time
    }


def main():
    """Основная функция тестирования."""
    print("🚀 ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ РЕНДЕРИНГА")
    print("=" * 50)
    print()
    
    try:
        pygame.init()
        
        results = test_rendering_performance()
        
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТЫ ТЕСТА:")
        print("=" * 50)
        print(f"Среднее время рендеринга: {results['avg_render_time_ms']:.2f} мс")
        print(f"Приблизительный FPS: {results['fps']:.1f}")
        print(f"Среднее время обновления: {results['avg_update_time_ms']:.4f} мс")
        print(f"Ускорение кэширования: {results['caching_speedup']:.2f}x")
        
        # Оценка производительности
        if results['fps'] >= 60:
            print("✅ Отличная производительность рендеринга")
        elif results['fps'] >= 30:
            print("⚠️  Удовлетворительная производительность рендеринга")
        else:
            print("❌ Низкая производительность рендеринга")
            
        if results['caching_speedup'] >= 2:
            print("✅ Эффективное кэширование")
        else:
            print("⚠️  Кэширование может быть улучшено")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()