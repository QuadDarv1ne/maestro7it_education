# -*- coding: utf-8 -*-
"""
API конечные точки расширенной безопасности для ПрофиТест
Предоставляет доступ к функциям безопасности и аутентификации
"""
from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from app.advanced_security import security_manager, SecurityLevel, AttackType
import json

security_api = Blueprint('security_api', __name__)


@security_api.route('/csrf-token', methods=['GET'])
@login_required
def get_csrf_token():
    """
    Получает CSRF токен для защиты от межсайтовой подделки запроса.
    """
    try:
        token = security_manager.generate_csrf_token()
        return jsonify({
            'success': True,
            'token': token
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/validate-password', methods=['POST'])
@login_required
def validate_password():
    """
    Проверяет надежность пароля.
    """
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        result = security_manager.validate_password_strength(password)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/security-config', methods=['GET'])
@login_required
def get_security_config():
    """
    Получает текущую конфигурацию безопасности.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        config = {
            'max_login_attempts': security_manager.security_config['max_login_attempts'],
            'lockout_duration': security_manager.security_config['lockout_duration'],
            'session_timeout': security_manager.security_config['session_timeout'],
            'password_min_length': security_manager.security_config['password_min_length'],
            'require_special_chars': security_manager.security_config['require_special_chars'],
            'require_numbers': security_manager.security_config['require_numbers'],
            'require_uppercase': security_manager.security_config['require_uppercase'],
            'rate_limit_requests': security_manager.security_config['rate_limit_requests'],
            'rate_limit_window': security_manager.security_config['rate_limit_window'],
            'security_level': security_manager.security_config['security_level'].value
        }
        
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/security-config', methods=['POST'])
@login_required
def update_security_config():
    """
    Обновляет конфигурацию безопасности.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        # Обновляем только разрешенные параметры
        allowed_params = [
            'max_login_attempts', 'lockout_duration', 'session_timeout',
            'password_min_length', 'require_special_chars', 'require_numbers',
            'require_uppercase', 'rate_limit_requests', 'rate_limit_window', 'security_level'
        ]
        
        for param in allowed_params:
            if param in data:
                if param == 'security_level':
                    from app.advanced_security import SecurityLevel
                    security_manager.security_config[param] = SecurityLevel(data[param])
                else:
                    security_manager.security_config[param] = data[param]
        
        return jsonify({
            'success': True,
            'message': 'Конфигурация безопасности обновлена'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/security-report', methods=['GET'])
@login_required
def get_security_report():
    """
    Получает отчет о состоянии безопасности системы.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        report = security_manager.get_security_report()
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/login-attempts', methods=['GET'])
@login_required
def get_login_attempts():
    """
    Получает информацию о неудачных попытках входа.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        attempts = []
        for identifier, info in security_manager.failed_attempts.items():
            attempts.append({
                'identifier': identifier,
                'count': info['count'],
                'reset_time': info['reset_time'].isoformat(),
                'blocked': info['count'] >= security_manager.security_config['max_login_attempts']
            })
        
        return jsonify({
            'success': True,
            'attempts': attempts,
            'total_blocked': sum(1 for info in security_manager.failed_attempts.values() 
                               if info['count'] >= security_manager.security_config['max_login_attempts'])
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/reset-login-attempts/<identifier>', methods=['POST'])
@login_required
def reset_login_attempts(identifier):
    """
    Сбрасывает счетчик неудачных попыток входа для указанного идентификатора.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        security_manager.reset_login_attempts(identifier)
        return jsonify({
            'success': True,
            'message': f'Счетчик неудачных попыток для {identifier} сброшен'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/rate-limit-check', methods=['POST'])
@login_required
def check_rate_limit():
    """
    Проверяет, превышено ли ограничение частоты запросов.
    """
    try:
        data = request.get_json()
        identifier = data.get('identifier', request.remote_addr)
        
        is_limited = security_manager.is_rate_limited(identifier)
        return jsonify({
            'success': True,
            'is_limited': is_limited,
            'identifier': identifier
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/generate-jwt-token', methods=['POST'])
@login_required
def generate_jwt_token():
    """
    Генерирует JWT токен для пользователя.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', current_user.id)
        expires_in = data.get('expires_in', 3600)
        
        # Только администратор может генерировать токены для других пользователей
        if user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для генерации токена другого пользователя'
            }), 403
        
        token = security_manager.generate_jwt_token(user_id, expires_in)
        return jsonify({
            'success': True,
            'token': token,
            'expires_in': expires_in
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/verify-jwt-token', methods=['POST'])
@login_required
def verify_jwt_token():
    """
    Проверяет JWT токен.
    """
    try:
        data = request.get_json()
        token = data.get('token')
        
        user_id = security_manager.verify_jwt_token(token)
        return jsonify({
            'success': True,
            'valid': user_id is not None,
            'user_id': user_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/create-session-token', methods=['POST'])
@login_required
def create_session_token():
    """
    Создает токен сессии для пользователя.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', current_user.id)
        
        # Только администратор может создавать токены для других пользователей
        if user_id != current_user.id and not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Недостаточно прав для создания токена другого пользователя'
            }), 403
        
        token = security_manager.create_session_token(user_id)
        return jsonify({
            'success': True,
            'token': token
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/validate-session-token', methods=['POST'])
@login_required
def validate_session_token():
    """
    Проверяет токен сессии.
    """
    try:
        data = request.get_json()
        token = data.get('token')
        
        is_valid = security_manager.validate_session_token(token)
        user_id = security_manager.get_user_from_session_token(token) if is_valid else None
        
        return jsonify({
            'success': True,
            'valid': is_valid,
            'user_id': user_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/security-events', methods=['GET'])
@login_required
def get_security_events():
    """
    Получает последние события безопасности.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        # В реальной реализации здесь будут события из логов безопасности
        # Пока возвращаем заглушку
        events = [
            {
                'timestamp': '2023-06-15T10:30:00Z',
                'type': 'failed_login',
                'severity': 'medium',
                'details': {'ip': '192.168.1.100', 'username': 'test_user'}
            },
            {
                'timestamp': '2023-06-15T11:15:00Z',
                'type': 'rate_limit_exceeded',
                'severity': 'low',
                'details': {'ip': '192.168.1.101', 'endpoint': '/api/login'}
            }
        ]
        
        return jsonify({
            'success': True,
            'events': events,
            'total_count': len(events)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/sanitize-input', methods=['POST'])
@login_required
def sanitize_input():
    """
    Санитизирует пользовательский ввод.
    """
    try:
        data = request.get_json()
        input_str = data.get('input', '')
        max_length = data.get('max_length', 1000)
        
        sanitized = security_manager.sanitize_input(input_str, max_length)
        return jsonify({
            'success': True,
            'original': input_str,
            'sanitized': sanitized
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/hash-password', methods=['POST'])
@login_required
def hash_password():
    """
    Хэширует пароль.
    """
    try:
        data = request.get_json()
        password = data.get('password')
        
        if not password:
            return jsonify({
                'success': False,
                'message': 'Пароль обязателен'
            }), 400
        
        hashed = security_manager.hash_password(password)
        return jsonify({
            'success': True,
            'hashed_password': hashed
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/verify-password', methods=['POST'])
@login_required
def verify_password():
    """
    Проверяет пароль против хэша.
    """
    try:
        data = request.get_json()
        password = data.get('password')
        hashed = data.get('hashed')
        
        if not password or not hashed:
            return jsonify({
                'success': False,
                'message': 'Пароль и хэш обязательны'
            }), 400
        
        is_valid = security_manager.verify_password(password, hashed)
        return jsonify({
            'success': True,
            'valid': is_valid
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@security_api.route('/security-levels', methods=['GET'])
@login_required
def get_security_levels():
    """
    Получает доступные уровни безопасности.
    """
    try:
        levels = [
            {'name': 'LOW', 'value': 'low', 'description': 'Низкий уровень безопасности'},
            {'name': 'MEDIUM', 'value': 'medium', 'description': 'Средний уровень безопасности'},
            {'name': 'HIGH', 'value': 'high', 'description': 'Высокий уровень безопасности'},
            {'name': 'MAXIMUM', 'value': 'maximum', 'description': 'Максимальный уровень безопасности'}
        ]
        
        return jsonify({
            'success': True,
            'levels': levels
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500