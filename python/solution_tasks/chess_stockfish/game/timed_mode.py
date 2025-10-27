# ============================================================================
# game/timed_mode.py
# ============================================================================

"""
Модуль: game/timed_mode.py

Описание:
    Реализация режима игры на время для шахматной игры chess_stockfish.
    Предоставляет различные временные контроли для игры.

Возможности:
    - Различные временные контроли (blitz, bullet, rapid)
    - Отслеживание времени для каждого игрока
    - Система инкремента времени
    - Визуальная индикация времени
"""

import pygame
import time
from typing import Dict, Optional, Tuple

from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer
from utils.sound_manager import SoundManager


class TimedMode:
    """
    Класс для управления режимом игры на время.
    """
    
    # Предопределенные временные контроли
    TIME_CONTROLS = {
        'bullet_1_0': {'base_time': 60, 'increment': 0, 'name': 'Bullet 1+0'},      # 1 минута, 0 инкремент
        'bullet_2_1': {'base_time': 120, 'increment': 1, 'name': 'Bullet 2+1'},     # 2 минуты, 1 инкремент
        'blitz_3_0': {'base_time': 180, 'increment': 0, 'name': 'Blitz 3+0'},       # 3 минуты, 0 инкремент
        'blitz_3_2': {'base_time': 180, 'increment': 2, 'name': 'Blitz 3+2'},       # 3 минуты, 2 инкремент
        'blitz_5_0': {'base_time': 300, 'increment': 0, 'name': 'Blitz 5+0'},       # 5 минут, 0 инкремент
        'rapid_10_0': {'base_time': 600, 'increment': 0, 'name': 'Rapid 10+0'},     # 10 минут, 0 инкремент
        'rapid_15_10': {'base_time': 900, 'increment': 10, 'name': 'Rapid 15+10'},  # 15 минут, 10 инкремент
    }
    
    def __init__(self, screen: pygame.Surface, player_color: str = 'white', 
                 time_control: str = 'blitz_3_0'):
        """
        Инициализация режима игры на время.
        
        Параметры:
            screen (pygame.Surface): Поверхность для отрисовки
            player_color (str): Цвет игрока ('white' или 'black')
            time_control (str): Временной контроль из TIME_CONTROLS
        """
        self.screen = screen
        self.player_color = player_color
        self.time_control_key = time_control
        self.time_control = self.TIME_CONTROLS.get(time_control, self.TIME_CONTROLS['blitz_3_0'])
        
        # Инициализация движка и рендерера
        self.engine = StockfishWrapper(skill_level=10)
        self.renderer = BoardRenderer(screen, player_color)
        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds()
        
        # Временные параметры
        self.white_time = self.time_control['base_time']  # Время в секундах
        self.black_time = self.time_control['base_time']
        self.increment = self.time_control['increment']
        self.last_move_time = time.time()
        self.game_started = False
        self.game_paused = False
        self.game_over = False
        self.winner = None
        self.game_over_reason = ""
        
        # Состояние игры
        self.selected_square: Optional[Tuple[int, int]] = None
        self.move_hints: list = []
        self.feedback_message = ""
        self.feedback_time = 0
        self.move_count = 0
        
        # Цвета для отображения времени
        self.time_colors = {
            'normal': (255, 255, 255),    # Белый - нормальное время
            'warning': (255, 255, 0),     # Желтый - мало времени
            'critical': (255, 100, 100)   # Красный - критически мало времени
        }
    
    def start_game(self):
        """Начать игру на время."""
        self.game_started = True
        self.last_move_time = time.time()
        self.feedback_message = f"Игра началась! {self.time_control['name']}"
        self.feedback_time = time.time()
        
        # Проигрываем звук начала игры
        if self.sound_manager:
            self.sound_manager.play_sound("move")
    
    def make_move(self, uci_move: str) -> bool:
        """
        Выполнить ход в режиме игры на время.
        
        Параметры:
            uci_move (str): Ход в формате UCI
            
        Возвращает:
            bool: True если ход выполнен успешно
        """
        if not self.game_started or self.game_over or self.game_paused:
            return False
            
        if not self.engine.is_move_correct(uci_move):
            self.feedback_message = "Недопустимый ход"
            self.feedback_time = time.time()
            if self.sound_manager:
                self.sound_manager.play_sound("button")
            return False
        
        # Обновляем время игрока
        current_time = time.time()
        elapsed_time = current_time - self.last_move_time
        self.last_move_time = current_time
        
        # Определяем, чей ход был сделан
        side_to_move = self.engine.get_side_to_move()
        is_white_move = side_to_move == 'w'
        
        # Вычитаем время из соответствующего игрока
        if is_white_move:
            self.white_time -= elapsed_time
            # Добавляем инкремент
            self.white_time += self.increment
        else:
            self.black_time -= elapsed_time
            # Добавляем инкремент
            self.black_time += self.increment
        
        # Проверяем, не закончилось ли время
        if (is_white_move and self.white_time <= 0) or (not is_white_move and self.black_time <= 0):
            self.game_over = True
            self.winner = 'black' if is_white_move else 'white'
            self.game_over_reason = "Время истекло"
            self.feedback_message = f"Время истекло! Победили {self.winner}"
            self.feedback_time = time.time()
            if self.sound_manager:
                self.sound_manager.play_sound("capture")
            return True
        
        # Выполняем ход
        if self.engine.make_move(uci_move):
            self.move_count += 1
            
            # Проверяем окончание игры
            is_over, reason = self.engine.is_game_over()
            if is_over:
                self.game_over = True
                self.game_over_reason = reason
                # Определяем победителя
                if reason and "мат" in reason.lower():
                    self.winner = 'white' if is_white_move else 'black'
                elif reason and "пат" in reason.lower():
                    self.winner = "draw"
                self.feedback_message = reason
            else:
                self.feedback_message = f"Ход выполнен: {uci_move}"
            
            self.feedback_time = time.time()
            
            # Проигрываем звук хода
            if self.sound_manager:
                self.sound_manager.play_sound("move")
            
            return True
        else:
            self.feedback_message = "Ошибка при выполнении хода"
            self.feedback_time = time.time()
            if self.sound_manager:
                self.sound_manager.play_sound("button")
            return False
    
    def get_time_string(self, seconds: float) -> str:
        """
        Преобразовать секунды в строку времени.
        
        Параметры:
            seconds (float): Время в секундах
            
        Возвращает:
            str: Отформатированная строка времени
        """
        if seconds <= 0:
            return "0:00"
        
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}:{secs:02d}"
    
    def get_time_color(self, seconds: float) -> Tuple[int, int, int]:
        """
        Получить цвет для отображения времени в зависимости от оставшегося времени.
        
        Параметры:
            seconds (float): Оставшееся время в секундах
            
        Возвращает:
            Tuple[int, int, int]: Цвет RGB
        """
        if seconds <= 10:
            return self.time_colors['critical']
        elif seconds <= 30:
            return self.time_colors['warning']
        else:
            return self.time_colors['normal']
    
    def pause_game(self):
        """Поставить игру на паузу."""
        if self.game_started and not self.game_over:
            self.game_paused = True
            self.feedback_message = "Игра на паузе"
            self.feedback_time = time.time()
    
    def resume_game(self):
        """Продолжить игру."""
        if self.game_paused:
            self.game_paused = False
            self.last_move_time = time.time()
            self.feedback_message = "Игра продолжается"
            self.feedback_time = time.time()
    
    def draw_ui(self):
        """Отрисовка пользовательского интерфейса режима игры на время."""
        BOARD_SIZE = 512
        
        # Информационная панель
        info_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
        pygame.draw.rect(self.screen, (50, 50, 50), info_rect)
        pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE), 
                        (BOARD_SIZE, BOARD_SIZE), 2)
        
        # Время игроков
        font = pygame.font.SysFont('Arial', 16, bold=True)
        
        # Время черных (вверху)
        black_time_str = self.get_time_string(self.black_time)
        black_time_color = self.get_time_color(self.black_time)
        black_text = font.render(f"Черные: {black_time_str}", True, black_time_color)
        self.screen.blit(black_text, (20, BOARD_SIZE + 10))
        
        # Время белых (внизу)
        white_time_str = self.get_time_string(self.white_time)
        white_time_color = self.get_time_color(self.white_time)
        white_text = font.render(f"Белые: {white_time_str}", True, white_time_color)
        self.screen.blit(white_text, (20, BOARD_SIZE + 60))
        
        # Название временного контроля
        control_font = pygame.font.SysFont('Arial', 14)
        control_text = control_font.render(self.time_control['name'], True, (200, 200, 200))
        self.screen.blit(control_text, (BOARD_SIZE - 150, BOARD_SIZE + 10))
        
        # Ходы
        moves_text = control_font.render(f"Ходы: {self.move_count}", True, (200, 200, 100))
        self.screen.blit(moves_text, (BOARD_SIZE - 150, BOARD_SIZE + 35))
        
        # Статус игры
        status_text = ""
        if not self.game_started:
            status_text = "Ожидание начала игры"
        elif self.game_paused:
            status_text = "ПАУЗА"
        elif self.game_over:
            status_text = "ИГРА ЗАВЕРШЕНА"
        else:
            side_to_move = self.engine.get_side_to_move()
            player_side = "Ваш ход" if (side_to_move == 'w' and self.player_color == 'white') or \
                                     (side_to_move == 'b' and self.player_color == 'black') else "Ход соперника"
            status_text = player_side
        
        status_color = (100, 255, 100) if "Ваш" in status_text else (200, 200, 200)
        status_render = control_font.render(status_text, True, status_color)
        self.screen.blit(status_render, (BOARD_SIZE // 2 - status_render.get_width() // 2, BOARD_SIZE + 35))
        
        # Обратная связь
        if self.feedback_message and time.time() - self.feedback_time < 3:
            feedback_font = pygame.font.SysFont('Arial', 14)
            feedback_color = (100, 255, 100) if "выполнен" in self.feedback_message or "Победили" in self.feedback_message else (255, 100, 100)
            feedback_text = feedback_font.render(self.feedback_message, True, feedback_color)
            self.screen.blit(feedback_text, (BOARD_SIZE // 2 - feedback_text.get_width() // 2, BOARD_SIZE + 75))
        
        # Кнопки управления
        button_font = pygame.font.SysFont('Arial', 12)
        
        # Кнопка паузы/продолжения
        pause_rect = pygame.Rect(BOARD_SIZE - 100, BOARD_SIZE + 60, 80, 25)
        pygame.draw.rect(self.screen, (70, 70, 150), pause_rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 200), pause_rect, 2, border_radius=5)
        pause_text = "Пауза" if not self.game_paused else "Продолжить"
        pause_render = button_font.render(pause_text, True, (255, 255, 255))
        self.screen.blit(pause_render, (pause_rect.centerx - pause_render.get_width() // 2, 
                                      pause_rect.centery - pause_render.get_height() // 2))
    
    def handle_click(self, x: int, y: int) -> str:
        """
        Обработка клика мыши.
        
        Параметры:
            x (int): Координата X клика
            y (int): Координата Y клика
            
        Возвращает:
            str: Действие, которое нужно выполнить ('pause', 'none')
        """
        BOARD_SIZE = 512
        
        # Проверяем клик по кнопке паузы
        if BOARD_SIZE <= y <= BOARD_SIZE + 100 and BOARD_SIZE - 100 <= x <= BOARD_SIZE - 20:
            if BOARD_SIZE + 60 <= y <= BOARD_SIZE + 85:
                return 'pause'
        
        return 'none'
    
    def update(self):
        """Обновление состояния режима игры на время."""
        if not self.game_started or self.game_over or self.game_paused:
            return
        
        # Обновляем время текущего игрока
        current_time = time.time()
        elapsed_time = current_time - self.last_move_time
        
        # Определяем, чей ход
        side_to_move = self.engine.get_side_to_move()
        is_white_move = side_to_move == 'w'
        
        # Обновляем время
        if is_white_move:
            remaining_time = self.white_time - elapsed_time
            if remaining_time <= 0:
                self.game_over = True
                self.winner = 'black'
                self.game_over_reason = "Время истекло"
                self.feedback_message = "Время истекло! Победили черные"
                self.feedback_time = time.time()
                if self.sound_manager:
                    self.sound_manager.play_sound("capture")
        else:
            remaining_time = self.black_time - elapsed_time
            if remaining_time <= 0:
                self.game_over = True
                self.winner = 'white'
                self.game_over_reason = "Время истекло"
                self.feedback_message = "Время истекло! Победили белые"
                self.feedback_time = time.time()
                if self.sound_manager:
                    self.sound_manager.play_sound("capture")
    
    def draw(self):
        """Отрисовка режима игры на время."""
        # Обновляем состояние
        self.update()
        
        # Получаем состояние доски
        board_state = self.engine.get_board_state()
        
        # Отрисовываем доску
        self.renderer.draw(board_state)
        
        # Отрисовываем UI
        self.draw_ui()
    
    def get_game_result(self) -> Dict:
        """
        Получить результат игры.
        
        Возвращает:
            Dict: Словарь с результатом игры
        """
        return {
            'winner': self.winner,
            'reason': self.game_over_reason,
            'white_time': self.white_time,
            'black_time': self.black_time,
            'move_count': self.move_count,
            'time_control': self.time_control_key
        }
    
    def cleanup(self):
        """Очистка ресурсов."""
        if self.engine:
            self.engine.quit()
        if self.sound_manager:
            self.sound_manager.cleanup()
