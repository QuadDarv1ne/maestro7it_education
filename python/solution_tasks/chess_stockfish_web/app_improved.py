# app_improved.py
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, disconnect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from stockfish import Stockfish
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
import sys
import time

# Глобальные переменные
active_game_count = 0
games = {}
stockfish_engine = None
game_histories = {}
session_timestamps = {}
user_preferences = {}
resource_stats = {
    'peak_active_games': 0,
    'peak_sessions': 0,
    'total_games_cleaned': 0
}
import logging
import json
import threading
import weakref
import pickle
import base64
import functools
import re
from collections import defaultdict, OrderedDict
from contextlib import contextmanager
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Импорт моделей базы данных
try:
    from models import (
        db, init_db, User, Game, Puzzle, create_user,
        get_recent_games_optimized, get_games_by_result
    )
    DATABASE_ENABLED = True
except ImportError as e:
    print(f"Database models import failed: {e}")
    DATABASE_ENABLED = False
    db = None
    init_db = None
    User = None
    Game = None
    Puzzle = None
    create_user = None
    get_recent_games_optimized = None
    get_games_by_result = None

# Импорт отслеживания производительности
try:
    from utils.performance_tracker import performance_tracker, track_engine_init, track_move_validation, track_move_execution, track_ai_calculation, track_game_status_check, track_fen_retrieval
    PERFORMANCE_TRACKING_ENABLED = True
except ImportError:
    # Резервный вариант, если модуль utils недоступен
    PERFORMANCE_TRACKING_ENABLED = False
    performance_tracker = None
    def track_engine_init(func): return func
    def track_move_validation(func): return func
    def track_move_execution(func): return func
    def track_ai_calculation(func): return func
    def track_game_status_check(func): return func
    def track_fen_retrieval(func): return func

# Импорт менеджера кэша
try:
    from utils.cache_manager import cache_manager, cached
    CACHE_MANAGER_ENABLED = True
except ImportError:
    # Резервный вариант, если менеджер кэша недоступен
    CACHE_MANAGER_ENABLED = False
    cache_manager = None
    def cached(cache_type='generic'): 
        def decorator(func):
            return func
        return decorator

# Импорт обработчика ошибок
try:
    from utils.error_handler import error_handler, handle_chess_errors, retry_on_failure
    # Импорт классов исключений
    from utils.error_handler import EngineInitializationError, MoveValidationError, GameLogicError
    ERROR_HANDLER_ENABLED = True
except ImportError:
    # Резервный вариант, если обработчик ошибок недоступен
    ERROR_HANDLER_ENABLED = False
    error_handler = None
    def handle_chess_errors(context=""): 
        def decorator(func):
            return func
        return decorator
    def retry_on_failure(max_attempts=3, delay=1.0, backoff=2.0):
        def decorator(func):
            return func
        return decorator
    # Определение локальных классов исключений
    class EngineInitializationError(Exception):
        pass
    class MoveValidationError(Exception):
        pass
    class GameLogicError(Exception):
        pass

# Вспомогательная функция для поиска исполняемого файла Stockfish
def _find_stockfish_executable():
    """Поиск исполняемого файла Stockfish в различных возможных местах"""
    import shutil
    executable_names = [
        'stockfish.exe',    # Windows
        'stockfish',        # Linux/Mac
        'stockfish_15_x64.exe',
        'stockfish_14_x64.exe',
        'stockfish_13_x64.exe',
        'stockfish-windows-x86-64.exe',
        'stockfish-linux-x64',
        'stockfish-mac-x64'
    ]
    
    search_paths = [
        os.path.dirname(__file__),
        os.path.join(os.path.dirname(__file__), '..'),
        os.path.join(os.path.dirname(__file__), 'engines'),
        os.path.expanduser('~'),
        os.path.expanduser('~/stockfish'),
        '/usr/local/bin',
        '/usr/bin',
        'C:\\Program Files\\Stockfish',
        'C:\\Program Files (x86)\\Stockfish',
        'C:\\Program Files\\stockfish'  # Additional path where Stockfish was found
    ]
    
    # Проверка переменной окружения
    env_path = os.getenv('STOCKFISH_PATH')
    if env_path:
        search_paths.insert(0, env_path)
    
    # Проверка конкретного пути к Stockfish, который точно существует
    specific_stockfish_path = 'C:\\Program Files\\stockfish\\stockfish-windows-x86-64.exe'
    if os.path.exists(specific_stockfish_path):
        return specific_stockfish_path
    
    # Попытка найти исполняемый файл
    for search_path in search_paths:
        if search_path and os.path.exists(search_path):
            # Сначала проверка прямого пути
            if os.path.isfile(search_path) and any(search_path.endswith(ext) for ext in ['.exe', '']):
                return search_path
            
            # Проверка в директории
            for exe_name in executable_names:
                full_path = os.path.join(search_path, exe_name)
                if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                    return full_path
    
    # Проверка системного PATH
    for exe_name in executable_names:
        try:
            path = shutil.which(exe_name)
            if path:
                return path
        except:
            pass
    
    return None

# Импорт пула соединений
try:
    from utils.connection_pool import stockfish_pool
    CONNECTION_POOLING_ENABLED = True
    # Импорт функции контекстного менеджера
    from utils.connection_pool import get_stockfish_engine as pool_get_stockfish_engine
except ImportError:
    # Резервный вариант, если пул соединений недоступен
    CONNECTION_POOLING_ENABLED = False
    stockfish_pool = None
    def pool_get_stockfish_engine(skill_level=5):
        # Простой контекстный менеджер, который создает новый движок каждый раз
        @contextmanager
        def engine_context_manager():
            # Создание нового движка
            engine_path = _find_stockfish_executable()
            if not engine_path:
                raise EngineInitializationError("Stockfish executable not found")
            
            engine = Stockfish(path=engine_path)
            engine.set_skill_level(skill_level)
            engine.set_depth(10)
            engine.update_engine_parameters({
                'Threads': 2,
                'Hash': 128,
                'Contempt': 0,
                'Ponder': False
            })
            try:
                yield engine
            finally:
                # Очистка движка
                try:
                    # Stockfish не имеет методов quit() или close(), просто позволяем сборщику мусора удалить его
                    pass
                except:
                    pass
        return engine_context_manager()

