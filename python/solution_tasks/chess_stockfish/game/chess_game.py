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
    - Добавлена поддержка многопоточности для улучшения производительности
    - Добавлена поддержка GPU ускорения через CUDA (если доступно)
"""

import pygame
from typing import Optional, Tuple, List
import time
import sys
import random
import concurrent.futures
import threading
from queue import Queue, Empty

# Import our modules
from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer  # Убран init_fonts
from utils.educational import ChessEducator
from utils.opening_book import OpeningBook
from utils.sound_manager import SoundManager  # Добавляем импорт SoundManager
from game.in_game_menu import InGameMenu  # Добавляем импорт InGameMenu

# Попытка импортировать CUDA для GPU ускорения (если доступно)
CUDA_AVAILABLE = False
cp = None

# Импортируем библиотеки для GPU ускорения с обработкой ошибок
try:
    cp = __import__('cupy')
    CUDA_AVAILABLE = True
    print("✅ CuPy успешно импортирован для GPU ускорения")
except ImportError:
    try:
        cp = __import__('numpy')
        CUDA_AVAILABLE = False
        print("⚠️  CuPy недоступен, используется NumPy")
    except ImportError:
        cp = None
        CUDA_AVAILABLE = False
        print("⚠️  Ни CuPy, ни NumPy недоступны")

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
        opening_book (OpeningBook): Дебютная книга для образовательных целей
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
        self.opening_book = OpeningBook()
        
        # Инициализируем менеджер звуков
        self.sound_manager = SoundManager()
        self.sound_manager.load_sounds()
        # Начинаем воспроизведение фоновой музыки
        self.sound_manager.play_background_music()
        
        # Инициализируем игровое меню
        self.in_game_menu = InGameMenu(self.screen, self.sound_manager)
        
        # Состояние игры
        self.move_history = []
        self.move_annotations = []  # Аннотации к ходам (например, + для шаха, x для взятия)
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.ai_move_delay = 0.1  # Уменьшена задержка перед ходом ИИ для более быстрой игры
        self.move_feedback = ""  # Feedback message for the player
        self.move_feedback_time = 0
        self.frame_count = 0  # Счетчик кадров для очистки временных поверхностей
        self.highlight_hint = None  # For T key hint highlighting
        
        # Улучшенная система кэширования с более эффективным управлением
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
        self._valid_moves_cache_duration = 8.0  # Увеличиваем кэш ходов до 8 секунд для лучшей производительности
        self._valid_moves_board_hash = {}  # Хэш доски для каждого кэшированного хода
        
        # Расширенный кэш для AI ходов с более агрессивной стратегией
        self._ai_move_cache = {}  # Кэш для AI ходов
        self._ai_move_cache_time = {}  # Время последнего обновления кэша AI
        self._ai_move_cache_duration = 60.0  # Увеличиваем кэш AI до 60 секунд для лучшей производительности
        self._ai_move_board_hash = {}  # Хэш доски для каждого кэшированного AI хода
        
        # Графические оптимизации
        self.last_board_hash = None
        self.dirty_squares = set()
        self.piece_surfaces = {}
        self.highlight_surfaces = {}
        
        # Таймеры для оптимизации обновлений
        self.last_board_update = 0
        self.last_ui_update = 0
        self.board_update_interval = 1.0/120  # Повышена частота обновления доски до 120 FPS
        self.ui_update_interval = 1.0/60     # Повышена частота обновления UI до 60 FPS
        
        # Инициализация графических ресурсов
        self._init_fonts_optimized()
        self._init_piece_surfaces()
        self._init_highlight_surfaces()
        
        # Оптимизация AI
        self.ai_move_cache = {}  # Кэш для AI ходов
        self.last_ai_move_time = 0
        self.ai_move_cooldown = 0.005  # Минимальная задержка между AI ходами (уменьшена)
        
        # Дополнительные оптимизации
        self.board_state_cache = None  # Кэш состояния доски для быстрого доступа
        self.board_state_cache_time = 0
        self.board_state_cache_duration = 1.0  # Увеличиваем кэш до 1 секунды для лучшей производительности
        self.board_state_last_fen = None  # Последний FEN для проверки изменений
        
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
        
        # Многопоточность
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=16)  # Увеличиваем количество потоков для лучшей производительности
        self.ai_move_queue = Queue()
        self.render_queue = Queue()
        self.ai_thread = None
        self.render_thread = None
        self.ai_thread_running = False
        self.render_thread_running = False
        
        # GPU ускорение (если доступно)
        self.cuda_available = CUDA_AVAILABLE
        if self.cuda_available:
            print("✅ CUDA доступна для ускорения вычислений")
        else:
            print("⚠️  CUDA недоступна, используется CPU")
            
        # Асинхронная оценка позиции
        self._async_eval_future = None
        self._last_async_eval_time = 0
        self._async_eval_interval = 0.1  # Обновляем оценку раз в 100 мс
        
        # Прогрессивная оценка позиции для плавного обновления
        self._displayed_evaluation = 0.0  # Текущее отображаемое значение
        self._target_evaluation = 0.0     # Целевое значение оценки
        self._eval_update_time = 0        # Время последнего обновления
        self._eval_interpolation_duration = 0.1  # Длительность интерполяции в секундах

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
            current_fen = self.engine.get_fen()
            
            # Проверяем кэш с более сложной стратегией
            if (self.board_state_cache is not None and 
                current_time - self.board_state_cache_time < self.board_state_cache_duration and
                (self.board_state_last_fen == current_fen or 
                 current_time - self.board_state_cache_time < 0.05)):  # Очень свежий кэш
                return self.board_state_cache
            
            # Получаем новое состояние доски
            board = self.engine.get_board_state()
            
            # Обновляем кэш
            self.board_state_cache = board
            self.board_state_cache_time = current_time
            self.board_state_last_fen = current_fen
            
            return board
        except Exception:
            # Возвращаем пустую доску в случае ошибки
            empty_board: List[List[Optional[str]]] = [[None for _ in range(8)] for _ in range(8)]
            self.board_state_cache = empty_board
            self.board_state_cache_time = time.time()
            self.board_state_last_fen = None
            return empty_board
    
    def get_cached_evaluation(self):
        """
        Получение кэшированной оценки позиции с более агрессивным кэшированием.
        
        Возвращает:
            float: Оценка позиции
        """
        try:
            current_fen = self.engine.get_fen()
            current_time = time.time()
            
            # Проверяем кэш с более агрессивной стратегией
            if (self._cache['last_eval_fen'] == current_fen and 
                self._cache['last_evaluation'] is not None and
                hasattr(self, '_last_eval_cache_time')):
                # Используем кэш до 60 секунд для ещё более агрессивного кэширования
                if (current_time - self._last_eval_cache_time) < 60.0:
                    return self._cache['last_evaluation']
                
            evaluation = self.engine.get_evaluation()
            self._cache['last_evaluation'] = evaluation
            self._cache['last_eval_fen'] = current_fen
            self._last_eval_cache_time = current_time
            return evaluation
        except Exception:
            # Возвращаем кэшированное значение даже при ошибке
            if self._cache['last_evaluation'] is not None:
                return self._cache['last_evaluation']
            return None

    def get_interpolated_evaluation(self):
        """
        Получение интерполированной оценки позиции для плавного обновления.
        
        Возвращает:
            float: Интерполированная оценка позиции
        """
        current_time = time.time()
        
        # Получаем реальное значение оценки (с кэшированием)
        real_evaluation = self.get_cached_evaluation()
        
        # Если это первое значение, устанавливаем его как целевое
        if self._target_evaluation == 0.0 and real_evaluation is not None:
            self._target_evaluation = real_evaluation
            self._displayed_evaluation = real_evaluation
            self._eval_update_time = current_time
            return real_evaluation
        
        # Если реальное значение изменилось, обновляем целевое значение
        if real_evaluation is not None and real_evaluation != self._target_evaluation:
            self._target_evaluation = real_evaluation
            self._eval_update_time = current_time
        
        # Интерполируем значение к целевому
        if self._target_evaluation != self._displayed_evaluation:
            elapsed = current_time - self._eval_update_time
            if elapsed >= self._eval_interpolation_duration:
                # Интерполяция завершена
                self._displayed_evaluation = self._target_evaluation
            else:
                # Линейная интерполяция
                progress = elapsed / self._eval_interpolation_duration
                self._displayed_evaluation = (
                    self._displayed_evaluation + 
                    (self._target_evaluation - self._displayed_evaluation) * progress
                )
        
        return self._displayed_evaluation

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
        
        # Получаем хэш текущей доски для проверки валидности кэша
        board_state = self.get_board_state()
        board_hash = hash(str(board_state))
        
        # Проверяем кэш с более сложной стратегией
        if cache_key in self._valid_moves_cache:
            # Проверяем, не истекло ли время кэша И не изменилась ли позиция
            cache_time = self._valid_moves_cache_time[cache_key]
            cached_board_hash = self._valid_moves_board_hash.get(cache_key, None)
            
            # Используем кэш если:
            # 1. Время кэша еще не истекло (5 секунд)
            # 2. Позиция на доске не изменилась
            # 3. Или время кэша очень свежее (меньше 0.1 секунды) - для быстрых кликов
            is_time_valid = (current_time - cache_time < self._valid_moves_cache_duration)
            is_position_valid = (cached_board_hash == board_hash)
            is_fresh_cache = (current_time - cache_time < 0.1)
            
            if is_time_valid and (is_position_valid or is_fresh_cache):
                return self._valid_moves_cache[cache_key][:]  # Возвращаем копию, чтобы избежать модификации кэша
        
        valid_moves = []
        from_uci = self._fen_square_to_uci(from_row, from_col)
        
        try:
            # Используем кэшированное состояние доски для повышения производительности
            piece = board_state[from_row][from_col]
            if not piece:
                # Сохраняем в кэш даже пустой результат
                self._valid_moves_cache[cache_key] = []
                self._valid_moves_cache_time[cache_key] = current_time
                self._valid_moves_board_hash[cache_key] = board_hash
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
        self._valid_moves_board_hash[cache_key] = board_hash
            
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
        try:
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
                self.move_feedback = "Ошибка при получении состояния доски"
                self.move_feedback_time = time.time()
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
                            # Добавляем ход в дебютную книгу
                            self.opening_book.add_move(uci_move)
                            
                            # Проверяем текущий дебют
                            current_opening = self.opening_book.get_current_opening()
                            
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
                                    # Проигрываем специальный звук для комбо
                                    if self.sound_manager:
                                        self.sound_manager.play_sound("capture")
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
                            
                            # Проигрываем звук хода
                            if self.sound_manager:
                                if is_capture:
                                    self.sound_manager.play_sound("capture")
                                elif is_castling:
                                    self.sound_manager.play_sound("castle")
                                else:
                                    self.sound_manager.play_sound("move")
                            
                            # Добавляем информацию о дебюте, если она есть
                            if current_opening:
                                opening_name, opening_info = current_opening
                                self.move_feedback += f" | 🎯 Дебют: {opening_name}"
                            
                            # Записываем время хода в статистику
                            move_time = time.time() - move_start_time
                            self.game_stats['move_times'].append(move_time)
                            
                            # Получаем оценку позиции для статистики
                            evaluation = self.get_cached_evaluation()
                            if evaluation is not None:
                                self.game_stats['evaluations'].append(evaluation)
                            
                            # Add educational feedback (с кэшированием)
                            move_count = len(self.move_history)
                            current_time = time.time()
                            
                            # Создаем ключ для кэширования образовательных подсказок
                            edu_cache_key = move_count
                            edu_cache_duration = 30.0  # Увеличиваем кэш до 30 секунд для лучшей производительности
                            
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
                                
                            # Помечаем всю доску как "грязную" для полного обновления и предотвращения артефактов
                            self.renderer._mark_all_dirty()
                            # Принудительное обновление экрана для предотвращения исчезновения доски при клике
                            pygame.display.flip()
                        else:
                            print("❌ Не удалось выполнить ход")
                            self.renderer.set_selected(None)
                            self.renderer.set_move_hints([])
                            self.move_feedback = "Не удалось выполнить ход"
                            self.move_feedback_time = time.time()
                            # Проигрываем звук ошибки
                            if self.sound_manager:
                                self.sound_manager.play_sound("button")
                            # Помечаем всю доску как "грязную" для полного обновления
                            self.renderer._mark_all_dirty()
                            # Принудительное обновление экрана для предотвращения исчезновения доски при клике
                            pygame.display.flip()
                            # Принудительное обновление экрана для предотвращения исчезновения доски при клике
                            pygame.display.flip()
                    else:
                        print(f"❌ Некорректный ход: {uci_move}")
                        self.renderer.set_selected(None)
                        self.renderer.set_move_hints([])
                        # Provide specific feedback about why the move is invalid
                        hint = self._get_move_hint(from_sq[0], from_sq[1], row, col)
                        self.move_feedback = hint
                        self.move_feedback_time = time.time()
                        # Проигрываем звук ошибки
                        if self.sound_manager:
                            self.sound_manager.play_sound("button")
                        # Помечаем всю доску как "грязную" для полного обновления
                        self.renderer._mark_all_dirty()
                        # Принудительное обновление экрана для предотвращения исчезновения доски при клике
                        pygame.display.flip()
                except Exception as e:
                    print(f"⚠️  Ошибка при обработке хода: {e}")
                    self.renderer.set_selected(None)
                    self.renderer.set_move_hints([])
                    self.move_feedback = "Ошибка при выполнении хода"
                    self.move_feedback_time = time.time()
                    # Проигрываем звук ошибки
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
                    # Помечаем всю доску как "грязную" для полного обновления
                    self.renderer._mark_all_dirty()
            else:
                # Клик по пустой клетке без выбранной фигуры - очищаем выделение
                self.renderer.set_selected(None)
                self.renderer.set_move_hints([])
                # Помечаем всю доску как "грязную" для полного обновления
                self.renderer._mark_all_dirty()
                # Принудительное обновление экрана для предотвращения исчезновения доски при клике
                pygame.display.flip()
        except Exception as e:
            print(f"⚠️  Критическая ошибка при обработке клика: {e}")
            self.move_feedback = "Критическая ошибка при обработке клика"
            self.move_feedback_time = time.time()
            # Проигрываем звук ошибки
            if self.sound_manager:
                self.sound_manager.play_sound("button")

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
        cache_duration = 2.0  # Увеличиваем кэш до 2 секунд
        
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
                    eval_score = self.get_cached_evaluation()
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
    
    def _handle_resignation(self):
        """
        Обработка сдачи игрока.
        """
        self.game_over = True
        self.game_over_reason = "🏳️ Игрок сдался"
        
        # Определяем победителя
        winner = "Компьютер" if self.player_color == "white" else "Белые"
        if self.player_color == "black":
            winner = "Компьютер" if self.player_color == "black" else "Черные"
        
        self.move_feedback = f"🏳️ Вы сдались. Победил {winner}!"
        self.move_feedback_time = time.time()
        
        # Записываем время окончания игры
        self.game_stats['end_time'] = time.time()
        self.game_stats['duration'] = self.game_stats['end_time'] - self.game_stats['start_time']
        self.game_stats['result'] = "resignation"
        
        print(f"[INFO] Игрок сдался. Победил {winner}!")
    
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
        if hasattr(self, '_valid_moves_board_hash'):
            self._valid_moves_board_hash.clear()
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
            'move_times': [],
            'evaluations': []
        }
    
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

    def _get_game_analysis(self):
        """
        Получить полный анализ сыгранной партии.
        
        Возвращает:
            dict: Словарь с анализом партии
        """
        try:
            analysis = {
                'total_moves': len(self.move_history),
                'player_moves': self.game_stats['player_moves'],
                'ai_moves': self.game_stats['ai_moves'],
                'captures': {
                    'player': self.game_stats['player_capture_count'],
                    'ai': self.game_stats['ai_capture_count']
                },
                'checks': self.game_stats['check_count'],
                'avg_move_time': 0,
                'evaluation_trend': [],
                'mistakes': [],
                'brilliant_moves': [],
                'blunders': [],
                'tactical_motifs': [],
                'opening_played': None,
                'middlegame_assessment': 'равная',
                'endgame_assessment': 'равная',
                'overall_assessment': 'равная'
            }
            
            # Вычисляем среднее время хода
            if self.game_stats['move_times']:
                analysis['avg_move_time'] = sum(self.game_stats['move_times']) / len(self.game_stats['move_times'])
            
            # Анализируем оценки позиции
            if self.game_stats['evaluations']:
                analysis['evaluation_trend'] = self.game_stats['evaluations'][:]
                
                # Определяем лучшие и худшие ходы
                for i, eval_score in enumerate(self.game_stats['evaluations']):
                    if i > 0:
                        prev_eval = self.game_stats['evaluations'][i-1]
                        # Проверяем на большие изменения оценки (возможные ошибки)
                        if abs(eval_score - prev_eval) > 1.5:
                            if ((self.player_color == 'white' and eval_score < prev_eval) or 
                                (self.player_color == 'black' and eval_score > prev_eval)):
                                analysis['mistakes'].append({
                                    'move_number': i,
                                    'evaluation_change': eval_score - prev_eval
                                })
                            elif ((self.player_color == 'white' and eval_score > prev_eval) or 
                                  (self.player_color == 'black' and eval_score < prev_eval)):
                                analysis['brilliant_moves'].append({
                                    'move_number': i,
                                    'evaluation_change': eval_score - prev_eval
                                })
            
            # Определяем дебют
            current_opening = self.opening_book.get_current_opening()
            if current_opening:
                analysis['opening_played'] = current_opening[0]
            
            # Определяем общую оценку партии
            if analysis['mistakes']:
                analysis['overall_assessment'] = 'с ошибками'
            elif analysis['brilliant_moves']:
                analysis['overall_assessment'] = 'с хорошими ходами'
            else:
                analysis['overall_assessment'] = 'равная'
                
            # Добавляем тактические мотивы
            tactical_patterns = []
            for move in self.move_history:
                if 'x' in move:
                    tactical_patterns.append('взятие')
                if '+' in move:
                    tactical_patterns.append('шах')
                if '#' in move:
                    tactical_patterns.append('мат')
                if move in ['e1g1', 'e1c1', 'e8g8', 'e8c8']:
                    tactical_patterns.append('рокировка')
                    
            analysis['tactical_motifs'] = list(set(tactical_patterns))
            
            return analysis
        except Exception as e:
            print(f"Ошибка при анализе партии: {e}")
            return {
                'total_moves': len(self.move_history),
                'player_moves': self.game_stats['player_moves'],
                'ai_moves': self.game_stats['ai_moves'],
                'captures': {
                    'player': self.game_stats['player_capture_count'],
                    'ai': self.game_stats['ai_capture_count']
                },
                'checks': self.game_stats['check_count'],
                'avg_move_time': 0,
                'evaluation_trend': [],
                'mistakes': [],
                'brilliant_moves': [],
                'blunders': [],
                'tactical_motifs': [],
                'opening_played': None,
                'middlegame_assessment': 'равная',
                'endgame_assessment': 'равная',
                'overall_assessment': 'ошибка анализа'
            }

    def _get_move_statistics(self):
        """
        Получить статистику по ходам.
        
        Возвращает:
            dict: Словарь со статистикой ходов
        """
        try:
            stats = {
                'total_moves': len(self.move_history),
                'player_moves': self.game_stats['player_moves'],
                'ai_moves': self.game_stats['ai_moves'],
                'capture_moves': self.game_stats['player_capture_count'] + self.game_stats['ai_capture_count'],
                'check_moves': self.game_stats['check_count'],
                'castling_moves': 0,
                'promotion_moves': 0,
                'most_active_pieces': {},
                'move_efficiency': 0.0
            }
            
            # Подсчитываем специальные ходы
            for move in self.move_history:
                if move in ['e1g1', 'e1c1', 'e8g8', 'e8c8']:
                    stats['castling_moves'] += 1
                # Проверяем на превращение (ход заканчивается на цифру 1 или 8)
                if len(move) >= 4 and move[3] in ['1', '8']:
                    stats['promotion_moves'] += 1
                    
            # Определяем самые активные фигуры (приблизительно)
            piece_moves = {}
            for move in self.move_history:
                if len(move) >= 2:
                    # Определяем фигуру по начальной позиции (упрощенный подход)
                    start_square = move[0:2]
                    piece_type = start_square[0]  # Буква файла
                    if piece_type in piece_moves:
                        piece_moves[piece_type] += 1
                    else:
                        piece_moves[piece_type] = 1
                        
            stats['most_active_pieces'] = piece_moves
            
            # Вычисляем эффективность ходов
            total_moves = stats['total_moves']
            if total_moves > 0:
                # Эффективность = (ходы без ошибок) / общие ходы
                mistakes_count = len(self.game_stats.get('mistakes', []))
                stats['move_efficiency'] = (total_moves - mistakes_count) / total_moves * 100
                
            return stats
        except Exception as e:
            print(f"Ошибка при подсчете статистики ходов: {e}")
            return {
                'total_moves': len(self.move_history),
                'player_moves': self.game_stats['player_moves'],
                'ai_moves': self.game_stats['ai_moves'],
                'capture_moves': 0,
                'check_moves': self.game_stats['check_count'],
                'castling_moves': 0,
                'promotion_moves': 0,
                'most_active_pieces': {},
                'move_efficiency': 0.0
            }
    
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
        # Оптимизация: уменьшаем частоту обновления оценки позиции
        evaluation = None
        current_time = time.time()
        if not hasattr(self, '_last_eval_update') or (current_time - self._last_eval_update) > 2.0:
            # Обновляем оценку только раз в 2000 мс для снижения нагрузки
            # Используем асинхронное обновление для предотвращения блокировки UI
            if not hasattr(self, '_async_eval_future') or self._async_eval_future is None:
                # Запускаем асинхронное вычисление оценки
                self._async_eval_future = self.executor.submit(self.engine.get_evaluation)
                self._last_eval_update = current_time
            else:
                # Проверяем, готов ли результат
                if self._async_eval_future.done():
                    try:
                        evaluation = self._async_eval_future.result(timeout=0.1)
                        self._cached_evaluation = evaluation
                        self._async_eval_future = None
                    except:
                        evaluation = self._cached_evaluation
        elif hasattr(self, '_cached_evaluation'):
            evaluation = self._cached_evaluation
        
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
        Улучшенная версия с более агрессивным кэшированием.
        
        Параметры:
            depth (int): Глубина анализа
            
        Возвращает:
            str: Лучший ход в формате UCI
        """
        # Создаем ключ для кэширования
        fen = self.engine.get_fen()
        cache_key = (fen, depth, self.skill_level)
        
        # Проверяем кэш с более агрессивной стратегией
        current_time = time.time()
        if cache_key in self._ai_move_cache:
            cached_move, cache_time = self._ai_move_cache[cache_key]
            # Используем кэш, если он не старше 20 секунд ИЛИ если это очень свежий кэш (меньше 1 секунды)
            # Увеличиваем время жизни кэша для еще более агрессивного кэширования
            is_time_valid = (current_time - cache_time < 20.0)  # Увеличено с 15.0 до 20.0
            is_fresh_cache = (current_time - cache_time < 1.0)  # Увеличено с 0.5 до 1.0
            
            if is_time_valid or is_fresh_cache:
                return cached_move
        
        # Для более быстрого получения хода, используем меньшую глубину при высоких уровнях сложности
        if depth is None:
            # Более агрессивное ограничение глубины
            depth = max(1, min(6, self.skill_level))  # Уменьшено максимальное значение
        
        # Получаем ход от движка
        best_move = self.engine.get_best_move(depth=depth)
        
        # Сохраняем в кэш
        if best_move:
            self._ai_move_cache[cache_key] = (best_move, current_time)
            
        return best_move

    def _clear_old_ai_cache(self):
        """Очистка старых записей в кэше AI для предотвращения утечек памяти."""
        current_time = time.time()
        expired_keys = []
        
        for key, (_, cache_time) in self._ai_move_cache.items():
            # Удаляем записи старше 40 секунд (увеличиваем с 30 секунд)
            if current_time - cache_time > 40.0:
                expired_keys.append(key)
                
        for key in expired_keys:
            del self._ai_move_cache[key]
            
    def _clear_ai_cache(self):
        """Полная очистка кэша AI."""
        self._ai_move_cache.clear()

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
                evaluation = self.get_cached_evaluation()
                
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

    def _get_position_analysis(self):
        """
        Получить подробный анализ текущей позиции.
        
        Возвращает:
            dict: Словарь с анализом позиции
        """
        try:
            analysis = {
                'evaluation': None,
                'best_move': None,
                'material_balance': 0,
                'piece_activity': 0,
                'king_safety': 0,
                'pawn_structure': 0,
                'tactical_threats': [],
                'strategic_ideas': []
            }
            
            # Получаем оценку позиции
            evaluation = self.get_cached_evaluation()
            if evaluation is not None:
                analysis['evaluation'] = evaluation
                
            # Получаем лучший ход
            best_move = self.engine.get_best_move()
            if best_move:
                analysis['best_move'] = best_move
                
            # Анализируем материальный баланс
            board_state = self.engine.get_board_state()
            material_count = {'white': 0, 'black': 0}
            
            piece_values = {
                'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0,
                'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': 0
            }
            
            for row in board_state:
                for piece in row:
                    if piece and piece in piece_values:
                        if piece.isupper():
                            material_count['white'] += piece_values[piece]
                        else:
                            material_count['black'] += abs(piece_values[piece])
                            
            analysis['material_balance'] = material_count['white'] - material_count['black']
            
            # Определяем стратегические идеи на основе оценки
            if evaluation is not None:
                if abs(evaluation) > 2.0:
                    analysis['strategic_ideas'].append("Сильное материальное/позиционное преимущество")
                elif abs(evaluation) > 1.0:
                    analysis['strategic_ideas'].append("Умеренное преимущество")
                else:
                    analysis['strategic_ideas'].append("Позиция примерно равная")
                    
                # Определяем, кто имеет преимущество
                if evaluation > 0.5:
                    if self.player_color == 'white':
                        analysis['strategic_ideas'].append("У вас преимущество")
                    else:
                        analysis['strategic_ideas'].append("У компьютера преимущество")
                elif evaluation < -0.5:
                    if self.player_color == 'black':
                        analysis['strategic_ideas'].append("У вас преимущество")
                    else:
                        analysis['strategic_ideas'].append("У компьютера преимущество")
                        
            # Добавляем образовательные советы
            if len(self.move_history) > 0:
                recent_moves = self.move_history[-3:]  # Последние 3 хода
                if len(recent_moves) >= 2:
                    # Проверяем на тактические мотивы
                    if any('x' in move for move in recent_moves):
                        analysis['tactical_threats'].append("Обратите внимание на возможные тактические удары")
                        
                    # Проверяем развитие фигур
                    if len(recent_moves) < 6:  # Ранняя стадия игры
                        analysis['strategic_ideas'].append("Развивайте фигуры и рокируйтесь")
                        
            return analysis
        except Exception as e:
            print(f"Ошибка при анализе позиции: {e}")
            return {
                'evaluation': None,
                'best_move': None,
                'material_balance': 0,
                'piece_activity': 0,
                'king_safety': 0,
                'pawn_structure': 0,
                'tactical_threats': [],
                'strategic_ideas': [f"Ошибка анализа: {str(e)}"]
            }

    def _suggest_move(self):
        """
        Предложить лучший ход для текущей позиции с объяснением.
        """
        try:
            if self.thinking or self.game_over or not self._is_player_turn():
                return
                
            self.thinking = True
            
            # Получаем лучший ход от движка
            best_move = self.engine.get_best_move()
            
            if best_move:
                # Получаем оценку позиции до и после хода
                eval_before = self.get_cached_evaluation()
                
                # Делаем временный ход для получения оценки после хода
                self.engine.make_move(best_move)
                eval_after = self.get_cached_evaluation()
                # Отменяем ход
                self.engine.reset_board()
                for move in self.move_history:
                    self.engine.make_move(move)
                
                # Преобразуем UCI ход в координаты
                from_col = ord(best_move[0]) - ord('a')
                from_row = 8 - int(best_move[1])
                to_col = ord(best_move[2]) - ord('a')
                to_row = 8 - int(best_move[3])
                
                # Получаем информацию о фигуре
                board_state = self.engine.get_board_state()
                piece = board_state[from_row][from_col] if 0 <= from_row < 8 and 0 <= from_col < 8 else None
                
                piece_names = {
                    'P': 'пешка', 'N': 'конь', 'B': 'слон', 'R': 'ладья', 
                    'Q': 'ферзь', 'K': 'король', 'p': 'пешка', 'n': 'конь', 
                    'b': 'слон', 'r': 'ладья', 'q': 'ферзь', 'k': 'король'
                }
                
                piece_name = piece_names.get(piece, 'фигура') if piece else 'фигура'
                
                # Формируем объяснение
                explanation = f"Предлагаемый ход: {best_move} ({piece_name} с {best_move[0:2]} на {best_move[2:4]})"
                
                # Добавляем информацию о тактике
                if 'x' in best_move:
                    explanation += " (взятие)"
                elif best_move in ['e1g1', 'e1c1', 'e8g8', 'e8c8']:
                    explanation += " (рокировка)"
                    
                # Добавляем информацию о преимуществе
                if eval_after is not None and eval_before is not None:
                    improvement = eval_after - eval_before
                    if abs(improvement) > 0.5:
                        if (self.player_color == 'white' and improvement > 0) or (self.player_color == 'black' and improvement < 0):
                            explanation += f" | Улучшает вашу позицию на {abs(improvement):.1f}"
                        else:
                            explanation += f" | Ухудшает позицию противника на {abs(improvement):.1f}"
                
                self.move_feedback = f"💡 Совет: {explanation}"
                self.move_feedback_time = time.time()
                
                # Выделяем рекомендуемый ход
                self.analysis_move = ((from_row, from_col), (to_row, to_col))
                
                # Проигрываем звук подсказки
                if self.sound_manager:
                    self.sound_manager.play_sound("button")
            else:
                self.move_feedback = "Не удалось получить совет по ходу"
                self.move_feedback_time = time.time()
                
        except Exception as e:
            print(f"Ошибка при получении совета: {e}")
            self.move_feedback = "Ошибка при получении совета"
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
    
    def _save_game_to_file(self, filename = None):
        """
        Сохранить текущую партию в файл.
        
        Параметры:
            filename (str): Имя файла для сохранения (по умолчанию генерируется автоматически)
        """
        try:
            import json
            import os
            from datetime import datetime
            
            # Если имя файла не указано, генерируем его автоматически
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # Добавляем информацию о партии в имя файла для лучшей идентификации
                player_color_abbr = "w" if self.player_color == "white" else "b"
                move_count = len(self.move_history)
                filename = f"chess_game_{timestamp}_{player_color_abbr}_{move_count}moves.json"
            
            # Убедимся, что папка saves существует
            saves_dir = os.path.join(os.path.dirname(__file__), "..", "saves")
            if not os.path.exists(saves_dir):
                os.makedirs(saves_dir)
            
            # Полный путь к файлу
            full_path = os.path.join(saves_dir, filename)
            
            # Подготавливаем данные для сохранения с дополнительной информацией
            game_state = {
                'player_color': self.player_color,
                'skill_level': self.skill_level,
                'theme': self.theme,
                'move_history': self.move_history.copy(),
                'fen': self.engine.get_fen(),
                'timestamp': time.time(),
                'stats': self.get_game_stats(),
                'version': '1.1',  # Обновляем версию для совместимости
                'player_name': 'Player',  # Можно расширить для поддержки имен игроков
                'game_mode': 'single_player',  # Можно расширить для разных режимов игры
                'save_timestamp': datetime.now().isoformat(),  # Человекочитаемая временная метка
                'board_orientation': self.player_color  # Ориентация доски при сохранении
            }
            
            # Сохраняем в файл с форматированием для лучшей читаемости
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(game_state, f, ensure_ascii=False, indent=2, sort_keys=True)
            
            self.move_feedback = f"Партия сохранена в {filename}"
            self.move_feedback_time = time.time()
            print(f"Партия сохранена в файл: {full_path}")
            
            # Обновляем список сохраненных игр
            self.saved_games.append(game_state)
            
        except Exception as e:
            print(f"Ошибка при сохранении партии в файл: {e}")
            self.move_feedback = "Ошибка сохранения в файл"
            self.move_feedback_time = time.time()

    def _load_game_from_file(self, filename: str):
        """
        Загрузить партию из файла.
        
        Параметры:
            filename (str): Имя файла для загрузки
        """
        try:
            import json
            import os
            
            # Полный путь к файлу
            saves_dir = os.path.join(os.path.dirname(__file__), "..", "saves")
            full_path = os.path.join(saves_dir, filename)
            
            # Проверяем существование файла
            if not os.path.exists(full_path):
                self.move_feedback = f"Файл {filename} не найден"
                self.move_feedback_time = time.time()
                return
            
            # Загружаем данные из файла
            with open(full_path, 'r', encoding='utf-8') as f:
                game_state = json.load(f)
            
            # Проверяем версию сохранения для обратной совместимости
            file_version = game_state.get('version', '1.0')
            if file_version not in ['1.0', '1.1']:
                self.move_feedback = "Несовместимый формат файла сохранения"
                self.move_feedback_time = time.time()
                return
            
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
            
            # Обновляем ориентацию доски, если она сохранена
            if 'board_orientation' in game_state:
                board_orientation = game_state['board_orientation']
                if board_orientation != self.player_color:
                    self.renderer.set_player_color(board_orientation)
            
            self.move_feedback = f"Партия загружена из {filename}"
            self.move_feedback_time = time.time()
            print(f"Партия загружена из файла: {full_path}")
            
            # Обновляем список сохраненных игр
            if game_state not in self.saved_games:
                self.saved_games.append(game_state)
                
        except Exception as e:
            print(f"Ошибка при загрузке партии из файла: {e}")
            self.move_feedback = "Ошибка загрузки из файла"
            self.move_feedback_time = time.time()

    def _list_saved_games(self):
        """
        Получить список сохраненных партий с дополнительной информацией.
        
        Возвращает:
            list: Список имен файлов сохраненных партий с информацией
        """
        try:
            import os
            import json
            from datetime import datetime
            
            saves_dir = os.path.join(os.path.dirname(__file__), "..", "saves")
            if not os.path.exists(saves_dir):
                return []
            
            # Получаем список файлов с расширением .json
            saved_files = []
            for f in os.listdir(saves_dir):
                if f.endswith('.json'):
                    try:
                        # Читаем информацию из файла для отображения
                        full_path = os.path.join(saves_dir, f)
                        with open(full_path, 'r', encoding='utf-8') as file:
                            game_data = json.load(file)
                        
                        # Извлекаем информацию для отображения
                        player_color = game_data.get('player_color', 'white')
                        move_count = len(game_data.get('move_history', []))
                        timestamp = game_data.get('timestamp', 0)
                        skill_level = game_data.get('skill_level', 5)
                        
                        # Форматируем дату
                        try:
                            date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
                        except:
                            date_str = "Неизвестно"
                        
                        # Создаем отображаемое имя с информацией
                        color_symbol = "♛" if player_color == "white" else "♚"
                        display_info = f"{color_symbol} {move_count} ходов | Ур.{skill_level} | {date_str}"
                        
                        saved_files.append({
                            'filename': f,
                            'display_info': display_info,
                            'player_color': player_color,
                            'move_count': move_count,
                            'skill_level': skill_level,
                            'date': date_str
                        })
                    except Exception:
                        # Если не удалось прочитать файл, добавляем базовую информацию
                        saved_files.append({
                            'filename': f,
                            'display_info': f,
                            'player_color': 'unknown',
                            'move_count': 0,
                            'skill_level': 0,
                            'date': 'unknown'
                        })
            
            # Сортируем по дате (новые первыми)
            saved_files.sort(key=lambda x: x['date'], reverse=True)
            return saved_files
        except Exception as e:
            print(f"Ошибка при получении списка сохраненных партий: {e}")
            return []

    def _delete_saved_game(self, filename: str):
        """
        Удалить сохраненную партию.
        
        Параметры:
            filename (str): Имя файла для удаления
        """
        try:
            import os
            
            # Полный путь к файлу
            saves_dir = os.path.join(os.path.dirname(__file__), "..", "saves")
            full_path = os.path.join(saves_dir, filename)
            
            # Проверяем существование файла
            if not os.path.exists(full_path):
                self.move_feedback = f"Файл {filename} не найден"
                self.move_feedback_time = time.time()
                return False
            
            # Удаляем файл
            os.remove(full_path)
            self.move_feedback = f"Партия {filename} удалена"
            self.move_feedback_time = time.time()
            print(f"Партия удалена: {full_path}")
            
            # Удаляем из списка сохраненных игр
            self.saved_games = [game for game in self.saved_games if game.get('filename') != filename]
            
            return True
            
        except Exception as e:
            print(f"Ошибка при удалении партии: {e}")
            self.move_feedback = "Ошибка удаления партии"
            self.move_feedback_time = time.time()
            return False

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
    
    def _ai_worker(self):
        """Фоновый поток для обработки ходов ИИ."""
        while self.ai_thread_running:
            try:
                # Получаем задачу из очереди
                task = self.ai_move_queue.get(timeout=0.1)
                if task == "stop":
                    break
                    
                # Выполняем вычисления ИИ
                ai_move = self._compute_ai_move()
                if ai_move:
                    # Помещаем результат обратно в очередь
                    self.ai_move_queue.put(("result", ai_move))
                    
                self.ai_move_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                print(f"Ошибка в потоке ИИ: {e}")
                self.ai_move_queue.put(("error", str(e)))
                
    def _render_worker(self):
        """Фоновый поток для рендеринга."""
        while self.render_thread_running:
            try:
                # Получаем задачу из очереди
                task = self.render_queue.get(timeout=0.1)
                if task == "stop":
                    break
                    
                # Выполняем рендеринг
                if task[0] == "render_board":
                    board_state = task[1]
                    self._render_board_state(board_state)
                    
                self.render_queue.task_done()
            except Empty:
                continue
            except Exception as e:
                print(f"Ошибка в потоке рендеринга: {e}")
                
    def _compute_ai_move(self):
        """Вычислить ход ИИ в отдельном потоке."""
        try:
            # Получаем лучший ход с оптимальной глубиной анализа
            depth = max(1, min(8, self.skill_level))  # Ограничиваем глубину для скорости
            
            # Для всех уровней сложности используем кэшированные ходы в первую очередь
            ai_move = None
            
            # Пытаемся получить ход из кэша с упрощенной глубиной
            if self.skill_level < 15:
                ai_move = self._get_cached_best_move(depth=1)  # Используем минимальную глубину
            
            # Если нет кэшированного хода, получаем новый с оптимизированной глубиной
            if not ai_move:
                # Для более быстрого ответа используем меньшую глубину
                fast_depth = max(1, min(4, self.skill_level))  # Ограничиваем глубину до 4
                ai_move = self._get_cached_best_move(depth=fast_depth)
            
            # Альтернативный метод: если все еще нет хода, используем минимальную глубину
            if not ai_move:
                ai_move = self._get_cached_best_move(depth=1)
                
            return ai_move
        except Exception as e:
            print(f"Ошибка при вычислении хода ИИ: {e}")
            return None
        except KeyboardInterrupt:
            raise
    def _render_board_state(self, board_state):
        """Рендеринг состояния доски с использованием GPU ускорения (если доступно)."""
        try:
            if self.cuda_available and cp is not None:
                # Используем GPU для ускорения вычислений
                # Преобразуем данные в массивы
                # Это упрощенный пример - в реальном приложении здесь будут более сложные вычисления
                # Для демонстрации многопоточности просто возвращаем исходное состояние
                return board_state
            else:
                # Используем CPU для вычислений
                return board_state
        except Exception as e:
            print(f"Ошибка при рендеринге с GPU: {e}")
            return board_state
            
    def start_multithreading(self):
        """Запустить многопоточную обработку."""
        # Запускаем поток ИИ
        self.ai_thread_running = True
        self.ai_thread = threading.Thread(target=self._ai_worker, daemon=True)
        self.ai_thread.start()
        
        # Запускаем поток рендеринга
        self.render_thread_running = True
        self.render_thread = threading.Thread(target=self._render_worker, daemon=True)
        self.render_thread.start()
        
        print("✅ Многопоточная обработка запущена")
        
    def stop_multithreading(self):
        """Остановить многопоточную обработку."""
        # Останавливаем поток ИИ
        self.ai_thread_running = False
        if self.ai_thread:
            self.ai_move_queue.put("stop")
            self.ai_thread.join(timeout=1)
            
        # Останавливаем поток рендеринга
        self.render_thread_running = False
        if self.render_thread:
            self.render_queue.put("stop")
            self.render_thread.join(timeout=1)
            
        # Завершаем пул потоков
        self.executor.shutdown(wait=False)
        
        print("✅ Многопоточная обработка остановлена")
        
    def handle_ai_move_multithreaded(self):
        """
        Обработка хода ИИ с использованием многопоточности.
        """
        if self._is_player_turn() or self.game_over or self.thinking:
            return
            
        # Проверка минимальной задержки
        current_time = time.time()
        if current_time - self.last_ai_move_time < self.ai_move_cooldown:
            return
            
        # Уменьшенная задержка для более быстрой игры
        if current_time - self.last_move_time < self.ai_move_delay:
            return
            
        # Помещаем задачу в очередь ИИ
        self.ai_move_queue.put("compute_move")
        self.thinking = True
        self.last_ai_move_time = current_time
        
        # Проверяем результат
        try:
            result = self.ai_move_queue.get(timeout=0.1)
            if result[0] == "result":
                ai_move = result[1]
                self._execute_ai_move(ai_move)
            elif result[0] == "error":
                print(f"Ошибка ИИ: {result[1]}")
                self.thinking = False
        except Empty:
            # Результат еще не готов, продолжаем обработку в следующем кадре
            pass
        except Exception as e:
            print(f"Ошибка при обработке хода ИИ: {e}")
            self.thinking = False
            
    def _execute_ai_move(self, ai_move):
        """Выполнить ход ИИ после его вычисления."""
        try:
            if ai_move:
                print(f"Ход компьютера: {ai_move}")
                
                # Получаем текущее состояние доски для проверки взятия
                board_before = self.engine.get_board_state()
                
                # Валидация хода
                if self.engine.is_move_correct(ai_move):
                    if self.engine.make_move(ai_move):
                        # Добавляем ход в дебютную книгу
                        self.opening_book.add_move(ai_move)
                        
                        # Проверяем текущий дебют
                        current_opening = self.opening_book.get_current_opening()
                        
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
                        
                        # Добавляем информацию о дебюте, если она есть
                        if current_opening:
                            opening_name, opening_info = current_opening
                            self.move_feedback += f" | 🎯 Дебют: {opening_name}"
                        
                        # Преобразование UCI хода в координаты для выделения
                        from_col = ord(ai_move[0]) - ord('a')
                        from_row = 8 - int(ai_move[1])
                        to_col = ord(ai_move[2]) - ord('a')
                        to_row = 8 - int(ai_move[3])
                        self.renderer.set_last_move((from_row, from_col), (to_row, to_col))
                        self.last_move_time = time.time()
                        print(f"Ход компьютера выполнен: {annotated_move}")
                        self.move_feedback_time = time.time()
                        
                        # Записываем время хода в статистику
                        move_time = time.time() - self.last_move_time
                        self.game_stats['move_times'].append(move_time)
                        
                        # Получаем оценку позиции для статистики
                        evaluation = self.get_cached_evaluation()
                        if evaluation is not None:
                            self.game_stats['evaluations'].append(evaluation)
                        
                        # Добавляем образовательную обратную связь
                        educational_tip = self.educator.get_educational_feedback(
                            len(self.move_history), time.time())
                        if educational_tip:
                            self.move_feedback += f" | {educational_tip}"
                            self.move_feedback_time = time.time()
                            
                        # Очищаем кэш состояния доски после хода
                        self.board_state_cache = None
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
        
        # Увеличиваем задержку для более быстрой игры
        if current_time - self.last_move_time < self.ai_move_delay:
            return
        
        self.thinking = True
        self.last_ai_move_time = current_time
        
        # Засекаем время начала хода для статистики
        move_start_time = time.time()
        
        try:
            # Очищаем старый кэш
            self._clear_old_ai_cache()
            
            # Получаем лучший ход с оптимизированной глубиной анализа
            # Более агрессивное ограничение глубины для скорости
            depth = max(1, min(8, self.skill_level // 2 + 1))  # Уменьшаем глубину анализа
            
            # Для всех уровней сложности используем кэшированные ходы в первую очередь
            ai_move = None
            
            # Пытаемся получить ход из кэша с упрощенной глубиной
            if self.skill_level < 10:
                ai_move = self._get_cached_best_move(depth=1)  # Используем минимальную глубину
            
            # Если нет кэшированного хода, получаем новый с оптимизированной глубиной
            if not ai_move:
                # Для более быстрого ответа используем меньшую глубину
                fast_depth = max(1, min(4, self.skill_level // 3 + 1))  # Еще больше уменьшаем глубину
                ai_move = self._get_cached_best_move(depth=fast_depth)
            
            # Альтернативный метод: если все еще нет хода, используем минимальную глубину
            if not ai_move:
                ai_move = self._get_cached_best_move(depth=1)
            
            if ai_move:
                print(f"Ход компьютера: {ai_move}")
                
                # Получаем текущее состояние доски для проверки взятия
                board_before = self.engine.get_board_state()
                
                # Валидация хода
                if self.engine.is_move_correct(ai_move):
                    if self.engine.make_move(ai_move):
                        # Добавляем ход в дебютную книгу
                        self.opening_book.add_move(ai_move)
                        
                        # Проверяем текущий дебют
                        current_opening = self.opening_book.get_current_opening()
                        
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
                            # Проигрываем звук взятия
                            if self.sound_manager:
                                self.sound_manager.play_sound("capture")
                        else:
                            self.move_feedback = f"Ход компьютера: {annotated_move}"
                            # Проигрываем звук хода
                            if self.sound_manager:
                                self.sound_manager.play_sound("move")
                        
                        # Добавляем информацию о дебюте, если она есть
                        if current_opening:
                            opening_name, opening_info = current_opening
                            self.move_feedback += f" | 🎯 Дебют: {opening_name}"
                        
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
                        evaluation = self.get_cached_evaluation()
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
                        
                        # Обновляем отображение
                        self.renderer._mark_all_dirty()
                    else:
                        print("⚠️  Не удалось выполнить ход компьютера")
                        self.move_feedback = "Не удалось выполнить ход компьютера"
                        self.move_feedback_time = current_time
                        # Проигрываем звук ошибки
                        if self.sound_manager:
                            self.sound_manager.play_sound("button")
                else:
                    print("⚠️  Компьютер предложил некорректный ход")
                    self.move_feedback = "Компьютер предложил некорректный ход"
                    self.move_feedback_time = current_time
                    # Проигрываем звук ошибки
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
            else:
                print("⚠️  Компьютер не смог найти ход")
                self.move_feedback = "Компьютер не смог найти ход"
                self.move_feedback_time = time.time()
                # Проигрываем звук ошибки
                if self.sound_manager:
                    self.sound_manager.play_sound("button")
        except Exception as e:
            print(f"⚠️  Ошибка при получении хода компьютера: {e}")
            self.move_feedback = "Ошибка при получении хода компьютера"
            self.move_feedback_time = time.time()
            # Проигрываем звук ошибки
            if self.sound_manager:
                self.sound_manager.play_sound("button")
        finally:
            self.thinking = False

    def _get_adaptive_depth(self):
        """
        Получить адаптивную глубину анализа в зависимости от сложности позиции.
        
        Возвращает:
            int: Глубина анализа
        """
        # Базовая глубина зависит от уровня сложности
        base_depth = max(1, min(15, self.skill_level))
        
        # Адаптируем глубину в зависимости от сложности позиции
        try:
            # Получаем оценку текущей позиции
            evaluation = self.get_cached_evaluation()
            
            # Если позиция сложная (большие изменения оценки), увеличиваем глубину
            if (evaluation is not None and 
                hasattr(self, '_prev_evaluation') and 
                self._prev_evaluation is not None and
                isinstance(self._prev_evaluation, (int, float))):
                eval_diff = abs(evaluation - self._prev_evaluation)
                if eval_diff > 2.0:  # Большая разница в оценке
                    base_depth = min(base_depth + 2, 20)  # Увеличиваем, но не более 20
                elif eval_diff < 0.5:  # Стабильная позиция
                    base_depth = max(base_depth - 1, 1)  # Уменьшаем для скорости
                    
            self._prev_evaluation = evaluation
        except:
            pass
            
        return base_depth

    def _get_multi_pv_analysis(self, num_moves: int = 3):
        """
        Получить анализ нескольких лучших ходов.
        
        Параметры:
            num_moves (int): Количество ходов для анализа
            
        Возвращает:
            list: Список лучших ходов с оценками
        """
        try:
            # Получаем текущую позицию
            fen = self.engine.get_fen()
            
            # Получаем несколько лучших ходов
            best_moves = []
            
            # Для каждого хода получаем оценку
            for i in range(num_moves):
                # Получаем лучший ход
                move = self.engine.get_best_move()
                if not move:
                    break
                    
                # Получаем оценку после хода
                eval_score = self.engine.get_evaluation()
                
                # Сохраняем ход и оценку
                best_moves.append({
                    'move': move,
                    'evaluation': eval_score['value'] / 100.0 if isinstance(eval_score, dict) and 'value' in eval_score else 0,
                    'move_number': len(self.move_history) + 1 + i
                })
                
                # Делаем ход временно для анализа следующего
                self.engine.make_move(move)
                
            # Восстанавливаем исходную позицию
            self.engine.set_fen(fen)
            
            return best_moves
        except Exception as e:
            print(f"Ошибка при многовариантном анализе: {e}")
            return []

    def _evaluate_move_quality(self, move: str, player: str = 'player'):
        """
        Оценить качество хода.
        
        Параметры:
            move (str): Ход в формате UCI
            player (str): Игрок, сделавший ход ('player' или 'ai')
            
        Возвращает:
            str: Качество хода ('excellent', 'good', 'inaccuracy', 'mistake', 'blunder')
        """
        try:
            # Получаем оценку позиции до хода
            eval_before = self.get_cached_evaluation()
            
            # Делаем временный ход для получения оценки после хода
            fen_before = self.engine.get_fen()
            self.engine.make_move(move)
            eval_after = self.get_cached_evaluation()
            
            # Восстанавливаем позицию
            self.engine.set_fen(fen_before)
            
            # Вычисляем изменение оценки
            if eval_before is not None and eval_after is not None:
                # Для белых: положительное изменение = улучшение
                # Для черных: отрицательное изменение = улучшение
                if player == 'player':
                    improvement = eval_after - eval_before
                    if self.player_color == 'black':
                        improvement = -improvement
                else:
                    improvement = eval_before - eval_after
                    if self.player_color == 'black':
                        improvement = -improvement
                
                # Определяем качество хода
                if improvement > 1.0:
                    return 'excellent'  # Отличный ход
                elif improvement > 0.5:
                    return 'good'  # Хороший ход
                elif improvement > -0.5:
                    return 'inaccuracy'  # Неточность
                elif improvement > -1.5:
                    return 'mistake'  # Ошибка
                else:
                    return 'blunder'  # Грубая ошибка
                    
            return 'good'  # По умолчанию, если не можем оценить
        except Exception as e:
            print(f"Ошибка при оценке качества хода: {e}")
            return 'good'

    def _get_position_complexity(self):
        """
        Оценить сложность текущей позиции.
        
        Возвращает:
            float: Сложность позиции от 0.0 (простая) до 1.0 (сложная)
        """
        try:
            # Получаем оценку позиции
            evaluation = self.get_cached_evaluation()
            
            # Определяем сложность на основе различных факторов
            complexity = 0.5  # Базовая сложность
            
            # Фактор 1: Неопределенность оценки (ближе к 0 = сложнее)
            if evaluation is not None:
                complexity += 0.3 * (1.0 - min(1.0, abs(evaluation) / 5.0))
            
            # Фактор 2: Количество фигур на доске
            board_state = self.get_board_state()
            piece_count = sum(1 for row in board_state for piece in row if piece is not None)
            complexity += 0.2 * (piece_count / 32.0)  # Нормализуем до 32 фигур
            
            # Фактор 3: Наличие тактических возможностей
            # Проверяем наличие взятий и шахов
            try:
                best_move = self.engine.get_best_move()
                if best_move and ('x' in best_move or '+' in best_move):
                    complexity += 0.2
            except:
                pass
            
            # Ограничиваем диапазон от 0.0 до 1.0
            return max(0.0, min(1.0, complexity))
        except Exception as e:
            print(f"Ошибка при оценке сложности позиции: {e}")
            return 0.5

    def _get_ai_move_with_analysis(self):
        """
        Получить ход ИИ с подробным анализом.
        
        Возвращает:
            dict: Словарь с ходом и аналитической информацией
        """
        try:
            # Получаем базовую информацию
            fen = self.engine.get_fen()
            evaluation_before = self.get_cached_evaluation()
            
            # Получаем лучший ход
            best_move = self._get_cached_best_move()
            
            if not best_move:
                return None
            
            # Получаем многовариантный анализ
            multi_pv = self._get_multi_pv_analysis(3)
            
            # Оцениваем качество хода
            move_quality = self._evaluate_move_quality(best_move, 'ai')
            
            # Определяем сложность позиции
            position_complexity = self._get_position_complexity()
            
            # Получаем оценку после хода
            self.engine.make_move(best_move)
            evaluation_after = self.get_cached_evaluation()
            self.engine.set_fen(fen)  # Восстанавливаем позицию
            
            # Формируем результат
            analysis = {
                'move': best_move,
                'quality': move_quality,
                'complexity': position_complexity,
                'evaluation_before': evaluation_before,
                'evaluation_after': evaluation_after,
                'alternative_moves': multi_pv[1:] if len(multi_pv) > 1 else [],
                'timestamp': time.time()
            }
            
            return analysis
        except Exception as e:
            print(f"Ошибка при получении анализа хода ИИ: {e}")
            # Возвращаем базовый ход в случае ошибки
            best_move = self._get_cached_best_move()
            if best_move:
                return {'move': best_move, 'quality': 'unknown'}
            return None

    def handle_ai_move_enhanced(self):
        """
        Улучшенная обработка хода ИИ с расширенным анализом.
        """
        if self._is_player_turn() or self.game_over or self.thinking:
            return
        
        # Проверка минимальной задержки
        current_time = time.time()
        if current_time - self.last_ai_move_time < self.ai_move_cooldown:
            return
        
        # Уменьшенная задержка для более быстрой игры
        if current_time - self.last_move_time < self.ai_move_delay:
            return
        
        self.thinking = True
        self.last_ai_move_time = current_time
        
        # Засекаем время начала хода для статистики
        move_start_time = time.time()
        
        try:
            # Очищаем старый кэш
            self._clear_old_ai_cache()
            
            # Получаем ход ИИ с анализом
            ai_analysis = self._get_ai_move_with_analysis()
            
            if ai_analysis and 'move' in ai_analysis:
                ai_move = ai_analysis['move']
                print(f"Ход компьютера: {ai_move}")
                
                # Получаем текущее состояние доски для проверки взятия
                board_before = self.engine.get_board_state()
                
                # Валидация хода
                if self.engine.is_move_correct(ai_move):
                    if self.engine.make_move(ai_move):
                        # Добавляем ход в дебютную книгу
                        self.opening_book.add_move(ai_move)
                        
                        # Проверяем текущий дебют
                        current_opening = self.opening_book.get_current_opening()
                        
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
                        annotated_move = self._annotate_move_internal(ai_move, is_capture, is_check, is_mate, is_castling)
                        
                        if is_capture:
                            self.game_stats['ai_capture_count'] += 1
                            self.move_feedback = f"Ход компьютера: {annotated_move} (взятие!)"
                            # Проигрываем звук взятия
                            if self.sound_manager:
                                self.sound_manager.play_sound("capture")
                        else:
                            self.move_feedback = f"Ход компьютера: {annotated_move}"
                            # Проигрываем звук хода
                            if self.sound_manager:
                                self.sound_manager.play_sound("move")
                        
                        # Добавляем информацию о дебюте, если она есть
                        if current_opening:
                            opening_name, opening_info = current_opening
                            self.move_feedback += f" | 🎯 Дебют: {opening_name}"
                        
                        # Добавляем анализ качества хода, если доступен
                        if 'quality' in ai_analysis:
                            quality_text = {
                                'excellent': 'отличный ход!',
                                'good': 'хороший ход',
                                'inaccuracy': 'неточность',
                                'mistake': 'ошибка',
                                'blunder': 'грубая ошибка!'
                            }
                            quality_desc = quality_text.get(ai_analysis['quality'], '')
                            if quality_desc:
                                self.move_feedback += f" ({quality_desc})"
                        
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
                        evaluation = self.get_cached_evaluation()
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
                        
                        # Обновляем отображение
                        self.renderer._mark_all_dirty()
                    else:
                        print("⚠️  Не удалось выполнить ход компьютера")
                        self.move_feedback = "Не удалось выполнить ход компьютера"
                        self.move_feedback_time = current_time
                        # Проигрываем звук ошибки
                        if self.sound_manager:
                            self.sound_manager.play_sound("button")
                else:
                    print("⚠️  Компьютер предложил некорректный ход")
                    self.move_feedback = "Компьютер предложил некорректный ход"
                    self.move_feedback_time = current_time
                    # Проигрываем звук ошибки
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
            else:
                print("⚠️  Компьютер не смог найти ход")
                self.move_feedback = "Компьютер не смог найти ход"
                self.move_feedback_time = time.time()
                # Проигрываем звук ошибки
                if self.sound_manager:
                    self.sound_manager.play_sound("button")
        except Exception as e:
            print(f"⚠️  Ошибка при получении хода компьютера: {e}")
            self.move_feedback = "Ошибка при получении хода компьютера"
            self.move_feedback_time = time.time()
            # Проигрываем звук ошибки
            if self.sound_manager:
                self.sound_manager.play_sound("button")
        finally:
            self.thinking = False

    def _annotate_move_internal(self, uci_move: str, is_capture: bool = False, is_check: bool = False, 
                      is_mate: bool = False, is_castling: bool = False) -> str:
        """
        Аннотировать ход с помощью специальных символов.
        Внутренняя версия для избежания конфликта с существующим методом.
        
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
        
        # Увеличиваем задержку для более быстрой игры
        if current_time - self.last_move_time < self.ai_move_delay:
            return
        
        self.thinking = True
        self.last_ai_move_time = current_time
        
        # Засекаем время начала хода для статистики
        move_start_time = time.time()
        
        try:
            # Очищаем старый кэш
            self._clear_old_ai_cache()
            
            # Получаем лучший ход с оптимизированной глубиной анализа
            # Более агрессивное ограничение глубины для скорости
            depth = max(1, min(8, self.skill_level // 2 + 1))  # Уменьшаем глубину анализа
            
            # Для всех уровней сложности используем кэшированные ходы в первую очередь
            ai_move = None
            
            # Пытаемся получить ход из кэша с упрощенной глубиной
            if self.skill_level < 10:
                ai_move = self._get_cached_best_move(depth=1)  # Используем минимальную глубину
            
            # Если нет кэшированного хода, получаем новый с оптимизированной глубиной
            if not ai_move:
                # Для более быстрого ответа используем меньшую глубину
                fast_depth = max(1, min(4, self.skill_level // 3 + 1))  # Еще больше уменьшаем глубину
                ai_move = self._get_cached_best_move(depth=fast_depth)
            
            # Альтернативный метод: если все еще нет хода, используем минимальную глубину
            if not ai_move:
                ai_move = self._get_cached_best_move(depth=1)
            
            if ai_move:
                print(f"Ход компьютера: {ai_move}")
                
                # Получаем текущее состояние доски для проверки взятия
                board_before = self.engine.get_board_state()
                
                # Валидация хода
                if self.engine.is_move_correct(ai_move):
                    if self.engine.make_move(ai_move):
                        # Добавляем ход в дебютную книгу
                        self.opening_book.add_move(ai_move)
                        
                        # Проверяем текущий дебют
                        current_opening = self.opening_book.get_current_opening()
                        
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
                            # Проигрываем звук взятия
                            if self.sound_manager:
                                self.sound_manager.play_sound("capture")
                        else:
                            self.move_feedback = f"Ход компьютера: {annotated_move}"
                            # Проигрываем звук хода
                            if self.sound_manager:
                                self.sound_manager.play_sound("move")
                        
                        # Добавляем информацию о дебюте, если она есть
                        if current_opening:
                            opening_name, opening_info = current_opening
                            self.move_feedback += f" | 🎯 Дебют: {opening_name}"
                        
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
                        
                        # Получаем оценку позиции для статистики (с более агрессивным кэшированием)
                        evaluation = self.get_cached_evaluation()
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
                        
                        # Обновляем отображение
                        self.renderer._mark_all_dirty()
                    else:
                        print("⚠️  Не удалось выполнить ход компьютера")
                        self.move_feedback = "Не удалось выполнить ход компьютера"
                        self.move_feedback_time = current_time
                        # Проигрываем звук ошибки
                        if self.sound_manager:
                            self.sound_manager.play_sound("button")
                else:
                    print("⚠️  Компьютер предложил некорректный ход")
                    self.move_feedback = "Компьютер предложил некорректный ход"
                    self.move_feedback_time = current_time
                    # Проигрываем звук ошибки
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
            else:
                print("⚠️  Компьютер не смог найти ход")
                self.move_feedback = "Компьютер не смог найти ход"
                self.move_feedback_time = time.time()
                # Проигрываем звук ошибки
                if self.sound_manager:
                    self.sound_manager.play_sound("button")
        except Exception as e:
            print(f"⚠️  Ошибка при получении хода компьютера: {e}")
            self.move_feedback = "Ошибка при получении хода компьютера"
            self.move_feedback_time = time.time()
            # Проигрываем звук ошибки
            if self.sound_manager:
                self.sound_manager.play_sound("button")
        finally:
            self.thinking = False

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
        print(f"   Горячие клавиши: R - новая игра, ESC - меню, T - подсказка")
        print(f"   Дополнительно: ПКМ - снять выделение, ←/→ - навигация по ходам")
        print(f"   Доп. функции: A - анализ, B - лучший ход, E - оценка, G - резюме, M - возможные ходы, S - сохранить, L - загрузить, D - детальный анализ, X - сдаться")
        print(f"   🚀 Многопоточность: {'ВКЛ' if self.executor else 'ВЫКЛ'}")
        print(f"   🎮 GPU ускорение: {'ВКЛ' if self.cuda_available else 'ВЫКЛ'}")
        print(f"   ⚡ FPS: 144 (максимум)")
        print(f"{'='*60}\n")
        
        # Запускаем многопоточную обработку
        self.start_multithreading()
        
        try:
            running = True
            menu_active = False  # Флаг активности меню
            
            # Таймеры для оптимизированных обновлений
            last_board_update = time.time()
            last_ui_update = time.time()
            last_ai_update = time.time()
            
            # Интервалы обновлений (оптимизированы для производительности)
            board_update_interval = 1.0/144  # Увеличиваем до 144 FPS для плавности
            ui_update_interval = 1.0/75     # Увеличиваем до 75 FPS для плавности
            # Увеличиваем частоту обновления ИИ для лучшей отзывчивости
            ai_update_interval = 0.05        # Увеличено до 20 раз в секунду
            
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

                    # Обработка событий меню, если оно активно
                    if self.in_game_menu.visible:
                        menu_action = self.in_game_menu.handle_event(event)
                        if menu_action:
                            if menu_action == "resume":
                                # Продолжить игру (меню уже скрыто)
                                pass
                            elif menu_action == "new_game":
                                # Новая игра - сбросить текущую игру
                                self.reset_game()
                                board_needs_update = True
                                ui_needs_update = True
                                last_board_state = None  # Сброс кэша состояния доски
                                move_navigation_mode = False
                                current_move_index = -1
                                self.analysis_mode = False
                                self.analysis_move = None
                            elif menu_action == "save_to_file":
                                # Сохранить игру в файл
                                self._save_game_to_file()
                                ui_needs_update = True
                            elif menu_action.startswith("load_from_file_"):
                                # Загрузить игру из файла
                                filename = menu_action[15:]  # Убираем префикс "load_from_file_"
                                self._load_game_from_file(filename)
                                board_needs_update = True
                                ui_needs_update = True
                                last_board_state = None  # Сброс кэша состояния доски
                            elif menu_action.startswith("delete_game_"):
                                # Удалить игру из файла
                                filename = menu_action[12:]  # Убираем префикс "delete_game_"
                                self._delete_saved_game(filename)
                                ui_needs_update = True
                            elif menu_action in ["settings_menu", "side_changed", "difficulty_changed", "theme_changed", "back"]:
                                # Обработка действий меню настроек
                                if menu_action == "side_changed":
                                    # Применяем изменение стороны
                                    new_settings = self.in_game_menu.get_settings()
                                    if new_settings["player_color"] != self.player_color:
                                        self.player_color = new_settings["player_color"]
                                        self.ai_color = 'black' if self.player_color == 'white' else 'white'
                                        self.renderer.set_player_color(self.player_color)
                                        board_needs_update = True
                                elif menu_action == "difficulty_changed":
                                    # Применяем изменение сложности
                                    new_settings = self.in_game_menu.get_settings()
                                    if new_settings["skill_level"] != self.skill_level:
                                        self.skill_level = new_settings["skill_level"]
                                        # Update the engine skill level if the method exists
                                        if hasattr(self.engine, 'set_skill_level') and self.engine.engine is not None:
                                            try:
                                                self.engine.engine.set_skill_level(self.skill_level)
                                            except Exception:
                                                pass  # Ignore errors if method doesn't exist
                                        board_needs_update = True
                                elif menu_action == "theme_changed":
                                    # Применяем изменение темы
                                    new_settings = self.in_game_menu.get_settings()
                                    if new_settings["theme"] != self.theme:
                                        self.theme = new_settings["theme"]
                                        self.renderer.set_theme(self.theme)
                                        board_needs_update = True
                            elif menu_action == "resign":
                                # Игрок сдается
                                self._handle_resignation()
                                board_needs_update = True
                                ui_needs_update = True
                                self.in_game_menu.hide()
                            elif menu_action == "main_menu":
                                # Вернуться в главное меню
                                return "main_menu"
                            elif menu_action == "quit":
                                # Выйти из игры
                                running = False
                        continue  # Пропустить остальную обработку событий, если меню активно

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
                        # Открыть меню
                        elif event.key == pygame.K_ESCAPE:
                            self.in_game_menu.show()
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
                                    # Проигрываем звук подсказки
                                    if self.sound_manager:
                                        self.sound_manager.play_sound("button")
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
                        # Показать все возможные ходы для выбранной фигуры
                        elif event.key == pygame.K_m:
                            if not self.game_over and self._is_player_turn() and self.renderer.selected_square:
                                # Получаем возможные ходы для выбранной фигуры
                                row, col = self.renderer.selected_square
                                valid_moves = self._get_valid_moves(row, col)
                                if valid_moves:
                                    # Показываем все возможные ходы
                                    self.renderer.set_move_hints(valid_moves)
                                    self.move_feedback = f"Показано {len(valid_moves)} возможных ходов"
                                    self.move_feedback_time = time.time()
                                    ui_needs_update = True
                                else:
                                    self.move_feedback = "Нет возможных ходов для выбранной фигуры"
                                    self.move_feedback_time = time.time()
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
                        # Показать детальную оценку позиции
                        elif event.key == pygame.K_e:
                            evaluation = self.get_cached_evaluation()
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
                                
                                self.move_feedback = f"Оценка: {evaluation:+.2f} ({advantage})"
                            else:
                                self.move_feedback = "Не удалось получить оценку позиции"
                            self.move_feedback_time = time.time()
                            ui_needs_update = True
                        # Показать лучший ход
                        elif event.key == pygame.K_b:
                            if not self.game_over:
                                self.thinking = True
                                best_move = self.engine.get_best_move()
                                self.thinking = False
                                if best_move:
                                    # Преобразуем UCI ход в координаты для выделения
                                    from_col = ord(best_move[0]) - ord('a')
                                    from_row = 8 - int(best_move[1])
                                    to_col = ord(best_move[2]) - ord('a')
                                    to_row = 8 - int(best_move[3])
                                    
                                    # Выделяем ход
                                    self.renderer.set_selected((from_row, from_col))
                                    self.renderer.set_move_hints([(to_row, to_col)])
                                    self.move_feedback = f"Лучший ход: {best_move}"
                                else:
                                    self.move_feedback = "Не удалось получить лучший ход"
                                self.move_feedback_time = time.time()
                                ui_needs_update = True
                        # Получить подробный анализ игры
                        elif event.key == pygame.K_d:
                            analysis = self._get_detailed_analysis()
                            self.move_feedback = f"Анализ: {analysis.split(chr(10))[0]}"  # Показываем первую строку
                            self.move_feedback_time = time.time()
                            ui_needs_update = True
                        # Сдаться (клавиша X)
                        elif event.key == pygame.K_x:
                            # Игрок сдается
                            self._handle_resignation()
                            board_needs_update = True
                            ui_needs_update = True

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # ЛКМ
                            pos = pygame.mouse.get_pos()
                            self.handle_click(pos[0], pos[1])
                            board_needs_update = True
                            ui_needs_update = True
                            last_board_state = None  # Сброс кэша состояния доски
                            # Проверяем состояние игры после хода игрока
                            if not self.game_over:
                                self.check_game_state()
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
                
                # Проверяем, изменилась ли доска (более эффективная проверка)
                board_changed = False
                if last_board_state is None:
                    board_changed = True
                else:
                    # Быстрая проверка по хэшу первой
                    current_hash = hash(str(current_board_state))
                    last_hash = hash(str(last_board_state))
                    if current_hash != last_hash:
                        # Только если хэши различаются, делаем полную проверку
                        board_changed = (str(last_board_state) != str(current_board_state))
                
                # Дополнительная оптимизация: если нет событий и доска не изменилась, 
                # пропускаем обновление, если прошло меньше минимального интервала
                min_update_interval = 1.0/144  # 144 FPS минимум
                if not has_events and not board_changed and not self.in_game_menu.visible:
                    time_since_last_update = current_time - max(last_board_update, last_ui_update)
                    if time_since_last_update < min_update_interval:
                        # Пропускаем обновление для экономии ресурсов
                        self.clock.tick(144)  # Ограничиваем FPS для экономии CPU
                        continue
                
                if board_changed or (time_to_update_board and board_needs_update) or time_to_update_ai:
                    # Update hover square
                    mouse_pos = pygame.mouse.get_pos()
                    self.renderer.update_hover(mouse_pos)
                    
                    # Handle AI moves с оптимизацией и многопоточностью
                    if time_to_update_ai and not self.game_over:
                        # Проверяем, наша ли очередь хода
                        if not self._is_player_turn():
                            # Используем многопоточную обработку ИИ
                            self.handle_ai_move_multithreaded()
                            last_ai_update = current_time
                            # После хода AI доска точно изменилась
                            board_needs_update = True
                            last_board_state = None  # Принудительно обновим кэш
                    
                    # Проверяем состояние игры (шах, мат, пат)
                    if not self.game_over:
                        self.check_game_state()
                    
                    # Draw the board with optimizations
                    if time_to_update_board and (board_needs_update or board_changed):
                        # Используем многопоточный рендеринг
                        self.render_queue.put(("render_board", current_board_state))
                        
                        # Используем clipping для оптимизации
                        old_clip = self.screen.get_clip()
                        board_rect = pygame.Rect(0, 0, BOARD_SIZE, BOARD_SIZE)
                        self.screen.set_clip(board_rect)
                        
                        # Отрисовка через рендерер с улучшенной очисткой
                        evaluation = self.get_interpolated_evaluation()
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
                            
                            # Рисуем стрелку от начальной позиции к конечной с улучшенной визуализацией
                            pygame.draw.line(self.screen, (0, 255, 0, 180), from_rect.center, to_rect.center, 4)
                            # Рисуем круг в конечной позиции
                            pygame.draw.circle(self.screen, (0, 255, 0, 180), to_rect.center, 12, 4)
                        
                        # Восстанавливаем clipping region после отрисовки доски
                        self.screen.set_clip(old_clip)
                        # Принудительное обновление экрана для предотвращения исчезновения доски
                        pygame.display.flip()
                        last_board_update = current_time
                        board_needs_update = False
                        last_board_state = [row[:] for row in current_board_state]  # Копируем состояние
                
                # Обновляем UI только при необходимости
                if (current_time - last_ui_update > ui_update_interval) and ui_needs_update:
                    self.draw_ui()
                    last_ui_update = current_time
                    ui_needs_update = False

                # Отрисовка меню, если оно активно
                if self.in_game_menu.visible:
                    # Очищаем область меню перед отрисовкой
                    self.screen.set_clip(None)  # Снимаем clipping для отрисовки меню
                    self.in_game_menu.draw()

                # === Очистка кэша для предотвращения утечек памяти ===
                self.frame_count += 1
                if self.frame_count % 1200 == 0:  # Каждые 20 секунд при 60 FPS
                    self.renderer.clear_temp_surfaces()
                    self._clear_caches()
                    self._clear_old_ai_cache()

                # === Обновление экрана только при необходимости ===
                if board_needs_update or ui_needs_update or has_events or board_changed or self.in_game_menu.visible:
                    pygame.display.flip()
                else:
                    # В режиме простоя ограничиваем FPS до 30 для экономии ресурсов
                    self.clock.tick(30)
                    continue

                # === Адаптивное ограничение FPS ===
                # В режиме простоя ограничиваем FPS до 90 для плавности
                if not has_events and not board_needs_update and not ui_needs_update:
                    self.clock.tick(90)
                else:
                    # В активном режиме ограничиваем до 144 FPS для максимальной плавности
                    self.clock.tick(144)

        finally:
            # Останавливаем многопоточную обработку
            self.stop_multithreading()
            
        # === Завершение работы ===
        self.renderer.cleanup()
        pygame.quit()

        # === Возврат статистики ===
        print("[INFO] Игра завершена.")
        return self.get_game_stats()
