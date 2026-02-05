# -*- coding: utf-8 -*-
"""
Performance Dashboard Module
Provides real-time monitoring and visualization of application performance metrics
"""
import time
import psutil
import logging
from datetime import datetime, timedelta
from collections import defaultdict, deque
from threading import Thread, Lock
from flask import Blueprint, render_template, jsonify
import json

logger = logging.getLogger(__name__)

class PerformanceMetrics:
    """Collects and stores performance metrics"""
    
    def __init__(self, max_history=1000):
        self.max_history = max_history
        self.metrics = defaultdict(lambda: deque(maxlen=max_history))
        self.lock = Lock()
        
        # System metrics collectors
        self.system_metrics = {
            'cpu_percent': [],
            'memory_percent': [],
            'disk_io': [],
            'network_io': []
        }
    
    def record_metric(self, metric_name, value, tags=None):
        """Record a performance metric"""
        with self.lock:
            timestamp = datetime.now()
            metric_data = {
                'timestamp': timestamp.isoformat(),
                'value': value,
                'tags': tags or {}
            }
            self.metrics[metric_name].append(metric_data)
            
            # Keep only recent metrics
            if len(self.metrics[metric_name]) > self.max_history:
                self.metrics[metric_name].popleft()
    
    def get_metrics(self, metric_name, hours=1):
        """Get metrics for a specific name within time range"""
        with self.lock:
            if metric_name not in self.metrics:
                return []
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_metrics = [
                metric for metric in self.metrics[metric_name]
                if datetime.fromisoformat(metric['timestamp']) > cutoff_time
            ]
            return recent_metrics
    
    def get_system_metrics(self):
        """Get current system metrics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'network_io': {
                    'bytes_sent': psutil.net_io_counters().bytes_sent,
                    'bytes_recv': psutil.net_io_counters().bytes_recv
                }
            }
        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {}
    
    def get_aggregated_metrics(self, metric_name, hours=1):
        """Get aggregated statistics for a metric"""
        metrics = self.get_metrics(metric_name, hours)
        if not metrics:
            return {}
        
        values = [m['value'] for m in metrics]
        return {
            'count': len(values),
            'avg': sum(values) / len(values),
            'min': min(values),
            'max': max(values),
            'latest': values[-1] if values else None
        }

class PerformanceDashboard:
    """Main performance dashboard class"""
    
    def __init__(self):
        self.metrics_collector = PerformanceMetrics()
        self.is_monitoring = False
        self.monitoring_thread = None
        
    def start_monitoring(self, interval=5):
        """Start background monitoring"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.monitoring_thread = Thread(target=self._monitoring_loop, args=(interval,), daemon=True)
        self.monitoring_thread.start()
        logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Performance monitoring stopped")
    
    def _monitoring_loop(self, interval):
        """Background monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect system metrics
                system_metrics = self.metrics_collector.get_system_metrics()
                
                if system_metrics:
                    self.metrics_collector.record_metric('system.cpu_percent', system_metrics['cpu_percent'])
                    self.metrics_collector.record_metric('system.memory_percent', system_metrics['memory_percent'])
                    self.metrics_collector.record_metric('system.disk_usage', system_metrics['disk_usage'])
                
                # Collect application-specific metrics would go here
                # self.metrics_collector.record_metric('app.response_time', response_time)
                # self.metrics_collector.record_metric('app.requests_per_second', rps)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
            
            time.sleep(interval)
    
    def get_dashboard_data(self):
        """Get data for dashboard display"""
        return {
            'system_metrics': self.metrics_collector.get_system_metrics(),
            'recent_metrics': {
                'cpu': self.metrics_collector.get_metrics('system.cpu_percent', 1),
                'memory': self.metrics_collector.get_metrics('system.memory_percent', 1),
                'disk': self.metrics_collector.get_metrics('system.disk_usage', 1)
            },
            'aggregated_metrics': {
                'cpu': self.metrics_collector.get_aggregated_metrics('system.cpu_percent', 1),
                'memory': self.metrics_collector.get_aggregated_metrics('system.memory_percent', 1),
                'disk': self.metrics_collector.get_aggregated_metrics('system.disk_usage', 1)
            }
        }

# Global dashboard instance
performance_dashboard = PerformanceDashboard()

# Flask blueprint for dashboard endpoints
dashboard_bp = Blueprint('performance_dashboard', __name__)

@dashboard_bp.route('/dashboard/performance')
def performance_dashboard_page():
    """Render the performance dashboard page"""
    return render_template('performance/dashboard.html')

@dashboard_bp.route('/api/performance/metrics')
def get_performance_metrics():
    """API endpoint for performance metrics"""
    try:
        data = performance_dashboard.get_dashboard_data()
        return jsonify({
            'success': True,
            'data': data
        })
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@dashboard_bp.route('/api/performance/start_monitoring')
def start_monitoring():
    """Start performance monitoring"""
    try:
        performance_dashboard.start_monitoring()
        return jsonify({'success': True, 'message': 'Monitoring started'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@dashboard_bp.route('/api/performance/stop_monitoring')
def stop_monitoring():
    """Stop performance monitoring"""
    try:
        performance_dashboard.stop_monitoring()
        return jsonify({'success': True, 'message': 'Monitoring stopped'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Performance decorator for monitoring function execution
def monitor_performance(metric_name):
    """Decorator to monitor function performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                performance_dashboard.metrics_collector.record_metric(
                    f'function.{metric_name}.execution_time', 
                    execution_time
                )
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                performance_dashboard.metrics_collector.record_metric(
                    f'function.{metric_name}.execution_time', 
                    execution_time
                )
                performance_dashboard.metrics_collector.record_metric(
                    f'function.{metric_name}.errors', 
                    1
                )
                raise
        return wrapper
    return decorator

# Context manager for performance monitoring
class PerformanceTimer:
    """Context manager for timing code blocks"""
    
    def __init__(self, metric_name):
        self.metric_name = metric_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        execution_time = time.time() - self.start_time
        performance_dashboard.metrics_collector.record_metric(
            f'block.{self.metric_name}.execution_time',
            execution_time
        )
        
        if exc_type is not None:
            performance_dashboard.metrics_collector.record_metric(
                f'block.{self.metric_name}.errors',
                1
            )

# Initialize monitoring when module is imported
def init_performance_monitoring(app):
    """Initialize performance monitoring for the application"""
    # Register blueprint
    app.register_blueprint(dashboard_bp, url_prefix='/admin')
    
    # Start monitoring
    performance_dashboard.start_monitoring()
    
    logger.info("Performance monitoring initialized")
