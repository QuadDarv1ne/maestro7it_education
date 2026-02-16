"""
API Gateway - Единая точка входа для всех микросервисов
Использует Kong-подобную архитектуру с маршрутизацией, аутентификацией и rate limiting
"""
from flask import Flask, request, jsonify, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import jwt
import redis
from datetime import datetime, timedelta
from functools import wraps
import logging
import os
import time

app = Flask(__name__)

# Конфигурация
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_EXPIRATION_HOURS'] = int(os.environ.get('JWT_EXPIRATION_HOURS', 24))
app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://redis:6379/0')

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis для кэширования и rate limiting
try:
    redis_client = redis.from_url(app.config['REDIS_URL'])
    redis_client.ping()
    logger.info("Redis connected successfully")
except Exception as e:
    logger.error(f"Redis connection failed: {e}")
    redis_client = None

# Rate Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=app.config['REDIS_URL'],
    default_limits=["1000 per day", "100 per hour"]
)

# Маршруты микросервисов
SERVICES = {
    'tournaments': os.environ.get('TOURNAMENT_SERVICE_URL', 'http://tournament-service:5001'),
    'users': os.environ.get('USER_SERVICE_URL', 'http://user-service:5002'),
    'parser': os.environ.get('PARSER_SERVICE_URL', 'http://parser-service:5003'),
    'cdn': os.environ.get('CDN_SERVICE_URL', 'http://cdn-service:5004'),
    'image': os.environ.get('IMAGE_SERVICE_URL', 'http://image-optimization-service:5005'),
    'calendar': os.environ.get('CALENDAR_SERVICE_URL', 'http://calendar-service:5006'),
    'notifications': os.environ.get('NOTIFICATION_SERVICE_URL', 'http://notification-service:5007'),
    'recommendations': os.environ.get('RECOMMENDATION_SERVICE_URL', 'http://recommendation-service:5008'),
    'favorites': os.environ.get('FAVORITES_SERVICE_URL', 'http://favorites-service:5009'),
}

