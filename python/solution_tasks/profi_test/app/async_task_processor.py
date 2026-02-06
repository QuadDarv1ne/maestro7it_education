"""
Advanced asynchronous task processing with Celery optimization
"""
import logging
from celery import Celery
from celery.schedules import crontab
from flask import current_app
from typing import Dict, Any, Optional
import time
import json
from datetime import datetime
import asyncio

logger = logging.getLogger(__name__)

class AsyncTaskProcessor:
    """Advanced async task processing with performance optimization"""
    
    def __init__(self, app=None):
        self.app = app
        self.celery = None
        self.task_stats = {}
        self.performance_metrics = {}
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize Celery with Flask app"""
        self.app = app
        
        # Configure Celery
        self.celery = Celery(
            app.import_name,
            backend=app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0'),
            broker=app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
        )
        
        # Update Celery configuration
        self.celery.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True,
            task_track_started=True,
            worker_prefetch_multiplier=1,  # Reduce memory usage
            task_acks_late=True,  # Acknowledge after task completion
            worker_max_tasks_per_child=1000,  # Restart workers periodically
            task_compression='gzip',  # Compress large task data
            result_compression='gzip',
            worker_disable_rate_limits=False,
            task_soft_time_limit=300,  # 5 minutes soft limit
            task_time_limit=360,  # 6 minutes hard limit
        )
        
        # Setup task routes for better distribution
        self.celery.conf.task_routes = {
            'app.tasks.high_priority.*': {'queue': 'high_priority'},
            'app.tasks.medium_priority.*': {'queue': 'medium_priority'},
            'app.tasks.low_priority.*': {'queue': 'low_priority'},
            'app.tasks.background.*': {'queue': 'background'},
        }
        
        # Register task classes
        self.register_tasks()
        
        # Setup periodic tasks
        self.setup_periodic_tasks()
    
    def register_tasks(self):
        """Register all task classes with Celery"""
        
        @self.celery.task(bind=True, name='app.tasks.high_priority.send_notification')
        def send_notification_task(self, user_id: int, message: str, notification_type: str = 'info'):
            """High priority notification sending task"""
            try:
                start_time = time.time()
                
                # Import here to avoid circular imports
                from app.advanced_notifications import notification_manager
                
                result = notification_manager.create_notification(
                    user_id=user_id,
                    title=message[:50],
                    message=message,
                    notification_type=notification_type
                )
                
                execution_time = time.time() - start_time
                self.update_task_stats('send_notification', execution_time, 'success')
                
                return {
                    'status': 'success',
                    'notification_id': result.id if result else None,
                    'execution_time': execution_time
                }
                
            except Exception as e:
                execution_time = time.time() - start_time
                self.update_task_stats('send_notification', execution_time, 'error', str(e))
                logger.error(f"Notification task failed: {e}")
                raise
    
        @self.celery.task(bind=True, name='app.tasks.medium_priority.process_ml_recommendation')
        def process_ml_recommendation_task(self, user_id: int, test_result_id: int):
            """Medium priority ML recommendation processing"""
            try:
                start_time = time.time()
                
                from app.ml_recommendations import recommendation_engine
                
                recommendations = recommendation_engine.generate_recommendations(
                    user_id=user_id,
                    test_result_id=test_result_id
                )
                
                execution_time = time.time() - start_time
                self.update_task_stats('process_ml_recommendation', execution_time, 'success')
                
                return {
                    'status': 'success',
                    'recommendations_count': len(recommendations) if recommendations else 0,
                    'execution_time': execution_time
                }
                
            except Exception as e:
                execution_time = time.time() - start_time
                self.update_task_stats('process_ml_recommendation', execution_time, 'error', str(e))
                logger.error(f"ML recommendation task failed: {e}")
                raise
    
        @self.celery.task(bind=True, name='app.tasks.low_priority.generate_report')
        def generate_report_task(self, user_id: int, report_type: str, filters: Dict = None):
            """Low priority report generation task"""
            try:
                start_time = time.time()
                
                from app.enhanced_reports import enhanced_reports
                
                report = enhanced_reports.generate_report(
                    user_id=user_id,
                    report_type=report_type,
                    filters=filters or {}
                )
                
                execution_time = time.time() - start_time
                self.update_task_stats('generate_report', execution_time, 'success')
                
                return {
                    'status': 'success',
                    'report_id': report.id if hasattr(report, 'id') else None,
                    'execution_time': execution_time
                }
                
            except Exception as e:
                execution_time = time.time() - start_time
                self.update_task_stats('generate_report', execution_time, 'error', str(e))
                logger.error(f"Report generation task failed: {e}")
                raise
    
        @self.celery.task(bind=True, name='app.tasks.background.data_cleanup')
        def data_cleanup_task(self, days_old: int = 30):
            """Background data cleanup task"""
            try:
                start_time = time.time()
                
                # Cleanup old notifications
                from app.models import Notification, db
                from datetime import datetime, timedelta
                
                cutoff_date = datetime.utcnow() - timedelta(days=days_old)
                deleted_count = Notification.query.filter(
                    Notification.created_at < cutoff_date
                ).delete()
                
                db.session.commit()
                
                execution_time = time.time() - start_time
                self.update_task_stats('data_cleanup', execution_time, 'success')
                
                return {
                    'status': 'success',
                    'deleted_records': deleted_count,
                    'execution_time': execution_time
                }
                
            except Exception as e:
                execution_time = time.time() - start_time
                self.update_task_stats('data_cleanup', execution_time, 'error', str(e))
                logger.error(f"Data cleanup task failed: {e}")
                raise
    
    def setup_periodic_tasks(self):
        """Setup periodic task scheduling"""
        self.celery.conf.beat_schedule = {
            'daily-data-cleanup': {
                'task': 'app.tasks.background.data_cleanup',
                'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM UTC
                'args': (30,)  # Cleanup data older than 30 days
            },
            'hourly-performance-monitoring': {
                'task': 'app.tasks.low_priority.performance_monitoring',
                'schedule': crontab(minute=0),  # Run every hour
                'args': ()
            },
            'daily-ml-model-update': {
                'task': 'app.tasks.medium_priority.update_ml_models',
                'schedule': crontab(hour=3, minute=0),  # Run daily at 3 AM UTC
                'args': ()
            }
        }
        
        # Add performance monitoring task
        @self.celery.task(name='app.tasks.low_priority.performance_monitoring')
        def performance_monitoring_task():
            """Monitor system performance and generate reports"""
            try:
                from app.performance_monitoring import db_performance_monitor
                from app.system_monitoring import system_monitor
                
                # Collect performance metrics
                db_metrics = db_performance_monitor.get_current_metrics()
                system_metrics = system_monitor.get_system_metrics()
                
                # Generate performance report
                report = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'database_metrics': db_metrics,
                    'system_metrics': system_metrics,
                    'task_stats': self.task_stats
                }
                
                logger.info(f"Performance monitoring report generated: {json.dumps(report, indent=2)}")
                return report
                
            except Exception as e:
                logger.error(f"Performance monitoring task failed: {e}")
                raise
        
        # Add ML model update task
        @self.celery.task(name='app.tasks.medium_priority.update_ml_models')
        def update_ml_models_task():
            """Update ML models with new training data"""
            try:
                from app.ml_recommendations import recommendation_engine
                
                # Retrain models with new data
                training_result = recommendation_engine.retrain_models()
                
                logger.info(f"ML models updated: {training_result}")
                return training_result
                
            except Exception as e:
                logger.error(f"ML model update task failed: {e}")
                raise
    
    def update_task_stats(self, task_name: str, execution_time: float, status: str, error: str = None):
        """Update task execution statistics"""
        if task_name not in self.task_stats:
            self.task_stats[task_name] = {
                'total_executions': 0,
                'successful_executions': 0,
                'failed_executions': 0,
                'total_execution_time': 0,
                'avg_execution_time': 0,
                'min_execution_time': float('inf'),
                'max_execution_time': 0,
                'last_error': None
            }
        
        stats = self.task_stats[task_name]
        stats['total_executions'] += 1
        stats['total_execution_time'] += execution_time
        
        if status == 'success':
            stats['successful_executions'] += 1
        else:
            stats['failed_executions'] += 1
            stats['last_error'] = error
        
        stats['avg_execution_time'] = stats['total_execution_time'] / stats['total_executions']
        stats['min_execution_time'] = min(stats['min_execution_time'], execution_time)
        stats['max_execution_time'] = max(stats['max_execution_time'], execution_time)
    
    def get_task_statistics(self) -> Dict[str, Any]:
        """Get comprehensive task execution statistics"""
        return {
            'task_stats': self.task_stats,
            'celery_config': dict(self.celery.conf),
            'worker_info': self.get_worker_info()
        }
    
    def get_worker_info(self) -> Dict[str, Any]:
        """Get information about Celery workers"""
        try:
            inspector = self.celery.control.inspect()
            return {
                'active': inspector.active() or {},
                'scheduled': inspector.scheduled() or {},
                'reserved': inspector.reserved() or {},
                'stats': inspector.stats() or {}
            }
        except Exception as e:
            logger.error(f"Error getting worker info: {e}")
            return {'error': str(e)}

# Global instance
async_task_processor = AsyncTaskProcessor()

# Flask CLI commands
def register_async_commands(app):
    """Register CLI commands for async task management"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('task-stats')
    @with_appcontext
    def show_task_stats():
        """Show async task execution statistics"""
        stats = async_task_processor.get_task_statistics()
        click.echo("Async Task Statistics:")
        click.echo(json.dumps(stats, indent=2, default=str))
    
    @app.cli.command('task-cleanup')
    @click.option('--days', default=30, help='Days old to cleanup')
    @with_appcontext
    def cleanup_old_tasks(days):
        """Cleanup old task results"""
        try:
            from celery import current_app as celery_app
            celery_app.control.purge()
            click.echo(f"Cleaned up tasks older than {days} days")
        except Exception as e:
            click.echo(f"Error cleaning up tasks: {e}")
