# -*- coding: utf-8 -*-
"""
Модуль расширенной системы уведомлений для ПрофиТест
Предоставляет продвинутые возможности управления уведомлениями
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Any
import logging
from dataclasses import dataclass, field
from collections import defaultdict
import json


class NotificationType(Enum):
    """Типы уведомлений"""
    COMMENT_REPLY = 'comment_reply'
    COMMENT_MENTION = 'comment_mention'
    CONTENT_LIKE = 'content_like'
    CONTENT_SHARE = 'content_share'
    NEW_FOLLOWER = 'new_follower'
    SYSTEM_MESSAGE = 'system_message'
    TEST_RESULT = 'test_result'
    RECOMMENDATION = 'recommendation'
    ACHIEVEMENT = 'achievement'
    REMINDER = 'reminder'
    UPDATE = 'update'


class NotificationPriority(Enum):
    """Приоритеты уведомлений"""
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'
    URGENT = 'urgent'


class NotificationStatus(Enum):
    """Статусы уведомлений"""
    UNREAD = 'unread'
    READ = 'read'
    ARCHIVED = 'archived'
    DELETED = 'deleted'


class NotificationChannel(Enum):
    """Каналы доставки уведомлений"""
    IN_APP = 'in_app'
    EMAIL = 'email'
    PUSH = 'push'
    SMS = 'sms'
    TELEGRAM = 'telegram'


@dataclass
class Notification:
    """Класс уведомления"""
    id: str
    user_id: int
    notification_type: NotificationType
    title: str
    message: str
    priority: NotificationPriority
    status: NotificationStatus
    created_at: datetime
    expires_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    channels: List[NotificationChannel] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    is_sent: bool = False
    sent_channels: List[NotificationChannel] = field(default_factory=list)
    delivery_attempts: int = 0
    max_delivery_attempts: int = 3


class NotificationPreferences:
    """Настройки уведомлений пользователя"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.preferences: Dict[NotificationType, Dict[NotificationChannel, bool]] = defaultdict(dict)
        self.global_enabled: bool = True
        self.digest_enabled: bool = False
        self.digest_frequency: str = 'daily'  # daily, weekly
        self.quiet_hours: Dict[str, Any] = {
            'enabled': False,
            'start_time': '22:00',
            'end_time': '08:00'
        }
        
        # Установка настроек по умолчанию
        self._set_default_preferences()
    
    def _set_default_preferences(self):
        """Устанавливает настройки по умолчанию"""
        default_settings = {
            NotificationType.COMMENT_REPLY: {
                NotificationChannel.IN_APP: True,
                NotificationChannel.EMAIL: True,
                NotificationChannel.PUSH: True
            },
            NotificationType.COMMENT_MENTION: {
                NotificationChannel.IN_APP: True,
                NotificationChannel.EMAIL: True,
                NotificationChannel.PUSH: True
            },
            NotificationType.CONTENT_LIKE: {
                NotificationChannel.IN_APP: True,
                NotificationChannel.PUSH: True
            },
            NotificationType.SYSTEM_MESSAGE: {
                NotificationChannel.IN_APP: True,
                NotificationChannel.EMAIL: True,
                NotificationChannel.PUSH: True
            },
            NotificationType.TEST_RESULT: {
                NotificationChannel.IN_APP: True,
                NotificationChannel.EMAIL: True
            },
            NotificationType.RECOMMENDATION: {
                NotificationChannel.IN_APP: True,
                NotificationChannel.EMAIL: False
            }
        }
        
        for notif_type, channels in default_settings.items():
            for channel, enabled in channels.items():
                self.preferences[notif_type][channel] = enabled


