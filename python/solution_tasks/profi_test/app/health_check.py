"""
Расширенные endpoints проверки состояния с комплексным мониторингом системы
"""
from flask import Blueprint, jsonify, current_app
from flask_login import login_required, current_user
import psutil
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Any

logger = logging.getLogger(__name__)

health_api = Blueprint('health_api', __name__)

@health_api.route('/health')
def basic_health_check():
    """Базовый endpoint проверки состояния"""
    try:
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'services': {}
        }
        
        # Проверка базы данных
        try:
            from app import db
            db.session.execute('SELECT 1')
            health_status['services']['database'] = 'healthy'
        except Exception as e:
            health_status['services']['database'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'degraded'
        
        # Проверка кэша
        try:
            from app import cache
            cache.set('health_check', 'ok', timeout=1)
            cache.get('health_check')
            health_status['services']['cache'] = 'healthy'
        except Exception as e:
            health_status['services']['cache'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'degraded'
        
        # Проверка менеджера кэша Redis
        try:
            from app import redis_cache
            if redis_cache.redis_available:
                redis_cache.set('health_check', 'ok', timeout=1)
                redis_cache.get('health_check')
                health_status['services']['redis_cache'] = 'healthy'
            else:
                health_status['services']['redis_cache'] = 'unavailable'
        except Exception as e:
            health_status['services']['redis_cache'] = f'unhealthy: {str(e)}'
            health_status['status'] = 'degraded'
        
        return jsonify(health_status), 200 if health_status['status'] == 'healthy' else 503
        
    except Exception as e:
        logger.error(f"Проверка состояния не удалась: {e}")
        return jsonify({
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@health_api.route('/health/detailed')
@login_required
def detailed_health_check():
    """Подробная проверка состояния с системными метриками (только для админов)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    try:
        health_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'system': _get_system_metrics(),
            'application': _get_application_metrics(),
            'database': _get_database_metrics(),
            'cache': _get_cache_metrics(),
            'performance': _get_performance_metrics()
        }
        
        # Определение общего состояния
        health_data['overall_status'] = _calculate_overall_status(health_data)
        
        return jsonify(health_data)
        
    except Exception as e:
        logger.error(f"Подробная проверка состояния не удалась: {e}")
        return jsonify({'error': str(e)}), 500

@health_api.route('/health/services')
@login_required
def services_health():
    """Проверка состояния отдельных сервисов"""
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    services = {}
    
    # Сервис базы данных
    services['database'] = _check_database_service()
    
    # Сервисы кэша
    services['cache'] = _check_cache_service()
    services['redis_cache'] = _check_redis_cache_service()
    
    # Внешние сервисы
    services['external_apis'] = _check_external_services()
    
    # Фоновые задачи
    services['celery'] = _check_celery_service()
    
    return jsonify(services)

@health_api.route('/health/alerts')
@login_required
def health_alerts():
    """Получение текущих алертов состояния"""
    if not current_user.is_admin:
        return jsonify({'error': 'Доступ запрещен'}), 403
    
    try:
        from app.system_monitoring import system_monitor
        health_status = system_monitor.get_system_health()
        return jsonify({
            'alerts': health_status.get('alerts', []),
            'timestamp': health_status.get('timestamp')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def _get_system_metrics() -> Dict[str, Any]:
    """Получение системных метрик"""
    try:
        return {
            'cpu': {
                'percent': psutil.cpu_percent(interval=1),
                'count': psutil.cpu_count(),
                'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
            },
            'memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent,
                'used': psutil.virtual_memory().used
            },
            'disk': {
                'total': psutil.disk_usage('/').total,
                'used': psutil.disk_usage('/').used,
                'free': psutil.disk_usage('/').free,
                'percent': psutil.disk_usage('/').percent
            },
            'network': {
                'connections': len(psutil.net_connections()),
                'io_counters': dict(psutil.net_io_counters()._asdict()) if hasattr(psutil, 'net_io_counters') else None
            }
        }
    except Exception as e:
        logger.error(f"Ошибка получения системных метрик: {e}")
        return {'error': str(e)}

def _get_application_metrics() -> Dict[str, Any]:
    """Получение метрик приложения"""
    try:
        from app import db
        
        # Получение количества пользователей и результатов тестов
        user_count = db.session.query(db.func.count('user.id')).scalar() or 0
        test_count = db.session.query(db.func.count('test_result.id')).scalar() or 0
        
        return {
            'users': {
                'total': user_count,
                'active_today': 0,  # Требуется дополнительное отслеживание
                'new_today': 0      # Требуется дополнительное отслеживание
            },
            'test_results': {
                'total': test_count,
                'completed_today': 0  # Требуется дополнительное отслеживание
            },
            'uptime': _get_application_uptime()
        }
    except Exception as e:
        logger.error(f"Ошибка получения метрик приложения: {e}")
        return {'error': str(e)}

def _get_database_metrics() -> Dict[str, Any]:
    """Получение метрик базы данных"""
    try:
        from app import db
        
        # Получение размеров таблиц и количества строк
        table_stats = {}
        tables = ['user', 'test_result', 'notification', 'comment']
        
        for table in tables:
            try:
                count = db.session.query(db.func.count(f'{table}.id')).scalar()
                table_stats[table] = {'row_count': count or 0}
            except Exception:
                table_stats[table] = {'error': 'Не удалось получить количество'}
        
        return {
            'status': 'healthy',
            'tables': table_stats,
            'connection_pool': _get_db_pool_stats()
        }
    except Exception as e:
        logger.error(f"Ошибка получения метрик базы данных: {e}")
        return {'status': 'error', 'error': str(e)}

def _get_cache_metrics() -> Dict[str, Any]:
    """Получение метрик кэша"""
    try:
        from app import cache, redis_cache
        
        metrics = {
            'flask_cache': {
                'status': 'available' if cache else 'unavailable'
            },
            'redis_cache': {
                'status': 'healthy' if redis_cache.redis_available else 'unavailable',
                'stats': redis_cache.get_stats() if redis_cache.redis_available else {}
            }
        }
        
        return metrics
    except Exception as e:
        logger.error(f"Ошибка получения метрик кэша: {e}")
        return {'error': str(e)}

def _get_performance_metrics() -> Dict[str, Any]:
    """Получение метрик производительности"""
    try:
        from app.performance import performance_monitor
        
        perf_stats = performance_monitor.get_stats()
        
        return {
            'query_performance': {
                'slow_queries': len(perf_stats.get('slow_queries', [])),
                'query_counts': perf_stats.get('query_counts', {})
            },
            'response_times': perf_stats.get('metrics_summary', {}).get('application.request_time', {}),
            'memory_usage': psutil.Process().memory_info()._asdict()
        }
    except Exception as e:
        logger.error(f"Ошибка получения метрик производительности: {e}")
        return {'error': str(e)}

def _get_db_pool_stats() -> Dict[str, Any]:
    """Получение статистики пула соединений с базой данных"""
    try:
        from app import db_pool_manager
        return db_pool_manager.get_pool_stats()
    except Exception:
        return {'error': 'Не удалось получить статистику пула'}

def _get_application_uptime() -> Dict[str, Any]:
    """Получение информации о времени работы приложения"""
    # Это требует отслеживания с момента запуска приложения
    return {
        'start_time': 'unknown',
        'uptime_seconds': 0
    }

def _check_database_service() -> Dict[str, Any]:
    """Проверка состояния сервиса базы данных"""
    try:
        from app import db
        db.session.execute('SELECT 1')
        return {'status': 'healthy', 'response_time_ms': 0}  # Требуется замер времени
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}

def _check_cache_service() -> Dict[str, Any]:
    """Проверка сервиса кэша Flask"""
    try:
        from app import cache
        if cache:
            cache.set('health_check', 'ok', timeout=1)
            cache.get('health_check')
            return {'status': 'healthy'}
        else:
            return {'status': 'unavailable'}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}

def _check_redis_cache_service() -> Dict[str, Any]:
    """Проверка сервиса кэша Redis"""
    try:
        from app import redis_cache
        if redis_cache.redis_available:
            redis_cache.set('health_check', 'ok', timeout=1)
            redis_cache.get('health_check')
            return {'status': 'healthy'}
        else:
            return {'status': 'unavailable'}
    except Exception as e:
        return {'status': 'unhealthy', 'error': str(e)}

def _check_external_services() -> Dict[str, Any]:
    """Проверка состояния внешних сервисов"""
    # Заглушка для проверки внешних API типа HH.ru
    return {
        'hh_api': {'status': 'unknown'},
        'superjob_api': {'status': 'unknown'}
    }

def _check_celery_service() -> Dict[str, Any]:
    """Проверка сервиса фоновых задач Celery"""
    try:
        from app.tasks import get_celery
        celery = get_celery()
        # Это проверит состояние воркеров Celery
        return {'status': 'unknown'}  # Требуется фактическая инспекция Celery
    except Exception as e:
        return {'status': 'error', 'error': str(e)}

def _calculate_overall_status(health_data: Dict[str, Any]) -> str:
    """Расчет общего состояния системы"""
    services = health_data.get('services', {})
    
    if any(status.startswith('unhealthy') for status in services.values()):
        return 'critical'
    elif any(status.startswith('degraded') or status == 'unavailable' for status in services.values()):
        return 'degraded'
    else:
        return 'healthy'