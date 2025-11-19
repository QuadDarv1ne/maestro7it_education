"""
Health Check Routes и мониторинг состояния приложения.

Предоставляет endpoints для проверки здоровья приложения,
готовности и детальной диагностики.
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

import psutil
from flask import Blueprint, current_app, jsonify
from sqlalchemy import text

logger = logging.getLogger(__name__)

health_bp = Blueprint('health', __name__, url_prefix='/health')


class HealthChecker:
    """System health checker with detailed diagnostics."""

    def check_database(self) -> Dict[str, Any]:
        """Check database connectivity and performance."""
        try:
            from app import db

            start_time = time.time()
            db.session.execute(text('SELECT 1'))
            elapsed = time.time() - start_time

            return {
                'status': 'healthy',
                'response_time_ms': round(elapsed * 1000, 2),
                'timestamp': datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Database check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
            }

    def check_cache(self) -> Dict[str, Any]:
        """Check cache connectivity."""
        try:
            from app import cache

            start_time = time.time()
            test_key = '__health_check__'
            cache.set(test_key, 'ok', timeout=10)
            result = cache.get(test_key)
            elapsed = time.time() - start_time
            cache.delete(test_key)

            if result == 'ok':
                return {
                    'status': 'healthy',
                    'type': 'SimpleCache',
                    'response_time_ms': round(elapsed * 1000, 2),
                    'timestamp': datetime.utcnow().isoformat(),
                }
            else:
                return {
                    'status': 'degraded',
                    'error': 'Cache read-write failed',
                    'timestamp': datetime.utcnow().isoformat(),
                }

        except Exception as e:
            logger.warning(f"Cache check failed: {str(e)}")
            return {
                'status': 'degraded',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
            }

    def check_filesystem(self) -> Dict[str, Any]:
        """Check filesystem accessibility."""
        try:
            required_dirs = ['logs', 'uploads', 'instance']

            for dir_name in required_dirs:
                dir_path = os.path.join(current_app.root_path, '..', dir_name)
                if not os.path.exists(dir_path):
                    return {
                        'status': 'unhealthy',
                        'error': f'Required directory not found: {dir_name}',
                    }

                if not os.access(dir_path, os.W_OK):
                    return {
                        'status': 'unhealthy',
                        'error': f'Directory not writable: {dir_name}',
                    }

            return {
                'status': 'healthy',
                'message': 'Filesystem is accessible',
                'timestamp': datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Filesystem check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
            }

    def check_memory(self) -> Dict[str, Any]:
        """Check memory usage."""
        try:
            memory = psutil.virtual_memory()
            percent = memory.percent

            if percent > 90:
                status = 'unhealthy'
            elif percent > 75:
                status = 'degraded'
            else:
                status = 'healthy'

            return {
                'status': status,
                'percent': percent,
                'available_mb': round(memory.available / 1024 / 1024, 2),
                'total_mb': round(memory.total / 1024 / 1024, 2),
                'timestamp': datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.warning(f"Memory check failed: {str(e)}")
            return {
                'status': 'unknown',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat(),
            }

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health."""
        database = self.check_database()
        cache = self.check_cache()
        filesystem = self.check_filesystem()
        memory = self.check_memory()

        dependencies = {
            'database': database,
            'cache': cache,
            'filesystem': filesystem,
            'memory': memory,
        }

        statuses = [dep.get('status') for dep in dependencies.values()]

        if all(s == 'healthy' for s in statuses):
            overall_status = 'healthy'
        elif any(s == 'unhealthy' for s in statuses):
            overall_status = 'unhealthy'
        else:
            overall_status = 'degraded'

        return {
            'status': overall_status,
            'timestamp': datetime.utcnow().isoformat(),
            'dependencies': dependencies,
        }


_health_checker = HealthChecker()


