#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import os
import random
import math
import queue
import threading
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.chess_engine_wrapper import ChessEngineWrapper

@dataclass
class AnimationState:
    """Состояние анимации перемещения фигуры"""
    active: bool = False
    piece: str = ''
    from_pos: Tuple[int, int] = (0, 0)
    to_pos: Tuple[int, int] = (0, 0)
    progress: float = 0.0
    duration: float = 300  # мс

class PygameChessGUI:
    def __init__(self):
        pygame.init()
        
        # Настройки экрана
        self.WIDTH = 800
        self.HEIGHT = 640
        self.BOARD_SIZE = 8
        self.SIDE_PANEL_WIDTH = 160
        self.SQUARE_SIZE = 640 // self.BOARD_SIZE
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.SELECTED_COLOR = (124, 252, 0)
        self.HIGHLIGHT_COLOR = (255, 255, 0)
        self.MOVE_HINT_COLOR = (100, 200, 100)
        self.RED = (255, 0, 0)
        self.GRAY = (128, 128, 128)
        self.PANEL_BG = (245, 245, 245)
        
        # Создание окна
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Шахматы - Многопоточная версия")
        self.clock = pygame.time.Clock()
        
        # Используем оптимизированный движок
        self.engine = ChessEngineWrapper()
        self.engine.board_state = self.engine.get_initial_board()
        self.engine.current_turn = True
        
        # Многопоточность для AI
        self.ai_thread: Optional[threading.Thread] = None
        self.ai_queue = queue.Queue()
        self.ai_result: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        self.ai_calculating = False
        self.lock = threading.Lock()
        
        # Игровое состояние
        self.selected_square: Optional[Tuple[int, int]] = None
        self.valid_moves: List[Tuple[int, int]] = []
        self.game_active = True
        self.white_turn = True
        self.move_history: List[str] = []
        self.captured_pieces: Dict[str, List[str]] = {'white': [], 'black': []}
        self.game_mode = 'computer'  # 'computer' or 'human'
        self.player_color = 'white'  # 'white' or 'black'
        self.ai_color = 'black'      # 'white' or 'black'
        
        # Превращение пешки
        self.pawn_promotion_pending = False
        self.promotion_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        
        # Анимация
        self.animation = AnimationState()
        self.last_move_highlight: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        
        # Шрифты
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 32, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
        # Загрузка ресурсов
        self.piece_images = self.load_piece_images()
        self.sounds = self.load_sounds()
        
        # Статистика
        self.game_stats = {
            'moves_count': 0,
            'captures_count': 0,
            'check_count': 0,
            'game_start_time': pygame.time.get_ticks(),
            'ai_thinking_time': 0
        }
        self.last_ai_stats = {}
        self.show_performance_stats = False  # Новый флаг для отображения статистики
        
        # Таймер для визуальной задержки (отключен по запросу)
        self.computer_move_delay = 0
        self.COMPUTER_VISUAL_DELAY = 0  # Отключено - AI ходит сразу
        self.pending_ai_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        
    def load_piece_images(self):
        """Загрузка иконок фигур"""
        import os
        pieces = {}
        
        piece_files = {
            'K': 'white_king.png', 'Q': 'white_queen.png', 'R': 'white_rook.png',
            'B': 'white_bishop.png', 'N': 'white_knight.png', 'P': 'white_pawn.png',
            'k': 'black_king.png', 'q': 'black_queen.png', 'r': 'black_rook.png',
            'b': 'black_bishop.png', 'n': 'black_knight.png', 'p': 'black_pawn.png'
        }
        
        icons_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'icons')
        
        for piece, filename in piece_files.items():
            try:
                file_path = os.path.join(icons_path, filename)
                if os.path.exists(file_path):
                    image = pygame.image.load(file_path).convert_alpha()
                    
                    # Отзеркаливаем коней (N и n)
                    if piece in ['N', 'n']:  # Белый и черный кони
                        image = pygame.transform.flip(image, True, False)  # flip horizontally
                    
                    scaled_image = pygame.transform.smoothscale(
                        image, (self.SQUARE_SIZE - 10, self.SQUARE_SIZE - 10)
                    )
                    pieces[piece] = scaled_image
                else:
                    pieces[piece] = None
            except Exception as e:
                print(f"Ошибка загрузки {filename}: {e}")
                pieces[piece] = None
        
        return pieces
    
    def load_sounds(self):
        """Загрузка звуков"""
        return {}
    
    def ai_worker(self, depth: int = 4):
        """Воркер для вычисления AI хода в отдельном потоке"""
        try:
            # Вызываем метод AI движка
            best_move = self.engine.get_best_move(depth)
            
            # Помещаем результат в очередь
            with self.lock:
                self.ai_result = best_move
                self.ai_calculating = False
                # Store stats
                self.last_ai_stats = self.engine.get_game_statistics()
        except Exception as e:
            print(f"Ошибка в AI потоке: {e}")
            with self.lock:
                self.ai_result = None
                self.ai_calculating = False
    
    def start_ai_calculation(self, depth: int = 4):
        """Запуск AI вычислений в отдельном потоке"""
        if self.ai_calculating:
            return
        
        with self.lock:
            self.ai_calculating = True
            self.ai_result = None
            # Останавливаем любые активные анимации
            self.animation.active = False
            self.animation.progress = 0.0
        
        # Создаем и запускаем поток
        self.ai_thread = threading.Thread(target=self.ai_worker, args=(depth,), daemon=True)
        self.ai_thread.start()
    
    def check_ai_result(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Проверка результата AI вычислений"""
        with self.lock:
            if self.ai_result is not None and not self.ai_calculating:
                result = self.ai_result
                self.ai_result = None
                return result
        return None
    
    def update_adaptive_sizes(self):
        """Обновление адаптивных размеров при изменении окна"""
        pass  # Не используется в фиксированном режиме
    
    def draw_static_board(self):
        """Отрисовка статической шахматной доски без анимаций и подсветок"""
        # Полностью статическая отрисовка - никаких обновлений во время AI расчетов
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                
                # Базовая доска без подсветок во время AI расчетов
                rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                 self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                
                # Отрисовка фигур (без анимации)
                piece = self.engine.board_state[row][col]
                if piece != '.':
                    self.draw_piece_static(piece, rect)
    
    def draw_piece_static(self, piece: str, rect: pygame.Rect):
        """Статическая отрисовка фигуры без эффектов"""
        if piece in self.piece_images and self.piece_images[piece] is not None:
            piece_surface = self.piece_images[piece]
            piece_rect = piece_surface.get_rect(center=rect.center)
            # Отключаем любые визуальные эффекты
            self.screen.blit(piece_surface, piece_rect)
        else:
            # Резервный вариант
            unicode_symbols = {
                'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
                'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
            }
            symbol = unicode_symbols.get(piece, piece)
            text_color = self.BLACK if piece.isupper() else self.RED
            text = self.font.render(symbol, True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def draw_board(self):
        """Отрисовка шахматной доски"""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                
                # Подсветка короля под шахом
                piece = self.engine.board_state[row][col]
                if piece.lower() == 'k':
                    king_is_white = piece.isupper()
                    if self.is_king_in_check(king_is_white):
                        color = (255, 100, 100)  # Красная подсветка
                
                # Подсветка последнего хода
                if self.last_move_highlight:
                    from_pos, to_pos = self.last_move_highlight
                    if (row, col) in [from_pos, to_pos]:
                        color = tuple(min(c + 30, 255) for c in color)
                
                # Выделение выбранной клетки
                if self.selected_square == (row, col):
                    color = self.SELECTED_COLOR
                
                rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE,
                                 self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Подсветка возможных ходов
                if (row, col) in self.valid_moves:
                    center = rect.center
                    target_piece = self.engine.board_state[row][col]
                    if target_piece != '.':
                        # Возможное взятие - кольцо
                        pygame.draw.circle(self.screen, self.MOVE_HINT_COLOR, center,
                                         self.SQUARE_SIZE // 2 - 5, 4)
                    else:
                        # Обычный ход - точка
                        pygame.draw.circle(self.screen, self.MOVE_HINT_COLOR, center, 10)
                
                # Рамка клетки
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                
                # Отрисовка фигуры (если не анимируется)
                if not (self.animation.active and (row, col) == self.animation.from_pos):
                    piece = self.engine.board_state[row][col]
                    if piece != '.':
                        self.draw_piece(piece, rect)
        
        # Отрисовка анимируемой фигуры
        if self.animation.active and not self.ai_calculating:
            self.draw_animated_piece()
    
    def draw_piece(self, piece: str, rect: pygame.Rect):
        """Отрисовка фигуры"""
        if piece in self.piece_images and self.piece_images[piece] is not None:
            piece_surface = self.piece_images[piece]
            piece_rect = piece_surface.get_rect(center=rect.center)
            self.screen.blit(piece_surface, piece_rect)
        else:
            # Резервный вариант
            unicode_symbols = {
                'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
                'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
            }
            symbol = unicode_symbols.get(piece, piece)
            text_color = self.BLACK if piece.isupper() else self.RED
            text = self.font.render(symbol, True, text_color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def draw_animated_piece(self):
        """Отрисовка анимируемой фигуры"""
        if not self.animation.active:
            return
        
        from_row, from_col = self.animation.from_pos
        to_row, to_col = self.animation.to_pos
        
        # Интерполяция позиции
        start_x = from_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        start_y = from_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        end_x = to_col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        end_y = to_row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        
        t = self.animation.progress
        # Easing function для плавности
        t_eased = 1 - (1 - t) ** 3  # Cubic ease-out
        
        current_x = start_x + (end_x - start_x) * t_eased
        current_y = start_y + (end_y - start_y) * t_eased
        
        piece = self.animation.piece
        if piece in self.piece_images and self.piece_images[piece] is not None:
            piece_surface = self.piece_images[piece]
            piece_rect = piece_surface.get_rect(center=(current_x, current_y))
            # Тень для глубины
            shadow = pygame.Surface(piece_surface.get_size(), pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 50))
            shadow_rect = shadow.get_rect(center=(current_x + 3, current_y + 3))
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(piece_surface, piece_rect)
    
    def draw_thinking_indicator(self, x: int, y: int) -> int:
        """Анимированный индикатор обдумывания AI"""
        if not self.ai_calculating:
            return y
        
        # Во время AI расчетов показываем статический индикатор без анимации
        thinking_text = self.small_font.render("AI думает", True, self.GRAY)
        self.screen.blit(thinking_text, (x, y))
        
        # Статические точки вместо анимированных
        dots_text = self.small_font.render("...", True, self.GRAY)
        self.screen.blit(dots_text, (x + 80, y))
        
        return y + 25
    
    def draw_coordinates_static(self):
        """Статическая отрисовка координат доски"""
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i, letter in enumerate(letters):
            text = self.small_font.render(letter, True, self.BLACK)
            x = i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            self.screen.blit(text, (x - text.get_width()//2, self.HEIGHT - 20))
        
        for i in range(8):
            text = self.small_font.render(str(8-i), True, self.BLACK)
            y = i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            self.screen.blit(text, (5, y - text.get_height()//2))
    
    def draw_coordinates(self):
        """Отрисовка координат доски"""
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        for i, letter in enumerate(letters):
            text = self.small_font.render(letter, True, self.BLACK)
            x = i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            self.screen.blit(text, (x - text.get_width()//2, self.HEIGHT - 20))
        
        for i in range(8):
            text = self.small_font.render(str(8-i), True, self.BLACK)
            y = i * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            self.screen.blit(text, (5, y - text.get_height()//2))
    
    def draw_promotion_dialog(self) -> Dict[str, pygame.Rect]:
        """Отрисовка диалога выбора фигуры при превращении пешки"""
        if not self.pawn_promotion_pending:
            return {}
        
        # Полупрозрачный фон
        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        # Диалоговое окно
        dialog_width = 400
        dialog_height = 250
        dialog_x = (self.WIDTH - dialog_width) // 2
        dialog_y = (self.HEIGHT - dialog_height) // 2
        
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(self.screen, self.WHITE, dialog_rect)
        pygame.draw.rect(self.screen, self.BLACK, dialog_rect, 3)
        
        # Заголовок
        title = self.big_font.render("Выберите фигуру", True, self.BLACK)
        title_rect = title.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 40))
        self.screen.blit(title, title_rect)
        
        # Фигуры для выбора
        pieces = ['Q', 'R', 'B', 'N']
        piece_names = {'Ферзь', 'Ладья', 'Слон', 'Конь'}
        piece_rects = {}
        
        box_size = 80
        spacing = 20
        total_width = len(pieces) * box_size + (len(pieces) - 1) * spacing
        start_x = dialog_x + (dialog_width - total_width) // 2
        start_y = dialog_y + 100
        
        for i, (piece, name) in enumerate(zip(pieces, ['Ферзь', 'Ладья', 'Слон', 'Конь'])):
            x = start_x + i * (box_size + spacing)
            rect = pygame.Rect(x, start_y, box_size, box_size)
            
            # Коробка
            pygame.draw.rect(self.screen, self.LIGHT_SQUARE, rect)
            pygame.draw.rect(self.screen, self.BLACK, rect, 2)
            
            # Фигура
            display_piece = piece if self.white_turn else piece.lower()
            if display_piece in self.piece_images and self.piece_images[display_piece]:
                img = pygame.transform.scale(self.piece_images[display_piece], (60, 60))
                img_rect = img.get_rect(center=rect.center)
                self.screen.blit(img, img_rect)
            else:
                symbols = {'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘',
                          'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞'}
                symbol = symbols.get(display_piece, piece)
                text = self.big_font.render(symbol, True, self.BLACK)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)
            
            # Название
            name_text = self.small_font.render(name, True, self.BLACK)
            name_rect = name_text.get_rect(center=(rect.centerx, rect.bottom + 15))
            self.screen.blit(name_text, name_rect)
            
            piece_rects[piece] = rect
        
        return piece_rects
    
    def draw_side_panel_minimal_frozen(self):
        """Полностью замороженная боковая панель без ИИ индикатора"""
        # Абсолютно статическая панель - никаких изменений во время AI расчетов
        panel_rect = pygame.Rect(640, 0, self.SIDE_PANEL_WIDTH, self.HEIGHT)
        pygame.draw.rect(self.screen, self.PANEL_BG, panel_rect)
        pygame.draw.line(self.screen, self.BLACK, (640, 0), (640, self.HEIGHT), 2)
        
        y_offset = 20
        
        # Заголовок
        title = self.big_font.render("Инфо", True, self.BLACK)
        self.screen.blit(title, (650, y_offset))
        y_offset += 50
        
        # Текущий игрок (замороженный)
        player_text = "Белые" if self.white_turn else "Черные"
        turn_text = self.font.render(f"Ход: {player_text}", True, self.BLACK)
        self.screen.blit(turn_text, (650, y_offset))
        y_offset += 30
        
        # Информация об игроках
        if self.game_mode == 'computer':
            player_color_text = "Вы: " + ("Белые" if self.player_color == 'white' else "Черные")
            ai_color_text = "AI: " + ("Белые" if self.ai_color == 'white' else "Черные")
            
            player_render = self.small_font.render(player_color_text, True, self.BLACK)
            ai_render = self.small_font.render(ai_color_text, True, self.BLACK)
            
            self.screen.blit(player_render, (650, y_offset))
            y_offset += 25
            self.screen.blit(ai_render, (650, y_offset))
            y_offset += 35
        
        # НЕ отображаем индикатор AI во время расчетов (полная заморозка)
        # Только режим игры
        mode_text = "vs AI" if self.game_mode == 'computer' else "2 игрока"
        mode_render = self.small_font.render(mode_text, True, self.GRAY)
        self.screen.blit(mode_render, (650, y_offset))
        
        # Только базовые кнопки
        self.draw_control_buttons_simple_frozen()
    
    def draw_side_panel_minimal(self):
        """Минимальная отрисовка боковой панели во время AI расчетов"""
        # Полностью статическая панель без анимаций
        panel_rect = pygame.Rect(640, 0, self.SIDE_PANEL_WIDTH, self.HEIGHT)
        pygame.draw.rect(self.screen, self.PANEL_BG, panel_rect)
        pygame.draw.line(self.screen, self.BLACK, (640, 0), (640, self.HEIGHT), 2)
        
        y_offset = 20
        
        # Заголовок
        title = self.big_font.render("Инфо", True, self.BLACK)
        self.screen.blit(title, (650, y_offset))
        y_offset += 50
        
        # Текущий игрок (без подсветки шаха во время AI расчетов)
        player_text = "Белые" if self.white_turn else "Черные"
        turn_text = self.font.render(f"Ход: {player_text}", True, self.BLACK)
        self.screen.blit(turn_text, (650, y_offset))
        y_offset += 30
        
        # Информация об игроках
        if self.game_mode == 'computer':
            player_color_text = "Вы: " + ("Белые" if self.player_color == 'white' else "Черные")
            ai_color_text = "AI: " + ("Белые" if self.ai_color == 'white' else "Черные")
            
            player_render = self.small_font.render(player_color_text, True, self.BLACK)
            ai_render = self.small_font.render(ai_color_text, True, self.BLACK)
            
            self.screen.blit(player_render, (650, y_offset))
            y_offset += 25
            self.screen.blit(ai_render, (650, y_offset))
            y_offset += 35
        
        # Индикатор обдумывания AI (статический)
        if self.ai_calculating:
            y_offset = self.draw_thinking_indicator_static(650, y_offset)
        
        # Режим игры
        mode_text = "vs AI" if self.game_mode == 'computer' else "2 игрока"
        mode_render = self.small_font.render(mode_text, True, self.GRAY)
        self.screen.blit(mode_render, (650, y_offset))
        
        # Только базовые кнопки без сложных элементов
        self.draw_control_buttons_simple()
    
    def draw_thinking_indicator_static(self, x: int, y: int) -> int:
        """Статический индикатор обдумывания AI без анимации"""
        if not self.ai_calculating:
            return y
        
        # Полностью статический текст без анимации
        thinking_text = self.small_font.render("AI думает...", True, self.GRAY)
        self.screen.blit(thinking_text, (x, y))
        
        return y + 25
    
    def draw_side_panel(self):
        """Отрисовка боковой панели"""
        panel_rect = pygame.Rect(640, 0, self.SIDE_PANEL_WIDTH, self.HEIGHT)
        pygame.draw.rect(self.screen, self.PANEL_BG, panel_rect)
        pygame.draw.line(self.screen, self.BLACK, (640, 0), (640, self.HEIGHT), 2)
        
        y_offset = 20
        
        # Заголовок
        title = self.big_font.render("Инфо", True, self.BLACK)
        self.screen.blit(title, (650, y_offset))
        y_offset += 50
        
        # Текущий игрок
        player_text = "Белые" if self.white_turn else "Черные"
        king_in_check = self.is_king_in_check(self.white_turn)
        
        if king_in_check:
            status = f"{player_text} ⚠"
            color = self.RED
        else:
            status = player_text
            color = self.BLACK
        
        turn_text = self.font.render(f"Ход: {status}", True, color)
        self.screen.blit(turn_text, (650, y_offset))
        y_offset += 30
        
        # Информация об игроках
        if self.game_mode == 'computer':
            player_color_text = "Вы: " + ("Белые" if self.player_color == 'white' else "Черные")
            ai_color_text = "AI: " + ("Белые" if self.ai_color == 'white' else "Черные")
            
            player_render = self.small_font.render(player_color_text, True, self.BLACK)
            ai_render = self.small_font.render(ai_color_text, True, self.BLACK)
            
            self.screen.blit(player_render, (650, y_offset))
            y_offset += 25
            self.screen.blit(ai_render, (650, y_offset))
            y_offset += 35
        
        # Индикатор обдумывания AI
        if self.ai_calculating:
            y_offset = self.draw_thinking_indicator(650, y_offset)
        elif self.last_ai_stats:
            nodes = self.last_ai_stats.get('ai_nodes', 0)
            tt_hits = self.last_ai_stats.get('ai_tt_hits', 0)
            if nodes > 0:
                stats_text = self.small_font.render(f"AI: {nodes} узлов", True, self.GRAY)
                self.screen.blit(stats_text, (650, y_offset))
                y_offset += 20
                tt_text = self.small_font.render(f"TT Hits: {tt_hits}", True, self.GRAY)
                self.screen.blit(tt_text, (650, y_offset))
                y_offset += 25
        
        # Режим игры
        mode_text = "vs AI" if self.game_mode == 'computer' else "2 игрока"
        mode_render = self.small_font.render(mode_text, True, self.GRAY)
        self.screen.blit(mode_render, (650, y_offset))
        y_offset += 35
        
        # Захваченные фигуры
        y_offset = self.draw_captured_pieces(650, y_offset)
        y_offset += 15
        
        # История ходов
        y_offset = self.draw_move_history(650, y_offset)
        
        # Кнопки управления
        self.draw_control_buttons()
    
    def draw_captured_pieces(self, x: int, y: int) -> int:
        """Отрисовка захваченных фигур"""
        cap_title = self.small_font.render("Захвачено:", True, self.BLACK)
        self.screen.blit(cap_title, (x, y))
        y += 25
        
        # Символы фигур для отображения
        piece_symbols = {'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙'}
        
        white_captured = self.captured_pieces['white']
        if white_captured:
            symbols = ''.join(piece_symbols.get(p, p) for p in white_captured)
            white_text = self.small_font.render(f"⬜: {symbols}", True, self.BLACK)
            self.screen.blit(white_text, (x, y))
            y += 20
        
        black_captured = self.captured_pieces['black']
        if black_captured:
            symbols = ''.join(piece_symbols.get(p, p) for p in black_captured)
            black_text = self.small_font.render(f"⬛: {symbols}", True, self.BLACK)
            self.screen.blit(black_text, (x, y))
            y += 20
        
        return y
    
    def draw_move_history(self, x: int, y: int) -> int:
        """Отрисовка истории ходов"""
        history_title = self.small_font.render("Ходы:", True, self.BLACK)
        self.screen.blit(history_title, (x, y))
        y += 25
        
        start_index = max(0, len(self.move_history) - 8)
        for i, move in enumerate(self.move_history[start_index:], start_index):
            move_text = self.small_font.render(f"{i+1}. {move}", True, self.BLACK)
            self.screen.blit(move_text, (x, y))
            y += 20
        
        return y
    
    def draw_control_buttons_simple_frozen(self) -> Dict[str, pygame.Rect]:
        """Полностью замороженные кнопки управления без обработки событий"""
        # Абсолютно статические кнопки - никаких изменений
        buttons = {}
        button_y = self.HEIGHT - 180  # Выше, чтобы поместилось меньше кнопок
        
        # Новая игра (замороженная)
        new_game_btn = pygame.Rect(650, button_y, 140, 35)
        pygame.draw.rect(self.screen, (70, 130, 180), new_game_btn)
        pygame.draw.rect(self.screen, self.BLACK, new_game_btn, 2)
        text = self.small_font.render("Новая игра", True, self.WHITE)
        self.screen.blit(text, text.get_rect(center=new_game_btn.center))
        buttons['new_game'] = new_game_btn
        
        # Выход (замороженная)
        button_y += 40
        exit_btn = pygame.Rect(650, button_y, 140, 35)
        pygame.draw.rect(self.screen, (169, 169, 169), exit_btn)
        pygame.draw.rect(self.screen, self.BLACK, exit_btn, 2)
        text = self.small_font.render("Выход", True, self.BLACK)
        self.screen.blit(text, text.get_rect(center=exit_btn.center))
        buttons['exit'] = exit_btn
        
        return buttons
    
    def draw_control_buttons_simple(self) -> Dict[str, pygame.Rect]:
        """Упрощенная отрисовка кнопок управления во время AI расчетов"""
        # Полностью статические кнопки без hover-эффектов
        buttons = {}
        button_y = self.HEIGHT - 180  # Выше, чтобы поместилось меньше кнопок
        
        # Новая игра
        new_game_btn = pygame.Rect(650, button_y, 140, 35)
        pygame.draw.rect(self.screen, (70, 130, 180), new_game_btn)
        pygame.draw.rect(self.screen, self.BLACK, new_game_btn, 2)
        text = self.small_font.render("Новая игра", True, self.WHITE)
        self.screen.blit(text, text.get_rect(center=new_game_btn.center))
        buttons['new_game'] = new_game_btn
        
        # Выход
        button_y += 40
        exit_btn = pygame.Rect(650, button_y, 140, 35)
        pygame.draw.rect(self.screen, (169, 169, 169), exit_btn)
        pygame.draw.rect(self.screen, self.BLACK, exit_btn, 2)
        text = self.small_font.render("Выход", True, self.BLACK)
        self.screen.blit(text, text.get_rect(center=exit_btn.center))
        buttons['exit'] = exit_btn
        
        return buttons
    
    def draw_control_buttons(self) -> Dict[str, pygame.Rect]:
        """Отрисовка кнопок управления"""
        buttons = {}
        button_y = self.HEIGHT - 260  # Сдвигаем выше, чтобы влезли новые кнопки
        
        # Новая игра
        new_game_btn = pygame.Rect(650, button_y, 140, 35)
        pygame.draw.rect(self.screen, (70, 130, 180), new_game_btn)
        pygame.draw.rect(self.screen, self.BLACK, new_game_btn, 2)
        text = self.small_font.render("Новая игра", True, self.WHITE)
        self.screen.blit(text, text.get_rect(center=new_game_btn.center))
        buttons['new_game'] = new_game_btn
        
        # Смена режима
        button_y += 40
        mode_btn = pygame.Rect(650, button_y, 140, 35)
        mode_color = (220, 20, 60) if self.game_mode == 'computer' else (50, 205, 50)
        pygame.draw.rect(self.screen, mode_color, mode_btn)
        pygame.draw.rect(self.screen, self.BLACK, mode_btn, 2)
        mode_text = "2 игрока" if self.game_mode == 'computer' else "vs AI"
        text = self.small_font.render(mode_text, True, self.WHITE)
        self.screen.blit(text, text.get_rect(center=mode_btn.center))
        buttons['mode'] = mode_btn
        
        # Выбор цвета
        button_y += 40
        color_btn = pygame.Rect(650, button_y, 140, 35)
        color_color = (100, 100, 200) if self.game_mode == 'computer' else (200, 200, 200)
        pygame.draw.rect(self.screen, color_color, color_btn)
        pygame.draw.rect(self.screen, self.BLACK, color_btn, 2)
        color_text = "Вы: " + ("Бел" if self.player_color == 'white' else "Чер") if self.game_mode == 'computer' else "---"
        text = self.small_font.render(color_text, True, self.WHITE if self.game_mode == 'computer' else self.GRAY)
        self.screen.blit(text, text.get_rect(center=color_btn.center))
        buttons['color'] = color_btn

        # Сохранить
        button_y += 40
        save_btn = pygame.Rect(650, button_y, 140, 35)
        pygame.draw.rect(self.screen, (60, 179, 113), save_btn)
        pygame.draw.rect(self.screen, self.BLACK, save_btn, 2)
        text = self.small_font.render("Сохранить", True, self.WHITE)
        self.screen.blit(text, text.get_rect(center=save_btn.center))
        buttons['save'] = save_btn

        # Загрузить
        button_y += 40
        load_btn = pygame.Rect(650, button_y, 140, 35)
        pygame.draw.rect(self.screen, (218, 165, 32), load_btn)
        pygame.draw.rect(self.screen, self.BLACK, load_btn, 2)
        text = self.small_font.render("Загрузить", True, self.WHITE)
        self.screen.blit(text, text.get_rect(center=load_btn.center))
        buttons['load'] = load_btn
        
        # Выход
        button_y += 40
        exit_btn = pygame.Rect(650, button_y, 140, 35)
        pygame.draw.rect(self.screen, (169, 169, 169), exit_btn)
        pygame.draw.rect(self.screen, self.BLACK, exit_btn, 2)
        text = self.small_font.render("Выход", True, self.BLACK)
        self.screen.blit(text, text.get_rect(center=exit_btn.center))
        buttons['exit'] = exit_btn
        
        # Статистика (новая кнопка)
        button_y += 40
        stats_btn = pygame.Rect(650, button_y, 140, 30)
        stats_color = (30, 144, 255) if self.show_performance_stats else (180, 180, 180)
        pygame.draw.rect(self.screen, stats_color, stats_btn)
        pygame.draw.rect(self.screen, self.BLACK, stats_btn, 2)
        text = self.small_font.render("Статистика", True, self.WHITE if self.show_performance_stats else self.BLACK)
        self.screen.blit(text, text.get_rect(center=stats_btn.center))
        buttons['stats'] = stats_btn
        
        return buttons
    
    def get_square_from_mouse(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Преобразование координат мыши в координаты доски"""
        x, y = pos
        if x >= 640 or y >= 640:
            return None
        col = x // self.SQUARE_SIZE
        row = y // self.SQUARE_SIZE
        return (row, col) if 0 <= row < 8 and 0 <= col < 8 else None
    
    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка корректности хода"""
        return self.engine.is_valid_move(from_pos, to_pos)
    
    def is_king_in_check(self, is_white: bool) -> bool:
        """Проверка шаха"""
        return self.engine.is_king_in_check(is_white)
    
    def is_checkmate(self) -> bool:
        """Проверка мата"""
        return self.engine.is_checkmate(self.white_turn)
    
    def is_stalemate(self) -> bool:
        """Проверка пата"""
        return self.engine.is_stalemate(self.white_turn)
    
    def get_valid_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Получение допустимых ходов"""
        valid_moves = []
        from_row, from_col = pos
        piece = self.engine.board_state[from_row][from_col]
        
        if piece == '.':
            return valid_moves
        
        king_color = piece.isupper()
        
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(pos, (row, col)):
                    if not self.engine.would_still_be_in_check(pos, (row, col), king_color):
                        valid_moves.append((row, col))
        
        return valid_moves
    
    def start_move_animation(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]):
        """Запуск анимации хода"""
        from_row, from_col = from_pos
        piece = self.engine.board_state[from_row][from_col]
        
        self.animation.active = True
        self.animation.piece = piece
        self.animation.from_pos = from_pos
        self.animation.to_pos = to_pos
        self.animation.progress = 0.0
    
    def update_animation(self, delta_time: int) -> bool:
        """Обновление анимации"""
        # Во время AI расчетов анимации не обновляем
        if self.ai_calculating:
            return False
            
        if not self.animation.active:
            return False
        
        self.animation.progress += delta_time / self.animation.duration
        
        if self.animation.progress >= 1.0:
            self.animation.active = False
            self.animation.progress = 1.0
            return True
        
        return False
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], promotion_piece: str = 'Q') -> bool:
        """Выполнение хода"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Проверяем, чья очередь хода
        piece = self.engine.board_state[from_row][from_col]
        is_white_piece = piece.isupper()
        
        if (is_white_piece and not self.white_turn) or (not is_white_piece and self.white_turn):
            print(f"Неправильная очередь хода! Попытка хода {piece} когда очередь {'белых' if self.white_turn else 'черных'}")
            return False
        
        # Проверка превращения пешки
        is_pawn_promotion = (piece.lower() == 'p' and 
                            ((is_white_piece and to_row == 0) or 
                             (not is_white_piece and to_row == 7)))
        
        # Если превращение пешки и не указана фигура, показываем диалог
        if is_pawn_promotion and not self.pawn_promotion_pending:
            self.pawn_promotion_pending = True
            self.promotion_move = (from_pos, to_pos)
            return False  # Ожидаем выбора фигуры
        
        # Сохранение захваченной фигуры
        captured = self.engine.board_state[to_row][to_col]
        
        # Запуск анимации (только если не во время AI расчетов)
        if not self.ai_calculating:
            self.start_move_animation(from_pos, to_pos)
        
        # Выполнение хода в движке
        if not self.engine.make_move(from_pos, to_pos):
            if not self.ai_calculating:
                self.animation.active = False
            return False
        
        # Превращение пешки
        if is_pawn_promotion:
            promo_piece = promotion_piece.upper() if is_white_piece else promotion_piece.lower()
            self.engine.board_state[to_row][to_col] = promo_piece
            self.pawn_promotion_pending = False
            self.promotion_move = None
        
        # Обновление истории
        piece = self.engine.board_state[to_row][to_col]
        from_square = chr(ord('a') + from_col) + str(8 - from_row)
        to_square = chr(ord('a') + to_col) + str(8 - to_row)
        
        piece_symbol = '' if piece.lower() == 'p' else piece.upper()
        capture_symbol = 'x' if captured != '.' else '-'
        
        move_notation = f"{piece_symbol}{from_square}{capture_symbol}{to_square}"
        if is_pawn_promotion:
            move_notation += f"={promotion_piece.upper()}"
        self.move_history.append(move_notation)
        
        # Обновление захваченных фигур
        if captured != '.':
            captured_color = 'white' if captured.isupper() else 'black'
            self.captured_pieces[captured_color].append(captured.upper())
            self.game_stats['captures_count'] += 1
        
        # Обновление статистики
        self.game_stats['moves_count'] += 1
        if self.is_king_in_check(not self.white_turn):
            self.game_stats['check_count'] += 1
        
        # Подсветка последнего хода (только если не во время AI расчетов)
        if not self.ai_calculating:
            self.last_move_highlight = (from_pos, to_pos)
        
        # Смена хода
        self.white_turn = not self.white_turn
        self.engine.current_turn = self.white_turn
        self.selected_square = None
        self.valid_moves = []
        
        # Проверка окончания игры
        if self.is_checkmate():
            self.game_active = False
        elif self.is_stalemate():
            self.game_active = False
        
        return True
    
    def handle_button_click(self, pos: Tuple[int, int]) -> bool:
        """Обработка кликов по кнопкам"""
        buttons = self.draw_control_buttons()
        
        if buttons['new_game'].collidepoint(pos):
            self.new_game()
        elif buttons['mode'].collidepoint(pos):
            self.toggle_game_mode()
        elif buttons['color'].collidepoint(pos):
            self.toggle_player_color()
        elif buttons['save'].collidepoint(pos):
            self.save_game()
        elif buttons['load'].collidepoint(pos):
            self.load_game()
        elif buttons.get('stats') and buttons['stats'].collidepoint(pos):
            self.show_performance_stats = not self.show_performance_stats
        elif buttons['exit'].collidepoint(pos):
            return False
        
        return True

    def save_game(self, filename: str = "pygame_save.json"):
        """Сохранение игры"""
        if self.engine.save_game(filename):
            print(f"Игра сохранена в {filename}")
        else:
            print("Ошибка сохранения")

    def load_game(self, filename: str = "pygame_save.json"):
        """Загрузка игры"""
        if self.engine.load_game(filename):
            self.white_turn = self.engine.current_turn
            self.move_history = self.engine.move_history
            self.captured_pieces = self.engine.captured_pieces
            self.last_move_highlight = None
            self.selected_square = None
            self.valid_moves = []
            print(f"Игра загружена из {filename}")
        else:
            print("Ошибка загрузки")
    
    def toggle_game_mode(self):
        """Переключение режима игры"""
        self.game_mode = 'human' if self.game_mode == 'computer' else 'computer'
        self.new_game()
    
    def toggle_player_color(self):
        """Переключение цвета игрока (только для режима vs AI)"""
        if self.game_mode == 'computer':
            self.player_color = 'black' if self.player_color == 'white' else 'white'
            self.ai_color = 'white' if self.player_color == 'black' else 'black'
            self.new_game()
    
    def handle_square_click(self, square: Tuple[int, int]):
        """Обработка клика по клетке"""
        if self.animation.active or self.ai_calculating:
            return
        
        # В режиме vs AI проверяем, что игрок ходит своими фигурами
        if self.game_mode == 'computer':
            if ((self.player_color == 'white' and not self.white_turn) or 
                (self.player_color == 'black' and self.white_turn)):
                return  # Не наш ход
        
        row, col = square
        piece = self.engine.board_state[row][col]
        
        if self.selected_square is None:
            if piece != '.':
                is_white_piece = piece.isupper()
                if (is_white_piece and self.white_turn) or (not is_white_piece and not self.white_turn):
                    self.selected_square = square
                    self.valid_moves = self.get_valid_moves(square)
        else:
            if square in self.valid_moves:
                self.make_move(self.selected_square, square)
            elif square == self.selected_square:
                self.selected_square = None
                self.valid_moves = []
            elif piece != '.':
                is_white_piece = piece.isupper()
                if (is_white_piece and self.white_turn) or (not is_white_piece and not self.white_turn):
                    self.selected_square = square
                    self.valid_moves = self.get_valid_moves(square)
                else:
                    self.selected_square = None
                    self.valid_moves = []
    
    def new_game(self):
        """Начало новой игры"""
        # Останавливаем AI поток если он работает
        if self.ai_thread and self.ai_thread.is_alive():
            with self.lock:
                self.ai_calculating = False
        
        self.engine.board_state = self.engine.get_initial_board()
        self.engine.current_turn = True
        self.selected_square = None
        self.valid_moves = []
        self.game_active = True
        self.white_turn = True
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.last_move_highlight = None
        self.animation.active = False
        self.ai_calculating = False
        self.ai_result = None
        self.pending_ai_move = None
        self.computer_move_delay = 0
        self.game_stats = {
            'moves_count': 0,
            'captures_count': 0,
            'check_count': 0,
            'game_start_time': pygame.time.get_ticks(),
            'ai_thinking_time': 0
        }
        
        # В режиме vs AI запускаем AI, если он должен ходить первым
        if (self.game_mode == 'computer' and 
            self.ai_color == 'white' and 
            not self.animation.active):
            pygame.time.set_timer(pygame.USEREVENT, 500)  # Задержка перед первым ходом AI
    
    def handle_events(self) -> bool:
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                
                # Обработка диалога превращения пешки
                if self.pawn_promotion_pending:
                    piece_rects = self.draw_promotion_dialog()
                    for piece, rect in piece_rects.items():
                        if rect.collidepoint(pos):
                            # Выполняем ход с выбранной фигурой
                            if self.promotion_move:
                                from_pos, to_pos = self.promotion_move
                                self.make_move(from_pos, to_pos, piece)
                            return True
                
                if pos[0] >= 640:
                    return self.handle_button_click(pos)
                elif self.game_active:
                    square = self.get_square_from_mouse(pos)
                    if square:
                        self.handle_square_click(square)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    self.new_game()
                elif event.key == pygame.K_m:
                    self.toggle_game_mode()
                elif event.key == pygame.K_c:
                    self.toggle_player_color()
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def draw(self):
        """Основная отрисовка"""
        # Если AI считает, показываем минимальную отрисовку без анимаций
        if self.ai_calculating:
            # Абсолютно статическая отрисовка без каких-либо изменений
            self.screen.fill(self.WHITE)
            self.draw_static_board()  # Только статическая доска
            self.draw_coordinates_static()  # Статические координаты
            self.draw_side_panel_minimal_frozen()  # Замороженная боковая панель
            pygame.display.flip()
            return
        
        # Нормальная отрисовка когда AI не считает
        self.screen.fill(self.WHITE)
        self.draw_board()
        self.draw_coordinates()
        self.draw_side_panel()
        
        # Диалог превращения пешки
        if self.pawn_promotion_pending:
            self.draw_promotion_dialog()
        
        # Статистика производительности
        if self.show_performance_stats:
            self.draw_performance_stats()
        
        # Сообщение о завершении игры
        if not self.game_active:
            overlay = pygame.Surface((640, 640), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            if self.is_checkmate():
                winner = "Черные" if self.white_turn else "Белые"
                message = f"Мат! Победа: {winner}"
            else:
                message = "Пат! Ничья"
            
            text = self.big_font.render(message, True, self.WHITE)
            text_rect = text.get_rect(center=(320, 320))
            self.screen.blit(text, text_rect)
        
        pygame.display.flip()
    
    def draw_performance_stats(self):
        """Отрисовка статистики производительности"""
        # Получаем статистику из движка
        stats = self.engine.get_game_statistics()
        
        # Полупрозрачное окно
        panel_width = 300
        panel_height = 250
        panel_x = (640 - panel_width) // 2
        panel_y = 50
        
        # Фон
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((50, 50, 50, 230))
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        # Рамка
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        (panel_x, panel_y, panel_width, panel_height), 2)
        
        # Заголовок
        y = panel_y + 10
        title = self.font.render("Статистика производительности", True, (255, 255, 255))
        self.screen.blit(title, (panel_x + 10, y))
        y += 35
        
        # Основная статистика
        cache_stats = stats.get('cache_size', {})
        perf_metrics = stats.get('performance_metrics', {})
        
        info_lines = [
            f"Кэш валидации: {cache_stats.get('move_validation', 0)}",
            f"Кэш шахов: {cache_stats.get('king_check', 0)}",
            f"Попадания: {stats.get('cache_hits', 0)}",
            f"Промахи: {stats.get('cache_misses', 0)}",
            f"Время проверки мата: {perf_metrics.get('checkmate_detection_time', 0):.4f}s",
            f"Оценок позиций: {stats.get('position_evaluations', 0)}"
        ]
        
        for line in info_lines:
            text = self.small_font.render(line, True, (220, 220, 220))
            self.screen.blit(text, (panel_x + 15, y))
            y += 25
        
        # Подсказка
        hint = self.small_font.render("Нажмите кнопку еще раз для закрытия", True, (180, 180, 180))
        self.screen.blit(hint, (panel_x + 10, panel_y + panel_height - 25))
    
    def run(self):
        """Основной цикл игры с многопоточным AI"""
        running = True
        
        while running:
            delta_time = self.clock.tick(60)
            running = self.handle_events()
            
            # Обновление анимации (только если не во время AI расчетов)
            if self.animation.active and not self.ai_calculating:
                self.update_animation(delta_time)
            
            # Логика AI хода
            if (self.game_mode == 'computer' and 
                ((self.ai_color == 'white' and self.white_turn) or 
                 (self.ai_color == 'black' and not self.white_turn)) and
                self.game_active and not self.animation.active):
                
                # Проверяем результат AI
                ai_move = self.check_ai_result()
                
                if ai_move is not None:
                    # AI закончил вычисления, выполняем ход
                    from_pos, to_pos = ai_move
                    self.make_move(from_pos, to_pos)
                elif not self.ai_calculating:
                    # Запускаем AI вычисления с меньшей глубиной
                    ai_start_time = pygame.time.get_ticks()
                    self.start_ai_calculation(depth=2)
            
            # Отрисовка (только если не во время AI расчетов или с минимальной отрисовкой)
            self.draw()
        
        # Cleanup
        if self.ai_thread and self.ai_thread.is_alive():
            with self.lock:
                self.ai_calculating = False
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PygameChessGUI()
    game.run()