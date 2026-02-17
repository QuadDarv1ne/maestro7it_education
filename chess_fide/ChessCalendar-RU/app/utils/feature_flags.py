"""
Система feature flags для управления функциональностью
"""
import logging
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from enum import Enum
import redis

logger = logging.getLogger(__name__)


class FeatureFlagStatus(Enum):
    """Статусы feature flags"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    ROLLOUT = "rollout"  # Постепенное включение


class FeatureFlagManager:
    """Менеджер feature flags"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis = redis_client
        self.flags = {}
        self.rollout_strategies = {}
        
        # Дефолтные флаги
        self._init_default_flags()
    
    def _init_default_flags(self):
        """Инициализация дефолтных флагов"""
        self.flags = {
            'enable_ab_testing': True,
            'enable_analytics': True,
            'enable_recommendations': True,
            'enable_websockets': True,
            'enable_email_notifications': False,
            'enable_push_notifications': False,
            'enable_advanced_search': False,
            'enable_tournament_ratings': True,
            'enable_user_profiles': True,
            'enable_forum': True,
            'maintenance_mode': False,
            'read_only_mode': False
        }
    
    def is_enabled(
        self,
        flag_name: str,
        user_id: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> bool:
        """
        Проверить, включен ли флаг
        
        Args:
            flag_name: имя флага
            user_id: ID пользователя (для rollout)
            context: дополнительный контекст
            
        Returns:
            True если флаг включен
        """
        # Проверяем в Redis (если доступен)
        if self.redis:
            try:
                redis_value = self.redis.get(f"feature_flag:{flag_name}")
                if redis_value is not None:
                    return redis_value.decode() == 'true'
            except Exception as e:
                logger.warning(f"Failed to get flag from Redis: {e}")
        
        # Проверяем локальное значение
        if flag_name not in self.flags:
            logger.warning(f"Unknown feature flag: {flag_name}")
            return False
        
        flag_value = self.flags[flag_name]
        
        # Простое булево значение
        if isinstance(flag_value, bool):
            return flag_value
        
        # Rollout стратегия
        if isinstance(flag_value, dict):
            return self._check_rollout(flag_name, flag_value, user_id, context)
        
        return False
    
    def _check_rollout(
        self,
        flag_name: str,
        config: Dict,
        user_id: Optional[str],
        context: Optional[Dict]
    ) -> bool:
        """Проверка rollout стратегии"""
        strategy = config.get('strategy', 'percentage')
        
        if strategy == 'percentage':
            return self._check_percentage_rollout(config, user_id)
        elif strategy == 'whitelist':
            return self._check_whitelist(config, user_id)
        elif strategy == 'custom':
            return self._check_custom_strategy(flag_name, config, user_id, context)
        
        return False
    
    def _check_percentage_rollout(self, config: Dict, user_id: Optional[str]) -> bool:
        """Проверка процентного rollout"""
        if not user_id:
            return False
        
        percentage = config.get('percentage', 0)
        
        # Используем хэш user_id для детерминированного результата
        user_hash = hash(user_id) % 100
        return user_hash < percentage
    
    def _check_whitelist(self, config: Dict, user_id: Optional[str]) -> bool:
        """Проверка whitelist"""
        if not user_id:
            return False
        
        whitelist = config.get('whitelist', [])
        return user_id in whitelist
    
    def _check_custom_strategy(
        self,
        flag_name: str,
        config: Dict,
        user_id: Optional[str],
        context: Optional[Dict]
    ) -> bool:
        """Проверка пользовательской стратегии"""
        strategy_func = self.rollout_strategies.get(flag_name)
        
        if not strategy_func:
            logger.warning(f"No custom strategy for flag: {flag_name}")
            return False
        
        try:
            return strategy_func(user_id, context)
        except Exception as e:
            logger.error(f"Custom strategy error for {flag_name}: {e}")
            return False
    
    def enable(self, flag_name: str, persist: bool = True):
        """Включить флаг"""
        self.flags[flag_name] = True
        
        if persist and self.redis:
            try:
                self.redis.set(f"feature_flag:{flag_name}", 'true')
            except Exception as e:
                logger.error(f"Failed to persist flag: {e}")
        
        logger.info(f"Feature flag '{flag_name}' enabled")
    
    def disable(self, flag_name: str, persist: bool = True):
        """Отключить флаг"""
        self.flags[flag_name] = False
        
        if persist and self.redis:
            try:
                self.redis.set(f"feature_flag:{flag_name}", 'false')
            except Exception as e:
                logger.error(f"Failed to persist flag: {e}")
        
        logger.info(f"Feature flag '{flag_name}' disabled")
    
    def set_rollout(
        self,
        flag_name: str,
        strategy: str,
        config: Dict,
        persist: bool = True
    ):
        """
        Установить rollout стратегию
        
        Args:
            flag_name: имя флага
            strategy: тип стратегии (percentage, whitelist, custom)
            config: конфигурация стратегии
            persist: сохранить в Redis
        """
        rollout_config = {
            'strategy': strategy,
            **config
        }
        
        self.flags[flag_name] = rollout_config
        
        if persist and self.redis:
            try:
                import json
                self.redis.set(
                    f"feature_flag:{flag_name}",
                    json.dumps(rollout_config)
                )
            except Exception as e:
                logger.error(f"Failed to persist rollout config: {e}")
        
        logger.info(f"Feature flag '{flag_name}' set to rollout: {strategy}")
    
    def register_custom_strategy(
        self,
        flag_name: str,
        strategy_func: Callable[[Optional[str], Optional[Dict]], bool]
    ):
        """
        Зарегистрировать пользовательскую стратегию
        
        Args:
            flag_name: имя флага
            strategy_func: функция стратегии (user_id, context) -> bool
        """
        self.rollout_strategies[flag_name] = strategy_func
        logger.info(f"Custom strategy registered for '{flag_name}'")
    
    def get_all_flags(self) -> Dict[str, Any]:
        """Получить все флаги"""
        return self.flags.copy()
    
    def get_flag_status(self, flag_name: str) -> Dict[str, Any]:
        """Получить статус флага"""
        if flag_name not in self.flags:
            return {'exists': False}
        
        flag_value = self.flags[flag_name]
        
        if isinstance(flag_value, bool):
            return {
                'exists': True,
                'type': 'boolean',
                'enabled': flag_value
            }
        elif isinstance(flag_value, dict):
            return {
                'exists': True,
                'type': 'rollout',
                'strategy': flag_value.get('strategy'),
                'config': flag_value
            }
        
        return {'exists': True, 'type': 'unknown'}


def feature_flag(flag_name: str, default: bool = False):
    """
    Декоратор для защиты функции feature flag
    
    Args:
        flag_name: имя флага
        default: значение по умолчанию если флаг не найден
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            from flask import g
            
            # Получаем менеджер флагов
            flag_manager = getattr(g, 'feature_flag_manager', None)
            
            if not flag_manager:
                # Создаем временный менеджер
                flag_manager = FeatureFlagManager()
            
            # Получаем user_id из контекста
            user_id = None
            if hasattr(g, 'current_user'):
                user_id = str(g.current_user.id)
            
            # Проверяем флаг
            if flag_manager.is_enabled(flag_name, user_id):
                return func(*args, **kwargs)
            else:
                from flask import jsonify
                return jsonify({
                    'error': 'Feature not available',
                    'message': f'Feature {flag_name} is not enabled'
                }), 403
        
        return wrapper
    return decorator


class FeatureFlagMiddleware:
    """Middleware для feature flags"""
    
    def __init__(self, app=None, redis_client=None):
        self.app = app
        self.manager = FeatureFlagManager(redis_client)
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        app.before_request(self.before_request)
        
        # Добавляем endpoint для управления флагами
        @app.route('/admin/feature-flags', methods=['GET'])
        def get_feature_flags():
            from flask import jsonify
            return jsonify(self.manager.get_all_flags())
        
        @app.route('/admin/feature-flags/<flag_name>', methods=['POST'])
        def toggle_feature_flag(flag_name):
            from flask import request, jsonify
            
            action = request.json.get('action')
            
            if action == 'enable':
                self.manager.enable(flag_name)
            elif action == 'disable':
                self.manager.disable(flag_name)
            else:
                return jsonify({'error': 'Invalid action'}), 400
            
            return jsonify({
                'flag': flag_name,
                'status': self.manager.get_flag_status(flag_name)
            })
    
    def before_request(self):
        """Добавить менеджер флагов в контекст запроса"""
        from flask import g
        g.feature_flag_manager = self.manager


# Глобальный экземпляр
feature_flag_manager = FeatureFlagManager()