# Настройка логирования с улучшенным форматированием и ротацией
def setup_logging():
    """Настройка системы логирования с ротацией файлов и расширенным форматированием"""
    try:
        from logging.handlers import RotatingFileHandler
        import os
        
        # Создаем директорию для логов если её нет
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Основной обработчик с ротацией (10 файлов по 10MB)
        main_handler = RotatingFileHandler(
            os.path.join(log_dir, 'chess_app.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        
        # Обработчик для критических ошибок
        error_handler = RotatingFileHandler(
            os.path.join(log_dir, 'chess_app_errors.log'),
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        
        # Расширенное форматирование
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - [%(levelname)s] - %(process)d:%(thread)d - '
            '%(filename)s:%(lineno)d - %(funcName)s - %(message)s'
        )
        
        main_handler.setFormatter(formatter)
        error_handler.setFormatter(formatter)
        
        # Настройка корневого логгера
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        # Очистка существующих обработчиков
        root_logger.handlers.clear()
        
        # Добавление обработчиков
        root_logger.addHandler(main_handler)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(logging.StreamHandler(sys.stdout))
        
        # Отдельный логгер для отслеживания производительности
        perf_handler = RotatingFileHandler(
            os.path.join(log_dir, 'performance.log'),
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        perf_handler.setFormatter(formatter)
        perf_logger = logging.getLogger('performance')
        perf_logger.addHandler(perf_handler)
        perf_logger.setLevel(logging.INFO)
        
        logging.info("Logging system initialized successfully")
    except Exception as e:
        print(f"Failed to initialize logging system: {e}")
        # Fallback to basic logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )

# Инициализация системы логирования
setup_logging()
logger = logging.getLogger(__name__)

from utils.app_state import app_state

# Максимальное количество одновременных игр для предотвращения перегрузки сервера
MAX_CONCURRENT_GAMES = 20  # Увеличено с 10 до 20

# Пул потоков для фоновых задач (расчет ходов AI)
# Используется небольшой пул, чтобы не перегружать систему
AI_MOVE_THREAD_POOL = ThreadPoolExecutor(max_workers=4, thread_name_prefix="ai_move")

# Интервал очистки в секундах
CLEANUP_INTERVAL = 300  # 5 минут

# Таймаут неактивности игры в секундах
GAME_TIMEOUT = 3600  # 1 час

# Таймаут инициализации игры
GAME_INIT_TIMEOUT = 30  # 30 секунд для инициализации игры

def cleanup_stale_games():
    """Периодическая очистка устаревших игровых сессий для предотвращения утечек памяти."""
    while True:
        try:
            time.sleep(CLEANUP_INTERVAL)
            # Получение устаревших сессий через AppState
            stale_sessions = app_state.get_stale_sessions(GAME_TIMEOUT)
            
            # Очистка устаревших сессий
            cleanup_count = 0
            for session_id in stale_sessions:
                try:
                    if session_id in games:
                        # Очистка ресурсов игры
                        try:
                            game = games[session_id]
                            # Правильная очистка игрового движка
                            if hasattr(game, 'engine') and game.engine:
                                if CONNECTION_POOLING_ENABLED and hasattr(game, '_engine_context') and game._engine_context:
                                    try:
                                        game._engine_context.__exit__(None, None, None)
                                    except Exception as pool_error:
                                        logger.warning(f"Error returning engine to pool for session {session_id}: {pool_error}")
                                else:
                                    # Для непулованных движков просто удаляем ссылку
                                    game.engine = None
                            
                            del games[session_id]
                            active_game_count = max(0, active_game_count - 1)
                            resource_stats['total_games_cleaned'] += 1
                            cleanup_count += 1
                            logger.info(f"Cleaned up stale game for session: {session_id}")
                        except Exception as e:
                            logger.error(f"Error cleaning up stale game for session {session_id}: {e}")
                except Exception as e:
                    logger.error(f"Error processing session {session_id}: {e}")
                
                # Удаление временной метки
                try:
                    if session_id in session_timestamps:
                        del session_timestamps[session_id]
                except Exception as e:
                    logger.error(f"Error removing timestamp for session {session_id}: {e}")
                
                # Удаление пользовательских настроек
                try:
                    if session_id in user_preferences:
                        del user_preferences[session_id]
                except Exception as e:
                    logger.warning(f"Error removing user preferences for session {session_id}: {e}")
                
                # Удаление истории игры
                try:
                    if session_id in game_histories:
                        del game_histories[session_id]
                except Exception as e:
                    logger.warning(f"Error removing game history for session {session_id}: {e}")
            
            # Очистка устаревших записей кэша
            if CACHE_MANAGER_ENABLED:
                # Менеджер кэша автоматически обрабатывает истечение TTL
                pass
            
            # Обновление статистики ресурсов
            resource_stats['peak_active_games'] = max(resource_stats['peak_active_games'], active_game_count)
            resource_stats['peak_sessions'] = max(resource_stats['peak_sessions'], len(session_timestamps))
            
            logger.info(f"Cleanup completed. Active games: {active_game_count}, Tracked sessions: {len(session_timestamps)}, Cleaned up: {cleanup_count}")
            logger.info(f"Resource stats: {resource_stats}")
        except Exception as e:
            logger.error(f"Error in cleanup thread: {e}")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'maestro7it-chess-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///chess.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация ограничителя частоты запросов
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Инициализация базы данных, если включена
if DATABASE_ENABLED and init_db:
    db = init_db(app)

socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=30, ping_interval=25)

# Запуск потока очистки после определения всех переменных для предотвращения гонок

class ChessGame:
    def __init__(self, player_color='white', skill_level=5):
        self.player_color = player_color
        self.skill_level = skill_level
        self.engine = None
        self.initialized = False
        self.engine_path = None
        self._engine_context = None
        self.last_move = None  # Отслеживание последнего сделанного хода
        self.move_history = []  # Отслеживание истории ходов для функции отмены
        self._fen_cache = None  # Кэш FEN позиции
        self._fen_cache_timestamp = 0
        self._fen_cache_ttl = 0.5  # Кэш FEN позиций на 500мс
    
    def _is_engine_compatible(self, engine, skill_level):
        """
        Проверка, можно ли переиспользовать существующий движок с запрошенным уровнем сложности.
        Для простоты предполагаем совместимость и просто обновляем уровень сложности.
        """
        try:
            engine.set_skill_level(skill_level)
            return True
        except:
            return False
    
    def _calculate_engine_parameters(self, skill_level):
        """
        Расчет оптимальных параметров движка на основе уровня сложности.
        
        Args:
            skill_level: Уровень сложности (0-20)
            
        Returns:
            Словарь с параметрами движка
        """
        # Настройка параметров в зависимости от уровня сложности для баланса производительности/точности
        if skill_level <= 5:
            # Начальный уровень - быстрее, но менее точно
            depth = 5
            threads = 1
            hash_size = 64
        elif skill_level <= 10:
            # Средний уровень - сбалансировано
            depth = 8
            threads = 2
            hash_size = 128
        elif skill_level <= 15:
            # Продвинутый уровень - более точно
            depth = 12
            threads = 2
            hash_size = 256
        else:
            # Экспертный уровень - максимальная точность
            depth = 15
            threads = 4
            hash_size = 512
        
        return {
            'Threads': threads,
            'Hash': hash_size,
            'Contempt': 0,
            'Ponder': False,
            'Slow Mover': 100,
            'Move Overhead': 10,
            'Skill Level': skill_level,
            'Depth': depth
        }
    
    def _find_stockfish_executable(self):
        """Поиск исполняемого файла Stockfish в различных возможных местах с улучшенным обнаружением"""
        # Общие имена исполняемых файлов для разных платформ
        executable_names = [
            'stockfish.exe',    # Windows
            'stockfish',        # Linux/Mac
            'stockfish_15_x64.exe',  # Конкретные версии
            'stockfish_14_x64.exe',
            'stockfish_13_x64.exe',
            'stockfish-windows-x86-64.exe',
            'stockfish-linux-x64',
            'stockfish-mac-x64'
        ]
        
        # Общие пути поиска
        search_paths = [
            os.path.dirname(__file__),  # Текущая директория
            os.path.join(os.path.dirname(__file__), '..'),  # Родительская директория
            os.path.join(os.path.dirname(__file__), 'engines'),  # Поддиректория engines
            os.path.join(os.path.dirname(__file__), '..', 'engines'),  # Engines в родительской директории
            os.path.expanduser('~'),  # Домашняя директория
            os.path.expanduser('~/stockfish'),  # Stockfish в домашней директории
            '/usr/local/bin',  # Общие пути Unix
            '/usr/bin',
            'C:\\Program Files\\Stockfish',
            'C:\\Program Files (x86)\\Stockfish',
            'C:\\Program Files\\stockfish'  # Дополнительный путь, где был найден Stockfish
        ]
        
        # Проверка переменной окружения
        env_path = os.getenv('STOCKFISH_PATH')
        if env_path:
            search_paths.insert(0, env_path)
            logger.info(f"Using STOCKFISH_PATH environment variable: {env_path}")
        
        # Проверка конкретного пути к Stockfish, который точно существует
        specific_stockfish_path = 'C:\\Program Files\\stockfish\\stockfish-windows-x86-64.exe'
        if os.path.exists(specific_stockfish_path):
            logger.info(f"Found Stockfish executable at specific path: {specific_stockfish_path}")
            return specific_stockfish_path
        
        # Попытка найти исполняемый файл in search paths
        import shutil
        found_paths = []
        for search_path in search_paths:
            if search_path and os.path.exists(search_path):
                # Сначала проверка прямого пути
                if os.path.isfile(search_path) and any(search_path.endswith(ext) for ext in ['.exe', '']):
                    logger.info(f"Found Stockfish executable at direct path: {search_path}")
                    found_paths.append(search_path)
                
                # Проверка в директории
                for exe_name in executable_names:
                    full_path = os.path.join(search_path, exe_name)
                    if os.path.exists(full_path) and os.access(full_path, os.X_OK):
                        logger.info(f"Found Stockfish executable at: {full_path}")
                        found_paths.append(full_path)
        
        # Проверка системного PATH
        for exe_name in executable_names:
            try:
                path = shutil.which(exe_name)
                if path:
                    logger.info(f"Found Stockfish executable in PATH: {path}")
                    found_paths.append(path)
            except Exception as e:
                logger.warning(f"Error checking PATH for {exe_name}: {e}")
                continue
        
        # Возврат первого найденного пути или None, если ничего не найдено
        if found_paths:
            selected_path = found_paths[0]
            logger.info(f"Selected Stockfish executable: {selected_path}")
            return selected_path
        
        logger.error("Stockfish executable not found in any expected location")
        logger.error(f"Search paths checked: {search_paths}")
        return None
    
    @retry_on_failure(max_attempts=3, delay=1.0, backoff=2.0)
    @track_engine_init
    @handle_chess_errors(context="engine_initialization")
    def init_engine(self):
        global stockfish_engine
        start_time = time.time()
        try:
            logger.info(f"Starting engine initialization for skill level {self.skill_level}")
            
            # Использование пула соединений, если доступен
            if CONNECTION_POOLING_ENABLED and stockfish_pool:
                logger.info("Using connection pooling for Stockfish engine")
                # Получение движка из пула с использованием контекстного менеджера
                self._engine_context = pool_get_stockfish_engine(self.skill_level)
                # Правильное использование контекстного менеджера
                self.engine = self._engine_context.__enter__()
                self.initialized = True
                init_duration = time.time() - start_time
                logger.info(f"Got Stockfish engine from pool with skill level {self.skill_level} in {init_duration:.2f} seconds")
                return True
            
            # Переиспользование существующего движка, если доступен и правильно настроен
            if stockfish_engine and self._is_engine_compatible(stockfish_engine, self.skill_level):
                logger.info(f"Reusing existing Stockfish engine with skill level {self.skill_level}")
                self.engine = stockfish_engine
                # Настройка движка с оптимизированными параметрами на основе уровня сложности
                engine_params = self._calculate_engine_parameters(self.skill_level)
                self.engine.set_skill_level(self.skill_level)
                self.engine.set_depth(engine_params['Depth'])
                self.engine.update_engine_parameters({
                    'Threads': engine_params['Threads'],
                    'Hash': engine_params['Hash'],
                    'Contempt': engine_params['Contempt'],
                    'Ponder': engine_params['Ponder'],
                    'Slow Mover': engine_params['Slow Mover'],
                    'Move Overhead': engine_params['Move Overhead']
                })
                self.initialized = True
                init_duration = time.time() - start_time
                logger.info(f"Engine reuse took {init_duration:.2f} seconds with parameters: {engine_params}")
                return True
            
            # Поиск исполняемого файла Stockfish
            logger.info("Searching for Stockfish executable")
            self.engine_path = self._find_stockfish_executable()
            if not self.engine_path:
                error_msg = "Stockfish executable not found"
                logger.error(error_msg)
                raise EngineInitializationError(error_msg)
            
            # Инициализация нового движка с таймаутом
            logger.info(f"Initializing Stockfish engine from: {self.engine_path}")
            try:
                # Добавление таймаута для предотвращения бесконечного ожидания (кросс-платформенное решение)
                from concurrent.futures import TimeoutError as FutureTimeoutError
                
                def init_engine_task():
                    """Инициализация движка в отдельном потоке для контроля таймаута"""
                    logger.info(f"Creating Stockfish engine instance with skill level {self.skill_level}")
                    engine = Stockfish(path=self.engine_path)
                    
                    # Настройка движка с оптимизированными параметрами на основе уровня сложности
                    engine_params = self._calculate_engine_parameters(self.skill_level)
                    logger.info(f"Configuring engine parameters: {engine_params}")
                    engine.set_skill_level(self.skill_level)
                    engine.set_depth(engine_params['Depth'])
                    engine.update_engine_parameters({
                        'Threads': engine_params['Threads'],
                        'Hash': engine_params['Hash'],
                        'Contempt': engine_params['Contempt'],
                        'Ponder': engine_params['Ponder'],
                        'Slow Mover': engine_params['Slow Mover'],
                        'Move Overhead': engine_params['Move Overhead']
                    })
                    
                    # Тестирование движка простой операцией
                    logger.info("Testing engine functionality")
                    test_fen = engine.get_fen_position()
                    if test_fen is None:
                        raise EngineInitializationError("Engine test failed - returned None for FEN position")
                    logger.info(f"Engine test successful. Initial FEN: {test_fen}")
                    return engine
                
                # Использование ThreadPoolExecutor с таймаутом (работает на всех платформах)
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(init_engine_task)
                    try:
                        self.engine = future.result(timeout=15)  # Таймаут 15 секунд
                    except FutureTimeoutError:
                        error_msg = "Stockfish engine initialization timed out (15 seconds)"
                        logger.error(error_msg)
                        # Попытка отменить задачу (может не сработать, если уже выполняется)
                        future.cancel()
                        raise EngineInitializationError(error_msg)
                
                # Сохранение движка для переиспользования
                stockfish_engine = self.engine
                self.initialized = True
                init_duration = time.time() - start_time
                logger.info(f"Stockfish engine initialized successfully with skill level {self.skill_level} in {init_duration:.2f} seconds")
                return True
            except Exception as e:
                error_msg = f"Stockfish engine initialization failed: {str(e)}"
                logger.error(error_msg)
                logger.exception("Full traceback:")
                raise EngineInitializationError(error_msg) from e
        except EngineInitializationError:
            # Повторный выброс ошибок инициализации движка
            raise
        except Exception as e:
            error_msg = f"Stockfish initialization error: {str(e)}"
            logger.error(error_msg)
            logger.exception("Full traceback:")
            # Попытка очистки частично инициализированного движка
            try:
                if hasattr(self, 'engine') and self.engine:
                    if CONNECTION_POOLING_ENABLED and self._engine_context:
                        try:
                            self._engine_context.__exit__(None, None, None)
                        except Exception as cleanup_error:
                            logger.warning(f"Error cleaning up engine context: {cleanup_error}")
                    else:
                        # Stockfish не имеет явного метода закрытия, просто удаляем ссылку
                        self.engine = None
            except Exception as cleanup_error:
                logger.warning(f"Error during engine cleanup: {cleanup_error}")
            self.initialized = False
            raise EngineInitializationError(error_msg) from e
    
    def __del__(self):
        """Очистка движка при уничтожении экземпляра ChessGame"""
        try:
            if hasattr(self, 'initialized') and hasattr(self, 'engine'):
                if self.initialized and self.engine:
                    if hasattr(self, '_engine_context') and self._engine_context:
                        try:
                            # Безопасное закрытие контекста движка
                            self._engine_context.__exit__(None, None, None)
                        except Exception as e:
                            logger.warning(f"Error closing engine context: {e}")
                    try:
                        # Принудительное закрытие процесса Stockfish
                        if hasattr(self.engine, 'process') and self.engine.process:
                            self.engine.process.terminate()
                            self.engine.process.wait(timeout=1)
                    except Exception as e:
                        logger.warning(f"Error terminating Stockfish process: {e}")
                    finally:
                        # Очистка ссылок
                        self.engine = None
                        self._engine_context = None
                        self.initialized = False
        except Exception as e:
            logger.error(f"Critical error during engine cleanup: {e}")
            # В случае критической ошибки пытаемся очистить все ссылки
            self.engine = None
            self._engine_context = None
            self.initialized = False
    
    @cached('board_state')
    @track_fen_retrieval
    @handle_chess_errors(context="fen_retrieval")
    def get_fen(self):
        if self.engine and self.initialized:
            try:
                # Сначала проверка кэша
                current_time = time.time()
                if (self._fen_cache and 
                    current_time - self._fen_cache_timestamp < self._fen_cache_ttl):
                    return self._fen_cache
                
                fen = self.engine.get_fen_position()
                if fen is None:
                    logger.warning("Stockfish returned None for FEN position")
                
                # Обновление кэша
                self._fen_cache = fen
                self._fen_cache_timestamp = current_time
                
                return fen
            except Exception as e:
                logger.error(f"Error getting FEN position: {e}")
                raise GameLogicError(f"Failed to get FEN position: {str(e)}") from e
        else:
            logger.warning("Engine not initialized when trying to get FEN")
            raise EngineInitializationError("Engine not initialized")
        return None
    
    @track_move_execution
    @handle_chess_errors(context="move_execution")
    def make_move(self, move):
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
        # Проверка формата хода
        if not isinstance(move, str) or len(move) != 4:
            logger.error(f"Invalid move format: {move}")
            raise MoveValidationError(f"Invalid move format: {move}")
        try:
            # Очистка кэша FEN, так как позиция изменится
            self._fen_cache = None
            
            # make_moves_from_current_position возвращает None при успехе, False при неудаче
            result = self.engine.make_moves_from_current_position([move])
            success = result is not False
            if not success:
                logger.warning(f"Move {move} was rejected by Stockfish engine")
                raise MoveValidationError(f"Move {move} was rejected by Stockfish engine")
            return success
        except MoveValidationError:
            raise
        except Exception as e:
            logger.error(f"Error making move {move}: {e}")
            raise GameLogicError(f"Failed to execute move {move}: {str(e)}") from e
    
    @cached('valid_moves')
    @track_move_validation
    @handle_chess_errors(context="move_validation")
    def is_move_correct(self, move):
        """
        Проверка корректности хода с использованием встроенной валидации Stockfish для лучшей производительности.
        Если это не удается, используется метод сравнения позиций.
        """
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
            
        # Проверка формата хода first
        if not isinstance(move, str) or len(move) != 4:
            logger.warning(f"Invalid move format: {move}")
            raise MoveValidationError(f"Invalid move format: {move}")
            
        # Сначала попытка использовать встроенную валидацию Stockfish (быстрее)
        try:
            return self.engine.is_move_correct(move)
        except Exception as e:
            logger.warning(f"Built-in move validation failed: {e}")
            # Возврат к методу сравнения позиций, если встроенная валидация не удалась
            try:
                # Сохранение текущей позиции
                fen_before = self.engine.get_fen_position()
                
                # Попытка сделать ход
                result = self.engine.make_moves_from_current_position([move])
                
                # Проверка, изменилась ли позиция
                fen_after = self.engine.get_fen_position()
                move_successful = (result is not False) and (fen_before != fen_after)
                
                # Если ход был успешным, отменяем его для сохранения текущего состояния
                if move_successful:
                    # Сброс к предыдущей позиции
                    self.engine.set_fen_position(fen_before)
                
                return move_successful
            except Exception as e:
                logger.error(f"Position comparison method failed: {e}")
                raise MoveValidationError(f"Failed to validate move {move}: {str(e)}") from e
    
    @cached('ai_move')
    @track_ai_calculation
    @handle_chess_errors(context="ai_move_calculation")
    @retry_on_failure(max_attempts=2, delay=0.5, backoff=1.5)
    def get_best_move(self):
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
        try:
            best_move = self.engine.get_best_move()
            if best_move is None:
                logger.warning("Stockfish returned None for best move")
            return best_move
        except Exception as e:
            logger.error(f"Error getting best move: {e}")
            raise GameLogicError(f"Failed to get best move: {str(e)}") from e
    
    @cached('evaluation')
    @handle_chess_errors(context="position_evaluation")
    def get_evaluation(self):
        """Получение оценки позиции от Stockfish"""
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
        try:
            return self.engine.get_evaluation()
        except Exception as e:
            logger.error(f"Error getting evaluation: {e}")
            raise GameLogicError(f"Failed to get position evaluation: {str(e)}") from e
    
    @cached('valid_moves')
    @handle_chess_errors(context="top_moves")
    def get_top_moves(self, limit=5):
        """Получение лучших ходов от Stockfish"""
        if not self.initialized or not self.engine:
            logger.error("Engine not initialized")
            raise EngineInitializationError("Engine not initialized")
        try:
            return self.engine.get_top_moves(limit)
        except Exception as e:
            logger.error(f"Error getting top moves: {e}")
            raise GameLogicError(f"Failed to get top moves: {str(e)}") from e
    
    @cached('game_status')
    @track_game_status_check
    @handle_chess_errors(context="game_status_check")
    def get_game_status(self, fen):
        """
        Определение статуса игры (шах, мат, пат) из строки FEN.
        Возвращает словарь с информацией о статусе игры.
        """
        if not fen:
            return {'game_over': False}
        
        # Проверка мата с использованием оценки Stockfish
        if self.engine and self.initialized:
            try:
                # Получение оценки для проверки мата
                evaluation = self.engine.get_evaluation()
                if evaluation and 'type' in evaluation:
                    if evaluation['type'] == 'mate' and evaluation['value'] == 0:
                        # Мат в 0 означает, что текущий игрок получил мат
                        winner = 'black' if 'w' in fen else 'white'
                        return {
                            'game_over': True,
                            'result': 'checkmate',
                            'winner': winner
                        }
                    elif evaluation['type'] == 'cp' and evaluation['value'] == 0:
                        # Проверка пата проверкой наличия легальных ходов
                        best_move = self.engine.get_best_move()
                        if not best_move:
                            return {
                                'game_over': True,
                                'result': 'stalemate'
                            }
            except Exception as e:
                logger.warning(f"Stockfish evaluation failed: {e}")
                # Возврат к FEN-основанному обнаружению, если оценка не удалась
                pass
        
        # Возврат к оригинальному FEN-основанному обнаружению
        try:
            if '#' in fen:
                # Проверка мата
                if ' w ' in fen:
                    # Белые ходят, но в мате
                    if not any(c.isupper() for c in fen.split()[0] if c.isalpha()):
                        return {
                            'game_over': True,
                            'result': 'checkmate',
                            'winner': 'black'
                        }
                else:
                    # Черные ходят, но в мате
                    if not any(c.islower() for c in fen.split()[0] if c.isalpha()):
                        return {
                            'game_over': True,
                            'result': 'checkmate',
                            'winner': 'white'
                        }
        except Exception as e:
            logger.warning(f"FEN-based game status detection failed: {e}")
            pass
        
        return {'game_over': False}

@app.route('/')
def index():
    # Генерация уникального ID сессии для каждого пользователя
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    logger.info(f"HTTP session created with session_id: {session.get('session_id')}")
    return render_template('index.html')

@app.route('/profile_page')
def profile_page():
    """Отображение страницы профиля"""
    # Проверка, вошел ли пользователь в систему
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    
    return render_template('profile.html')

@socketio.on('connect')
@handle_chess_errors(context="websocket_connect")
def handle_connect(auth=None):
    try:
        # Создание ID сессии для Socket.IO соединения, если его нет
        logger.info("WebSocket connect event received")
        logger.info(f"Current session keys: {list(session.keys())}")
        logger.info(f"Current session_id: {session.get('session_id')}")
        
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            logger.info(f"Created new session_id for WebSocket: {session.get('session_id')}")
        else:
            logger.info(f"Using existing session_id for WebSocket: {session.get('session_id')}")
            
        # Обновление временной метки сессии с проверкой существования
        session_id = session.get('session_id')
        if session_id:
            if session_id not in session_timestamps:
                session_timestamps[session_id] = time.time()
            else:
                session_timestamps[session_id] = time.time()
            
        # Отправка подтверждения соединения
        emit('connected', {'status': 'success', 'message': 'Connected successfully'})
    except Exception as e:
        logger.error(f"Error in connect handler: {e}")
        emit('error', {'message': 'Connection error'})

@socketio.on('disconnect')
@handle_chess_errors(context="websocket_disconnect")
def handle_disconnect():
    try:
        session_id = session.get('session_id')
        logger.info(f"WebSocket disconnect event received for session: {session_id}")
        if session_id:
            # Удаление игры через AppState
            if app_state.remove_game(session_id):
                logger.info(f"Client disconnected, cleaned up game for session: {session_id}")
                
                # Получение актуальной статистики
                stats = app_state.get_stats()
                logger.info(f"Active games count: {stats['active_games']}")
            else:
                logger.warning(f"No game found for session: {session_id}")
        
        # Отправка подтверждения отключения
        logger.info("Client disconnected successfully")
    except Exception as e:
        logger.error(f"Error in disconnect handler: {e}")

# Функции валидации
def validate_username(username):
    """Проверка формата имени пользователя"""
    if not username:
        return False, "Username is required"
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    if len(username) > 30:
        return False, "Username must be less than 30 characters"
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    return True, None

def validate_email(email):
    """Проверка формата email"""
    if not email:
        return False, "Email is required"
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    return True, None

def validate_password(password):
    """Проверка надежности пароля"""
    if not password:
        return False, "Password is required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    return True, None

# Добавлено после существующих маршрутов и перед endpoint проверки здоровья

@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
@handle_chess_errors(context="user_registration")
def register_user():
    """Регистрация нового пользователя"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        # Валидация входных данных
        if not username or not email or not password:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Валидация имени пользователя
        is_valid, error_msg = validate_username(username)
        if not is_valid:
            return jsonify({'success': False, 'message': error_msg}), 400
        
        # Валидация email
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            return jsonify({'success': False, 'message': error_msg}), 400
        
        # Валидация пароля
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({'success': False, 'message': error_msg}), 400
        
        # Проверка, включена ли база данных и доступны ли модели
        if not DATABASE_ENABLED or User is None or db is None:
            return jsonify({'success': False, 'message': 'Database not enabled'}), 500
        
        # Проверка, существует ли пользователь
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'User already exists'}), 400
        
        # Безопасное хеширование пароля
        password_hash = generate_password_hash(password)
        
        # Создание нового пользователя
        if create_user is not None:
            user = create_user(username, email, password_hash)
            logger.info(f"User registered successfully: {username}")
            return jsonify({'success': True, 'message': 'User registered successfully', 'user_id': user.id})
        else:
            return jsonify({'success': False, 'message': 'User creation failed'}), 500
    except Exception as e:
        logger.error(f"Error registering user: {e}")
        return jsonify({'success': False, 'message': 'Registration failed'}), 500

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
@handle_chess_errors(context="user_login")
def login_user():
    """Вход пользователя в систему"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        # Валидация входных данных
        if not username or not password:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Проверка, включена ли база данных и доступны ли модели
        if not DATABASE_ENABLED or User is None or db is None:
            return jsonify({'success': False, 'message': 'Database not enabled'}), 500
        
        # Проверка, существует ли пользователь
        user = User.query.filter(User.username == username).first() if User is not None else None
        
        # Проверка пароля (поддержка как старых паролей в открытом виде, так и новых хешированных для миграции)
        if user:
            # Проверка, хеширован ли пароль (начинается с pbkdf2:)
            if user.password_hash.startswith('pbkdf2:'):
                password_valid = check_password_hash(user.password_hash, password)
            else:
                # Поддержка старого формата: пароль в открытом виде (для существующих пользователей)
                password_valid = (user.password_hash == password)
                # Если пароль совпадает в открытом виде, хешируем его для будущего использования
                if password_valid:
                    logger.info(f"Upgrading password hash for user: {username}")
                    user.password_hash = generate_password_hash(password)
            
            if password_valid:
                # Обновление времени последнего входа
                user.last_login = datetime.utcnow()
                if db is not None:
                    try:
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        logger.error(f"Error updating user login timestamp: {e}")
                        return jsonify({'success': False, 'message': 'Login failed'}), 500
                
                # Сохранение ID пользователя в сессии
                session['user_id'] = user.id
                logger.info(f"User logged in successfully: {username}")
                
                return jsonify({
                    'success': True, 
                    'message': 'Login successful', 
                    'user_id': user.id,
                    'username': user.username
                })
        
        # Неверные учетные данные - используем общее сообщение для предотвращения перечисления пользователей
        logger.warning(f"Failed login attempt for username: {username}")
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Error logging in user: {e}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@app.route('/logout')
@handle_chess_errors(context="user_logout")
def logout_user():
    """Выход пользователя из системы"""
    try:
        # Удаление ID пользователя из сессии
        session.pop('user_id', None)
        return jsonify({'success': True, 'message': 'Logout successful'})
    except Exception as e:
        logger.error(f"Error logging out user: {e}")
        return jsonify({'success': False, 'message': 'Logout failed'}), 500

@app.route('/profile')
@handle_chess_errors(context="user_profile")
def user_profile():
    """Отображение профиля пользователя"""
    try:
        # Проверка, вошел ли пользователь в систему
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'message': 'User not logged in'}), 401
        
        # Проверка, включена ли база данных
        if not DATABASE_ENABLED or User is None or Game is None:
            return jsonify({'success': False, 'message': 'Database not enabled'}), 500
        
        # Получение информации о пользователе
        user = User.query.get(user_id) if User is not None else None
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Получение последних игр пользователя с использованием оптимизированной функции
        if get_recent_games_optimized is not None:
            recent_games = get_recent_games_optimized(user_id, limit=10)
        else:
            recent_games = Game.query.filter_by(user_id=user_id).order_by(Game.start_time.desc()).limit(10).all() if Game is not None else []
        
        # Расчет статистики
        total_games = user.games_played or 0
        wins = user.games_won or 0
        losses = total_games - wins
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        
        # Подготовка данных истории игр
        game_history = []
        for game in recent_games:
            game_history.append({
                'id': game.id,
                'result': game.result,
                'player_color': game.player_color,
                'skill_level': game.skill_level,
                'start_time': game.start_time.isoformat() if game.start_time else None,
                'duration': game.duration
            })
        
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'rating': user.rating or 1200,
                'games_played': total_games,
                'wins': wins,
                'losses': losses,
                'win_rate': round(win_rate, 2)
            },
            'recent_games': game_history
        })
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        return jsonify({'success': False, 'message': 'Failed to fetch profile'}), 500

