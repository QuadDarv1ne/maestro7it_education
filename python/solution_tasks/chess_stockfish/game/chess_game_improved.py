# ============================================================================
# game/chess_game_improved.py
# ============================================================================

"""
Модуль: game/chess_game_improved.py

Описание:
    Улучшенная версия главного класса ChessGame с оптимизированным управлением кэшем,
    устранением дублирования кода и улучшенной производительностью.
"""

import pygame
from typing import Optional, Tuple, List
import time
import sys
import random
import concurrent.futures
import threading
from queue import Queue, Empty

# Import our game modules
from engine.stockfish_wrapper import StockfishWrapper
from ui.board_renderer import BoardRenderer
from utils.educational import ChessEducator
from utils.opening_book import OpeningBook
from utils.sound_manager import SoundManager
from game.in_game_menu import InGameMenu
from utils.performance_monitor import get_performance_monitor, PerformanceTimer

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

class LRUCache:
    """
    Простая реализация LRU кэша для предотвращения утечек памяти.
    """
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self.cache = {}
        self.access_order = []
    
    def get(self, key):
        if key in self.cache:
            # Перемещаем ключ в конец (последний использованный)
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            # Обновляем значение и перемещаем в конец
            self.cache[key] = value
            self.access_order.remove(key)
            self.access_order.append(key)
        else:
            # Добавляем новую запись
            self.cache[key] = value
            self.access_order.append(key)
            
            # Если превышен размер, удаляем наименее используемый элемент
            if len(self.cache) > self.max_size:
                oldest_key = self.access_order.pop(0)
                del self.cache[oldest_key]
    
    def clear(self):
        self.cache.clear()
        self.access_order.clear()

