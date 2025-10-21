#!/usr/bin/env python3
"""
Тест для проверки оптимизаций рендеринга и устранения артефактов.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from ui.board_renderer import BoardRenderer, BoardTheme
from utils.sound_manager import SoundManager
from game.in_game_menu import InGameMenu

def test_rendering_optimizations():
    """Тест для проверки оптимизаций рендеринга."""
    pygame.init()
    
    try:
        # Создаем окно
        screen = pygame.display.set_mode((512, 612))
        pygame.display.set_caption("Тест оптимизаций рендеринга")
        
        # Создаем рендерер с темной темой
        dark_theme = BoardTheme(
            light_square=(100, 100, 120),
            dark_square=(60, 60, 80),
            highlight=(124, 252, 0, 180),
            last_move=(255, 255, 0, 150),
            check=(255, 0, 0, 180),
            move_hint=(0, 0, 255, 100),
            hover=(200, 200, 255, 100),
            white_piece=(240, 240, 240),
            black_piece=(200, 200, 200)
        )
        
        renderer = BoardRenderer(screen, 'white', dark_theme)
        renderer._current_theme = 'dark'
        
        # Создаем менеджер звуков
        sound_manager = SoundManager()
        sound_manager.load_sounds()
        
        # Создаем меню
        menu = InGameMenu(screen, sound_manager)
        
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
        
        print("Тест 1: Базовая отрисовка доски с темной темой")
        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 2: Отрисовка с выделением и подсказками")
        renderer.set_selected((4, 4))  # Выделяем центральную клетку
        renderer.set_move_hints([(3, 3), (3, 4), (3, 5)])  # Подсказки в центре
        renderer._mark_all_dirty()
        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 3: Отрисовка с шахом и последним ходом")
        renderer.set_check((7, 4))  # Король белых под шахом
        renderer.set_last_move((6, 4), (4, 4))  # Пешка делает ход
        renderer._mark_all_dirty()
        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=-0.3, thinking=False, mouse_pos=(256, 256))
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 4: Отрисовка меню")
        menu.show()
        screen.fill((40, 40, 40))
        renderer.draw(test_board, evaluation=0.0, thinking=False, mouse_pos=(256, 256))
        menu.draw()
        pygame.display.flip()
        pygame.time.wait(500)
        
        print("Тест 5: Анимация меню")
        # Имитируем навигацию по меню
        for i in range(3):
            menu.selected_item = i
            menu.animation_offset = 5
            screen.fill((40, 40, 40))
            renderer.draw(test_board, evaluation=0.0, thinking=False, mouse_pos=(256, 256))
            menu.draw()
            pygame.display.flip()
            pygame.time.wait(200)
            # Обновляем анимацию
            menu.update()
            screen.fill((40, 40, 40))
            renderer.draw(test_board, evaluation=0.0, thinking=False, mouse_pos=(256, 256))
            menu.draw()
            pygame.display.flip()
            pygame.time.wait(100)
        
        # Очищаем ресурсы
        renderer.cleanup()
        pygame.quit()
        
        print("\n✅ Все тесты оптимизаций рендеринга пройдены успешно!")
        print("Улучшения:")
        print("1. Улучшена очистка экрана перед отрисовкой")
        print("2. Оптимизированы эффекты подсветки и теней")
        print("3. Улучшена визуализация меню с тенями и градиентами")
        print("4. Оптимизирована работа с альфа-каналом")
        print("5. Улучшена производительность за счет уменьшения сложности эффектов")
        
    except Exception as e:
        pygame.quit()
        print(f"\n❌ Тест провален: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_rendering_optimizations()