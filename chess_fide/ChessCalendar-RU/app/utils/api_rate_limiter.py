"""
Продвинутый rate limiting для API
"""
import logging
import time
from typing import Optional, Callable
from functools import wraps
from flask import request, jsonify, g
import redis
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RateLimitExceeded(Exception):
    """Исключение при превышении лимита"""
    pass


class AdvancedRateLimiter:
    """
    Продвинутый rate limiter с поддержкой:
    - Скользящего окна
    - Разных лимитов для разных пользователей
    - Burst режима
    - Whitelist/Blacklist
    """
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.whitelist = set()
        self.blacklist = set()
    
    def add_to_whitelist(self, identifier: str):
        """Добавить в whitelist (без ограничений)"""
        self.whitelist.add(identifier)
        logger.info(f"Added {identifier} to whitelist")
    
    def add_to_blacklist(self, identifier: str):
        """Добавить в blacklist (полный запрет)"""
        self.blacklist.add(identifier)
        logger.info(f"Added {identifier} to blacklist")
    
    def is_allowed(self, identifier: str, limit: int, window: int, 
                   burst_limit: Optional[int] = None) -> tuple[bool, dict]:
        """
        Проверить, разрешен ли запрос
        
        Args:
            identifier: уникальный идентификатор (IP, user_id, API key)
            limit: максимальное количество запросов
            window: временное окно в секундах
            burst_limit: максимальное количество запросов в burst режиме
            
        Returns:
            (allowed, info) - разрешен ли запрос и информация о лимитах
        """
        # Проверка whitelist
        if identifier in self.whitelist:
            return True, {'whitelisted': True}
        
        # Проверка blacklist
        if identifier in self.blacklist:
            return False, {'blacklisted': True, 'reason': 'Blocked'}
        
        key = f"rate_limit:{identifier}"
        now = time.time()
        
        try:
            # Используем sorted set для скользящего окна
            pipe = self.redis.pipeline()
            
            # Удаляем старые записи
            pipe.zremrangebyscore(key, 0, now - window)
            
            # Получаем текущее количество запросов
            pipe.zcard(key)
            
            # Добавляем текущий запрос
            pipe.zadd(key, {str(now): now})
            
            # Устанавливаем TTL
            pipe.expire(key, window)
            
            results = pipe.execute()
            current_count = results[1]
            
            # Проверка burst лимита
            if burst_limit:
                burst_key = f"rate_limit_burst:{identifier}"
                burst_count = self.redis.get(burst_key)
                
                if burst_count and int(burst_count) >= burst_limit:
                    return False, {
                        'allowed': False,
                        'reason': 'Burst limit exceeded',
                        'burst_limit': burst_limit,
                        'retry_after': 60
                    }
            
            # Проверка основного лимита
            if current_count > limit:
                # Вычисляем время до сброса
                oldest = self.redis.zrange(key, 0, 0, withscores=True)
                if oldest:
                    retry_after = int(oldest[0][1] + window - now)
                else:
                    retry_after = window
                
                return False, {
                    'allowed': False,
                    'limit': limit,
                    'remaining': 0,
                    'reset': int(now + retry_after),
                    'retry_after': retry_after
                }
            
            return True, {
                'allowed': True,
                'limit': limit,
                'remaining': limit - current_count,
                'reset': int(now + window)
            }
            
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            # В случае ошибки разрешаем запрос
            return True, {'error': str(e)}
    
    def increment_burst(self, identifier: str, ttl: int = 60):
        """Увеличить счетчик burst запросов"""
        try:
            burst_key = f"rate_limit_burst:{identifier}"
            pipe = self.redis.pipeline()
            pipe.incr(burst_key)
            pipe.expire(burst_key, ttl)
            pipe.execute()
        except Exception as e:
            logger.error(f"Failed to increment burst counter: {e}")
    
    def reset_limit(self, identifier: str):
        """Сбросить лимит для идентификатора"""
        try:
            key = f"rate_limit:{identifier}"
            burst_key = f"rate_limit_burst:{identifier}"
            self.redis.delete(key, burst_key)
            logger.info(f"Rate limit reset for {identifier}")
        except Exception as e:
            logger.error(f"Failed to reset limit: {e}")
    
    def get_stats(self, identifier: str) -> dict:
        """Получить статистику по идентификатору"""
        try:
            key = f"rate_limit:{identifier}"
            count = self.redis.zcard(key)
            
            if count > 0:
                oldest = self.redis.zrange(key, 0, 0, withscores=True)
                newest = self.redis.zrange(key, -1, -1, withscores=True)
                
                return {
                    'identifier': identifier,
                    'current_count': count,
                    'first_request': datetime.fromtimestamp(oldest[0][1]).isoformat(),
                    'last_request': datetime.fromtimestamp(newest[0][1]).isoformat()
                }
            
            return {
                'identifier': identifier,
                'current_count': 0
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}


class TieredRateLimiter:
    """Rate limiter с уровнями доступа"""
    
    TIERS = {
        'free': {'requests': 100, 'window': 3600},      # 100 req/hour
        'basic': {'requests': 1000, 'window': 3600},    # 1000 req/hour
        'premium': {'requests': 10000, 'window': 3600}, # 10000 req/hour
        'unlimited': {'requests': 999999, 'window': 3600}
    }
    
    def __init__(self, redis_client: redis.Redis):
        self.limiter = AdvancedRateLimiter(redis_client)
    
    def check_limit(self, identifier: str, tier: str = 'free') -> tuple[bool, dict]:
        """Проверить лимит для определенного уровня"""
        tier_config = self.TIERS.get(tier, self.TIERS['free'])
        return self.limiter.is_allowed(
            identifier,
            tier_config['requests'],
            tier_config['window']
        )


