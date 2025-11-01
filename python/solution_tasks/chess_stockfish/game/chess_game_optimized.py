# ============================================================================
# game/chess_game_optimized.py
# ============================================================================

"""
Модуль: game/chess_game_optimized.py

Описание:
    Оптимизированная версия класса ChessGame с улучшенными алгоритмами кэширования,
    многопоточностью и производительностью.

Основные улучшения:
    - Улучшенные алгоритмы кэширования с более агрессивной стратегией
    - Оптимизированная многопоточность с пулом потоков
    - Адаптивная частота обновления на основе производительности
    - Улучшенное управление памятью с использованием слабых ссылок
    - Оптимизированные алгоритмы генерации ходов
"""

import pygame
from typing import Optional, Tuple, List
import time
import sys
import random
import concurrent.futures
import threading
from queue import Queue, Empty
import weakref

# Import our modules
from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer
from utils.educational import ChessEducator
from utils.opening_book import OpeningBook
from utils.sound_manager import SoundManager
from game.in_game_menu import InGameMenu
from utils.performance_monitor import get_performance_monitor, PerformanceTimer  # Добавляем импорт монитора производительности

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

class ChessGameOptimized:
    """
    Оптимизированная версия класса ChessGame с улучшенной производительностью.
    """
    
    def __init__(self, player_color: str = 'white', skill_level: int = 5, theme: str = 'classic'):
        """
        Инициализация оптимизированной игры.
        
        Параметры:
            player_color (str): Выбранная сторона ('white' или 'black')
            skill_level (int): Уровень сложности Stockfish (0-20)
            theme (str): Цветовая тема доски
        """
        # Инициализируем монитор производительности
        self.performance_monitor = get_performance_monitor()
        self.performance_monitor.start_monitoring(0.25)  # Мониторим каждые 0.25 секунды для оптимизированной версии
        
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
            if not pygame.get_init():
                pygame.init()
            
            self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE + 100))
            pygame.display.set_caption(f"♟️  chess_stockfish OPTIMIZED — Maestro7IT (уровень {skill_level})")
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось инициализировать графический интерфейс: {e}")
        
        # Создаём рендерер
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
        self.sound_manager.play_background_music()
        
        # Инициализируем игровое меню
        self.in_game_menu = InGameMenu(self.screen, self.sound_manager)
        
        # Состояние игры
        self.move_history = []
        self.move_annotations = []
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.ai_move_delay = 0.02  # Ещё более быстрая задержка ИИ
        self.move_feedback = ""
        self.move_feedback_time = 0
        self.frame_count = 0
        self.highlight_hint = None
        
        # Улучшенная система кэширования
        self._cache = {
            'board_state': None,
            'board_fen': None,
            'valid_moves': {},
            'uci_conversions': {},
            'last_evaluation': None,
            'last_eval_fen': None
        }
        
        # Расширенные кэши с увеличенным временем жизни
        self._valid_moves_cache = {}
        self._valid_moves_cache_time = {}
        self._valid_moves_cache_duration = 15.0  # Увеличиваем до 15 секунд для лучшей производительности
        self._valid_moves_board_hash = {}
        
        self._ai_move_cache = {}
        self._ai_move_cache_time = {}
        self._ai_move_cache_duration = 300.0  # Увеличиваем до 5 минут для максимального кэширования
        self._ai_move_board_hash = {}
        
        # Графические оптимизации
        self.last_board_hash = None
        self.dirty_squares = set()
        
        # Таймеры для оптимизации обновлений
        self.last_board_update = 0
        self.last_ui_update = 0
        self.board_update_interval = 1.0/144  # 144 FPS для доски
        self.ui_update_interval = 1.0/90     # Увеличиваем до 90 FPS для UI
        
        # Инициализация графических ресурсов
        self._init_fonts_optimized()
        self._init_piece_surfaces()
        self._init_highlight_surfaces()
        
        # Оптимизация AI
        self.ai_move_cache = {}
        self.last_ai_move_time = 0
        self.ai_move_cooldown = 0.0001  # Уменьшаем минимальную задержку ИИ для более быстрой игры
        
        # Дополнительные оптимизации
        self.board_state_cache = None
        self.board_state_cache_time = 0
        self.board_state_cache_duration = 5.0  # Увеличиваем до 5 секунд кэширования состояния доски
        self.board_state_last_fen = None
        
        # Расширенная статистика игры
        self.game_stats = {
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
        
        # Улучшенный геймплей
        self.last_move_was_capture = False
        self.combo_counter = 0
        self.special_move_messages = []
        self.last_evaluation = 0
        
        # Для режима анализа
        self.analysis_mode = False
        self.analysis_move = None
        
        # Для сохранения/загрузки партий
        self.saved_games = []
        
        # Многопоточность с увеличенным пулом
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=32)  # Увеличиваем до 32 потоков
        self.ai_move_queue = Queue()
        self.render_queue = Queue()
        self.ai_thread = None
        self.render_thread = None
        self.ai_thread_running = False
        self.render_thread_running = False
        
        # GPU ускорение
        self.cuda_available = CUDA_AVAILABLE
        if self.cuda_available:
            print("✅ CUDA доступна для ускорения вычислений")
        else:
            print("⚠️  CUDA недоступна, используется CPU")
            
        # Асинхронная оценка позиции
        self._async_eval_future = None
        self._last_async_eval_time = 0
        self._async_eval_interval = 0.01  # Увеличиваем частоту до 100 FPS для оценки позиции
        
        # Прогрессивная оценка позиции
        self._displayed_evaluation = 0.0
        self._target_evaluation = 0.0
        self._eval_update_time = 0
        self._eval_interpolation_duration = 0.01  # Быстрая интерполяция 100 FPS
        
        # Слабые ссылки для предотвращения утечек памяти
        self._weakref_cache = weakref.WeakValueDictionary()
        
        # Адаптивная частота обновления
        self._perf_metrics = {
            'frame_times': [],
            'last_perf_check': time.time(),
            'target_fps': 144  # Целевая частота кадров
        }

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
        try:
            self.fonts = {
                'piece': pygame.font.SysFont('Segoe UI Symbol', SQUARE_SIZE - 10),
                'coord': pygame.font.SysFont('Arial', 14, bold=True),
                'ui': pygame.font.SysFont('Arial', 16),
                'ui_small': pygame.font.SysFont('Arial', 12)
            }
        except:
            self.fonts = {
                'piece': pygame.font.Font(None, SQUARE_SIZE - 10),
                'coord': pygame.font.Font(None, 14),
                'ui': pygame.font.Font(None, 16),
                'ui_small': pygame.font.Font(None, 12)
            }
    
    def _init_piece_surfaces(self):
        """Предзагрузка и кэширование поверхностей фигур."""
        self.piece_surfaces = {}
        
        PIECE_UNICODE = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }
        
        for piece in ['K', 'Q', 'R', 'B', 'N', 'P', 'k', 'q', 'r', 'b', 'n', 'p']:
            if piece in PIECE_UNICODE:
                try:
                    surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    font = self.fonts.get('piece', pygame.font.SysFont('Arial', SQUARE_SIZE - 10))
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
        
        highlight_configs = {
            'selected': ((124, 252, 0, 180), 3),
            'last_move': ((255, 255, 0, 150), 2),
            'valid_move': ((0, 0, 255, 100), 0),
            'check': ((255, 0, 0, 180), 2),
            'hint': ((0, 255, 0, 120), 2)
        }
        
        for highlight_type, (color, width) in highlight_configs.items():
            surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            
            if highlight_type == 'valid_move':
                pygame.draw.circle(surface, color, 
                                 (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//6)
            else:
                rect = surface.get_rect()
                if width > 0:
                    pygame.draw.rect(surface, color, rect, width)
                else:
                    pygame.draw.rect(surface, color, rect)
                
            self.highlight_surfaces[highlight_type] = surface

    def _coord_to_fen_square(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Преобразует экранные координаты клика в FEN координаты."""
        return self.renderer.coord_mapper.pixel_to_square(x, y)
    
    def _fen_square_to_uci(self, row: int, col: int) -> str:
        """Преобразует FEN координаты в UCI формат с кэшированием."""
        if not hasattr(self, '_uci_cache'):
            self._uci_cache = {}
        
        cache_key = (row, col)
        if cache_key in self._uci_cache:
            return self._uci_cache[cache_key]
        
        uci = chr(ord('a') + col) + str(8 - row)
        self._uci_cache[cache_key] = uci
        return uci
    
    def get_board_state(self) -> List[List[Optional[str]]]:
        """Получение состояния доски с кэшированием."""
        try:
            current_time = time.time()
            current_fen = self.engine.get_fen()
            
            if (self.board_state_cache is not None and 
                current_time - self.board_state_cache_time < self.board_state_cache_duration and
                (self.board_state_last_fen == current_fen or 
                 current_time - self.board_state_cache_time < 0.05)):
                return self.board_state_cache
            
            board = self.engine.get_board_state()
            
            self.board_state_cache = board
            self.board_state_cache_time = current_time
            self.board_state_last_fen = current_fen
            
            return board
        except Exception:
            empty_board: List[List[Optional[str]]] = [[None for _ in range(8)] for _ in range(8)]
            self.board_state_cache = empty_board
            self.board_state_cache_time = time.time()
            self.board_state_last_fen = None
            return empty_board
    
    def get_cached_evaluation(self):
        """Получение кэшированной оценки позиции."""
        try:
            current_fen = self.engine.get_fen()
            current_time = time.time()
            
            if (self._cache['last_eval_fen'] == current_fen and 
                self._cache['last_evaluation'] is not None and
                hasattr(self, '_last_eval_cache_time')):
                if (current_time - self._last_eval_cache_time) < 120.0:  # 2 минуты кэширования
                    return self._cache['last_evaluation']
                
            evaluation = self.engine.get_evaluation()
            self._cache['last_evaluation'] = evaluation
            self._cache['last_eval_fen'] = current_fen
            self._last_eval_cache_time = current_time
            return evaluation
        except Exception:
            if self._cache['last_evaluation'] is not None:
                return self._cache['last_evaluation']
            return None

    def get_interpolated_evaluation(self):
        """Получение интерполированной оценки позиции."""
        current_time = time.time()
        real_evaluation = self.get_cached_evaluation()
        
        if self._target_evaluation == 0.0 and real_evaluation is not None:
            self._target_evaluation = real_evaluation
            self._displayed_evaluation = real_evaluation
            self._eval_update_time = current_time
            return real_evaluation
        
        if real_evaluation is not None and real_evaluation != self._target_evaluation:
            self._target_evaluation = real_evaluation
            self._eval_update_time = current_time
        
        if self._target_evaluation != self._displayed_evaluation:
            elapsed = current_time - self._eval_update_time
            if elapsed >= self._eval_interpolation_duration:
                self._displayed_evaluation = self._target_evaluation
            else:
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
        direction = -1 if is_white else 1
        
        new_row = row + direction
        if 0 <= new_row < 8 and board[new_row][col] is None:
            moves.append((new_row, col))
            
            start_row = 6 if is_white else 1
            if row == start_row:
                new_row_2 = row + 2 * direction
                if 0 <= new_row_2 < 8 and board[new_row][col] is None and board[new_row_2][col] is None:
                    moves.append((new_row_2, col))
        
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
        bishop_moves = self._get_bishop_moves(row, col, piece, board)
        rook_moves = self._get_rook_moves(row, col, piece, board)
        return bishop_moves + rook_moves

    def _get_king_moves(self, row: int, col: int, piece: str, board: List[List[Optional[str]]]) -> List[Tuple[int, int]]:
        """Генерация возможных ходов для короля."""
        moves = []
        is_white = piece.isupper()
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
        """
        cache_key = (from_row, from_col)
        current_time = time.time()
        
        board_state = self.get_board_state()
        board_hash = hash(str(board_state))
        
        if cache_key in self._valid_moves_cache:
            cache_time = self._valid_moves_cache_time[cache_key]
            cached_board_hash = self._valid_moves_board_hash.get(cache_key, None)
            
            is_time_valid = (current_time - cache_time < self._valid_moves_cache_duration)
            is_position_valid = (cached_board_hash == board_hash)
            is_fresh_cache = (current_time - cache_time < 0.1)
            
            if is_time_valid and (is_position_valid or is_fresh_cache):
                return self._valid_moves_cache[cache_key][:]
        
        valid_moves = []
        from_uci = self._fen_square_to_uci(from_row, from_col)
        
        try:
            piece = board_state[from_row][from_col]
            if not piece:
                self._valid_moves_cache[cache_key] = []
                self._valid_moves_cache_time[cache_key] = current_time
                self._valid_moves_board_hash[cache_key] = board_hash
                return valid_moves
                
            piece_lower = piece.lower()
            
            if piece_lower == 'p':
                candidate_moves = self._get_pawn_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'n':
                candidate_moves = self._get_knight_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'b':
                candidate_moves = self._get_bishop_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'r':
                candidate_moves = self._get_rook_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'q':
                candidate_moves = self._get_queen_moves(from_row, from_col, piece, board_state)
            elif piece_lower == 'k':
                candidate_moves = self._get_king_moves(from_row, from_col, piece, board_state)
            else:
                candidate_moves = []
                
            for to_row, to_col in candidate_moves:
                to_uci = self._fen_square_to_uci(to_row, to_col)
                uci_move = from_uci + to_uci
                if self.engine.is_move_correct(uci_move):
                    valid_moves.append((to_row, to_col))
                    
        except Exception as e:
            print(f"Ошибка при расчете допустимых ходов: {e}")
        
        self._valid_moves_cache[cache_key] = valid_moves[:]
        self._valid_moves_cache_time[cache_key] = current_time
        self._valid_moves_board_hash[cache_key] = board_hash
            
        return valid_moves

    def _is_player_turn(self) -> bool:
        """Проверяет, является ли текущий ход ходом игрока."""
        try:
            side = self.engine.get_side_to_move()
            return (
                (self.player_color == 'white' and side == 'w') or
                (self.player_color == 'black' and side == 'b')
            )
        except Exception:
            return True
    
    def _is_player_piece(self, piece: Optional[str]) -> bool:
        """Проверяет, принадлежит ли фигура игроку."""
        if not piece:
            return False
        is_white = piece.isupper()
        return (self.player_color == 'white') == is_white

    def handle_click(self, x: int, y: int):
        """Обработка клика по доске."""
        try:
            if self.game_over or self.thinking or not self._is_player_turn():
                return
            
            coords = self._coord_to_fen_square(x, y)
            if coords is None:
                self.renderer.set_selected(None)
                self.renderer.set_move_hints([])
                return
            
            row, col = coords
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
            
            if self._is_player_piece(piece) and piece is not None:
                self.renderer.set_selected((row, col))
                valid_moves = self._get_valid_moves(row, col)
                self.renderer.set_move_hints(valid_moves)
                piece_name = {
                    'P': 'пешка', 'N': 'конь', 'B': 'слон', 'R': 'ладья', 
                    'Q': 'ферзь', 'K': 'король', 'p': 'пешка', 'n': 'конь', 
                    'b': 'слон', 'r': 'ладья', 'q': 'ферзь', 'k': 'король'
                }.get(piece, piece)
                self.move_feedback = f"Выбрана {piece_name}"
                self.move_feedback_time = time.time()
                
                if hasattr(self, '_piece_hint_cache') and piece in self._piece_hint_cache:
                    piece_hint = self._piece_hint_cache[piece]
                else:
                    piece_hint = self.educator.get_piece_hint(piece_name)
                    if not hasattr(self, '_piece_hint_cache'):
                        self._piece_hint_cache = {}
                    self._piece_hint_cache[piece] = piece_hint
                self.move_feedback += f" | {piece_hint}"
            elif self.renderer.selected_square:
                from_sq = self.renderer.selected_square
                to_sq = (row, col)
                
                from_uci = self._fen_square_to_uci(*from_sq)
                to_uci = self._fen_square_to_uci(*to_sq)
                uci_move = from_uci + to_uci
                
                move_start_time = time.time()
                
                try:
                    if self.engine.is_move_correct(uci_move):
                        target_piece = board[to_sq[0]][to_sq[1]]
                        is_capture = target_piece is not None
                        
                        is_check = False
                        is_mate = False
                        is_castling = uci_move in ['e1g1', 'e1c1', 'e8g8', 'e8c8']
                        
                        if self.engine.make_move(uci_move):
                            self.opening_book.add_move(uci_move)
                            current_opening = self.opening_book.get_current_opening()
                            
                            is_over, reason = self.engine.is_game_over()
                            if is_over and reason and "мат" in reason:
                                is_mate = True
                            
                            try:
                                eval_result = self.engine.get_evaluation()
                                if eval_result and isinstance(eval_result, dict):
                                    is_check = eval_result.get('check', False)
                            except:
                                pass
                            
                            annotated_move = self._annotate_move(uci_move, is_capture, is_check, is_mate, is_castling)
                            
                            self.move_history.append(uci_move)
                            self.move_annotations.append(annotated_move)
                            self.game_stats['player_moves'] += 1
                            if is_capture:
                                self.game_stats['player_capture_count'] += 1
                                self.last_move_was_capture = True
                                self.combo_counter += 1
                                if self.combo_counter >= 2:
                                    self.special_move_messages.append(f"Комбо x{self.combo_counter}!")
                                    if self.sound_manager:
                                        self.sound_manager.play_sound("capture")
                            else:
                                self.last_move_was_capture = False
                                self.combo_counter = 0
                            
                            self.renderer.set_last_move(from_sq, to_sq)
                            self.renderer.set_selected(None)
                            self.renderer.set_move_hints([])
                            
                            self.last_move_time = time.time()
                            print(f"Ход выполнен: {annotated_move}")
                            self.move_feedback = f"Ход {annotated_move} выполнен"
                            self.move_feedback_time = time.time()
                            
                            if self.sound_manager:
                                if is_capture:
                                    self.sound_manager.play_sound("capture")
                                elif is_castling:
                                    self.sound_manager.play_sound("castle")
                                else:
                                    self.sound_manager.play_sound("move")
                            
                            if current_opening:
                                opening_name, opening_info = current_opening
                                self.move_feedback += f" | 🎯 Дебют: {opening_name}"
                            
                            move_time = time.time() - move_start_time
                            self.game_stats['move_times'].append(move_time)
                            
                            evaluation = self.get_cached_evaluation()
                            if evaluation is not None:
                                self.game_stats['evaluations'].append(evaluation)
                            
                            move_count = len(self.move_history)
                            current_time = time.time()
                            
                            edu_cache_key = move_count
                            edu_cache_duration = 60.0  # Максимальное кэширование подсказок
                            
                            educational_tip = None
                            if hasattr(self, '_edu_feedback_cache') and hasattr(self, '_edu_feedback_cache_time'):
                                if (edu_cache_key in self._edu_feedback_cache and 
                                    current_time - self._edu_feedback_cache_time[edu_cache_key] < edu_cache_duration):
                                    educational_tip = self._edu_feedback_cache[edu_cache_key]
                            
                            if educational_tip is None:
                                educational_tip = self.educator.get_educational_feedback(move_count, current_time)
                                if not hasattr(self, '_edu_feedback_cache'):
                                    self._edu_feedback_cache = {}
                                    self._edu_feedback_cache_time = {}
                                self._edu_feedback_cache[edu_cache_key] = educational_tip
                                self._edu_feedback_cache_time[edu_cache_key] = current_time
                            
                            if educational_tip:
                                self.move_feedback += f" | {educational_tip}"
                                self.move_feedback_time = current_time
                            
                            if self.special_move_messages:
                                self.move_feedback += f" | {self.special_move_messages[0]}"
                                self.special_move_messages.pop(0)
                                
                            self.renderer._mark_all_dirty()
                            pygame.display.flip()
                        else:
                            print("❌ Не удалось выполнить ход")
                            self.renderer.set_selected(None)
                            self.renderer.set_move_hints([])
                            self.move_feedback = "Не удалось выполнить ход"
                            self.move_feedback_time = time.time()
                            if self.sound_manager:
                                self.sound_manager.play_sound("button")
                            self.renderer._mark_all_dirty()
                            pygame.display.flip()
                            pygame.display.flip()
                    else:
                        print(f"❌ Некорректный ход: {uci_move}")
                        self.renderer.set_selected(None)
                        self.renderer.set_move_hints([])
                        hint = self._get_move_hint(from_sq[0], from_sq[1], row, col)
                        self.move_feedback = hint
                        self.move_feedback_time = time.time()
                        if self.sound_manager:
                            self.sound_manager.play_sound("button")
                        self.renderer._mark_all_dirty()
                        pygame.display.flip()
                except Exception as e:
                    print(f"⚠️  Ошибка при обработке хода: {e}")
                    self.renderer.set_selected(None)
                    self.renderer.set_move_hints([])
                    self.move_feedback = "Ошибка при выполнении хода"
                    self.move_feedback_time = time.time()
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
                    self.renderer._mark_all_dirty()
            else:
                self.renderer.set_selected(None)
                self.renderer.set_move_hints([])
                self.renderer._mark_all_dirty()
                pygame.display.flip()
        except Exception as e:
            print(f"⚠️  Критическая ошибка при обработке клика: {e}")
            self.move_feedback = "Критическая ошибка при обработке клика"
            self.move_feedback_time = time.time()
            if self.sound_manager:
                self.sound_manager.play_sound("button")

    def handle_ai_move(self):
        """Получить и выполнить ход ИИ."""
        if self._is_player_turn() or self.game_over or self.thinking:
            return
        
        if time.time() - self.last_move_time < self.ai_move_delay:
            return
        
        self.thinking = True
        try:
            depth = max(1, min(20, self.skill_level + 5))
            
            ai_move = None
            best_moves = self.engine.get_best_moves(3)
            
            if len(best_moves) > 1 and self.skill_level < 15:
                if random.random() < 0.3:
                    ai_move = best_moves[min(1, len(best_moves) - 1)]
                else:
                    ai_move = best_moves[0]
            else:
                ai_move = self.engine.get_best_move(depth=depth)
            
            if ai_move:
                print(f"Ход компьютера: {ai_move}")
                if self.engine.is_move_correct(ai_move):
                    if self.engine.make_move(ai_move):
                        self.move_history.append(ai_move)
                        
                        if hasattr(self, '_cached_board'):
                            delattr(self, '_cached_board')
                        
                        from_col = ord(ai_move[0]) - ord('a')
                        from_row = 8 - int(ai_move[1])
                        to_col = ord(ai_move[2]) - ord('a')
                        to_row = 8 - int(ai_move[3])
                        self.renderer.set_last_move((from_row, from_col), (to_row, to_col))
                        self.last_move_time = time.time()
                        print(f"Ход компьютера выполнен: {ai_move}")
                        self.move_feedback = f"Ход компьютера: {ai_move}"
                        self.move_feedback_time = time.time()
                        
                        educational_tip = self.educator.get_educational_feedback(
                            len(self.move_history), time.time())
                        if educational_tip:
                            self.move_feedback += f" | {educational_tip}"
                            self.move_feedback_time = time.time()
                        
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

    def _annotate_move(self, uci_move: str, is_capture: bool = False, is_check: bool = False, 
                      is_mate: bool = False, is_castling: bool = False) -> str:
        """Аннотировать ход с помощью специальных символов."""
        annotation = uci_move
        
        if is_castling:
            if uci_move in ['e1g1', 'e8g8']:
                annotation = "O-O"
            elif uci_move in ['e1c1', 'e8c8']:
                annotation = "O-O-O"
            
        if is_capture:
            annotation += "x"
            
        if is_check and not is_mate:
            annotation += "+"
        elif is_mate:
            annotation += "#"
            
        return annotation

    def run(self):
        """Запустить основной цикл игры с оптимизациями."""
        print(f"\n{'='*60}")
        print(f"🎮 Игра началась! (ОПТИМИЗИРОВАННАЯ ВЕРСИЯ)")
        print(f"   Вы играете: {self.player_color.upper()}")
        print(f"   Компьютер: {self.ai_color.upper()}")
        print(f"   Уровень: {self.skill_level}/20")
        print(f"   🚀 Многопоточность: ВКЛ ({12} потоков)")
        print(f"   🎮 GPU ускорение: {'ВКЛ' if self.cuda_available else 'ВЫКЛ'}")
        print(f"   ⚡ FPS: 144 (максимум)")
        print(f"{'='*60}\n")
        
        try:
            running = True
            menu_active = False
            
            last_board_update = time.time()
            last_ui_update = time.time()
            last_ai_update = time.time()
            
            board_update_interval = 1.0/144  # 144 FPS для доски
            ui_update_interval = 1.0/90     # 90 FPS для UI
            ai_update_interval = 0.025       # 40 FPS для ИИ
            
            board_needs_update = True
            ui_needs_update = True
            last_board_state: Optional[List[List[Optional[str]]]] = None
            
            move_navigation_mode = False
            current_move_index = -1
            
            while running:
                current_time = time.time()
                has_events = False
                
                for event in pygame.event.get():
                    has_events = True
                    if event.type == pygame.QUIT:
                        running = False

                    if self.in_game_menu.visible:
                        menu_action = self.in_game_menu.handle_event(event)
                        if menu_action:
                            # Обработка действий меню
                            continue
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()
                            board_needs_update = True
                            ui_needs_update = True
                            last_board_state = None
                            move_navigation_mode = False
                            current_move_index = -1
                            self.analysis_mode = False
                            self.analysis_move = None
                        elif event.key == pygame.K_t:
                            if not self.game_over and self._is_player_turn():
                                self.thinking = True
                                best_move = self._get_cached_best_move()
                                self.thinking = False
                                if best_move:
                                    print(f"[ENGINE] Совет: {best_move}")
                                    self.highlight_hint = best_move
                                    self.move_feedback = f"Подсказка: {best_move}"
                                    self.move_feedback_time = time.time()
                                    ui_needs_update = True
                                    if self.sound_manager:
                                        self.sound_manager.play_sound("button")
                                else:
                                    self.move_feedback = "Не удалось получить подсказку"
                                    self.move_feedback_time = time.time()
                                    ui_needs_update = True
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            self.handle_click(pos[0], pos[1])
                            board_needs_update = True
                            ui_needs_update = True
                            last_board_state = None
                            if not self.game_over:
                                self.check_game_state()

                time_to_update_board = (current_time - last_board_update > board_update_interval)
                time_to_update_ai = (current_time - last_ai_update > ai_update_interval)
                
                current_board_state: List[List[Optional[str]]] = self.get_board_state()
                
                board_changed = False
                if last_board_state is None:
                    board_changed = True
                else:
                    current_hash = hash(str(current_board_state))
                    last_hash = hash(str(last_board_state))
                    if current_hash != last_hash:
                        board_changed = (str(last_board_state) != str(current_board_state))
                
                # Увеличиваем минимальный интервал для лучшей производительности
                min_update_interval = 1.0/144  # 144 FPS минимум
                if not has_events and not board_changed and not self.in_game_menu.visible:
                    time_since_last_update = current_time - max(last_board_update, last_ui_update)
                    if time_since_last_update < min_update_interval:
                        # Ограничиваем FPS для экономии CPU при бездействии
                        self.clock.tick(144)
                        continue
                
                if board_changed or (time_to_update_board and board_needs_update) or time_to_update_ai:
                    mouse_pos = pygame.mouse.get_pos()
                    self.renderer.update_hover(mouse_pos)
                    
                    if time_to_update_ai and not self.game_over:
                        if not self._is_player_turn():
                            self.handle_ai_move_multithreaded()
                            last_ai_update = current_time
                            board_needs_update = True
                            last_board_state = None
                    
                    if not self.game_over:
                        self.check_game_state()
                    
                    if time_to_update_board and (board_needs_update or board_changed):
                        old_clip = self.screen.get_clip()
                        board_rect = pygame.Rect(0, 0, BOARD_SIZE, BOARD_SIZE)
                        self.screen.set_clip(board_rect)
                        
                        evaluation = self.get_interpolated_evaluation()
                        self.renderer.draw(current_board_state, evaluation=evaluation, thinking=self.thinking, 
                                         mouse_pos=mouse_pos, move_count=len(self.move_history),
                                         capture_count=(self.game_stats['player_capture_count'], 
                                                      self.game_stats['ai_capture_count']),
                                         check_count=self.game_stats['check_count'])
                        
                        self.screen.set_clip(old_clip)
                        pygame.display.flip()
                        last_board_update = current_time
                        board_needs_update = False
                        last_board_state = [row[:] for row in current_board_state]
                
                if (current_time - last_ui_update > ui_update_interval) and ui_needs_update:
                    self.draw_ui()
                    last_ui_update = current_time
                    ui_needs_update = False

                if self.in_game_menu.visible:
                    self.screen.set_clip(None)
                    self.in_game_menu.draw()

                    menu_active = True
                else:
                    menu_active = False

                self.frame_count += 1
                if self.frame_count % 600 == 0:  # Каждые 10 секунд при 60 FPS
                    self.renderer.clear_temp_surfaces()
                    self._clear_caches()
                    self._clear_old_ai_cache()

                if board_needs_update or ui_needs_update or has_events or board_changed or self.in_game_menu.visible:
                    pygame.display.flip()
                else:
                    self.clock.tick(45)
                    continue

                # Адаптивное ограничение FPS для максимальной плавности
                if not has_events and not board_needs_update and not ui_needs_update:
                    self.clock.tick(90)  # В режиме простоя
                else:
                    self.clock.tick(144)  # В активном режиме

        finally:
            self.executor.shutdown(wait=False)
            
        self.renderer.cleanup()
        pygame.quit()
        print("[INFO] Игра завершена.")
        return self.get_game_stats()

    def _get_cached_best_move(self, depth=None):
        """Получить лучший ход с кэшированием."""
        fen = self.engine.get_fen()
        cache_key = (fen, depth, self.skill_level)
        
        current_time = time.time()
        if cache_key in self._ai_move_cache:
            cached_move, cache_time = self._ai_move_cache[cache_key]
            is_time_valid = (current_time - cache_time < 30.0)
            is_fresh_cache = (current_time - cache_time < 1.5)
            
            if is_time_valid or is_fresh_cache:
                return cached_move
        
        if depth is None:
            depth = max(1, min(8, self.skill_level))
        
        best_move = self.engine.get_best_move(depth=depth)
        
        if best_move:
            self._ai_move_cache[cache_key] = (best_move, current_time)
            
        return best_move

    def _clear_old_ai_cache(self):
        """Очистка старых записей в кэше AI."""
        current_time = time.time()
        expired_keys = []
        
        for key, (_, cache_time) in self._ai_move_cache.items():
            if current_time - cache_time > 60.0:  # 1 минута
                expired_keys.append(key)
                
        for key in expired_keys:
            del self._ai_move_cache[key]
            
    def _clear_caches(self):
        """Очистить кэши для оптимизации памяти."""
        if hasattr(self, '_uci_cache'):
            self._uci_cache.clear()
        if hasattr(self, '_cached_board'):
            delattr(self, '_cached_board')
        if hasattr(self, '_piece_name_cache'):
            self._piece_name_cache.clear()
        self._valid_moves_cache.clear()
        self._valid_moves_cache_time.clear()
        if hasattr(self, '_valid_moves_board_hash'):
            self._valid_moves_board_hash.clear()
        if hasattr(self, '_edu_feedback_cache'):
            self._edu_feedback_cache.clear()
        if hasattr(self, '_edu_feedback_cache_time'):
            self._edu_feedback_cache_time.clear()
        if hasattr(self, '_piece_hint_cache'):
            self._piece_hint_cache.clear()
        if hasattr(self, '_king_pos_cache'):
            self._king_pos_cache.clear()
        if hasattr(self, '_king_pos_cache_time'):
            self._king_pos_cache_time.clear()

    def reset_game(self):
        """Сбросить игру к начальному состоянию."""
        print("🔄 Новая игра...")
        self.engine.reset_board()
        
        self.move_history = []
        self.thinking = False
        self.game_over = False
        self.game_over_reason = None
        self.last_move_time = 0
        self.move_feedback = ""
        self.move_feedback_time = 0
        self.highlight_hint = None
        
        self.renderer.set_selected(None)
        self.renderer.last_move = None
        self.renderer.set_move_hints([])
        self.renderer.set_check(None)
        
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

    def check_game_state(self) -> bool:
        """Проверить текущее состояние игры."""
        try:
            is_over, reason = self.engine.is_game_over()
            if is_over:
                self.game_over = True
                self.game_over_reason = reason
                self.move_feedback = reason
                self.move_feedback_time = time.time()
                
                self.game_stats['end_time'] = time.time()
                self.game_stats['duration'] = self.game_stats['end_time'] - self.game_stats['start_time']
                
                if reason and ("мат" in reason or "Мат" in reason):
                    self.game_stats['result'] = "checkmate"
                elif reason and ("Пат" in reason or "пат" in reason or "Ничья" in reason):
                    self.game_stats['result'] = "stalemate"
                else:
                    self.game_stats['result'] = "resignation"
                
                return True
            
            try:
                side_to_move = self.engine.get_side_to_move()
                is_white_to_move = (side_to_move == 'w')
                
                eval_result = self.engine.get_evaluation()
                is_king_in_check = False
                
                if eval_result and isinstance(eval_result, dict):
                    if 'check' in eval_result:
                        is_king_in_check = eval_result['check']
                    elif isinstance(eval_result, dict) and eval_result.get('type') == 'cp':
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
                    
                    board_state = self.engine.get_board_state()
                    king_pos = self._find_king_position(board_state, is_white_to_move)
                    if king_pos:
                        self.renderer.set_check(king_pos)
                    else:
                        self.renderer.set_check(None)
                else:
                    self.renderer.set_check(None)
                    
            except Exception:
                pass
                
        except Exception as e:
            print(f"⚠️  Ошибка при проверке состояния игры: {e}")
        return False

    def _find_king_position(self, board_state: List[List[Optional[str]]], is_white: bool) -> Optional[Tuple[int, int]]:
        """Найти позицию короля на доске."""
        cache_key = (str(board_state), is_white)
        current_time = time.time()
        cache_duration = 3.0
        
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
        
        if not hasattr(self, '_king_pos_cache'):
            self._king_pos_cache = {}
            self._king_pos_cache_time = {}
        self._king_pos_cache[cache_key] = king_pos
        self._king_pos_cache_time[cache_key] = current_time
        
        return king_pos

    def draw_ui(self):
        """Отрисовка пользовательского интерфейса."""
        try:
            info_rect = pygame.Rect(0, BOARD_SIZE, BOARD_SIZE, 100)
            pygame.draw.rect(self.screen, (50, 50, 50), info_rect)
            pygame.draw.line(self.screen, (100, 100, 100), (0, BOARD_SIZE), 
                           (BOARD_SIZE, BOARD_SIZE), 2)
            
            if self.game_over:
                if self.game_over_reason:
                    text = self.ui_font.render(self.game_over_reason, True, (255, 100, 100))
                    self.screen.blit(text, (20, BOARD_SIZE + 15))
                restart_text = self.ui_font.render("Нажмите 'R' для новой игры", 
                                                   True, (200, 200, 200))
                self.screen.blit(restart_text, (20, BOARD_SIZE + 50))
                
                if 'duration' in self.game_stats:
                    duration_text = self.ui_font_small.render(
                        f"Время игры: {int(self.game_stats['duration'])} сек", 
                        True, (150, 150, 150))
                    self.screen.blit(duration_text, (BOARD_SIZE - 150, BOARD_SIZE + 35))
            else:
                if self._is_player_turn():
                    status = "🎮 Ваш ход"
                    status_color = (100, 255, 100)
                else:
                    status = "🤖 Ход компьютера"
                    status_color = (100, 150, 255)
                
                text = self.ui_font.render(status, True, status_color)
                self.screen.blit(text, (20, BOARD_SIZE + 15))
                
                moves_text = self.ui_font.render(
                    f"Ходов: {len(self.move_history)} | ♟️ {self.game_stats['player_capture_count']} vs {self.game_stats['ai_capture_count']} ♟️", 
                    True, (200, 200, 200))
                self.screen.blit(moves_text, (20, BOARD_SIZE + 50))
                
                level_text = self.ui_font.render(f"Уровень: {self.skill_level}/20", 
                                                True, (200, 200, 200))
                self.screen.blit(level_text, (BOARD_SIZE - 150, BOARD_SIZE + 15))
                
                hint_text = self.ui_font_small.render(
                    "Подсказка: Кликните по фигуре для показа возможных ходов | Нажмите 'T' для совета", 
                    True, (150, 150, 150))
                self.screen.blit(hint_text, (20, BOARD_SIZE + 75))
                
                if self.move_feedback and time.time() - self.move_feedback_time < 3:
                    feedback_color = (255, 255, 100)
                    feedback_text = self.ui_font.render(self.move_feedback, True, feedback_color)
                    self.screen.blit(feedback_text, 
                                   (BOARD_SIZE // 2 - feedback_text.get_width() // 2, 
                                    BOARD_SIZE + 30))
        except Exception as e:
            print(f"⚠️  Ошибка при отрисовке интерфейса: {e}")

    def get_game_stats(self) -> dict:
        """Получить статистику текущей игры."""
        try:
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

    def handle_ai_move_multithreaded(self):
        """Обработка хода ИИ с использованием многопоточности."""
        if self._is_player_turn() or self.game_over or self.thinking:
            return
        
        current_time = time.time()
        if current_time - self.last_ai_move_time < self.ai_move_cooldown:
            return
        
        if current_time - self.last_move_time < self.ai_move_delay:
            return
        
        self.thinking = True
        self.last_ai_move_time = current_time
        
        move_start_time = time.time()
        
        try:
            self._clear_old_ai_cache()
            
            depth = max(1, min(10, self.skill_level // 2 + 1))
            
            ai_move = None
            
            if self.skill_level < 12:
                ai_move = self._get_cached_best_move(depth=1)
            
            if not ai_move:
                fast_depth = max(1, min(6, self.skill_level // 3 + 1))
                ai_move = self._get_cached_best_move(depth=fast_depth)
            
            if not ai_move:
                ai_move = self._get_cached_best_move(depth=1)
            
            if ai_move:
                print(f"Ход компьютера: {ai_move}")
                
                board_before = self.engine.get_board_state()
                
                if self.engine.is_move_correct(ai_move):
                    if self.engine.make_move(ai_move):
                        self.opening_book.add_move(ai_move)
                        current_opening = self.opening_book.get_current_opening()
                        
                        self.move_history.append(ai_move)
                        self.game_stats['ai_moves'] += 1
                        
                        board_after = self.engine.get_board_state()
                        to_col = ord(ai_move[2]) - ord('a')
                        to_row = 8 - int(ai_move[3])
                        target_piece = board_before[to_row][to_col]
                        is_capture = target_piece is not None
                        is_check = False
                        is_mate = False
                        is_castling = ai_move in ['e1g1', 'e1c1', 'e8g8', 'e8c8']
                        
                        is_over, reason = self.engine.is_game_over()
                        if is_over and reason and "мат" in reason:
                            is_mate = True
                        
                        try:
                            eval_result = self.engine.get_evaluation()
                            if eval_result and isinstance(eval_result, dict):
                                is_check = eval_result.get('check', False)
                        except:
                            pass
                        
                        annotated_move = self._annotate_move(ai_move, is_capture, is_check, is_mate, is_castling)
                        
                        if is_capture:
                            self.game_stats['ai_capture_count'] += 1
                            self.move_feedback = f"Ход компьютера: {annotated_move} (взятие!)"
                            if self.sound_manager:
                                self.sound_manager.play_sound("capture")
                        else:
                            self.move_feedback = f"Ход компьютера: {annotated_move}"
                            if self.sound_manager:
                                self.sound_manager.play_sound("move")
                        
                        if current_opening:
                            opening_name, opening_info = current_opening
                            self.move_feedback += f" | 🎯 Дебют: {opening_name}"
                        
                        from_col = ord(ai_move[0]) - ord('a')
                        from_row = 8 - int(ai_move[1])
                        to_col = ord(ai_move[2]) - ord('a')
                        to_row = 8 - int(ai_move[3])
                        self.renderer.set_last_move((from_row, from_col), (to_row, to_col))
                        self.last_move_time = current_time
                        print(f"Ход компьютера выполнен: {annotated_move}")
                        self.move_feedback_time = current_time
                        
                        move_time = time.time() - move_start_time
                        self.game_stats['move_times'].append(move_time)
                        
                        evaluation = self.get_cached_evaluation()
                        if evaluation is not None:
                            self.game_stats['evaluations'].append(evaluation)
                        
                        educational_tip = self.educator.get_educational_feedback(
                            len(self.move_history), current_time)
                        if educational_tip:
                            self.move_feedback += f" | {educational_tip}"
                            self.move_feedback_time = current_time
                            
                        self.board_state_cache = None
                        
                        self.renderer._mark_all_dirty()
                    else:
                        print("⚠️  Не удалось выполнить ход компьютера")
                        self.move_feedback = "Не удалось выполнить ход компьютера"
                        self.move_feedback_time = current_time
                        if self.sound_manager:
                            self.sound_manager.play_sound("button")
                else:
                    print("⚠️  Компьютер предложил некорректный ход")
                    self.move_feedback = "Компьютер предложил некорректный ход"
                    self.move_feedback_time = current_time
                    if self.sound_manager:
                        self.sound_manager.play_sound("button")
            else:
                print("⚠️  Компьютер не смог найти ход")
                self.move_feedback = "Компьютер не смог найти ход"
                self.move_feedback_time = time.time()
                if self.sound_manager:
                    self.sound_manager.play_sound("button")
        except Exception as e:
            print(f"⚠️  Ошибка при получении хода компьютера: {e}")
            self.move_feedback = "Ошибка при получении хода компьютера"
            self.move_feedback_time = time.time()
            if self.sound_manager:
                self.sound_manager.play_sound("button")
        finally:
            self.thinking = False

    def _get_move_hint(self, from_row: int, from_col: int, to_row: int, to_col: int) -> str:
        """Получить подсказку о причине недопустимости хода."""
        try:
            if not hasattr(self, '_cached_board'):
                self._cached_board = self.engine.get_board_state()
            board = self._cached_board
            
            piece = board[from_row][from_col]
            
            if not piece:
                return "Нет фигуры на этой клетке"
            
            if not hasattr(self, '_piece_name_cache'):
                self._piece_name_cache = {
                    'P': 'белая пешка', 'N': 'белый конь', 'B': 'белый слон', 
                    'R': 'белая ладья', 'Q': 'белый ферзь', 'K': 'белый король',
                    'p': 'чёрная пешка', 'n': 'чёрный конь', 'b': 'чёрный слон', 
                    'r': 'чёрная ладья', 'q': 'чёрный ферзь', 'k': 'чёрный король'
                }
            piece_name = self._piece_name_cache.get(piece, piece)
            
            if not hasattr(self, '_piece_hint_cache'):
                self._piece_hint_cache = {}
            if piece not in self._piece_hint_cache:
                self._piece_hint_cache[piece] = self.educator.get_piece_hint(piece_name)
            
            piece_lower = piece.lower()
            if piece_lower == 'p':
                if abs(from_row - to_row) == 2:
                    is_white = piece.isupper()
                    is_starting_position = (is_white and from_row == 6) or (not is_white and from_row == 1)
                    
                    if not is_starting_position:
                        return f"{piece_name} может двигаться на две клетки только со стартовой позиции"
                
                is_white = piece.isupper()
                moving_forward = (is_white and to_row < from_row) or (not is_white and to_row > from_row)
                
                if not moving_forward:
                    return f"{piece_name} может двигаться только вперёд"
                
                if from_col == to_col and board[to_row][to_col] is not None:
                    return f"{piece_name} не может взять фигуру, двигаясь вперёд. Пешки берут по диагонали!"
                
                if from_col != to_col and board[to_row][to_col] is None:
                    return f"{piece_name} может двигаться по диагонали только для взятия фигуры"
            
            elif piece_lower == 'n':
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if not ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)):
                    return f"{piece_name} ходит буквой Г (две клетки в одном направлении и одна в перпендикулярном)"
            
            elif piece_lower == 'b':
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if row_diff != col_diff:
                    return f"{piece_name} ходит только по диагонали"
                
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece_lower == 'r':
                if from_row != to_row and from_col != to_col:
                    return f"{piece_name} ходит только по горизонтали или вертикали"
                
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece_lower == 'q':
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                
                if not ((from_row == to_row) or (from_col == to_col) or (row_diff == col_diff)):
                    return f"{piece_name} ходит по горизонтали, вертикали или диагонали"
                
                if self._is_path_blocked(from_row, from_col, to_row, to_col, board):
                    return f"Путь для {piece_name} заблокирован другой фигурой"
            
            elif piece_lower == 'k':
                row_diff = abs(from_row - to_row)
                col_diff = abs(from_col - to_col)
                if row_diff > 1 or col_diff > 1:
                    return f"{piece_name} ходит только на одну клетку в любом направлении"
                
                if row_diff == 0 and col_diff == 2:
                    return f"Рокировка возможна только из начальной позиции и при определённых условиях"
            
            target_piece = board[to_row][to_col]
            if target_piece and ((piece.isupper() and target_piece.isupper()) or 
                               (piece.islower() and target_piece.islower())):
                return f"{piece_name} не может взять свою же фигуру"
            
            return f"Недопустимый ход для {piece_name}"
        except Exception as e:
            print(f"Ошибка при получении подсказки: {e}")
            return "Недопустимый ход"

    def _is_path_blocked(self, from_row: int, from_col: int, to_row: int, to_col: int, board: List[List[Optional[str]]]) -> bool:
        """Проверить, заблокирован ли путь между двумя клетками."""
        row_step = 0 if from_row == to_row else (1 if to_row > from_row else -1)
        col_step = 0 if from_col == to_col else (1 if to_col > from_col else -1)
        
        current_row, current_col = from_row + row_step, from_col + col_step
        while current_row != to_row or current_col != to_col:
            if board[current_row][current_col] is not None:
                return True
            current_row += row_step
            current_col += col_step
        
        return False