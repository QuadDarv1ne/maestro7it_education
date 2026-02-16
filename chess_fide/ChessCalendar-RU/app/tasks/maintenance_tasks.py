"""
Celery задачи для обслуживания системы
"""
from app.celery_app import celery_app
from app import create_app, db
from app.models.notification import Notification
from app.utils.backup import DatabaseBackupManager
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)

@celery_app.task
def cleanup_old_data():
    """
    Очистка старых данных
    """
    app = create_app()
    
    with app.app_context():
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=90)
            
            # Удаляем старые прочитанные уведомления
            old_notifications = Notification.query.filter(
                Notification.is_read == True,
                Notification.created_at < cutoff_date
            ).all()
            
            deleted_count = len(old_notifications)
            for notification in old_notifications:
                db.session.delete(notification)
            
            db.session.commit()
            
            logger.info(f"Cleaned up {deleted_count} old notifications")
            
            return {
                'status': 'success',
                'deleted_notifications': deleted_count
            }
            
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
            db.session.rollback()
            return {'status': 'error', 'message': str(e)}

@celery_app.task
def backup_database():
    """
    Резервное копирование базы данных
    """
    try:
        db_path = os.environ.get('DATABASE_PATH', 'instance/chess_calendar.db')
        backup_manager = DatabaseBackupManager(db_path)
        
        backup_path = backup_manager.create_compressed_backup()
        
        logger.info(f"Database backup created: {backup_path}")
        
        return {
            'status': 'success',
            'backup_path': backup_path,
            'created_at': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Backup error: {e}")
        return {'status': 'error', 'message': str(e)}

@celery_app.task
def cleanup_old_backups(keep_days=30):
    """
    Удаление старых резервных копий
    """
    try:
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            return {'status': 'success', 'deleted': 0}
        
        cutoff_time = datetime.utcnow() - timedelta(days=keep_days)
        deleted_count = 0
        
        for filename in os.listdir(backup_dir):
            filepath = os.path.join(backup_dir, filename)
            
            if os.path.isfile(filepath):
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_time < cutoff_time:
                    os.remove(filepath)
                    deleted_count += 1
                    logger.info(f"Deleted old backup: {filename}")
        
        return {
            'status': 'success',
            'deleted': deleted_count
        }
        
    except Exception as e:
        logger.error(f"Backup cleanup error: {e}")
        return {'status': 'error', 'message': str(e)}

@celery_app.task
def optimize_database():
    """
    Оптимизация базы данных
    """
    app = create_app()
    
    with app.app_context():
        try:
            # Для SQLite выполняем VACUUM
            db.session.execute('VACUUM')
            db.session.commit()
            
            logger.info("Database optimized")
            
            return {
                'status': 'success',
                'optimized_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Database optimization error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
def check_system_health():
    """
    Проверка здоровья системы
    """
    app = create_app()
    
    with app.app_context():
        try:
            from app.utils.cache_manager import cache_manager
            
            # Проверка БД
            db_healthy = True
            try:
                db.session.execute('SELECT 1')
            except Exception as e:
                db_healthy = False
                logger.error(f"Database health check failed: {e}")
            
            # Проверка кэша
            cache_stats = cache_manager.get_stats()
            
            # Проверка дискового пространства
            import shutil
            disk_usage = shutil.disk_usage('/')
            disk_free_percent = (disk_usage.free / disk_usage.total) * 100
            
            health_report = {
                'timestamp': datetime.utcnow().isoformat(),
                'database': 'healthy' if db_healthy else 'unhealthy',
                'cache': cache_stats,
                'disk_free_percent': round(disk_free_percent, 2),
                'status': 'healthy' if db_healthy and disk_free_percent > 10 else 'warning'
            }
            
            logger.info(f"System health check: {health_report['status']}")
            
            return health_report
            
        except Exception as e:
            logger.error(f"Health check error: {e}")
            return {'status': 'error', 'message': str(e)}

@celery_app.task
def rotate_logs(keep_days=30):
    """
    Ротация логов
    """
    try:
        logs_dir = 'logs'
        if not os.path.exists(logs_dir):
            return {'status': 'success', 'rotated': 0}
        
        cutoff_time = datetime.utcnow() - timedelta(days=keep_days)
        rotated_count = 0
        
        for filename in os.listdir(logs_dir):
            if filename.endswith('.log'):
                filepath = os.path.join(logs_dir, filename)
                
                if os.path.isfile(filepath):
                    file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                    
                    if file_time < cutoff_time:
                        # Архивируем старый лог
                        import gzip
                        import shutil
                        
                        with open(filepath, 'rb') as f_in:
                            with gzip.open(f"{filepath}.gz", 'wb') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                        
                        os.remove(filepath)
                        rotated_count += 1
                        logger.info(f"Rotated log: {filename}")
        
        return {
            'status': 'success',
            'rotated': rotated_count
        }
        
    except Exception as e:
        logger.error(f"Log rotation error: {e}")
        return {'status': 'error', 'message': str(e)}
