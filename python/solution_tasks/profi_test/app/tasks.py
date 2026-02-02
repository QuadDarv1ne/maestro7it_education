"""
Background task processing system
"""
import threading
import queue
import time
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """Background task representation"""
    id: str
    name: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: int = 0
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()

class TaskQueue:
    """Priority queue for background tasks"""
    
    def __init__(self, max_workers=4):
        self.tasks = queue.PriorityQueue()
        self.task_dict = {}  # For quick lookup by ID
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.futures = {}  # Track running futures
        self.lock = threading.Lock()
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
        
    def add_task(self, task: Task) -> str:
        """Add a task to the queue"""
        with self.lock:
            # Use negative priority for proper ordering (higher priority first)
            self.tasks.put((-task.priority, task.id, task))
            self.task_dict[task.id] = task
            logging.info(f"Task {task.id} ({task.name}) added to queue with priority {task.priority}")
            return task.id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        with self.lock:
            return self.task_dict.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task if it's still pending"""
        with self.lock:
            task = self.task_dict.get(task_id)
            if task and task.status == TaskStatus.PENDING:
                task.status = TaskStatus.CANCELLED
                task.completed_at = datetime.utcnow()
                logging.info(f"Task {task_id} cancelled")
                return True
            return False
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        with self.lock:
            pending_count = sum(1 for task in self.task_dict.values() 
                              if task.status == TaskStatus.PENDING)
            running_count = sum(1 for task in self.task_dict.values() 
                              if task.status == TaskStatus.RUNNING)
            completed_count = sum(1 for task in self.task_dict.values() 
                                if task.status == TaskStatus.COMPLETED)
            failed_count = sum(1 for task in self.task_dict.values() 
                             if task.status == TaskStatus.FAILED)
            
            return {
                'total_tasks': len(self.task_dict),
                'pending': pending_count,
                'running': running_count,
                'completed': completed_count,
                'failed': failed_count,
                'active_workers': len(self.futures)
            }
    
    def _worker(self):
        """Main worker thread"""
        while self.running:
            try:
                # Get task from queue (blocking)
                priority, task_id, task = self.tasks.get(timeout=1)
                
                # Check if task was cancelled
                with self.lock:
                    if task.status == TaskStatus.CANCELLED:
                        self.tasks.task_done()
                        continue
                
                # Execute task
                self._execute_task(task)
                self.tasks.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Error in task worker: {e}")
                time.sleep(1)
    
    def _execute_task(self, task: Task):
        """Execute a single task"""
        try:
            with self.lock:
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.utcnow()
            
            logging.info(f"Starting task {task.id} ({task.name})")
            
            # Execute the function
            future = self.executor.submit(task.func, *task.args, **task.kwargs)
            self.futures[task.id] = future
            
            # Wait for completion
            result = future.result(timeout=300)  # 5 minute timeout
            
            with self.lock:
                task.status = TaskStatus.COMPLETED
                task.result = result
                task.completed_at = datetime.utcnow()
                del self.futures[task.id]
            
            logging.info(f"Task {task.id} ({task.name}) completed successfully")
            
        except Exception as e:
            with self.lock:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.completed_at = datetime.utcnow()
                if task.id in self.futures:
                    del self.futures[task.id]
            
            logging.error(f"Task {task.id} ({task.name}) failed: {e}")
            
            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                logging.info(f"Retrying task {task.id} (attempt {task.retry_count})")
                self.add_task(task)
    
    def shutdown(self, wait=True):
        """Shutdown the task queue"""
        self.running = False
        self.executor.shutdown(wait=wait)
        if wait:
            self.worker_thread.join()

