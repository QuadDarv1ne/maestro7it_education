import time
import logging
import psutil
import os
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict, deque
import threading

class PerformanceMonitor:
    """Performance monitoring utility for tracking API response times and system metrics"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.request_times = deque(maxlen=1000)  # Keep last 1000 requests
        self.endpoint_stats = defaultdict(lambda: {
            'count': 0,
            'total_time': 0,
            'min_time': float('inf'),
            'max_time': 0
        })
        self.lock = threading.Lock()
        
    def record_request(self, endpoint, method, response_time, status_code=200):
        """Record a request's performance metrics"""
        with self.lock:
            self.request_times.append({
                'endpoint': endpoint,
                'method': method,
                'response_time': response_time,
                'status_code': status_code,
                'timestamp': datetime.utcnow()
            })
            
            # Update endpoint statistics
            stats = self.endpoint_stats[f"{method} {endpoint}"]
            stats['count'] += 1
            stats['total_time'] += response_time
            stats['min_time'] = min(stats['min_time'], response_time)
            stats['max_time'] = max(stats['max_time'], response_time)
    
    def get_recent_requests(self, minutes=5):
        """Get recent requests from the last N minutes"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        with self.lock:
            recent = [req for req in self.request_times if req['timestamp'] > cutoff_time]
        return recent
    
    def get_endpoint_stats(self, endpoint=None):
        """Get statistics for a specific endpoint or all endpoints"""
        with self.lock:
            if endpoint:
                return self.endpoint_stats.get(endpoint, {})
            return dict(self.endpoint_stats)
    
    def get_performance_summary(self):
        """Get overall performance summary"""
        with self.lock:
            if not self.request_times:
                return {
                    'avg_response_time': 0,
                    'total_requests': 0,
                    'error_rate': 0,
                    'slow_requests': 0
                }
            
            total_requests = len(self.request_times)
            total_time = sum(req['response_time'] for req in self.request_times)
            avg_response_time = total_time / total_requests if total_requests > 0 else 0
            error_count = sum(1 for req in self.request_times if req['status_code'] >= 400)
            slow_requests = sum(1 for req in self.request_times if req['response_time'] > 1.0)  # > 1 second
            
            return {
                'avg_response_time': avg_response_time,
                'total_requests': total_requests,
                'error_rate': error_count / total_requests if total_requests > 0 else 0,
                'slow_requests': slow_requests,
                'slow_request_percentage': (slow_requests / total_requests * 100) if total_requests > 0 else 0
            }
    
    def get_slow_endpoints(self, threshold=1.0):
        """Get endpoints with average response time above threshold"""
        with self.lock:
            slow_endpoints = []
            for endpoint, stats in self.endpoint_stats.items():
                if stats['count'] > 0:
                    avg_time = stats['total_time'] / stats['count']
                    if avg_time > threshold:
                        slow_endpoints.append({
                            'endpoint': endpoint,
                            'avg_time': avg_time,
                            'count': stats['count'],
                            'min_time': stats['min_time'],
                            'max_time': stats['max_time']
                        })
            return sorted(slow_endpoints, key=lambda x: x['avg_time'], reverse=True)
    
    def get_system_resources(self):
        """Get current system resource usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_info = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_info.percent,
                'memory_available_gb': memory_info.available / (1024**3),
                'memory_total_gb': memory_info.total / (1024**3),
                'disk_percent': disk_usage.percent,
                'disk_free_gb': disk_usage.free / (1024**3),
                'process_count': len(psutil.pids()),
                'timestamp': datetime.utcnow()
            }
        except Exception as e:
            self.logger.error(f"Failed to get system resources: {e}")
            return {}
    
    def log_system_health_check(self):
        """Log a comprehensive system health check"""
        resources = self.get_system_resources()
        if resources:
            self.logger.info(
                f"System Health: CPU {resources['cpu_percent']:.1f}%, "
                f"Memory {resources['memory_percent']:.1f}%, "
                f"Disk {resources['disk_percent']:.1f}%",
                extra=resources
            )
        
        # Log performance summary
        perf_summary = self.get_performance_summary()
        self.logger.info(
            f"Performance Summary: Avg Response Time {perf_summary['avg_response_time']:.3f}s, "
            f"Total Requests {perf_summary['total_requests']}, "
            f"Error Rate {perf_summary['error_rate']:.2%}",
            extra=perf_summary
        )


# Global performance monitor instance
perf_monitor = PerformanceMonitor()


def monitor_performance(endpoint_name=None):
    """Decorator to monitor performance of functions/endpoints"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                response_time = time.time() - start_time
                
                # Determine endpoint name
                actual_endpoint = endpoint_name or f"{func.__module__}.{func.__name__}"
                
                # Record performance
                perf_monitor.record_request(
                    endpoint=actual_endpoint,
                    method='FUNC',
                    response_time=response_time,
                    status_code=200
                )
                
                return result
            except Exception as e:
                response_time = time.time() - start_time
                # Record error
                perf_monitor.record_request(
                    endpoint=actual_endpoint,
                    method='FUNC',
                    response_time=response_time,
                    status_code=500
                )
                raise e
        return wrapper
    return decorator


def measure_execution_time(func):
    """Decorator to measure execution time of any function"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Log execution time
        logging.info(f"Function {func.__name__} executed in {execution_time:.4f}s")
        
        return result
    return wrapper


# Create a decorator for Flask routes
def track_performance():
    """Track performance of Flask routes"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                
                # Get the request object if available
                try:
                    from flask import request
                    endpoint = request.endpoint or func.__name__
                    method = request.method
                    response_time = time.time() - start_time
                    
                    # If result is a tuple (response, status), extract status
                    status_code = 200
                    if isinstance(result, tuple):
                        if len(result) >= 2 and isinstance(result[1], int):
                            status_code = result[1]
                    
                    perf_monitor.record_request(
                        endpoint=endpoint,
                        method=method,
                        response_time=response_time,
                        status_code=status_code
                    )
                except ImportError:
                    # Flask not available, just measure time
                    pass
                
                return result
            except Exception as e:
                # Record error
                try:
                    from flask import request
                    endpoint = request.endpoint or func.__name__
                    method = request.method
                    response_time = time.time() - start_time
                    
                    perf_monitor.record_request(
                        endpoint=endpoint,
                        method=method,
                        response_time=response_time,
                        status_code=500
                    )
                except ImportError:
                    pass
                raise e
        return wrapper
    return decorator