# -*- coding: utf-8 -*-
"""
Оптимизация обслуживания статических файлов и доставки ресурсов
"""
import logging
import os
import hashlib
import gzip
from flask import Flask, send_from_directory, request, Response
from typing import Dict, Any, Optional
import time
from datetime import datetime, timedelta
import mimetypes
import threading
from collections import defaultdict

logger = logging.getLogger(__name__)

class StaticAssetOptimizer:
    """Оптимизирует обслуживание статических файлов и доставку ресурсов"""
    
    def __init__(self, app: Optional[Flask] = None):
        self.app = app
        self.asset_cache = {}
        self.compression_cache = {}
        self.stats = defaultdict(int)
        self.cache_lock = threading.Lock()
        
        # Asset optimization settings
        self.optimization_config = {
            'enable_compression': True,
            'enable_caching': True,
            'enable_etags': True,
            'compression_level': 6,
            'max_age': 31536000,  # 1 year
            'cache_control': 'public, immutable',
            'static_folder': 'static',
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Инициализирует оптимизатор статических ресурсов с Flask приложением"""
        self.app = app
        
        # Update configuration
        static_folder = app.static_folder or 'static'
        self.optimization_config['static_folder'] = static_folder
        
        # Register optimized static file handler
        self._register_static_handler(app)
        
        # Add to app context
        app.static_asset_optimizer = self
        
        logger.info(f"Static asset optimizer initialized for folder: {static_folder}")
    
    def _register_static_handler(self, app: Flask):
        """Регистрирует оптимизированный обработчик обслуживания статических файлов"""
        
        # Store original static handler
        original_send_static_file = app.send_static_file
        
        def optimized_send_static_file(filename: str) -> Response:
            """Оптимизированное обслуживание статических файлов с кэшированием и сжатием"""
            try:
                # Get file path
                static_folder = self.optimization_config['static_folder']
                file_path = os.path.join(static_folder, filename)
                
                # Check if file exists
                if not os.path.exists(file_path):
                    return original_send_static_file(filename)
                
                # Generate ETag
                etag = self._generate_etag(file_path)
                
                # Check If-None-Match header
                if request.if_none_match and etag in request.if_none_match:
                    response = Response(status=304)
                    response.headers['ETag'] = etag
                    return response
                
                # Check If-Modified-Since header
                if_modified_since = request.headers.get('If-Modified-Since')
                if if_modified_since:
                    try:
                        file_mtime = os.path.getmtime(file_path)
                        if_modified_since_time = time.mktime(
                            datetime.strptime(if_modified_since, '%a, %d %b %Y %H:%M:%S GMT').timetuple()
                        )
                        if file_mtime <= if_modified_since_time:
                            return Response(status=304)
                    except ValueError:
                        pass
                
                # Get file content with caching
                content = self._get_cached_file_content(file_path)
                if content is None:
                    return original_send_static_file(filename)
                
                # Determine content type
                content_type, _ = mimetypes.guess_type(filename)
                if not content_type:
                    content_type = 'application/octet-stream'
                
                # Check if client accepts compression
                accept_encoding = request.headers.get('Accept-Encoding', '')
                use_compression = (
                    self.optimization_config['enable_compression'] and
                    'gzip' in accept_encoding and
                    len(content) > 1024 and  # Only compress larger files
                    not content_type.startswith(('image/', 'video/', 'audio/'))
                )
                
                # Apply compression if beneficial
                if use_compression:
                    compressed_content = self._get_compressed_content(content, file_path)
                    if compressed_content and len(compressed_content) < len(content) * 0.9:
                        content = compressed_content
                        content_type += '; charset=gzip'
                
                # Create response
                response = Response(content, mimetype=content_type)
                
                # Add caching headers
                if self.optimization_config['enable_caching']:
                    response.headers['Cache-Control'] = self.optimization_config['cache_control']
                    response.headers['Expires'] = (datetime.utcnow() + timedelta(seconds=self.optimization_config['max_age'])).strftime('%a, %d %b %Y %H:%M:%S GMT')
                
                # Add ETag header
                if self.optimization_config['enable_etags']:
                    response.headers['ETag'] = etag
                
                # Add compression headers
                if use_compression and content != self._get_cached_file_content(file_path):
                    response.headers['Content-Encoding'] = 'gzip'
                    response.headers['Vary'] = 'Accept-Encoding'
                
                # Add last modified header
                file_mtime = os.path.getmtime(file_path)
                response.headers['Last-Modified'] = datetime.utcfromtimestamp(file_mtime).strftime('%a, %d %b %Y %H:%M:%S GMT')
                
                self.stats['files_served'] += 1
                logger.debug(f"Served static file: {filename} ({len(content)} bytes)")
                
                return response
                
            except Exception as e:
                logger.error(f"Error serving static file {filename}: {e}")
                return original_send_static_file(filename)
        
        # Replace Flask's static file handler
        app.send_static_file = optimized_send_static_file
    
    def _generate_etag(self, file_path: str) -> str:
        """Генерирует ETag для файла на основе хэша содержимого"""
        try:
            # Use cached ETag if available
            cache_key = f"etag:{file_path}"
            if cache_key in self.asset_cache:
                cached_etag, cache_time = self.asset_cache[cache_key]
                # Refresh ETag if file was modified
                if os.path.getmtime(file_path) <= cache_time:
                    return cached_etag
            
            # Generate new ETag
            with open(file_path, 'rb') as f:
                content = f.read()
                etag = hashlib.md5(content).hexdigest()
            
            # Cache ETag
            with self.cache_lock:
                self.asset_cache[cache_key] = (etag, time.time())
            
            return etag
        except Exception as e:
            logger.error(f"Error generating ETag for {file_path}: {e}")
            return f"error-{hash(file_path)}"
    
    def _get_cached_file_content(self, file_path: str) -> Optional[bytes]:
        """Получает содержимое файла с кэшированием"""
        try:
            # Check cache first
            cache_key = f"content:{file_path}"
            if cache_key in self.asset_cache:
                cached_content, cache_time = self.asset_cache[cache_key]
                # Refresh cache if file was modified
                if os.path.getmtime(file_path) <= cache_time:
                    self.stats['cache_hits'] += 1
                    return cached_content
            
            # Read file content
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Cache content
            with self.cache_lock:
                self.asset_cache[cache_key] = (content, time.time())
                # Keep cache size reasonable
                if len(self.asset_cache) > 1000:
                    # Remove oldest entries
                    oldest_keys = sorted(
                        [(k, v[1]) for k, v in self.asset_cache.items() if k.startswith('content:')],
                        key=lambda x: x[1]
                    )[:100]
                    for key, _ in oldest_keys:
                        self.asset_cache.pop(key, None)
            
            self.stats['cache_misses'] += 1
            return content
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def _get_compressed_content(self, content: bytes, file_path: str) -> Optional[bytes]:
        """Получает содержимое сжатое gzip с кэшированием"""
        try:
            # Check compression cache
            cache_key = f"compressed:{file_path}"
            if cache_key in self.compression_cache:
                return self.compression_cache[cache_key]
            
            # Compress content
            compressed = gzip.compress(content, compresslevel=self.optimization_config['compression_level'])
            
            # Cache compressed content
            with self.cache_lock:
                self.compression_cache[cache_key] = compressed
                # Keep compression cache size reasonable
                if len(self.compression_cache) > 500:
                    oldest_keys = sorted(
                        [(k, time.time()) for k in self.compression_cache.keys() if k.startswith('compressed:')],
                        key=lambda x: x[1]
                    )[:50]
                    for key, _ in oldest_keys:
                        self.compression_cache.pop(key, None)
            
            return compressed
            
        except Exception as e:
            logger.error(f"Error compressing content for {file_path}: {e}")
            return None
    
    def preload_critical_assets(self, asset_paths: list):
        """Предварительно загружает критические статические ресурсы в кэш"""
        def preload():
            start_time = time.time()
            loaded_count = 0
            
            for asset_path in asset_paths:
                try:
                    static_folder = self.optimization_config['static_folder']
                    full_path = os.path.join(static_folder, asset_path)
                    if os.path.exists(full_path):
                        self._get_cached_file_content(full_path)
                        loaded_count += 1
                except Exception as e:
                    logger.warning(f"Failed to preload asset {asset_path}: {e}")
            
            duration = time.time() - start_time
            logger.info(f"Preloaded {loaded_count}/{len(asset_paths)} assets in {duration:.2f}s")
        
        # Run in background thread
        thread = threading.Thread(target=preload, daemon=True)
        thread.start()
        return thread
    
    def get_asset_statistics(self) -> Dict[str, Any]:
        """Получает статистику обслуживания статических ресурсов"""
        with self.cache_lock:
            return {
                'files_served': self.stats['files_served'],
                'cache_hits': self.stats['cache_hits'],
                'cache_misses': self.stats['cache_misses'],
                'cache_hit_ratio': self.stats['cache_hits'] / max(self.stats['cache_hits'] + self.stats['cache_misses'], 1),
                'cached_assets': len([k for k in self.asset_cache.keys() if k.startswith('content:')]),
                'compressed_assets': len([k for k in self.compression_cache.keys() if k.startswith('compressed:')]),
                'cache_size_mb': sum(len(v[0]) for v in self.asset_cache.values() if isinstance(v[0], bytes)) / (1024 * 1024),
                'compression_cache_size_mb': sum(len(v) for v in self.compression_cache.values() if isinstance(v, bytes)) / (1024 * 1024)
            }
    
    def clear_asset_cache(self):
        """Очищает весь кэш ресурсов"""
        with self.cache_lock:
            # Keep ETags, clear content and compression caches
            self.asset_cache = {k: v for k, v in self.asset_cache.items() if k.startswith('etag:')}
            self.compression_cache.clear()
            self.stats['cache_cleared'] = self.stats.get('cache_cleared', 0) + 1
        logger.info("Static asset cache cleared")

class CDNManager:
    """Интеграция Content Delivery Network для статических ресурсов"""
    
    def __init__(self, app: Optional[Flask] = None):
        self.app = app
        self.cdn_config = {
            'enabled': False,
            'base_url': '',
            'asset_mapping': {}
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Инициализирует менеджер CDN с Flask приложением"""
        self.app = app
        
        # Load CDN configuration from app config
        cdn_config = app.config.get('CDN_CONFIG', {})
        self.cdn_config.update(cdn_config)
        
        # Add to app context
        app.cdn_manager = self
        
        if self.cdn_config['enabled']:
            logger.info(f"CDN enabled with base URL: {self.cdn_config['base_url']}")
    
    def get_asset_url(self, asset_path: str) -> str:
        """Получает URL ресурса CDN если доступен, иначе локальный URL"""
        if not self.cdn_config['enabled']:
            return f"/static/{asset_path}"
        
        # Check if asset is mapped to CDN
        if asset_path in self.cdn_config['asset_mapping']:
            return self.cdn_config['asset_mapping'][asset_path]
        
        # Use default CDN base URL
        return f"{self.cdn_config['base_url']}/{asset_path}"
    
    def add_asset_mapping(self, local_path: str, cdn_url: str):
        """Добавляет отображение для конкретного ресурса в URL CDN"""
        self.cdn_config['asset_mapping'][local_path] = cdn_url

# Global instances
static_asset_optimizer = StaticAssetOptimizer()
cdn_manager = CDNManager()

# Flask CLI commands
def register_static_asset_commands(app):
    """Регистрирует CLI команды для оптимизации статических ресурсов"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('asset-stats')
    @with_appcontext
    def show_asset_stats():
        """Показывает статистику обслуживания статических ресурсов"""
        if hasattr(app, 'static_asset_optimizer'):
            stats = app.static_asset_optimizer.get_asset_statistics()
            click.echo("Static Asset Statistics:")
            for key, value in stats.items():
                if isinstance(value, float):
                    click.echo(f"  {key}: {value:.2%}")
                else:
                    click.echo(f"  {key}: {value}")
        else:
            click.echo("Static asset optimizer not initialized")
    
    @app.cli.command('asset-cache-clear')
    @with_appcontext
    def clear_asset_cache():
        """Очищает кэш статических ресурсов"""
        if hasattr(app, 'static_asset_optimizer'):
            app.static_asset_optimizer.clear_asset_cache()
            click.echo("Static asset cache cleared")
        else:
            click.echo("Static asset optimizer not initialized")
    
    @app.cli.command('asset-preload')
    @click.argument('assets', nargs=-1)
    @with_appcontext
    def preload_assets(assets):
        """Предварительно загружает указанные статические ресурсы в кэш"""
        if hasattr(app, 'static_asset_optimizer') and assets:
            thread = app.static_asset_optimizer.preload_critical_assets(list(assets))
            click.echo(f"Preloading {len(assets)} assets in background")
        else:
            click.echo("No assets specified or optimizer not initialized")