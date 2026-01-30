import pygame
import sys
import threading
import queue
import time
import random
import math
from typing import List, Tuple, Optional
from chess_engine_wrapper import advanced_engine

class ProChessGUI:
    def __init__(self):
        pygame.init()
        
        # Используем продвинутый движок
        self.engine = advanced_engine
        self.engine.board_state = self.engine.get_initial_board()
        self.engine.current_turn = True
        
        # Многопоточность
        self.ai_thread = None
        self.ai_queue = queue.Queue()
        self.ai_result = None
        self.ai_calculating = False
        self.lock = threading.Lock()
        
        # Настройки экрана
        self.WIDTH = 900
        self.HEIGHT = 640
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = 640 // self.BOARD_SIZE
        self.SIDE_PANEL_WIDTH = 260
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.SELECTED_COLOR = (124, 252, 0)
        self.HIGHLIGHT_COLOR = (255, 255, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 100, 255)
        self.GRAY = (128, 128, 128)
        self.PANEL_BG = (245, 245, 245)
        
        # Создание окна
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Профессиональные шахматы v2.0")
        self.clock = pygame.time.Clock()
        
        # Игровое состояние
        self.selected_square = None
        self.valid_moves = []
        self.game_active = True
        self.white_turn = True
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.game_mode = 'computer'
        self.promotion_pending = None  # Для промоции пешки
        
        # Шрифты
        self.font = pygame.font.SysFont('Arial', 20)
        self.big_font = pygame.font.SysFont('Arial', 28, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        # Загрузка иконок
        self.piece_images = self.load_piece_images()
        
        # Статистика
        self.game_stats = {
            'moves_count': 0,
            'captures_count': 0,
            'check_count': 0,
            'castling_count': 0,
            'en_passant_count': 0,
            'promotion_count': 0,
            'game_start_time': pygame.time.get_ticks(),
            'ai_think_time': 0
        }
        
        # Обработка ошибок
        self.error_message = None
        self.last_error_time = 0
        
        # Эффекты
        self.particles = []
        self.notifications = []
    
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
        
        icons_path = os.path.join(os.path.dirname(__file__), 'icons')
        
        for piece, filename in piece_files.items():
            try:
                file_path = os.path.join(icons_path, filename)
                if os.path.exists(file_path):
                    image = pygame.image.load(file_path).convert_alpha()
                    scaled_image = pygame.transform.smoothscale(image, 
                                                              (self.SQUARE_SIZE, self.SQUARE_SIZE))
                    pieces[piece] = scaled_image
                else:
                    pieces[piece] = None
            except Exception as e:
                pieces[piece] = None
        
        return pieces
    
    def add_notification(self, message: str, color=(0, 0, 0)):
        """Добавление уведомления"""
        self.notifications.append({
            'message': message,
            'color': color,
            'time': pygame.time.get_ticks(),
            'y': 50
        })
    
    def update_notifications(self):
        """Обновление уведомлений"""
        current_time = pygame.time.get_ticks()
        for notif in self.notifications[:]:
            age = current_time - notif['time']
            if age > 3000:  # 3 секунды
                self.notifications.remove(notif)
            else:
                # Анимация появления
                notif['y'] = 50 - (age / 3000) * 20
    
    def ai_worker(self):
        """Продвинутый ИИ с анализом позиции"""
        try:
            start_time = time.time()
            
            # Анализируем позицию
            best_move = None
            best_score = -10000
            
            # Генерируем все возможные ходы
            all_moves = []
            for row in range(8):
                for col in range(8):
                    piece = self.engine.board_state[row][col]
                    if piece != '.' and piece.islower() == (not self.engine.current_turn):
                        moves = self.engine.get_cached_valid_moves((row, col))
                        for move in moves:
                            all_moves.append(((row, col), move))
            
            # Оцениваем каждый ход
            for move in all_moves:
                score = self.evaluate_move(move)
                if score > best_score:
                    best_score = score
                    best_move = move
            
            think_time = time.time() - start_time
            self.game_stats['ai_think_time'] = think_time
            
            if best_move:
                self.ai_queue.put(('result', best_move))
            else:
                self.ai_queue.put(('no_move', None))
                
        except Exception as e:
            self.ai_queue.put(('error', str(e)))
    
    def evaluate_move(self, move: Tuple[Tuple[int, int], Tuple[int, int]]) -> int:
        """Оценка качества хода"""
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.engine.board_state[from_row][from_col]
        target = self.engine.board_state[to_row][to_col]
        
        score = 0
        
        # Ценность захвата
        piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 100}
        if target != '.':
            score += piece_values.get(target.lower(), 1) * 10
        
        # Контроль центра
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        if to_pos in center_squares:
            score += 2
        
        # Развитие фигур
        if piece.lower() in ['n', 'b']:
            score += 1
        
        # Безопасность короля
        if piece.lower() == 'k':
            # Избегаем края доски
            if to_col in [0, 1, 6, 7]:
                score -= 1
        
        return score
    
    def start_ai_calculation(self):
        """Запуск вычислений ИИ"""
        if self.ai_calculating or not self.game_active or self.promotion_pending:
            return
        
        with self.lock:
            self.ai_calculating = True
            self.ai_thread = threading.Thread(target=self.ai_worker, daemon=True)
            self.ai_thread.start()
    
    def check_ai_result(self):
        """Проверка результатов ИИ"""
        try:
            while not self.ai_queue.empty():
                msg_type, data = self.ai_queue.get_nowait()
                if msg_type == 'result':
                    self.ai_result = data
                    self.process_ai_move()
                elif msg_type == 'no_move':
                    self.show_error("ИИ не нашел допустимых ходов")
                elif msg_type == 'error':
                    self.show_error(f"Ошибка ИИ: {data}")
        except queue.Empty:
            pass
        except Exception as e:
            self.show_error(f"Ошибка очереди: {e}")
    
    def process_ai_move(self):
        """Обработка хода ИИ"""
        if self.ai_result and self.game_active and not self.white_turn and not self.promotion_pending:
            try:
                from_pos, to_pos = self.ai_result
                if self.make_move(from_pos, to_pos):
                    self.game_stats['moves_count'] += 1
                    self.add_notification(f"ИИ сходил за {self.game_stats['ai_think_time']:.2f}с", self.BLUE)
            except Exception as e:
                self.show_error(f"Ошибка хода ИИ: {e}")
        
        with self.lock:
            self.ai_calculating = False
            self.ai_result = None
            self.ai_thread = None
    
    def show_error(self, message: str):
        """Отображение ошибки"""
        self.error_message = message
        self.last_error_time = pygame.time.get_ticks()
        print(f"ОШИБКА: {message}")
    
    def clear_error(self):
        """Очистка ошибки"""
        if self.error_message and pygame.time.get_ticks() - self.last_error_time > 5000:
            self.error_message = None
    
    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Проверка допустимости хода"""
        return self.engine.is_valid_move(from_pos, to_pos)
    
    def get_valid_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Получение допустимых ходов"""
        return self.engine.get_cached_valid_moves(pos)
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Выполнение хода"""
        if not self.is_valid_move(from_pos, to_pos):
            return False
        
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.engine.board_state[from_row][from_col]
        captured = self.engine.board_state[to_row][to_col]
        piece_type = piece.lower()
        
        # Проверка промоции пешки
        if piece_type == 'p' and (to_row == 0 or to_row == 7):
            self.promotion_pending = (from_pos, to_pos)
            return True
        
        # Выполнение хода
        if not self.engine.make_move(from_pos, to_pos):
            return False
        
        # Статистика
        if abs(from_col - to_col) == 2 and piece_type == 'k':
            self.game_stats['castling_count'] += 1
            self.add_notification("Рокировка!", self.GREEN)
        elif from_col != to_col and captured == '.' and piece_type == 'p':
            self.game_stats['en_passant_count'] += 1
            self.add_notification("Взятие на проходе!", self.GREEN)
        elif captured != '.':
            self.game_stats['captures_count'] += 1
            self.captured_pieces['white' if captured.isupper() else 'black'].append(captured)
        
        # Проверка шаха
        if self.engine.is_king_in_check(not self.engine.current_turn):
            self.game_stats['check_count'] += 1
            self.add_notification("ШАХ!", self.RED)
        
        # Смена очереди
        self.white_turn = not self.white_turn
        
        # Сброс выбора
        self.selected_square = None
        self.valid_moves = []
        
        return True
    
    def promote_pawn(self, promotion_piece: str):
        """Промоция пешки"""
        if not self.promotion_pending:
            return
        
        from_pos, to_pos = self.promotion_pending
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Определяем цвет промоции
        promoted_piece = promotion_piece.upper() if self.engine.board_state[from_row][from_col].isupper() else promotion_piece.lower()
        
        # Выполняем промоцию
        self.engine.board_state[to_row][to_col] = promoted_piece
        self.engine.board_state[from_row][from_col] = '.'
        
        # Обновляем состояние
        self.engine.current_turn = not self.engine.current_turn
        self.game_stats['promotion_count'] += 1
        self.game_stats['moves_count'] += 1
        self.add_notification(f"Пешка превратилась в {promotion_piece.upper()}", self.GREEN)
        
        # Сброс
        self.promotion_pending = None
        self.selected_square = None
        self.valid_moves = []
        
        # Очистка кэша
        self.engine.move_cache.clear()
        self.engine.update_position_hash()
    
    def handle_mouse_click(self, pos: Tuple[int, int]):
        """Обработка клика мыши"""
        if not self.game_active or self.promotion_pending:
            return
        
        x, y = pos
        col = x // self.SQUARE_SIZE
        row = y // self.SQUARE_SIZE
        
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            self.handle_square_click((row, col))
        elif self.SIDE_PANEL_WIDTH > x > self.BOARD_SIZE * self.SQUARE_SIZE:
            self.handle_panel_click(pos)
    
    def handle_square_click(self, square: Tuple[int, int]):
        """Обработка клика по клетке"""
        row, col = square
        piece = self.engine.board_state[row][col]
        
        # Проверка очереди хода
        is_white_piece = piece.isupper()
        if (is_white_piece and not self.white_turn) or (not is_white_piece and self.white_turn):
            return
        
        if self.selected_square is None:
            # Выбор фигуры
            if piece != '.':
                self.selected_square = square
                self.valid_moves = self.get_valid_moves(square)
        else:
            # Выполнение хода
            if square in self.valid_moves:
                self.make_move(self.selected_square, square)
            # Сброс выбора
            self.selected_square = None
            self.valid_moves = []
    
    def handle_panel_click(self, pos: Tuple[int, int]):
        """Обработка клика по панели"""
        x, y = pos
        
        # Проверка кнопок промоции
        if self.promotion_pending:
            promo_y = 200
            pieces = ['Q', 'R', 'B', 'N']
            for i, piece in enumerate(pieces):
                button_rect = pygame.Rect(self.BOARD_SIZE * self.SQUARE_SIZE + 20, 
                                        promo_y + i * 40, 100, 35)
                if button_rect.collidepoint(x, y):
                    self.promote_pawn(piece)
                    return
        
        # Проверка обычных кнопок
        button_y = self.HEIGHT - 120
        buttons = [(0, "Новая игра", self.reset_game), 
                  (1, "Режим", self.toggle_game_mode),
                  (2, "Отмена", self.undo_move)]
        
        for i, (_, text, func) in enumerate(buttons):
            button_rect = pygame.Rect(self.BOARD_SIZE * self.SQUARE_SIZE + 20, 
                                    button_y + i * 40, 100, 35)
            if button_rect.collidepoint(x, y):
                func()
                return
    
    def undo_move(self):
        """Отмена последнего хода"""
        if self.move_history:
            # TODO: Реализовать отмену хода
            pass
    
    def handle_events(self):
        """Обработка событий"""
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_mouse_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_m:
                        self.toggle_game_mode()
                    elif event.key == pygame.K_u:
                        self.undo_move()
                    elif event.key == pygame.K_SPACE:
                        if self.game_mode == 'computer' and not self.white_turn and not self.promotion_pending:
                            self.start_ai_calculation()
            
            return True
        
        except Exception as e:
            self.show_error(f"Ошибка событий: {e}")
            return True
    
    def draw_board(self):
        """Отрисовка доски"""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                # Цвет клетки
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                
                # Выделение
                if self.selected_square == (row, col):
                    color = self.SELECTED_COLOR
                elif (row, col) in self.valid_moves:
                    highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill((*self.HIGHLIGHT_COLOR, 120))
                    rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                     self.SQUARE_SIZE, self.SQUARE_SIZE)
                    self.screen.blit(highlight_surface, rect)
                    continue
                
                # Отрисовка клетки
                rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                 self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                
                # Координаты
                if row == 7:
                    coord_text = self.small_font.render(chr(97 + col), True, self.BLACK)
                    self.screen.blit(coord_text, (col * self.SQUARE_SIZE + 5, 
                                                row * self.SQUARE_SIZE + self.SQUARE_SIZE - 20))
                if col == 0:
                    coord_text = self.small_font.render(str(8 - row), True, self.BLACK)
                    self.screen.blit(coord_text, (5, row * self.SQUARE_SIZE + 5))
                
                # Отрисовка фигуры
                piece = self.engine.board_state[row][col]
                if piece != '.':
                    if piece in self.piece_images and self.piece_images[piece] is not None:
                        piece_surface = self.piece_images[piece]
                        piece_rect = piece_surface.get_rect(center=rect.center)
                        self.screen.blit(piece_surface, piece_rect)
                    else:
                        # Резервные символы
                        unicode_symbols = {
                            'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
                            'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'
                        }
                        symbol = unicode_symbols.get(piece, piece)
                        text_color = self.BLACK if piece.isupper() else self.RED
                        text = self.font.render(symbol, True, text_color)
                        text_rect = text.get_rect(center=rect.center)
                        self.screen.blit(text, text_rect)
        
        # Индикатор шаха
        if self.engine.is_king_in_check(self.engine.current_turn):
            king_piece = 'K' if self.engine.current_turn else 'k'
            king_pos = self.engine.king_positions[king_piece]
            king_rect = pygame.Rect(king_pos[1] * self.SQUARE_SIZE, king_pos[0] * self.SQUARE_SIZE,
                                  self.SQUARE_SIZE, self.SQUARE_SIZE)
            pygame.draw.rect(self.screen, self.RED, king_rect, 5)
    
    def draw_side_panel(self):
        """Отрисовка боковой панели"""
        panel_rect = pygame.Rect(self.BOARD_SIZE * self.SQUARE_SIZE, 0, 
                               self.SIDE_PANEL_WIDTH, self.HEIGHT)
        pygame.draw.rect(self.screen, self.PANEL_BG, panel_rect)
        pygame.draw.line(self.screen, self.BLACK, 
                        (self.BOARD_SIZE * self.SQUARE_SIZE, 0),
                        (self.BOARD_SIZE * self.SQUARE_SIZE, self.HEIGHT), 2)
        
        # Заголовок
        title = self.big_font.render("Шахматы PRO", True, self.BLACK)
        self.screen.blit(title, (self.BOARD_SIZE * self.SQUARE_SIZE + 20, 10))
        
        # Информация об игре
        elapsed = (pygame.time.get_ticks() - self.game_stats['game_start_time']) // 1000
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        info_lines = [
            f"Ход: {'Белые' if self.white_turn else 'Черные'}",
            f"Игра: {'Активна' if self.game_active else 'Завершена'}",
            f"Режим: {'Компьютер' if self.game_mode == 'computer' else 'Два игрока'}",
            "",
            f"Ходов: {self.game_stats['moves_count']}",
            f"Взятий: {self.game_stats['captures_count']}",
            f"Шахов: {self.game_stats['check_count']}",
            f"Рокировок: {self.game_stats['castling_count']}",
            f"En Passant: {self.game_stats['en_passant_count']}",
            f"Промоций: {self.game_stats['promotion_count']}",
            f"Время: {minutes:02d}:{seconds:02d}",
            f"AI время: {self.game_stats['ai_think_time']:.2f}с"
        ]
        
        for i, line in enumerate(info_lines):
            color = self.RED if i == 1 and not self.game_active else self.BLACK
            text_surface = self.font.render(line, True, color)
            self.screen.blit(text_surface, (self.BOARD_SIZE * self.SQUARE_SIZE + 20, 60 + i * 22))
        
        # Кнопки
        button_y = self.HEIGHT - 120
        buttons = [("Новая (R)", self.reset_game), 
                  ("Режим (M)", self.toggle_game_mode),
                  ("Отмена (U)", self.undo_move)]
        
        for i, (text, _) in enumerate(buttons):
            button_rect = pygame.Rect(self.BOARD_SIZE * self.SQUARE_SIZE + 20, 
                                    button_y + i * 40, 100, 35)
            pygame.draw.rect(self.screen, self.LIGHT_SQUARE, button_rect)
            pygame.draw.rect(self.screen, self.BLACK, button_rect, 2)
            
            text_surface = self.small_font.render(text, True, self.BLACK)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
        
        # Статус ИИ
        if self.ai_calculating:
            ai_status = self.small_font.render("ИИ анализирует...", True, self.BLUE)
            self.screen.blit(ai_status, (self.BOARD_SIZE * self.SQUARE_SIZE + 20, button_y - 30))
        
        # Промоция пешки
        if self.promotion_pending:
            promo_text = self.font.render("Выберите фигуру:", True, self.BLACK)
            self.screen.blit(promo_text, (self.BOARD_SIZE * self.SQUARE_SIZE + 20, 180))
            
            pieces = ['Ферзь (Q)', 'Ладья (R)', 'Слон (B)', 'Конь (N)']
            for i, piece_text in enumerate(pieces):
                button_rect = pygame.Rect(self.BOARD_SIZE * self.SQUARE_SIZE + 20, 
                                        200 + i * 40, 100, 35)
                pygame.draw.rect(self.screen, self.LIGHT_SQUARE, button_rect)
                pygame.draw.rect(self.screen, self.BLACK, button_rect, 2)
                
                text_surface = self.small_font.render(piece_text, True, self.BLACK)
                text_rect = text_surface.get_rect(center=button_rect.center)
                self.screen.blit(text_surface, text_rect)
        
        # Ошибки
        if self.error_message:
            error_surface = self.small_font.render(self.error_message, True, self.RED)
            self.screen.blit(error_surface, (self.BOARD_SIZE * self.SQUARE_SIZE + 20, button_y - 60))
    
    def draw_notifications(self):
        """Отрисовка уведомлений"""
        for notif in self.notifications:
            text_surface = self.font.render(notif['message'], True, notif['color'])
            text_rect = text_surface.get_rect(center=(self.WIDTH // 2, notif['y']))
            # Тень
            shadow_surface = self.font.render(notif['message'], True, (100, 100, 100))
            self.screen.blit(shadow_surface, (text_rect.x + 2, text_rect.y + 2))
            # Основной текст
            self.screen.blit(text_surface, text_rect)
    
    def draw(self):
        """Основная отрисовка"""
        self.screen.fill(self.WHITE)
        self.draw_board()
        self.draw_side_panel()
        self.draw_notifications()
    
    def reset_game(self):
        """Сброс игры"""
        self.engine.board_state = self.engine.get_initial_board()
        self.engine.current_turn = True
        self.engine.castling_rights = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.engine.en_passant_target = None
        self.engine.king_positions = {'K': (7, 4), 'k': (0, 4)}
        self.engine.move_cache.clear()
        self.engine.update_position_hash()
        
        self.selected_square = None
        self.valid_moves = []
        self.game_active = True
        self.white_turn = True
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.promotion_pending = None
        self.game_stats = {
            'moves_count': 0,
            'captures_count': 0,
            'check_count': 0,
            'castling_count': 0,
            'en_passant_count': 0,
            'promotion_count': 0,
            'game_start_time': pygame.time.get_ticks(),
            'ai_think_time': 0
        }
        self.ai_calculating = False
        self.ai_result = None
        self.error_message = None
        self.notifications = []
    
    def toggle_game_mode(self):
        """Смена режима"""
        self.game_mode = 'two_players' if self.game_mode == 'computer' else 'computer'
        self.reset_game()
    
    def run(self):
        """Основной цикл"""
        running = True
        
        while running:
            self.clock.tick(60)
            
            # Обновления
            self.update_notifications()
            self.check_ai_result()
            
            # События
            running = self.handle_events()
            
            # Очистка ошибок
            self.clear_error()
            
            # Запуск ИИ
            if (self.game_mode == 'computer' and not self.white_turn and 
                self.game_active and not self.ai_calculating and 
                not self.ai_result and not self.promotion_pending):
                self.start_ai_calculation()
            
            # Отрисовка
            self.draw()
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        game = ProChessGUI()
        game.run()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        pygame.quit()
        sys.exit(1)