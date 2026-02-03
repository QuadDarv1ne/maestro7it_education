# -*- coding: utf-8 -*-
"""
API конечные точки системного мониторинга для ПрофиТест
Предоставляет доступ к функциям мониторинга состояния системы
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.system_monitoring import system_monitor
import json

monitoring_api = Blueprint('monitoring_api', __name__)


@monitoring_api.route('/health', methods=['GET'])
def get_system_health():
    """
    Получает общее состояние здоровья системы.
    """
    try:
        health_status = system_monitor.get_system_health()
        return jsonify({
            'success': True,
            'health': health_status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/system/metrics', methods=['GET'])
@login_required
def get_system_metrics():
    """
    Получает системные метрики (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        health_status = system_monitor.get_system_health()
        system_metrics = health_status.get('system_metrics', {})
        
        return jsonify({
            'success': True,
            'metrics': system_metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/application/metrics', methods=['GET'])
@login_required
def get_application_metrics():
    """
    Получает метрики приложения (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        health_status = system_monitor.get_system_health()
        app_metrics = health_status.get('application_metrics', {})
        
        return jsonify({
            'success': True,
            'metrics': app_metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/database/metrics', methods=['GET'])
@login_required
def get_database_metrics():
    """
    Получает метрики базы данных (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        health_status = system_monitor.get_system_health()
        db_metrics = health_status.get('database_metrics', {})
        
        return jsonify({
            'success': True,
            'metrics': db_metrics
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/alerts', methods=['GET'])
@login_required
def get_system_alerts():
    """
    Получает текущие алерты системы (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        health_status = system_monitor.get_system_health()
        alerts = health_status.get('alerts', [])
        
        return jsonify({
            'success': True,
            'alerts': alerts,
            'total_alerts': len(alerts)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/performance/report', methods=['GET'])
@login_required
def get_performance_report():
    """
    Генерирует детальный отчет о производительности системы (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        performance_report = system_monitor.get_detailed_performance_report()
        
        if 'error' in performance_report:
            return jsonify({
                'success': False,
                'message': performance_report['error']
            }), 500
        
        return jsonify({
            'success': True,
            'report': performance_report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/recommendations', methods=['GET'])
@login_required
def get_performance_recommendations():
    """
    Получает рекомендации по оптимизации производительности (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        performance_report = system_monitor.get_detailed_performance_report()
        recommendations = performance_report.get('recommendations', [])
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/resource/trends', methods=['GET'])
@login_required
def get_resource_trends():
    """
    Получает тренды использования ресурсов (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        performance_report = system_monitor.get_detailed_performance_report()
        trends = performance_report.get('resource_trends', {})
        
        return jsonify({
            'success': True,
            'trends': trends
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/benchmarks', methods=['GET'])
@login_required
def get_performance_benchmarks():
    """
    Выполняет и возвращает результаты бенчмарков производительности (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        performance_report = system_monitor.get_detailed_performance_report()
        benchmarks = performance_report.get('performance_benchmarks', {})
        
        return jsonify({
            'success': True,
            'benchmarks': benchmarks
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/status/summary', methods=['GET'])
def get_status_summary():
    """
    Получает краткое резюме состояния системы.
    """
    try:
        health_status = system_monitor.get_system_health()
        
        summary = {
            'overall_status': health_status.get('overall_status', 'unknown'),
            'timestamp': health_status.get('timestamp'),
            'alert_count': len(health_status.get('alerts', [])),
            'critical_alerts': len([a for a in health_status.get('alerts', []) if a.get('severity') == 'critical']),
            'warning_alerts': len([a for a in health_status.get('alerts', []) if a.get('severity') == 'warning'])
        }
        
        return jsonify({
            'success': True,
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/health/check', methods=['POST'])
def custom_health_check():
    """
    Выполняет пользовательскую проверку здоровья системы.
    """
    try:
        data = request.get_json()
        check_type = data.get('check_type', 'basic')
        
        if check_type == 'basic':
            health_status = system_monitor.get_system_health()
        elif check_type == 'performance':
            health_status = system_monitor.get_detailed_performance_report()
        else:
            return jsonify({
                'success': False,
                'message': 'Неподдерживаемый тип проверки'
            }), 400
        
        return jsonify({
            'success': True,
            'result': health_status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/metrics/history', methods=['GET'])
@login_required
def get_metrics_history():
    """
    Получает исторические данные метрик (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # В реальной системе здесь будут данные из системы хранения метрик
        # Пока возвращаем текущие метрики как исторические данные
        health_status = system_monitor.get_system_health()
        
        history_data = {
            'timestamp': health_status.get('timestamp'),
            'system_metrics': health_status.get('system_metrics', {}),
            'application_metrics': health_status.get('application_metrics', {}),
            'database_metrics': health_status.get('database_metrics', {})
        }
        
        return jsonify({
            'success': True,
            'history': [history_data]  # Массив для совместимости
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/alert/thresholds', methods=['GET', 'POST'])
@login_required
def manage_alert_thresholds():
    """
    Получает или обновляет пороговые значения для алертов (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        if request.method == 'GET':
            # Возвращаем текущие пороговые значения
            return jsonify({
                'success': True,
                'thresholds': system_monitor.alert_thresholds
            })
        
        elif request.method == 'POST':
            # Обновляем пороговые значения
            data = request.get_json()
            new_thresholds = data.get('thresholds', {})
            
            # Валидация и обновление порогов
            for key, value in new_thresholds.items():
                if key in system_monitor.alert_thresholds:
                    system_monitor.alert_thresholds[key] = value
            
            return jsonify({
                'success': True,
                'message': 'Пороговые значения обновлены',
                'updated_thresholds': system_monitor.alert_thresholds
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@monitoring_api.route('/system/info', methods=['GET'])
@login_required
def get_system_info():
    """
    Получает общую информацию о системе (только для администраторов).
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        import platform
        import sys
        
        system_info = {
            'platform': {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor()
            },
            'python': {
                'version': sys.version,
                'implementation': platform.python_implementation(),
                'compiler': platform.python_compiler()
            },
            'application': {
                'name': 'ProfiTest',
                'version': '1.0.0'  # Заглушка, в реальной системе можно получать из конфигурации
            }
        }
        
        return jsonify({
            'success': True,
            'info': system_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500