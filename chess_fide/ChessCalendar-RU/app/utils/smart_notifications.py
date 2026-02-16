"""
Система умных уведомлений с приоритетами
Интеллектуальная отправка уведомлений на основе предпочтений пользователя
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum


class NotificationPriority(Enum):
    """Приоритеты уведомлений"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class NotificationChannel(Enum):
    """Каналы доставки уведомлений"""
    EMAIL = 'email'
    PUSH = 'push'
    SMS = 'sms'
    IN_APP = 'in_app'
    TELEGRAM = 'telegram'


class SmartNotificationEngine:
    """Движок умных уведомлений"""
    
    def __init__(self):
        self.notification_rules = {}
        self.user_preferences = {}
        self.delivery_stats = {}
    
    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        data: Optional[Dict[str, Any]] = None,
        scheduled_for: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Создать умное уведомление
        
        Args:
            user_id: ID пользователя
            title: Заголовок
            message: Текст сообщения
            notification_type: Тип уведомления
            priority: Приоритет
            data: Дополнительные данные
            scheduled_for: Время отправки (опционально)
        """
        from app.models.notification import Notification
        
        # Определение оптимального канала доставки
        channels = self._determine_delivery_channels(
            user_id, notification_type, priority
        )
        
        # Определение оптимального времени отправки
        if scheduled_for is None and priority != NotificationPriority.URGENT:
            scheduled_for = self._determine_optimal_time(user_id)
        
        # Создание уведомления
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            priority=priority.value,
            channels=','.join([c.value for c in channels]),
            data=data,
            scheduled_for=scheduled_for,
            created_at=datetime.utcnow()
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # Немедленная отправка для срочных уведомлений
        if priority == NotificationPriority.URGENT:
            self._send_notification(notification, channels)
        
        return {
            'notification_id': notification.id,
            'channels': [c.value for c in channels],
            'scheduled_for': scheduled_for.isoformat() if scheduled_for else None,
            'status': 'created'
        }
    
    def _determine_delivery_channels(
        self,
        user_id: int,
        notification_type: str,
        priority: NotificationPriority
    ) -> List[NotificationChannel]:
        """
        Определить оптимальные каналы доставки
        
        Основано на:
        - Предпочтениях пользователя
        - Приоритете уведомления
        - Истории взаимодействий
        """
        # Получение предпочтений пользователя
        preferences = self._get_user_preferences(user_id)
        
        channels = []
        
        # Срочные уведомления - все доступные каналы
        if priority == NotificationPriority.URGENT:
            if preferences.get('email_enabled', True):
                channels.append(NotificationChannel.EMAIL)
            if preferences.get('push_enabled', True):
                channels.append(NotificationChannel.PUSH)
            if preferences.get('telegram_enabled', False):
                channels.append(NotificationChannel.TELEGRAM)
            channels.append(NotificationChannel.IN_APP)
        
        # Высокий приоритет - email + push + in-app
        elif priority == NotificationPriority.HIGH:
            if preferences.get('email_enabled', True):
                channels.append(NotificationChannel.EMAIL)
            if preferences.get('push_enabled', True):
                channels.append(NotificationChannel.PUSH)
            channels.append(NotificationChannel.IN_APP)
        
        # Средний приоритет - push + in-app
        elif priority == NotificationPriority.MEDIUM:
            if preferences.get('push_enabled', True):
                channels.append(NotificationChannel.PUSH)
            channels.append(NotificationChannel.IN_APP)
        
        # Низкий приоритет - только in-app
        else:
            channels.append(NotificationChannel.IN_APP)
        
        # Фильтрация по типу уведомления
        type_preferences = preferences.get('notification_types', {})
        if notification_type in type_preferences:
            allowed_channels = type_preferences[notification_type].get('channels', [])
            if allowed_channels:
                channels = [c for c in channels if c.value in allowed_channels]
        
        return channels if channels else [NotificationChannel.IN_APP]
    
    def _determine_optimal_time(self, user_id: int) -> datetime:
        """
        Определить оптимальное время отправки
        
        Анализирует:
        - Историю активности пользователя
        - Часовой пояс
        - Предпочтения по времени
        """
        from app.models.user import User
        
        user = User.query.get(user_id)
        if not user:
            return datetime.utcnow()
        
        # Анализ истории активности
        activity_hours = self._analyze_user_activity(user_id)
        
        now = datetime.utcnow()
        current_hour = now.hour
        
        # Если текущий час - активное время, отправляем сейчас
        if current_hour in activity_hours[:3]:  # Топ-3 активных часа
            return now
        
        # Иначе откладываем на следующий активный час
        next_active_hour = activity_hours[0] if activity_hours else 9
        
        if next_active_hour > current_hour:
            # Сегодня
            scheduled = now.replace(hour=next_active_hour, minute=0, second=0)
        else:
            # Завтра
            scheduled = (now + timedelta(days=1)).replace(
                hour=next_active_hour, minute=0, second=0
            )
        
        return scheduled
    
    def _analyze_user_activity(self, user_id: int) -> List[int]:
        """
        Анализ активности пользователя по часам
        
        Returns:
            Список часов, отсортированных по активности (от самого активного)
        """
        from app.models.notification import Notification
        from sqlalchemy import func, extract
        
        # Получение статистики взаимодействий с уведомлениями
        activity = db.session.query(
            extract('hour', Notification.read_at).label('hour'),
            func.count(Notification.id).label('count')
        ).filter(
            Notification.user_id == user_id,
            Notification.read_at.isnot(None),
            Notification.read_at >= datetime.utcnow() - timedelta(days=30)
        ).group_by('hour').order_by(func.count(Notification.id).desc()).all()
        
        if activity:
            return [int(hour) for hour, _ in activity]
        
        # Дефолтные активные часы (9:00, 14:00, 19:00)
        return [9, 14, 19]
    
    def _get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Получить предпочтения пользователя по уведомлениям"""
        from app.models.preference import UserPreference
        
        if user_id in self.user_preferences:
            return self.user_preferences[user_id]
        
        preference = UserPreference.query.filter_by(user_id=user_id).first()
        
        if preference and preference.notification_settings:
            prefs = preference.notification_settings
        else:
            # Дефолтные настройки
            prefs = {
                'email_enabled': True,
                'push_enabled': True,
                'telegram_enabled': False,
                'notification_types': {}
            }
        
        self.user_preferences[user_id] = prefs
        return prefs
    
    def _send_notification(
        self,
        notification: Any,
        channels: List[NotificationChannel]
    ):
        """Отправить уведомление через указанные каналы"""
        for channel in channels:
            try:
                if channel == NotificationChannel.EMAIL:
                    self._send_email(notification)
                elif channel == NotificationChannel.PUSH:
                    self._send_push(notification)
                elif channel == NotificationChannel.TELEGRAM:
                    self._send_telegram(notification)
                elif channel == NotificationChannel.IN_APP:
                    # In-app уведомления уже сохранены в БД
                    pass
            except Exception as e:
                import logging
                logging.error(f"Failed to send notification via {channel.value}: {e}")
    
    def _send_email(self, notification: Any):
        """Отправить email уведомление"""
        from app.utils.email_notifications import email_service
        from app.models.user import User
        
        user = User.query.get(notification.user_id)
        if user and user.email:
            email_service.send_notification_email(
                user.email,
                notification.title,
                notification.message
            )
    
    def _send_push(self, notification: Any):
        """Отправить push уведомление"""
        # Интеграция с push-сервисом (Firebase, OneSignal и т.д.)
        pass
    
    def _send_telegram(self, notification: Any):
        """Отправить Telegram уведомление"""
        from app.utils.external_integrations import integration_manager
        from app.models.user import User
        
        user = User.query.get(notification.user_id)
        if user and hasattr(user, 'telegram_chat_id'):
            integration_manager.telegram.send_message(
                user.telegram_chat_id,
                f"<b>{notification.title}</b>\n\n{notification.message}"
            )
    
    def process_scheduled_notifications(self):
        """
        Обработать запланированные уведомления
        
        Вызывается периодически (например, каждую минуту)
        """
        from app.models.notification import Notification
        
        now = datetime.utcnow()
        
        # Получение уведомлений, готовых к отправке
        notifications = Notification.query.filter(
            Notification.scheduled_for <= now,
            Notification.sent_at.is_(None)
        ).all()
        
        for notification in notifications:
            channels = [
                NotificationChannel(c)
                for c in notification.channels.split(',')
            ]
            
            self._send_notification(notification, channels)
            
            notification.sent_at = now
            db.session.commit()
    
    def batch_notify_users(
        self,
        user_ids: List[int],
        title: str,
        message: str,
        notification_type: str,
        priority: NotificationPriority = NotificationPriority.MEDIUM
    ) -> Dict[str, Any]:
        """
        Массовая отправка уведомлений
        
        Оптимизировано для большого количества пользователей
        """
        results = {
            'total': len(user_ids),
            'created': 0,
            'failed': 0
        }
        
        for user_id in user_ids:
            try:
                self.create_notification(
                    user_id, title, message,
                    notification_type, priority
                )
                results['created'] += 1
            except Exception as e:
                results['failed'] += 1
                import logging
                logging.error(f"Failed to create notification for user {user_id}: {e}")
        
        return results
    
    def get_user_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Получить уведомления пользователя"""
        from app.models.notification import Notification
        
        query = Notification.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter(Notification.read_at.is_(None))
        
        notifications = query.order_by(
            Notification.created_at.desc()
        ).limit(limit).all()
        
        return [
            {
                'id': n.id,
                'title': n.title,
                'message': n.message,
                'type': n.type,
                'priority': n.priority,
                'read': n.read_at is not None,
                'created_at': n.created_at.isoformat()
            }
            for n in notifications
        ]
    
    def mark_as_read(self, notification_id: int) -> bool:
        """Отметить уведомление как прочитанное"""
        from app.models.notification import Notification
        
        notification = Notification.query.get(notification_id)
        if notification and not notification.read_at:
            notification.read_at = datetime.utcnow()
            db.session.commit()
            return True
        
        return False
    
    def get_statistics(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Получить статистику уведомлений"""
        from app.models.notification import Notification
        from sqlalchemy import func
        
        query = Notification.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        total = query.count()
        unread = query.filter(Notification.read_at.is_(None)).count()
        sent = query.filter(Notification.sent_at.isnot(None)).count()
        
        # Статистика по типам
        by_type = db.session.query(
            Notification.type,
            func.count(Notification.id)
        ).group_by(Notification.type).all()
        
        return {
            'total': total,
            'unread': unread,
            'sent': sent,
            'pending': total - sent,
            'by_type': dict(by_type)
        }


# Глобальный экземпляр
smart_notification_engine = SmartNotificationEngine()


# Импорт db
from app import db
