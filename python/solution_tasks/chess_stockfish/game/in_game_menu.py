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
    - Анимация и визуальные эффекты
    - Плавные переходы и улучшенная отзывчивость
"""

import pygame
import time
from typing import Tuple, Optional, Dict, Any

# Цвета для меню
MENU_BG = (30, 30, 40, 220)  # Полупрозрачный темно-синий фон
MENU_BORDER = (100, 100, 150)
MENU_TEXT = (255, 255, 255)
MENU_HIGHLIGHT = (100, 150, 255)
MENU_HIGHLIGHT_TEXT = (255, 255, 255)
MENU_DISABLED = (100, 100, 100)
MENU_HOVER = (120, 170, 255, 100)

# Анимационные параметры
ANIMATION_SPEED = 0.3
MENU_FADE_SPEED = 8


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
        self.setting_font = pygame.font.SysFont('Arial', 20)
        
        # Размеры меню
        self.menu_width = 400
        self.menu_height = 500
        self.menu_x = (screen.get_width() - self.menu_width) // 2
        self.menu_y = (screen.get_height() - self.menu_height) // 2
        
        # Состояние меню
        self.visible = False
        self.result = None
        self.menu_stack = []  # Стек для навигации между меню
        self.current_menu = "main"  # Текущее меню: "main", "settings"
        
        # Анимация
        self.animation_progress = 0
        self.animation_direction = 1  # 1 для открытия, -1 для закрытия
        self.last_animation_time = 0
        self.fade_alpha = 0
        
        # Выбор и наведение
        self.selected_item = 0
        self.hovered_item = -1
        self.last_selected_item = -1
        self.animation_offset = 0
        
        # Настройки игры
        self.game_settings = {
            "player_color": "white",
            "skill_level": 5,
            "theme": "classic"
        }
        
        # Темы оформления
        self.available_themes = ["classic", "dark", "blue", "green", "contrast"]
        self.theme_index = 0
        
        # Элементы основного меню
        self.main_menu_items = [
            {"text": "Продолжить игру", "action": "resume", "enabled": True, "icon": "▶"},
            {"text": "Сдаться", "action": "resign", "enabled": True, "icon": "🏳"},
            {"text": "Новая игра", "action": "new_game", "enabled": True, "icon": "🔄"},
            {"text": "Сохранить игру", "action": "save_game", "enabled": True, "icon": "💾"},
            {"text": "Загрузить игру", "action": "load_game", "enabled": True, "icon": "📂"},
            {"text": "Удалить игру", "action": "delete_game", "enabled": True, "icon": "🗑"},
            {"text": "Настройки", "action": "settings", "enabled": True, "icon": "⚙"},
            {"text": "Переключить музыку", "action": "toggle_music", "enabled": sound_manager is not None, "icon": "♪"},
            {"text": "Переключить звуки", "action": "toggle_sound", "enabled": sound_manager is not None, "icon": "🔊"},
            {"text": "Главное меню", "action": "main_menu", "enabled": True, "icon": "🏠"},
            {"text": "Выход из игры", "action": "quit", "enabled": True, "icon": "❌"}
        ]
        
        # Элементы меню настроек
        self.settings_menu_items = [
            {"text": f"Сторона: {self._get_side_text()}", "action": "toggle_side", "enabled": True, "icon": "♟"},
            {"text": f"Сложность: {self.game_settings['skill_level']}", "action": "change_difficulty", "enabled": True, "icon": "📊"},
            {"text": f"Тема: {self.game_settings['theme']}", "action": "change_theme", "enabled": True, "icon": "🎨"},
            {"text": "Назад", "action": "back", "enabled": True, "icon": "↩"}
        ]
        
        # Элементы меню загрузки игр
        self.load_menu_items = []
        
        # Текущие элементы меню
        self.menu_items = self.main_menu_items[:]
        
    def _get_side_text(self) -> str:
        """Получить текст для отображения стороны игрока."""
        return "Белые" if self.game_settings["player_color"] == "white" else "Черные"
        
    def show(self):
        """Показать меню с анимацией."""
        self.visible = True
        self.current_menu = "main"
        self.menu_items = self.main_menu_items[:]
        self.selected_item = 0
        self.result = None
        self.last_selected_item = -1
        self.animation_offset = 0
        self.last_animation_time = time.time()
        self.hovered_item = -1
        self.animation_direction = 1
        self.animation_progress = 0
        self.fade_alpha = 0
        
    def hide(self):
        """Скрыть меню с анимацией."""
        self.animation_direction = -1
        self.animation_progress = 1.0

    def toggle(self):
        """Переключить видимость меню."""
        if self.visible:
            self.hide()
        else:
            self.show()
        
    def _complete_hide(self):
        """Завершить скрытие меню."""
        self.visible = False
        self.result = None
        self.last_selected_item = -1
        self.animation_offset = 0
        self.hovered_item = -1
        self.fade_alpha = 0
        
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
                # Проигрываем звук только при изменении выбора
                if self.sound_manager and self.selected_item != self.last_selected_item:
                    self.sound_manager.play_sound("button")
                    self.last_selected_item = self.selected_item
                    self.animation_offset = 5  # Начинаем анимацию
                    
            elif event.key == pygame.K_DOWN:
                # Перемещение вниз по меню
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                # Пропускаем недоступные элементы
                while not self.menu_items[self.selected_item]["enabled"]:
                    self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                # Проигрываем звук только при изменении выбора
                if self.sound_manager and self.selected_item != self.last_selected_item:
                    self.sound_manager.play_sound("button")
                    self.last_selected_item = self.selected_item
                    self.animation_offset = 5  # Начинаем анимацию
                    
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Выбор элемента меню
                item = self.menu_items[self.selected_item]
                if item["enabled"]:
                    action = item["action"]
                    # Проигрываем звук только при выборе элемента
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
                    return self._execute_action(action)
                    
            elif event.key == pygame.K_ESCAPE:
                # Закрыть меню
                if self.current_menu == "settings":
                    return self._go_back()
                else:
                    self.hide()
                    # Проигрываем звук только при закрытии меню
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
                    # Проигрываем звук только при выборе элемента мышью
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
                    return self._execute_action(item["action"])
                    
        elif event.type == pygame.MOUSEMOTION:
            # Обработка наведения мыши
            mouse_x, mouse_y = event.pos
            self.hovered_item = -1
            for i, item in enumerate(self.menu_items):
                item_y = self.menu_y + 100 + i * 50
                if (self.menu_x + 50 <= mouse_x <= self.menu_x + self.menu_width - 50 and
                    item_y <= mouse_y <= item_y + 40):
                    self.hovered_item = i
                    break
                    
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
            # Обновляем текст элемента меню
            music_status = "ВКЛ" if self.sound_manager.music_enabled else "ВЫКЛ"
            for item in self.menu_items:
                if item["action"] == "toggle_music":
                    item["text"] = f"Музыка: {music_status}"
                    break
        elif action == "toggle_sound" and self.sound_manager:
            self.sound_manager.toggle_sound()
            # Обновляем текст элемента меню
            sound_status = "ВКЛ" if self.sound_manager.sound_enabled else "ВЫКЛ"
            for item in self.menu_items:
                if item["action"] == "toggle_sound":
                    item["text"] = f"Звуки: {sound_status}"
                    break
        elif action == "settings":
            return self._show_settings_menu()
        elif action == "toggle_side":
            return self._toggle_player_side()
        elif action == "change_difficulty":
            return self._change_difficulty()
        elif action == "change_theme":
            return self._change_theme()
        elif action == "save_game":
            return self._save_game_to_file()
        elif action == "load_game":
            return self._show_load_menu()
        elif action == "delete_game":
            return self._show_delete_menu()
        elif action == "resign":
            return "resign"
        elif action == "back":
            return self._go_back()
        elif action.startswith("load_game_"):
            # Загрузка конкретной игры
            filename = action[10:]  # Убираем префикс "load_game_"
            return self._load_game_from_file(filename)
        elif action.startswith("delete_game_"):
            # Удаление конкретной игры
            filename = action[12:]  # Убираем префикс "delete_game_"
            return self._delete_game_file(filename)
            
        self.hide()
        return action
        
    def _show_settings_menu(self) -> str:
        """Показать меню настроек."""
        self.menu_stack.append(self.menu_items)
        self.current_menu = "settings"
        self.menu_items = self.settings_menu_items[:]
        self.selected_item = 0
        self.last_selected_item = -1
        self.hovered_item = -1
        self.animation_offset = 0
        return "settings_menu"
        
    def _show_load_menu(self) -> str:
        """Показать меню загрузки игр."""
        # Получаем список сохраненных игр
        try:
            from game.chess_game import ChessGame
            game = ChessGame()  # Создаем временный экземпляр для получения списка
            saved_games = game._list_saved_games()
            
            if not saved_games:
                # Импортируем pygame для доступа к move_feedback
                import pygame
                self.move_feedback = "Нет сохраненных партий"
                self.move_feedback_time = time.time()
                return "no_saved_games"
                
            # Создаем элементы меню для каждой сохраненной игры с дополнительной информацией
            self.load_menu_items = []
            import json
            import os
            saves_dir = os.path.join(os.path.dirname(__file__), "..", "saves")
            
            for filename in saved_games[:10]:  # Ограничиваем 10 последними играми
                try:
                    # Читаем информацию из файла сохранения
                    full_path = os.path.join(saves_dir, filename)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        game_data = json.load(f)
                    
                    # Извлекаем информацию для отображения
                    player_color = game_data.get('player_color', 'white')
                    move_count = len(game_data.get('move_history', []))
                    timestamp = game_data.get('timestamp', 0)
                    
                    # Форматируем дату
                    import datetime
                    try:
                        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
                    except:
                        date_str = "Неизвестно"
                    
                    # Создаем отображаемое имя с информацией
                    color_symbol = "♛" if player_color == "white" else "♚"
                    display_name = f"{color_symbol} {filename.replace('.json', '')} | {move_count} ходов | {date_str}"
                    
                    self.load_menu_items.append({
                        "text": display_name,
                        "action": f"load_game_{filename}",
                        "enabled": True,
                        "icon": "📜"
                    })
                except Exception as e:
                    # Если не удалось прочитать файл, показываем базовую информацию
                    display_name = filename.replace(".json", "")
                    self.load_menu_items.append({
                        "text": display_name,
                        "action": f"load_game_{filename}",
                        "enabled": True,
                        "icon": "📜"
                    })
            
            # Добавляем пункт "Назад"
            self.load_menu_items.append({
                "text": "Назад",
                "action": "back",
                "enabled": True,
                "icon": "↩"
            })
            
            self.menu_stack.append(self.menu_items)
            self.current_menu = "load"
            self.menu_items = self.load_menu_items[:]
            self.selected_item = 0
            self.last_selected_item = -1
            self.hovered_item = -1
            self.animation_offset = 0
            return "load_menu"
        except Exception as e:
            print(f"Ошибка при создании меню загрузки: {e}")
            # Импортируем pygame для доступа к move_feedback
            import pygame
            self.move_feedback = "Ошибка при загрузке списка партий"
            self.move_feedback_time = time.time()
            return "load_error"
        
    def _show_delete_menu(self) -> str:
        """Показать меню удаления игр."""
        # Получаем список сохраненных игр
        try:
            from game.chess_game import ChessGame
            game = ChessGame()  # Создаем временный экземпляр для получения списка
            saved_games = game._list_saved_games()
            
            if not saved_games:
                self.move_feedback = "Нет сохраненных партий для удаления"
                self.move_feedback_time = time.time()
                return "no_saved_games"
                
            # Создаем элементы меню для каждой сохраненной игры с дополнительной информацией
            self.load_menu_items = []
            import json
            import os
            saves_dir = os.path.join(os.path.dirname(__file__), "..", "saves")
            
            for filename in saved_games[:10]:  # Ограничиваем 10 последними играми
                try:
                    # Читаем информацию из файла сохранения
                    full_path = os.path.join(saves_dir, filename)
                    with open(full_path, 'r', encoding='utf-8') as f:
                        game_data = json.load(f)
                    
                    # Извлекаем информацию для отображения
                    player_color = game_data.get('player_color', 'white')
                    move_count = len(game_data.get('move_history', []))
                    timestamp = game_data.get('timestamp', 0)
                    
                    # Форматируем дату
                    import datetime
                    try:
                        date_str = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
                    except:
                        date_str = "Неизвестно"
                    
                    # Создаем отображаемое имя с информацией
                    color_symbol = "♛" if player_color == "white" else "♚"
                    display_name = f"{color_symbol} {filename.replace('.json', '')} | {move_count} ходов | {date_str}"
                    
                    self.load_menu_items.append({
                        "text": display_name,
                        "action": f"delete_game_{filename}",
                        "enabled": True,
                        "icon": "🗑"
                    })
                except Exception as e:
                    # Если не удалось прочитать файл, показываем базовую информацию
                    display_name = filename.replace(".json", "")
                    self.load_menu_items.append({
                        "text": display_name,
                        "action": f"delete_game_{filename}",
                        "enabled": True,
                        "icon": "🗑"
                    })
            
            # Добавляем пункт "Назад"
            self.load_menu_items.append({
                "text": "Назад",
                "action": "back",
                "enabled": True,
                "icon": "↩"
            })
            
            self.menu_stack.append(self.menu_items)
            self.current_menu = "delete"
            self.menu_items = self.load_menu_items[:]
            self.selected_item = 0
            self.last_selected_item = -1
            self.hovered_item = -1
            self.animation_offset = 0
            return "delete_menu"
        except Exception as e:
            print(f"Ошибка при создании меню удаления: {e}")
            self.move_feedback = "Ошибка при загрузке списка партий для удаления"
            self.move_feedback_time = time.time()
            return "delete_error"
        
    def _save_game_to_file(self) -> str:
        """Сохранить игру в файл."""
        # Эта функция будет вызывать метод сохранения в ChessGame
        # Возвращаем специальное значение, которое будет обработано в основном цикле игры
        return "save_to_file"
        
    def _load_game_from_file(self, filename: str) -> str:
        """Загрузить игру из файла."""
        # Эта функция будет вызывать метод загрузки в ChessGame
        # Возвращаем специальное значение, которое будет обработано в основном цикле игры
        return f"load_from_file_{filename}"
        
    def _toggle_player_side(self) -> str:
        """Переключить сторону игрока."""
        self.game_settings["player_color"] = "black" if self.game_settings["player_color"] == "white" else "white"
        # Обновляем текст элемента меню
        for item in self.menu_items:
            if item["action"] == "toggle_side":
                item["text"] = f"Сторона: {self._get_side_text()}"
                break
        # Проигрываем звук
        if self.sound_manager:
            self.sound_manager.play_sound("button")
        return "side_changed"
        
    def _change_difficulty(self) -> str:
        """Изменить уровень сложности."""
        # Циклически переключаем уровень сложности от 1 до 20
        self.game_settings["skill_level"] = (self.game_settings["skill_level"] % 20) + 1
        # Обновляем текст элемента меню
        for item in self.menu_items:
            if item["action"] == "change_difficulty":
                item["text"] = f"Сложность: {self.game_settings['skill_level']}"
                break
        # Проигрываем звук
        if self.sound_manager:
            self.sound_manager.play_sound("button")
        return "difficulty_changed"
        
    def _change_theme(self) -> str:
        """Изменить тему оформления."""
        # Циклически переключаем темы
        self.theme_index = (self.theme_index + 1) % len(self.available_themes)
        self.game_settings["theme"] = self.available_themes[self.theme_index]
        # Обновляем текст элемента меню
        for item in self.menu_items:
            if item["action"] == "change_theme":
                item["text"] = f"Тема: {self.game_settings['theme']}"
                break
        # Проигрываем звук
        if self.sound_manager:
            self.sound_manager.play_sound("button")
        return "theme_changed"
        
    def _go_back(self) -> str:
        """Вернуться в предыдущее меню."""
        if self.menu_stack:
            self.menu_items = self.menu_stack.pop()
            self.current_menu = "main" if not self.menu_stack else "settings"
            self.selected_item = 0
            self.last_selected_item = -1
            self.hovered_item = -1
            self.animation_offset = 0
            # Проигрываем звук
            if self.sound_manager:
                self.sound_manager.play_sound("button")
            return "back"
        else:
            self.hide()
            return "resume"
        
    def update(self):
        """Обновление анимации меню."""
        if not self.visible:
            return
            
        current_time = time.time()
        delta_time = current_time - self.last_animation_time
        self.last_animation_time = current_time
        
        # Обновление анимации открытия/закрытия
        if self.animation_direction == 1:  # Открытие
            self.animation_progress = min(1.0, self.animation_progress + ANIMATION_SPEED * delta_time)
            self.fade_alpha = min(180, self.fade_alpha + MENU_FADE_SPEED * delta_time)
        else:  # Закрытие
            self.animation_progress = max(0.0, self.animation_progress - ANIMATION_SPEED * delta_time)
            self.fade_alpha = max(0, self.fade_alpha - MENU_FADE_SPEED * delta_time)
            
            # Если анимация закрытия завершена, полностью скрываем меню
            if self.animation_progress <= 0:
                self._complete_hide()
                return
        
        # Обновление анимации выбора
        if current_time - self.last_animation_time > 0.016:  # Примерно 60 FPS
            if self.animation_offset > 0:
                self.animation_offset -= 0.5
                if self.animation_offset < 0:
                    self.animation_offset = 0
            self.last_animation_time = current_time
        
    def draw(self):
        """Отрисовка меню."""
        if not self.visible:
            return
            
        # Обновляем анимацию
        self.update()
        
        # Применяем easing функцию для плавной анимации
        eased_progress = self._ease_out_cubic(self.animation_progress)
        
        # Полупрозрачный оверлей с анимацией появления
        overlay_alpha = int(self.fade_alpha * eased_progress)
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, overlay_alpha))
        self.screen.blit(overlay, (0, 0))
        
        # Анимированное позиционирование меню
        animated_menu_y = self.menu_y + (1 - eased_progress) * 50
        
        # Фон меню с анимацией масштабирования
        scale_factor = 0.8 + 0.2 * eased_progress
        menu_rect = pygame.Rect(
            self.menu_x + (1 - scale_factor) * self.menu_width // 2,
            animated_menu_y + (1 - scale_factor) * self.menu_height // 2,
            self.menu_width * scale_factor,
            self.menu_height * scale_factor
        )
        
        # Рисуем тень с анимацией
        shadow_offset = int(3 * eased_progress)
        shadow_rect = pygame.Rect(
            menu_rect.x + shadow_offset,
            menu_rect.y + shadow_offset,
            menu_rect.width,
            menu_rect.height
        )
        shadow_surface = pygame.Surface((menu_rect.width, menu_rect.height), pygame.SRCALPHA)
        shadow_surface.fill((0, 0, 0, int(100 * eased_progress)))
        self.screen.blit(shadow_surface, (menu_rect.x + shadow_offset, menu_rect.y + shadow_offset))
        
        # Основной фон меню
        pygame.draw.rect(self.screen, MENU_BG, menu_rect, border_radius=int(12 * scale_factor))
        pygame.draw.rect(self.screen, MENU_BORDER, menu_rect, int(3 * scale_factor), border_radius=int(12 * scale_factor))
        
        # Заголовок меню
        title_text = "Настройки" if self.current_menu == "settings" else "Игровое меню"
        title = self.title_font.render(title_text, True, MENU_TEXT)
        title_rect = title.get_rect(center=(menu_rect.centerx, menu_rect.top + int(40 * scale_factor)))
        self.screen.blit(title, title_rect)
        
        # Элементы меню
        for i, item in enumerate(self.menu_items):
            item_y = menu_rect.top + int(100 * scale_factor) + i * int(50 * scale_factor)
            
            # Анимация для выбранного элемента
            animated_offset = 0
            if i == self.selected_item and self.animation_offset > 0:
                animated_offset = self.animation_offset * eased_progress
            
            # Фон элемента
            item_rect = pygame.Rect(
                menu_rect.left + int(50 * scale_factor) - animated_offset,
                item_y,
                menu_rect.width - int(100 * scale_factor) + 2 * animated_offset,
                int(40 * scale_factor)
            )
            
            # Выделение выбранного элемента
            if i == self.selected_item:
                highlight_rect = pygame.Rect(
                    item_rect.x - 2,
                    item_rect.y - 2,
                    item_rect.width + 4,
                    item_rect.height + 4
                )
                pygame.draw.rect(self.screen, MENU_HIGHLIGHT, highlight_rect, border_radius=int(8 * scale_factor))
                text_color = MENU_HIGHLIGHT_TEXT
            elif i == self.hovered_item:
                # Эффект наведения
                hover_surface = pygame.Surface((item_rect.width, item_rect.height), pygame.SRCALPHA)
                hover_surface.fill(MENU_HOVER)
                self.screen.blit(hover_surface, (item_rect.x, item_rect.y))
                pygame.draw.rect(self.screen, MENU_HIGHLIGHT, item_rect, 2, border_radius=int(6 * scale_factor))
                text_color = MENU_TEXT
            else:
                text_color = MENU_TEXT if item["enabled"] else MENU_DISABLED
                
            # Иконка элемента
            if "icon" in item:
                icon = self.font.render(item["icon"], True, text_color)
                icon_rect = icon.get_rect(midleft=(item_rect.left + 5, item_rect.centery))
                self.screen.blit(icon, icon_rect)
                
            # Текст элемента
            text = self.setting_font.render(item["text"], True, text_color)
            text_rect = text.get_rect(midleft=(item_rect.left + 30, item_rect.centery))
            self.screen.blit(text, text_rect)
            
            # Иконка для недоступных элементов
            if not item["enabled"]:
                disabled_text = self.small_font.render("(недоступно)", True, MENU_DISABLED)
                disabled_rect = disabled_text.get_rect(
                    center=(menu_rect.centerx, item_y + int(45 * scale_factor)))
                self.screen.blit(disabled_text, disabled_rect)
        
        # Подсказка
        hint_text = "↑↓ - навигация, Enter - выбор, Esc - закрыть"
        if self.current_menu == "settings":
            hint_text = "↑↓ - навигация, Enter - выбор, Esc - назад"
            
        hint_bg = pygame.Surface((int((menu_rect.width - 40) * 0.8), int(30 * scale_factor)), pygame.SRCALPHA)
        hint_bg.fill((0, 0, 0, int(120 * eased_progress)))
        hint_bg_rect = hint_bg.get_rect(center=(menu_rect.centerx, menu_rect.bottom - int(30 * scale_factor)))
        self.screen.blit(hint_bg, hint_bg_rect)
        
        hint = self.small_font.render(hint_text, True, MENU_TEXT)
        hint_rect = hint.get_rect(center=(menu_rect.centerx, menu_rect.bottom - int(30 * scale_factor)))
        self.screen.blit(hint, hint_rect)
        
    def _ease_out_cubic(self, t: float) -> float:
        """Easing функция для плавной анимации."""
        return 1 - pow(1 - t, 3)
        
    def get_settings(self) -> Dict[str, Any]:
        """Получить текущие настройки игры."""
        return self.game_settings.copy()
        
    def set_settings(self, settings: Dict[str, Any]):
        """Установить настройки игры."""
        self.game_settings.update(settings)
        # Обновляем индекс темы
        if "theme" in settings:
            try:
                self.theme_index = self.available_themes.index(settings["theme"])
            except ValueError:
                self.theme_index = 0
        # Обновляем элементы меню настроек
        for item in self.settings_menu_items:
            if item["action"] == "toggle_side":
                item["text"] = f"Сторона: {self._get_side_text()}"
            elif item["action"] == "change_difficulty":
                item["text"] = f"Сложность: {self.game_settings['skill_level']}"
            elif item["action"] == "change_theme":
                item["text"] = f"Тема: {self.game_settings['theme']}"

    def _delete_game_file(self, filename: str) -> str:
        """Удалить игру из файла."""
        # Эта функция будет вызывать метод удаления в ChessGame
        # Возвращаем специальное значение, которое будет обработано в основном цикле игры
        return f"delete_game_{filename}"