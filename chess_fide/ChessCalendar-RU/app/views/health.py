#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Health Check endpoints
"""

from flask import Blueprint, jsonify, request
from app.utils.health_check import get_health_check
import logging

logger = logging.getLogger('chess_calendar')

health_bp = Blueprint('health', __name__, url_prefix='/health')


@health_bp.route('/', methods=['GET'])
@health_bp.route('', methods=['GET'])
def health_check():
    """
    Простая проверка здоровья приложения
    
    Returns:
        JSON с базовым статусом
    """
    health = get_health_check()
    
    if not health:
        return jsonify({
            'status': 'error',
            'message': 'Health check system not initialized'
        }), 503
    
    result = health.get_simple_status()
    status_code = 200 if result['status'] == 'ok' else 503
    
    return jsonify(result), status_code


@health_bp.route('/detailed', methods=['GET'])
def health_check_detailed():
    """
    Подробная проверка здоровья приложения
    
    Returns:
        JSON с детальной информацией о всех компонентах
    """
    health = get_health_check()
    
    if not health:
        return jsonify({
            'status': 'error',
            'message': 'Health check system not initialized'
        }), 503
    
    result = health.run_all_checks()
    
    # Определяем HTTP статус код
    if result['overall_status'] == 'unhealthy':
        status_code = 503
    elif result['overall_status'] == 'degraded':
        status_code = 200  # Работает, но с предупреждениями
    else:
        status_code = 200
    
    return jsonify(result), status_code


@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """
    Проверка готовности приложения (для Kubernetes)
    
    Returns:
        200 если приложение готово обрабатывать запросы
        503 если приложение не готово
    """
    health = get_health_check()
    
    if not health:
        return jsonify({
            'ready': False,
            'message': 'Health check system not initialized'
        }), 503
    
    # Проверяем только критичные компоненты
    db_check = health.check_database()
    
    if db_check['healthy']:
        return jsonify({
            'ready': True,
            'message': 'Application is ready'
        }), 200
    else:
        return jsonify({
            'ready': False,
            'message': 'Application is not ready',
            'details': db_check
        }), 503


@health_bp.route('/live', methods=['GET'])
def liveness_check():
    """
    Проверка живости приложения (для Kubernetes)
    
    Returns:
        200 если приложение живо
        503 если приложение мертво
    """
    # Простая проверка - если мы можем ответить, значит живы
    return jsonify({
        'alive': True,
        'message': 'Application is alive'
    }), 200


@health_bp.route('/startup', methods=['GET'])
def startup_check():
    """
    Проверка запуска приложения (для Kubernetes)
    
    Returns:
        200 если приложение запустилось
        503 если приложение ещё запускается
    """
    health = get_health_check()
    
    if not health:
        return jsonify({
            'started': False,
            'message': 'Health check system not initialized'
        }), 503
    
    # Проверяем, что все критичные компоненты инициализированы
    result = health.run_all_checks()
    
    critical_checks = ['database']
    all_critical_healthy = all(
        result['checks'].get(check, {}).get('healthy', False)
        for check in critical_checks
    )
    
    if all_critical_healthy:
        return jsonify({
            'started': True,
            'message': 'Application has started successfully',
            'uptime': result['uptime']
        }), 200
    else:
        return jsonify({
            'started': False,
            'message': 'Application is still starting',
            'checks': {k: v for k, v in result['checks'].items() if k in critical_checks}
        }), 503


@health_bp.route('/metrics', methods=['GET'])
def health_metrics():
    """
    Метрики здоровья в формате Prometheus
    
    Returns:
        Текстовый формат метрик Prometheus
    """
    health = get_health_check()
    
    if not health:
        return "# Health check system not initialized\n", 503
    
    result = health.run_all_checks()
    
    # Формируем метрики в формате Prometheus
    metrics = []
    
    # Общий статус
    overall_healthy = 1 if result['healthy'] else 0
    metrics.append(f'app_health_status{{status="{result["overall_status"]}"}} {overall_healthy}')
    
    # Uptime
    metrics.append(f'app_uptime_seconds {result["uptime"]["seconds"]}')
    
    # Статус каждой проверки
    for check_name, check_result in result['checks'].items():
        healthy = 1 if check_result.get('healthy', False) else 0
        metrics.append(f'app_health_check{{check="{check_name}"}} {healthy}')
        
        # Дополнительные метрики
        if 'details' in check_result:
            details = check_result['details']
            
            if check_name == 'memory' and 'percent' in details:
                metrics.append(f'app_memory_usage_percent {details["percent"]}')
            
            if check_name == 'cpu' and 'percent' in details:
                metrics.append(f'app_cpu_usage_percent {details["percent"]}')
            
            if check_name == 'disk' and 'percent' in details:
                metrics.append(f'app_disk_usage_percent {details["percent"]}')
    
    return '\n'.join(metrics) + '\n', 200, {'Content-Type': 'text/plain; charset=utf-8'}
