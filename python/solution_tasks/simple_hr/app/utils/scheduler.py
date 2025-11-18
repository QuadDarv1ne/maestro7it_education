"""
Планировщик фоновых задач для Simple HR
Использует APScheduler для автоматизации рутинных операций
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import logging
from pathlib import Path
import shutil
from typing import Optional

from app import db
from app.models import Employee, Vacation, AuditLog, Notification
from app.utils.backup import create_backup
from app.utils.vacation_reminders import send_vacation_reminders

logger = logging.getLogger(__name__)

# Глобальный планировщик
scheduler: Optional[BackgroundScheduler] = None


def cleanup_old_logs(days: int = 30):
    """Очистка старых логов"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Очистка логов аудита
        deleted_count = AuditLog.query.filter(
            AuditLog.timestamp < cutoff_date
        ).delete()
        
        db.session.commit()
        logger.info(f"Удалено {deleted_count} записей аудита старше {days} дней")
        
        # Очистка файлов логов
        logs_dir = Path('logs')
        if logs_dir.exists():
            for log_file in logs_dir.glob('*.log'):
                if log_file.stat().st_mtime < cutoff_date.timestamp():
                    log_file.unlink()
                    logger.info(f"Удален файл лога: {log_file}")
                    
    except Exception as e:
        logger.error(f"Ошибка при очистке логов: {e}")
        db.session.rollback()


