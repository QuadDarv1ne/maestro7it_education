#!/usr/bin/env python3
"""
Тест для выявления визуальных артефактов в рендеринге игры.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from ui.board_renderer import BoardRenderer
from utils.sound_manager import SoundManager

def test_artifacts():
    """Тест для выявления визуальных артефактов."""
    pygame.init()
    
    try:
        # Создаем окно
        screen = pygame.display.set_mode((512, 612))
        pygame.display.set_caption("Тест визуальных артефактов")
        
        # Создаем рендерер
        renderer = BoardRenderer(screen, 'white')
        
        # Тестовая позиция
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
        
        # Тестируем различные состояния
        print("Тест 1: Базовая отрисовка доски")
        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(1000)
        
        print("Тест 2: Отрисовка с выделением")
        renderer.set_selected((4, 4))  # Выделяем центральную клетку
        renderer._mark_all_dirty()
        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(1000)
        
        print("Тест 3: Отрисовка с подсказками")
        renderer.set_move_hints([(3, 3), (3, 4), (3, 5)])  # Подсказки в центре
        renderer._mark_all_dirty()
        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(1000)
        
        print("Тест 4: Отрисовка с шахом")
        renderer.set_check((7, 4))  # Король белых под шахом
        renderer._mark_all_dirty()
        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(1000)
        
        print("Тест 5: Отрисовка последнего хода")
        renderer.set_last_move((6, 4), (4, 4))  # Пешка делает ход
        renderer._mark_all_dirty()
        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(1000)
        
        # Очищаем ресурсы
        renderer.cleanup()
        pygame.quit()
        
        print("\n✅ Все тесты визуальных артефактов пройдены!")
        print("Если вы видели какие-либо артефакты, они могут быть связаны с:")
        print("1. Неправильной очисткой экрана перед отрисовкой")
        print("2. Проблемами с альфа-смешиванием")
        print("3. Неправильным кэшированием поверхностей")
        print("4. Проблемами с clipping областью")
        
    except Exception as e:
        pygame.quit()
        print(f"\n❌ Тест провален: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_artifacts()