class AdvancedNotificationManager:
    """
    Расширенный менеджер уведомлений для системы ПрофиТест.
    Обеспечивает управление уведомлениями, настройки и доставку.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.notifications: Dict[str, Notification] = {}
        self.user_notifications: Dict[int, Set[str]] = defaultdict(set)  # user_id -> notification_ids
        self.type_index: Dict[NotificationType, Set[str]] = defaultdict(set)
        self.status_index: Dict[NotificationStatus, Set[str]] = defaultdict(set)
        self.priority_index: Dict[NotificationPriority, Set[str]] = defaultdict(set)
        
        self.user_preferences: Dict[int, NotificationPreferences] = {}
        self.notification_templates: Dict[NotificationType, Dict[str, str]] = {}
        
        # Инициализация системных уведомлений
        self._create_system_notifications()
        self._load_notification_templates()
    
    def _create_system_notifications(self):
        """Создает системные уведомления по умолчанию"""
        pass  # Пока пусто, можно добавить примеры позже
    
    def _load_notification_templates(self):
        """Загружает шаблоны уведомлений"""
        self.notification_templates = {
            NotificationType.COMMENT_REPLY: {
                'title': 'Новый ответ на ваш комментарий',
                'message': 'Пользователь {username} ответил на ваш комментарий: "{comment}"'
            },
            NotificationType.COMMENT_MENTION: {
                'title': 'Вас упомянули в комментарии',
                'message': 'Пользователь {username} упомянул вас в комментарии: "{comment}"'
            },
            NotificationType.CONTENT_LIKE: {
                'title': 'Ваш контент понравился',
                'message': 'Пользователю {username} понравился ваш {content_type}: "{title}"'
            },
            NotificationType.SYSTEM_MESSAGE: {
                'title': 'Системное сообщение',
                'message': '{message}'
            },
            NotificationType.TEST_RESULT: {
                'title': 'Результаты теста готовы',
                'message': 'Ваши результаты теста "{test_name}" готовы. Результат: {score}%'
            },
            NotificationType.RECOMMENDATION: {
                'title': 'Новые рекомендации',
                'message': 'Мы подготовили для вас новые рекомендации по профориентации'
            }
        }
    
    def create_notification(self, user_id: int, notification_type: NotificationType, 
                          title: str = None, message: str = None, 
                          priority: NotificationPriority = NotificationPriority.NORMAL,
                          data: Dict[str, Any] = None, 
                          channels: List[NotificationChannel] = None,
                          expires_in_hours: int = 168) -> Optional[str]:  # 168 = 1 неделя
        """
        Создает новое уведомление.
        
        Args:
            user_id: ID пользователя
            notification_type: Тип уведомления
            title: Заголовок (опционально, будет использован шаблон если не указан)
            message: Сообщение (опционально, будет использован шаблон если не указан)
            priority: Приоритет
            data: Дополнительные данные
            channels: Каналы доставки
            expires_in_hours: Через сколько часов истекает
            
        Returns:
            str: ID уведомления или None
        """
        try:
            import uuid
            notification_id = str(uuid.uuid4())
            
            # Используем шаблоны если заголовок/сообщение не указаны
            if not title or not message:
                template = self.notification_templates.get(notification_type, {})
                title = title or template.get('title', 'Уведомление')
                message = message or template.get('message', 'У вас новое уведомление')
                
                # Подставляем данные в шаблон
                if data:
                    try:
                        title = title.format(**data)
                        message = message.format(**data)
                    except KeyError:
                        pass  # Оставляем оригинальный текст если данные не совпадают
            
            # Определяем каналы доставки
            if channels is None:
                channels = self._get_user_channels(user_id, notification_type)
            
            # Создаем уведомление
            notification = Notification(
                id=notification_id,
                user_id=user_id,
                notification_type=notification_type,
                title=title,
                message=message,
                priority=priority,
                status=NotificationStatus.UNREAD,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(hours=expires_in_hours),
                channels=channels,
                data=data or {}
            )
            
            # Добавляем уведомление
            self.notifications[notification_id] = notification
            self.user_notifications[user_id].add(notification_id)
            self.type_index[notification_type].add(notification_id)
            self.status_index[notification.status].add(notification_id)
            self.priority_index[priority].add(notification_id)
            
            self.logger.info(f"Уведомление {notification_id} создано для пользователя {user_id}")
            return notification_id
            
        except Exception as e:
            self.logger.error(f"Ошибка при создании уведомления: {str(e)}")
            return None
    
    def _get_user_channels(self, user_id: int, notification_type: NotificationType) -> List[NotificationChannel]:
        """
        Получает каналы доставки для пользователя и типа уведомления.
        
        Args:
            user_id: ID пользователя
            notification_type: Тип уведомления
            
        Returns:
            list: Список каналов доставки
        """
        # Получаем настройки пользователя
        preferences = self.get_user_preferences(user_id)
        
        # Проверяем глобальные настройки
        if not preferences.global_enabled:
            return []
        
        # Проверяем настройки для конкретного типа
        type_preferences = preferences.preferences.get(notification_type, {})
        enabled_channels = [channel for channel, enabled in type_preferences.items() if enabled]
        
        # Проверяем тихие часы
        if preferences.quiet_hours['enabled']:
            current_time = datetime.now().strftime('%H:%M')
            quiet_start = preferences.quiet_hours['start_time']
            quiet_end = preferences.quiet_hours['end_time']
            
            # Если сейчас тихие часы, отключаем мгновенные уведомления
            if self._is_time_in_range(current_time, quiet_start, quiet_end):
                enabled_channels = [c for c in enabled_channels if c != NotificationChannel.PUSH]
        
        return enabled_channels if enabled_channels else [NotificationChannel.IN_APP]
    
    def _is_time_in_range(self, current_time: str, start_time: str, end_time: str) -> bool:
        """
        Проверяет, находится ли время в заданном диапазоне.
        
        Args:
            current_time: Текущее время (HH:MM)
            start_time: Время начала (HH:MM)
            end_time: Время окончания (HH:MM)
            
        Returns:
            bool: Находится ли время в диапазоне
        """
        try:
            current = int(current_time.replace(':', ''))
            start = int(start_time.replace(':', ''))
            end = int(end_time.replace(':', ''))
            
            if start <= end:
                return start <= current <= end
            else:  # диапазон пересекает полночь
                return current >= start or current <= end
        except ValueError:
            return False
    
    def get_user_preferences(self, user_id: int) -> NotificationPreferences:
        """
        Получает настройки уведомлений пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            NotificationPreferences: Настройки пользователя
        """
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = NotificationPreferences(user_id)
        return self.user_preferences[user_id]
    
    def update_user_preferences(self, user_id: int, preferences_data: Dict[str, Any]) -> bool:
        """
        Обновляет настройки уведомлений пользователя.
        
        Args:
            user_id: ID пользователя
            preferences_data: Данные настроек
            
        Returns:
            bool: Успешность операции
        """
        try:
            preferences = self.get_user_preferences(user_id)
            
            # Обновляем глобальные настройки
            if 'global_enabled' in preferences_data:
                preferences.global_enabled = preferences_data['global_enabled']
            
            if 'digest_enabled' in preferences_data:
                preferences.digest_enabled = preferences_data['digest_enabled']
            
            if 'digest_frequency' in preferences_data:
                preferences.digest_frequency = preferences_data['digest_frequency']
            
            if 'quiet_hours' in preferences_data:
                preferences.quiet_hours.update(preferences_data['quiet_hours'])
            
            # Обновляем настройки по типам уведомлений
            if 'notification_types' in preferences_data:
                for notif_type, channels in preferences_data['notification_types'].items():
                    try:
                        notif_type_enum = NotificationType(notif_type)
                        for channel, enabled in channels.items():
                            try:
                                channel_enum = NotificationChannel(channel)
                                preferences.preferences[notif_type_enum][channel_enum] = enabled
                            except ValueError:
                                continue
                    except ValueError:
                        continue
            
            self.logger.info(f"Настройки уведомлений обновлены для пользователя {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении настроек уведомлений: {str(e)}")
            return False
    
    def get_notification(self, notification_id: str) -> Optional[Notification]:
        """
        Получает уведомление по ID.
        
        Args:
            notification_id: ID уведомления
            
        Returns:
            Notification: Объект уведомления или None
        """
        return self.notifications.get(notification_id)
    
    def get_user_notifications(self, user_id: int, status: NotificationStatus = None, 
                             notification_type: NotificationType = None, 
                             limit: int = 50) -> List[Notification]:
        """
        Получает уведомления пользователя.
        
        Args:
            user_id: ID пользователя
            status: Фильтр по статусу
            notification_type: Фильтр по типу
            limit: Максимальное количество
            
        Returns:
            list: Список уведомлений
        """
        notification_ids = self.user_notifications.get(user_id, set())
        notifications = [self.notifications[nid] for nid in notification_ids if nid in self.notifications]
        
        # Применяем фильтры
        if status:
            notifications = [n for n in notifications if n.status == status]
        
        if notification_type:
            notifications = [n for n in notifications if n.notification_type == notification_type]
        
        # Сортировка по дате создания (новые первыми)
        notifications.sort(key=lambda x: x.created_at, reverse=True)
        
        # Ограничиваем количество
        return notifications[:limit]
    
    def mark_as_read(self, notification_id: str) -> bool:
        """
        Помечает уведомление как прочитанное.
        
        Args:
            notification_id: ID уведомления
            
        Returns:
            bool: Успешность операции
        """
        try:
            notification = self.get_notification(notification_id)
            if not notification:
                return False
            
            if notification.status == NotificationStatus.UNREAD:
                # Обновляем статус
                old_status = notification.status
                notification.status = NotificationStatus.READ
                notification.read_at = datetime.now()
                
                # Обновляем индексы
                self.status_index[old_status].discard(notification_id)
                self.status_index[notification.status].add(notification_id)
                
                self.logger.info(f"Уведомление {notification_id} помечено как прочитанное")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при пометке уведомления как прочитанного: {str(e)}")
            return False
    
    def mark_multiple_as_read(self, user_id: int, notification_ids: List[str] = None) -> int:
        """
        Помечает несколько уведомлений как прочитанные.
        
        Args:
            user_id: ID пользователя
            notification_ids: Список ID уведомлений (если None, то все непрочитанные)
            
        Returns:
            int: Количество помеченных уведомлений
        """
        try:
            if notification_ids is None:
                # Получаем все непрочитанные уведомления пользователя
                user_notif_ids = self.user_notifications.get(user_id, set())
                notification_ids = [nid for nid in user_notif_ids 
                                  if nid in self.notifications 
                                  and self.notifications[nid].status == NotificationStatus.UNREAD]
            
            marked_count = 0
            for notif_id in notification_ids:
                if self.mark_as_read(notif_id):
                    marked_count += 1
            
            self.logger.info(f"Помечено {marked_count} уведомлений как прочитанные для пользователя {user_id}")
            return marked_count
            
        except Exception as e:
            self.logger.error(f"Ошибка при массовой пометке уведомлений: {str(e)}")
            return 0
    
    def delete_notification(self, notification_id: str) -> bool:
        """
        Удаляет уведомление.
        
        Args:
            notification_id: ID уведомления
            
        Returns:
            bool: Успешность операции
        """
        try:
            notification = self.get_notification(notification_id)
            if not notification:
                return False
            
            user_id = notification.user_id
            
            # Обновляем индексы
            self.status_index[notification.status].discard(notification_id)
            self.type_index[notification.notification_type].discard(notification_id)
            self.priority_index[notification.priority].discard(notification_id)
            self.user_notifications[user_id].discard(notification_id)
            
            # Удаляем из основного хранилища
            del self.notifications[notification_id]
            
            self.logger.info(f"Уведомление {notification_id} удалено")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка при удалении уведомления: {str(e)}")
            return False
    
    def send_notification(self, notification_id: str) -> bool:
        """
        Отправляет уведомление через указанные каналы.
        
        Args:
            notification_id: ID уведомления
            
        Returns:
            bool: Успешность операции
        """
        try:
            notification = self.get_notification(notification_id)
            if not notification:
                return False
            
            if notification.is_sent:
                return True
            
            success = True
            for channel in notification.channels:
                if not self._send_via_channel(notification, channel):
                    success = False
                    notification.delivery_attempts += 1
                else:
                    notification.sent_channels.append(channel)
            
            notification.is_sent = success or notification.delivery_attempts >= notification.max_delivery_attempts
            
            if notification.is_sent:
                self.logger.info(f"Уведомление {notification_id} успешно отправлено")
            else:
                self.logger.warning(f"Уведомление {notification_id} не отправлено (попытка {notification.delivery_attempts})")
            
            return notification.is_sent
            
        except Exception as e:
            self.logger.error(f"Ошибка при отправке уведомления: {str(e)}")
            return False
    
    def _send_via_channel(self, notification: Notification, channel: NotificationChannel) -> bool:
        """
        Отправляет уведомление через конкретный канал.
        
        Args:
            notification: Уведомление
            channel: Канал доставки
            
        Returns:
            bool: Успешность отправки
        """
        try:
            if channel == NotificationChannel.IN_APP:
                # Для in-app уведомлений просто помечаем как готовое к показу
                return True
            
            elif channel == NotificationChannel.EMAIL:
                # Здесь будет логика отправки email
                self.logger.debug(f"Отправка email уведомления {notification.id}")
                return self._send_email_notification(notification)
            
            elif channel == NotificationChannel.PUSH:
                # Здесь будет логика отправки push-уведомлений
                self.logger.debug(f"Отправка push уведомления {notification.id}")
                return self._send_push_notification(notification)
            
            elif channel == NotificationChannel.SMS:
                # Здесь будет логика отправки SMS
                self.logger.debug(f"Отправка SMS уведомления {notification.id}")
                return self._send_sms_notification(notification)
            
            elif channel == NotificationChannel.TELEGRAM:
                # Здесь будет логика отправки через Telegram
                self.logger.debug(f"Отправка Telegram уведомления {notification.id}")
                return self._send_telegram_notification(notification)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Ошибка при отправке через канал {channel}: {str(e)}")
            return False
    
    def _send_email_notification(self, notification: Notification) -> bool:
        """Отправляет email уведомление (заглушка)"""
        # В реальной системе здесь будет интеграция с почтовым сервисом
        return True
    
    def _send_push_notification(self, notification: Notification) -> bool:
        """Отправляет push уведомление (заглушка)"""
        # В реальной системе здесь будет интеграция с push-сервисом
        return True
    
    def _send_sms_notification(self, notification: Notification) -> bool:
        """Отправляет SMS уведомление (заглушка)"""
        # В реальной системе здесь будет интеграция с SMS-сервисом
        return True
    
    def _send_telegram_notification(self, notification: Notification) -> bool:
        """Отправляет уведомление через Telegram (заглушка)"""
        # В реальной системе здесь будет интеграция с Telegram API
        return True
    
    def get_unread_count(self, user_id: int) -> int:
        """
        Получает количество непрочитанных уведомлений пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            int: Количество непрочитанных уведомлений
        """
        user_notif_ids = self.user_notifications.get(user_id, set())
        unread_count = sum(1 for nid in user_notif_ids 
                          if nid in self.notifications 
                          and self.notifications[nid].status == NotificationStatus.UNREAD)
        return unread_count
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получает статистику по уведомлениям.
        
        Returns:
            dict: Статистика уведомлений
        """
        total_notifications = len(self.notifications)
        unread_notifications = len(self.status_index.get(NotificationStatus.UNREAD, set()))
        read_notifications = len(self.status_index.get(NotificationStatus.READ, set()))
        
        notification_types = {}
        for notif_type, ids in self.type_index.items():
            notification_types[notif_type.value] = len(ids)
        
        notification_priorities = {}
        for priority, ids in self.priority_index.items():
            notification_priorities[priority.value] = len(ids)
        
        return {
            'total_notifications': total_notifications,
            'unread_notifications': unread_notifications,
            'read_notifications': read_notifications,
            'archived_notifications': len(self.status_index.get(NotificationStatus.ARCHIVED, set())),
            'deleted_notifications': len(self.status_index.get(NotificationStatus.DELETED, set())),
            'notifications_by_type': notification_types,
            'notifications_by_priority': notification_priorities,
            'total_users': len(self.user_notifications),
            'sent_notifications': sum(1 for n in self.notifications.values() if n.is_sent),
            'failed_deliveries': sum(1 for n in self.notifications.values() 
                                   if n.delivery_attempts > 0 and not n.is_sent)
        }
    
    def cleanup_expired_notifications(self) -> int:
        """
        Удаляет истекшие уведомления.
        
        Returns:
            int: Количество удаленных уведомлений
        """
        try:
            current_time = datetime.now()
            expired_ids = [nid for nid, notification in self.notifications.items() 
                          if notification.expires_at and notification.expires_at < current_time]
            
            deleted_count = 0
            for notif_id in expired_ids:
                if self.delete_notification(notif_id):
                    deleted_count += 1
            
            if deleted_count > 0:
                self.logger.info(f"Удалено {deleted_count} истекших уведомлений")
            
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Ошибка при очистке истекших уведомлений: {str(e)}")
            return 0


# Глобальный экземпляр менеджера уведомлений
notification_manager = AdvancedNotificationManager()