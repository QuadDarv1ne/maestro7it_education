"""
Мониторинг и управление Celery задачами
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from celery import current_app
from celery.result import AsyncResult

logger = logging.getLogger(__name__)


class CeleryMonitor:
    """Мониторинг Celery workers и задач"""
    
    def __init__(self, celery_app=None):
        self.celery = celery_app or current_app
        
    def get_workers_status(self) -> Dict[str, Any]:
        """Получить статус всех workers"""
        try:
            inspect = self.celery.control.inspect()
            
            active = inspect.active() or {}
            reserved = inspect.reserved() or {}
            stats = inspect.stats() or {}
            registered = inspect.registered() or {}
            
            workers_info = []
            for worker_name in stats.keys():
                worker_stats = stats.get(worker_name, {})
                workers_info.append({
                    'name': worker_name,
                    'status': 'online',
                    'active_tasks': len(active.get(worker_name, [])),
                    'reserved_tasks': len(reserved.get(worker_name, [])),
                    'total_tasks': worker_stats.get('total', {}).get('tasks', 0),
                    'registered_tasks': len(registered.get(worker_name, [])),
                    'pool': worker_stats.get('pool', {})
                })
            
            return {
                'workers': workers_info,
                'total_workers': len(workers_info),
                'total_active_tasks': sum(w['active_tasks'] for w in workers_info),
                'total_reserved_tasks': sum(w['reserved_tasks'] for w in workers_info),
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get workers status: {e}")
            return {
                'workers': [],
                'total_workers': 0,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def get_active_tasks(self) -> List[Dict[str, Any]]:
        """Получить список активных задач"""
        try:
            inspect = self.celery.control.inspect()
            active = inspect.active() or {}
            
            tasks = []
            for worker_name, worker_tasks in active.items():
                for task in worker_tasks:
                    tasks.append({
                        'id': task.get('id'),
                        'name': task.get('name'),
                        'worker': worker_name,
                        'args': task.get('args'),
                        'kwargs': task.get('kwargs'),
                        'time_start': task.get('time_start'),
                        'acknowledged': task.get('acknowledged', False)
                    })
            
            return tasks
        except Exception as e:
            logger.error(f"Failed to get active tasks: {e}")
            return []
    
    def get_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """Получить список запланированных задач"""
        try:
            inspect = self.celery.control.inspect()
            scheduled = inspect.scheduled() or {}
            
            tasks = []
            for worker_name, worker_tasks in scheduled.items():
                for task in worker_tasks:
                    tasks.append({
                        'id': task.get('request', {}).get('id'),
                        'name': task.get('request', {}).get('name'),
                        'worker': worker_name,
                        'eta': task.get('eta'),
                        'priority': task.get('priority', 5)
                    })
            
            return tasks
        except Exception as e:
            logger.error(f"Failed to get scheduled tasks: {e}")
            return []
    
    def get_task_result(self, task_id: str) -> Dict[str, Any]:
        """Получить результат задачи по ID"""
        try:
            result = AsyncResult(task_id, app=self.celery)
            
            return {
                'id': task_id,
                'state': result.state,
                'result': result.result if result.successful() else None,
                'traceback': result.traceback if result.failed() else None,
                'ready': result.ready(),
                'successful': result.successful(),
                'failed': result.failed()
            }
        except Exception as e:
            logger.error(f"Failed to get task result for {task_id}: {e}")
            return {
                'id': task_id,
                'error': str(e)
            }
    
    def revoke_task(self, task_id: str, terminate: bool = False) -> bool:
        """Отменить задачу"""
        try:
            self.celery.control.revoke(task_id, terminate=terminate)
            logger.info(f"Task {task_id} revoked (terminate={terminate})")
            return True
        except Exception as e:
            logger.error(f"Failed to revoke task {task_id}: {e}")
            return False
    
    def purge_queue(self, queue_name: Optional[str] = None) -> int:
        """Очистить очередь"""
        try:
            if queue_name:
                count = self.celery.control.purge()
            else:
                count = self.celery.control.purge()
            logger.info(f"Purged {count} tasks from queue")
            return count
        except Exception as e:
            logger.error(f"Failed to purge queue: {e}")
            return 0
    
    def get_queue_length(self, queue_name: str = 'celery') -> int:
        """Получить длину очереди"""
        try:
            from kombu import Connection
            with Connection(self.celery.conf.broker_url) as conn:
                queue = conn.SimpleQueue(queue_name)
                length = queue.qsize()
                queue.close()
                return length
        except Exception as e:
            logger.error(f"Failed to get queue length: {e}")
            return 0
    
    def get_failed_tasks(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Получить список неудачных задач из Redis"""
        try:
            import redis
            redis_url = self.celery.conf.result_backend
            r = redis.from_url(redis_url)
            
            # Получаем ключи результатов
            keys = r.keys('celery-task-meta-*')
            failed_tasks = []
            
            for key in keys[:limit]:
                try:
                    data = r.get(key)
                    if data:
                        import json
                        task_data = json.loads(data)
                        if task_data.get('status') == 'FAILURE':
                            failed_tasks.append({
                                'id': task_data.get('task_id'),
                                'name': task_data.get('name'),
                                'exception': task_data.get('result'),
                                'traceback': task_data.get('traceback'),
                                'date_done': task_data.get('date_done')
                            })
                except Exception as e:
                    logger.warning(f"Failed to parse task data: {e}")
                    continue
            
            return failed_tasks
        except Exception as e:
            logger.error(f"Failed to get failed tasks: {e}")
            return []
    
    def get_task_stats(self) -> Dict[str, Any]:
        """Получить статистику задач"""
        try:
            inspect = self.celery.control.inspect()
            stats = inspect.stats() or {}
            
            total_stats = {
                'total_tasks_executed': 0,
                'total_tasks_received': 0,
                'workers': []
            }
            
            for worker_name, worker_stats in stats.items():
                total = worker_stats.get('total', {})
                total_stats['total_tasks_executed'] += total.get('tasks', 0)
                total_stats['workers'].append({
                    'name': worker_name,
                    'tasks_executed': total.get('tasks', 0),
                    'pool': worker_stats.get('pool', {})
                })
            
            return total_stats
        except Exception as e:
            logger.error(f"Failed to get task stats: {e}")
            return {}
    
    def restart_worker(self, worker_name: str) -> bool:
        """Перезапустить worker (graceful restart)"""
        try:
            self.celery.control.pool_restart([worker_name])
            logger.info(f"Worker {worker_name} restarted")
            return True
        except Exception as e:
            logger.error(f"Failed to restart worker {worker_name}: {e}")
            return False
    
    def get_registered_tasks(self) -> Dict[str, List[str]]:
        """Получить список зарегистрированных задач"""
        try:
            inspect = self.celery.control.inspect()
            registered = inspect.registered() or {}
            return registered
        except Exception as e:
            logger.error(f"Failed to get registered tasks: {e}")
            return {}
    
    def get_beat_schedule(self) -> Dict[str, Any]:
        """Получить расписание периодических задач"""
        try:
            schedule = self.celery.conf.beat_schedule
            
            formatted_schedule = {}
            for task_name, task_config in schedule.items():
                formatted_schedule[task_name] = {
                    'task': task_config.get('task'),
                    'schedule': str(task_config.get('schedule')),
                    'args': task_config.get('args', []),
                    'kwargs': task_config.get('kwargs', {}),
                    'options': task_config.get('options', {})
                }
            
            return formatted_schedule
        except Exception as e:
            logger.error(f"Failed to get beat schedule: {e}")
            return {}


