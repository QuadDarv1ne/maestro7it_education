"""
Health Check Routes для Simple HR
Endpoints для мониторинга состояния приложения
"""

from datetime import datetime
from flask import Blueprint, jsonify, current_app
from sqlalchemy import text
import psutil
import os

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Базовая проверка здоровья приложения.
    Возвращает 200 OK если приложение работает.
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'simple-hr',
        'version': '1.0.0'
    }), 200


@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """
    Проверка готовности приложения к обработке запросов.
    Проверяет подключение к БД, доступность файловой системы.
    """
    checks = {
        'database': check_database(),
        'filesystem': check_filesystem(),
        'memory': check_memory()
    }
    
    all_healthy = all(check['status'] == 'healthy' for check in checks.values())
    
    response = {
        'status': 'ready' if all_healthy else 'not_ready',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': checks
    }
    
    status_code = 200 if all_healthy else 503
    return jsonify(response), status_code


@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """
    Проверка жизнеспособности приложения (для Kubernetes).
    Должен отвечать быстро, без проверки внешних зависимостей.
    """
    return jsonify({
        'status': 'alive',
        'timestamp': datetime.utcnow().isoformat()
    }), 200


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
