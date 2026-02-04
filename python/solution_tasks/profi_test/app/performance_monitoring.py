"""
Advanced database performance monitoring and metrics collection
"""
import logging
import time
import psutil
import os
from collections import defaultdict, deque
from threading import Lock, Thread
from datetime import datetime, timedelta, timezone
from sqlalchemy import text
import json

logger = logging.getLogger(__name__)

class DatabasePerformanceMonitor:
    """Advanced database performance monitoring system"""
    
    def __init__(self, app=None):
        self.app = app
        self.metrics = defaultdict(list)
        self.alerts = deque(maxlen=100)
        self.lock = Lock()
        self.monitoring_thread = None
        self.is_monitoring = False
        self.monitoring_interval = 30  # seconds
        
        # Performance thresholds
        self.thresholds = {
            'slow_query': 0.5,  # seconds
            'high_connection_usage': 0.8,  # 80% of pool
            'slow_request': 1.0,  # seconds
            'high_memory_usage': 500,  # MB
            'high_cpu_usage': 80,  # percentage
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start background monitoring thread"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            logger.info("Database performance monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Database performance monitoring stopped")
    
    def _monitoring_loop(self):
        """Background monitoring loop"""
        while self.is_monitoring:
            try:
                self._collect_metrics()
                self._check_thresholds()
                time.sleep(self.monitoring_interval)
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(5)  # Wait before retrying
    
    def _collect_metrics(self):
        """Collect various performance metrics"""
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Database metrics
        db_metrics = self._collect_database_metrics()
        self._store_metrics('database', db_metrics, timestamp)
        
        # System metrics
        system_metrics = self._collect_system_metrics()
        self._store_metrics('system', system_metrics, timestamp)
        
        # Application metrics
        app_metrics = self._collect_application_metrics()
        self._store_metrics('application', app_metrics, timestamp)
    
    def _collect_database_metrics(self):
        """Collect database-specific metrics"""
        metrics = {}
        
        try:
            from app import db
            
            # Query execution statistics
            if hasattr(db, 'connection_manager'):
                pool_stats = db.connection_manager.get_pool_statistics()
                metrics.update({
                    'connections_in_use': pool_stats.get('connections_in_use', 0),
                    'pool_size': pool_stats.get('pool_size', 0),
                    'avg_query_time': pool_stats.get('avg_query_time', 0),
                    'queries_executed': pool_stats.get('queries_executed', 0),
                    'slow_queries': pool_stats.get('slow_queries', 0)
                })
            
            # Database size (SQLite specific)
            try:
                result = db.engine.execute(text("PRAGMA page_count"))
                page_count = result.fetchone()[0]
                result = db.engine.execute(text("PRAGMA page_size"))
                page_size = result.fetchone()[0]
                db_size = (page_count * page_size) / (1024 * 1024)  # MB
                metrics['database_size_mb'] = round(db_size, 2)
            except Exception:
                pass
            
            # Index statistics
            try:
                result = db.engine.execute(text("""
                    SELECT count(*) FROM sqlite_master 
                    WHERE type = 'index' AND name NOT LIKE 'sqlite_%'
                """))
                metrics['index_count'] = result.fetchone()[0]
            except Exception:
                pass
                
        except Exception as e:
            logger.warning(f"Failed to collect database metrics: {e}")
        
        return metrics
    
    def _collect_system_metrics(self):
        """Collect system-level metrics"""
        metrics = {}
        
        try:
            # Process metrics
            process = psutil.Process(os.getpid())
            metrics.update({
                'memory_rss_mb': round(process.memory_info().rss / 1024 / 1024, 2),
                'memory_vms_mb': round(process.memory_info().vms / 1024 / 1024, 2),
                'cpu_percent': process.cpu_percent(),
                'num_threads': process.num_threads(),
                'num_fds': process.num_fds() if hasattr(process, 'num_fds') else 0
            })
            
            # System metrics
            metrics.update({
                'system_cpu_percent': psutil.cpu_percent(),
                'system_memory_percent': psutil.virtual_memory().percent,
                'system_memory_available_mb': round(psutil.virtual_memory().available / 1024 / 1024, 2),
                'disk_usage_percent': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:').percent
            })
            
        except Exception as e:
            logger.warning(f"Failed to collect system metrics: {e}")
        
        return metrics
    
    def _collect_application_metrics(self):
        """Collect application-level metrics"""
        metrics = {}
        
        try:
            # Request statistics
            if hasattr(self.app, 'structured_logger'):
                log_stats = self.app.structured_logger.get_log_statistics()
                metrics.update({
                    'total_requests': log_stats.get('total_requests', 0),
                    'slow_requests': log_stats.get('slow_requests', 0),
                    'errors': log_stats.get('errors', 0),
                    'slow_queries': log_stats.get('slow_queries', 0)
                })
            
            # Cache statistics
            if hasattr(self.app, 'cache'):
                try:
                    cache_stats = self.app.cache.get_stats()
                    if cache_stats:
                        metrics['cache_hits'] = cache_stats.get('hits', 0)
                        metrics['cache_misses'] = cache_stats.get('misses', 0)
                        metrics['cache_hit_ratio'] = (
                            cache_stats.get('hits', 0) / 
                            (cache_stats.get('hits', 0) + cache_stats.get('misses', 1))
                        )
                except Exception:
                    pass
                    
        except Exception as e:
            logger.warning(f"Failed to collect application metrics: {e}")
        
        return metrics
    
    def _store_metrics(self, category, metrics, timestamp):
        """Store collected metrics"""
        if not metrics:
            return
            
        with self.lock:
            for key, value in metrics.items():
                metric_key = f"{category}.{key}"
                self.metrics[metric_key].append({
                    'value': value,
                    'timestamp': timestamp
                })
                
                # Keep only last 1000 measurements
                if len(self.metrics[metric_key]) > 1000:
                    self.metrics[metric_key] = self.metrics[metric_key][-500:]
    
    def _check_thresholds(self):
        """Check metrics against thresholds and generate alerts"""
        current_metrics = self.get_current_metrics()
        
        # Check slow queries
        if current_metrics.get('database.avg_query_time', 0) > self.thresholds['slow_query']:
            self._generate_alert('slow_query', 'High average query time detected')
        
        # Check connection pool usage
        pool_usage = (
            current_metrics.get('database.connections_in_use', 0) / 
            max(current_metrics.get('database.pool_size', 1), 1)
        )
        if pool_usage > self.thresholds['high_connection_usage']:
            self._generate_alert('high_connection_usage', 'High database connection pool usage')
        
        # Check system resources
        if current_metrics.get('system.memory_rss_mb', 0) > self.thresholds['high_memory_usage']:
            self._generate_alert('high_memory_usage', 'High memory usage detected')
            
        if current_metrics.get('system.cpu_percent', 0) > self.thresholds['high_cpu_usage']:
            self._generate_alert('high_cpu_usage', 'High CPU usage detected')
    
    def _generate_alert(self, alert_type, message):
        """Generate performance alert"""
        alert = {
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'severity': self._determine_severity(alert_type)
        }
        
        with self.lock:
            self.alerts.append(alert)
        
        logger.warning(f"Performance Alert [{alert_type}]: {message}")
    
    def _determine_severity(self, alert_type):
        """Determine alert severity"""
        critical_alerts = ['high_memory_usage', 'high_cpu_usage']
        warning_alerts = ['slow_query', 'high_connection_usage']
        
        if alert_type in critical_alerts:
            return 'critical'
        elif alert_type in warning_alerts:
            return 'warning'
        else:
            return 'info'
    
    def get_current_metrics(self):
        """Get current metric values"""
        current = {}
        with self.lock:
            for metric_key, values in self.metrics.items():
                if values:
                    current[metric_key] = values[-1]['value']
        return current
    
    def get_metrics_history(self, metric_name, hours=1):
        """Get historical metrics for a specific metric"""
        with self.lock:
            if metric_name not in self.metrics:
                return []
            
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
            cutoff_timestamp = cutoff_time.isoformat()
            
            return [
                entry for entry in self.metrics[metric_name]
                if entry['timestamp'] >= cutoff_timestamp
            ]
    
    def get_performance_report(self, hours=24):
        """Generate comprehensive performance report"""
        current_metrics = self.get_current_metrics()
        recent_alerts = list(self.alerts)[-20:]  # Last 20 alerts
        
        # Calculate trends
        trends = self._calculate_trends(hours)
        
        # System health score
        health_score = self._calculate_health_score(current_metrics)
        
        return {
            'current_metrics': current_metrics,
            'trends': trends,
            'alerts': recent_alerts,
            'health_score': health_score,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'report_period_hours': hours
        }
    
    def _calculate_trends(self, hours):
        """Calculate metric trends over time"""
        trends = {}
        
        with self.lock:
            for metric_key, values in self.metrics.items():
                if len(values) < 2:
                    continue
                
                # Get values from the specified time period
                cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
                cutoff_timestamp = cutoff_time.isoformat()
                
                recent_values = [
                    v['value'] for v in values 
                    if v['timestamp'] >= cutoff_timestamp
                ]
                
                if len(recent_values) >= 2:
                    # Calculate trend (simple linear trend)
                    first_value = recent_values[0]
                    last_value = recent_values[-1]
                    trend = ((last_value - first_value) / first_value * 100) if first_value != 0 else 0
                    
                    trends[metric_key] = {
                        'trend_percent': round(trend, 2),
                        'first_value': first_value,
                        'last_value': last_value,
                        'count': len(recent_values)
                    }
        
        return trends
    
    def _calculate_health_score(self, metrics):
        """Calculate overall system health score (0-100)"""
        score = 100
        
        # Deduct points for various issues
        if metrics.get('database.avg_query_time', 0) > 1.0:
            score -= 20
        elif metrics.get('database.avg_query_time', 0) > 0.5:
            score -= 10
            
        if metrics.get('system.memory_rss_mb', 0) > 800:
            score -= 25
        elif metrics.get('system.memory_rss_mb', 0) > 500:
            score -= 15
            
        if metrics.get('system.cpu_percent', 0) > 90:
            score -= 20
        elif metrics.get('system.cpu_percent', 0) > 70:
            score -= 10
            
        if metrics.get('application.errors', 0) > 10:
            score -= 15
        elif metrics.get('application.errors', 0) > 5:
            score -= 5
            
        return max(0, score)  # Ensure score doesn't go below 0

# Global performance monitor instance
db_performance_monitor = DatabasePerformanceMonitor()

def get_database_performance_status():
    """Get current database performance status"""
    try:
        return db_performance_monitor.get_performance_report()
    except Exception as e:
        logger.error(f"Failed to get performance status: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

def register_monitoring_commands(app):
    """Register monitoring CLI commands"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('perf-report')
    @click.option('--hours', default=24, help='Report period in hours')
    @with_appcontext
    def performance_report(hours):
        """Generate performance report"""
        report = db_performance_monitor.get_performance_report(hours)
        
        click.echo(f"Performance Report (Last {hours} hours):")
        click.echo(f"Health Score: {report['health_score']}/100")
        click.echo(f"Current Time: {report['timestamp']}")
        
        click.echo("\nCurrent Metrics:")
        for key, value in report['current_metrics'].items():
            click.echo(f"  {key}: {value}")
        
        if report['alerts']:
            click.echo("\nRecent Alerts:")
            for alert in report['alerts'][-5:]:  # Last 5 alerts
                click.echo(f"  [{alert['severity']}] {alert['type']}: {alert['message']}")
        
        if report['trends']:
            click.echo("\nTrends:")
            for metric, trend in list(report['trends'].items())[:5]:  # First 5 trends
                direction = "↑" if trend['trend_percent'] > 0 else "↓"
                click.echo(f"  {metric}: {direction} {trend['trend_percent']:.2f}%")