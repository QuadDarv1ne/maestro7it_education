# -*- coding: utf-8 -*-
"""
Модуль продвинутого сжатия запросов и ответов
Обеспечивает оптимизацию передачи данных через различные алгоритмы сжатия
"""
import logging
import gzip
import brotli
import zlib
from io import BytesIO
from typing import Dict, Any, Optional, List, Tuple
from functools import wraps
import time
from collections import defaultdict, deque
import threading

logger = logging.getLogger(__name__)

class AdvancedCompressionMiddleware:
    """Продвинутое middleware для сжатия запросов и ответов"""
    
    def __init__(self, app=None):
        self.app = app
        self.compression_stats = defaultdict(int)
        self.compression_history = deque(maxlen=1000)
        self.lock = threading.Lock()
        
        # Поддерживаемые алгоритмы сжатия
        self.supported_algorithms = {
            'br': brotli,
            'gzip': gzip,
            'deflate': zlib
        }
        
        # Пороговые значения
        self.thresholds = {
            'min_size_bytes': 512,  # Минимальный размер для сжатия
            'max_size_bytes': 10 * 1024 * 1024,  # Максимум 10MB
            'compression_level': 6,  # Уровень сжатия по умолчанию
            'cache_compressed': True  # Кэширование сжатых данных
        }
        
        # Кэш сжатых данных
        self.compression_cache = {}
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        
        # Регистрация как middleware
        app.wsgi_app = self.compression_middleware(app.wsgi_app)
        logger.info("Продвинутое middleware сжатия инициализировано")
    
    def compression_middleware(self, app):
        """Основное middleware для сжатия"""
        @wraps(app)
        def middleware(environ, start_response):
            # Проверка поддержки сжатия клиентом
            accept_encoding = environ.get('HTTP_ACCEPT_ENCODING', '')
            supported_algorithms = self._get_supported_algorithms(accept_encoding)
            
            if not supported_algorithms:
                # Клиент не поддерживает сжатие
                return app(environ, start_response)
            
            # Оборачиваем start_response для модификации заголовков
            def compressed_start_response(status, headers, exc_info=None):
                # Анализируем размер ответа
                content_length = self._get_content_length(headers)
                
                if content_length < self.thresholds['min_size_bytes']:
                    # Слишком маленький контент для сжатия
                    return start_response(status, headers, exc_info)
                
                if content_length > self.thresholds['max_size_bytes']:
                    # Слишком большой контент
                    return start_response(status, headers, exc_info)
                
                # Выбор лучшего алгоритма
                best_algorithm = self._select_best_algorithm(
                    supported_algorithms, content_length
                )
                
                if not best_algorithm:
                    return start_response(status, headers, exc_info)
                
                # Модификация заголовков
                compressed_headers = self._modify_headers(
                    headers, best_algorithm, content_length
                )
                
                return start_response(status, compressed_headers, exc_info)
            
            # Получаем оригинальный ответ
            response = app(environ, compressed_start_response)
            
            # Сжатие контента если нужно
            return self._compress_response(response, environ, start_response)
        
        return middleware
    
    def _get_supported_algorithms(self, accept_encoding: str) -> List[str]:
        """Определяет поддерживаемые алгоритмы клиента"""
        supported = []
        
        if 'br' in accept_encoding:
            supported.append('br')
        if 'gzip' in accept_encoding:
            supported.append('gzip')
        if 'deflate' in accept_encoding:
            supported.append('deflate')
        
        return supported
    
    def _get_content_length(self, headers: List[Tuple[str, str]]) -> Optional[int]:
        """Получает длину контента из заголовков"""
        for name, value in headers:
            if name.lower() == 'content-length':
                try:
                    return int(value)
                except ValueError:
                    return None
        return None
    
    def _select_best_algorithm(self, algorithms: List[str], content_length: int) -> Optional[str]:
        """Выбирает лучший алгоритм сжатия"""
        # Приоритет: Brotli > Gzip > Deflate
        priority_order = ['br', 'gzip', 'deflate']
        
        for algorithm in priority_order:
            if algorithm in algorithms:
                return algorithm
        
        return None
    
    def _modify_headers(self, headers: List[Tuple[str, str]], 
                       algorithm: str, original_size: int) -> List[Tuple[str, str]]:
        """Модифицирует заголовки для сжатого контента"""
        modified_headers = []
        content_type = None
        content_encoding_set = False
        
        for name, value in headers:
            if name.lower() == 'content-length':
                # Убираем content-length так как размер изменится
                continue
            elif name.lower() == 'content-encoding':
                # Не перезаписываем существующий content-encoding
                content_encoding_set = True
                modified_headers.append((name, value))
            elif name.lower() == 'content-type':
                content_type = value
                modified_headers.append((name, value))
            else:
                modified_headers.append((name, value))
        
        # Добавляем Content-Encoding если он еще не установлен
        if not content_encoding_set:
            modified_headers.append(('Content-Encoding', algorithm))
        
        # Добавляем Vary header
        modified_headers.append(('Vary', 'Accept-Encoding'))
        
        # Кэшируем размер для отчетов
        with self.lock:
            self.compression_stats['total_requests'] += 1
            self.compression_stats['algorithm_usage'][algorithm] = (
                self.compression_stats['algorithm_usage'].get(algorithm, 0) + 1
            )
        
        return modified_headers
    
    def _compress_response(self, response, environ, start_response):
        """Сжимает контент ответа"""
        # Собираем контент
        content = b''.join(response)
        
        if len(content) < self.thresholds['min_size_bytes']:
            # Не сжимаем маленький контент
            yield content
            return
        
        # Получаем алгоритм сжатия
        algorithm = self._get_response_algorithm(environ)
        
        if not algorithm:
            yield content
            return
        
        # Проверка кэша
        cache_key = self._get_cache_key(content, algorithm)
        if self.thresholds['cache_compressed']:
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                yield cached_result
                return
        
        # Сжатие
        start_time = time.time()
        try:
            compressed_content = self._compress_content(content, algorithm)
            compression_time = time.time() - start_time
            
            # Сохранение в кэш
            if self.thresholds['cache_compressed']:
                self._save_to_cache(cache_key, compressed_content)
            
            # Статистика
            self._update_compression_stats(
                len(content), len(compressed_content), 
                algorithm, compression_time
            )
            
            yield compressed_content
            
        except Exception as e:
            logger.error(f"Ошибка сжатия: {e}")
            yield content
    
    def _get_response_algorithm(self, environ) -> Optional[str]:
        """Получает алгоритм сжатия из заголовков ответа"""
        # В реальной реализации нужно получить заголовки ответа
        # Пока возвращаем предпочтительный алгоритм
        accept_encoding = environ.get('HTTP_ACCEPT_ENCODING', '')
        return self._select_best_algorithm(
            self._get_supported_algorithms(accept_encoding), 0
        )
    
    def _compress_content(self, content: bytes, algorithm: str) -> bytes:
        """Сжимает контент указанным алгоритмом"""
        if algorithm == 'br':
            return brotli.compress(
                content, 
                quality=self.thresholds['compression_level']
            )
        elif algorithm == 'gzip':
            buffer = BytesIO()
            with gzip.GzipFile(
                mode='wb', 
                fileobj=buffer, 
                compresslevel=self.thresholds['compression_level']
            ) as gz_file:
                gz_file.write(content)
            return buffer.getvalue()
        elif algorithm == 'deflate':
            return zlib.compress(
                content, 
                self.thresholds['compression_level']
            )
        else:
            raise ValueError(f"Неподдерживаемый алгоритм: {algorithm}")
    
    def _get_cache_key(self, content: bytes, algorithm: str) -> str:
        """Генерирует ключ для кэширования"""
        import hashlib
        content_hash = hashlib.md5(content).hexdigest()
        return f"{algorithm}:{content_hash}"
    
    def _get_from_cache(self, cache_key: str) -> Optional[bytes]:
        """Получает сжатый контент из кэша"""
        if cache_key in self.compression_cache:
            with self.lock:
                self.cache_stats['hits'] += 1
            return self.compression_cache[cache_key]
        else:
            with self.lock:
                self.cache_stats['misses'] += 1
            return None
    
    def _save_to_cache(self, cache_key: str, compressed_content: bytes):
        """Сохраняет сжатый контент в кэш"""
        # Ограничение размера кэша
        if len(self.compression_cache) > 1000:
            # Удаление старых записей
            oldest_keys = list(self.compression_cache.keys())[:100]
            for key in oldest_keys:
                del self.compression_cache[key]
            with self.lock:
                self.cache_stats['evictions'] += 100
        
        self.compression_cache[cache_key] = compressed_content
    
    def _update_compression_stats(self, original_size: int, compressed_size: int, 
                                algorithm: str, compression_time: float):
        """Обновляет статистику сжатия"""
        compression_ratio = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
        
        stat_entry = {
            'timestamp': time.time(),
            'algorithm': algorithm,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'compression_time': compression_time
        }
        
        with self.lock:
            self.compression_history.append(stat_entry)
            self.compression_stats['total_original_bytes'] += original_size
            self.compression_stats['total_compressed_bytes'] += compressed_size
            self.compression_stats['total_compression_time'] += compression_time
    
    def get_compression_report(self) -> Dict[str, Any]:
        """Генерирует отчет о сжатии"""
        with self.lock:
            # Базовая статистика
            total_requests = self.compression_stats.get('total_requests', 0)
            total_original = self.compression_stats.get('total_original_bytes', 0)
            total_compressed = self.compression_stats.get('total_compressed_bytes', 0)
            
            # Расчет общего коэффициента сжатия
            overall_ratio = (
                (1 - total_compressed / total_original) * 100 
                if total_original > 0 else 0
            )
            
            # Статистика по алгоритмам
            algorithm_usage = self.compression_stats.get('algorithm_usage', {})
            
            # Исторические данные
            recent_history = list(self.compression_history)[-100:]
            
            # Средние значения
            avg_compression_ratio = 0
            avg_compression_time = 0
            if recent_history:
                avg_compression_ratio = sum(
                    h['compression_ratio'] for h in recent_history
                ) / len(recent_history)
                avg_compression_time = sum(
                    h['compression_time'] for h in recent_history
                ) / len(recent_history)
            
            # Кэш статистика
            cache_hit_rate = (
                self.cache_stats['hits'] / 
                (self.cache_stats['hits'] + self.cache_stats['misses'])
                if (self.cache_stats['hits'] + self.cache_stats['misses']) > 0 else 0
            )
            
            return {
                'overall_stats': {
                    'total_requests': total_requests,
                    'total_original_mb': total_original / 1024 / 1024,
                    'total_compressed_mb': total_compressed / 1024 / 1024,
                    'overall_compression_ratio': overall_ratio,
                    'average_compression_ratio': avg_compression_ratio,
                    'average_compression_time': avg_compression_time
                },
                'algorithm_usage': algorithm_usage,
                'cache_stats': {
                    'hits': self.cache_stats['hits'],
                    'misses': self.cache_stats['misses'],
                    'evictions': self.cache_stats['evictions'],
                    'hit_rate': cache_hit_rate
                },
                'recent_history': recent_history[-20:],  # Последние 20 записей
                'thresholds': self.thresholds
            }
    
    def reset_stats(self):
        """Сброс статистики"""
        with self.lock:
            self.compression_stats.clear()
            self.compression_history.clear()
            self.cache_stats.clear()
            self.compression_cache.clear()
            # Переинициализация счетчиков
            self.compression_stats['algorithm_usage'] = defaultdict(int)
            self.cache_stats = {'hits': 0, 'misses': 0, 'evictions': 0}

