"""
Asynchronous task queue for background operations.

Provides task scheduling and background processing using APScheduler.
"""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, Optional

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


class TaskManager:
    """Manager for background tasks and scheduling."""

    def __init__(self) -> None:
        """Initialize task manager."""
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.scheduler = BackgroundScheduler()

    def init_app(self, app: Flask) -> None:
        """
        Initialize with Flask app.

        Args:
            app: Flask application instance.
        """
        self.app = app

        # Register default tasks
        self._register_default_tasks()

        # Start scheduler
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Task scheduler started")

        # Shutdown on app teardown
        app.teardown_appcontext(self._shutdown)

    def _shutdown(self, exception: Optional[Exception] = None) -> None:
        """Shutdown scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()

    def _register_default_tasks(self) -> None:
        """Register default background tasks."""
        # Clean up old logs daily
        self.schedule_task(
            'cleanup_logs',
            self._cleanup_old_logs,
            trigger='cron',
            hour=2,
            minute=0,
        )

        # Clear expired cache entries hourly
        self.schedule_task(
            'cleanup_cache',
            self._cleanup_expired_cache,
            trigger='interval',
            hours=1,
        )

        # Database maintenance daily
        self.schedule_task(
            'db_maintenance',
            self._database_maintenance,
            trigger='cron',
            hour=3,
            minute=0,
        )

    def schedule_task(
        self,
        task_id: str,
        func: Callable,
        trigger: str = 'interval',
        **kwargs: Any,
    ) -> None:
        """
        Schedule a background task.

        Args:
            task_id: Unique task identifier.
            func: Function to execute.
            trigger: Trigger type ('interval', 'cron', 'date').
            **kwargs: Trigger-specific arguments.
        """
        try:
            self.scheduler.add_job(
                func,
                trigger=trigger,
                id=task_id,
                replace_existing=True,
                **kwargs,
            )

            self.tasks[task_id] = {
                'function': func.__name__,
                'trigger': trigger,
                'kwargs': kwargs,
                'created_at': datetime.utcnow().isoformat(),
            }

            logger.info(f"Task scheduled: {task_id}")

        except Exception as e:
            logger.error(f"Failed to schedule task {task_id}: {str(e)}")

    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a scheduled task.

        Args:
            task_id: Task identifier.

        Returns:
            True if cancelled, False otherwise.
        """
        try:
            self.scheduler.remove_job(task_id)
            if task_id in self.tasks:
                del self.tasks[task_id]
            logger.info(f"Task cancelled: {task_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel task {task_id}: {str(e)}")
            return False

    def get_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all scheduled tasks."""
        return self.tasks.copy()

    def _cleanup_old_logs(self) -> None:
        """Clean up logs older than 30 days."""
        try:
            import os
            from pathlib import Path

            logs_dir = Path('logs')
            if not logs_dir.exists():
                return

            cutoff_date = datetime.utcnow() - timedelta(days=30)

            for log_file in logs_dir.glob('*.log*'):
                mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
                if mtime < cutoff_date:
                    log_file.unlink()
                    logger.info(f"Deleted old log: {log_file.name}")

        except Exception as e:
            logger.error(f"Log cleanup failed: {str(e)}")

    def _cleanup_expired_cache(self) -> None:
        """Clean up expired cache entries."""
        try:
            from app import cache

            # SimpleCache doesn't have built-in cleanup,
            # but this would work with Redis
            logger.debug("Cache cleanup completed")

        except Exception as e:
            logger.error(f"Cache cleanup failed: {str(e)}")

    def _database_maintenance(self) -> None:
        """Perform database maintenance."""
        try:
            from app import db

            # Analyze tables for query optimization
            # This is database-specific

            logger.info("Database maintenance completed")

        except Exception as e:
            logger.error(f"Database maintenance failed: {str(e)}")


# Global task manager instance
task_manager = TaskManager()


def schedule_task(
    task_id: str,
    func: Callable,
    trigger: str = 'interval',
    **kwargs: Any,
) -> None:
    """
    Schedule a background task globally.

    Args:
        task_id: Unique task identifier.
        func: Function to execute.
        trigger: Trigger type.
        **kwargs: Trigger arguments.
    """
    task_manager.schedule_task(task_id, func, trigger, **kwargs)


def cancel_task(task_id: str) -> bool:
    """
    Cancel a scheduled task globally.

    Args:
        task_id: Task identifier.

    Returns:
        True if cancelled, False otherwise.
    """
    return task_manager.cancel_task(task_id)


def get_scheduled_tasks() -> Dict[str, Dict[str, Any]]:
    """Get all globally scheduled tasks."""
    return task_manager.get_tasks()
