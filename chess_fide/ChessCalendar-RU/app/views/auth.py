"""
API endpoints для аутентификации с улучшенной безопасностью
"""
from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models.user import User
from app.models.audit_log import AuditLog, LoginAttempt, TwoFactorSecret
from app.utils.security import (
    PasswordManager, RateLimiter, JWTManager, TwoFactorAuth,
    AuditLogger, rate_limit, require_auth, require_admin
)
from app.utils.unified_cache import cache
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
@rate_limit(max_attempts=3, window=3600)  # 3 попытки в час
def register():
    """
    Регистрация нового пользователя
    
    POST /auth/register
    {
        "username": "user",
        "email": "user@example.com",
        "password": "SecurePassword123"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Валидация
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Проверка надежности пароля
    is_valid, error_msg = PasswordManager.validate_password_strength(password)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    # Проверка существования пользователя
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Создание пользователя
    user = User(
        username=username,
        email=email,
        password=password
    )
    user.is_active = True
    
    db.session.add(user)
    db.session.commit()
    
    # Логирование
    audit_logger = AuditLogger(db)
    audit_logger.log_action(
        user_id=user.id,
        action='register',
        resource='user',
        resource_id=user.id
    )
    
    logger.info(f"New user registered: {username}")
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 201


@auth_bp.route('/login', methods=['POST'])
@rate_limit(max_attempts=10, window=300)  # 10 попыток за 5 минут
def login():
    """
    Вход в систему
    
    POST /auth/login
    {
        "username": "user",
        "password": "password",
        "totp_code": "123456"  // опционально, если включен 2FA
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    totp_code = data.get('totp_code')
    
    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    
    # Получаем пользователя
    user = User.query.filter_by(username=username).first()
    
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    
    # Проверка блокировки
    if user and user.locked_until and user.locked_until > datetime.utcnow():
        remaining = (user.locked_until - datetime.utcnow()).total_seconds()
        
        LoginAttempt.log_attempt(username, ip_address, False, user_agent)
        
        return jsonify({
            'error': 'Account is locked',
            'locked_until': user.locked_until.isoformat(),
            'remaining_seconds': int(remaining)
        }), 403
    
    # Проверка пароля
    if not user or not user.check_password(password):
        # Логируем неудачную попытку
        LoginAttempt.log_attempt(username, ip_address, False, user_agent)
        
        if user:
            user.failed_login_attempts += 1
            
            # Блокировка после 5 неудачных попыток
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=30)
                db.session.commit()
                
                logger.warning(f"Account locked: {username} from {ip_address}")
                
                return jsonify({
                    'error': 'Account locked due to too many failed attempts',
                    'locked_until': user.locked_until.isoformat()
                }), 403
            
            db.session.commit()
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Проверка активности
    if not user.is_active:
        LoginAttempt.log_attempt(username, ip_address, False, user_agent)
        return jsonify({'error': 'Account is disabled'}), 403
    
    # Проверка 2FA
    if user.two_factor_enabled:
        if not totp_code:
            return jsonify({
                'error': '2FA code required',
                'requires_2fa': True
            }), 401
        
        # Получаем секрет 2FA
        two_factor = TwoFactorSecret.query.filter_by(user_id=user.id).first()
        
        if not two_factor or not two_factor.enabled:
            return jsonify({'error': '2FA not properly configured'}), 500
        
        # Проверяем TOTP код
        if not TwoFactorAuth.verify_totp(two_factor.secret, totp_code):
            # Проверяем резервный код
            if not two_factor.verify_backup_code(totp_code):
                LoginAttempt.log_attempt(username, ip_address, False, user_agent)
                return jsonify({'error': 'Invalid 2FA code'}), 401
        
        # Обновляем время последнего использования
        two_factor.last_used = datetime.utcnow()
        db.session.commit()
    
    # Успешный вход
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Логируем успешную попытку
    LoginAttempt.log_attempt(username, ip_address, True, user_agent)
    
    # Генерируем токены
    access_token = JWTManager.generate_token(
        user_id=user.id,
        username=user.username,
        is_admin=user.is_admin,
        expires_in=3600  # 1 час
    )
    
    refresh_token = JWTManager.generate_refresh_token(user.id)
    
    # Логируем действие
    audit_logger = AuditLogger(db)
    audit_logger.log_action(
        user_id=user.id,
        action='login',
        resource='user',
        resource_id=user.id
    )
    
    logger.info(f"User logged in: {username} from {ip_address}")
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'two_factor_enabled': user.two_factor_enabled
        }
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Обновление access токена
    
    POST /auth/refresh
    Authorization: Bearer <refresh_token>
    """
    token = request.headers.get('Authorization')
    
    if not token or not token.startswith('Bearer '):
        return jsonify({'error': 'No refresh token provided'}), 401
    
    token = token[7:]
    
    # Проверяем токен
    payload = JWTManager.verify_token(token)
    if not payload or payload.get('type') != 'refresh':
        return jsonify({'error': 'Invalid refresh token'}), 401
    
    # Проверяем отзыв
    if JWTManager.is_token_revoked(payload.get('jti'), cache_manager.redis_client):
        return jsonify({'error': 'Token has been revoked'}), 401
    
    # Получаем пользователя
    user = User.query.get(payload.get('user_id'))
    if not user or not user.is_active:
        return jsonify({'error': 'User not found or inactive'}), 401
    
    # Генерируем новый access токен
    access_token = JWTManager.generate_token(
        user_id=user.id,
        username=user.username,
        is_admin=user.is_admin,
        expires_in=3600
    )
    
    return jsonify({
        'access_token': access_token
    }), 200


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout():
    """
    Выход из системы (отзыв токена)
    
    POST /auth/logout
    Authorization: Bearer <access_token>
    """
    payload = request.current_user
    jti = payload.get('jti')
    exp = payload.get('exp')
    
    # Вычисляем время до истечения
    expires_in = int(exp - datetime.utcnow().timestamp())
    
    # Отзываем токен
    JWTManager.revoke_token(jti, expires_in, cache_manager.redis_client)
    
    # Логируем действие
    audit_logger = AuditLogger(db)
    audit_logger.log_action(
        user_id=payload.get('user_id'),
        action='logout',
        resource='user',
        resource_id=payload.get('user_id')
    )
    
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_bp.route('/verify', methods=['GET'])
@require_auth
def verify():
    """
    Проверка токена
    
    GET /auth/verify
    Authorization: Bearer <access_token>
    """
    return jsonify({
        'valid': True,
        'user': request.current_user
    }), 200


@auth_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """
    Смена пароля
    
    POST /auth/change-password
    {
        "old_password": "old",
        "new_password": "new"
    }
    """
    data = request.get_json()
    
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return jsonify({'error': 'Missing passwords'}), 400
    
    # Получаем пользователя
    user = User.query.get(request.current_user.get('user_id'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Проверяем старый пароль
    if not user.check_password(old_password):
        return jsonify({'error': 'Invalid old password'}), 401
    
    # Проверяем надежность нового пароля
    is_valid, error_msg = PasswordManager.validate_password_strength(new_password)
    if not is_valid:
        return jsonify({'error': error_msg}), 400
    
    # Устанавливаем новый пароль
    user.set_password(new_password)
    user.password_changed_at = datetime.utcnow()
    user.require_password_change = False
    db.session.commit()
    
    # Логируем действие
    audit_logger = AuditLogger(db)
    audit_logger.log_action(
        user_id=user.id,
        action='change_password',
        resource='user',
        resource_id=user.id
    )
    
    logger.info(f"Password changed: user={user.username}")
    
    return jsonify({'message': 'Password changed successfully'}), 200


@auth_bp.route('/2fa/setup', methods=['POST'])
@require_auth
def setup_2fa():
    """
    Настройка 2FA
    
    POST /auth/2fa/setup
    """
    user_id = request.current_user.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Проверяем, не настроен ли уже 2FA
    existing = TwoFactorSecret.query.filter_by(user_id=user_id).first()
    if existing and existing.enabled:
        return jsonify({'error': '2FA already enabled'}), 400
    
    # Генерируем секрет
    secret = TwoFactorAuth.generate_secret()
    
    # Создаем или обновляем запись
    if existing:
        existing.secret = secret
        existing.enabled = False
        two_factor = existing
    else:
        two_factor = TwoFactorSecret(
            user_id=user_id,
            secret=secret,
            enabled=False
        )
        db.session.add(two_factor)
    
    db.session.commit()
    
    # Генерируем QR код URL
    qr_url = TwoFactorAuth.generate_qr_code_url(user.username, secret)
    
    return jsonify({
        'secret': secret,
        'qr_code_url': qr_url,
        'message': 'Scan QR code with authenticator app and verify with code'
    }), 200


@auth_bp.route('/2fa/enable', methods=['POST'])
@require_auth
def enable_2fa():
    """
    Включение 2FA после проверки кода
    
    POST /auth/2fa/enable
    {
        "totp_code": "123456"
    }
    """
    data = request.get_json()
    totp_code = data.get('totp_code')
    
    if not totp_code:
        return jsonify({'error': 'TOTP code required'}), 400
    
    user_id = request.current_user.get('user_id')
    two_factor = TwoFactorSecret.query.filter_by(user_id=user_id).first()
    
    if not two_factor:
        return jsonify({'error': '2FA not set up'}), 400
    
    # Проверяем код
    if not TwoFactorAuth.verify_totp(two_factor.secret, totp_code):
        return jsonify({'error': 'Invalid TOTP code'}), 401
    
    # Включаем 2FA
    two_factor.enabled = True
    two_factor.last_used = datetime.utcnow()
    
    user = User.query.get(user_id)
    user.two_factor_enabled = True
    
    # Генерируем резервные коды
    backup_codes = two_factor.generate_backup_codes()
    
    db.session.commit()
    
    # Логируем действие
    audit_logger = AuditLogger(db)
    audit_logger.log_action(
        user_id=user_id,
        action='enable_2fa',
        resource='user',
        resource_id=user_id
    )
    
    logger.info(f"2FA enabled: user={user.username}")
    
    return jsonify({
        'message': '2FA enabled successfully',
        'backup_codes': backup_codes,
        'warning': 'Save these backup codes in a safe place. They can only be used once.'
    }), 200


@auth_bp.route('/2fa/disable', methods=['POST'])
@require_auth
def disable_2fa():
    """
    Отключение 2FA
    
    POST /auth/2fa/disable
    {
        "password": "password",
        "totp_code": "123456"
    }
    """
    data = request.get_json()
    password = data.get('password')
    totp_code = data.get('totp_code')
    
    if not password or not totp_code:
        return jsonify({'error': 'Password and TOTP code required'}), 400
    
    user_id = request.current_user.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Проверяем пароль
    if not user.check_password(password):
        return jsonify({'error': 'Invalid password'}), 401
    
    two_factor = TwoFactorSecret.query.filter_by(user_id=user_id).first()
    
    if not two_factor or not two_factor.enabled:
        return jsonify({'error': '2FA not enabled'}), 400
    
    # Проверяем TOTP код
    if not TwoFactorAuth.verify_totp(two_factor.secret, totp_code):
        return jsonify({'error': 'Invalid TOTP code'}), 401
    
    # Отключаем 2FA
    two_factor.enabled = False
    user.two_factor_enabled = False
    db.session.commit()
    
    # Логируем действие
    audit_logger = AuditLogger(db)
    audit_logger.log_action(
        user_id=user_id,
        action='disable_2fa',
        resource='user',
        resource_id=user_id
    )
    
    logger.info(f"2FA disabled: user={user.username}")
    
    return jsonify({'message': '2FA disabled successfully'}), 200


@auth_bp.route('/audit-log', methods=['GET'])
@require_admin
def get_audit_log():
    """
    Получить audit log (только для администраторов)
    
    GET /auth/audit-log?user_id=1&action=login&limit=100
    """
    filters = {}
    
    if request.args.get('user_id'):
        filters['user_id'] = int(request.args.get('user_id'))
    
    if request.args.get('action'):
        filters['action'] = request.args.get('action')
    
    if request.args.get('resource'):
        filters['resource'] = request.args.get('resource')
    
    limit = int(request.args.get('limit', 100))
    
    logs = AuditLog.search(filters, limit)
    
    return jsonify({
        'logs': [log.to_dict() for log in logs],
        'count': len(logs)
    }), 200


@auth_bp.route('/login-attempts', methods=['GET'])
@require_admin
def get_login_attempts():
    """
    Получить попытки входа (только для администраторов)
    
    GET /auth/login-attempts?username=user&limit=100
    """
    username = request.args.get('username')
    limit = int(request.args.get('limit', 100))
    
    query = LoginAttempt.query
    
    if username:
        query = query.filter_by(username=username)
    
    attempts = query.order_by(LoginAttempt.timestamp.desc()).limit(limit).all()
    
    return jsonify({
        'attempts': [attempt.to_dict() for attempt in attempts],
        'count': len(attempts)
    }), 200
