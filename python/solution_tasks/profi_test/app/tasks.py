"""
Background tasks for the profi_test application using Celery
"""
from celery import Celery
import logging

logger = logging.getLogger(__name__)

# Global variable to hold celery instance - will be initialized later
celery = None


def make_celery(app):
    """Create Celery instance with app configuration"""
    
    celery_instance = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery_instance.conf.update(app.config)

    class ContextTask(celery_instance.Task):
        """Make celery tasks work with Flask app context."""
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_instance.Task = ContextTask
    return celery_instance


def init_celery_app(flask_app):
    """Initialize Celery with Flask app - call this from the main app"""
    global celery
    if celery is None:
        celery = make_celery(flask_app)
        
        # Register periodic tasks configuration after celery is initialized
        from celery.schedules import crontab
        celery.conf.beat_schedule = {
            # Update user statistics daily
            'update-user-statistics-daily': {
                'task': 'app.tasks.update_user_statistics_task',
                'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
            },
            # Retrain ML models weekly
            'retrain-ml-models-weekly': {
                'task': 'app.tasks.train_ml_models_task',
                'schedule': crontab(hour=3, minute=0, day_of_week=1),  # Run weekly on Mondays at 3 AM
            },
            # Clean up old data daily
            'cleanup-old-data-daily': {
                'task': 'app.tasks.cleanup_old_data_task',
                'schedule': crontab(hour=4, minute=0),  # Run daily at 4 AM
            },
        }
        
        celery.conf.timezone = 'UTC'
    
    return celery


def get_celery():
    """Get the initialized celery instance"""
    global celery
    if celery is None:
        raise RuntimeError("Celery not initialized. Call init_celery_app() first.")
    return celery


# Define tasks - they will be registered after celery is initialized
def define_tasks():
    """Define all tasks after celery is initialized"""
    global celery
    if celery is None:
        return  # Skip if celery not initialized yet
    
    @celery.task(bind=True)
    def generate_user_report_task(self, user_id, report_type='comprehensive'):
        """
        Background task to generate user reports
        
        Args:
            user_id: ID of the user
            report_type: Type of report to generate
        """
        try:
            from app.models import User
            from app.advanced_notifications import notification_manager
            from app.enhanced_reports import enhanced_reports
            
            user = User.query.get(user_id)
            if not user:
                logger.error(f"User with ID {user_id} not found")
                return {'success': False, 'error': 'User not found'}
            
            # Generate report using enhanced reports module
            report_data = enhanced_reports.generate_user_report(user_id, report_type)
            
            # Save report or send notification
            notification_manager.create_notification(
                user_id=user_id,
                title=f"Ваш {report_type} отчет готов",
                message="Отчет по вашим тестам успешно сгенерирован и доступен для скачивания.",
                notification_type='info'
            )
            
            return {'success': True, 'user_id': user_id, 'report_type': report_type}
            
        except Exception as e:
            logger.error(f"Error generating report for user {user_id}: {str(e)}")
            self.retry(exc=e, countdown=60, max_retries=3)  # Retry after 1 minute, up to 3 times
            return {'success': False, 'error': str(e)}

    @celery.task(bind=True)
    def process_test_results_task(self, test_result_ids):
        """
        Background task to process multiple test results
        
        Args:
            test_result_ids: List of test result IDs to process
        """
        try:
            from app.models import TestResult
            from app.advanced_notifications import notification_manager
            from app.ml_recommendations import recommendation_engine
            
            for result_id in test_result_ids:
                test_result = TestResult.query.get(result_id)
                if test_result:
                    # Process the test result - this could include:
                    # - Updating user progress
                    # - Generating recommendations
                    # - Sending notifications
                    # - Updating ML models
                    
                    # Update user progress
                    from app.progress import update_user_progress
                    update_user_progress(test_result.user_id, test_result.id)
                    
                    # Generate personalized recommendations
                    recommendation_engine.generate_recommendations(test_result.user_id)
                    
                    # Send notification about processed results
                    notification_manager.create_notification(
                        user_id=test_result.user_id,
                        title="Результаты теста обработаны",
                        message="Ваши результаты теста были успешно обработаны. Рекомендации обновлены.",
                        notification_type='success'
                    )
            
            return {'success': True, 'processed_count': len(test_result_ids)}
            
        except Exception as e:
            logger.error(f"Error processing test results {test_result_ids}: {str(e)}")
            self.retry(exc=e, countdown=120, max_retries=2)  # Retry after 2 minutes, up to 2 times
            return {'success': False, 'error': str(e)}

    @celery.task(bind=True)
    def send_bulk_notifications_task(self, notification_data_list):
        """
        Background task to send bulk notifications
        
        Args:
            notification_data_list: List of notification data dictionaries
        """
        try:
            from app.advanced_notifications import notification_manager
            
            sent_count = 0
            for notification_data in notification_data_list:
                try:
                    user_id = notification_data.get('user_id')
                    title = notification_data.get('title')
                    message = notification_data.get('message')
                    notification_type = notification_data.get('type', 'info')
                    
                    notification_manager.create_notification(
                        user_id=user_id,
                        title=title,
                        message=message,
                        notification_type=notification_type
                    )
                    sent_count += 1
                    
                except Exception as e:
                    logger.error(f"Error sending notification to user {notification_data.get('user_id')}: {str(e)}")
            
            return {'success': True, 'sent_count': sent_count}
            
        except Exception as e:
            logger.error(f"Error sending bulk notifications: {str(e)}")
            return {'success': False, 'error': str(e)}

    @celery.task(bind=True)
    def cleanup_old_data_task(self, days_old=30):
        """
        Background task to clean up old data
        
        Args:
            days_old: Days threshold for cleaning up old data
        """
        try:
            from app import db
            from app.models import Notification
            from datetime import datetime, timedelta
            
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            # Clean up old notifications (keeping only recent ones)
            old_notifications = Notification.query.filter(
                Notification.created_at < cutoff_date
            ).filter(
                Notification.is_read == True  # Only delete read notifications
            )
            
            deleted_notifications = old_notifications.delete(synchronize_session=False)
            
            # Commit the changes
            db.session.commit()
            
            logger.info(f"Cleaned up {deleted_notifications} old notifications")
            
            return {'success': True, 'cleaned_items': deleted_notifications}
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {str(e)}")
            return {'success': False, 'error': str(e)}

    @celery.task(bind=True)
    def train_ml_models_task(self):
        """
        Background task to retrain ML models with new data
        """
        try:
            from app.ml_recommendations import recommendation_engine
            
            # Retrain recommendation models with latest data
            recommendation_engine.train_models()
            
            logger.info("ML models retrained successfully")
            
            return {'success': True, 'models_trained': True}
            
        except Exception as e:
            logger.error(f"Error retraining ML models: {str(e)}")
            return {'success': False, 'error': str(e)}

    @celery.task(bind=True)
    def update_user_statistics_task(self, user_id):
        """
        Background task to update user statistics
        
        Args:
            user_id: ID of the user to update statistics for
        """
        try:
            from app.analytics_api import update_user_analytics
            update_user_analytics(user_id)
            
            return {'success': True, 'user_id': user_id}
            
        except Exception as e:
            logger.error(f"Error updating statistics for user {user_id}: {str(e)}")
            return {'success': False, 'error': str(e)}


# Export the functions that need to be imported elsewhere
__all__ = ['init_celery_app', 'define_tasks', 'get_celery']