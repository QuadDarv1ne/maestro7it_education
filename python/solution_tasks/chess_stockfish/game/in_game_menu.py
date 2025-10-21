# ============================================================================
# game/in_game_menu.py
# ============================================================================

"""
Модуль: game/in_game_menu.py

Описание:
    Содержит функции для отображения игрового меню во время игры.
    Позволяет игроку:
    - Вернуться в главное меню
    - Изменить параметры игры (сторона, уровень сложности, тема)
    - Перезапустить игру
    - Переключить музыку
    - Выйти из игры
    
Возможности:
    - Интеграция с Pygame UI
    - Красивое оформление меню
    - Управление звуком и музыкой
"""

import pygame
from typing import Tuple, Optional

# Цвета для меню
MENU_BG = (30, 30, 40, 220)  # Полупрозрачный темно-синий фон
MENU_BORDER = (100, 100, 150)
MENU_TEXT = (255, 255, 255)
MENU_HIGHLIGHT = (100, 150, 255)
MENU_HIGHLIGHT_TEXT = (255, 255, 255)
MENU_DISABLED = (100, 100, 100)

class InGameMenu:
    """Класс для отображения и управления игровым меню."""
    
    def __init__(self, screen: pygame.Surface, sound_manager=None):
        """
        Инициализация игрового меню.
        
        Параметры:
            screen (pygame.Surface): Поверхность для отрисовки меню
            sound_manager: Менеджер звуков (опционально)
        """
        self.screen = screen
        self.sound_manager = sound_manager
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
        # Размеры меню
        self.menu_width = 400
        self.menu_height = 500
        self.menu_x = (screen.get_width() - self.menu_width) // 2
        self.menu_y = (screen.get_height() - self.menu_height) // 2
        
        # Элементы меню
        self.menu_items = [
            {"text": "Продолжить игру", "action": "resume", "enabled": True},
            {"text": "Новая игра", "action": "new_game", "enabled": True},
            {"text": "Изменить параметры", "action": "settings", "enabled": True},
            {"text": "Переключить музыку", "action": "toggle_music", "enabled": sound_manager is not None},
            {"text": "Переключить звуки", "action": "toggle_sound", "enabled": sound_manager is not None},
            {"text": "Главное меню", "action": "main_menu", "enabled": True},
            {"text": "Выход из игры", "action": "quit", "enabled": True}
        ]
        
        self.selected_item = 0
        self.visible = False
        self.result = None  # Результат действия меню
        
    def show(self):
        """Показать меню."""
        self.visible = True
        self.selected_item = 0
        self.result = None
        
    def hide(self):
        """Скрыть меню."""
        self.visible = False
        self.result = None
        
    def handle_event(self, event) -> Optional[str]:
        """
        Обработка событий меню.
        
        Параметры:
            event: Событие Pygame
            
        Возвращает:
            str: Действие меню или None
        """
        if not self.visible:
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Перемещение вверх по меню
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                # Пропускаем недоступные элементы
                while not self.menu_items[self.selected_item]["enabled"]:
                    self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                if self.sound_manager:
                    self.sound_manager.play_sound("button")
                    
            elif event.key == pygame.K_DOWN:
                # Перемещение вниз по меню
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                # Пропускаем недоступные элементы
                while not self.menu_items[self.selected_item]["enabled"]:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                if self.sound_manager:
                    self.sound_manager.play_sound("button")
                    
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Выбор элемента меню
                item = self.menu_items[self.selected_item]
                if item["enabled"]:
                    action = item["action"]
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
                    return self._execute_action(action)
                    
            elif event.key == pygame.K_ESCAPE:
                # Закрыть меню
                self.hide()
                if self.sound_manager:
                    self.sound_manager.play_sound("button")
                return "resume"
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Обработка кликов мыши
            mouse_x, mouse_y = event.pos
            for i, item in enumerate(self.menu_items):
                item_y = self.menu_y + 100 + i * 50
                if (self.menu_x + 50 <= mouse_x <= self.menu_x + self.menu_width - 50 and
                    item_y <= mouse_y <= item_y + 40 and
                    item["enabled"]):
                    self.selected_item = i
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
                    return self._execute_action(item["action"])
                    
        return None
        
    def _execute_action(self, action: str) -> str:
        """
        Выполнение действия меню.
        
        Параметры:
            action (str): Действие для выполнения
            
        Возвращает:
            str: Результат действия
        """
        if action == "toggle_music" and self.sound_manager:
            self.sound_manager.toggle_music()
        elif action == "toggle_sound" and self.sound_manager:
            self.sound_manager.toggle_sound()
        elif action == "settings":
            # Показать меню настроек
            return self._show_settings_menu()
            
        self.hide()
        return action
        
    def _show_settings_menu(self) -> str:
        """
        Показать меню настроек.
        
        Возвращает:
            str: Результат действия меню настроек
        """
        # Сохраняем текущие элементы меню
        original_items = self.menu_items[:]
        
        # Создаем элементы меню настроек
        settings_items = [
            {"text": "Сторона: Белые", "action": "toggle_side", "enabled": True},
            {"text": "Сложность: 5", "action": "change_difficulty", "enabled": True},
            {"text": "Тема: classic", "action": "change_theme", "enabled": True},
            {"text": "Назад", "action": "back", "enabled": True}
        ]
        
        # Обновляем меню настроек
        self.menu_items = settings_items
        self.selected_item = 0
        
        # Показываем меню настроек
        return "settings_menu"
        
    def draw(self):
        """Отрисовка меню."""
        if not self.visible:
            return
            
        # Полупрозрачный оверлей
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Фон меню
        menu_rect = pygame.Rect(self.menu_x, self.menu_y, self.menu_width, self.menu_height)
        pygame.draw.rect(self.screen, MENU_BG, menu_rect, border_radius=10)
        pygame.draw.rect(self.screen, MENU_BORDER, menu_rect, 3, border_radius=10)
        
        # Заголовок меню
        title = self.title_font.render("Игровое меню", True, MENU_TEXT)
        title_rect = title.get_rect(center=(self.menu_x + self.menu_width // 2, self.menu_y + 40))
        self.screen.blit(title, title_rect)
        
        # Элементы меню
        for i, item in enumerate(self.menu_items):
            item_y = self.menu_y + 100 + i * 50
            
            # Фон элемента
            item_rect = pygame.Rect(self.menu_x + 50, item_y, self.menu_width - 100, 40)
            
            # Выделение выбранного элемента
            if i == self.selected_item:
                pygame.draw.rect(self.screen, MENU_HIGHLIGHT, item_rect, border_radius=5)
                text_color = MENU_HIGHLIGHT_TEXT
            else:
                text_color = MENU_TEXT if item["enabled"] else MENU_DISABLED
                
            # Текст элемента
            text = self.font.render(item["text"], True, text_color)
            text_rect = text.get_rect(center=(self.menu_x + self.menu_width // 2, item_y + 20))
            self.screen.blit(text, text_rect)
            
            # Иконка для недоступных элементов
            if not item["enabled"]:
                disabled_text = self.small_font.render("(недоступно)", True, MENU_DISABLED)
                disabled_rect = disabled_text.get_rect(
                    center=(self.menu_x + self.menu_width // 2, item_y + 45))
                self.screen.blit(disabled_text, disabled_rect)
        
        # Подсказка
        hint = self.small_font.render("↑↓ - навигация, Enter - выбор, Esc - закрыть", True, MENU_TEXT)
        hint_rect = hint.get_rect(center=(self.menu_x + self.menu_width // 2, self.menu_y + self.menu_height - 30))
        self.screen.blit(hint, hint_rect)