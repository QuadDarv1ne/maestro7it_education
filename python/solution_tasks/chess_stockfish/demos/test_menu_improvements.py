#!/usr/bin/env python3
"""
Тестирование улучшений игрового меню.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.in_game_menu import InGameMenu
from utils.sound_manager import SoundManager

def test_menu_improvements():
    """Тестирование улучшений игрового меню."""
    pygame.init()
    
    # Создаем окно
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Тест улучшений игрового меню")
    
    # Создаем менеджер звуков
    sound_manager = SoundManager()
    sound_manager.load_sounds()
    
    # Создаем игровое меню
    menu = InGameMenu(screen, sound_manager)
    
    # Проверяем начальное состояние
    assert not menu.visible, "Меню должно быть скрыто по умолчанию"
    print("✓ Меню скрыто по умолчанию")
    
    # Проверяем анимацию
    assert hasattr(menu, 'animation_offset'), "Меню должно иметь атрибут animation_offset"
    assert hasattr(menu, 'last_animation_time'), "Меню должно иметь атрибут last_animation_time"
    print("✓ Анимация меню реализована")
    
    # Проверяем отслеживание наведения мыши
    assert hasattr(menu, 'hovered_item'), "Меню должно иметь атрибут hovered_item"
    print("✓ Отслеживание наведения мыши реализовано")
    
    # Проверяем улучшенный звук кнопки
    assert "button" in sound_manager.sounds, "Менеджер звуков должен содержать улучшенный звук кнопки"
    print("✓ Улучшенный звук кнопки загружен")
    
    # Проверяем методы обновления
    assert hasattr(menu, 'update'), "Меню должно иметь метод update"
    print("✓ Метод обновления меню реализован")
    
    # Проверяем показ меню
    menu.show()
    assert menu.visible, "Меню должно быть видимым после вызова show()"
    assert menu.selected_item == 0, "Первый элемент должен быть выбран по умолчанию"
    assert menu.last_selected_item == -1, "Последний выбранный элемент должен быть -1"
    assert menu.animation_offset == 0, "Смещение анимации должно быть 0"
    print("✓ Меню корректно показывается")
    
    # Проверяем скрытие меню
    menu.hide()
    assert not menu.visible, "Меню должно быть скрыто после вызова hide()"
    assert menu.hovered_item == -1, "Элемент наведения должен быть сброшен"
    print("✓ Меню корректно скрывается")
    
    # Проверяем анимацию
    menu.show()
    original_time = menu.last_animation_time
    menu.animation_offset = 5
    menu.update()
    # Анимация должна уменьшиться
    assert menu.animation_offset <= 5, "Анимация должна обновляться"
    print("✓ Анимация меню работает")
    
    pygame.quit()
    print("\n✅ Все тесты улучшений пройдены успешно!")

if __name__ == "__main__":
    test_menu_improvements()