from app.models.tournament import Tournament
from app.models.notification import Notification, Subscription, NotificationType, TournamentReminder
from app import db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

class NotificationService:
    def __init__(self, smtp_server='localhost', smtp_port=587, 
                 username=None, password=None, sender_email=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender_email = sender_email or username
        self.logger = logging.getLogger(__name__)
    
    def send_new_tournament_notification(self, tournament):
        """Отправить уведомление о новом турнире"""
        try:
            # Создаем уведомление
            title = f"Новый турнир: {tournament.name}"
            message = f"Добавлен новый турнир: {tournament.name}. Начало: {tournament.start_date}. Место: {tournament.location}."
            
            notification = Notification(
                title=title,
                message=message,
                type=NotificationType.NEW_TOURNAMENT,
                tournament_id=tournament.id
            )
            
            db.session.add(notification)
            db.session.commit()
            
            # Отправляем уведомления подписчикам
            self._send_to_subscribers(notification)
            
            self.logger.info(f"New tournament notification created for {tournament.name}")
        except Exception as e:
            self.logger.error(f"Error sending new tournament notification: {e}")
    
    def send_tournament_update_notification(self, tournament, changes):
        """Отправить уведомление об изменении турнира"""
        try:
            # Создаем уведомление
            title = f"Изменения в турнире: {tournament.name}"
            change_descriptions = []
            for field, (old_val, new_val) in changes.items():
                field_names = {
                    'name': 'название',
                    'start_date': 'дата начала',
                    'end_date': 'дата окончания',
                    'location': 'место проведения',
                    'category': 'категория',
                    'status': 'статус'
                }
                field_name = field_names.get(field, field)
                change_descriptions.append(f"{field_name}: {old_val} → {new_val}")
            
            message = f"В турнире '{tournament.name}' произошли изменения:\n" + "\n".join(change_descriptions)
            
            notification = Notification(
                title=title,
                message=message,
                type=NotificationType.TOURNAMENT_UPDATE,
                tournament_id=tournament.id
            )
            
            db.session.add(notification)
            db.session.commit()

            # Отправляем уведомления подписчикам
            self._send_to_subscribers(notification)
            
            self.logger.info(f"Tournament update notification created for {tournament.name}")
        except Exception as e:
            self.logger.error(f"Error sending tournament update notification: {e}")
    
    def send_tournament_cancelled_notification(self, tournament):
        """Отправить уведомление об отмене турнира"""
        try:
            title = f"Турнир отменен: {tournament.name}"
            message = f"Турнир '{tournament.name}' был отменен."
            
            notification = Notification(
                title=title,
                message=message,
                type=NotificationType.TOURNAMENT_CANCELLED,
                tournament_id=tournament.id,
                priority=3  # High priority
            )
            
            db.session.add(notification)
            db.session.commit()

            # Отправляем уведомления подписчикам
            self._send_to_subscribers(notification)
            
            self.logger.info(f"Tournament cancelled notification created for {tournament.name}")
        except Exception as e:
            self.logger.error(f"Error sending tournament cancelled notification: {e}")
    
    def _send_to_subscribers(self, notification):
        """Отправить уведомление всем подходящим подписчикам"""
        try:
            # Получаем активных подписчиков с соответствующими предпочтениями
            subscriptions = Subscription.query.filter_by(active=True).all()

            for subscription in subscriptions:
                # Проверяем предпочтения подписчика
                should_send = False
                if notification.type == NotificationType.NEW_TOURNAMENT and subscription.preferences.get('new_tournaments', True):
                    should_send = True
                elif notification.type == NotificationType.TOURNAMENT_UPDATE and subscription.preferences.get('tournament_updates', True):
                    should_send = True
                elif notification.type == NotificationType.TOURNAMENT_CANCELLED:
                    should_send = True  # Отправляем всегда при отмене

                if should_send:
                    # В реальной системе здесь будет отправка email
                    self.logger.info(f"Notification {notification.title} queued for {subscription.email}")
                    
                    # Здесь можно добавить фактическую отправку email
                    # self._send_email(subscription.email, notification.title, notification.message)
        except Exception as e:
            self.logger.error(f"Error sending notification to subscribers: {e}")
    
    def create_subscription(self, email, preferences=None):
        """Создать новую подписку"""
        try:
            if not preferences:
                preferences = {
                    'new_tournaments': True,
                    'tournament_updates': True,
                    'reminders': True
                }
            
            subscription = Subscription(email=email, preferences=preferences)
            db.session.add(subscription)
            db.session.commit()
            
            self.logger.info(f"New subscription created for {email}")
            return subscription
        except Exception as e:
            self.logger.error(f"Error creating subscription for {email}: {e}")
            return None
    
    def get_unread_notifications(self, email):
        """Получить непрочитанные уведомления для пользователя"""
        try:
            notifications = Notification.query.filter(
                Notification.recipient_email == email,
                Notification.is_read == False
            ).order_by(Notification.created_at.desc()).all()
            
            return notifications
        except Exception as e:
            self.logger.error(f"Error getting unread notifications for {email}: {e}")
            return []
    
    def mark_notification_as_read(self, notification_id):
        """Отметить уведомление как прочитанное"""
        try:
            notification = Notification.query.get(notification_id)
            if notification:
                notification.is_read = True
                notification.sent_at = datetime.utcnow()
                db.session.commit()
                return True
        except Exception as e:
            self.logger.error(f"Error marking notification {notification_id} as read: {e}")
        return False

    def add_subscriber(self, email, preferences=None):
        """Добавить подписчика на уведомления"""
        return self.create_subscription(email, preferences)

    def get_subscriber_stats(self):
        """Получить статистику по подписчикам"""
        try:
            total_subscribers = Subscription.query.filter_by(active=True).count()
            return {
                'total_subscribers': total_subscribers,
                'new_tournaments_enabled': Subscription.query.filter(
                    Subscription.active == True,
                    db.func.json_extract(Subscription.preferences, '$.new_tournaments') == True
                ).count(),
                'tournament_updates_enabled': Subscription.query.filter(
                    Subscription.active == True,
                    db.func.json_extract(Subscription.preferences, '$.tournament_updates') == True
                ).count(),
                'reminders_enabled': Subscription.query.filter(
                    Subscription.active == True,
                    db.func.json_extract(Subscription.preferences, '$.reminders') == True
                ).count()
            }
        except Exception as e:
            self.logger.error(f"Error getting subscriber stats: {e}")
            return {'total_subscribers': 0}
    
    def create_tournament_reminder(self, tournament_id, subscription_id, reminder_days=1):
        """Создать напоминание о турнире"""
        try:
            reminder = TournamentReminder(
                tournament_id=tournament_id,
                subscription_id=subscription_id,
                reminder_days=reminder_days
            )
            db.session.add(reminder)
            db.session.commit()
            self.logger.info(f"Tournament reminder created for tournament {tournament_id}")
            return reminder
        except Exception as e:
            self.logger.error(f"Error creating tournament reminder: {e}")
            return None
    
    def send_reminders(self):
        """Отправить все запланированные напоминания"""
        try:
            from datetime import date, timedelta
            
            # Находим напоминания, которые нужно отправить сегодня
            today = date.today()
            reminders_to_send = db.session.query(TournamentReminder).filter(
                TournamentReminder.sent == False,
                TournamentReminder.tournament.has(
                    Tournament.start_date == today + timedelta(days=TournamentReminder.reminder_days)
                )
            ).all()
            
            sent_count = 0
            for reminder in reminders_to_send:
                try:
                    # Создаем уведомление
                    tournament = reminder.tournament
                    subscription = reminder.subscription
                    
                    title = f"Напоминание: {tournament.name} начинается через {reminder.reminder_days} дней"
                    message = f"Турнир '{tournament.name}' начнется {tournament.start_date.strftime('%d.%m.%Y')} в {tournament.location}."
                    
                    notification = Notification(
                        title=title,
                        message=message,
                        type=NotificationType.REMINDER,
                        recipient_email=subscription.email,
                        tournament_id=tournament.id,
                        priority=1
                    )
                    
                    db.session.add(notification)
                    reminder.sent = True
                    reminder.sent_at = datetime.utcnow()
                    sent_count += 1
                    
                    self.logger.info(f"Reminder sent to {subscription.email} for tournament {tournament.name}")
                    
                except Exception as e:
                    self.logger.error(f"Error sending reminder {reminder.id}: {e}")
                    continue
            
            db.session.commit()
            self.logger.info(f"Sent {sent_count} tournament reminders")
            return sent_count
            
        except Exception as e:
            self.logger.error(f"Error sending reminders: {e}")
            return 0
    
    def get_upcoming_tournaments(self, days_ahead=7):
        """Получить турниры, начинающиеся в ближайшие дни"""
        try:
            from datetime import date, timedelta
            
            start_date = date.today()
            end_date = start_date + timedelta(days=days_ahead)
            
            tournaments = Tournament.query.filter(
                Tournament.start_date >= start_date,
                Tournament.start_date <= end_date,
                Tournament.status.in_(['Scheduled', 'Ongoing'])
            ).order_by(Tournament.start_date).all()
            
            return tournaments
        except Exception as e:
            self.logger.error(f"Error getting upcoming tournaments: {e}")
            return []

# Глобальный экземпляр сервиса уведомлений
notification_service = NotificationService()