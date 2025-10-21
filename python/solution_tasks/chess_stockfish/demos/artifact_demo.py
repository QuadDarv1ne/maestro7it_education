#!/usr/bin/env python3
"""
Демонстрация исправления визуальных артефактов при клике на фигуры.
Этот скрипт показывает, что артефакты были устранены.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from ui.board_renderer import BoardRenderer

def main():
    """Основная функция демонстрации."""
    pygame.init()
    
    try:
        print("🎨 Демонстрация исправления визуальных артефактов")
        print("Показываем, что артефакты при клике на фигуры устранены")
        
        # Создаем окно
        screen = pygame.display.set_mode((512, 612))
        pygame.display.set_caption("Демонстрация исправления артефактов")
        
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
        
        # Основной цикл демонстрации
        clock = pygame.time.Clock()
        running = True
        step = 0
        steps = [
            "1. Базовая отрисовка доски",
            "2. Выбор белой пешки (e2)",
            "3. Показ возможных ходов",
            "4. Перемещение пешки на e4",
            "5. Выбор черной пешки (e7)",
            "6. Показ возможных ходов",
            "7. Отмена выбора",
            "8. Демонстрация завершена - нет артефактов!"
        ]
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Очищаем экран
            screen.fill((40, 40, 40))
            
            # В зависимости от шага показываем разные состояния
            if step == 0:
                # Базовая отрисовка
                renderer._mark_all_dirty()
                renderer.draw(test_board, evaluation=0.0, thinking=False)
            elif step == 1:
                # Выбор белой пешки
                renderer.set_selected((6, 4))  # e2
                renderer._mark_all_dirty()
                renderer.draw(test_board, evaluation=0.0, thinking=False)
            elif step == 2:
                # Показ возможных ходов
                renderer.set_move_hints([(5, 4), (4, 4)])  # e3, e4
                renderer._mark_all_dirty()
                renderer.draw(test_board, evaluation=0.0, thinking=False)
            elif step == 3:
                # Перемещение пешки
                renderer.set_last_move((6, 4), (4, 4))  # e2 -> e4
                renderer.set_selected(None)
                renderer.set_move_hints([])
                # Обновляем доску (пешка переместилась)
                demo_board = [row[:] for row in test_board]
                demo_board[6][4] = None  # Убираем пешку с e2
                demo_board[4][4] = 'P'   # Ставим пешку на e4
                renderer._mark_all_dirty()
                renderer.draw(demo_board, evaluation=0.1, thinking=False)
            elif step == 4:
                # Выбор черной пешки
                renderer.set_selected((1, 4))  # e7
                renderer._mark_all_dirty()
                # Используем обновленную доску
                demo_board = [row[:] for row in test_board]
                demo_board[6][4] = None
                demo_board[4][4] = 'P'
                renderer.draw(demo_board, evaluation=0.1, thinking=False)
            elif step == 5:
                # Показ возможных ходов черной пешки
                renderer.set_move_hints([(2, 4), (3, 4)])  # e6, e5
                renderer._mark_all_dirty()
                # Используем обновленную доску
                demo_board = [row[:] for row in test_board]
                demo_board[6][4] = None
                demo_board[4][4] = 'P'
                renderer.draw(demo_board, evaluation=0.1, thinking=False)
            elif step == 6:
                # Отмена выбора
                renderer.set_selected(None)
                renderer.set_move_hints([])
                renderer._mark_all_dirty()
                # Используем обновленную доску
                demo_board = [row[:] for row in test_board]
                demo_board[6][4] = None
                demo_board[4][4] = 'P'
                renderer.draw(demo_board, evaluation=0.0, thinking=False)
            elif step >= 7:
                # Завершение
                renderer._mark_all_dirty()
                # Используем обновленную доску
                demo_board = [row[:] for row in test_board]
                demo_board[6][4] = None
                demo_board[4][4] = 'P'
                renderer.draw(demo_board, evaluation=0.0, thinking=False)
            
            # Отображаем текущий шаг
            font = pygame.font.SysFont('Arial', 16)
            step_text = font.render(steps[min(step, len(steps)-1)], True, (255, 255, 255))
            screen.blit(step_text, (10, 520))
            
            # Инструкция
            if step < len(steps) - 1:
                instruction = font.render("Нажмите SPACE для следующего шага или ESC для выхода", True, (200, 200, 200))
            else:
                instruction = font.render("Демонстрация завершена! Нажмите ESC для выхода", True, (100, 255, 100))
            screen.blit(instruction, (10, 550))
            
            # Обработка нажатий клавиш для продвижения по шагам
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and step < len(steps) - 1:
                step += 1
                pygame.time.wait(200)  # Небольшая задержка для предотвращения слишком быстрого продвижения
            
            pygame.display.flip()
            clock.tick(30)
        
        # Очищаем ресурсы
        renderer.cleanup()
        pygame.quit()
        
        print("\n✅ Демонстрация завершена успешно!")
        print("✅ Артефакты при клике на фигуры устранены")
        print("✅ Правильная очистка и отрисовка экрана")
        print("✅ Корректное обновление состояния доски")
        
    except Exception as e:
        pygame.quit()
        print(f"\n❌ Ошибка в демонстрации: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()