# Добавление endpoint проверки здоровья
@app.route('/health')
@handle_chess_errors(context="health_check")
def health_check():
    """Endpoint проверки здоровья для мониторинга"""
    try:
        # Проверка, можем ли мы создать простой экземпляр ChessGame
        game = ChessGame()
        
        # Получение статистики кэша, если менеджер кэша включен
        cache_stats = {}
        if CACHE_MANAGER_ENABLED and cache_manager:
            cache_stats = cache_manager.get_cache_stats()
        
        # Получение метрик производительности, если отслеживание производительности включено
        perf_metrics = {}
        if PERFORMANCE_TRACKING_ENABLED and performance_tracker:
            perf_metrics = performance_tracker.get_metrics_summary()
        
        # Получение статистики ошибок, если обработчик ошибок включен
        error_stats = {}
        if ERROR_HANDLER_ENABLED and error_handler:
            error_stats = error_handler.get_error_stats()
        
        # Получение статистики пула соединений, если пул соединений включен
        pool_stats = {}
        if CONNECTION_POOLING_ENABLED and stockfish_pool:
            pool_stats = stockfish_pool.get_stats()
        
        return {
            'status': 'healthy',
            'active_games': active_game_count,
            'tracked_sessions': len(session_timestamps),
            'cache_stats': cache_stats,
            'performance_metrics': perf_metrics,
            'error_stats': error_stats,
            'pool_stats': pool_stats
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {'status': 'unhealthy', 'error': str(e)}, 500

@socketio.on('init_game')
@handle_chess_errors(context="game_initialization")
def handle_init(data):
    start_time = time.time()
    logger.info(f"Game initialization requested with data: {data}")
    logger.info(f"Current session keys: {list(session.keys())}")
    session_id = session.get('session_id')
    logger.info(f"Session ID: {session_id}")
    
    if not session_id:
        logger.error("No session ID found")
        emit('error', {'message': 'Ошибка сессии. Попробуйте обновить страницу.'})
        return
        
    # Проверка лимита игр через AppState
    stats = app_state.get_stats()
    if stats['active_games'] >= MAX_CONCURRENT_GAMES:
        logger.warning(f"Maximum concurrent games reached ({MAX_CONCURRENT_GAMES}). Rejecting new game request.")
        emit('error', {'message': 'Сервер перегружен. Пожалуйста, попробуйте позже.'})
        return
    
    try:
        player_color = data.get('color', 'white')
        skill_level = min(20, max(0, int(data.get('level', 5))))
        
        logger.info(f"Creating game with color: {player_color}, skill level: {skill_level}")
        
        # Проверка, достигнуто ли максимальное количество одновременных игр
        global active_game_count
        if active_game_count >= MAX_CONCURRENT_GAMES:
            logger.warning(f"Maximum concurrent games reached ({MAX_CONCURRENT_GAMES}). Rejecting new game request.")
            emit('error', {'message': 'Сервер перегружен. Пожалуйста, попробуйте позже.'})
            total_init_time = time.time() - start_time
            logger.info(f"Total initialization time: {total_init_time:.2f} seconds")
            return
        
        # Проверка, есть ли у сессии уже активная игра
        if session_id in games:
            logger.info(f"Session {session_id} already has an active game. Cleaning up old game.")
            try:
                del games[session_id]
                active_game_count = max(0, active_game_count - 1)
            except:
                pass
        
        # Create a new game instance for this session
        game_init_start = time.time()
        game = ChessGame(player_color, skill_level)
        game_init_time = time.time() - game_init_start
        logger.info(f"Game initialization took {game_init_time:.2f} seconds")
        logger.info(f"Game initialization result: {game.initialized}")
        
        # Initialize engine with timeout
        engine_init_start = time.time()
        try:
            if game.init_engine():
                engine_init_time = time.time() - engine_init_start
                logger.info(f"Engine initialization took {engine_init_time:.2f} seconds")
                
                # Добавление игры через AppState
                if not app_state.add_game(session_id, game):
                    logger.error("Failed to add game to AppState")
                    emit('error', {'message': 'Ошибка инициализации игры'})
                    return
                
                # Get initial FEN with timeout handling
                try:
                    fen = game.get_fen()
                    if fen is None:
                        logger.error("Failed to get initial FEN position")
                        emit('error', {'message': 'Ошибка получения начальной позиции. Попробуйте перезапустить игру.'})
                        # Clean up
                        if session_id in games:
                            del games[session_id]
                            active_game_count -= 1
                        return
                    
                    logger.info(f"Game initialized successfully. Initial FEN: {fen}")
                    logger.info(f"Active games count: {active_game_count}")
                    
                    # Save game to database if user is logged in and database is enabled
                    game_id = None
                    user_id = session.get('user_id')
                    if DATABASE_ENABLED and user_id and Game is not None and db is not None:
                        try:
                            db_game = Game(
                                user_id=user_id,
                                fen=fen,
                                player_color=player_color,
                                skill_level=skill_level,
                                result='in_progress'
                            )
                            if db is not None:
                                db.session.add(db_game)
                                db.session.commit()
                                game_id = db_game.id
                                logger.info(f"Game saved to database with ID: {game_id}")
                        except Exception as e:
                            db.session.rollback()
                            logger.error(f"Failed to save game to database: {e}")
                    emit('game_initialized', {'fen': fen, 'player_color': player_color, 'game_id': game_id})
                    logger.info("Sent game_initialized event to client")
                    total_init_time = time.time() - start_time
                    logger.info(f"Total initialization time: {total_init_time:.2f} seconds")
                except Exception as e:
                    logger.error(f"Error getting initial FEN: {e}")
                    emit('error', {'message': 'Ошибка получения начальной позиции. Попробуйте перезапустить игру.'})
                    # Clean up
                    if session_id in games:
                        del games[session_id]
                        active_game_count -= 1
                    return
            else:
                logger.error("Failed to initialize Stockfish engine")
                emit('error', {'message': 'Ошибка движка Stockfish. Попробуйте перезапустить игру.'})
                total_init_time = time.time() - start_time
                logger.info(f"Total initialization time: {total_init_time:.2f} seconds")
        except EngineInitializationError as e:
            logger.error(f"Engine initialization error: {e}")
            emit('error', {'message': 'Ошибка движка Stockfish. Попробуйте перезапустить игру.'})
            # Re-enable start button on error
            try:
                emit('enable_start_button')
            except:
                pass  # Ignore if client is not connected
            total_init_time = time.time() - start_time
            logger.info(f"Total initialization time: {total_init_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error initializing game: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': 'Ошибка инициализации игры. Пожалуйста, проверьте консоль для получения дополнительной информации.'})
        # Re-enable start button on error
        try:
            emit('enable_start_button')
        except:
            pass  # Ignore if client is not connected
        total_init_time = time.time() - start_time
        logger.info(f"Total initialization time: {total_init_time:.2f} seconds")

@socketio.on('make_move')
@handle_chess_errors(context="move_processing")
def handle_move(data):
    start_time = time.time()
    try:
        logger.info(f"Move request received: {data}")
        logger.info(f"Current session keys: {list(session.keys())}")
        session_id = session.get('session_id')
        logger.info(f"Session ID: {session_id}")
        
        # Получение игры через AppState
        game = app_state.get_game(session_id)
        if not session_id or not game:
            logger.error("Game not initialized for this session")
            emit('error', {'message': 'Game not initialized'})
            return
        uci_move = data.get('move')
        
        # Validate move exists
        if not uci_move:
            logger.error("No move provided in request")
            emit('invalid_move', {'move': '', 'message': 'No move provided'})
            return

        # Проверка формата хода
        if not isinstance(uci_move, str) or len(uci_move) != 4:
            logger.warning(f"Invalid move format: {uci_move}")
            emit('invalid_move', {'move': uci_move, 'message': 'Invalid move format'})
            return

        # Store the move as the last move
        game.last_move = uci_move

        # Validate move using Stockfish with timeout
        move_validation_start = time.time()
        try:
            is_valid_move = game.is_move_correct(uci_move)
            move_validation_time = time.time() - move_validation_start
            logger.info(f"Move validation took {move_validation_time:.2f} seconds")
        except MoveValidationError as e:
            logger.warning(f"Move validation error: {e}")
            emit('invalid_move', {'move': uci_move, 'message': str(e)})
            return
        except Exception as e:
            logger.error(f"Unexpected error during move validation: {e}")
            emit('error', {'message': 'Ошибка проверки хода'})
            return
        
        if is_valid_move:
            move_execution_start = time.time()
            try:
                if not game.make_move(uci_move):
                    logger.warning(f"Move execution failed for move: {uci_move}")
                    emit('invalid_move', {'move': uci_move, 'message': 'Invalid move'})
                    return
                move_execution_time = time.time() - move_execution_start
                logger.info(f"Move execution took {move_execution_time:.2f} seconds")
            except Exception as e:
                logger.error(f"Error executing move {uci_move}: {e}")
                emit('error', {'message': 'Ошибка выполнения хода'})
                return
                
            # Add move to history
            game.move_history.append(uci_move)
                
            try:
                fen = game.get_fen()
                if fen is None:
                    logger.error("Failed to get FEN after move execution")
                    emit('error', {'message': 'Ошибка получения позиции после хода'})
                    return
            except Exception as e:
                logger.error(f"Error getting FEN after move: {e}")
                emit('error', {'message': 'Ошибка получения позиции после хода'})
                return
            
            # Update session timestamp
            if session_id not in session_timestamps:
                session_timestamps[session_id] = time.time()
            else:
                session_timestamps[session_id] = time.time()

            # Check game status using improved logic
            game_status_start = time.time()
            try:
                game_status = game.get_game_status(fen)
                game_status_time = time.time() - game_status_start
                logger.info(f"Game status check took {game_status_time:.2f} seconds")
            except Exception as e:
                logger.error(f"Error checking game status: {e}")
                emit('error', {'message': 'Ошибка проверки статуса игры'})
                return
            
            if game_status['game_over']:
                # Update game result in database if user is logged in and database is enabled
                user_id = session.get('user_id')
                if DATABASE_ENABLED and user_id and Game is not None and db is not None:
                    try:
                        # Find the game in the database (optimized with index)
                        db_game = Game.query.filter_by(user_id=user_id, result='in_progress').order_by(Game.start_time.desc()).first()
                        if db_game:
                            # Update game result
                            db_game.result = game_status['result']
                            db_game.end_time = datetime.utcnow()
                            db_game.duration = int((db_game.end_time - db_game.start_time).total_seconds()) if db_game.start_time else 0
                            db_game.move_history = json.dumps(game.move_history) if game.move_history else None
                            
                            # Update user stats
                            user = User.query.get(user_id) if User is not None else None
                            if user:
                                # Use a transaction to ensure consistency
                                user.games_played = (user.games_played or 0) + 1
                                if game_status.get('winner') == game.player_color:
                                    user.games_won = (user.games_won or 0) + 1
                                    # Simple rating update - in a real app, you'd use a proper rating system
                                    user.rating = (user.rating or 1200) + 10
                                elif game_status['result'] == 'stalemate':
                                    # No rating change for stalemate
                                    pass
                                else:
                                    # Loss - decrease rating
                                    user.rating = max(100, (user.rating or 1200) - 5)
                            
                            db.session.commit()
                            logger.info(f"Game result saved to database: {game_status['result']}")
                    except Exception as e:
                        db.session.rollback()
                        logger.error(f"Failed to save game result to database: {e}")
                        logger.exception("Full traceback:")
                
                emit('game_over', {
                    'result': game_status['result'],
                    'fen': fen,
                    'winner': game_status.get('winner'),
                    'last_move': game.last_move
                })
                total_move_time = time.time() - start_time
                logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
                return

            # Notify client that AI is thinking
            emit('ai_thinking', {'status': 'calculating'})
            
            # AI move with timeout and retry logic
            ai_move_start = time.time()
            try:
                ai_move = game.get_best_move()
                ai_move_time = time.time() - ai_move_start
                logger.info(f"AI move calculation took {ai_move_time:.2f} seconds")
                
                # Уведомление клиента, что AI закончил думать
                emit('ai_thinking', {'status': 'complete', 'time': ai_move_time})
            except Exception as e:
                logger.error(f"Error getting AI move: {e}")
                emit('ai_thinking', {'status': 'error'})
                emit('error', {'message': 'Ошибка получения хода компьютера'})
                return
            
            if ai_move:
                # Сохранение хода AI как последнего хода
                game.last_move = ai_move
                
                ai_move_execution_start = time.time()
                try:
                    if not game.make_move(ai_move):
                        logger.warning(f"AI move execution failed for move: {ai_move}")
                        emit('position_update', {'fen': fen, 'last_move': game.last_move})
                        return
                    ai_move_execution_time = time.time() - ai_move_execution_start
                    logger.info(f"AI move execution took {ai_move_execution_time:.2f} seconds")
                except Exception as e:
                    logger.error(f"Error executing AI move {ai_move}: {e}")
                    emit('error', {'message': 'Ошибка выполнения хода компьютера'})
                    return
                    
                # Добавление хода AI в историю
                game.move_history.append(ai_move)
                    
                try:
                    fen = game.get_fen()
                    if fen is None:
                        logger.error("Failed to get FEN after AI move execution")
                        emit('error', {'message': 'Ошибка получения позиции после хода компьютера'})
                        return
                except Exception as e:
                    logger.error(f"Error getting FEN after AI move: {e}")
                    emit('error', {'message': 'Ошибка получения позиции после хода компьютера'})
                    return
                
                # Проверка статуса игры после хода AI
                game_status_start = time.time()
                try:
                    game_status = game.get_game_status(fen)
                    game_status_time = time.time() - game_status_start
                    logger.info(f"Post-AI game status check took {game_status_time:.2f} seconds")
                except Exception as e:
                    logger.error(f"Error checking game status after AI move: {e}")
                    emit('error', {'message': 'Ошибка проверки статуса игры после хода компьютера'})
                    return
                
                if game_status['game_over']:
                    # Обновление результата игры в базе данных, если пользователь вошел и база данных включена
                    user_id = session.get('user_id')
                    if DATABASE_ENABLED and user_id and Game is not None and db is not None:
                        try:
                            # Поиск игры в базе данных
                            db_game = Game.query.filter_by(user_id=user_id, result='in_progress').order_by(Game.start_time.desc()).first()
                            if db_game:
                                # Обновление результата игры
                                db_game.result = game_status['result']
                                db_game.end_time = datetime.utcnow()
                                db_game.duration = int((db_game.end_time - db_game.start_time).total_seconds()) if db_game.start_time else 0
                                db_game.move_history = json.dumps(game.move_history) if game.move_history else None
                                
                                # Обновление статистики пользователя
                                user = User.query.get(user_id) if User is not None else None
                                if user and User is not None:
                                    # Использование транзакции для обеспечения согласованности
                                    user.games_played = (user.games_played or 0) + 1
                                    if game_status.get('winner') == game.player_color:
                                        user.games_won = (user.games_won or 0) + 1
                                        # Простое обновление рейтинга - в реальном приложении использовалась бы правильная система рейтинга
                                        user.rating = (user.rating or 1200) + 10
                                    elif game_status['result'] == 'stalemate':
                                        # Нет изменения рейтинга при пате
                                        pass
                                    else:
                                        # Поражение - уменьшение рейтинга
                                        user.rating = max(100, (user.rating or 1200) - 5)
                                
                                db.session.commit()
                                logger.info(f"Game result saved to database: {game_status['result']}")
                        except Exception as e:
                            db.session.rollback()
                            logger.error(f"Failed to save game result to database: {e}")
                            logger.exception("Full traceback:")
                    
                    emit('game_over', {
                        'result': game_status['result'],
                        'fen': fen,
                        'winner': game_status.get('winner'),
                        'last_move': game.last_move
                    })
                    total_move_time = time.time() - start_time
                    logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
                    return
                    
                emit('position_update', {'fen': fen, 'ai_move': ai_move, 'last_move': game.last_move})
            else:
                logger.warning("No AI move available")
                emit('position_update', {'fen': fen, 'last_move': game.last_move})
                
            total_move_time = time.time() - start_time
            logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
        else:
            logger.warning(f"Invalid move: {uci_move}")
            emit('invalid_move', {'move': uci_move, 'message': 'Invalid move'})
            total_move_time = time.time() - start_time
            logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
    except MoveValidationError as e:
        logger.warning(f"Move validation error: {e}")
        emit('invalid_move', {'move': data.get('move', ''), 'message': str(e)})
        total_move_time = time.time() - start_time
        logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
    except EngineInitializationError as e:
        logger.error(f"Engine error during move processing: {e}")
        emit('error', {'message': 'Ошибка движка. Попробуйте перезапустить игру.'})
        total_move_time = time.time() - start_time
        logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
    except GameLogicError as e:
        logger.error(f"Game logic error: {e}")
        emit('error', {'message': 'Ошибка обработки хода'})
        total_move_time = time.time() - start_time
        logger.info(f"Total move processing time: {total_move_time:.2f} seconds")
    except Exception as e:
        logger.error(f"Error processing move: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': 'Ошибка обработки хода'})
        total_move_time = time.time() - start_time
        logger.info(f"Total move processing time: {total_move_time:.2f} seconds")

@socketio.on('takeback_move')
@handle_chess_errors(context="move_takeback")
def handle_takeback():
    """Обработка запроса на отмену хода"""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in games:
            emit('error', {'message': 'Game not initialized'})
            return

        game = games[session_id]
        
        if not game.engine or not game.initialized:
            emit('error', {'message': 'Engine not initialized'})
            return
            
        # Check if there are moves to take back
        if len(game.move_history) < 1:
            emit('error', {'message': 'No moves to take back'})
            return
            
        # Remove the last move from history
        last_move = game.move_history.pop()
        
        # Set the engine to the previous position
        if game.move_history:
            # Reset to starting position first
            game.engine.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            # Apply all moves except the last one
            if game.move_history:
                game.engine.make_moves_from_current_position(game.move_history)
        else:
            # Reset to starting position
            game.engine.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        
        fen = game.get_fen()
        if fen is None:
            logger.error("Failed to get FEN after takeback")
            emit('error', {'message': 'Ошибка получения позиции после отмены хода'})
            return
            
        # Update session timestamp
        session_timestamps[session_id] = time.time()
        
        emit('position_update', {'fen': fen, 'takeback': True})
        
    except Exception as e:
        logger.error(f"Error processing takeback: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': 'Ошибка отмены хода'})

@socketio.on('analyze_position')
@handle_chess_errors(context="position_analysis")
def handle_analysis(data):
    """Анализ текущей позиции и возврат оценки"""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in games:
            emit('error', {'message': 'Game not initialized'})
            return

        game = games[session_id]
        fen = data.get('fen', game.get_fen())
        
        if game.engine:
            # Set position for analysis
            game.engine.set_fen_position(fen)
            
            # Get evaluation
            evaluation = game.get_evaluation()
            
            # Get best move for analysis
            best_move = game.get_best_move()
            
            # Get top moves
            top_moves = game.get_top_moves(3)  # Get top 3 moves
            
            emit('analysis_result', {
                'fen': fen,
                'evaluation': evaluation,
                'best_move': best_move,
                'top_moves': top_moves
            })
        else:
            emit('error', {'message': 'Engine not available'})
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        emit('error', {'message': 'Ошибка анализа позиции'})

@socketio.on('save_preferences')
@handle_chess_errors(context="preferences_save")
def handle_save_preferences(data):
    """Сохранение пользовательских настроек"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            emit('error', {'message': 'Session not found'})
            return
            
        # Store preferences
        user_preferences[session_id] = data.get('preferences', {})
        
        emit('preferences_saved', {
            'success': True,
            'message': 'Настройки сохранены успешно'
        })
    except Exception as e:
        logger.error(f"Error saving preferences: {e}")
        emit('error', {'message': 'Ошибка сохранения настроек'})

@socketio.on('load_preferences')
@handle_chess_errors(context="preferences_load")
def handle_load_preferences():
    """Загрузка пользовательских настроек"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            emit('error', {'message': 'Session not found'})
            return
            
        # Get preferences
        preferences = user_preferences.get(session_id, {})
        
        emit('preferences_loaded', {
            'preferences': preferences
        })
    except Exception as e:
        logger.error(f"Error loading preferences: {e}")
        emit('error', {'message': 'Ошибка загрузки настроек'})

@socketio.on('save_game')
@handle_chess_errors(context="game_save")
def handle_save_game(data):
    """Сохранение текущего состояния игры"""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in games:
            emit('error', {'message': 'Game not initialized'})
            return

        game = games[session_id]
        
        # Get current FEN
        fen = game.get_fen()
        if fen is None:
            logger.error("Failed to get FEN for game save")
            emit('error', {'message': 'Ошибка получения позиции для сохранения'})
            return
        
        # Create game state object
        game_state = {
            'fen': fen,
            'player_color': game.player_color,
            'skill_level': game.skill_level,
            'game_history': game_histories.get(session_id, []) if session_id in game_histories else [],
            'timestamp': time.time()
        }
        
        # Serialize game state
        try:
            serialized_state = base64.b64encode(pickle.dumps(game_state)).decode('utf-8')
        except Exception as e:
            logger.error(f"Error serializing game state: {e}")
            emit('error', {'message': 'Ошибка сериализации игры'})
            return
        
        emit('game_saved', {
            'success': True,
            'game_state': serialized_state,
            'message': 'Игра сохранена успешно'
        })
    except Exception as e:
        logger.error(f"Error saving game: {e}")
        emit('error', {'message': 'Ошибка сохранения игры'})

@socketio.on('load_game')
@handle_chess_errors(context="game_load")
def handle_load_game(data):
    """Загрузка сохраненного состояния игры"""
    try:
        session_id = session.get('session_id')
        serialized_state = data.get('game_state')
        
        if not serialized_state:
            emit('error', {'message': 'Нет данных для загрузки'})
            return
        
        # Deserialize game state
        try:
            game_state = pickle.loads(base64.b64decode(serialized_state.encode('utf-8')))
        except Exception as e:
            logger.error(f"Error deserializing game state: {e}")
            emit('error', {'message': 'Ошибка десериализации сохраненной игры'})
            return
        
        # Validate game state
        if not isinstance(game_state, dict):
            logger.error("Invalid game state format")
            emit('error', {'message': 'Неверный формат сохраненной игры'})
            return
            
        required_fields = ['player_color', 'skill_level', 'fen']
        for field in required_fields:
            if field not in game_state:
                logger.error(f"Missing required field in game state: {field}")
                emit('error', {'message': f'Отсутствует обязательное поле: {field}'})
                return
        
        # Create new game instance with saved parameters
        game = ChessGame(game_state['player_color'], game_state['skill_level'])
        
        # Initialize engine
        if not game.init_engine():
            emit('error', {'message': 'Не удалось инициализировать движок'})
            return
            
        # Set position
        if game.engine:
            try:
                game.engine.set_fen_position(game_state['fen'])
                game.initialized = True
                
                # Store game in session
                games[session_id] = game
                
                # Update session timestamp
                session_timestamps[session_id] = time.time()
                
                emit('game_loaded', {
                    'fen': game_state['fen'],
                    'player_color': game_state['player_color'],
                    'skill_level': game_state['skill_level'],
                    'game_history': game_state.get('game_history', []),
                    'message': 'Игра загружена успешно'
                })
            except Exception as e:
                logger.error(f"Error setting FEN position: {e}")
                emit('error', {'message': 'Ошибка установки позиции доски'})
                return
        else:
            emit('error', {'message': 'Не удалось инициализировать движок'})
    except Exception as e:
        logger.error(f"Error loading game: {e}")
        emit('error', {'message': 'Ошибка загрузки игры'})

@app.route('/pool-stats')
def pool_stats():
    """Endpoint для получения статистики пула соединений"""
    try:
        # Test connection pooling if enabled
        pool_stats = {}
        if CONNECTION_POOLING_ENABLED and stockfish_pool:
            pool_stats = stockfish_pool.get_stats()
        
        return {
            'status': 'success',
            'connection_pooling_enabled': CONNECTION_POOLING_ENABLED,
            'pool_stats': pool_stats,
            'timestamp': time.time()
        }
    except Exception as e:
        logger.error(f"Pool stats endpoint failed: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }, 500

@app.route('/metrics')
@handle_chess_errors(context="metrics")
def metrics_endpoint():
    """Endpoint для получения метрик производительности в формате Prometheus"""
    try:
        metrics = []
        
        # Get cache statistics
        if CACHE_MANAGER_ENABLED and cache_manager:
            cache_stats = cache_manager.get_cache_stats()
            for cache_name, stats in cache_stats.items():
                if isinstance(stats, dict):
                    metrics.append(f'cache_hits{{cache="{cache_name}"}} {stats.get("hits", 0)}')
                    metrics.append(f'cache_misses{{cache="{cache_name}"}} {stats.get("misses", 0)}')
                    metrics.append(f'cache_size{{cache="{cache_name}"}} {stats.get("size", 0)}')
                    hit_rate = stats.get("hit_rate", 0)
                    if hit_rate is not None:
                        metrics.append(f'cache_hit_rate{{cache="{cache_name}"}} {hit_rate:.4f}')
        
        # Get performance metrics
        if PERFORMANCE_TRACKING_ENABLED and performance_tracker:
            perf_metrics = performance_tracker.get_metrics_summary()
            for operation, data in perf_metrics.items():
                if isinstance(data, dict):
                    avg_time = data.get('avg_time', 0)
                    if avg_time:
                        metrics.append(f'operation_duration_seconds{{operation="{operation}"}} {avg_time:.4f}')
        
        # Game statistics
        metrics.append(f'active_games_total {active_game_count}')
        metrics.append(f'tracked_sessions_total {len(session_timestamps)}')
        metrics.append(f'concurrent_games_limit {MAX_CONCURRENT_GAMES}')
        
        # Resource statistics
        resource_stats['peak_active_games'] = max(resource_stats['peak_active_games'], active_game_count)
        metrics.append(f'peak_active_games {resource_stats["peak_active_games"]}')
        
        # Connection pool statistics
        if CONNECTION_POOLING_ENABLED and stockfish_pool:
            pool_stats = stockfish_pool.get_stats()
            metrics.append(f'engine_pool_size {pool_stats.get("pool_size", 0)}')
            metrics.append(f'engine_pool_active {pool_stats.get("active_engines", 0)}')
            metrics.append(f'engine_pool_max {pool_stats.get("max_engines", 0)}')
            metrics.append(f'engine_pool_total_created {pool_stats.get("total_created", 0)}')
            metrics.append(f'engine_pool_total_reused {pool_stats.get("total_reused", 0)}')
        
        return '\n'.join(metrics), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}
    except Exception as e:
        logger.error(f"Metrics endpoint failed: {e}")
        return f'# Error generating metrics: {str(e)}', 500, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/resource-stats')
def resource_stats_endpoint():
    """Endpoint to get resource usage statistics"""
    try:
        # Получение статистики через AppState
        app_stats = app_state.get_stats()
        
        # Сбор статистики использования памяти
        memory_stats = {}
        try:
            import psutil
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_stats = {
                'rss': memory_info.rss / (1024 * 1024),  # MB
                'vms': memory_info.vms / (1024 * 1024),  # MB
                'percent': process.memory_percent(),
                'cpu_percent': process.cpu_percent()
            }
        except ImportError:
            memory_stats = {'error': 'psutil not available'}
        except Exception as e:
            memory_stats = {'error': str(e)}

        # Сбор статистики кэша
        cache_stats = {}
        if CACHE_MANAGER_ENABLED and cache_manager:
            try:
                cache_stats = cache_manager.get_cache_stats()
            except Exception as e:
                cache_stats = {'error': str(e)}

        # Сбор статистики пула соединений
        pool_stats = {}
        if CONNECTION_POOLING_ENABLED and stockfish_pool:
            try:
                pool_stats = stockfish_pool.get_stats()
            except Exception as e:
                pool_stats = {'error': str(e)}
        
        # Сбор статистики производительности
        perf_metrics = {}
        if PERFORMANCE_TRACKING_ENABLED and performance_tracker:
            try:
                perf_metrics = performance_tracker.get_metrics_summary()
            except Exception as e:
                perf_metrics = {'error': str(e)}
        
        response = {
            'status': 'success',
            'timestamp': time.time(),
            'resource_stats': app_stats['resource_stats'],
            'current_stats': {
                'active_games': app_stats['active_games'],
                'tracked_sessions': len(app_stats['game_stats']),
                'game_stats': app_stats['game_stats'],
                'memory_usage': memory_stats,
                'cache_stats': cache_stats,
                'pool_stats': pool_stats,
                'performance_metrics': perf_metrics,
                'recent_errors': app_stats.get('recent_errors', [])
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in resource stats endpoint: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# Запуск потока очистки после определения всех переменных для предотвращения гонок
cleanup_thread = threading.Thread(target=cleanup_stale_games, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    logger.info("Starting Chess Stockfish Web application...")
    
    # Create database tables if they don't exist
    if DATABASE_ENABLED and db is not None:
        with app.app_context():
            db.create_all()
    
    socketio.run(app, host='127.0.0.1', port=5001, debug=False)