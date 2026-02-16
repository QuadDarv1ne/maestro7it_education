"""
Система webhook для интеграций с внешними сервисами
"""
import requests
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from flask import current_app
import hashlib
import hmac

logger = logging.getLogger(__name__)


class WebhookManager:
    """Менеджер webhook уведомлений"""
    
    def __init__(self, app=None):
        self.app = app
        self.webhooks = {}
        self.secret_key = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация менеджера"""
        self.secret_key = app.config.get('WEBHOOK_SECRET_KEY', 'default_secret')
        logger.info("Webhook manager initialized")
    
    def register_webhook(self, event_type: str, url: str, 
                        headers: Dict[str, str] = None, 
                        enabled: bool = True):
        """Зарегистрировать webhook"""
        if event_type not in self.webhooks:
            self.webhooks[event_type] = []
        
        webhook = {
            'url': url,
            'headers': headers or {},
            'enabled': enabled,
            'created_at': datetime.utcnow(),
            'last_triggered': None,
            'success_count': 0,
            'failure_count': 0
        }
        
        self.webhooks[event_type].append(webhook)
        logger.info(f"Webhook registered: {event_type} -> {url}")
        
        return webhook
    
    def unregister_webhook(self, event_type: str, url: str):
        """Отменить регистрацию webhook"""
        if event_type in self.webhooks:
            self.webhooks[event_type] = [
                w for w in self.webhooks[event_type] 
                if w['url'] != url
            ]
            logger.info(f"Webhook unregistered: {event_type} -> {url}")
            return True
        return False
    
    def _generate_signature(self, payload: str) -> str:
        """Генерация подписи для webhook"""
        return hmac.new(
            self.secret_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def trigger_webhook(self, event_type: str, data: Dict[str, Any], 
                       timeout: int = 10) -> List[Dict[str, Any]]:
        """Отправить webhook уведомление"""
        if event_type not in self.webhooks:
            logger.debug(f"No webhooks registered for event: {event_type}")
            return []
        
        results = []
        
        for webhook in self.webhooks[event_type]:
            if not webhook['enabled']:
                continue
            
            try:
                # Подготовка payload
                payload = {
                    'event': event_type,
                    'timestamp': datetime.utcnow().isoformat(),
                    'data': data
                }
                
                payload_json = json.dumps(payload)
                signature = self._generate_signature(payload_json)
                
                # Подготовка заголовков
                headers = {
                    'Content-Type': 'application/json',
                    'X-Webhook-Signature': signature,
                    'X-Webhook-Event': event_type,
                    **webhook['headers']
                }
                
                # Отправка запроса
                response = requests.post(
                    webhook['url'],
                    data=payload_json,
                    headers=headers,
                    timeout=timeout
                )
                
                # Обновление статистики
                webhook['last_triggered'] = datetime.utcnow()
                
                if response.status_code == 200:
                    webhook['success_count'] += 1
                    logger.info(f"Webhook triggered successfully: {webhook['url']}")
                    
                    results.append({
                        'url': webhook['url'],
                        'success': True,
                        'status_code': response.status_code,
                        'response': response.text[:200]
                    })
                else:
                    webhook['failure_count'] += 1
                    logger.warning(
                        f"Webhook failed: {webhook['url']} "
                        f"(status: {response.status_code})"
                    )
                    
                    results.append({
                        'url': webhook['url'],
                        'success': False,
                        'status_code': response.status_code,
                        'error': response.text[:200]
                    })
                
            except requests.exceptions.Timeout:
                webhook['failure_count'] += 1
                logger.error(f"Webhook timeout: {webhook['url']}")
                
                results.append({
                    'url': webhook['url'],
                    'success': False,
                    'error': 'Request timeout'
                })
                
            except Exception as e:
                webhook['failure_count'] += 1
                logger.error(f"Webhook error: {webhook['url']} - {e}")
                
                results.append({
                    'url': webhook['url'],
                    'success': False,
                    'error': str(e)
                })
        
        return results
    
    def get_webhooks(self, event_type: Optional[str] = None) -> Dict[str, List[Dict]]:
        """Получить список зарегистрированных webhooks"""
        if event_type:
            return {event_type: self.webhooks.get(event_type, [])}
        return self.webhooks
    
    def get_webhook_stats(self) -> Dict[str, Any]:
        """Получить статистику webhooks"""
        total_webhooks = sum(len(hooks) for hooks in self.webhooks.values())
        total_success = sum(
            w['success_count'] 
            for hooks in self.webhooks.values() 
            for w in hooks
        )
        total_failures = sum(
            w['failure_count'] 
            for hooks in self.webhooks.values() 
            for w in hooks
        )
        
        return {
            'total_webhooks': total_webhooks,
            'event_types': list(self.webhooks.keys()),
            'total_success': total_success,
            'total_failures': total_failures,
            'success_rate': round(
                (total_success / (total_success + total_failures) * 100) 
                if (total_success + total_failures) > 0 else 0, 
                2
            )
        }


# Предопределенные события
class WebhookEvents:
    """Типы событий для webhooks"""
    
    # Пользователи
    USER_CREATED = 'user.created'
    USER_UPDATED = 'user.updated'
    USER_DELETED = 'user.deleted'
    USER_LOGIN = 'user.login'
    USER_LOGOUT = 'user.logout'
    PASSWORD_CHANGED = 'user.password_changed'
    
    # Турниры
    TOURNAMENT_CREATED = 'tournament.created'
    TOURNAMENT_UPDATED = 'tournament.updated'
    TOURNAMENT_DELETED = 'tournament.deleted'
    TOURNAMENT_STARTED = 'tournament.started'
    TOURNAMENT_ENDED = 'tournament.ended'
    
    # Безопасность
    SECURITY_ALERT = 'security.alert'
    ACCOUNT_LOCKED = 'security.account_locked'
    SUSPICIOUS_ACTIVITY = 'security.suspicious_activity'


# Глобальный экземпляр
webhook_manager = WebhookManager()


# Вспомогательные функции

def trigger_user_created(user_data: Dict[str, Any]):
    """Отправить webhook о создании пользователя"""
    return webhook_manager.trigger_webhook(
        WebhookEvents.USER_CREATED,
        user_data
    )


def trigger_tournament_created(tournament_data: Dict[str, Any]):
    """Отправить webhook о создании турнира"""
    return webhook_manager.trigger_webhook(
        WebhookEvents.TOURNAMENT_CREATED,
        tournament_data
    )


def trigger_security_alert(alert_data: Dict[str, Any]):
    """Отправить webhook о событии безопасности"""
    return webhook_manager.trigger_webhook(
        WebhookEvents.SECURITY_ALERT,
        alert_data
    )
