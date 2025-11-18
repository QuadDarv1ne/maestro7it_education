"""
Утилиты для мониторинга здоровья приложения
"""
from flask import jsonify
from app import db
from datetime import datetime
import psutil
import os

def get_system_health():
    """Получить информацию о состоянии системы"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        return {
            'cpu_usage': cpu_percent,
            'memory_usage': memory_percent,
            'disk_usage': disk_percent,
            'status': 'healthy' if cpu_percent < 80 and memory_percent < 80 else 'warning'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }


def get_database_health():
    """Проверить состояние подключения к базе данных"""
    try:
        # Простой запрос для проверки соединения
        db.session.execute('SELECT 1')
        return {
            'status': 'healthy',
            'message': 'Database connection is working'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Database connection failed: {str(e)}'
        }


def get_application_health():
    """Получить общее состояние приложения"""
    system_health = get_system_health()
    db_health = get_database_health()
    
    overall_status = 'healthy'
    if system_health.get('status') == 'error' or db_health.get('status') == 'error':
        overall_status = 'error'
    elif system_health.get('status') == 'warning':
        overall_status = 'warning'
    
    return {
        'status': overall_status,
        'timestamp': datetime.utcnow().isoformat(),
        'system': system_health,
        'database': db_health,
        'version': '2.0',
        'uptime': get_uptime()
    }


def get_uptime():
    """Получить время работы приложения"""
    try:
        process = psutil.Process(os.getpid())
        create_time = process.create_time()
        uptime_seconds = datetime.now().timestamp() - create_time
        
        # Конвертировать в читаемый формат
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        return f"{days}d {hours}h {minutes}m"
    except Exception:
        return "Unknown"


def create_health_check_blueprint():
    """Создать blueprint для health check endpoints"""
    from flask import Blueprint
    
    bp = Blueprint('health', __name__, url_prefix='/health')
    
    @bp.route('/')
    def health_check():
        """Основной health check endpoint"""
        health = get_application_health()
        status_code = 200 if health['status'] == 'healthy' else 503
        return jsonify(health), status_code
    
    @bp.route('/system')
    def system_health():
        """Health check только системных ресурсов"""
        health = get_system_health()
        return jsonify(health)
    
    @bp.route('/database')
    def database_health():
        """Health check только базы данных"""
        health = get_database_health()
        status_code = 200 if health['status'] == 'healthy' else 503
        return jsonify(health), status_code
    
    @bp.route('/ping')
    def ping():
        """Простой ping endpoint"""
        return jsonify({'status': 'ok', 'message': 'pong'}), 200
    
    return bp