@health_bp.route('', methods=['GET'])
def health_check() -> Tuple[Any, int]:
    """
    Базовая проверка здоровья приложения.

    Returns:
        JSON response with status code.
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'simple-hr',
        'version': '2.4'
    }), 200
@health_bp.route('/ready', methods=['GET'])
def readiness_check() -> Tuple[Any, int]:
    """
    Проверка готовности приложения к обработке запросов.

    Returns:
        JSON response with status code.
    """
    checks = {
        'database': _health_checker.check_database(),
        'filesystem': _health_checker.check_filesystem(),
        'memory': _health_checker.check_memory(),
    }

    all_healthy = all(
        check.get('status') == 'healthy' for check in checks.values()
    )

    response = {
        'status': 'ready' if all_healthy else 'not_ready',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': checks,
    }

    status_code = 200 if all_healthy else 503
    return jsonify(response), status_code


@health_bp.route('/live', methods=['GET'])
def liveness_check() -> Tuple[Any, int]:
    """
    Проверка жизнеспособности приложения (для Kubernetes).

    Returns:
        JSON response with status code.
    """
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat(),
    }), 200


@health_bp.route('/deep', methods=['GET'])
def deep_health() -> Tuple[Any, int]:
    """
    Глубокая проверка с детальной диагностикой.

    Returns:
        JSON response with detailed health information.
    """
    try:
        health_status = _health_checker.get_system_health()
        return jsonify(health_status), 200

    except Exception as e:
        logger.error(f"Deep health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
        }), 503


@health_bp.route('/ready/db', methods=['GET'])
def database_readiness() -> Tuple[Any, int]:
    """
    Проверка готовности базы данных.

    Returns:
        JSON response with database status.
    """
    db_status = _health_checker.check_database()

    status_code = 200 if db_status['status'] == 'healthy' else 503
    return jsonify(db_status), status_code


@health_bp.route('/ready/cache', methods=['GET'])
def cache_readiness() -> Tuple[Any, int]:
    """
    Проверка готовности кэша.

    Returns:
        JSON response with cache status.
    """
    cache_status = _health_checker.check_cache()

    status_code = 200 if cache_status['status'] == 'healthy' else 503
    return jsonify(cache_status), status_code


@health_bp.route('/metrics', methods=['GET'])
def metrics() -> Tuple[Any, int]:
    """
    Метрики приложения для мониторинга.

    Returns:
        JSON response with metrics.
    """
    try:
        process = psutil.Process()

        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'process': {
                'pid': process.pid,
                'cpu_percent': process.cpu_percent(interval=0.1),
                'memory_mb': round(process.memory_info().rss / 1024 / 1024, 2),
                'threads': process.num_threads(),
                'uptime_seconds': (
                    datetime.now()
                    - datetime.fromtimestamp(process.create_time())
                ).total_seconds(),
            },
            'system': {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
            },
        }), 200

    except Exception as e:
        logger.error(f"Metrics collection failed: {str(e)}")
        return jsonify({
            'error': 'Failed to collect metrics',
            'message': str(e),
        }), 500


def check_database():
    """Проверка подключения к базе данных"""
    try:
        from app import db
        # Простой запрос для проверки соединения
        db.session.execute(text('SELECT 1'))
        return {
            'status': 'healthy',
            'message': 'Database connection is working'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'message': f'Database connection failed: {str(e)}'
        }


def check_filesystem():
    """Проверка доступности файловой системы"""
    try:
        # Проверяем доступность критичных директорий
        required_dirs = ['logs', 'uploads', 'instance']
        
        for dir_name in required_dirs:
            dir_path = os.path.join(current_app.root_path, '..', dir_name)
            if not os.path.exists(dir_path):
                return {
                    'status': 'unhealthy',
                    'message': f'Required directory not found: {dir_name}'
                }
            
            # Проверяем права на запись
            if not os.access(dir_path, os.W_OK):
                return {
                    'status': 'unhealthy',
                    'message': f'Directory not writable: {dir_name}'
                }
        
        return {
            'status': 'healthy',
            'message': 'Filesystem is accessible'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'message': f'Filesystem check failed: {str(e)}'
        }


def check_memory():
    """Проверка использования памяти"""
    try:
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Предупреждение если использовано >90% памяти
        if memory_percent > 90:
            status = 'unhealthy'
            message = f'High memory usage: {memory_percent}%'
        elif memory_percent > 75:
            status = 'degraded'
            message = f'Memory usage warning: {memory_percent}%'
        else:
            status = 'healthy'
            message = f'Memory usage normal: {memory_percent}%'
        
        return {
            'status': status,
            'message': message,
            'details': {
                'percent': memory_percent,
                'available_mb': round(memory.available / 1024 / 1024, 2),
                'total_mb': round(memory.total / 1024 / 1024, 2)
            }
        }
    except Exception as e:
        return {
            'status': 'unknown',
            'message': f'Memory check failed: {str(e)}'
        }


@health_bp.route('/health/metrics', methods=['GET'])
def metrics():
    """
    Метрики приложения для мониторинга.
    Возвращает информацию о процессе, памяти, диске.
    """
    try:
        process = psutil.Process()
        
        return jsonify({
            'timestamp': datetime.utcnow().isoformat(),
            'process': {
                'pid': process.pid,
                'cpu_percent': process.cpu_percent(interval=0.1),
                'memory_mb': round(process.memory_info().rss / 1024 / 1024, 2),
                'threads': process.num_threads(),
                'uptime_seconds': (datetime.now() - datetime.fromtimestamp(process.create_time())).total_seconds()
            },
            'system': {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent
            }
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'Failed to collect metrics',
            'message': str(e)
        }), 500