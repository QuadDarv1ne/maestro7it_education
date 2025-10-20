#!/usr/bin/env python3
# ============================================================================
# game/chess_game.py (Обновлённая версия)
# ============================================================================

"""
Модуль: game/chess_game.py

Описание:
    Содержит главный класс ChessGame, который управляет игровым процессом.
    
Изменения в этой версии:
    - Удалён импорт и вызов init_fonts() (инициализация теперь в BoardRenderer)
    - Обновлены методы для работы с новым API BoardRenderer
    - Улучшена обработка ошибок
"""

import pygame
from typing import Optional, Tuple, List
import time
import sys
import random

# Import our modules
from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer  # Убран init_fonts
from utils.educational import ChessEducator

# Constants from board_renderer
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8


class ChessGame:
    """
    Главный класс для управления ходом игры.
    
    Атрибуты:
        player_color (str): Сторона, за которую играет игрок
        ai_color (str): Сторона, за которую играет компьютер
        engine (StockfishWrapper): Экземпляр шахматного движка
        move_history (List): История всех сделанных ходов
        game_over (bool): Флаг окончания игры
        renderer (BoardRenderer): Рендерер для отображения доски
        educator (ChessEducator): Образовательный компонент для подсказок
    """
    
    def __init__(self, player_color: str = 'white', skill_level: int = 5, theme: str = 'classic'):
        """
        Инициализация новой игры.
        
        Параметры:
            player_color (str): Выбранная сторона ('white' или 'black')
            skill_level (int): Уровень сложности Stockfish (0-20)
            theme (str): Цветовая тема доски
            
        Исключения:
            RuntimeError: Если не удалось инициализировать Stockfish
        """
        self.player_color = player_color
        self.ai_color = 'black' if player_color == 'white' else 'white'
        self.skill_level = skill_level
        self.theme = theme
        
        try:
            self.engine = StockfishWrapper(skill_level=skill_level)
        except RuntimeError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось инициализировать игру: {e}")
        
        # Инициализация Pygame UI
        try:
            # Инициализируем pygame если ещё не инициализирован
            if not pygame.get_init():
                pygame.init()
            
            self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
            pygame.display.set_caption(f"♟️  chess_stockfish — Maestro7IT (уровень {skill_level})")
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось инициализировать графический интерфейс: {e}")
        
        # Создаём рендерер (шрифты инициализируются автоматически)
        self.renderer = BoardRenderer(self.screen, player_color)
        self.renderer.set_theme(theme)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Инициализируем шрифты для UI панели
        self._init_ui_fonts()
        
        # Образовательные компоненты
        self.educator = ChessEducator()
        
        # Состояние игры
        self.move_history = []
        self.move_annotations = []  # Аннотации к ходам (например, + для шаха, x для взятия)
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.ai_move_delay = 0.3  # Уменьшена задержка перед ходом ИИ для более быстрой игры
        self.move_feedback = ""  # Feedback message for the player
        self.move_feedback_time = 0
        self.frame_count = 0  # Счетчик кадров для очистки временных поверхностей
        self.highlight_hint = None  # For T key hint highlighting
        
        # Улучшенная система кэширования
        self._cache = {
            'board_state': None,
            'board_fen': None,
            'valid_moves': {},  # Кэш для допустимых ходов
            'uci_conversions': {},  # Кэш для преобразований координат
            'last_evaluation': None,
            'last_eval_fen': None
        }
        
        # Дополнительные кэши для оптимизации производительности
        self._valid_moves_cache = {}  # Кэш для вычисленных допустимых ходов
        self._valid_moves_cache_time = {}  # Время последнего обновления кэша ходов
        self._valid_moves_cache_duration = 0.5  # Кэш ходов действует 500 мс
        
        # Графические оптимизации
        self.last_board_hash = None
        self.dirty_squares = set()
        self.piece_surfaces = {}
        self.highlight_surfaces = {}
        
        # Таймеры для оптимизации обновлений
        self.last_board_update = 0
        self.last_ui_update = 0
        self.board_update_interval = 1.0/60  # Повышена частота обновления доски до 60 FPS
        self.ui_update_interval = 1.0/30     # Повышена частота обновления UI до 30 FPS
        
        # Инициализация графических ресурсов
        self._init_fonts_optimized()
        self._init_piece_surfaces()
        self._init_highlight_surfaces()
        
        # Оптимизация AI
        self.ai_move_cache = {}  # Кэш для AI ходов
        self.last_ai_move_time = 0
        self.ai_move_cooldown = 0.05  # Минимальная задержка между AI ходами (уменьшена)
        
        # Дополнительные оптимизации
        self.board_state_cache = None  # Кэш состояния доски для быстрого доступа
        self.board_state_cache_time = 0
        self.board_state_cache_duration = 0.1  # Кэш действует 100 мс
        
        # Расширенная статистика игры
        self.game_stats = {
            'start_time': time.time(),
            'player_moves': 0,
            'ai_moves': 0,
            'player_capture_count': 0,
            'ai_capture_count': 0,
            'check_count': 0,
            'move_times': [],  # Время, затраченное на каждый ход
            'evaluations': [],  # Оценки позиции
            'advantage_changes': 0  # Количество изменений преимущества
        }
        
        # Улучшенный геймплей
        self.last_move_was_capture = False
        self.combo_counter = 0
        self.special_move_messages = []
        self.last_evaluation = 0  # Для отслеживания изменений оценки
        
        # Для режима анализа
        self.analysis_mode = False
        self.analysis_move = None
        
        # Для сохранения/загрузки партий
        self.saved_games = []
    
    def _init_ui_fonts(self):
        """Инициализация шрифтов для UI элементов."""
        try:
            self.ui_font = pygame.font.SysFont('Arial', 14)
            self.ui_font_small = pygame.font.SysFont('Arial', 12)
        except Exception as e:
            print(f"⚠️  Не удалось загрузить шрифты UI: {e}")
            self.ui_font = pygame.font.Font(None, 14)
            self.ui_font_small = pygame.font.Font(None, 12)
    
    def _init_fonts_optimized(self):
        """Оптимизированная инициализация шрифтов."""
        # Используем системные шрифты для лучшей производительности
        try:
            # Предзагружаем часто используемые размеры шрифтов
            self.fonts = {
                'piece': pygame.font.SysFont('Segoe UI Symbol', SQUARE_SIZE - 10),
                'coord': pygame.font.SysFont('Arial', 14, bold=True),
                'ui': pygame.font.SysFont('Arial', 16),
                'ui_small': pygame.font.SysFont('Arial', 12)
            }
        except:
            # Резервные шрифты
            self.fonts = {
                'piece': pygame.font.Font(None, SQUARE_SIZE - 10),
                'coord': pygame.font.Font(None, 14),
                'ui': pygame.font.Font(None, 16),
                'ui_small': pygame.font.Font(None, 12)
            }
    
    def _init_piece_surfaces(self):
        """Предзагрузка и кэширование поверхностей фигур для ускорения отрисовки."""
        self.piece_surfaces = {}
        
        # Unicode символы фигур
        PIECE_UNICODE = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        
        # Создаем поверхности для каждой фигуры один раз
        for piece in ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']:
            if piece in PIECE_UNICODE:
                try:
                    # Создаем поверхность с фигурой
                    surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    # Рендерим фигуру на поверхность
                    font = self.fonts.get('piece', pygame.font.SysFont('Arial', SQUARE_SIZE - 10))
                    # Определяем цвет фигуры (белые - черные)
                    color = (255, 255, 255) if piece.isupper() else (0, 0, 0)
                    text = font.render(PIECE_UNICODE[piece], True, color)
                    text_rect = text.get_rect(center=(SQUARE_SIZE//2, SQUARE_SIZE//2))
                    surface.blit(text, text_rect)
                    self.piece_surfaces[piece] = surface
                except Exception as e:
                    print(f"Ошибка при создании поверхности для фигуры {piece}: {e}")

    def _init_highlight_surfaces(self):
        """Предзагрузка поверхностей для эффектов выделения."""
        self.highlight_surfaces = {}
        
        # Создаем поверхности для различных типов выделения
        highlight_configs = {
            'selected': ((124, 252, 0, 180), 3),      # Зеленый, толстая рамка
            'last_move': ((255, 255, 0, 150), 2),     # Желтый, средняя рамка
            'valid_move': ((0, 0, 255, 100), 0),      # Синий, круг (толщина 0 для заливки)
            'check': ((255, 0, 0, 180), 2),           # Красный, рамка
            'hint': ((0, 255, 0, 120), 2)             # Зеленый, рамка для подсказок
        }
        
        for highlight_type, (color, width) in highlight_configs.items():
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            
            if highlight_type == 'valid_move':
                # Для точек возможных ходов рисуем круг
                pygame.draw.circle(surface, color, 
                                 (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//6)
            else:
                # Для других типов выделения рисуем прямоугольники
                rect = surface.get_rect()
                if width > 0:
                    pygame.draw.rect(surface, color, rect, width)
                else:
                    pygame.draw.rect(surface, color, rect)
                
            self.highlight_surfaces[highlight_type] = surface

    def _coord_to_fen_square(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """
        Преобразует экранные координаты клика в FEN координаты.
        Использует новый метод coord_mapper из BoardRenderer.
        
        Параметры:
            x (int): X координата клика
            y (int): Y координата клика
            
        Возвращает:
            Tuple: (row, col) в FEN или None если клик вне доски
        """
        return self.renderer.coord_mapper.pixel_to_square(x, y)
    
    def _fen_square_to_uci(self, row: int, col: int) -> str:
        """
        Преобразует FEN координаты в UCI формат с кэшированием.
        
        Параметры:
            row (int): Ряд (0-7)
            col (int): Колонна (0-7)
            
        Возвращает:
            str: Координата в UCI формате (например, 'e4')
        """
        # Кэширование для улучшения производительности
        if not hasattr(self, '_uci_cache'):
            self._uci_cache = {}
        
        cache_key = (row, col)
        if cache_key in self._uci_cache:
            return self._uci_cache[cache_key]
        
        uci = chr(ord('a') + col) + str(8 - row)
        self._uci_cache[cache_key] = uci
        return uci
    
    def get_board_state(self) -> List[List[Optional[str]]]:
        """
        Получение состояния доски с кэшированием.
        
        Возвращает:
            List[List[Optional[str]]]: Состояние доски
        """
        try:
            current_time = time.time()
            # Проверяем кэш
            if (self.board_state_cache is not None and 
                current_time - self.board_state_cache_time < self.board_state_cache_duration):
                return self.board_state_cache
            
            # Получаем новое состояние доски
            board = self.engine.get_board_state()
            
            # Обновляем кэш
            self.board_state_cache = board
            self.board_state_cache_time = current_time
            
            return board
        except Exception:
            # Возвращаем пустую доску в случае ошибки
            empty_board: List[List[Optional[str]]] = [[None for _ in range(8)] for _ in range(8)]
            self.board_state_cache = empty_board
            self.board_state_cache_time = time.time()
            return empty_board
    
    def get_cached_evaluation(self):
        """
        Получение кэшированной оценки позиции.
        
        Возвращает:
            float: Оценка позиции
        """
        try:
            current_fen = self.engine.get_fen()
            if self._cache['last_eval_fen'] == current_fen and self._cache['last_evaluation'] is not None:
                return self._cache['last_evaluation']
                
            evaluation = self.engine.get_evaluation()
            self._cache['last_evaluation'] = evaluation
            self._cache['last_eval_fen'] = current_fen
            return evaluation
        except Exception:
            return None
    
    def _get_pawn_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для пешки."""
        moves = []
        is_white = piece.isupper()
        
        # Направление движения
        direction = -1 if is_white else 1
        
        # Ход вперед на одну клетку
        new_row = row + direction
        if 0 <= new_row < 8 and board[new_row][col] is None:
            moves.append((new_row, col))
            
            # Ход вперед на две клетки с начальной позиции
            start_row = 6 if is_white else 1
            if row == start_row:
                new_row_2 = row + 2 * direction
                if 0 <= new_row_2 < 8 and board[new_row][col] is None and board[new_row_2][col] is None:
                    moves.append((new_row_2, col))
        
        # Взятие по диагонали
        for dc in [-1, 1]:
            new_col = col + dc
            new_row = row + direction
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is not None and ((is_white and target.islower()) or (not is_white and target.isupper())):
                    moves.append((new_row, new_col))
                    
        return moves

    def _get_knight_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для коня."""
        moves = []
        is_white = piece.isupper()
        
        # Все возможные ходы коня
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or ((is_white and target.islower()) or (not is_white and target.isupper())):
                    moves.append((new_row, new_col))
                    
        return moves

    def _get_bishop_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для слона."""
        moves = []
        is_white = piece.isupper()
        
        # Диагональные направления
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                else:
                    if (is_white and target.islower()) or (not is_white and target.isupper()):
                        moves.append((new_row, new_col))
                    break
                new_row += dr
                new_col += dc
                    
        return moves

    def _get_rook_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для ладьи."""
        moves = []
        is_white = piece.isupper()
        
        # Горизонтальные и вертикальные направления
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            while 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None:
                    moves.append((new_row, new_col))
                else:
                    if (is_white and target.islower()) or (not is_white and target.isupper()):
                        moves.append((new_row, new_col))
                    break
                new_row += dr
                new_col += dc
                    
        return moves

    def _get_queen_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для ферзя."""
        # Ферзь = слон + ладья
        bishop_moves = self._get_bishop_moves(row, col, piece, board)
        rook_moves = self._get_rook_moves(row, col, piece, board)
        return bishop_moves + rook_moves

    def _get_king_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для короля."""
        moves = []
        is_white = piece.isupper()
        
        # Все направления для короля
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = board[new_row][new_col]
                if target is None or ((is_white and target.islower()) or (not is_white and target.isupper())):
                    moves.append((new_row, new_col))
                    
        return moves

    def _get_valid_moves(self, from_row: int, from_col: int) -> List[Tuple[int, int]]:
        """
        Получить список допустимых ходов для фигуры на заданной позиции.
        Оптимизированная версия с использованием правил движения фигур и кэширования.
        
        Параметры:
            from_row (int): Ряд фигуры
            from_col (int): Колонна фигуры
            
        Возвращает:
            List[Tuple[int, int]]: Список допустимых позиций для хода
        """
        # Создаем ключ для кэширования
        cache_key = (from_row, from_col)
        current_time = time.time()
        
        # Проверяем кэш
        if cache_key in self._valid_moves_cache:
            # Проверяем, не истекло ли время кэша
            if current_time - self._valid_moves_cache_time[cache_key] < self._valid_moves_cache_duration:
                return self._valid_moves_cache[cache_key][:]  # Возвращаем копию, чтобы избежать модификации кэша
        
        valid_moves = []
        from_uci = self._fen_square_to_uci(from_row, from_col)
        
        try:
            # Используем кэшированное состояние доски для повышения производительности
            board_state: List[List[Optional[str]]] = self.get_board_state()
            
            piece = board_state[from_row][from_col]
            if not piece:
                # Сохраняем в кэш даже пустой результат
                self._valid_moves_cache[cache_key] = []
                self._valid_moves_cache_time[cache_key] = current_time
                return valid_moves
                
            piece_lower = piece.lower()
            
            # Оптимизация: генерируем только возможные ходы для каждой фигуры
            if piece_lower == 'p':  # Пешка
                candidate_moves = self._get_pawn_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'n':  # Конь
                candidate_moves = self._get_knight_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'b':  # Слон
                candidate_moves = self._get_bishop_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'r':  # Ладья
                candidate_moves = self._get_rook_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'q':  # Ферзь
                candidate_moves = self._get_queen_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'k':  # Король
                candidate_moves = self._get_king_moves(from_row, from_col, piece, board_state)
            else:
                candidate_moves = []
                
            # Проверяем допустимость ходов через движок
            for to_row, to_col in candidate_moves:
                to_uci = self._fen_square_to_uci(to_row, to_col)
                uci_move = from_uci + to_uci
                if self.engine.is_move_correct(uci_move):
                    valid_moves.append((to_row, to_col))
                    
        except Exception as e:
            print(f"Ошибка при расчете допустимых ходов: {e}")
        
        # Сохраняем результат в кэш
        self._valid_moves_cache[cache_key] = valid_moves[:]
        self._valid_moves_cache_time[cache_key] = current_time
            
        return valid_moves

    def _is_path_blocked(self, from_row: int, from_col: int, to_row: int, to_col: int, board: List[List[Optional[str]]]) -> bool:
        """
        Проверить, заблокирован ли путь между двумя клетками.
        
        Параметры:
            from_row (int): Исходный ряд
            from_col (int): Исходная колонна
            to_row (int): Целевой ряд
            to_col (int): Целевая колонна
            board (List[List[Optional[str]]]): Состояние доски
            
        Возвращает:
            bool: True если путь заблокирован, False если свободен
        """
        # Determine direction
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        # Check each square along the path (excluding start and end)
        current_row, current_col = from_row + row_step, from_col + col_step
        while current_row != to_row or current_col != to_col:
            if board[current_row][current_col] is not None:
                return True  # Path is blocked
            current_row += row_step
            current_col += col_step
        
        return False  # Path is clear
    
    def _get_move_hint(self, from_row: int, from_col: int, to_row: int, to_col: int) -> str:
        """
        Получить подсказку о причине недопустимости хода.
        
        Параметры:
            from_row (int): Исходный ряд
            from_col (int): Исходная колонна
            to_row (int): Целевой ряд
            to_col (int): Целевая колонна
            
        Возвращает:
            str: Подсказка о причине недопустимости хода
        """
        try:
            # Оптимизация: кэшируем доску, чтобы не запрашивать её несколько раз
            if not hasattr(self, '_cached_board'):
                self._cached_board = self.engine.get_board_state()
            board = self._cached_board
            
            piece = board[from_row][from_col]
            
            if not piece:
                return "Нет фигуры на этой клетке"
            
            # Оптимизация: кэшируем имена фигур
            if not hasattr(self, '_piece_name_cache'):
                self._piece_name_cache = {
                    'P': 'белая пешка', 'N': 'белый конь', 'B': 'белый слон', 
                    'R': 'белая ладья', 'Q': 'белый ферзь', 'K': 'белый король',
                    'p': 'чёрная пешка', 'n': 'чёрный конь', 'b': 'чёрный слон', 
                    'r': 'чёрная ладья', 'q': 'чёрный ферзь', 'k': 'чёрный король'
                }
            piece_name = self._piece_name_cache.get(piece, piece)
            
            # Кэшируем результаты для дальнейшего использования
            if not hasattr(self, '_piece_hint_cache'):
                self._piece_hint_cache = {}
            if piece not in self._piece_hint_cache:
                self._piece_hint_cache[piece] = self.educator.get_piece_hint(piece_name)
            
            # Special hints for pawns
            piece_lower = piece.lower()
            if piece_lower == 'p':
                # Check if it's a pawn trying to move two squares from non-starting position
                if abs(from_row - to_row) == 2:
                    # White pawn starting position is row 6 in FEN (rank 2)
                    # Black pawn starting position is row 1 in FEN (rank 7)
                    is_white = piece.isupper()
                    is_starting_position = (is_white and from_row == 6) or (not is_white and from_row == 1)
                    
                    if not is_starting_position:
                        return f"{piece_name} может двигаться на две клетки только со стартовой позиции"
                
                # Check if moving backward
                is_white = piece.isupper()
                moving_forward = (is_white and to_row < from_row) or (not is_white and to_row > from_row)
                
                if not moving_forward:
                    return f"{piece_name} может двигаться только вперёд"
                
                # Check if trying to capture forward (pawns capture diagonally)
                if from_col == to_col and board[to_row][to_col] is not None:
                    return f"{piece_name} не может взять фигуру, двигаясь вперёд. Пешки берут по диагонали!"
                
                # Check if trying to move diagonally without capturing
                if from_col != to_col and board[to_row][to_col] is None:
                    return f"{piece_name} может двигаться по диагонали только для взятия фигуры"
            
            # Special hints for other pieces
            elif piece_lower == 'n':  # Knight
                # Knights move in L-shape, check if the move is valid for a knight
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
                    return f"{piece_name} ходит буквой Г (две клетки в одном направлении и одна в перпендикулярном)"
            
            elif piece_lower == 'b':  # Bishop
                # Bishops move diagonally, check if the move is diagonal
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if row_diff != col_diff:
                    return f"{piece_name} ходит только по диагонали"
                
                # Check if path is blocked
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece_lower == 'r':  # Rook
                # Rooks move horizontally or vertically
                if from_row != to_row and from_col != to_col:
                    return f"{piece_name} ходит только по горизонтали или вертикали"
                
                # Check if path is blocked
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece_lower == 'q':  # Queen
                # Queens move like bishops or rooks
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                
                # Not diagonal, horizontal, or vertical
                if not ((from_row == to_row) or (from_col == to_col) or (row_diff == col_diff)):
                    return f"{piece_name} ходит по горизонтали, вертикали или диагонали"
                
                # Check if path is blocked
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece_lower == 'k':  # King
                # Kings move one square in any direction
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if row_diff > 1 or col_diff > 1:
                    return f"{piece_name} ходит только на одну клетку в любом направлении"
                
                # Special hint for castling
                if row_diff == 0 and col_diff == 2:
                    return f"Рокировка возможна только из начальной позиции и при определённых условиях"
            
            # Check if trying to capture own piece
            target_piece = board[to_row][to_col]
            if target_piece and ((piece.isupper() and target_piece.isupper()) or 
                               (piece.islower() and target_piece.islower())):
                return f"{piece_name} не может взять свою же фигуру"
            
            return f"Недопустимый ход для {piece_name}"
        except Exception as e:
            print(f"Ошибка при получении подсказки: {e}")
            return "Недопустимый ход"

    def _is_player_turn(self) -> bool:
        """
        Проверяет, является ли текущий ход ходом игрока.
        
        Возвращает:
            bool: True если ход игрока, False если ход компьютера
        """
        try:
            side = self.engine.get_side_to_move()
            return (
                (self.player_color == 'white' and side == 'w') or
                (self.player_color == 'black' and side == 'b')
            )
        except Exception:
            # Если не удалось получить сторону, предполагаем, что ход игрока
            return True
    
    def _is_player_piece(self, piece: Optional[str]) -> bool:
        """
        Проверяет, принадлежит ли фигура игроку.
        
        Параметры:
            piece (str): Символ фигуры
            
        Возвращает:
            bool: True если фигура принадлежит игроку
        """
        if not piece:
            return False
        is_white = piece.isupper()
        return (self.player_color == 'white') == is_white

    def handle_click(self, x: int, y: int):
        """
        Обработка клика по доске для выбора и перемещения фигур.
        
        Параметры:
            x (int): X координата клика
            y (int): Y координата клика
        """
        if self.game_over or self.thinking or not self._is_player_turn():
            return
        
        coords = self._coord_to_fen_square(x, y)
        if coords is None:
            # Клик вне доски - очищаем выделение и подсказки
            self.renderer.set_selected(None)
            self.renderer.set_move_hints([])
            return
        
        row, col = coords
        # Очистка кэша доски перед получением нового состояния
        if hasattr(self, '_cached_board'):
            delattr(self, '_cached_board')
        try:
            board = self.engine.get_board_state()
        except Exception as e:
            print(f"⚠️  Ошибка при получении состояния доски: {e}")
            return
        
        piece = board[row][col]
        
        # Выбор фигуры
        if self._is_player_piece(piece) and piece is not None:
            self.renderer.set_selected((row, col))
            # Показываем подсказки возможных ходов
            valid_moves = self._get_valid_moves(row, col)
            self.renderer.set_move_hints(valid_moves)
            # Provide feedback about the selected piece
            piece_name = {
                'P': 'пешка', 'N': 'конь', 'B': 'слон', 'R': 'ладья', 
                'Q': 'ферзь', 'K': 'король', 'p': 'пешка', 'n': 'конь', 
                'b': 'слон', 'r': 'ладья', 'q': 'ферзь', 'k': 'король'
            }.get(piece, piece)
            self.move_feedback = f"Выбрана {piece_name}"
            self.move_feedback_time = time.time()
            
            # Add educational hint about the piece (используем кэш)
            if hasattr(self, '_piece_hint_cache') and piece in self._piece_hint_cache:
                piece_hint = self._piece_hint_cache[piece]
            else:
                piece_hint = self.educator.get_piece_hint(piece_name)
                # Сохраняем в кэш для будущего использования
                if not hasattr(self, '_piece_hint_cache'):
                    self._piece_hint_cache = {}
                self._piece_hint_cache[piece] = piece_hint
            self.move_feedback += f" | {piece_hint}"
        # Перемещение выбранной фигуры
        elif self.renderer.selected_square:
            from_sq = self.renderer.selected_square
            to_sq = (row, col)
            
            from_uci = self._fen_square_to_uci(*from_sq)
            to_uci = self._fen_square_to_uci(*to_sq)
            uci_move = from_uci + to_uci
            
            print(f"Попытка хода: {uci_move} (из {from_sq} в {to_sq})")
            
            # Засекаем время начала хода для статистики
            move_start_time = time.time()
            
            try:
                # Validate the move using our improved method
                if self.engine.is_move_correct(uci_move):
                    # Проверяем, является ли ход взятием фигуры
                    target_piece = board[to_sq[0]][to_sq[1]]
                    is_capture = target_piece is not None
                    
                    # Проверяем, будет ли шах после хода
                    is_check = False
                    is_mate = False
                    is_castling = uci_move in ['e1g1', 'e1c1', 'e8g8', 'e8c8']
                    
                    # Make the move and verify it was successful
                    if self.engine.make_move(uci_move):
                        # Проверяем состояние игры после хода
                        is_over, reason = self.engine.is_game_over()
                        if is_over and reason and "мат" in reason:
                            is_mate = True
                        
                        # Проверяем шах
                        try:
                            eval_result = self.engine.get_evaluation()
                            if eval_result and isinstance(eval_result, dict):
                                is_check = eval_result.get('check', False)
                        except:
                            pass
                        
                        # Аннотируем ход
                        annotated_move = self._annotate_move(uci_move, is_capture, is_check, is_mate, is_castling)
                        
                        self.move_history.append(uci_move)
                        self.move_annotations.append(annotated_move)
                        self.game_stats['player_moves'] += 1
                        if is_capture:
                            self.game_stats['player_capture_count'] += 1
                            self.last_move_was_capture = True
                            self.combo_counter += 1
                            # Combo message
                            if self.combo_counter >= 2:
                                self.special_move_messages.append(f"Комбо x{self.combo_counter}!")
                        else:
                            self.last_move_was_capture = False
                            self.combo_counter = 0  # Сброс комбо при обычном ходе
                        
                        self.renderer.set_last_move(from_sq, to_sq)
                        self.renderer.set_selected(None)
                        self.renderer.set_move_hints([])
                        self.last_move_time = time.time()
                        print(f"Ход выполнен: {annotated_move}")
                        self.move_feedback = f"Ход {annotated_move} выполнен"
                        self.move_feedback_time = time.time()
                        
                        # Записываем время хода в статистику
                        move_time = time.time() - move_start_time
                        self.game_stats['move_times'].append(move_time)
                        
                        # Получаем оценку позиции для статистики
                        evaluation = self.engine.get_evaluation()
                        if evaluation is not None:
                            self.game_stats['evaluations'].append(evaluation)
                        
                        # Add educational feedback (с кэшированием)
                        move_count = len(self.move_history)
                        current_time = time.time()
                        
                        # Создаем ключ для кэширования образовательных подсказок
                        edu_cache_key = move_count
                        edu_cache_duration = 10.0  # Кэш действует 10 секунд
                        
                        # Проверяем кэш образовательных подсказок
                        educational_tip = None
                        if hasattr(self, '_edu_feedback_cache') and hasattr(self, '_edu_feedback_cache_time'):
                            if (edu_cache_key in self._edu_feedback_cache and 
                                current_time - self._edu_feedback_cache_time[edu_cache_key] < edu_cache_duration):
                                educational_tip = self._edu_feedback_cache[edu_cache_key]
                        
                        # Если нет кэшированной подсказки, получаем новую
                        if educational_tip is None:
                            educational_tip = self.educator.get_educational_feedback(move_count, current_time)
                            # Сохраняем в кэш
                            if not hasattr(self, '_edu_feedback_cache'):
                                self._edu_feedback_cache = {}
                                self._edu_feedback_cache_time = {}
                            self._edu_feedback_cache[edu_cache_key] = educational_tip
                            self._edu_feedback_cache_time[edu_cache_key] = current_time
                        
                        if educational_tip:
                            self.move_feedback += f" | {educational_tip}"
                            self.move_feedback_time = current_time
                            
                        # Special move messages
                        if self.special_move_messages:
                            self.move_feedback += f" | {self.special_move_messages[0]}"
                            self.special_move_messages.pop(0)
                    else:
                        print("❌ Не удалось выполнить ход")
                        self.renderer.set_selected(None)
                        self.renderer.set_move_hints([])
                        self.move_feedback = "Не удалось выполнить ход"
                        self.move_feedback_time = time.time()
                else:
                    print(f"❌ Некорректный ход: {uci_move}")
                    self.renderer.set_selected(None)
                    self.renderer.set_move_hints([])
                    # Provide specific feedback about why the move is invalid
                    hint = self._get_move_hint(from_sq[0], from_sq[1], row, col)
                    self.move_feedback = hint
                    self.move_feedback_time = time.time()
            except Exception as e:
                print(f"⚠️  Ошибка при обработке хода: {e}")
                self.renderer.set_selected(None)
                self.renderer.set_move_hints([])
                self.move_feedback = "Ошибка при выполнении хода"
                self.move_feedback_time = time.time()
        else:
            # Клик по пустой клетке без выбранной фигуры - очищаем выделение
            self.renderer.set_selected(None)
            self.renderer.set_move_hints([])
    
    def handle_ai_move(self):
        """
        Получить и выполнить ход ИИ (Stockfish).
        
        Добавляет реалистичную задержку перед ходом.
        """
        if self._is_player_turn() or self.game_over or self.thinking:
            return
        
        # Задержка для более реалистичной игры
        if time.time() - self.last_move_time < self.ai_move_delay:
            return
        
        self.thinking = True
        try:
            # Get the best move with appropriate depth based on skill level
            depth = max(1, min(20, self.skill_level + 5))  # Limit depth between 1 and 20
            
            # Try to get multiple move options for better decision making
            ai_move = None
            best_moves = self.engine.get_best_moves(3)
            
            # If we have multiple options, try to choose a more interesting move
            if len(best_moves) > 1 and self.skill_level < 15:
                # For lower skill levels, sometimes choose a suboptimal but more interesting move
                if random.random() < 0.3:  # 30% chance to choose a different move
                    ai_move = best_moves[min(1, len(best_moves) - 1)]  # Choose second best
                else:
                    ai_move = best_moves[0]  # Choose best move
            else:
                # For higher skill levels or when only one move is available
                ai_move = self.engine.get_best_move(depth=depth)
            
            if ai_move:
                print(f"Ход компьютера: {ai_move}")
                # Validate the move before making it
                if self.engine.is_move_correct(ai_move):
                    if self.engine.make_move(ai_move):
                        self.move_history.append(ai_move)
                        
                        # Очистка кэша доски после хода
                        if hasattr(self, '_cached_board'):
                            delattr(self, '_cached_board')
                        
                        # Преобразование UCI хода в координаты для выделения
                        from_col = ord(ai_move[0]) - ord('a')
                        from_row = 8 - int(ai_move[1])
                        to_col = ord(ai_move[2]) - ord('a')
                        to_row = 8 - int(ai_move[3])
                        self.renderer.set_last_move((from_row, from_col), (to_row, to_col))
                        self.last_move_time = time.time()
                        print(f"Ход компьютера выполнен: {ai_move}")
                        self.move_feedback = f"Ход компьютера: {ai_move}"
                        self.move_feedback_time = time.time()
                        
                        # Add general educational feedback
                        educational_tip = self.educator.get_educational_feedback(
                            len(self.move_history), time.time())
                        if educational_tip:
                            self.move_feedback += f" | {educational_tip}"
                            self.move_feedback_time = time.time()
                        
                        # Add educational feedback for interesting moves
                        if len(best_moves) > 1 and ai_move != best_moves[0]:
                            self.move_feedback += " (интересный выбор!)"
                    else:
                        print("⚠️  Не удалось выполнить ход компьютера")
                        self.move_feedback = "Не удалось выполнить ход компьютера"
                        self.move_feedback_time = time.time()
                else:
                    print("⚠️  Компьютер предложил некорректный ход")
                    self.move_feedback = "Компьютер предложил некорректный ход"
                    self.move_feedback_time = time.time()
            else:
                print("⚠️  Компьютер не смог найти ход")
                self.move_feedback = "Компьютер не смог найти ход"
                self.move_feedback_time = time.time()
        except Exception as e:
            print(f"⚠️  Ошибка при получении хода компьютера: {e}")
            self.move_feedback = "Ошибка при получении хода компьютера"
            self.move_feedback_time = time.time()
        finally:
            self.thinking = False
    
    def _find_king_position(self, board_state: List[List[Optional[str]]], is_white: bool) -> Optional[Tuple[int, int]]:
        """
        Найти позицию короля на доске. Использует кэширование для оптимизации.
        
        Параметры:
            board_state: Состояние доски
            is_white: Искать белого короля (True) или черного (False)
            
        Возвращает:
            Позицию короля (row, col) или None если не найден
        """
        # Создаем ключ для кэширования
        cache_key = (str(board_state), is_white)
        current_time = time.time()
        cache_duration = 1.0  # Кэш действует 1 секунду
        
        # Проверяем кэш
        if hasattr(self, '_king_pos_cache') and hasattr(self, '_king_pos_cache_time'):
            if (cache_key in self._king_pos_cache and 
                current_time - self._king_pos_cache_time[cache_key] < cache_duration):
                return self._king_pos_cache[cache_key]
        
        king_piece = 'K' if is_white else 'k'
        king_pos = None
        for row in range(8):
            for col in range(8):
                if board_state[row][col] == king_piece:
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        # Сохраняем в кэш
        if not hasattr(self, '_king_pos_cache'):
            self._king_pos_cache = {}
            self._king_pos_cache_time = {}
        self._king_pos_cache[cache_key] = king_pos
        self._king_pos_cache_time[cache_key] = current_time
        
        return king_pos

    def _is_king_in_check(self, is_white_king: bool) -> bool:
        """
        Проверить, находится ли король под шахом.
        Используем более точный метод через Stockfish evaluation.
        
        Параметры:
            is_white_king: Проверять белого короля (True) или черного (False)
            
        Возвращает:
            True если король под шахом
        """
        try:
            # Получаем оценку позиции от Stockfish
            # Если король находится под шахом, это будет отражено в оценке
            eval_result = self.engine.get_evaluation()
            if eval_result and isinstance(eval_result, dict):
                # Проверяем специальные поля в оценке, которые указывают на шах
                if 'check' in eval_result and eval_result['check']:
                    # Определяем, чей король под шахом
                    side_to_move = self.engine.get_side_to_move()
                    # Если сейчас ход того же цвета, что и проверяемый король, 
                    # то этот король под шахом
                    is_side_to_move_white = (side_to_move == 'w')
                    return is_side_to_move_white == is_white_king
            
            # Резервный метод - проверяем через движок напрямую
            # Получаем FEN и проверяем флаг шаха в нем
            fen = self.engine.get_fen()
            fen_parts = fen.split()
            if len(fen_parts) > 1:
                # В FEN третий компонент содержит информацию о шахе
                # 'w' - белые, 'b' - черные, '-' - нет шаха
                check_info = fen_parts[1] if len(fen_parts) > 1 else '-'
                if check_info != '-':
                    # Проверяем, соответствует ли цвет короля цвету стороны под шахом
                    is_king_under_check = (is_white_king and check_info == 'w') or \
                                        (not is_white_king and check_info == 'b')
                    return is_king_under_check
                    
            return False
        except Exception:
            # В случае ошибки предполагаем, что король не под шахом
            return False

    def check_game_state(self) -> bool:
        """
        Проверить текущее состояние игры (мат, пат, конец).
        Используем улучшенную логику определения состояния игры.
        
        Возвращает:
            bool: True если игра завершена
        """
        try:
            # Используем улучшенный метод определения окончания игры
            is_over, reason = self.engine.is_game_over()
            if is_over:
                self.game_over = True
                self.game_over_reason = reason
                self.move_feedback = reason
                self.move_feedback_time = time.time()
                
                # Записываем время окончания игры
                self.game_stats['end_time'] = time.time()
                self.game_stats['duration'] = self.game_stats['end_time'] - self.game_stats['start_time']
                
                # Финальная статистика
                if reason and ("мат" in reason or "Мат" in reason):
                    self.game_stats['result'] = "checkmate"
                elif reason and ("Пат" in reason or "пат" in reason or "Ничья" in reason):
                    self.game_stats['result'] = "stalemate"
                else:
                    self.game_stats['result'] = "resignation"
                
                return True
            
            # Проверяем шах через Stockfish evaluation для более точного определения
            try:
                # Определяем, чей сейчас ход
                side_to_move = self.engine.get_side_to_move()
                is_white_to_move = (side_to_move == 'w')
                
                # Получаем оценку позиции для определения шаха
                eval_result = self.engine.get_evaluation()
                is_king_in_check = False
                
                if eval_result and isinstance(eval_result, dict):
                    # Проверяем наличие поля check в оценке
                    if 'check' in eval_result:
                        is_king_in_check = eval_result['check']
                    # Альтернативный метод - проверяем через FEN
                    elif isinstance(eval_result, dict) and eval_result.get('type') == 'cp':
                        # Получаем FEN и проверяем флаг шаха
                        fen = self.engine.get_fen()
                        fen_parts = fen.split()
                        if len(fen_parts) > 1:
                            check_info = fen_parts[1]
                            is_king_in_check = (check_info != '-')
                
                if is_king_in_check:
                    self.game_stats['check_count'] += 1
                    if is_white_to_move:
                        if self.player_color == 'white':
                            self.move_feedback = "⚠️  Ваш король под шахом!"
                        else:
                            self.move_feedback = "✅  Король компьютера под шахом!"
                    else:
                        if self.player_color == 'black':
                            self.move_feedback = "⚠️  Ваш король под шахом!"
                        else:
                            self.move_feedback = "✅  Король компьютера под шахом!"
                    self.move_feedback_time = time.time()
                    
                    # Выделяем клетку с королем
                    board_state = self.engine.get_board_state()
                    king_pos = self._find_king_position(board_state, is_white_to_move)
                    if king_pos:
                        self.renderer.set_check(king_pos)
                    else:
                        self.renderer.set_check(None)
                else:
                    # Снимаем выделение шаха если его нет
                    self.renderer.set_check(None)
                    
            except Exception as e:
                # Игнорируем ошибки при проверке шаха, это только для образовательных целей
                pass
                
            # Check for check state for educational purposes
            # Get raw evaluation from engine (not the processed float version)
            try:
                if self.engine.engine is not None:
                    eval_score = self.engine.engine.get_evaluation()
                    if eval_score and isinstance(eval_score, dict) and eval_score.get('type') == 'mate':
                        mate_in = eval_score.get('value', 0)
                        side = self.engine.get_side_to_move()
                        if mate_in > 0:  # Mate in N moves
                            if (side == 'w' and self.player_color == 'white') or (side == 'b' and self.player_color == 'black'):
                                self.move_feedback = f"⚠️  Вам поставлен мат в {mate_in} ходов!"
                            else:
                                self.move_feedback = f"✅  Вы поставили мат в {mate_in} ходов!"
                            self.move_feedback_time = time.time()
                            self.game_stats['check_count'] += 1
                        elif mate_in < 0:  # Mate in N moves for opponent
                            mate_in = abs(mate_in)
                            if (side == 'w' and self.player_color == 'white') or (side == 'b' and self.player_color == 'black'):
                                self.move_feedback = f"✅  Вы поставите мат в {mate_in} ходов!"
                            else:
                                self.move_feedback = f"⚠️  Вам поставят мат в {mate_in} ходов!"
                            self.move_feedback_time = time.time()
                            self.game_stats['check_count'] += 1
                    elif eval_score and isinstance(eval_score, dict) and eval_score.get('type') == 'cp':
                        # Check for check (positive evaluation for player means advantage)
                        cp_value = eval_score.get('value', 0)
                        # If evaluation is very high, it might indicate a strong advantage
                        if abs(cp_value) > 200:  # More than 2 pawn advantage
                            if (cp_value > 0 and self.player_color == 'white') or (cp_value < 0 and self.player_color == 'black'):
                                self.move_feedback = "✅  У вас сильное преимущество!"
                            else:
                                self.move_feedback = "⚠️  У компьютера сильное преимущество!"
                            self.move_feedback_time = time.time()
            except Exception:
                # Ignore errors in mate detection, it's just for educational purposes
                pass
        except Exception as e:
            print(f"⚠️  Ошибка при проверке состояния игры: {e}")
        return False
    
    def draw_ui(self):
        """Отрисовка пользовательского интерфейса (информационная полоса внизу)."""
        try:
            # Информационная панель внизу экрана
            info_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
            pygame.draw.rect(self.screen, (50, 50, 50), info_rect)
            pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE), 
                           (BOARD_SIZE, BOARD_SIZE), 2)
            
            if self.game_over:
                # Экран окончания игры
                if self.game_over_reason:
                    text = self.ui_font.render(self.game_over_reason, True, (255, 100, 100))
                    self.screen.blit(text, (20, BOARD_SIZE + 15))
                restart_text = self.ui_font.render("Нажмите 'R' для новой игры", 
                                                   True, (200, 200, 200))
                self.screen.blit(restart_text, (20, BOARD_SIZE + 50))
                
                # Отображаем дополнительную статистику в конце игры
                if 'duration' in self.game_stats:
                    duration_text = self.ui_font_small.render(
                        f"Время игры: {int(self.game_stats['duration'])} сек", 
                        True, (150, 150, 150))
                    self.screen.blit(duration_text, (BOARD_SIZE - 150, BOARD_SIZE + 35))
            else:
                # Статус хода
                if self._is_player_turn():
                    status = "🎮 Ваш ход"
                    status_color = (100, 255, 100)
                else:
                    status = "🤖 Ход компьютера"
                    status_color = (100, 150, 255)
                
                text = self.ui_font.render(status, True, status_color)
                self.screen.blit(text, (20, BOARD_SIZE + 15))
                
                # Информация о ходах и взятиях
                moves_text = self.ui_font.render(
                    f"Ходов: {len(self.move_history)} | ♟️ {self.game_stats['player_capture_count']} vs {self.game_stats['ai_capture_count']} ♟️", 
                    True, (200, 200, 200))
                self.screen.blit(moves_text, (20, BOARD_SIZE + 50))
                
                # Уровень сложности
                level_text = self.ui_font.render(f"Уровень: {self.skill_level}/20", 
                                                True, (200, 200, 200))
                self.screen.blit(level_text, (BOARD_SIZE - 150, BOARD_SIZE + 15))
                
                # Подсказка
                hint_text = self.ui_font_small.render(
                    "Подсказка: Кликните по фигуре для показа возможных ходов | Нажмите 'T' для совета", 
                    True, (150, 150, 150))
                self.screen.blit(hint_text, (20, BOARD_SIZE + 75))
                
                # Move feedback (show for 3 seconds)
                if self.move_feedback and time.time() - self.move_feedback_time < 3:
                    feedback_color = (255, 255, 100)  # Yellow feedback
                    feedback_text = self.ui_font.render(self.move_feedback, True, feedback_color)
                    self.screen.blit(feedback_text, 
                                   (BOARD_SIZE // 2 - feedback_text.get_width() // 2, 
                                    BOARD_SIZE + 30))
        except Exception as e:
            print(f"⚠️  Ошибка при отрисовке интерфейса: {e}")
    
    def get_game_stats(self) -> dict:
        """
        Получить статистику текущей игры.
        
        Возвращает:
            dict: Словарь со статистикой игры
        """
        try:
            # Вычисляем дополнительные метрики
            total_moves = len(self.move_history)
            avg_move_time = sum(self.game_stats['move_times']) / len(self.game_stats['move_times']) if self.game_stats['move_times'] else 0
            avg_evaluation = sum(self.game_stats['evaluations']) / len(self.game_stats['evaluations']) if self.game_stats['evaluations'] else 0
            
            stats = {
                'player_color': self.player_color,
                'ai_color': self.ai_color,
                'skill_level': self.skill_level,
                'total_moves': total_moves,
                'player_moves': self.game_stats['player_moves'],
                'ai_moves': self.game_stats['ai_moves'],
                'player_captures': self.game_stats['player_capture_count'],
                'ai_captures': self.game_stats['ai_capture_count'],
                'check_count': self.game_stats['check_count'],
                'avg_move_time': round(avg_move_time, 2),
                'avg_evaluation': round(avg_evaluation, 2),
                'move_history': self.move_history.copy(),
                'fen': self.engine.get_fen(),
                'game_over': self.game_over,
                'game_reason': self.game_over_reason,
                'duration': self.game_stats.get('duration', 0),
                'result': self.game_stats.get('result', 'ongoing')
            }
            
            # Добавляем время окончания, если игра завершена
            if 'end_time' in self.game_stats:
                stats['end_time'] = self.game_stats['end_time']
                
            return stats
        except Exception as e:
            print(f"⚠️  Ошибка при получении статистики игры: {e}")
            return {
                'player_color': self.player_color,
                'ai_color': self.ai_color,
                'skill_level': self.skill_level,
                'total_moves': len(self.move_history),
                'player_moves': self.game_stats['player_moves'],
                'ai_moves': self.game_stats['ai_moves'],
                'player_captures': self.game_stats['player_capture_count'],
                'ai_captures': self.game_stats['ai_capture_count'],
                'check_count': self.game_stats['check_count'],
                'avg_move_time': 0,
                'avg_evaluation': 0,
                'move_history': self.move_history.copy(),
                'fen': '',
                'game_over': self.game_over,
                'game_reason': self.game_over_reason,
                'duration': self.game_stats.get('duration', 0),
                'result': self.game_stats.get('result', 'ongoing')
            }
    
    def _clear_caches(self):
        """Очистить кэши для оптимизации памяти."""
        if hasattr(self, '_uci_cache'):
            self._uci_cache.clear()
        if hasattr(self, '_cached_board'):
            delattr(self, '_cached_board')
        if hasattr(self, '_piece_name_cache'):
            self._piece_name_cache.clear()
        # Очищаем кэш допустимых ходов
        self._valid_moves_cache.clear()
        self._valid_moves_cache_time.clear()
        # Очищаем кэш образовательных подсказок
        if hasattr(self, '_edu_feedback_cache'):
            self._edu_feedback_cache.clear()
        if hasattr(self, '_edu_feedback_cache_time'):
            self._edu_feedback_cache_time.clear()
        # Очищаем кэш подсказок по фигурам
        if hasattr(self, '_piece_hint_cache'):
            self._piece_hint_cache.clear()
        # Очищаем кэш позиции короля
        if hasattr(self, '_king_pos_cache'):
            self._king_pos_cache.clear()
        if hasattr(self, '_king_pos_cache_time'):
            self._king_pos_cache_time.clear()

    def _navigate_to_move(self, move_index: int):
        """
        Навигация к определенному ходу в истории.
        
        Параметры:
            move_index (int): Индекс хода в истории
        """
        if move_index < 0 or move_index >= len(self.move_history):
            return
            
        try:
            # Сбрасываем доску в начальную позицию
            self.engine.reset_board()
            
            # Применяем ходы до нужного индекса
            moves_to_apply = self.move_history[:move_index + 1]
            if moves_to_apply and self.engine.engine is not None:
                self.engine.engine.make_moves_from_current_position(moves_to_apply)
        except Exception as e:
            print(f"Ошибка при навигации к ходу {move_index}: {e}")
    
    def reset_game(self):
        """Сбросить игру к начальному состоянию."""
        print("🔄 Новая игра...")
        
        # Reset the engine to initial position
        self.engine.reset_board()
        
        # Reset game state
        self.move_history = []
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.move_feedback = ""
        self.move_feedback_time = 0
        self.highlight_hint = None
        
        # Reset renderer state
        self.renderer.set_selected(None)
        # For set_last_move, we need to pass valid tuples or avoid calling it with None
        # We'll just reset the last_move attribute directly
        self.renderer.last_move = None
        self.renderer.set_move_hints([])
        self.renderer.set_check(None)
        
        # Reset game stats
        self.game_stats = {
            'start_time': time.time(),
            'player_moves': 0,
            'ai_moves': 0,
            'player_capture_count': 0,
            'ai_capture_count': 0,
            'check_count': 0,
            'move_times': [],  # Время, затраченное на каждый ход
            'evaluations': []  # Оценки позиции
        }
        
        # Reset gameplay enhancements
        self.last_move_was_capture = False
        self.combo_counter = 0
        self.special_move_messages = []
        
        print("[INFO] Игра сброшена до начальной позиции")

        
        print("[INFO] Игра сброшена до начальной позиции")
    
    def _get_changed_squares(self, old_board, new_board):
        """Получить список измененных клеток."""
        changed = set()
        for row in range(8):
            for col in range(8):
                if old_board[row][col] != new_board[row][col]:
                    changed.add((row, col))
                    # Также добавляем соседние клетки для корректного обновления
                    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < 8 and 0 <= nc < 8:
                            changed.add((nr, nc))
        return changed

    def draw_board_optimized(self, board_state):
        """Оптимизированная отрисовка доски - только измененные клетки."""
        current_hash = hash(str(board_state))
        
        # Если доска не изменилась, пропускаем отрисовку
        if self.last_board_hash == current_hash:
            return
            
        self.last_board_hash = current_hash
        
        # Вычисляем измененные клетки
        if hasattr(self, 'previous_board_state'):
            changed_squares = self._get_changed_squares(self.previous_board_state, board_state)
            self.dirty_squares.update(changed_squares)
        
        # Рисуем только измененные клетки
        # Note: We'll use the existing renderer for now, but this could be optimized further
        self.previous_board_state = [row[:] for row in board_state]
        self.dirty_squares.clear()

    def _draw_piece_optimized(self, row, col, piece):
        """Оптимизированная отрисовка фигуры с использованием кэшированных поверхностей."""
        if piece and piece in self.piece_surfaces:
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            self.screen.blit(self.piece_surfaces[piece], (x, y))

    def _draw_highlight_optimized(self, row, col, highlight_type):
        """Оптимизированная отрисовка выделения."""
        if highlight_type in self.highlight_surfaces:
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            self.screen.blit(self.highlight_surfaces[highlight_type], (x, y))

    def _draw_board_with_clipping(self, board_state):
        """Отрисовка доски с использованием clipping regions."""
        # Сохраняем текущий clipping region
        old_clip = self.screen.get_clip()
        
        # Устанавливаем clipping region только для доски
        board_rect = pygame.Rect(0, 0, BOARD_SIZE, BOARD_SIZE)
        self.screen.set_clip(board_rect)
        
        # Используем существующий рендерер
        # В будущем можно заменить на собственную реализацию для большей оптимизации
        evaluation = self.engine.get_evaluation()
        mouse_pos = pygame.mouse.get_pos()
        self.renderer.draw(board_state, evaluation=evaluation, thinking=self.thinking, 
                         mouse_pos=mouse_pos, move_count=len(self.move_history),
                         capture_count=(self.game_stats['player_capture_count'], 
                                      self.game_stats['ai_capture_count']),
                         check_count=self.game_stats['check_count'])
        
        # Восстанавливаем clipping region
        self.screen.set_clip(old_clip)

    def _get_cached_best_move(self, depth=None):
        """
        Получить лучший ход с кэшированием для ускорения работы AI.
        
        Параметры:
            depth (int): Глубина анализа
            
        Возвращает:
            str: Лучший ход в формате UCI
        """
        # Создаем ключ для кэширования
        fen = self.engine.get_fen()
        cache_key = (fen, depth, self.skill_level)
        
        # Проверяем кэш
        current_time = time.time()
        if cache_key in self.ai_move_cache:
            cached_move, cache_time = self.ai_move_cache[cache_key]
            # Используем кэш, если он не старше 5 секунд
            if current_time - cache_time < 5.0:
                return cached_move
        
        # Получаем ход от движка
        best_move = self.engine.get_best_move(depth=depth)
        
        # Сохраняем в кэш
        if best_move:
            self.ai_move_cache[cache_key] = (best_move, current_time)
            
        return best_move

    def _clear_old_ai_cache(self):
        """Очистка старых записей в кэше AI для предотвращения утечек памяти."""
        current_time = time.time()
        expired_keys = []
        
        for key, (_, cache_time) in self.ai_move_cache.items():
            if current_time - cache_time > 10.0:  # Удаляем записи старше 10 секунд
                expired_keys.append(key)
                
        for key in expired_keys:
            del self.ai_move_cache[key]

    def _analyze_position(self):
        """
        Анализ текущей позиции и предоставление рекомендаций.
        """
        try:
            if self.thinking or self.game_over:
                return
                
            self.thinking = True
            best_move = self.engine.get_best_move()
            
            if best_move:
                # Преобразуем UCI ход в координаты
                from_col = ord(best_move[0]) - ord('a')
                from_row = 8 - int(best_move[1])
                to_col = ord(best_move[2]) - ord('a')
                to_row = 8 - int(best_move[3])
                
                # Проверяем, будет ли шах или мат после хода
                is_check = False
                is_mate = False
                is_castling = best_move in ['e1g1', 'e1c1', 'e8g8', 'e8c8']
                is_capture = False
                
                # Проверяем взятие
                try:
                    board_state = self.engine.get_board_state()
                    target_row, target_col = to_row, to_col
                    if 0 <= target_row < 8 and 0 <= target_col < 8:
                        is_capture = board_state[target_row][target_col] is not None
                except:
                    pass
                
                # Проверяем состояние игры после хода
                is_over, reason = self.engine.is_game_over()
                if is_over and reason and "мат" in reason:
                    is_mate = True
                
                # Проверяем шах
                try:
                    eval_result = self.engine.get_evaluation()
                    if eval_result and isinstance(eval_result, dict):
                        is_check = eval_result.get('check', False)
                except:
                    pass
                
                # Аннотируем ход
                annotated_move = self._annotate_move(best_move, is_capture, is_check, is_mate, is_castling)
                
                # Получаем оценку позиции
                evaluation = self.engine.get_evaluation()
                
                if evaluation is not None:
                    # Определяем сторону с преимуществом
                    if evaluation > 0.5:
                        if self.player_color == 'white':
                            advantage = "у вас преимущество"
                        else:
                            advantage = "у компьютера преимущество"
                    elif evaluation < -0.5:
                        if self.player_color == 'black':
                            advantage = "у вас преимущество"
                        else:
                            advantage = "у компьютера преимущество"
                    else:
                        advantage = "позиция равная"
                    
                    self.move_feedback = f"Анализ: {annotated_move} ({advantage})"
                    
                    # Проверяем изменение оценки
                    if abs(evaluation - self.last_evaluation) > 0.5:
                        self.game_stats['advantage_changes'] += 1
                        self.last_evaluation = evaluation
                else:
                    self.move_feedback = f"Анализ: {annotated_move}"
                    
                self.move_feedback_time = time.time()
                
                # Выделяем рекомендуемый ход
                self.analysis_move = ((from_row, from_col), (to_row, to_col))
            else:
                self.move_feedback = "Анализ: нет хорошего хода"
                self.move_feedback_time = time.time()
                self.analysis_move = None
                
        except Exception as e:
            print(f"Ошибка при анализе позиции: {e}")
            self.move_feedback = "Ошибка анализа"
            self.move_feedback_time = time.time()
        finally:
            self.thinking = False
    
    def _save_game(self):
        """
        Сохранить текущую партию.
        """
        try:
            game_state = {
                'player_color': self.player_color,
                'skill_level': self.skill_level,
                'theme': self.theme,
                'move_history': self.move_history.copy(),
                'fen': self.engine.get_fen(),
                'timestamp': time.time(),
                'stats': self.get_game_stats()
            }
            self.saved_games.append(game_state)
            self.move_feedback = "Партия сохранена"
            self.move_feedback_time = time.time()
            print(f"Партия сохранена. Всего сохранено: {len(self.saved_games)}")
        except Exception as e:
            print(f"Ошибка при сохранении партии: {e}")
            self.move_feedback = "Ошибка сохранения"
            self.move_feedback_time = time.time()
    
    def _load_game(self, index: int = -1):
        """
        Загрузить сохраненную партию.
        
        Параметры:
            index (int): Индекс партии для загрузки (по умолчанию - последняя)
        """
        try:
            if not self.saved_games:
                self.move_feedback = "Нет сохраненных партий"
                self.move_feedback_time = time.time()
                return
                
            if index < -len(self.saved_games) or index >= len(self.saved_games):
                self.move_feedback = "Неверный номер партии"
                self.move_feedback_time = time.time()
                return
                
            game_state = self.saved_games[index]
            
            # Восстанавливаем состояние игры
            self.player_color = game_state['player_color']
            self.skill_level = game_state['skill_level']
            self.theme = game_state['theme']
            
            # Обновляем движок
            self.engine.reset_board()
            if game_state['move_history']:
                for move in game_state['move_history']:
                    self.engine.make_move(move)
            
            # Обновляем состояние игры
            self.move_history = game_state['move_history'].copy()
            self.game_over = False
            self.game_over_reason = None
            self.thinking = False
            
            # Обновляем рендерер
            self.renderer.set_player_color(self.player_color)
            self.renderer.set_theme(self.theme)
            self.renderer.set_selected(None)
            self.renderer.set_move_hints([])
            self.renderer.set_check(None)
            self.renderer.last_move = None
            
            # Сбрасываем статистику
            self.game_stats = game_state['stats'].copy() if 'stats' in game_state else {
                'start_time': time.time(),
                'player_moves': 0,
                'ai_moves': 0,
                'player_capture_count': 0,
                'ai_capture_count': 0,
                'check_count': 0,
                'move_times': [],
                'evaluations': [],
                'advantage_changes': 0
            }
            
            self.move_feedback = f"Партия загружена ({len(self.move_history)} ходов)"
            self.move_feedback_time = time.time()
            print(f"Партия загружена: {len(self.move_history)} ходов")
            
        except Exception as e:
            print(f"Ошибка при загрузке партии: {e}")
            self.move_feedback = "Ошибка загрузки"
            self.move_feedback_time = time.time()
    
    def _annotate_move(self, uci_move: str, is_capture: bool = False, is_check: bool = False, 
                      is_mate: bool = False, is_castling: bool = False) -> str:
        """
        Аннотировать ход с помощью специальных символов.
        
        Параметры:
            uci_move (str): Ход в формате UCI
            is_capture (bool): Было ли взятие
            is_check (bool): Был ли шах
            is_mate (bool): Был ли мат
            is_castling (bool): Была ли рокировка
            
        Возвращает:
            str: Аннотированный ход
        """
        annotation = uci_move
        
        # Добавляем символы аннотации
        if is_castling:
            # Короткая рокировка - O-O, длинная - O-O-O
            if uci_move in ['e1g1', 'e8g8']:  # Короткая рокировка
                annotation = "O-O"
            elif uci_move in ['e1c1', 'e8c8']:  # Длинная рокировка
                annotation = "O-O-O"
            
        if is_capture:
            annotation += "x"  # Символ взятия
            
        if is_check and not is_mate:
            annotation += "+"  # Символ шаха
        elif is_mate:
            annotation += "#"  # Символ мата
            
        return annotation
    
    def _get_game_summary(self) -> str:
        """
        Получить краткое резюме игры.
        
        Возвращает:
            str: Резюме игры
        """
        try:
            total_moves = len(self.move_history)
            player_captures = self.game_stats['player_capture_count']
            ai_captures = self.game_stats['ai_capture_count']
            checks = self.game_stats['check_count']
            advantage_changes = self.game_stats['advantage_changes']
            
            if total_moves == 0:
                return "Игра еще не началась"
                
            summary = f"Ходов: {total_moves}, Взятий: {player_captures} vs {ai_captures}"
            
            if checks > 0:
                summary += f", Шахов: {checks}"
                
            if advantage_changes > 0:
                summary += f", Смен преимуществ: {advantage_changes}"
                
            return summary
        except Exception:
            return "Нет данных для резюме"
    
    def _get_detailed_analysis(self) -> str:
        """
        Получить подробный анализ игры с стратегическими рекомендациями.
        
        Возвращает:
            str: Подробный анализ игры
        """
        try:
            total_moves = len(self.move_history)
            if total_moves == 0:
                return "Игра еще не началась"
            
            player_captures = self.game_stats['player_capture_count']
            ai_captures = self.game_stats['ai_capture_count']
            checks = self.game_stats['check_count']
            advantage_changes = self.game_stats['advantage_changes']
            avg_move_time = sum(self.game_stats['move_times']) / len(self.game_stats['move_times']) if self.game_stats['move_times'] else 0
            
            # Определяем стиль игры
            style = ""
            if player_captures > ai_captures * 1.5:
                style = "агрессивный"
            elif player_captures < ai_captures * 0.7:
                style = "позиционный"
            else:
                style = "сбалансированный"
            
            # Анализируем время ходов
            time_analysis = ""
            if avg_move_time < 5:
                time_analysis = "быстрое принятие решений"
            elif avg_move_time > 15:
                time_analysis = "тщательное обдумывание позиции"
            else:
                time_analysis = "умеренное время на размышления"
            
            # Анализируем смены преимуществ
            advantage_analysis = ""
            if advantage_changes == 0:
                advantage_analysis = "стабильная позиция"
            elif advantage_changes < 3:
                advantage_analysis = "небольшие колебания преимущества"
            else:
                advantage_analysis = "динамичная игра с частыми сменами преимуществ"
            
            # Формируем анализ
            analysis = f"Стиль игры: {style}\n"
            analysis += f"Время ходов: {time_analysis} (среднее {avg_move_time:.1f} сек)\n"
            analysis += f"Позиция: {advantage_analysis}\n"
            
            # Добавляем рекомендации
            recommendations = []
            if player_captures < ai_captures:
                recommendations.append("Попробуйте чаще атаковать фигуры противника")
            if checks == 0:
                recommendations.append("Ищите возможности поставить шах")
            if avg_move_time < 3:
                recommendations.append("Уделите больше времени анализу позиции")
            elif avg_move_time > 30:
                recommendations.append("Иногда достаточно и быстрого хода")
            
            if recommendations:
                analysis += "Рекомендации:\n"
                for i, rec in enumerate(recommendations, 1):
                    analysis += f"  {i}. {rec}\n"
            
            return analysis.strip()
        except Exception as e:
            return f"Ошибка при анализе: {e}"
    
    def handle_ai_move_optimized(self):
        """
        Оптимизированная обработка хода ИИ (Stockfish) с улучшенной производительностью.
        """
        if self._is_player_turn() or self.game_over or self.thinking:
            return
        
        # Проверка минимальной задержки
        current_time = time.time()
        if current_time - self.last_ai_move_time < self.ai_move_cooldown:
            return
        
        # Задержка для более реалистичной игры
        if current_time - self.last_move_time < self.ai_move_delay:
            return
        
        self.thinking = True
        self.last_ai_move_time = current_time
        
        # Засекаем время начала хода для статистики
        move_start_time = time.time()
        
        try:
            # Очищаем старый кэш
            self._clear_old_ai_cache()
            
            # Получаем лучший ход с оптимальной глубиной анализа
            depth = max(1, min(15, self.skill_level + 3))  # Ограниченная глубина для скорости
            
            # Для низких уровней сложности используем кэшированные ходы
            ai_move = None
            if self.skill_level < 10:
                # Пытаемся получить ход из кэша
                ai_move = self._get_cached_best_move(depth=depth)
            
            # Если нет кэшированного хода, получаем новый
            if not ai_move:
                ai_move = self._get_cached_best_move(depth=depth)
            
            if ai_move:
                print(f"Ход компьютера: {ai_move}")
                
                # Получаем текущее состояние доски для проверки взятия
                board_before = self.engine.get_board_state()
                
                # Валидация хода
                if self.engine.is_move_correct(ai_move):
                    if self.engine.make_move(ai_move):
                        self.move_history.append(ai_move)
                        self.game_stats['ai_moves'] += 1
                        
                        # Проверяем, было ли взятие
                        board_after = self.engine.get_board_state()
                        # Преобразуем UCI ход в координаты
                        to_col = ord(ai_move[2]) - ord('a')
                        to_row = 8 - int(ai_move[3])
                        target_piece = board_before[to_row][to_col]
                        is_capture = target_piece is not None
                        # Проверяем, будет ли шах или мат после хода
                        is_check = False
                        is_mate = False
                        is_castling = ai_move in ['e1g1', 'e1c1', 'e8g8', 'e8c8']
                        
                        # Проверяем состояние игры после хода
                        is_over, reason = self.engine.is_game_over()
                        if is_over and reason and "мат" in reason:
                            is_mate = True
                        
                        # Проверяем шах
                        try:
                            eval_result = self.engine.get_evaluation()
                            if eval_result and isinstance(eval_result, dict):
                                is_check = eval_result.get('check', False)
                        except:
                            pass
                        
                        # Аннотируем ход
                        annotated_move = self._annotate_move(ai_move, is_capture, is_check, is_mate, is_castling)
                        
                        if is_capture:
                            self.game_stats['ai_capture_count'] += 1
                            self.move_feedback = f"Ход компьютера: {annotated_move} (взятие!)"
                        else:
                            self.move_feedback = f"Ход компьютера: {annotated_move}"
                        
                        # Преобразование UCI хода в координаты для выделения
                        from_col = ord(ai_move[0]) - ord('a')
                        from_row = 8 - int(ai_move[1])
                        to_col = ord(ai_move[2]) - ord('a')
                        to_row = 8 - int(ai_move[3])
                        self.renderer.set_last_move((from_row, from_col), (to_row, to_col))
                        self.last_move_time = current_time
                        print(f"Ход компьютера выполнен: {annotated_move}")
                        self.move_feedback_time = current_time
                        
                        # Записываем время хода в статистику
                        move_time = time.time() - move_start_time
                        self.game_stats['move_times'].append(move_time)
                        
                        # Получаем оценку позиции для статистики
                        evaluation = self.engine.get_evaluation()
                        if evaluation is not None:
                            self.game_stats['evaluations'].append(evaluation)
                        
                        # Добавляем образовательную обратную связь
                        educational_tip = self.educator.get_educational_feedback(
                            len(self.move_history), current_time)
                        if educational_tip:
                            self.move_feedback += f" | {educational_tip}"
                            self.move_feedback_time = current_time
                            
                        # Очищаем кэш состояния доски после хода
                        self.board_state_cache = None
                    else:
                        print("⚠️  Не удалось выполнить ход компьютера")
                        self.move_feedback = "Не удалось выполнить ход компьютера"
                        self.move_feedback_time = current_time
                else:
                    print("⚠️  Компьютер предложил некорректный ход")
                    self.move_feedback = "Компьютер предложил некорректный ход"
                    self.move_feedback_time = current_time
            else:
                print("⚠️  Компьютер не смог найти ход")
                self.move_feedback = "Компьютер не смог найти ход"
                self.move_feedback_time = current_time
        except Exception as e:
            print(f"⚠️  Ошибка при получении хода компьютера: {e}")
            self.move_feedback = "Ошибка при получении хода компьютера"
            self.move_feedback_time = time.time()
        finally:
            self.thinking = False

    def run(self):
        """
        Запустить основной цикл игры с оптимизациями.
        
        Обрабатывает события, обновляет состояние и отрисовывает кадры.
        """
        print(f"\n{'='*60}")
        print(f"🎮 Игра началась!")
        print(f"   Вы играете: {self.player_color.upper()}")
        print(f"   Компьютер: {self.ai_color.upper()}")
        print(f"   Уровень: {self.skill_level}/20")
        print(f"   Горячие клавиши: R - новая игра, ESC - выход, T - подсказка")
        print(f"   Дополнительно: ПКМ - снять выделение, ←/→ - навигация по ходам")
        print(f"   Доп. функции: A - анализ, S - сохранить, L - загрузить, D - детальный анализ, G - резюме игры")
        print(f"{'='*60}\n")
        
        running = True
        
        # Таймеры для оптимизированных обновлений
        last_board_update = time.time()
        last_ui_update = time.time()
        last_ai_update = time.time()
        
        # Интервалы обновлений (повышена частота для более плавной игры)
        board_update_interval = 1.0/60  # 60 FPS для доски
        ui_update_interval = 1.0/30     # 30 FPS для UI
        ai_update_interval = 0.1       # AI проверяется каждые 100ms
        
        # Флаги для отслеживания изменений
        board_needs_update = True
        ui_needs_update = True
        last_board_state: Optional[List[List[Optional[str]]]] = None
        
        # Для навигации по ходам
        move_navigation_mode = False
        current_move_index = -1  # -1 означает текущую позицию
        
        while running:
            current_time = time.time()
            has_events = False
            
            # === Обработка событий ===
            for event in pygame.event.get():
                has_events = True
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    # Сброс игры
                    if event.key == pygame.K_r:
                        self.reset_game()
                        board_needs_update = True
                        ui_needs_update = True
                        last_board_state = None  # Сброс кэша состояния доски
                        move_navigation_mode = False
                        current_move_index = -1
                        self.analysis_mode = False
                        self.analysis_move = None
                    # Подсказка (ход Stockfish)
                    elif event.key == pygame.K_t:
                        if not self.game_over and self._is_player_turn():
                            self.thinking = True
                            # Get best move from engine with caching
                            best_move = self._get_cached_best_move()
                            self.thinking = False
                            if best_move:
                                print(f"[ENGINE] Совет: {best_move}")
                                self.highlight_hint = best_move
                                # Show hint for 3 seconds
                                self.move_feedback = f"Подсказка: {best_move}"
                                self.move_feedback_time = time.time()
                                ui_needs_update = True
                            else:
                                self.move_feedback = "Не удалось получить подсказку"
                                self.move_feedback_time = time.time()
                                ui_needs_update = True
                    # Навигация по ходам (влево/вправо)
                    elif event.key == pygame.K_LEFT and len(self.move_history) > 0:
                        move_navigation_mode = True
                        if current_move_index == -1:
                            current_move_index = len(self.move_history) - 1
                        elif current_move_index > 0:
                            current_move_index -= 1
                        self._navigate_to_move(current_move_index)
                        board_needs_update = True
                        ui_needs_update = True
                    elif event.key == pygame.K_RIGHT and move_navigation_mode:
                        if current_move_index < len(self.move_history) - 1:
                            current_move_index += 1
                            self._navigate_to_move(current_move_index)
                        else:
                            # Возвращаемся к текущей позиции
                            move_navigation_mode = False
                            current_move_index = -1
                            self.engine.set_fen(self.engine.get_fen())  # Обновляем позицию
                        board_needs_update = True
                        ui_needs_update = True
                    # Анализ позиции
                    elif event.key == pygame.K_a:
                        if not self.game_over:
                            self._analyze_position()
                            ui_needs_update = True
                    # Сохранить партию
                    elif event.key == pygame.K_s:
                        self._save_game()
                        ui_needs_update = True
                    # Загрузить партию
                    elif event.key == pygame.K_l:
                        self._load_game()
                        board_needs_update = True
                        ui_needs_update = True
                    # Получить резюме игры
                    elif event.key == pygame.K_g:
                        summary = self._get_game_summary()
                        self.move_feedback = f"Резюме: {summary}"
                        self.move_feedback_time = time.time()
                        ui_needs_update = True
                    # Получить подробный анализ игры
                    elif event.key == pygame.K_d:
                        analysis = self._get_detailed_analysis()
                        self.move_feedback = f"Анализ: {analysis.split(chr(10))[0]}"  # Показываем первую строку
                        self.move_feedback_time = time.time()
                        ui_needs_update = True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # ЛКМ
                        pos = pygame.mouse.get_pos()
                        self.handle_click(pos[0], pos[1])
                        board_needs_update = True
                        ui_needs_update = True
                        last_board_state = None  # Сброс кэша состояния доски
                        # Выход из режима навигации при клике
                        if move_navigation_mode:
                            move_navigation_mode = False
                            current_move_index = -1
                        # Выход из режима анализа при клике
                        if self.analysis_mode:
                            self.analysis_mode = False
                            self.analysis_move = None
                    elif event.button == 3:  # ПКМ - снять выделение
                        self.renderer.set_selected(None)
                        self.renderer.set_move_hints([])
                        board_needs_update = True
                        ui_needs_update = True

            # === Оптимизированное обновление и отрисовка ===
            
            # Проверяем, нужно ли обновлять доску
            time_to_update_board = (current_time - last_board_update > board_update_interval)
            time_to_update_ai = (current_time - last_ai_update > ai_update_interval)
            
            # Получаем текущее состояние доски для сравнения
            current_board_state: List[List[Optional[str]]] = self.get_board_state()
            
            # Проверяем, изменилась ли доска
            board_changed = (last_board_state is None or 
                           str(last_board_state) != str(current_board_state))
            
            if board_changed or (time_to_update_board and board_needs_update) or time_to_update_ai:
                # Update hover square
                mouse_pos = pygame.mouse.get_pos()
                self.renderer.update_hover(mouse_pos)
                
                # Handle AI moves с оптимизацией
                if time_to_update_ai and not self.game_over:
                    # Проверяем, наша ли очередь хода
                    if not self._is_player_turn():
                        self.handle_ai_move_optimized()
                        last_ai_update = current_time
                        # После хода AI доска точно изменилась
                        board_needs_update = True
                        last_board_state = None  # Принудительно обновим кэш
                
                # Draw the board with optimizations
                if time_to_update_board and (board_needs_update or board_changed):
                    # Используем clipping для оптимизации
                    old_clip = self.screen.get_clip()
                    board_rect = pygame.Rect(0, 0, BOARD_SIZE, BOARD_SIZE)
                    self.screen.set_clip(board_rect)
                    
                    # Отрисовка через рендерер
                    evaluation = self.get_cached_evaluation()
                    self.renderer.draw(current_board_state, evaluation=evaluation, thinking=self.thinking, 
                                     mouse_pos=mouse_pos, move_count=len(self.move_history),
                                     capture_count=(self.game_stats['player_capture_count'], 
                                                  self.game_stats['ai_capture_count']),
                                     check_count=self.game_stats['check_count'])
                    
                    # Добавляем визуализацию анализа, если в режиме анализа
                    if self.analysis_mode and self.analysis_move:
                        from_pos, to_pos = self.analysis_move
                        from_rect = self.renderer._get_square_rect(from_pos[0], from_pos[1])
                        to_rect = self.renderer._get_square_rect(to_pos[0], to_pos[1])
                        
                        # Рисуем стрелку от начальной позиции к конечной
                        pygame.draw.line(self.screen, (0, 255, 0), from_rect.center, to_rect.center, 3)
                        # Рисуем круг в конечной позиции
                        pygame.draw.circle(self.screen, (0, 255, 0), to_rect.center, 10, 3)
                    
                    self.screen.set_clip(old_clip)
                    last_board_update = current_time
                    board_needs_update = False
                    last_board_state = [row[:] for row in current_board_state]  # Копируем состояние
            
            # Обновляем UI только при необходимости
            if (current_time - last_ui_update > ui_update_interval) and ui_needs_update:
                self.draw_ui()
                last_ui_update = current_time
                ui_needs_update = False

            # === Очистка кэша для предотвращения утечек памяти ===
            self.frame_count += 1
            if self.frame_count % 1800 == 0:  # Каждые 30 секунд при 60 FPS
                self.renderer.clear_temp_surfaces()
                self._clear_caches()
                self._clear_old_ai_cache()

            # === Обновление экрана только при необходимости ===
            if board_needs_update or ui_needs_update or has_events or board_changed:
                pygame.display.flip()

            # === Ограничение FPS ===
            self.clock.tick(60)

        # === Завершение работы ===
        self.renderer.cleanup()
        pygame.quit()

        # === Возврат статистики ===
        print("[INFO] Игра завершена.")
        return self.get_game_stats()
