# ============================================================================
# engine/stockfish_pool.py
# ============================================================================

"""
Модуль: engine/stockfish_pool.py

Описание:
    Реализация пула подключений к шахматному движку Stockfish для уменьшения
    накладных расходов на запуск и остановку движков.

Возможности:
    - Пул предварительно запущенных движков Stockfish
    - Автоматическое управление жизненным циклом движков
    - Потокобезопасное получение и возврат движков
    - Автоматическая очистка неиспользуемых движков
"""

import threading
import queue
import time
from typing import Optional, Dict, Any
from stockfish import Stockfish
import os
import shutil


class StockfishEnginePool:
    """
    Пул подключений к движкам Stockfish для уменьшения накладных расходов.
    
    Атрибуты:
        _pool (queue.Queue): Очередь доступных движков
        _used_engines (set): Множество используемых движков
        _lock (threading.Lock): Блокировка для потокобезопасности
        _path (str): Путь к исполняемому файлу Stockfish
        _max_size (int): Максимальный размер пула
        _min_size (int): Минимальный размер пула
        _engine_config (dict): Конфигурация для новых движков
        _cleanup_thread (threading.Thread): Поток для очистки неиспользуемых движков
        _running (bool): Флаг работы пула
    """
    
    _instance = None
    _instance_lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        """Реализация singleton паттерна для пула движков."""
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super(StockfishEnginePool, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, path: Optional[str] = None, max_size: int = 10, min_size: int = 2, 
                 skill_level: int = 5, depth: int = 15):
        """
        Инициализация пула движков Stockfish.
        
        Параметры:
            path (str): Путь к исполняемому файлу Stockfish
            max_size (int): Максимальный размер пула (по умолчанию 10)
            min_size (int): Минимальный размер пула (по умолчанию 2)
            skill_level (int): Уровень сложности (0-20)
            depth (int): Глубина анализа
        """
        # Проверяем, инициализирован ли уже пул
        if hasattr(self, '_initialized') and self._initialized:
            return
            
        self._pool = queue.Queue()
        self._used_engines = set()
        self._lock = threading.Lock()
        self._max_size = max_size
        self._min_size = min_size
        self._engine_config = {
            'skill_level': skill_level,
            'depth': depth
        }
        self._running = True
        
        # Проверка наличия исполняемого файла Stockfish
        self._path = path
        if self._path is None:
            # Попробуем найти Stockfish в PATH
            self._path = shutil.which("stockfish")
            if self._path is None:
                print("⚠️  Stockfish не найден в PATH. Убедитесь, что он установлен.")
                print("💡 Решение:")
                print("   1. Скачайте Stockfish с https://stockfishchess.org/download/")
                print("   2. Распакуйте в папку и добавьте её в PATH")
                raise RuntimeError("Stockfish executable not found in PATH")
        
        # Проверим, что файл существует
        if not os.path.exists(self._path):
            raise RuntimeError(f"❌ Файл Stockfish не найден по пути: {self._path}")
        
        # Предварительно запускаем минимальное количество движков
        self._prepopulate_pool()
        
        # Запускаем поток очистки
        self._cleanup_thread = threading.Thread(target=self._cleanup_worker, daemon=True)
        self._cleanup_thread.start()
        
        # Помечаем как инициализированный
        self._initialized = True
        print(f"✅ Пул Stockfish движков инициализирован (размер: {min_size}-{max_size})")
    
    def _prepopulate_pool(self):
        """Предварительно заполняет пул минимальным количеством движков."""
        for _ in range(self._min_size):
            try:
                engine = self._create_engine()
                self._pool.put(engine)
            except Exception as e:
                print(f"⚠️  Не удалось создать движок для пула: {e}")
    
    def _create_engine(self) -> Stockfish:
        """
        Создает и настраивает новый движок Stockfish.
        
        Возвращает:
            Stockfish: Настроенный движок
        """
        try:
            engine = Stockfish(path=self._path)
            engine.set_skill_level(self._engine_config['skill_level'])
            engine.set_depth(self._engine_config['depth'])
            return engine
        except Exception as e:
            raise RuntimeError(f"❌ Не удалось создать Stockfish движок: {e}")
    
    def get_engine(self, timeout: float = 5.0) -> Optional[Stockfish]:
        """
        Получает доступный движок из пула.
        
        Параметры:
            timeout (float): Таймаут ожидания движка в секундах
            
        Возвращает:
            Stockfish: Доступный движок или None если таймаут
        """
        try:
            engine = self._pool.get(timeout=timeout)
            with self._lock:
                self._used_engines.add(id(engine))
            return engine
        except queue.Empty:
            # Если пул пуст, создаем новый движок если это возможно
            with self._lock:
                if len(self._used_engines) < self._max_size:
                    try:
                        engine = self._create_engine()
                        self._used_engines.add(id(engine))
                        return engine
                    except Exception as e:
                        print(f"⚠️  Не удалось создать новый движок: {e}")
            return None
        except Exception as e:
            print(f"⚠️  Ошибка при получении движка из пула: {e}")
            return None
    
    def return_engine(self, engine: Stockfish):
        """
        Возвращает движок в пул.
        
        Параметры:
            engine (Stockfish): Возвращаемый движок
        """
        if engine is None:
            return
            
        try:
            with self._lock:
                engine_id = id(engine)
                if engine_id in self._used_engines:
                    self._used_engines.remove(engine_id)
                    # Сбрасываем движок в начальное состояние
                    engine.set_fen_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
                
            # Возвращаем движок в пул если размер пула не превышен
            with self._lock:
                current_pool_size = self._pool.qsize() + len(self._used_engines)
                
            if current_pool_size <= self._max_size:
                self._pool.put(engine)
            else:
                # Если пул переполнен, закрываем движок
                try:
                    engine.__del__()  # Закрываем движок
                except:
                    pass
        except Exception as e:
            print(f"⚠️  Ошибка при возврате движка в пул: {e}")
    
    def _cleanup_worker(self):
        """Рабочий поток для очистки неиспользуемых движков."""
        while self._running:
            try:
                time.sleep(30)  # Проверяем каждые 30 секунд
                
                # Очищаем пул если он больше минимального размера
                with self._lock:
                    current_pool_size = self._pool.qsize()
                    
                while current_pool_size > self._min_size:
                    try:
                        engine = self._pool.get_nowait()
                        try:
                            engine.__del__()  # Закрываем движок
                        except:
                            pass
                        current_pool_size -= 1
                    except queue.Empty:
                        break
                        
            except Exception as e:
                if self._running:  # Только если пул еще работает
                    print(f"⚠️  Ошибка в потоке очистки пула: {e}")
    
    def get_pool_stats(self) -> Dict[str, Any]:
        """
        Получает статистику пула.
        
        Возвращает:
            Dict: Словарь со статистикой пула
        """
        with self._lock:
            return {
                'available_engines': self._pool.qsize(),
                'used_engines': len(self._used_engines),
                'max_size': self._max_size,
                'min_size': self._min_size
            }
    
    def resize_pool(self, new_min_size: int, new_max_size: int):
        """
        Изменяет размер пула.
        
        Параметры:
            new_min_size (int): Новый минимальный размер
            new_max_size (int): Новый максимальный размер
        """
        with self._lock:
            self._min_size = max(1, new_min_size)
            self._max_size = max(self._min_size, new_max_size)
    
    def cleanup(self):
        """Очищает пул и закрывает все движки."""
        self._running = False
        
        # Закрываем все движки в пуле
        while not self._pool.empty():
            try:
                engine = self._pool.get_nowait()
                try:
                    engine.__del__()  # Закрываем движок
                except:
                    pass
            except queue.Empty:
                break
        
        # Закрываем используемые движки
        with self._lock:
            self._used_engines.clear()
        
        print("✅ Пул Stockfish движков очищен")


# Глобальный пул движков
_stockfish_pool: Optional[StockfishEnginePool] = None
_pool_lock = threading.Lock()


def get_stockfish_pool(path: Optional[str] = None, max_size: int = 10, min_size: int = 2,
                      skill_level: int = 5, depth: int = 15) -> StockfishEnginePool:
    """
    Получает глобальный пул Stockfish движков (singleton).
    
    Параметры:
        path (str): Путь к исполняемому файлу Stockfish
        max_size (int): Максимальный размер пула
        min_size (int): Минимальный размер пула
        skill_level (int): Уровень сложности
        depth (int): Глубина анализа
        
    Возвращает:
        StockfishEnginePool: Глобальный пул движков
    """
    global _stockfish_pool
    
    with _pool_lock:
        if _stockfish_pool is None:
            _stockfish_pool = StockfishEnginePool(
                path=path, max_size=max_size, min_size=min_size,
                skill_level=skill_level, depth=depth
            )
        return _stockfish_pool


def cleanup_stockfish_pool():
    """Очищает глобальный пул Stockfish движков."""
    global _stockfish_pool
    
    with _pool_lock:
        if _stockfish_pool is not None:
            _stockfish_pool.cleanup()
            _stockfish_pool = None