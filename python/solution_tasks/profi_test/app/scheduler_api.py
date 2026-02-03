# -*- coding: utf-8 -*-
"""
API конечные точки планировщика задач для ПрофиТест
Предоставляет доступ к функциям планирования и управления фоновыми задачами
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.task_scheduler import task_scheduler, TaskPriority, TaskStatus
from datetime import datetime, timedelta
import json

scheduler_api = Blueprint('scheduler_api', __name__)


@scheduler_api.route('/start', methods=['POST'])
@login_required
def start_scheduler():
    """
    Запускает планировщик задач.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        task_scheduler.start()
        return jsonify({
            'success': True,
            'message': 'Планировщик задач запущен'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/stop', methods=['POST'])
@login_required
def stop_scheduler():
    """
    Останавливает планировщик задач.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        task_scheduler.stop()
        return jsonify({
            'success': True,
            'message': 'Планировщик задач остановлен'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/schedule', methods=['POST'])
@login_required
def schedule_task():
    """
    Планирует выполнение новой задачи.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        if not data or not data.get('function_name'):
            return jsonify({
                'success': False,
                'message': 'Необходимо указать имя функции'
            }), 400
        
        # Получаем параметры задачи
        function_name = data['function_name']
        name = data.get('name', function_name)
        args = tuple(data.get('args', []))
        kwargs = data.get('kwargs', {})
        priority = TaskPriority(data.get('priority', 2))  # NORMAL по умолчанию
        max_retries = data.get('max_retries', 3)
        
        # Обработка времени выполнения
        delay_seconds = data.get('delay_seconds')
        run_at_iso = data.get('run_at')
        
        if delay_seconds:
            delay = timedelta(seconds=delay_seconds)
            run_at = None
        elif run_at_iso:
            run_at = datetime.fromisoformat(run_at_iso.replace('Z', '+00:00'))
            delay = None
        else:
            delay = None
            run_at = None
        
        # Проверяем существование функции (заглушка)
        # В реальной реализации нужно проверять доступные функции
        if function_name not in ['test_function', 'cleanup_function', 'report_function']:
            return jsonify({
                'success': False,
                'message': f'Функция {function_name} не найдена'
            }), 404
        
        # Создаем тестовую функцию
        def test_function():
            import time
            time.sleep(2)  # Имитация работы
            return f"Функция {function_name} выполнена успешно"
        
        # Планируем задачу
        task_id = task_scheduler.schedule_task(
            func=test_function,
            name=name,
            args=args,
            kwargs=kwargs,
            priority=priority,
            delay=delay,
            run_at=run_at,
            max_retries=max_retries
        )
        
        return jsonify({
            'success': True,
            'message': 'Задача запланирована',
            'task_id': task_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/schedule/recurring', methods=['POST'])
@login_required
def schedule_recurring_task():
    """
    Планирует повторяющуюся задачу.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        data = request.get_json()
        
        if not data or not data.get('function_name') or not data.get('interval_seconds'):
            return jsonify({
                'success': False,
                'message': 'Необходимо указать имя функции и интервал'
            }), 400
        
        # Получаем параметры
        function_name = data['function_name']
        interval_seconds = data['interval_seconds']
        name = data.get('name', f"{function_name}_recurring")
        args = tuple(data.get('args', []))
        kwargs = data.get('kwargs', {})
        priority = TaskPriority(data.get('priority', 2))
        max_retries = data.get('max_retries', 3)
        start_delay_seconds = data.get('start_delay_seconds')
        
        # Создаем интервал
        interval = timedelta(seconds=interval_seconds)
        start_delay = timedelta(seconds=start_delay_seconds) if start_delay_seconds else None
        
        # Создаем тестовую функцию
        def recurring_function():
            import time
            time.sleep(1)  # Имитация работы
            return f"Повторяющаяся функция {function_name} выполнена"
        
        # Планируем повторяющуюся задачу
        task_id = task_scheduler.schedule_recurring_task(
            func=recurring_function,
            interval=interval,
            name=name,
            args=args,
            kwargs=kwargs,
            priority=priority,
            max_retries=max_retries,
            start_delay=start_delay
        )
        
        return jsonify({
            'success': True,
            'message': 'Повторяющаяся задача запланирована',
            'task_id': task_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/tasks', methods=['GET'])
@login_required
def get_all_tasks():
    """
    Получает список всех задач.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        status_filter = request.args.get('status')
        if status_filter:
            try:
                status = TaskStatus(status_filter)
                tasks = task_scheduler.get_all_tasks(status=status)
            except ValueError:
                return jsonify({
                    'success': False,
                    'message': 'Некорректный статус задачи'
                }), 400
        else:
            tasks = task_scheduler.get_all_tasks()
        
        return jsonify({
            'success': True,
            'tasks': tasks,
            'total_count': len(tasks)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/tasks/<task_id>', methods=['GET'])
@login_required
def get_task_status(task_id):
    """
    Получает статус конкретной задачи.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        task_status = task_scheduler.get_task_status(task_id)
        
        if task_status:
            return jsonify({
                'success': True,
                'task': task_status
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Задача не найдена'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/tasks/<task_id>/cancel', methods=['POST'])
@login_required
def cancel_task(task_id):
    """
    Отменяет задачу.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        success = task_scheduler.cancel_task(task_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Задача отменена'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Не удалось отменить задачу'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/stats', methods=['GET'])
@login_required
def get_scheduler_stats():
    """
    Получает статистику планировщика.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        stats = task_scheduler.get_scheduler_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/history/clear', methods=['POST'])
@login_required
def clear_history():
    """
    Очищает историю задач.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        task_scheduler.clear_history()
        return jsonify({
            'success': True,
            'message': 'История задач очищена'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/test-functions', methods=['GET'])
@login_required
def get_test_functions():
    """
    Получает список доступных тестовых функций.
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Требуется доступ администратора'
            }), 403
        
        test_functions = [
            {
                'name': 'test_function',
                'description': 'Тестовая функция для проверки планировщика',
                'parameters': ['param1', 'param2']
            },
            {
                'name': 'cleanup_function',
                'description': 'Функция очистки устаревших данных',
                'parameters': []
            },
            {
                'name': 'report_function',
                'description': 'Функция генерации отчетов',
                'parameters': ['report_type', 'date_range']
            }
        ]
        
        return jsonify({
            'success': True,
            'functions': test_functions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@scheduler_api.route('/available-priorities', methods=['GET'])
@login_required
def get_available_priorities():
    """
    Получает список доступных приоритетов задач.
    """
    try:
        priorities = [
            {'name': priority.name, 'value': priority.value, 'description': self._get_priority_description(priority)}
            for priority in TaskPriority
        ]
        
        return jsonify({
            'success': True,
            'priorities': priorities
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    def _get_priority_description(self, priority):
        """Получает описание приоритета."""
        descriptions = {
            TaskPriority.LOW: 'Низкий приоритет - выполняется при низкой нагрузке',
            TaskPriority.NORMAL: 'Нормальный приоритет - стандартный уровень выполнения',
            TaskPriority.HIGH: 'Высокий приоритет - выполняется в первую очередь',
            TaskPriority.CRITICAL: 'Критический приоритет - максимальный приоритет выполнения'
        }
        return descriptions.get(priority, 'Неизвестный приоритет')