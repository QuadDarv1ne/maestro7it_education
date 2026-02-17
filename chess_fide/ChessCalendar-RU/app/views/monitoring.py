"""
API endpoints для мониторинга и диагностики
"""

from flask import Blueprint, jsonify, request
from functools import wraps
from app.utils.unified_monitoring import health_checker, performance_monitor
from app.utils.predictive_cache import predictive_cache
from app.utils.ab_testing import ab_test_manager

monitoring_bp = Blueprint('monitoring', __name__, url_prefix='/api/monitoring')


def require_admin(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Простая проверка (в production использовать JWT)
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        
        # Проверка ключа (упрощенная версия)
        from app.models.user import User
        user = User.query.filter_by(api_key=api_key, is_admin=True).first()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


@monitoring_bp.route('/health', methods=['GET'])
def health_check():
    """
    Комплексная проверка здоровья системы
    
    GET /api/monitoring/health
    """
    detailed = request.args.get('detailed', 'false').lower() == 'true'
    
    if detailed:
        return jsonify(health_checker.check_all())
    else:
        return jsonify(health_checker.get_summary())


@monitoring_bp.route('/health/<component>', methods=['GET'])
def health_check_component(component):
    """
    Проверка конкретного компонента
    
    GET /api/monitoring/health/database
    GET /api/monitoring/health/redis
    GET /api/monitoring/health/disk
    """
    check_methods = {
        'database': health_checker.check_database,
        'redis': health_checker.check_redis,
        'disk': health_checker.check_disk_space,
        'memory': health_checker.check_memory,
        'cpu': health_checker.check_cpu,
        'celery': health_checker.check_celery
    }
    
    if component not in check_methods:
        return jsonify({'error': f'Unknown component: {component}'}), 404
    
    result = check_methods[component]()
    return jsonify(result)


@monitoring_bp.route('/performance/summary', methods=['GET'])
@require_admin
def performance_summary():
    """
    Общая сводка производительности
    
    GET /api/monitoring/performance/summary
    Headers: X-API-Key: <admin_api_key>
    """
    return jsonify(performance_monitor.get_summary())


@monitoring_bp.route('/performance/endpoints', methods=['GET'])
@require_admin
def performance_endpoints():
    """
    Статистика по endpoints
    
    GET /api/monitoring/performance/endpoints
    GET /api/monitoring/performance/endpoints?endpoint=/api/tournaments
    """
    endpoint = request.args.get('endpoint')
    stats = performance_monitor.get_endpoint_stats(endpoint)
    return jsonify(stats)


@monitoring_bp.route('/performance/slow', methods=['GET'])
@require_admin
def performance_slow_requests():
    """
    Медленные запросы
    
    GET /api/monitoring/performance/slow
    GET /api/monitoring/performance/slow?threshold=2000
    """
    threshold = request.args.get('threshold', type=int)
    slow_requests = performance_monitor.get_slow_requests(threshold)
    return jsonify({
        'count': len(slow_requests),
        'requests': slow_requests
    })


@monitoring_bp.route('/performance/recent', methods=['GET'])
@require_admin
def performance_recent_requests():
    """
    Последние запросы
    
    GET /api/monitoring/performance/recent
    GET /api/monitoring/performance/recent?limit=100
    """
    limit = request.args.get('limit', 50, type=int)
    recent = performance_monitor.get_recent_requests(limit)
    return jsonify({
        'count': len(recent),
        'requests': recent
    })


@monitoring_bp.route('/performance/alerts', methods=['GET'])
@require_admin
def performance_alerts():
    """
    Алерты производительности
    
    GET /api/monitoring/performance/alerts
    """
    alerts = performance_monitor.get_alerts()
    return jsonify({
        'count': len(alerts),
        'alerts': alerts
    })


@monitoring_bp.route('/cache/stats', methods=['GET'])
@require_admin
def cache_stats():
    """
    Статистика кэша
    
    GET /api/monitoring/cache/stats
    """
    if predictive_cache:
        stats = predictive_cache.get_stats()
        return jsonify(stats)
    else:
        return jsonify({'error': 'Predictive cache not initialized'}), 503


@monitoring_bp.route('/cache/patterns', methods=['GET'])
@require_admin
def cache_patterns():
    """
    Паттерны доступа к кэшу
    
    GET /api/monitoring/cache/patterns
    """
    if predictive_cache:
        patterns = predictive_cache.analyze_patterns()
        return jsonify({
            'count': len(patterns),
            'patterns': patterns
        })
    else:
        return jsonify({'error': 'Predictive cache not initialized'}), 503


@monitoring_bp.route('/ab-tests', methods=['GET'])
@require_admin
def ab_tests_list():
    """
    Список активных A/B тестов
    
    GET /api/monitoring/ab-tests
    """
    tests = [
        {
            'name': name,
            'variants': test.variants,
            'weights': test.weights
        }
        for name, test in ab_test_manager.tests.items()
    ]
    return jsonify({
        'count': len(tests),
        'tests': tests
    })


@monitoring_bp.route('/ab-tests/<test_name>/results', methods=['GET'])
@require_admin
def ab_test_results(test_name):
    """
    Результаты A/B теста
    
    GET /api/monitoring/ab-tests/homepage_layout/results
    GET /api/monitoring/ab-tests/homepage_layout/results?days=14
    """
    days = request.args.get('days', 7, type=int)
    results = ab_test_manager.get_results(test_name, days)
    return jsonify(results)


@monitoring_bp.route('/ab-tests/<test_name>/significance', methods=['GET'])
@require_admin
def ab_test_significance(test_name):
    """
    Статистическая значимость результатов A/B теста
    
    GET /api/monitoring/ab-tests/homepage_layout/significance
    GET /api/monitoring/ab-tests/homepage_layout/significance?metric=click
    """
    metric = request.args.get('metric', 'conversion')
    significance = ab_test_manager.calculate_significance(test_name, metric)
    return jsonify(significance)


@monitoring_bp.route('/system/info', methods=['GET'])
@require_admin
def system_info():
    """
    Информация о системе
    
    GET /api/monitoring/system/info
    """
    import platform
    import sys
    from datetime import datetime
    
    return jsonify({
        'platform': platform.platform(),
        'python_version': sys.version,
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'timestamp': datetime.utcnow().isoformat()
    })


@monitoring_bp.route('/reset', methods=['POST'])
@require_admin
def reset_monitoring():
    """
    Сброс статистики мониторинга
    
    POST /api/monitoring/reset
    Headers: X-API-Key: <admin_api_key>
    """
    performance_monitor.reset_stats()
    return jsonify({
        'message': 'Monitoring statistics reset successfully'
    })
