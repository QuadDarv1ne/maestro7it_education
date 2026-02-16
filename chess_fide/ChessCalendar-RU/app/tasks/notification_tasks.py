"""
Celery задачи для отправки уведомлений
"""
from app.celery_app import celery_app
from app import create_app, db
from app.models.notification import Notification, Subscription
from app.models.tournament import Tournament
from app.models.user import User
from app.utils.metrics import track_celery_task
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
@track_celery_task('send_notification')
def send_notification(self, user_id, title, message, notification_type='info'):
    """
    Отправка уведомления пользователю
    """
    app = create_app()
    
    with app.app_context():
        try:
            user = User.query.get(user_id)
            if not user:
                logger.error(f"User {user_id} not found")
                return {'status': 'error', 'message': 'User not found'}
            
            # Создаем уведомление
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                type=notification_type,
                is_read=False
            )
            db.session.add(notification)
            db.session.commit()
            
            logger.info(f"Notification sent to user {user_id}: {title}")
            
            return {
                'status': 'success',
                'notification_id': notification.id,
                'user_id': user_id
            }
            
        except Exception as e:
            logger.error(f"Notification sending error: {e}")
            raise self.retry(exc=e)

@celery_app.task
def send_pending_notifications():
    """
    Отправка всех ожидающих уведомлений
    """
    app = create_app()
    
    with app.app_context():
        try:
            # Получаем непрочитанные уведомления старше 5 минут
            pending = Notification.query.filter(
                Notification.is_read == False,
                Notification.created_at < datetime.utcnow() - timedelta(minutes=5)
            ).limit(100).all()
            
            sent_count = 0
            for notification in pending:
                # Здесь логика отправки (email, push и т.д.)
                logger.info(f"Processing notification {notification.id}")
                sent_count += 1
            
            return {
                'status': 'success',
                'sent': sent_count
            }
            
        except Exception as e:
            logger.error(f"Pending notifications error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
@track_celery_task('notify_upcoming_tournaments')
def notify_upcoming_tournaments():
    """
    Уведомление пользователей о предстоящих турнирах
    """
    app = create_app()
    
    with app.app_context():
        try:
            # Турниры, которые начинаются через 7 дней
            upcoming_date = datetime.utcnow().date() + timedelta(days=7)
            
            tournaments = Tournament.query.filter(
                Tournament.start_date == upcoming_date,
                Tournament.status == 'Scheduled'
            ).all()
            
            notifications_sent = 0
            
            for tournament in tournaments:
                # Получаем подписчиков
                subscriptions = Subscription.query.filter_by(
                    tournament_id=tournament.id,
                    is_active=True
                ).all()
                
                for subscription in subscriptions:
                    send_notification.delay(
                        subscription.user_id,
                        f"Турнир начинается через неделю",
                        f"Турнир '{tournament.name}' начнется {tournament.start_date.strftime('%d.%m.%Y')} в {tournament.location}",
                        'tournament_reminder'
                    )
                    notifications_sent += 1
            
            logger.info(f"Sent {notifications_sent} tournament reminders")
            
            return {
                'status': 'success',
                'tournaments': len(tournaments),
                'notifications': notifications_sent
            }
            
        except Exception as e:
            logger.error(f"Upcoming tournaments notification error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
def notify_tournament_changes(tournament_id):
    """
    Уведомление об изменениях в турнире
    """
    app = create_app()
    
    with app.app_context():
        try:
            tournament = Tournament.query.get(tournament_id)
            if not tournament:
                return {'status': 'error', 'message': 'Tournament not found'}
            
            # Получаем подписчиков
            subscriptions = Subscription.query.filter_by(
                tournament_id=tournament_id,
                is_active=True
            ).all()
            
            for subscription in subscriptions:
                send_notification.delay(
                    subscription.user_id,
                    f"Изменения в турнире",
                    f"В турнире '{tournament.name}' произошли изменения. Проверьте актуальную информацию.",
                    'tournament_update'
                )
            
            return {
                'status': 'success',
                'notified_users': len(subscriptions)
            }
            
        except Exception as e:
            logger.error(f"Tournament changes notification error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
def send_bulk_notifications(user_ids, title, message, notification_type='info'):
    """
    Массовая отправка уведомлений
    """
    results = []
    for user_id in user_ids:
        result = send_notification.delay(user_id, title, message, notification_type)
        results.append(result.id)
    
    return {
        'status': 'queued',
        'task_ids': results,
        'count': len(results)
    }