class TaskRetryManager:
    """Управление повторными попытками задач"""
    
    def __init__(self, celery_app=None):
        self.celery = celery_app or current_app
    
    def retry_failed_tasks(self, task_name: Optional[str] = None, max_retries: int = 3) -> int:
        """Повторить неудачные задачи"""
        monitor = CeleryMonitor(self.celery)
        failed_tasks = monitor.get_failed_tasks()
        
        retried_count = 0
        for task in failed_tasks:
            if task_name and task.get('name') != task_name:
                continue
            
            try:
                # Получаем задачу и повторяем
                task_func = self.celery.tasks.get(task.get('name'))
                if task_func:
                    task_func.apply_async(
                        args=task.get('args', []),
                        kwargs=task.get('kwargs', {}),
                        retry=True,
                        max_retries=max_retries
                    )
                    retried_count += 1
                    logger.info(f"Retried task {task.get('id')}")
            except Exception as e:
                logger.error(f"Failed to retry task {task.get('id')}: {e}")
        
        return retried_count


class TaskRateLimiter:
    """Ограничение частоты выполнения задач"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def is_allowed(self, task_name: str, limit: int, period: int) -> bool:
        """
        Проверить, разрешено ли выполнение задачи
        
        Args:
            task_name: имя задачи
            limit: максимальное количество выполнений
            period: период в секундах
        """
        key = f"task_rate_limit:{task_name}"
        
        try:
            current = self.redis.get(key)
            if current is None:
                self.redis.setex(key, period, 1)
                return True
            
            current = int(current)
            if current >= limit:
                return False
            
            self.redis.incr(key)
            return True
        except Exception as e:
            logger.error(f"Rate limit check failed: {e}")
            return True  # Разрешаем в случае ошибки
    
    def reset_limit(self, task_name: str):
        """Сбросить ограничение для задачи"""
        key = f"task_rate_limit:{task_name}"
        try:
            self.redis.delete(key)
        except Exception as e:
            logger.error(f"Failed to reset rate limit: {e}")


# Глобальные экземпляры
celery_monitor = CeleryMonitor()
task_retry_manager = TaskRetryManager()