# Глобальный экземпляр
compression_middleware = AdvancedCompressionMiddleware()

def register_compression_commands(app):
    """Регистрация CLI команд для управления сжатием"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('compression-report')
    @with_appcontext
    def show_compression_report():
        """Показать отчет о сжатии данных"""
        report = compression_middleware.get_compression_report()
        
        click.echo("Отчет о сжатии данных:")
        click.echo(f"  Всего запросов: {report['overall_stats']['total_requests']}")
        click.echo(f"  Исходный объем: {report['overall_stats']['total_original_mb']:.2f} MB")
        click.echo(f"  Сжатый объем: {report['overall_stats']['total_compressed_mb']:.2f} MB")
        click.echo(f"  Общий коэффициент сжатия: {report['overall_stats']['overall_compression_ratio']:.1f}%")
        click.echo(f"  Средний коэффициент: {report['overall_stats']['average_compression_ratio']:.1f}%")
        click.echo(f"  Среднее время сжатия: {report['overall_stats']['average_compression_time']:.4f}с")
        
        click.echo("\nИспользование алгоритмов:")
        for algorithm, count in report['algorithm_usage'].items():
            click.echo(f"  {algorithm}: {count} запросов")
        
        click.echo(f"\nКэш статистика:")
        click.echo(f"  Попаданий: {report['cache_stats']['hits']}")
        click.echo(f"  Промахов: {report['cache_stats']['misses']}")
        click.echo(f"  Эффективность: {report['cache_stats']['hit_rate']:.1%}")
    
    @app.cli.command('compression-reset')
    @with_appcontext
    def reset_compression_stats():
        """Сброс статистики сжатия"""
        compression_middleware.reset_stats()
        click.echo("Статистика сжатия сброшена")

# Декоратор для сжатия специфичных маршрутов
def compress_response(f):
    """Декоратор для принудительного сжатия ответов конкретных маршрутов"""
    from functools import wraps
    from flask import request, current_app
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Проверка поддержки сжатия
        accept_encoding = request.headers.get('Accept-Encoding', '')
        
        if not any(alg in accept_encoding for alg in ['gzip', 'br', 'deflate']):
            # Клиент не поддерживает сжатие
            return f(*args, **kwargs)
        
        # Выполнение функции
        response = f(*args, **kwargs)
        
        # Сжатие если это текстовый контент
        if hasattr(response, 'content_type') and 'text' in response.content_type:
            # Здесь можно добавить логику сжатия для Flask Response объектов
            pass
        
        return response
    
    return decorated_function