# JWT утилиты
def generate_token(user_id, username, is_admin=False):
    """Генерация JWT токена"""
    payload = {
        'user_id': user_id,
        'username': username,
        'is_admin': is_admin,
        'exp': datetime.utcnow() + timedelta(hours=app.config['JWT_EXPIRATION_HOURS']),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Проверка JWT токена"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Декораторы аутентификации
def token_required(f):
    """Декоратор для проверки JWT токена"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Получаем токен из заголовка Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        # Проверяем токен
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        # Сохраняем данные пользователя в контексте
        g.current_user = payload
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Декоратор для проверки прав администратора"""
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if not g.current_user.get('is_admin', False):
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    
    return decorated

# Кэширование ответов
def cache_response(timeout=300):
    """Декоратор для кэширования ответов"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not redis_client:
                return f(*args, **kwargs)
            
            # Создаем ключ кэша
            cache_key = f"gateway_cache:{request.path}:{request.query_string.decode()}"
            
            # Проверяем кэш
            cached = redis_client.get(cache_key)
            if cached:
                logger.info(f"Cache hit for {cache_key}")
                return jsonify(eval(cached.decode()))
            
            # Выполняем функцию
            response = f(*args, **kwargs)
            
            # Кэшируем результат
            if response.status_code == 200:
                redis_client.setex(cache_key, timeout, str(response.get_json()))
            
            return response
        return decorated
    return decorator

# Проксирование запросов к микросервисам
def proxy_request(service_name, path, method='GET', **kwargs):
    """Проксирование запроса к микросервису"""
    service_url = SERVICES.get(service_name)
    if not service_url:
        return jsonify({'error': f'Service {service_name} not found'}), 404
    
    url = f"{service_url}{path}"
    
    # Добавляем информацию о пользователе в заголовки
    headers = kwargs.get('headers', {})
    if hasattr(g, 'current_user'):
        headers['X-User-ID'] = str(g.current_user.get('user_id'))
        headers['X-Username'] = g.current_user.get('username')
        headers['X-Is-Admin'] = str(g.current_user.get('is_admin', False))
    
    kwargs['headers'] = headers
    
    try:
        start_time = time.time()
        response = requests.request(method, url, **kwargs)
        elapsed_time = time.time() - start_time
        
        logger.info(f"{method} {url} - {response.status_code} - {elapsed_time:.3f}s")
        
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Service request failed: {e}")
        return jsonify({'error': 'Service unavailable'}), 503

# Аутентификация
@app.route('/auth/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """Аутентификация пользователя и выдача JWT токена"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    # Проксируем запрос к user-service
    response = requests.post(
        f"{SERVICES['users']}/auth/login",
        json=data
    )
    
    if response.status_code == 200:
        user_data = response.json()['user']
        token = generate_token(
            user_data['id'],
            user_data['username'],
            user_data.get('is_admin', False)
        )
        
        return jsonify({
            'token': token,
            'user': user_data,
            'expires_in': app.config['JWT_EXPIRATION_HOURS'] * 3600
        })
    
    return jsonify(response.json()), response.status_code

@app.route('/auth/refresh', methods=['POST'])
@token_required
def refresh_token():
    """Обновление JWT токена"""
    new_token = generate_token(
        g.current_user['user_id'],
        g.current_user['username'],
        g.current_user.get('is_admin', False)
    )
    
    return jsonify({
        'token': new_token,
        'expires_in': app.config['JWT_EXPIRATION_HOURS'] * 3600
    })

@app.route('/auth/verify', methods=['GET'])
@token_required
def verify():
    """Проверка валидности токена"""
    return jsonify({
        'valid': True,
        'user': g.current_user
    })

# Маршруты для турниров
@app.route('/api/tournaments', methods=['GET'])
@limiter.limit("100 per minute")
@cache_response(timeout=300)
def get_tournaments():
    """Получить список турниров"""
    return proxy_request('tournaments', '/tournaments', params=request.args)

@app.route('/api/tournaments/<int:tournament_id>', methods=['GET'])
@cache_response(timeout=600)
def get_tournament(tournament_id):
    """Получить турнир по ID"""
    return proxy_request('tournaments', f'/tournaments/{tournament_id}')

@app.route('/api/tournaments', methods=['POST'])
@admin_required
def create_tournament():
    """Создать турнир (только для администраторов)"""
    invalidate_cache_pattern('gateway_cache:/api/tournaments*')
    return proxy_request('tournaments', '/tournaments', method='POST', json=request.get_json())

@app.route('/api/tournaments/<int:tournament_id>', methods=['PUT'])
@admin_required
def update_tournament(tournament_id):
    """Обновить турнир (только для администраторов)"""
    invalidate_cache_pattern(f'gateway_cache:/api/tournaments/{tournament_id}*')
    invalidate_cache_pattern('gateway_cache:/api/tournaments*')
    return proxy_request('tournaments', f'/tournaments/{tournament_id}', method='PUT', json=request.get_json())

@app.route('/api/tournaments/<int:tournament_id>', methods=['DELETE'])
@admin_required
def delete_tournament(tournament_id):
    """Удалить турнир (только для администраторов)"""
    invalidate_cache_pattern('gateway_cache:/api/tournaments*')
    return proxy_request('tournaments', f'/tournaments/{tournament_id}', method='DELETE')

# Маршруты для пользователей
@app.route('/api/users', methods=['GET'])
@admin_required
def get_users():
    """Получить список пользователей (только для администраторов)"""
    return proxy_request('users', '/users', params=request.args)

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """Получить пользователя по ID"""
    # Пользователь может получить только свои данные, админ - любые
    if g.current_user['user_id'] != user_id and not g.current_user.get('is_admin', False):
        return jsonify({'error': 'Access denied'}), 403
    
    return proxy_request('users', f'/users/{user_id}')

@app.route('/api/users', methods=['POST'])
@limiter.limit("3 per hour")
def create_user():
    """Регистрация нового пользователя"""
    return proxy_request('users', '/users', method='POST', json=request.get_json())

@app.route('/api/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """Обновить пользователя"""
    if g.current_user['user_id'] != user_id and not g.current_user.get('is_admin', False):
        return jsonify({'error': 'Access denied'}), 403
    
    return proxy_request('users', f'/users/{user_id}', method='PUT', json=request.get_json())

# Маршруты для других сервисов
@app.route('/api/recommendations', methods=['GET'])
@token_required
@cache_response(timeout=600)
def get_recommendations():
    """Получить рекомендации для пользователя"""
    return proxy_request('recommendations', f"/recommendations/{g.current_user['user_id']}")

@app.route('/api/favorites', methods=['GET'])
@token_required
def get_favorites():
    """Получить избранные турниры пользователя"""
    return proxy_request('favorites', f"/favorites/{g.current_user['user_id']}")

@app.route('/api/notifications', methods=['GET'])
@token_required
def get_notifications():
    """Получить уведомления пользователя"""
    return proxy_request('notifications', f"/notifications/{g.current_user['user_id']}")

# Утилиты для инвалидации кэша
def invalidate_cache_pattern(pattern):
    """Инвалидировать кэш по паттерну"""
    if redis_client:
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
                logger.info(f"Invalidated {len(keys)} cache keys matching {pattern}")
        except Exception as e:
            logger.error(f"Cache invalidation error: {e}")

# Health check
@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния API Gateway"""
    services_health = {}
    
    for service_name, service_url in SERVICES.items():
        try:
            response = requests.get(f"{service_url}/health", timeout=2)
            services_health[service_name] = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            services_health[service_name] = {
                'status': 'unreachable',
                'error': str(e)
            }
    
    redis_status = 'healthy' if redis_client else 'unavailable'
    
    return jsonify({
        'status': 'healthy',
        'service': 'api-gateway',
        'timestamp': datetime.utcnow().isoformat(),
        'redis': redis_status,
        'services': services_health
    })

# Метрики
@app.route('/metrics', methods=['GET'])
@admin_required
def get_metrics():
    """Получить метрики API Gateway"""
    if not redis_client:
        return jsonify({'error': 'Redis unavailable'}), 503
    
    try:
        info = redis_client.info()
        return jsonify({
            'redis': {
                'connected_clients': info.get('connected_clients'),
                'used_memory': info.get('used_memory_human'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace': redis_client.dbsize()
            },
            'rate_limiter': {
                'enabled': True,
                'default_limits': limiter._default_limits
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Обработка ошибок
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': str(e.description)}), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
