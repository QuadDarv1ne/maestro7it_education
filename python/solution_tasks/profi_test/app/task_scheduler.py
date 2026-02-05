# -*- coding: utf-8 -*-
"""
Модуль расширенного планировщика задач для ПрофиТест
Предоставляет продвинутые возможности планирования и выполнения фоновых задач
"""
import threading
import time
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable, Dict, List, Optional, Any
import logging
import json
from dataclasses import dataclass, asdict
from queue import Queue, PriorityQueue
import atexit


class TaskStatus(Enum):
    """Статусы выполнения задач"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Приоритеты задач"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """Класс задачи"""
    id: str
    name: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: TaskPriority
    scheduled_time: datetime
    status: TaskStatus
    created_at: datetime
    max_retries: int = 3
    retry_count: int = 0
    result: Any = None
    error: str = None
    execution_time: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует задачу в словарь"""
        task_dict = asdict(self)
        task_dict['priority'] = self.priority.value
        task_dict['status'] = self.status.value
        task_dict['scheduled_time'] = self.scheduled_time.isoformat()
        task_dict['created_at'] = self.created_at.isoformat()
        return task_dict


class TaskScheduler:
    """
    Расширенный планировщик задач для системы ПрофиТест.
    Обеспечивает управление фоновыми задачами с приоритетами и повторными попытками.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.tasks: Dict[str, Task] = {}
        self.task_queue = PriorityQueue()
        self.running = False
        self.worker_thread = None
        self.lock = threading.Lock()
        self.task_history: List[Task] = []
        self.max_history_size = 1000
        
        # Регистрация функции остановки при завершении программы
        atexit.register(self.shutdown)
    
    def start(self):
        """Запускает планировщик задач"""
        if self.running:
            self.logger.warning("Планировщик уже запущен")
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        self.logger.info("Планировщик задач запущен")
    
    def stop(self):
        """Останавливает планировщик задач"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        try:
            self.logger.info("Планировщик задач остановлен")
        except (ValueError, AttributeError):
            pass  # Ignore logging errors during shutdown
    
    def shutdown(self):
        """Корректно завершает работу планировщика"""
        try:
            self.logger.info("Завершение работы планировщика задач...")
        except (ValueError, AttributeError):
            pass  # Ignore logging errors during shutdown
        self.stop()
        self._save_task_history()
    
    def schedule_task(self, func: Callable, 
                     name: str = None,
                     args: tuple = (),
                     kwargs: dict = None,
                     priority: TaskPriority = TaskPriority.NORMAL,
                     delay: timedelta = None,
                     run_at: datetime = None,
                     max_retries: int = 3) -> str:
        """
        Планирует выполнение задачи.
        
        Args:
            func: Функция для выполнения
            name: Название задачи
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            priority: Приоритет задачи
            delay: Задержка перед выполнением
            run_at: Конкретное время выполнения
            max_retries: Максимальное количество повторных попыток
            
        Returns:
            str: ID задачи
        """
        if kwargs is None:
            kwargs = {}
        
        task_id = str(uuid.uuid4())
        task_name = name or func.__name__
        
        # Определение времени выполнения
        if run_at:
            scheduled_time = run_at
        elif delay:
            scheduled_time = datetime.utcnow() + delay
        else:
            scheduled_time = datetime.utcnow()
        
        task = Task(
            id=task_id,
            name=task_name,
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            scheduled_time=scheduled_time,
            status=TaskStatus.PENDING,
            created_at=datetime.utcnow(),
            max_retries=max_retries
        )
        
        with self.lock:
            self.tasks[task_id] = task
            # Добавляем в очередь с приоритетом (отрицательный приоритет для PriorityQueue)
            self.task_queue.put((-priority.value, scheduled_time, task_id))
        
        self.logger.info(f"Задача '{task_name}' запланирована (ID: {task_id})")
        return task_id
    
    def schedule_recurring_task(self, func: Callable,
                              interval: timedelta,
                              name: str = None,
                              args: tuple = (),
                              kwargs: dict = None,
                              priority: TaskPriority = TaskPriority.NORMAL,
                              max_retries: int = 3,
                              start_delay: timedelta = None) -> str:
        """
        Планирует повторяющуюся задачу.
        
        Args:
            func: Функция для выполнения
            interval: Интервал между выполнениями
            name: Название задачи
            args: Позиционные аргументы
            kwargs: Именованные аргументы
            priority: Приоритет задачи
            max_retries: Максимальное количество повторных попыток
            start_delay: Задержка перед первым выполнением
            
        Returns:
            str: ID задачи
        """
        def recurring_wrapper():
            try:
                # Выполняем оригинальную функцию
                result = func(*args, **kwargs)
                
                # Планируем следующее выполнение
                next_run = datetime.utcnow() + interval
                self.schedule_task(
                    recurring_wrapper,
                    name=f"{name or func.__name__}_recurring",
                    priority=priority,
                    run_at=next_run,
                    max_retries=max_retries
                )
                
                return result
            except Exception as e:
                self.logger.error(f"Ошибка в повторяющейся задаче: {str(e)}")
                raise
        
        # Планируем первое выполнение
        initial_delay = start_delay or timedelta(seconds=0)
        return self.schedule_task(
            recurring_wrapper,
            name=name or f"{func.__name__}_recurring",
            priority=priority,
            delay=initial_delay,
            max_retries=max_retries
        )
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Отменяет задачу.
        
        Args:
            task_id: ID задачи
            
        Returns:
            bool: Успешность отмены
        """
        with self.lock:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                if task.status == TaskStatus.PENDING:
                    task.status = TaskStatus.CANCELLED
                    self.logger.info(f"Задача '{task.name}' отменена")
                    return True
                else:
                    self.logger.warning(f"Невозможно отменить задачу '{task.name}' в статусе {task.status.value}")
                    return False
            else:
                self.logger.warning(f"Задача с ID {task_id} не найдена")
                return False
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает статус задачи.
        
        Args:
            task_id: ID задачи
            
        Returns:
            dict: Информация о статусе задачи или None
        """
        with self.lock:
            task = self.tasks.get(task_id)
            if task:
                return task.to_dict()
            return None
    
    def get_all_tasks(self, status: TaskStatus = None) -> List[Dict[str, Any]]:
        """
        Получает все задачи с опциональной фильтрацией по статусу.
        
        Args:
            status: Фильтр по статусу
            
        Returns:
            list: Список задач
        """
        with self.lock:
            tasks = list(self.tasks.values())
            if status:
                tasks = [task for task in tasks if task.status == status]
            return [task.to_dict() for task in tasks]
    
    def get_scheduler_stats(self) -> Dict[str, Any]:
        """
        Получает статистику планировщика.
        
        Returns:
            dict: Статистика планировщика
        """
        with self.lock:
            status_counts = {}
            for task in self.tasks.values():
                status_counts[task.status.value] = status_counts.get(task.status.value, 0) + 1
            
            return {
                'total_tasks': len(self.tasks),
                'queue_size': self.task_queue.qsize(),
                'running': self.running,
                'status_distribution': status_counts,
                'history_size': len(self.task_history)
            }
    
    def _worker(self):
        """Основной рабочий поток планировщика"""
        while self.running:
            try:
                # Получаем задачу из очереди (таймаут 1 секунда для возможности остановки)
                try:
                    priority, scheduled_time, task_id = self.task_queue.get(timeout=1.0)
                except:
                    continue
                
                with self.lock:
                    task = self.tasks.get(task_id)
                    if not task or task.status != TaskStatus.PENDING:
                        self.task_queue.task_done()
                        continue
                
                # Проверяем, пришло ли время выполнения
                if datetime.utcnow() < task.scheduled_time:
                    # Возвращаем задачу в очередь
                    self.task_queue.put((priority, scheduled_time, task_id))
                    self.task_queue.task_done()
                    time.sleep(0.1)  # Небольшая задержка чтобы не перегружать CPU
                    continue
                
                # Выполняем задачу
                self._execute_task(task)
                self.task_queue.task_done()
                
            except Exception as e:
                self.logger.error(f"Ошибка в рабочем потоке: {str(e)}")
                time.sleep(1)  # Задержка при ошибке
    
    def _execute_task(self, task: Task):
        """
        Выполняет задачу.
        
        Args:
            task: Задача для выполнения
        """
        task.status = TaskStatus.RUNNING
        start_time = time.time()
        
        try:
            self.logger.info(f"Начало выполнения задачи '{task.name}' (ID: {task.id})")
            
            # Выполняем функцию задачи
            result = task.func(*task.args, **task.kwargs)
            
            # Обновляем статус
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.execution_time = time.time() - start_time
            
            self.logger.info(f"Задача '{task.name}' успешно выполнена за {task.execution_time:.2f} секунд")
            
        except Exception as e:
            task.error = str(e)
            task.retry_count += 1
            
            self.logger.error(f"Ошибка в задаче '{task.name}': {str(e)}")
            
            # Проверяем возможность повторной попытки
            if task.retry_count < task.max_retries:
                task.status = TaskStatus.PENDING
                # Планируем повторную попытку с экспоненциальной задержкой
                retry_delay = timedelta(seconds=2 ** task.retry_count)
                task.scheduled_time = datetime.utcnow() + retry_delay
                self.task_queue.put((-task.priority.value, task.scheduled_time, task.id))
                self.logger.info(f"Планируется повторная попытка для задачи '{task.name}' (попытка {task.retry_count})")
            else:
                task.status = TaskStatus.FAILED
                self.logger.error(f"Задача '{task.name}' окончательно провалилась после {task.max_retries} попыток")
        
        finally:
            # Добавляем в историю
            self._add_to_history(task)
    
    def _add_to_history(self, task: Task):
        """
        Добавляет задачу в историю.
        
        Args:
            task: Задача для добавления в историю
        """
        self.task_history.append(task)
        # Ограничиваем размер истории
        if len(self.task_history) > self.max_history_size:
            self.task_history = self.task_history[-self.max_history_size:]
    
    def _save_task_history(self):
        """Сохраняет историю задач в файл"""
        try:
            history_data = [task.to_dict() for task in self.task_history]
            # В реальной реализации здесь будет сохранение в файл или базу данных
            self.logger.debug(f"История задач сохранена ({len(history_data)} записей)")
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении истории задач: {str(e)}")
    
    def clear_history(self):
        """Очищает историю задач"""
        with self.lock:
            self.task_history.clear()
        self.logger.info("История задач очищена")


# Глобальный экземпляр планировщика
task_scheduler = TaskScheduler()

# Add task_manager alias for compatibility with task_api.py
task_manager = task_scheduler
