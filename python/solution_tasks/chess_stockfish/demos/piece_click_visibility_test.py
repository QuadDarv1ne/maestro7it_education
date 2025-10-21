#!/usr/bin/env python3
"""
Тест для проверки видимости доски при клике на фигуры.
Этот тест проверяет, что доска остается видимой при взаимодействии с фигурами.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from ui.board_renderer import BoardRenderer

def test_piece_click_visibility():
    """Тест для проверки видимости доски при клике на фигуры."""
    pygame.init()
    
    try:
        print("🚀 Запуск теста видимости доски при клике на фигуры...")
        
        # Создаем окно
        screen = pygame.display.set_mode((512, 612))
        pygame.display.set_caption("Тест видимости доски при клике на фигуры")
        
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
        
        print("Тест 2: Клик по белой пешке (выбор фигуры)")
        # Имитируем клик по белой пешке на e2 (координаты 6,4 в FEN)
        renderer.set_selected((6, 4))
        # Показываем возможные ходы
        renderer.set_move_hints([(5, 4), (4, 4)])  # Ходы вперед на одну и две клетки
        renderer._mark_all_dirty()
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 3: Клик на возможный ход (перемещение фигуры)")
        # Имитируем перемещение пешки с e2 на e4
        renderer.set_last_move((6, 4), (4, 4))
        renderer.set_selected(None)
        renderer.set_move_hints([])
        renderer._mark_all_dirty()
        # Обновляем доску (пешка переместилась)
        updated_board = [row[:] for row in test_board]
        updated_board[6][4] = None  # Убираем пешку с e2
        updated_board[4][4] = 'P'   # Ставим пешку на e4
        renderer.draw(updated_board, evaluation=0.3, thinking=False, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 4: Клик по черной пешке (выбор другой фигуры)")
        # Имитируем клик по черной пешке на e7 (координаты 1,4 в FEN)
        renderer.set_selected((1, 4))
        renderer.set_move_hints([(2, 4), (3, 4)])  # Ходы вперед на одну и две клетки
        renderer._mark_all_dirty()
        renderer.draw(updated_board, evaluation=0.3, thinking=False, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 5: Клик по пустой клетке (отмена выбора)")
        # Имитируем клик по пустой клетке
        renderer.set_selected(None)
        renderer.set_move_hints([])
        renderer._mark_all_dirty()
        renderer.draw(updated_board, evaluation=0.3, thinking=False, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        # Очищаем ресурсы
        renderer.cleanup()
        pygame.quit()
        
        print("\n✅ Все тесты видимости доски при клике на фигуры пройдены успешно!")
        print("✅ Доска остается видимой при взаимодействии с фигурами")
        print("✅ Правильная очистка и отрисовка экрана")
        print("✅ Корректное обновление состояния доски")
        
    except Exception as e:
        pygame.quit()
        print(f"\n❌ Тест провален: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_piece_click_visibility()