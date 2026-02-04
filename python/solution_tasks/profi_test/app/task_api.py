# -*- coding: utf-8 -*-
"""
API endpoints for task management system
Provides access to background task functionality
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.tasks import task_manager, TaskStatus
import json
from datetime import datetime

task_api = Blueprint('task_api', __name__)

@task_api.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    """
    Get list of all tasks with filtering and pagination
    """
    try:
        # Get query parameters
        status_filter = request.args.get('status')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Get all tasks
        all_tasks = task_manager.get_all_tasks()
        
        # Apply status filter if provided
        if status_filter:
            all_tasks = [task for task in all_tasks if task['status'] == status_filter]
        
        # Pagination
        total_tasks = len(all_tasks)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_tasks = all_tasks[start_idx:end_idx]
        
        return jsonify({
            'success': True,
            'tasks': paginated_tasks,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_tasks,
                'pages': (total_tasks + per_page - 1) // per_page
            },
            'stats': task_manager.get_stats()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_api.route('/tasks/<task_id>', methods=['GET'])
@login_required
def get_task(task_id):
    """
    Get information about a specific task
    """
    try:
        task = task_manager.get_task_status(task_id)
        if not task:
            return jsonify({
                'success': False,
                'message': 'Task not found'
            }), 404
        
        return jsonify({
            'success': True,
            'task': task
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_api.route('/tasks', methods=['POST'])
@login_required
def create_task():
    """
    Create a new background task
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'name' not in data or 'function' not in data:
            return jsonify({
                'success': False,
                'message': 'Name and function are required'
            }), 400
        
        # For security, we'll only allow predefined functions
        allowed_functions = {
            'test_task': lambda: "Test task completed successfully",
            'data_processing': lambda: "Data processing completed",
            'report_generation': lambda: "Report generated successfully"
        }
        
        if data['function'] not in allowed_functions:
            return jsonify({
                'success': False,
                'message': 'Function not allowed'
            }), 400
        
        # Create task
        task_id = task_manager.create_task(
            name=data['name'],
            func=allowed_functions[data['function']],
            priority=data.get('priority', 0)
        )
        
        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'task_id': task_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_api.route('/tasks/<task_id>/cancel', methods=['POST'])
@login_required
def cancel_task(task_id):
    """
    Cancel a running task
    """
    try:
        result = task_manager.cancel_task(task_id)
        if result:
            return jsonify({
                'success': True,
                'message': 'Task cancelled successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Task not found or cannot be cancelled'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_api.route('/tasks/stats', methods=['GET'])
@login_required
def get_task_stats():
    """
    Get task statistics
    """
    try:
        stats = task_manager.get_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@task_api.route('/tasks/cleanup', methods=['POST'])
@login_required
def cleanup_tasks():
    """
    Clean up completed tasks
    """
    try:
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        older_than = int(request.args.get('older_than_hours', 24))
        task_manager.cleanup_completed_tasks(older_than)
        
        return jsonify({
            'success': True,
            'message': 'Completed tasks cleaned up successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500