def cleanup_old_notifications(days: int = 90):
    """Очистка старых прочитанных уведомлений"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        deleted_count = Notification.query.filter(
            Notification.created_at < cutoff_date,
            Notification.is_read == True
        ).delete()
        
        db.session.commit()
        logger.info(f"Удалено {deleted_count} старых уведомлений")
        
    except Exception as e:
        logger.error(f"Ошибка при очистке уведомлений: {e}")
        db.session.rollback()


def auto_backup():
    """Автоматическое резервное копирование"""
    try:
        backup_path = create_backup()
        logger.info(f"Автоматический бэкап создан: {backup_path}")
        
        # Удаление старых бэкапов (храним последние 30)
        backup_dir = Path('backups')
        if backup_dir.exists():
            backups = sorted(backup_dir.glob('*.db'), key=lambda p: p.stat().st_mtime)
            if len(backups) > 30:
                for old_backup in backups[:-30]:
                    old_backup.unlink()
                    logger.info(f"Удален старый бэкап: {old_backup}")
                    
    except Exception as e:
        logger.error(f"Ошибка при создании автоматического бэкапа: {e}")


def check_vacation_expiry():
    """Проверка истекающих отпусков и отправка уведомлений"""
    try:
        send_vacation_reminders()
        logger.info("Проверка истекающих отпусков выполнена")
    except Exception as e:
        logger.error(f"Ошибка при проверке отпусков: {e}")


def update_employee_statistics():
    """Обновление статистики сотрудников (кэш)"""
    try:
        from app.utils.analytics import calculate_employee_statistics
        
        total = Employee.query.count()
        active = Employee.query.filter_by(status='active').count()
        dismissed = Employee.query.filter_by(status='dismissed').count()
        
        # Можно сохранить в Redis или кэш
        logger.info(f"Статистика обновлена: всего={total}, активных={active}, уволенных={dismissed}")
        
    except Exception as e:
        logger.error(f"Ошибка при обновлении статистики: {e}")


def cleanup_temp_files():
    """Очистка временных файлов"""
    try:
        temp_dirs = ['uploads/temp', 'instance/temp']
        
        for temp_dir in temp_dirs:
            temp_path = Path(temp_dir)
            if temp_path.exists():
                cutoff = datetime.now() - timedelta(hours=24)
                
                for temp_file in temp_path.iterdir():
                    if temp_file.stat().st_mtime < cutoff.timestamp():
                        if temp_file.is_file():
                            temp_file.unlink()
                        elif temp_file.is_dir():
                            shutil.rmtree(temp_file)
                        logger.info(f"Удален временный файл: {temp_file}")
                        
    except Exception as e:
        logger.error(f"Ошибка при очистке временных файлов: {e}")


def health_check():
    """Проверка работоспособности системы"""
    try:
        # Проверка подключения к БД
        db.session.execute('SELECT 1')
        
        # Проверка свободного места
        import psutil
        disk = psutil.disk_usage('.')
        if disk.percent > 90:
            logger.warning(f"Мало места на диске: {disk.percent}% использовано")
            
        # Проверка памяти
        memory = psutil.virtual_memory()
        if memory.percent > 90:
            logger.warning(f"Мало оперативной памяти: {memory.percent}% использовано")
            
        logger.debug("Health check пройден успешно")
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")


def init_scheduler(app):
    """Инициализация планировщика задач"""
    global scheduler
    
    if scheduler is not None:
        logger.warning("Планировщик уже инициализирован")
        return scheduler
    
    scheduler = BackgroundScheduler(
        daemon=True,
        timezone='Europe/Moscow'
    )
    
    # Ежедневные задачи
    scheduler.add_job(
        func=cleanup_old_logs,
        trigger=CronTrigger(hour=2, minute=0),  # 02:00 каждый день
        id='cleanup_logs',
        name='Очистка старых логов',
        replace_existing=True
    )
    
    scheduler.add_job(
        func=cleanup_old_notifications,
        trigger=CronTrigger(hour=3, minute=0),  # 03:00 каждый день
        id='cleanup_notifications',
        name='Очистка старых уведомлений',
        replace_existing=True
    )
    
    scheduler.add_job(
        func=auto_backup,
        trigger=CronTrigger(hour=1, minute=0),  # 01:00 каждый день
        id='auto_backup',
        name='Автоматический бэкап',
        replace_existing=True
    )
    
    scheduler.add_job(
        func=check_vacation_expiry,
        trigger=CronTrigger(hour=9, minute=0),  # 09:00 каждый день
        id='check_vacations',
        name='Проверка истекающих отпусков',
        replace_existing=True
    )
    
    scheduler.add_job(
        func=cleanup_temp_files,
        trigger=CronTrigger(hour=4, minute=0),  # 04:00 каждый день
        id='cleanup_temp',
        name='Очистка временных файлов',
        replace_existing=True
    )
    
    # Задачи каждые N минут
    scheduler.add_job(
        func=update_employee_statistics,
        trigger=IntervalTrigger(hours=1),  # Каждый час
        id='update_stats',
        name='Обновление статистики',
        replace_existing=True
    )
    
    scheduler.add_job(
        func=health_check,
        trigger=IntervalTrigger(minutes=5),  # Каждые 5 минут
        id='health_check',
        name='Проверка работоспособности',
        replace_existing=True
    )
    
    # Запуск планировщика
    scheduler.start()
    logger.info("Планировщик задач запущен успешно")
    logger.info(f"Активных задач: {len(scheduler.get_jobs())}")
    
    # Регистрация shutdown
    import atexit
    atexit.register(lambda: shutdown_scheduler())
    
    return scheduler


def shutdown_scheduler():
    """Остановка планировщика"""
    global scheduler
    if scheduler is not None:
        scheduler.shutdown(wait=False)
        logger.info("Планировщик задач остановлен")
        scheduler = None


def get_scheduled_jobs():
    """Получить список запланированных задач"""
    if scheduler is None:
        return []
    
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            'id': job.id,
            'name': job.name,
            'next_run': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else None,
            'trigger': str(job.trigger)
        })
    
    return jobs


def run_job_now(job_id: str):
    """Запустить задачу немедленно"""
    if scheduler is None:
        raise RuntimeError("Планировщик не инициализирован")
    
    job = scheduler.get_job(job_id)
    if job is None:
        raise ValueError(f"Задача {job_id} не найдена")
    
    job.modify(next_run_time=datetime.now())
    logger.info(f"Задача {job_id} запущена вручную")


def pause_job(job_id: str):
    """Приостановить задачу"""
    if scheduler is None:
        raise RuntimeError("Планировщик не инициализирован")
    
    scheduler.pause_job(job_id)
    logger.info(f"Задача {job_id} приостановлена")


def resume_job(job_id: str):
    """Возобновить задачу"""
    if scheduler is None:
        raise RuntimeError("Планировщик не инициализирован")
    
    scheduler.resume_job(job_id)
    logger.info(f"Задача {job_id} возобновлена")
