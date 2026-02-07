# -*- coding: utf-8 -*-
"""
Middleware сжатия запросов/ответов для улучшения производительности
"""
import gzip
import logging
from flask import request, Response
from functools import wraps
import io
import time
from typing import Callable, Any

logger = logging.getLogger(__name__)

class CompressionMiddleware:
    """Middleware для сжатия HTTP запросов и ответов"""
    
    def __init__(self, app=None, compression_level=6):
        self.app = app
        self.compression_level = compression_level
        self.compression_stats = {
            'requests_compressed': 0,
            'responses_compressed': 0,
            'total_bytes_saved': 0,
            'compression_time': 0
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализирует middleware сжатия с Flask приложением"""
        self.app = app
        
        # Register middleware
        app.before_request(self.compress_request)
        app.after_request(self.compress_response)
        
        # Add to app context
        app.compression_middleware = self
    
    def compress_request(self):
        """Сжимает входящие данные запроса если они сжаты"""
        try:
            if request.content_encoding == 'gzip':
                start_time = time.time()
                
                # Decompress request data
                compressed_data = request.get_data()
                decompressed_data = gzip.decompress(compressed_data)
                
                # Replace request data
                request._cached_data = decompressed_data
                request._cached_json = None  # Clear cached JSON
                
                compression_time = time.time() - start_time
                self.compression_stats['requests_compressed'] += 1
                self.compression_stats['compression_time'] += compression_time
                
                logger.debug(f"Decompressed request: {len(compressed_data)} -> {len(decompressed_data)} bytes")
                
        except Exception as e:
            logger.warning(f"Error decompressing request: {e}")
    
    def compress_response(self, response: Response) -> Response:
        """Сжимает исходящие данные ответа если клиент поддерживает это"""
        try:
            # Check if client accepts gzip compression
            if 'gzip' not in request.headers.get('Accept-Encoding', ''):
                return response
            
            # Don't compress already compressed content
            if response.content_encoding:
                return response
            
            # Don't compress small responses (overhead not worth it)
            if len(response.get_data()) < 512:
                return response
            
            # Don't compress certain content types
            content_type = response.content_type or ''
            if any(ctype in content_type for ctype in [
                'image/', 'video/', 'audio/', 'application/zip', 
                'application/gzip', 'application/octet-stream'
            ]):
                return response
            
            start_time = time.time()
            
            # Compress response data
            original_data = response.get_data()
            compressed_data = gzip.compress(original_data, compresslevel=self.compression_level)
            
            # Only use compression if it actually saves space
            if len(compressed_data) < len(original_data) * 0.9:  # At least 10% saving
                response.set_data(compressed_data)
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Content-Length'] = len(compressed_data)
                response.headers['Vary'] = 'Accept-Encoding'
                
                # Update compression statistics
                bytes_saved = len(original_data) - len(compressed_data)
                self.compression_stats['responses_compressed'] += 1
                self.compression_stats['total_bytes_saved'] += bytes_saved
                
                compression_time = time.time() - start_time
                self.compression_stats['compression_time'] += compression_time
                
                logger.debug(f"Compressed response: {len(original_data)} -> {len(compressed_data)} bytes (saved {bytes_saved})")
            
        except Exception as e:
            logger.warning(f"Error compressing response: {e}")
        
        return response
    
    def get_compression_stats(self) -> dict:
        """Получает статистику сжатия"""
        return self.compression_stats.copy()

def compress_json_response(f: Callable) -> Callable:
    """
    Декоратор для включения сжатия для JSON ответов
    
    Usage:
        @app.route('/api/data')
        @compress_json_response
        def get_data():
            return jsonify(large_data_dict)
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        
        # Ensure response is JSON
        if hasattr(response, 'content_type') and 'application/json' in response.content_type:
            # Force compression for JSON responses
            request.headers.environ['HTTP_ACCEPT_ENCODING'] = 'gzip'
        
        return response
    return decorated_function

class BrotliCompressionMiddleware:
    """Альтернативное middleware с использованием сжатия Brotli (лучшее соотношение сжатия)"""
    
    def __init__(self, app=None, quality=4):
        self.app = app
        self.quality = quality
        self.stats = {
            'compressed_responses': 0,
            'total_bytes_saved': 0,
            'compression_time': 0
        }
        
        # Try to import brotli
        try:
            import brotli
            self.brotli = brotli
            self.brotli_available = True
        except ImportError:
            self.brotli = None
            self.brotli_available = False
            logger.warning("Сжатие Brotli недоступно. Установите пакет 'brotli' для лучшего сжатия.")
    
    def init_app(self, app):
        """Инициализирует middleware сжатия Brotli"""
        if not self.brotli_available:
            logger.warning("Пропуск инициализации middleware Brotli - brotli не установлен")
            return
            
        self.app = app
        app.before_request(self.handle_brotli_request)
        app.after_request(self.compress_brotli_response)
        app.brotli_compression = self
    
    def handle_brotli_request(self):
        """Обрабатывает сжатые Brotli входящие запросы"""
        try:
            if request.content_encoding == 'br' and self.brotli_available:
                compressed_data = request.get_data()
                decompressed_data = self.brotli.decompress(compressed_data)
                request._cached_data = decompressed_data
                request._cached_json = None
                logger.debug("Decompressed Brotli request")
        except Exception as e:
            logger.warning(f"Error decompressing Brotli request: {e}")
    
    def compress_brotli_response(self, response: Response) -> Response:
        """Сжимает ответ с использованием Brotli если клиент поддерживает это"""
        try:
            if not self.brotli_available:
                return response
                
            # Check client support
            if 'br' not in request.headers.get('Accept-Encoding', ''):
                return response
            
            # Skip if already encoded
            if response.content_encoding:
                return response
            
            # Skip small responses
            if len(response.get_data()) < 1024:
                return response
            
            # Skip binary content
            content_type = response.content_type or ''
            if any(ctype in content_type for ctype in [
                'image/', 'video/', 'audio/', 'application/'
            ]):
                return response
            
            start_time = time.time()
            original_data = response.get_data()
            
            # Compress with Brotli
            compressed_data = self.brotli.compress(
                original_data, 
                quality=self.quality,
                mode=self.brotli.MODE_TEXT  # Optimize for text content
            )
            
            # Use if compression saves space
            if len(compressed_data) < len(original_data) * 0.85:  # At least 15% saving
                response.set_data(compressed_data)
                response.headers['Content-Encoding'] = 'br'
                response.headers['Content-Length'] = len(compressed_data)
                response.headers['Vary'] = 'Accept-Encoding'
                
                bytes_saved = len(original_data) - len(compressed_data)
                self.stats['compressed_responses'] += 1
                self.stats['total_bytes_saved'] += bytes_saved
                
                compression_time = time.time() - start_time
                self.stats['compression_time'] += compression_time
                
                logger.debug(f"Brotli compressed: {len(original_data)} -> {len(compressed_data)} bytes")
        
        except Exception as e:
            logger.warning(f"Error in Brotli compression: {e}")
        
        return response

# Flask CLI commands for compression
def register_compression_commands(app):
    """Регистрирует CLI команды для мониторинга сжатия"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('compression-stats')
    @with_appcontext
    def show_compression_stats():
        """Показывает статистику сжатия"""
        if hasattr(app, 'compression_middleware'):
            stats = app.compression_middleware.get_compression_stats()
            click.echo("Gzip Compression Statistics:")
            for key, value in stats.items():
                click.echo(f"  {key}: {value}")
        else:
            click.echo("Compression middleware not initialized")
    
    @app.cli.command('enable-brotli')
    @with_appcontext
    def enable_brotli():
        """Включает сжатие Brotli (требуется пакет brotli)"""
        try:
            brotli_middleware = BrotliCompressionMiddleware()
            brotli_middleware.init_app(app)
            click.echo("Brotli compression enabled")
        except Exception as e:
            click.echo(f"Failed to enable Brotli: {e}")