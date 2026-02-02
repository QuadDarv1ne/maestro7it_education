"""
Performance monitoring and health check endpoints
"""
from flask import Blueprint, jsonify, current_app
from flask_login import login_required, current_user
from app import db, cache
from app.performance import get_cache_stats, performance_monitor
from sqlalchemy import text
import psutil
import time

monitoring = Blueprint('monitoring', __name__)

@monitoring.route('/health')
def health_check():
    """Basic health check endpoint"""
    try:
        # Check database connection
        db.session.execute(text('SELECT 1'))
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    # Check cache
    try:
        cache_status = 'healthy' if cache else 'unhealthy'
    except Exception as e:
        cache_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' and cache_status == 'healthy' else 'unhealthy',
        'database': db_status,
        'cache': cache_status,
        'timestamp': time.time()
    })

@monitoring.route('/metrics')
@login_required
def get_metrics():
    """Get application performance metrics"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        # Get cache statistics
        cache_stats = get_cache_stats()
        
        # Get performance monitor stats
        perf_stats = performance_monitor.get_stats()
        
        # Get system metrics
        system_stats = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent if hasattr(psutil, 'disk_usage') else None
        }
        
        # Get database stats
        try:
            # Count records in key tables
            user_count = db.session.query(db.func.count('user.id')).scalar()
            test_count = db.session.query(db.func.count('test_result.id')).scalar()
            db_stats = {
                'users': user_count,
                'test_results': test_count
            }
        except Exception as e:
            db_stats = {'error': str(e)}
        
        return jsonify({
            'cache': cache_stats,
            'performance': perf_stats,
            'system': system_stats,
            'database': db_stats,
            'timestamp': time.time()
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to collect metrics: {str(e)}'}), 500

@monitoring.route('/cache/clear')
@login_required
def clear_cache():
    """Clear application cache (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        cache.clear()
        return jsonify({'success': True, 'message': 'Cache cleared successfully'})
    except Exception as e:
        return jsonify({'error': f'Failed to clear cache: {str(e)}'}), 500

@monitoring.route('/cache/stats')
@login_required
def cache_stats():
    """Get detailed cache statistics"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(get_cache_stats())

@monitoring.route('/performance/queries')
@login_required
def slow_queries():
    """Get slow query information (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        slow_queries = list(performance_monitor.slow_queries)
        query_stats = dict(performance_monitor.query_stats)
        
        return jsonify({
            'slow_queries': slow_queries,
            'query_counts': query_stats,
            'total_slow_queries': len(slow_queries)
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get query stats: {str(e)}'}), 500

@monitoring.route('/memory')
@login_required
def memory_info():
    """Get memory usage information (admin only)"""
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return jsonify({
            'rss': memory_info.rss,  # Resident Set Size
            'vms': memory_info.vms,  # Virtual Memory Size
            'percent': process.memory_percent(),
            'system_memory': {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available,
                'percent': psutil.virtual_memory().percent
            }
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get memory info: {str(e)}'}), 500

# Add the blueprint to the app in __init__.py
# app.register_blueprint(monitoring, url_prefix='/api/monitoring')