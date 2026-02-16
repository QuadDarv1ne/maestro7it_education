"""
Система предиктивного кэширования
Анализирует паттерны использования и предзагружает данные
"""

import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from collections import defaultdict, deque
import threading


class AccessPattern:
    """Паттерн доступа к данным"""
    
    def __init__(self, key: str):
        self.key = key
        self.access_times = deque(maxlen=100)  # Последние 100 обращений
        self.access_count = 0
        self.last_access = None
        self.avg_interval = None
    
    def record_access(self):
        """Записать обращение"""
        now = time.time()
        self.access_times.append(now)
        self.access_count += 1
        
        if self.last_access:
            # Обновление среднего интервала
            interval = now - self.last_access
            if self.avg_interval is None:
                self.avg_interval = interval
            else:
                # Экспоненциальное скользящее среднее
                self.avg_interval = 0.7 * self.avg_interval + 0.3 * interval
        
        self.last_access = now
    
    def predict_next_access(self) -> Optional[float]:
        """Предсказать время следующего обращения"""
        if self.last_access and self.avg_interval:
            return self.last_access + self.avg_interval
        return None
    
    def get_frequency(self) -> float:
        """Получить частоту обращений (обращений в секунду)"""
        if len(self.access_times) < 2:
            return 0.0
        
        time_span = self.access_times[-1] - self.access_times[0]
        if time_span == 0:
            return 0.0
        
        return len(self.access_times) / time_span


class PredictiveCache:
    """Интеллектуальное кэширование с предсказанием"""
    
    def __init__(self, base_cache):
        """
        Args:
            base_cache: Базовый кэш (например, advanced_cache)
        """
        self.base_cache = base_cache
        self.patterns: Dict[str, AccessPattern] = {}
        self.preload_queue = deque(maxlen=100)
        self.preload_thread = None
        self.running = False
        
        # Статистика
        self.stats = {
            'predictions': 0,
            'preloads': 0,
            'hits_from_preload': 0,
            'misses': 0
        }
    
    def get(self, key: str, fetch_func: Optional[Callable] = None) -> Any:
        """
        Получить значение из кэша с отслеживанием паттерна
        
        Args:
            key: Ключ кэша
            fetch_func: Функция для получения данных при промахе
        """
        # Записываем паттерн доступа
        if key not in self.patterns:
            self.patterns[key] = AccessPattern(key)
        self.patterns[key].record_access()
        
        # Пытаемся получить из кэша
        value = self.base_cache.get(key)
        
        if value is not None:
            # Проверяем, был ли это результат предзагрузки
            if key in [item[0] for item in self.preload_queue]:
                self.stats['hits_from_preload'] += 1
            return value
        
        # Промах кэша
        self.stats['misses'] += 1
        
        if fetch_func:
            value = fetch_func()
            self.base_cache.set(key, value)
            return value
        
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Установить значение в кэш"""
        self.base_cache.set(key, value, ttl)
    
    def analyze_patterns(self) -> List[Dict[str, Any]]:
        """Анализ паттернов доступа"""
        now = time.time()
        predictions = []
        
        for key, pattern in self.patterns.items():
            # Пропускаем редко используемые ключи
            if pattern.access_count < 3:
                continue
            
            frequency = pattern.get_frequency()
            next_access = pattern.predict_next_access()
            
            if next_access and frequency > 0.01:  # Минимум 1 обращение в 100 секунд
                time_until_access = next_access - now
                
                # Если предсказываем обращение в ближайшие 60 секунд
                if 0 < time_until_access < 60:
                    predictions.append({
                        'key': key,
                        'predicted_time': next_access,
                        'time_until': time_until_access,
                        'frequency': frequency,
                        'confidence': min(pattern.access_count / 10, 1.0)
                    })
        
        # Сортируем по времени до предсказанного обращения
        predictions.sort(key=lambda x: x['time_until'])
        return predictions
    
    def preload_predicted(self, fetch_functions: Dict[str, Callable]):
        """
        Предзагрузка данных на основе предсказаний
        
        Args:
            fetch_functions: Словарь {key: функция_получения_данных}
        """
        predictions = self.analyze_patterns()
        self.stats['predictions'] = len(predictions)
        
        for pred in predictions[:10]:  # Топ-10 предсказаний
            key = pred['key']
            
            # Проверяем, есть ли уже в кэше
            if self.base_cache.get(key) is not None:
                continue
            
            # Проверяем, есть ли функция для получения данных
            if key in fetch_functions:
                try:
                    value = fetch_functions[key]()
                    self.base_cache.set(key, value)
                    self.preload_queue.append((key, time.time()))
                    self.stats['preloads'] += 1
                except Exception as e:
                    import logging
                    logging.error(f"Failed to preload {key}: {e}")
    
    def start_background_preload(self, fetch_functions: Dict[str, Callable], interval: int = 30):
        """
        Запустить фоновую предзагрузку
        
        Args:
            fetch_functions: Словарь функций для получения данных
            interval: Интервал проверки в секундах
        """
        if self.running:
            return
        
        self.running = True
        
        def preload_loop():
            while self.running:
                try:
                    self.preload_predicted(fetch_functions)
                except Exception as e:
                    import logging
                    logging.error(f"Error in preload loop: {e}")
                
                time.sleep(interval)
        
        self.preload_thread = threading.Thread(target=preload_loop, daemon=True)
        self.preload_thread.start()
    
    def stop_background_preload(self):
        """Остановить фоновую предзагрузку"""
        self.running = False
        if self.preload_thread:
            self.preload_thread.join(timeout=5)
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику"""
        total_accesses = sum(p.access_count for p in self.patterns.values())
        
        return {
            'total_patterns': len(self.patterns),
            'total_accesses': total_accesses,
            'predictions_made': self.stats['predictions'],
            'preloads_executed': self.stats['preloads'],
            'hits_from_preload': self.stats['hits_from_preload'],
            'cache_misses': self.stats['misses'],
            'preload_hit_rate': (
                self.stats['hits_from_preload'] / self.stats['preloads']
                if self.stats['preloads'] > 0 else 0
            ),
            'top_patterns': sorted(
                [
                    {
                        'key': key,
                        'access_count': pattern.access_count,
                        'frequency': round(pattern.get_frequency(), 4)
                    }
                    for key, pattern in self.patterns.items()
                ],
                key=lambda x: x['access_count'],
                reverse=True
            )[:10]
        }
    
    def clear_patterns(self, older_than_hours: int = 24):
        """Очистить старые паттерны"""
        now = time.time()
        cutoff = now - (older_than_hours * 3600)
        
        keys_to_remove = [
            key for key, pattern in self.patterns.items()
            if pattern.last_access and pattern.last_access < cutoff
        ]
        
        for key in keys_to_remove:
            del self.patterns[key]
        
        return len(keys_to_remove)


# Создание глобального экземпляра
def create_predictive_cache():
    """Создать предиктивный кэш"""
    try:
        from app.utils.advanced_cache import cache_manager
        return PredictiveCache(cache_manager)
    except ImportError:
        # Fallback на простой кэш
        from app.utils.cache import cache_service
        return PredictiveCache(cache_service)


predictive_cache = create_predictive_cache()  # Инициализация глобального экземпляра предиктивного кэша
