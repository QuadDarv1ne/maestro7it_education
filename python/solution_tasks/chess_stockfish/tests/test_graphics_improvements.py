#!/usr/bin/env python3
# ============================================================================
# test_graphics_improvements.py
# ============================================================================

"""
Тестирование улучшений графики шахматной доски.
"""

import pygame
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from ui.board_renderer import BoardRenderer, BOARD_SIZE

def test_graphics_improvements():
    """Тест улучшений графики."""
    print("Запуск теста графических улучшений...")
    
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
    pygame.display.set_caption("Тест графических улучшений")
    
    # Создание рендерера
    renderer = BoardRenderer(screen, 'white')
    
    # Тестовая позиция с различными фигурами
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
    
    # Установка различных эффектов для тестирования
    renderer.set_selected((7, 4))  # Выбран король
    renderer.set_last_move(((6, 4), (4, 4)))  # Последний ход
    renderer.set_check((0, 4))  # Король под шахом
    renderer.set_move_hints([(5, 3), (5, 4), (5, 5)])  # Подсказки ходов
    
    clock = pygame.time.Clock()
    running = True
    frame_count = 0
    
    print("Отображается тестовая доска с улучшенной графикой.")
    print("Нажмите ESC для выхода.")
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Обновление hover позиции
        mouse_pos = pygame.mouse.get_pos()
        
        # Очистка экрана
        screen.fill((40, 40, 40))
        
        # Отрисовка доски
        renderer.draw(test_board, evaluation=0.5, thinking=True, mouse_pos=mouse_pos)
        
        # Дополнительная отрисовка информации
        font = pygame.font.SysFont('Arial', 16)
        info_text = font.render("Тест графических улучшений", True, (200, 200, 200))
        screen.blit(info_text, (10, BOARD_SIZE + 60))
        
        info_text2 = font.render("ESC - выход", True, (200, 200, 200))
        screen.blit(info_text2, (10, BOARD_SIZE + 80))
        
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1
        
        # Очистка временных поверхностей каждые 3600 кадров (1 минута при 60 FPS)
        if frame_count % 3600 == 0:
            renderer.clear_temp_surfaces()
    
    # Очистка ресурсов
    renderer.cleanup()
    pygame.quit()
    print("Тест завершен.")

if __name__ == "__main__":
    test_graphics_improvements()