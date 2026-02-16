"""
Celery приложение для асинхронных задач
Включает парсинг турниров, отправку уведомлений, генерацию отчетов
"""
from celery import Celery
from celery.schedules import crontab
import os
import logging

logger = logging.getLogger(__name__)

# Конфигурация Celery
celery_app = Celery(
    'chess_calendar',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
    include=[
        'app.tasks.parser_tasks',
        'app.tasks.notification_tasks',
        'app.tasks.analytics_tasks',
        'app.tasks.maintenance_tasks'
    ]
)

# Конфигурация
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут
    task_soft_time_limit=25 * 60,  # 25 минут
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    result_expires=3600,  # Результаты хранятся 1 час
)

# Периодические задачи
celery_app.conf.beat_schedule = {
    # Парсинг турниров каждые 6 часов
    'parse-fide-tournaments': {
        'task': 'app.tasks.parser_tasks.parse_fide_tournaments',
        'schedule': crontab(minute=0, hour='*/6'),
    },
    'parse-cfr-tournaments': {
        'task': 'app.tasks.parser_tasks.parse_cfr_tournaments',
        'schedule': crontab(minute=30, hour='*/6'),
    },
    
    # Отправка уведомлений каждый час
    'send-pending-notifications': {
        'task': 'app.tasks.notification_tasks.send_pending_notifications',
        'schedule': crontab(minute=0, hour='*'),
    },
    
    # Проверка предстоящих турниров каждый день в 9:00
    'check-upcoming-tournaments': {
        'task': 'app.tasks.notification_tasks.notify_upcoming_tournaments',
        'schedule': crontab(minute=0, hour=9),
    },
    
    # Генерация аналитики каждый день в 3:00
    'generate-daily-analytics': {
        'task': 'app.tasks.analytics_tasks.generate_daily_report',
        'schedule': crontab(minute=0, hour=3),
    },
    
    # Очистка старых данных каждую неделю
    'cleanup-old-data': {
        'task': 'app.tasks.maintenance_tasks.cleanup_old_data',
        'schedule': crontab(minute=0, hour=2, day_of_week=1),
    },
    
    # Резервное копирование каждый день в 4:00
    'backup-database': {
        'task': 'app.tasks.maintenance_tasks.backup_database',
        'schedule': crontab(minute=0, hour=4),
    },
    
    # Обновление кэша рекомендаций каждые 2 часа
    'update-recommendations-cache': {
        'task': 'app.tasks.analytics_tasks.update_recommendations_cache',
        'schedule': crontab(minute=0, hour='*/2'),
    },
}

# Маршрутизация задач по очередям
celery_app.conf.task_routes = {
    'app.tasks.parser_tasks.*': {'queue': 'parser'},
    'app.tasks.notification_tasks.*': {'queue': 'notifications'},
    'app.tasks.analytics_tasks.*': {'queue': 'analytics'},
    'app.tasks.maintenance_tasks.*': {'queue': 'maintenance'},
}

# Приоритеты очередей
celery_app.conf.task_default_priority = 5
celery_app.conf.task_queue_max_priority = 10

logger.info("Celery application configured")
