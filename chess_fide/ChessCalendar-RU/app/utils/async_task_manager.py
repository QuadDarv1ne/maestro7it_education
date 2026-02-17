"""
Менеджер асинхронных задач с приоритетами и зависимостями
"""
import logging
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
from celery import group, chain, chord
from celery.result import AsyncResult

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Приоритеты задач"""
    LOW = 1
    NORMAL = 5
    HIGH = 8
    CRITICAL = 10


class TaskStatus(Enum):
    """Статусы задач"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    RETRY = "retry"
    REVOKED = "revoked"


class AsyncTaskManager:
    """Менеджер для управления асинхронными задачами"""
    
    def __init__(self, celery_app):
        self.celery = celery_app
        
    def submit_task(
        self,
        task_name: str,
        args: tuple = (),
        kwargs: dict = None,
        priority: TaskPriority = TaskPriority.NORMAL,
        eta: Optional[datetime] = None,
        countdown: Optional[int] = None,
        expires: Optional[int] = None,
        retry: bool = True,
        max_retries: int = 3
    ) -> str:
        """
        Отправить задачу на выполнение
        
        Args:
            task_name: имя задачи
            args: позиционные аргументы
            kwargs: именованные аргументы
            priority: приоритет задачи
            eta: время выполнения
            countdown: задержка в секундах
            expires: время истечения в секундах
            retry: повторять при ошибке
            max_retries: максимальное количество повторов
            
        Returns:
            task_id: ID задачи
        """
        kwargs = kwargs or {}
        
        task = self.celery.send_task(
            task_name,
            args=args,
            kwargs=kwargs,
            priority=priority.value,
            eta=eta,
            countdown=countdown,
            expires=expires,
            retry=retry,
            max_retries=max_retries
        )
        
        logger.info(f"Task {task_name} submitted with ID {task.id}")
        return task.id
    
    def submit_batch(
        self,
        task_name: str,
        items: List[Any],
        batch_size: int = 10,
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> List[str]:
        """
        Отправить пакет задач
        
        Args:
            task_name: имя задачи
            items: список элементов для обработки
            batch_size: размер пакета
            priority: приоритет
            
        Returns:
            список task_id
        """
        task_ids = []
        
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            task_id = self.submit_task(
                task_name,
                args=(batch,),
                priority=priority
            )
            task_ids.append(task_id)
        
        logger.info(f"Submitted {len(task_ids)} batch tasks for {task_name}")
        return task_ids
    
    def submit_parallel(
        self,
        task_name: str,
        items: List[Any],
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> str:
        """
        Отправить задачи для параллельного выполнения
        
        Args:
            task_name: имя задачи
            items: список элементов
            priority: приоритет
            
        Returns:
            group_id: ID группы задач
        """
        task = self.celery.tasks.get(task_name)
        if not task:
            raise ValueError(f"Task {task_name} not found")
        
        job = group(task.s(item) for item in items)
        result = job.apply_async(priority=priority.value)
        
        logger.info(f"Submitted {len(items)} parallel tasks for {task_name}")
        return result.id
    
    def submit_chain(
        self,
        tasks: List[tuple],
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> str:
        """
        Отправить цепочку задач (последовательное выполнение)
        
        Args:
            tasks: список (task_name, args, kwargs)
            priority: приоритет
            
        Returns:
            chain_id: ID цепочки
        """
        signatures = []
        for task_name, args, kwargs in tasks:
            task = self.celery.tasks.get(task_name)
            if not task:
                raise ValueError(f"Task {task_name} not found")
            signatures.append(task.s(*args, **kwargs))
        
        job = chain(*signatures)
        result = job.apply_async(priority=priority.value)
        
        logger.info(f"Submitted chain of {len(tasks)} tasks")
        return result.id
    
    def submit_chord(
        self,
        parallel_tasks: List[tuple],
        callback_task: tuple,
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> str:
        """
        Отправить chord (параллельные задачи + callback)
        
        Args:
            parallel_tasks: список (task_name, args, kwargs) для параллельного выполнения
            callback_task: (task_name, args, kwargs) для callback
            priority: приоритет
            
        Returns:
            chord_id: ID chord
        """
        # Создаем параллельные задачи
        parallel_sigs = []
        for task_name, args, kwargs in parallel_tasks:
            task = self.celery.tasks.get(task_name)
            if not task:
                raise ValueError(f"Task {task_name} not found")
            parallel_sigs.append(task.s(*args, **kwargs))
        
        # Создаем callback
        callback_name, callback_args, callback_kwargs = callback_task
        callback = self.celery.tasks.get(callback_name)
        if not callback:
            raise ValueError(f"Callback task {callback_name} not found")
        
        job = chord(parallel_sigs)(callback.s(*callback_args, **callback_kwargs))
        result = job.apply_async(priority=priority.value)
        
        logger.info(f"Submitted chord with {len(parallel_tasks)} parallel tasks")
        return result.id
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Получить статус задачи"""
        result = AsyncResult(task_id, app=self.celery)
        
        return {
            'task_id': task_id,
            'state': result.state,
            'ready': result.ready(),
            'successful': result.successful(),
            'failed': result.failed(),
            'result': result.result if result.ready() else None,
            'traceback': result.traceback if result.failed() else None
        }
    
    def wait_for_task(
        self,
        task_id: str,
        timeout: Optional[float] = None,
        interval: float = 0.5
    ) -> Any:
        """
        Ожидать завершения задачи
        
        Args:
            task_id: ID задачи
            timeout: таймаут в секундах
            interval: интервал проверки
            
        Returns:
            результат задачи
        """
        result = AsyncResult(task_id, app=self.celery)
        return result.get(timeout=timeout, interval=interval)
    
    def cancel_task(self, task_id: str, terminate: bool = False) -> bool:
        """
        Отменить задачу
        
        Args:
            task_id: ID задачи
            terminate: принудительно завершить
            
        Returns:
            успешность операции
        """
        try:
            self.celery.control.revoke(task_id, terminate=terminate)
            logger.info(f"Task {task_id} cancelled (terminate={terminate})")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel task {task_id}: {e}")
            return False
    
    def retry_failed_task(self, task_id: str) -> Optional[str]:
        """
        Повторить неудачную задачу
        
        Returns:
            новый task_id или None
        """
        result = AsyncResult(task_id, app=self.celery)
        
        if not result.failed():
            logger.warning(f"Task {task_id} is not failed, cannot retry")
            return None
        
        # Получаем информацию о задаче
        task_name = result.name
        args = result.args
        kwargs = result.kwargs
        
        # Отправляем новую задачу
        new_task_id = self.submit_task(task_name, args=args, kwargs=kwargs)
        logger.info(f"Retried failed task {task_id} as {new_task_id}")
        
        return new_task_id
    
    def schedule_periodic_task(
        self,
        task_name: str,
        schedule: str,
        args: tuple = (),
        kwargs: dict = None,
        enabled: bool = True
    ):
        """
        Запланировать периодическую задачу
        
        Args:
            task_name: имя задачи
            schedule: расписание (crontab или interval)
            args: аргументы
            kwargs: именованные аргументы
            enabled: включена ли задача
        """
        from celery.schedules import crontab
        
        kwargs = kwargs or {}
        
        # Парсим расписание
        if isinstance(schedule, str):
            # Формат: "*/5 * * * *" (каждые 5 минут)
            parts = schedule.split()
            if len(parts) == 5:
                schedule = crontab(
                    minute=parts[0],
                    hour=parts[1],
                    day_of_month=parts[2],
                    month_of_year=parts[3],
                    day_of_week=parts[4]
                )
        
        # Добавляем в beat_schedule
        self.celery.conf.beat_schedule[task_name] = {
            'task': task_name,
            'schedule': schedule,
            'args': args,
            'kwargs': kwargs,
            'options': {'enabled': enabled}
        }
        
        logger.info(f"Scheduled periodic task {task_name}")


class TaskDependencyManager:
    """Управление зависимостями между задачами"""
    
    def __init__(self, task_manager: AsyncTaskManager):
        self.task_manager = task_manager
        self.dependencies = {}
    
    def add_dependency(self, task_id: str, depends_on: List[str]):
        """
        Добавить зависимость задачи
        
        Args:
            task_id: ID задачи
            depends_on: список ID задач, от которых зависит
        """
        self.dependencies[task_id] = depends_on
        logger.info(f"Task {task_id} depends on {len(depends_on)} tasks")
    
    def can_execute(self, task_id: str) -> bool:
        """Проверить, можно ли выполнить задачу"""
        if task_id not in self.dependencies:
            return True
        
        depends_on = self.dependencies[task_id]
        
        for dep_id in depends_on:
            status = self.task_manager.get_task_status(dep_id)
            if not status['successful']:
                return False
        
        return True
    
    def wait_for_dependencies(
        self,
        task_id: str,
        timeout: Optional[float] = None
    ) -> bool:
        """
        Ожидать выполнения зависимостей
        
        Returns:
            True если все зависимости выполнены успешно
        """
        if task_id not in self.dependencies:
            return True
        
        depends_on = self.dependencies[task_id]
        
        for dep_id in depends_on:
            try:
                self.task_manager.wait_for_task(dep_id, timeout=timeout)
            except Exception as e:
                logger.error(f"Dependency {dep_id} failed: {e}")
                return False
        
        return True


class TaskScheduler:
    """Планировщик задач с учетом времени и условий"""
    
    def __init__(self, task_manager: AsyncTaskManager):
        self.task_manager = task_manager
        self.scheduled_tasks = {}
    
    def schedule_at(
        self,
        task_name: str,
        execute_at: datetime,
        args: tuple = (),
        kwargs: dict = None,
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> str:
        """
        Запланировать задачу на определенное время
        
        Args:
            task_name: имя задачи
            execute_at: время выполнения
            args: аргументы
            kwargs: именованные аргументы
            priority: приоритет
            
        Returns:
            task_id
        """
        task_id = self.task_manager.submit_task(
            task_name,
            args=args,
            kwargs=kwargs,
            eta=execute_at,
            priority=priority
        )
        
        self.scheduled_tasks[task_id] = {
            'task_name': task_name,
            'execute_at': execute_at,
            'scheduled_at': datetime.utcnow()
        }
        
        logger.info(f"Task {task_name} scheduled for {execute_at}")
        return task_id
    
    def schedule_in(
        self,
        task_name: str,
        delay_seconds: int,
        args: tuple = (),
        kwargs: dict = None,
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> str:
        """
        Запланировать задачу через N секунд
        
        Args:
            task_name: имя задачи
            delay_seconds: задержка в секундах
            args: аргументы
            kwargs: именованные аргументы
            priority: приоритет
            
        Returns:
            task_id
        """
        execute_at = datetime.utcnow() + timedelta(seconds=delay_seconds)
        return self.schedule_at(task_name, execute_at, args, kwargs, priority)
    
    def schedule_recurring(
        self,
        task_name: str,
        interval_seconds: int,
        max_executions: Optional[int] = None,
        args: tuple = (),
        kwargs: dict = None
    ) -> List[str]:
        """
        Запланировать повторяющуюся задачу
        
        Args:
            task_name: имя задачи
            interval_seconds: интервал в секундах
            max_executions: максимальное количество выполнений
            args: аргументы
            kwargs: именованные аргументы
            
        Returns:
            список task_id
        """
        task_ids = []
        executions = max_executions or 10
        
        for i in range(executions):
            delay = interval_seconds * (i + 1)
            task_id = self.schedule_in(task_name, delay, args, kwargs)
            task_ids.append(task_id)
        
        logger.info(f"Scheduled {len(task_ids)} recurring tasks for {task_name}")
        return task_ids
    
    def cancel_scheduled(self, task_id: str) -> bool:
        """Отменить запланированную задачу"""
        if task_id in self.scheduled_tasks:
            del self.scheduled_tasks[task_id]
        
        return self.task_manager.cancel_task(task_id)
    
    def get_scheduled_tasks(self) -> Dict[str, Any]:
        """Получить список запланированных задач"""
        return self.scheduled_tasks.copy()
