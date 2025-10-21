#!/usr/bin/env python3
"""
Тестирование игрового меню.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.in_game_menu import InGameMenu
from utils.sound_manager import SoundManager

def test_in_game_menu():
    """Тестирование игрового меню."""
    pygame.init()
    
    # Создаем окно
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Тест игрового меню")
    
    # Создаем менеджер звуков
    sound_manager = SoundManager()
    
    # Создаем игровое меню
    menu = InGameMenu(screen, sound_manager)
    
    # Показываем меню
    menu.show()
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.show()  # Показываем меню по нажатию ESC
            
            # Обрабатываем события меню
            if menu.visible:
                action = menu.handle_event(event)
                if action:
                    print(f"Выбрано действие меню: {action}")
                    if action == "quit":
                        running = False
        
        # Очищаем экран
        screen.fill((50, 50, 50))
        
        # Рисуем тестовый интерфейс
        font = pygame.font.SysFont('Arial', 24)
        text = font.render("Тест игрового меню - нажмите ESC для вызова меню", True, (255, 255, 255))
        screen.blit(text, (50, 50))
        
        # Отрисовываем меню
        menu.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("Тест завершен")

if __name__ == "__main__":
    test_in_game_menu()