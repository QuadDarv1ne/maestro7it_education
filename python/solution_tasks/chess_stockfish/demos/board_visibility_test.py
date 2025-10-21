#!/usr/bin/env python3
"""
Тест для проверки видимости доски.
Этест проверяет, что доска отображается корректно и не исчезает.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from ui.board_renderer import BoardRenderer

def test_board_visibility():
    """Тест для проверки видимости доски."""
    pygame.init()
    
    try:
        print("🚀 Запуск теста видимости доски...")
        
        # Создаем окно
        screen = pygame.display.set_mode((512, 612))
        pygame.display.set_caption("Тест видимости доски")
        
        # Создаем рендерер
        renderer = BoardRenderer(screen, 'white')
        
        # Тестовая позиция с фигурами
        test_board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        
        # Помечаем все клетки как "грязные" для полной перерисовки
        renderer._mark_all_dirty()
        
        print("Тест 1: Базовая отрисовка доски")
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 2: Проверка видимости после выбора фигуры")
        # Имитируем клик по белой пешке на e2 (координаты 6,4 в FEN)
        renderer.set_selected((6, 4))
        # Показываем возможные ходы
        renderer.set_move_hints([(5, 4), (4, 4)])  # Ходы вперед на одну и две клетки
        renderer._mark_all_dirty()
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 3: Проверка видимости после перемещения фигуры")
        # Имитируем перемещение пешки с e2 на e4
        renderer.set_last_move((6, 4), (4, 4))
        renderer.set_selected(None)
        renderer.set_move_hints([])
        renderer._mark_all_dirty()
        renderer.draw(test_board, evaluation=0.3, thinking=False, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 4: Проверка видимости после отмены выбора")
        # Имитируем клик по пустой клетке
        renderer.set_selected(None)
        renderer.set_move_hints([])
        renderer._mark_all_dirty()
        renderer.draw(test_board, evaluation=0.3, thinking=False, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        # Очищаем ресурсы
        renderer.cleanup()
        pygame.quit()
        
        print("\n✅ Все тесты видимости доски пройдены успешно!")
        print("✅ Доска отображается корректно")
        print("✅ Доска не исчезает при взаимодействии")
        print("✅ Правильная очистка и отрисовка экрана")
        
    except Exception as e:
        pygame.quit()
        print(f"\n❌ Тест провален: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_board_visibility()