class BackgroundTaskManager:
    """Main background task manager"""
    
    def __init__(self, max_workers=4):
        self.task_queue = TaskQueue(max_workers=max_workers)
        self.task_counter = 0
        self.lock = threading.Lock()
    
    def create_task(self, name: str, func: Callable, *args, 
                   priority: int = 0, max_retries: int = 3, **kwargs) -> str:
        """Create and queue a background task"""
        with self.lock:
            self.task_counter += 1
            task_id = f"task_{self.task_counter}_{int(time.time())}"
        
        task = Task(
            id=task_id,
            name=name,
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            max_retries=max_retries
        )
        
        return self.task_queue.add_task(task)
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status and details"""
        task = self.task_queue.get_task(task_id)
        if not task:
            return None
        
        duration = None
        if task.started_at:
            end_time = task.completed_at or datetime.utcnow()
            duration = (end_time - task.started_at).total_seconds()
        
        return {
            'id': task.id,
            'name': task.name,
            'status': task.status.value,
            'priority': task.priority,
            'created_at': task.created_at.isoformat(),
            'started_at': task.started_at.isoformat() if task.started_at else None,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None,
            'duration': duration,
            'retry_count': task.retry_count,
            'max_retries': task.max_retries,
            'result': task.result,
            'error': task.error
        }
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        return self.task_queue.cancel_task(task_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return self.task_queue.get_queue_stats()
    
    def get_recent_tasks(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent tasks"""
        with self.task_queue.lock:
            tasks = list(self.task_queue.task_dict.values())
            # Sort by creation time, newest first
            tasks.sort(key=lambda t: t.created_at, reverse=True)
            return [self.get_task_status(task.id) for task in tasks[:limit]]

# Global task manager instance
task_manager = BackgroundTaskManager(max_workers=4)

# Decorator for background tasks
def background_task(name: str = None, priority: int = 0, max_retries: int = 3):
    """
    Decorator to run function as background task
    
    Args:
        name: Task name (defaults to function name)
        priority: Task priority (higher = more important)
        max_retries: Maximum retry attempts
    """
    def decorator(func):
        task_name = name or func.__name__
        
        def wrapper(*args, **kwargs):
            return task_manager.create_task(
                name=task_name,
                func=func,
                priority=priority,
                max_retries=max_retries,
                *args,
                **kwargs
            )
        return wrapper
    return decorator

# Task monitoring API endpoints
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

task_api = Blueprint('tasks', __name__)

@task_api.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    """Create a new background task"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'function' not in data:
            return jsonify({'error': 'Missing required fields: name, function'}), 400
        
        # In a real implementation, you'd have a registry of allowed functions
        # For security, we'll only allow specific predefined tasks
        allowed_tasks = {
            'generate_reports': lambda: "Reports generated",
            'cleanup_old_data': lambda: "Old data cleaned up",
            'update_statistics': lambda: "Statistics updated"
        }
        
        if data['function'] not in allowed_tasks:
            return jsonify({'error': 'Function not allowed'}), 400
        
        task_id = task_manager.create_task(
            name=data['name'],
            func=allowed_tasks[data['function']],
            priority=data.get('priority', 0),
            max_retries=data.get('max_retries', 3)
        )
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'Task created successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@task_api.route('/api/tasks/<task_id>')
@login_required
def get_task(task_id):
    """Get task status"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    task_status = task_manager.get_task_status(task_id)
    if not task_status:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task_status)

@task_api.route('/api/tasks/<task_id>', methods=['DELETE'])
@login_required
def cancel_task(task_id):
    """Cancel a task"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    if task_manager.cancel_task(task_id):
        return jsonify({'success': True, 'message': 'Task cancelled'})
    else:
        return jsonify({'error': 'Task cannot be cancelled'}), 400

@task_api.route('/api/tasks')
@login_required
def list_tasks():
    """List recent tasks"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    limit = request.args.get('limit', 10, type=int)
    tasks = task_manager.get_recent_tasks(limit)
    return jsonify({
        'tasks': tasks,
        'stats': task_manager.get_stats()
    })

# Example background tasks
@background_task(name="Generate User Statistics", priority=1)
def generate_user_statistics():
    """Generate user statistics in background"""
    from app import db
    from app.models import User, TestResult
    
    # Simulate heavy computation
    time.sleep(2)
    
    # Get statistics
    total_users = User.query.count()
    total_tests = TestResult.query.count()
    
    # In real implementation, you'd do more complex analysis
    return {
        'total_users': total_users,
        'total_tests': total_tests,
        'generation_time': datetime.utcnow().isoformat()
    }

@background_task(name="Cleanup Old Sessions", priority=0)
def cleanup_old_sessions():
    """Cleanup old database sessions"""
    # This would contain actual cleanup logic
    time.sleep(1)
    return "Session cleanup completed"

@background_task(name="Send Notification Emails", priority=2)
def send_notification_emails():
    """Send batch notification emails"""
    # Simulate email sending
    time.sleep(3)
    return f"Sent notifications to {100} users"

# Register the blueprint in __init__.py
# app.register_blueprint(task_api, url_prefix='/api')