class ChessGame:
    """
    Главный класс для управления ходом игры с улучшенной производительностью.
    
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
        # Инициализируем монитор производительности
        self.performance_monitor = get_performance_monitor()
        self.performance_monitor.start_monitoring(0.5)  # Мониторим каждые 0.5 секунды
        
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
        self.ai_move_delay = 0.05  # Уменьшена задержка перед ходом ИИ для более быстрой игры
        self.move_feedback = ""  # Feedback message for the player
        self.move_feedback_time = 0
        self.frame_count = 0  # Счетчик кадров для очистки временных поверхностей
        self.highlight_hint = None  # For T key hint highlighting
        
        # Улучшенная система кэширования с LRU
        self._board_state_cache = LRUCache(max_size=50)
        self._valid_moves_cache = LRUCache(max_size=100)
        self._ai_move_cache = LRUCache(max_size=50)
        self._evaluation_cache = LRUCache(max_size=30)
        
        # Графические оптимизации
        self.last_board_hash = None
        self.dirty_squares = set()
        self.piece_surfaces = {}
        self.highlight_surfaces = {}
        
        # Таймеры для оптимизации обновлений
        self.last_board_update = 0
        self.last_ui_update = 0
        self.board_update_interval = 1.0/60  # Снижаем частоту обновления доски до 60 FPS для экономии ресурсов
        self.ui_update_interval = 1.0/30     # Снижаем частоту обновления UI до 30 FPS для экономии ресурсов
        
        # Инициализация графических ресурсов
        self._init_fonts_optimized()
        self._init_piece_surfaces()
        self._init_highlight_surfaces()
        
        # Оптимизация AI
        self.ai_move_cache = {}  # Кэш для AI ходов
        self.last_ai_move_time = 0
        self.ai_move_cooldown = 0.01  # Минимальная задержка между AI ходами
        
        # Дополнительные оптимизации
        self.board_state_cache = None  # Кэш состояния доски для быстрого доступа
        self.board_state_cache_time = 0
        self.board_state_cache_duration = 0.5  # Уменьшаем кэш до 0.5 секунды для лучшей производительности
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
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)  # Уменьшаем количество потоков для лучшей производительности
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
        self._async_eval_interval = 0.2  # Обновляем оценку раз в 200 мс
        
        # Прогрессивная оценка позиции для плавного обновления
        self._displayed_evaluation = 0.0  # Текущее отображаемое значение
        self._target_evaluation = 0.0     # Целевое значение оценки
        self._eval_update_time = 0        # Время последнего обновления
        self._eval_interpolation_duration = 0.2  # Длительность интерполяции в секундах

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

    def get_cached_evaluation(self):
        """
        Получение кэшированной оценки позиции с улучшенным кэшированием.
        
        Возвращает:
            float: Оценка позиции
        """
        try:
            current_fen = self.engine.get_fen()
            current_time = time.time()
            
            # Проверяем кэш
            cached_eval = self._evaluation_cache.get(current_fen)
            if cached_eval is not None:
                eval_value, cache_time = cached_eval
                # Используем кэш до 120 секунд
                if (current_time - cache_time) < 120.0:
                    return eval_value
                
            evaluation = self.engine.get_evaluation()
            # Сохраняем в кэш
            self._evaluation_cache.put(current_fen, (evaluation, current_time))
            return evaluation
        except Exception:
            # Возвращаем кэшированное значение даже при ошибке
            current_fen = self.engine.get_fen()
            cached_eval = self._evaluation_cache.get(current_fen)
            if cached_eval is not None:
                return cached_eval[0]
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
                # Линейная интерполяция с ускорением для более плавного обновления
                progress = elapsed / self._eval_interpolation_duration
                # Используем квадратичную функцию для более плавного обновления
                progress = progress * progress * (3 - 2 * progress)
                self._displayed_evaluation = (
                    self._displayed_evaluation + 
                    (self._target_evaluation - self._displayed_evaluation) * progress
                )
        
        return self._displayed_evaluation

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
        
        # Проверяем кэш
        cached_moves = self._valid_moves_cache.get(cache_key)
        if cached_moves is not None:
            cached_list, cache_time, cached_board_hash = cached_moves
            # Используем кэш если:
            # 1. Время кэша еще не истекло (10 секунд)
            # 2. Позиция на доске не изменилась
            # 3. Или время кэша очень свежее (меньше 0.2 секунды)
            is_time_valid = (current_time - cache_time < 10.0)
            is_position_valid = (cached_board_hash == board_hash)
            is_fresh_cache = (current_time - cache_time < 0.2)
            
            if is_time_valid and (is_position_valid or is_fresh_cache):
                return cached_list[:]  # Возвращаем копию, чтобы избежать модификации кэша
        
        valid_moves = []
        from_uci = self._fen_square_to_uci(from_row, from_col)
        
        try:
            # Используем кэшированное состояние доски для повышения производительности
            piece = board_state[from_row][from_col]
            if not piece:
                # Сохраняем в кэш даже пустой результат
                self._valid_moves_cache.put(cache_key, (valid_moves, current_time, board_hash))
                return valid_moves
                
            # Получаем все возможные ходы через движок (оригинальный метод)
            for to_row in range(8):
                for to_col in range(8):
                    to_uci = self._fen_square_to_uci(to_row, to_col)
                    uci_move = from_uci + to_uci
                    if self.engine.is_move_correct(uci_move):
                        valid_moves.append((to_row, to_col))
                    
        except Exception as e:
            print(f"Ошибка при расчете допустимых ходов: {e}")
        
        # Сохраняем результат в кэш
        self._valid_moves_cache.put(cache_key, (valid_moves[:], current_time, board_hash))
        return valid_moves

    def get_board_state(self) -> List[List[Optional[str]]]:
        """
        Получение состояния доски с кэшированием.
        
        Возвращает:
            List[List[Optional[str]]]: Состояние доски
        """
        try:
            current_time = time.time()
            current_fen = self.engine.get_fen()
            
            # Проверяем кэш
            cached_state = self._board_state_cache.get(current_fen)
            if cached_state is not None:
                board, cache_time = cached_state
                # Используем кэш если:
                # 1. Время кэша еще не истекло (2 секунды)
                # 2. Позиция на доске не изменилась
                # 3. Или время кэша очень свежее (меньше 0.2 секунды)
                is_time_valid = (current_time - cache_time < 2.0)
                is_position_same = (self.board_state_last_fen == current_fen)
                is_fresh_cache = (current_time - cache_time < 0.2)
                
                if is_time_valid and (is_position_same or is_fresh_cache):
                    return board
            
            # Получаем новое состояние доски
            board = self.engine.get_board_state()
            
            # Обновляем кэш
            self._board_state_cache.put(current_fen, (board, current_time))
            self.board_state_last_fen = current_fen
            
            return board
        except Exception:
            # Возвращаем пустую доску в случае ошибки
            empty_board: List[List[Optional[str]]] = [[None for _ in range(8)] for _ in range(8)]
            self._board_state_cache.put("error_state", (empty_board, time.time()))
            self.board_state_last_fen = None
            return empty_board

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
        # Очищаем все LRU кэши
        self._board_state_cache.clear()
        self._valid_moves_cache.clear()
        self._ai_move_cache.clear()
        self._evaluation_cache.clear()
        
        # Очищаем другие кэши
        if hasattr(self, '_uci_cache'):
            self._uci_cache.clear()
        if hasattr(self, '_cached_board'):
            delattr(self, '_cached_board')
        if hasattr(self, '_piece_name_cache'):
            self._piece_name_cache.clear()
        if hasattr(self, '_piece_hint_cache'):
            self._piece_hint_cache.clear()
        if hasattr(self, '_king_pos_cache'):
            self._king_pos_cache.clear()
        if hasattr(self, '_king_pos_cache_time'):
            self._king_pos_cache_time.clear()
        if hasattr(self, '_edu_feedback_cache'):
            self._edu_feedback_cache.clear()
        if hasattr(self, '_edu_feedback_cache_time'):
            self._edu_feedback_cache_time.clear()

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
        
        # Очищаем все кэши
        self._clear_caches()

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

# ============================================================================ #
# Конец файла
# ============================================================================ #
