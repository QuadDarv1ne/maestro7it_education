#!/usr/bin/env python3
"""
Integration test for the complete chess game system.
"""

import pygame
import sys
import os

# Добавляем путь к модулям игры
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from game.chess_game import ChessGame
from utils.sound_manager import SoundManager
from game.in_game_menu import InGameMenu

def test_integration():
    """Тестирование интеграции всех компонентов."""
    print("🚀 Запуск интеграционного теста...")
    
    # Инициализируем Pygame
    pygame.init()
    
    try:
        # Создаем игру
        print("🎮 Создание игры...")
        game = ChessGame(player_color='white', skill_level=1, theme='classic')
        print("✅ Игра создана успешно")
        
        # Проверяем наличие менеджера звуков
        assert hasattr(game, 'sound_manager'), "Игра должна иметь менеджер звуков"
        assert isinstance(game.sound_manager, SoundManager), "Менеджер звуков должен быть экземпляром SoundManager"
        print("✅ Менеджер звуков интегрирован")
        
        # Проверяем наличие игрового меню
        assert hasattr(game, 'in_game_menu'), "Игра должна иметь игровое меню"
        assert isinstance(game.in_game_menu, InGameMenu), "Игровое меню должно быть экземпляром InGameMenu"
        print("✅ Игровое меню интегрировано")
        
        # Проверяем интеграцию менеджера звуков с меню
        assert game.in_game_menu.sound_manager == game.sound_manager, "Менеджер звуков должен быть передан в меню"
        print("✅ Интеграция менеджера звуков с меню успешна")
        
        # Проверяем начальное состояние меню
        assert not game.in_game_menu.visible, "Меню должно быть скрыто по умолчанию"
        print("✅ Меню скрыто по умолчанию")
        
        # Проверяем функции меню
        game.in_game_menu.show()
        assert game.in_game_menu.visible, "Меню должно стать видимым"
        print("✅ Меню становится видимым")
        
        game.in_game_menu.hide()
        assert not game.in_game_menu.visible, "Меню должно стать скрытым"
        print("✅ Меню становится скрытым")
        
        # Проверяем элементы меню
        menu_items = game.in_game_menu.menu_items
        assert len(menu_items) >= 5, "Меню должно содержать как минимум 5 элементов"
        print(f"✅ Меню содержит {len(menu_items)} элементов")
        
        # Проверяем наличие ключевых элементов
        actions = [item['action'] for item in menu_items]
        assert 'resume' in actions, "Меню должно содержать действие 'resume'"
        assert 'new_game' in actions, "Меню должно содержать действие 'new_game'"
        assert 'main_menu' in actions, "Меню должно содержать действие 'main_menu'"
        assert 'quit' in actions, "Меню должно содержать действие 'quit'"
        print("✅ Все ключевые элементы меню присутствуют")
        
        # Очищаем ресурсы
        game.renderer.cleanup()
        pygame.quit()
        
        print("\n🎉 Интеграционный тест пройден успешно!")
        print("✅ Все компоненты интегрированы правильно")
        print("✅ Игровое меню работает корректно")
        print("✅ Менеджер звуков интегрирован")
        print("✅ Система готова к использованию")
        
    except Exception as e:
        pygame.quit()
        print(f"\n❌ Тест провален: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_integration()