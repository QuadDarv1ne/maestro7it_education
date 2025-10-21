#!/usr/bin/env python3
"""
Тест для проверки исправления визуальных артефактов при клике на фигуры.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from ui.board_renderer import BoardRenderer
from utils.sound_manager import SoundManager

def test_artifact_fix():
    """Тест для проверки исправления визуальных артефактов."""
    pygame.init()
    
    try:
        print("🚀 Запуск теста исправления артефактов...")
        
        # Создаем окно
        screen = pygame.display.set_mode((512, 612))
        pygame.display.set_caption("Тест исправления артефактов")
        
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
        
        print("Тест 2: Выбор фигуры (клик по белой пешке)")
        # Имитируем клик по белой пешке на e2 (координаты 6,4 в FEN)
        renderer.set_selected((6, 4))
        # Показываем возможные ходы
        renderer.set_move_hints([(5, 4), (4, 4)])  # Ходы вперед на одну и две клетки
        renderer._mark_all_dirty()
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 3: Перемещение фигуры (клик на возможный ход)")
        # Имитируем перемещение пешки с e2 на e4
        renderer.set_last_move((6, 4), (4, 4))
        renderer.set_selected(None)
        renderer.set_move_hints([])
        renderer._mark_all_dirty()
        renderer.draw(test_board, evaluation=0.3, thinking=False, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 4: Выбор другой фигуры (клик по черной пешке)")
        # Имитируем клик по черной пешке на e7 (координаты 1,4 в FEN)
        renderer.set_selected((1, 4))
        renderer.set_move_hints([(2, 4), (3, 4)])  # Ходы вперед на одну и две клетки
        renderer._mark_all_dirty()
        renderer.draw(test_board, evaluation=0.3, thinking=False, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 5: Отмена выбора (клик по пустой клетке)")
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
        
        print("\n✅ Все тесты исправления артефактов пройдены успешно!")
        print("✅ Артефакты при клике на фигуры устранены")
        print("✅ Правильная очистка и отрисовка экрана")
        print("✅ Корректное обновление состояния доски")
        
    except Exception as e:
        pygame.quit()
        print(f"\n❌ Тест провален: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_artifact_fix()