# -*- coding: utf-8 -*-
"""
Модуль управления фоновыми задачами для ProfiTest
"""

import uuid
import time
import threading
from enum import Enum
from datetime import datetime
from collections import defaultdict

class TaskStatus(Enum):
    """Статусы выполнения задач"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskManager:
    """Менеджер фоновых задач"""
    
    def __init__(self):
        self.tasks = {}
        self.task_lock = threading.Lock()
        self.running = True
        self.stats = {
            'total_tasks': 0,
            'pending': 0,
            'running': 0,
            'completed': 0,
            'failed': 0,
            'cancelled': 0
        }
    
    def create_task(self, name, func, priority=0, args=None, kwargs=None):
        """
        Создает новую фоновую задачу
        
        Args:
            name: Название задачи
            func: Функция для выполнения
            priority: Приоритет задачи (0 - самый высокий)
            args: Позиционные аргументы функции
            kwargs: Именованные аргументы функции
            
        Returns:
            str: ID созданной задачи
        """
        task_id = str(uuid.uuid4())
        args = args or ()
        kwargs = kwargs or {}
        
        task = {
            'id': task_id,
            'name': name,
            'func': func,
            'args': args,
            'kwargs': kwargs,
            'priority': priority,
            'status': TaskStatus.PENDING.value,
            'created_at': datetime.now(),
            'started_at': None,
            'completed_at': None,
            'result': None,
            'error': None,
            'thread': None
        }
        
        with self.task_lock:
            self.tasks[task_id] = task
            self.stats['total_tasks'] += 1
            self.stats['pending'] += 1
        
        # Запускаем задачу в отдельном потоке
        thread = threading.Thread(target=self._execute_task, args=(task_id,), daemon=True)
        task['thread'] = thread
        thread.start()
        
        return task_id
    
    def _execute_task(self, task_id):
        """Выполняет задачу в отдельном потоке"""
        with self.task_lock:
            if task_id not in self.tasks:
                return
            
            task = self.tasks[task_id]
            task['status'] = TaskStatus.RUNNING.value
            task['started_at'] = datetime.now()
            self.stats['pending'] -= 1
            self.stats['running'] += 1
        
        try:
            result = task['func'](*task['args'], **task['kwargs'])
            
            with self.task_lock:
                task['status'] = TaskStatus.COMPLETED.value
                task['result'] = result
                task['completed_at'] = datetime.now()
                self.stats['running'] -= 1
                self.stats['completed'] += 1
                
        except Exception as e:
            with self.task_lock:
                task['status'] = TaskStatus.FAILED.value
                task['error'] = str(e)
                task['completed_at'] = datetime.now()
                self.stats['running'] -= 1
                self.stats['failed'] += 1
    
    def get_task_status(self, task_id):
        """
        Получает статус задачи
        
        Args:
            task_id: ID задачи
            
        Returns:
            dict: Информация о задаче или None если задача не найдена
        """
        with self.task_lock:
            if task_id not in self.tasks:
                return None
            
            task = self.tasks[task_id].copy()
            # Удаляем поток из результата чтобы избежать сериализации
            task.pop('thread', None)
            # Преобразуем datetime в строки для сериализации
            for key in ['created_at', 'started_at', 'completed_at']:
                if task.get(key):
                    task[key] = task[key].isoformat()
            return task
    
    def cancel_task(self, task_id):
        """
        Отменяет выполнение задачи
        
        Args:
            task_id: ID задачи
            
        Returns:
            bool: True если задача была отменена, False если не найдена
        """
        with self.task_lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            if task['status'] in [TaskStatus.PENDING.value, TaskStatus.RUNNING.value]:
                task['status'] = TaskStatus.CANCELLED.value
                task['completed_at'] = datetime.now()
                
                # Обновляем статистику
                if task['status'] == TaskStatus.PENDING.value:
                    self.stats['pending'] -= 1
                elif task['status'] == TaskStatus.RUNNING.value:
                    self.stats['running'] -= 1
                self.stats['cancelled'] += 1
                
                return True
            return False
    
    def get_stats(self):
        """
        Получает статистику по задачам
        
        Returns:
            dict: Статистика задач
        """
        with self.task_lock:
            return self.stats.copy()
    
    def get_all_tasks(self):
        """
        Получает список всех задач
        
        Returns:
            list: Список задач с их статусами
        """
        with self.task_lock:
            tasks_list = []
            for task in self.tasks.values():
                task_copy = task.copy()
                task_copy.pop('thread', None)
                task_copy.pop('func', None)  # Удаляем функцию для безопасности
                # Преобразуем datetime в строки
                for key in ['created_at', 'started_at', 'completed_at']:
                    if task_copy.get(key):
                        task_copy[key] = task_copy[key].isoformat()
                tasks_list.append(task_copy)
            return tasks_list
    
    def cleanup_completed_tasks(self, older_than_hours=24):
        """
        Очищает завершенные задачи старше заданного времени
        
        Args:
            older_than_hours: Сколько часов назад задача должна быть завершена
        """
        cutoff_time = datetime.now().timestamp() - (older_than_hours * 3600)
        
        with self.task_lock:
            to_remove = []
            for task_id, task in self.tasks.items():
                if task['status'] in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value, TaskStatus.CANCELLED.value]:
                    if task['completed_at'] and task['completed_at'].timestamp() < cutoff_time:
                        to_remove.append(task_id)
            
            for task_id in to_remove:
                del self.tasks[task_id]

# Глобальный экземпляр менеджера задач
task_manager = TaskManager()

# Экспортируем классы и экземпляры
__all__ = ['TaskManager', 'TaskStatus', 'task_manager']