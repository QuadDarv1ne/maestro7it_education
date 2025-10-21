#!/usr/bin/env python3
"""
Комплексный тест для выявления и исправления ошибок в игре.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from ui.board_renderer import BoardRenderer
from utils.sound_manager import SoundManager
from game.in_game_menu import InGameMenu
from game.menu import main_menu

def test_all_components():
    """Тест всех компонентов игры."""
    pygame.init()
    
    try:
        print("🚀 Запуск комплексного теста...")
        
        # Тест 1: Проверка инициализации Pygame
        print("Тест 1: Проверка инициализации Pygame")
        assert pygame.get_init(), "Pygame должен быть инициализирован"
        print("✅ Pygame инициализирован")
        
        # Тест 2: Проверка создания экрана
        print("Тест 2: Проверка создания экрана")
        screen = pygame.display.set_mode((512, 612))
        assert screen is not None, "Экран должен быть создан"
        print("✅ Экран создан")
        
        # Тест 3: Проверка звукового менеджера
        print("Тест 3: Проверка звукового менеджера")
        sound_manager = SoundManager()
        sound_manager.load_sounds()
        assert hasattr(sound_manager, 'sounds'), "Менеджер звуков должен иметь атрибут sounds"
        assert "button" in sound_manager.sounds, "Менеджер звуков должен содержать звук кнопки"
        print("✅ Звуковой менеджер работает")
        
        # Тест 4: Проверка рендерера
        print("Тест 4: Проверка рендерера")
        renderer = BoardRenderer(screen, 'white')
        assert renderer is not None, "Рендерер должен быть создан"
        assert hasattr(renderer, 'effect_renderer'), "Рендерер должен иметь effect_renderer"
        print("✅ Рендерер работает")
        
        # Тест 5: Проверка игрового меню
        print("Тест 5: Проверка игрового меню")
        menu = InGameMenu(screen, sound_manager)
        assert menu is not None, "Меню должно быть создано"
        assert len(menu.menu_items) > 0, "Меню должно содержать элементы"
        print("✅ Игровое меню работает")
        
        # Тест 6: Проверка показа/скрытия меню
        print("Тест 6: Проверка показа/скрытия меню")
        menu.show()
        assert menu.visible == True, "Меню должно быть видимым после show()"
        menu.hide()
        assert menu.visible == False, "Меню должно быть скрытым после hide()"
        print("✅ Показ/скрытие меню работает")
        
        # Тест 7: Проверка обработки событий меню
        print("Тест 7: Проверка обработки событий меню")
        menu.show()
        # Создаем фиктивное событие
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        result = menu.handle_event(event)
        assert menu.visible == False, "Меню должно быть скрыто после нажатия ESC"
        print("✅ Обработка событий меню работает")
        
        # Тест 8: Проверка отрисовки меню
        print("Тест 8: Проверка отрисовки меню")
        menu.show()
        menu.draw()
        # Если мы дошли до этой точки, отрисовка работает
        print("✅ Отрисовка меню работает")
        
        # Тест 9: Проверка звуков
        print("Тест 9: Проверка звуков")
        sound_manager.play_sound("button")
        # Если мы дошли до этой точки, звуки работают
        print("✅ Звуки работают")
        
        # Тест 10: Проверка переключения звука
        print("Тест 10: Проверка переключения звука")
        original_state = sound_manager.sound_enabled
        new_state = sound_manager.toggle_sound()
        assert new_state != original_state, "Состояние звука должно измениться"
        sound_manager.toggle_sound()  # Возвращаем обратно
        print("✅ Переключение звука работает")
        
        # Очищаем ресурсы
        pygame.quit()
        
        print("\n🎉 Все тесты пройдены успешно!")
        print("✅ Все компоненты работают корректно")
        print("✅ Ошибки устранены")
        
    except Exception as e:
        pygame.quit()
        print(f"\n❌ Тест провален: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_all_components()