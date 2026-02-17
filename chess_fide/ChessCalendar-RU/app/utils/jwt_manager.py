"""
Управление JWT токенами с refresh механизмом
"""
import jwt
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Tuple
from functools import wraps
from flask import request, jsonify, g
import redis

logger = logging.getLogger(__name__)


class JWTManager:
    """Менеджер JWT токенов"""
    
    def __init__(
        self,
        secret_key: str,
        algorithm: str = 'HS256',
        access_token_expires: int = 3600,  # 1 час
        refresh_token_expires: int = 2592000,  # 30 дней
        redis_client: Optional[redis.Redis] = None
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expires = access_token_expires
        self.refresh_token_expires = refresh_token_expires
        self.redis = redis_client
    
    def create_access_token(
        self,
        user_id: str,
        additional_claims: Optional[Dict] = None
    ) -> str:
        """
        Создать access token
        
        Args:
            user_id: ID пользователя
            additional_claims: дополнительные claims
            
        Returns:
            JWT токен
        """
        now = datetime.utcnow()
        expires = now + timedelta(seconds=self.access_token_expires)
        
        payload = {
            'user_id': user_id,
            'type': 'access',
            'iat': now,
            'exp': expires,
            'jti': self._generate_jti()
        }
        
        if additional_claims:
            payload.update(additional_claims)
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        logger.info(f"Access token created for user {user_id}")
        return token
    
    def create_refresh_token(
        self,
        user_id: str,
        additional_claims: Optional[Dict] = None
    ) -> str:
        """
        Создать refresh token
        
        Args:
            user_id: ID пользователя
            additional_claims: дополнительные claims
            
        Returns:
            JWT токен
        """
        now = datetime.utcnow()
        expires = now + timedelta(seconds=self.refresh_token_expires)
        
        payload = {
            'user_id': user_id,
            'type': 'refresh',
            'iat': now,
            'exp': expires,
            'jti': self._generate_jti()
        }
        
        if additional_claims:
            payload.update(additional_claims)
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        # Сохраняем refresh token в Redis
        if self.redis:
            try:
                key = f"refresh_token:{user_id}:{payload['jti']}"
                self.redis.setex(key, self.refresh_token_expires, token)
            except Exception as e:
                logger.error(f"Failed to store refresh token: {e}")
        
        logger.info(f"Refresh token created for user {user_id}")
        return token
    
    def create_token_pair(
        self,
        user_id: str,
        additional_claims: Optional[Dict] = None
    ) -> Tuple[str, str]:
        """
        Создать пару токенов (access + refresh)
        
        Returns:
            (access_token, refresh_token)
        """
        access_token = self.create_access_token(user_id, additional_claims)
        refresh_token = self.create_refresh_token(user_id, additional_claims)
        
        return access_token, refresh_token
    
    def verify_token(
        self,
        token: str,
        token_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Проверить токен
        
        Args:
            token: JWT токен
            token_type: ожидаемый тип токена (access/refresh)
            
        Returns:
            payload токена
            
        Raises:
            jwt.ExpiredSignatureError: токен истек
            jwt.InvalidTokenError: невалидный токен
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            # Проверка типа токена
            if token_type and payload.get('type') != token_type:
                raise jwt.InvalidTokenError(f"Expected {token_type} token")
            
            # Проверка в blacklist
            if self._is_blacklisted(payload.get('jti')):
                raise jwt.InvalidTokenError("Token has been revoked")
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            raise
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            raise
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Обновить access token используя refresh token
        
        Args:
            refresh_token: refresh токен
            
        Returns:
            новый access token
        """
        # Проверяем refresh token
        payload = self.verify_token(refresh_token, token_type='refresh')
        user_id = payload['user_id']
        
        # Проверяем что refresh token существует в Redis
        if self.redis:
            try:
                key = f"refresh_token:{user_id}:{payload['jti']}"
                if not self.redis.exists(key):
                    raise jwt.InvalidTokenError("Refresh token not found")
            except Exception as e:
                logger.error(f"Failed to verify refresh token: {e}")
        
        # Создаем новый access token
        additional_claims = {
            k: v for k, v in payload.items()
            if k not in ['user_id', 'type', 'iat', 'exp', 'jti']
        }
        
        return self.create_access_token(user_id, additional_claims)
    
    def revoke_token(self, token: str):
        """
        Отозвать токен (добавить в blacklist)
        
        Args:
            token: JWT токен
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={'verify_exp': False}  # Не проверяем истечение
            )
            
            jti = payload.get('jti')
            if not jti:
                logger.warning("Token has no jti claim")
                return
            
            # Добавляем в blacklist
            if self.redis:
                try:
                    # TTL = оставшееся время жизни токена
                    exp = payload.get('exp')
                    if exp:
                        ttl = max(0, exp - datetime.utcnow().timestamp())
                        self.redis.setex(f"blacklist:{jti}", int(ttl), '1')
                        logger.info(f"Token {jti} revoked")
                except Exception as e:
                    logger.error(f"Failed to blacklist token: {e}")
            
        except jwt.InvalidTokenError as e:
            logger.error(f"Failed to revoke token: {e}")
    
    def revoke_all_user_tokens(self, user_id: str):
        """
        Отозвать все токены пользователя
        
        Args:
            user_id: ID пользователя
        """
        if not self.redis:
            logger.warning("Redis not available, cannot revoke tokens")
            return
        
        try:
            # Удаляем все refresh токены пользователя
            pattern = f"refresh_token:{user_id}:*"
            keys = self.redis.keys(pattern)
            
            if keys:
                self.redis.delete(*keys)
                logger.info(f"Revoked {len(keys)} tokens for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to revoke user tokens: {e}")
    
    def _generate_jti(self) -> str:
        """Генерация уникального ID токена"""
        import uuid
        return str(uuid.uuid4())
    
    def _is_blacklisted(self, jti: Optional[str]) -> bool:
        """Проверка в blacklist"""
        if not jti or not self.redis:
            return False
        
        try:
            return self.redis.exists(f"blacklist:{jti}") > 0
        except Exception as e:
            logger.error(f"Failed to check blacklist: {e}")
            return False
    
    def decode_token_without_verification(self, token: str) -> Dict[str, Any]:
        """
        Декодировать токен без проверки подписи
        Полезно для отладки
        """
        try:
            return jwt.decode(
                token,
                options={'verify_signature': False}
            )
        except Exception as e:
            logger.error(f"Failed to decode token: {e}")
            return {}


def jwt_required(optional: bool = False):
    """
    Декоратор для защиты endpoint JWT
    
    Args:
        optional: токен опционален
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем токен из заголовка
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                if optional:
                    g.current_user = None
                    return func(*args, **kwargs)
                
                return jsonify({
                    'error': 'Missing authorization header',
                    'message': 'Authorization header is required'
                }), 401
            
            # Парсим токен
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({
                    'error': 'Invalid authorization header',
                    'message': 'Format: Bearer <token>'
                }), 401
            
            token = parts[1]
            
            # Проверяем токен
            try:
                from flask import current_app
                jwt_manager = JWTManager(
                    secret_key=current_app.config['SECRET_KEY']
                )
                
                payload = jwt_manager.verify_token(token, token_type='access')
                
                # Загружаем пользователя
                from app.models.user import User
                user = User.query.get(payload['user_id'])
                
                if not user:
                    return jsonify({
                        'error': 'User not found',
                        'message': 'Token is valid but user does not exist'
                    }), 401
                
                if not user.is_active:
                    return jsonify({
                        'error': 'User inactive',
                        'message': 'Your account has been deactivated'
                    }), 401
                
                # Сохраняем пользователя в контексте
                g.current_user = user
                g.token_payload = payload
                
                return func(*args, **kwargs)
                
            except jwt.ExpiredSignatureError:
                return jsonify({
                    'error': 'Token expired',
                    'message': 'Your token has expired. Please refresh.'
                }), 401
            except jwt.InvalidTokenError as e:
                return jsonify({
                    'error': 'Invalid token',
                    'message': str(e)
                }), 401
            except Exception as e:
                logger.error(f"JWT verification error: {e}")
                return jsonify({
                    'error': 'Authentication failed',
                    'message': 'An error occurred during authentication'
                }), 500
        
        return wrapper
    return decorator


def admin_required():
    """Декоратор для проверки прав администратора"""
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            if not g.current_user.is_admin:
                return jsonify({
                    'error': 'Admin access required',
                    'message': 'You do not have permission to access this resource'
                }), 403
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def get_current_user():
    """Получить текущего пользователя из контекста"""
    return getattr(g, 'current_user', None)


def get_token_payload():
    """Получить payload токена из контекста"""
    return getattr(g, 'token_payload', None)
