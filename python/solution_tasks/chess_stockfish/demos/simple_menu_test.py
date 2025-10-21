#!/usr/bin/env python3
"""
Простое тестирование игрового меню без пользовательского ввода.
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
    
    # Проверяем начальное состояние
    assert not menu.visible, "Меню должно быть скрыто по умолчанию"
    print("✓ Меню скрыто по умолчанию")
    
    # Показываем меню
    menu.show()
    assert menu.visible, "Меню должно быть видимым после вызова show()"
    print("✓ Меню становится видимым после show()")
    
    # Скрываем меню
    menu.hide()
    assert not menu.visible, "Меню должно быть скрыто после вызова hide()"
    print("✓ Меню скрыто после hide()")
    
    # Проверяем количество элементов меню
    assert len(menu.menu_items) == 7, "Меню должно содержать 7 элементов"
    print("✓ Меню содержит правильное количество элементов")
    
    # Проверяем, что все элементы имеют необходимые поля
    for i, item in enumerate(menu.menu_items):
        assert "text" in item, f"Элемент {i} должен содержать поле 'text'"
        assert "action" in item, f"Элемент {i} должен содержать поле 'action'"
        assert "enabled" in item, f"Элемент {i} должен содержать поле 'enabled'"
    print("✓ Все элементы меню имеют необходимые поля")
    
    # Проверяем специфические элементы меню
    first_item = menu.menu_items[0]
    assert first_item["text"] == "Продолжить игру", "Первый элемент должен быть 'Продолжить игру'"
    assert first_item["action"] == "resume", "Первый элемент должен иметь действие 'resume'"
    assert first_item["enabled"] == True, "Первый элемент должен быть включен"
    print("✓ Первый элемент меню корректен")
    
    last_item = menu.menu_items[-1]
    assert last_item["text"] == "Выход из игры", "Последний элемент должен быть 'Выход из игры'"
    assert last_item["action"] == "quit", "Последний элемент должен иметь действие 'quit'"
    assert last_item["enabled"] == True, "Последний элемент должен быть включен"
    print("✓ Последний элемент меню корректен")
    
    pygame.quit()
    print("\n✅ Все тесты пройдены успешно!")

if __name__ == "__main__":
    test_in_game_menu()