def rate_limit(limit: int = 100, window: int = 3600, 
               key_func: Optional[Callable] = None,
               error_message: str = "Rate limit exceeded"):
    """
    Декоратор для rate limiting
    
    Args:
        limit: максимальное количество запросов
        window: временное окно в секундах
        key_func: функция для получения ключа (по умолчанию IP)
        error_message: сообщение об ошибке
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Получаем идентификатор
            if key_func:
                identifier = key_func()
            else:
                identifier = request.remote_addr
            
            # Проверяем лимит
            from app import create_app
            app = create_app()
            
            try:
                import redis
                redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/0')
                redis_client = redis.from_url(redis_url)
                
                limiter = AdvancedRateLimiter(redis_client)
                allowed, info = limiter.is_allowed(identifier, limit, window)
                
                # Добавляем заголовки
                g.rate_limit_info = info
                
                if not allowed:
                    response = jsonify({
                        'error': error_message,
                        'limit': info.get('limit'),
                        'retry_after': info.get('retry_after')
                    })
                    response.status_code = 429
                    response.headers['X-RateLimit-Limit'] = str(limit)
                    response.headers['X-RateLimit-Remaining'] = '0'
                    response.headers['X-RateLimit-Reset'] = str(info.get('reset', 0))
                    response.headers['Retry-After'] = str(info.get('retry_after', window))
                    return response
                
            except Exception as e:
                logger.error(f"Rate limiting error: {e}")
                # В случае ошибки разрешаем запрос
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def add_rate_limit_headers(response):
    """Добавить заголовки rate limit к ответу"""
    if hasattr(g, 'rate_limit_info'):
        info = g.rate_limit_info
        response.headers['X-RateLimit-Limit'] = str(info.get('limit', 0))
        response.headers['X-RateLimit-Remaining'] = str(info.get('remaining', 0))
        response.headers['X-RateLimit-Reset'] = str(info.get('reset', 0))
    
    return response


class IPBlocker:
    """Блокировка IP адресов"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def block_ip(self, ip: str, duration: int = 3600, reason: str = ""):
        """Заблокировать IP"""
        try:
            key = f"blocked_ip:{ip}"
            self.redis.setex(key, duration, reason or "Blocked")
            logger.warning(f"IP {ip} blocked for {duration}s: {reason}")
        except Exception as e:
            logger.error(f"Failed to block IP: {e}")
    
    def unblock_ip(self, ip: str):
        """Разблокировать IP"""
        try:
            key = f"blocked_ip:{ip}"
            self.redis.delete(key)
            logger.info(f"IP {ip} unblocked")
        except Exception as e:
            logger.error(f"Failed to unblock IP: {e}")
    
    def is_blocked(self, ip: str) -> tuple[bool, str]:
        """Проверить, заблокирован ли IP"""
        try:
            key = f"blocked_ip:{ip}"
            reason = self.redis.get(key)
            if reason:
                return True, reason.decode() if isinstance(reason, bytes) else reason
            return False, ""
        except Exception as e:
            logger.error(f"Failed to check IP block: {e}")
            return False, ""
    
    def auto_block_on_abuse(self, ip: str, threshold: int = 10, 
                           window: int = 60, block_duration: int = 3600):
        """Автоматическая блокировка при превышении порога"""
        try:
            key = f"abuse_counter:{ip}"
            count = self.redis.incr(key)
            
            if count == 1:
                self.redis.expire(key, window)
            
            if count >= threshold:
                self.block_ip(ip, block_duration, f"Auto-blocked: {count} requests in {window}s")
                self.redis.delete(key)
                return True
            
            return False
        except Exception as e:
            logger.error(f"Failed to check abuse: {e}")
            return False


class APIKeyManager:
    """Управление API ключами"""
    
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
    
    def create_api_key(self, user_id: str, tier: str = 'free', 
                      expires_in: Optional[int] = None) -> str:
        """Создать API ключ"""
        import secrets
        api_key = f"sk_{secrets.token_urlsafe(32)}"
        
        try:
            key = f"api_key:{api_key}"
            data = {
                'user_id': user_id,
                'tier': tier,
                'created_at': datetime.utcnow().isoformat()
            }
            
            if expires_in:
                self.redis.setex(key, expires_in, str(data))
            else:
                self.redis.set(key, str(data))
            
            logger.info(f"API key created for user {user_id}")
            return api_key
        except Exception as e:
            logger.error(f"Failed to create API key: {e}")
            return ""
    
    def validate_api_key(self, api_key: str) -> Optional[dict]:
        """Проверить API ключ"""
        try:
            key = f"api_key:{api_key}"
            data = self.redis.get(key)
            
            if data:
                import ast
                return ast.literal_eval(data.decode() if isinstance(data, bytes) else data)
            
            return None
        except Exception as e:
            logger.error(f"Failed to validate API key: {e}")
            return None
    
    def revoke_api_key(self, api_key: str):
        """Отозвать API ключ"""
        try:
            key = f"api_key:{api_key}"
            self.redis.delete(key)
            logger.info(f"API key revoked: {api_key}")
        except Exception as e:
            logger.error(f"Failed to revoke API key: {e}")
