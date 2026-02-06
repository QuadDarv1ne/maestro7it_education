"""
Enhanced performance monitoring dashboard with real-time metrics and visualization
"""
import logging
from flask import Blueprint, render_template, jsonify, request
from typing import Dict, Any, List
import time
import psutil
import threading
from collections import defaultdict, deque
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

# Create blueprint
performance_dashboard = Blueprint('performance_dashboard_enhanced', __name__, 
                                template_folder='templates')

class EnhancedPerformanceMonitor:
    """Enhanced performance monitoring with real-time metrics collection"""
    
    def __init__(self, app=None):
        self.app = app
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))
        self.alerts = deque(maxlen=100)
        self.monitoring_stats = defaultdict(int)
        self.thresholds = {
            'cpu_usage': 80,
            'memory_usage': 85,
            'response_time': 1.0,
            'error_rate': 0.05,
            'database_slow_queries': 0.5,
            'queue_size': 100
        }
        self.is_monitoring = False
        self.monitoring_thread = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize performance monitor with Flask app"""
        self.app = app
        app.performance_monitor_enhanced = self
        
        # Register routes
        app.register_blueprint(performance_dashboard, url_prefix='/performance')
        
        # Start monitoring
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start background performance monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitor_system, daemon=True)
            self.monitoring_thread.start()
            logger.info("Enhanced performance monitoring started")
    
    def _monitor_system(self):
        """Background system monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect system metrics
                metrics = self._collect_system_metrics()
                
                # Store metrics
                timestamp = time.time()
                for key, value in metrics.items():
                    self.metrics_history[key].append((timestamp, value))
                
                # Check for alerts
                self._check_alerts(metrics)
                
                # Update statistics
                self.monitoring_stats['collections'] += 1
                
                time.sleep(5)  # Collect every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in system monitoring: {e}")
                time.sleep(10)  # Wait longer on error
    
    def _collect_system_metrics(self) -> Dict[str, Any]:
        """Collect comprehensive system metrics"""
        metrics = {}
        
        try:
            # System metrics
            metrics['cpu_percent'] = psutil.cpu_percent(interval=1)
            metrics['memory_percent'] = psutil.virtual_memory().percent
            metrics['memory_available'] = psutil.virtual_memory().available / (1024 * 1024)  # MB
            metrics['disk_usage'] = psutil.disk_usage('/').percent if hasattr(psutil, 'disk_usage') else 0
            
            # Network metrics
            net_io = psutil.net_io_counters()
            metrics['network_bytes_sent'] = net_io.bytes_sent
            metrics['network_bytes_recv'] = net_io.bytes_recv
            
            # Process metrics
            current_process = psutil.Process()
            metrics['process_cpu_percent'] = current_process.cpu_percent()
            metrics['process_memory_mb'] = current_process.memory_info().rss / (1024 * 1024)
            metrics['process_threads'] = current_process.num_threads()
            
            # App-specific metrics (if available)
            if hasattr(self.app, 'db_engine'):
                # Database connection pool metrics
                pool = self.app.db_engine.pool
                # Handle different pool types
                if hasattr(pool, 'size'):
                    metrics['db_pool_size'] = pool.size()
                else:
                    metrics['db_pool_size'] = 1  # StaticPool default
                
                if hasattr(pool, 'checkedout'):
                    metrics['db_connections_used'] = pool.checkedout()
                else:
                    metrics['db_connections_used'] = 0
                
                if hasattr(pool, 'checkedin'):
                    metrics['db_connections_available'] = pool.checkedin()
                else:
                    metrics['db_connections_available'] = 1
            
            if hasattr(self.app, 'cache'):
                # Cache metrics
                try:
                    cache_stats = self.app.cache.get_stats()
                    metrics['cache_hits'] = cache_stats.get('hits', 0)
                    metrics['cache_misses'] = cache_stats.get('misses', 0)
                except:
                    pass
            
            # Request metrics (from app context)
            metrics['active_requests'] = len(psutil.Process().threads())
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            metrics['error'] = str(e)
        
        return metrics
    
    def _check_alerts(self, metrics: Dict[str, Any]):
        """Check metrics against thresholds and generate alerts"""
        timestamp = datetime.utcnow().isoformat()
        
        # CPU usage alert
        if metrics.get('cpu_percent', 0) > self.thresholds['cpu_usage']:
            self._add_alert('HIGH_CPU', f"CPU usage {metrics['cpu_percent']:.1f}% exceeds threshold", timestamp)
        
        # Memory usage alert
        if metrics.get('memory_percent', 0) > self.thresholds['memory_usage']:
            self._add_alert('HIGH_MEMORY', f"Memory usage {metrics['memory_percent']:.1f}% exceeds threshold", timestamp)
        
        # Process memory alert
        if metrics.get('process_memory_mb', 0) > 500:  # 500MB
            self._add_alert('HIGH_PROCESS_MEMORY', f"Process memory {metrics['process_memory_mb']:.1f}MB is high", timestamp)
    
    def _add_alert(self, alert_type: str, message: str, timestamp: str):
        """Add alert to alert queue"""
        alert = {
            'type': alert_type,
            'message': message,
            'timestamp': timestamp,
            'severity': 'warning' if 'HIGH' in alert_type else 'info'
        }
        self.alerts.append(alert)
        self.monitoring_stats['alerts_generated'] += 1
        logger.warning(f"Performance Alert [{alert_type}]: {message}")
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        return self._collect_system_metrics()
    
    def get_metrics_history(self, metric_name: str, hours: int = 1) -> List[Dict[str, Any]]:
        """Get historical metrics for a specific metric"""
        if metric_name not in self.metrics_history:
            return []
        
        cutoff_time = time.time() - (hours * 3600)
        history = []
        
        for timestamp, value in self.metrics_history[metric_name]:
            if timestamp >= cutoff_time:
                history.append({
                    'timestamp': datetime.fromtimestamp(timestamp).isoformat(),
                    'value': value
                })
        
        return history
    
    def get_all_metrics_history(self, hours: int = 1) -> Dict[str, List]:
        """Get historical data for all metrics"""
        result = {}
        for metric_name in self.metrics_history.keys():
            result[metric_name] = self.get_metrics_history(metric_name, hours)
        return result
    
    def get_alerts(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        return list(self.alerts)[-limit:]
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics"""
        return dict(self.monitoring_stats)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        current_metrics = self.get_current_metrics()
        alerts = self.get_alerts(20)
        stats = self.get_monitoring_stats()
        
        # Calculate averages from history
        averages = {}
        for metric_name, history in self.metrics_history.items():
            if history:
                values = [item[1] for item in history]
                averages[metric_name] = sum(values) / len(values)
        
        return {
            'current_metrics': current_metrics,
            'averages': averages,
            'alerts': alerts,
            'statistics': stats,
            'timestamp': datetime.utcnow().isoformat(),
            'thresholds': self.thresholds
        }

# Global instance
performance_monitor = EnhancedPerformanceMonitor()

@performance_dashboard.route('/')
def dashboard():
    """Performance dashboard main page"""
    return render_template('performance/dashboard.html')

@performance_dashboard.route('/api/metrics')
def api_metrics():
    """Get current metrics"""
    try:
        metrics = performance_monitor.get_current_metrics()
        return jsonify({
            'success': True,
            'data': metrics,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@performance_dashboard.route('/api/metrics/history')
def api_metrics_history():
    """Get metrics history"""
    try:
        metric_name = request.args.get('metric')
        hours = int(request.args.get('hours', 1))
        
        if metric_name:
            history = performance_monitor.get_metrics_history(metric_name, hours)
        else:
            history = performance_monitor.get_all_metrics_history(hours)
        
        return jsonify({
            'success': True,
            'data': history,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting metrics history: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@performance_dashboard.route('/api/alerts')
def api_alerts():
    """Get recent alerts"""
    try:
        limit = int(request.args.get('limit', 50))
        alerts = performance_monitor.get_alerts(limit)
        return jsonify({
            'success': True,
            'data': alerts,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@performance_dashboard.route('/api/report')
def api_performance_report():
    """Get comprehensive performance report"""
    try:
        report = performance_monitor.get_performance_report()
        return jsonify({
            'success': True,
            'data': report
        })
    except Exception as e:
        logger.error(f"Error generating performance report: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@performance_dashboard.route('/api/stats')
def api_monitoring_stats():
    """Get monitoring statistics"""
    try:
        stats = performance_monitor.get_monitoring_stats()
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        logger.error(f"Error getting monitoring stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Template for performance dashboard
def create_dashboard_template():
    """Create the HTML template for the performance dashboard"""
    template_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Performance Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .card { background: white; border-radius: 8px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .metric-card { background: #f8f9fa; padding: 15px; border-radius: 5px; }
        .metric-value { font-size: 24px; font-weight: bold; color: #007bff; }
        .metric-label { font-size: 14px; color: #6c757d; margin-top: 5px; }
        .alert { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .alert-warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; }
        .chart-container { height: 300px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Performance Monitoring Dashboard</h1>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value" id="cpu-value">--</div>
                <div class="metric-label">CPU Usage (%)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="memory-value">--</div>
                <div class="metric-label">Memory Usage (%)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="process-memory-value">--</div>
                <div class="metric-label">Process Memory (MB)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="db-connections-value">--</div>
                <div class="metric-label">DB Connections</div>
            </div>
        </div>
        
        <div class="card">
            <h3>System Metrics History</h3>
            <div class="chart-container">
                <canvas id="metrics-chart"></canvas>
            </div>
        </div>
        
        <div class="card">
            <h3>Recent Alerts</h3>
            <div id="alerts-container"></div>
        </div>
    </div>

    <script>
        let metricsChart;
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            initializeChart();
            updateDashboard();
            setInterval(updateDashboard, 5000); // Update every 5 seconds
        });
        
        function initializeChart() {
            const ctx = document.getElementById('metrics-chart').getContext('2d');
            metricsChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'CPU Usage %',
                        data: [],
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }, {
                        label: 'Memory Usage %',
                        data: [],
                        borderColor: 'rgb(54, 162, 235)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
        
        async function updateDashboard() {
            try {
                // Get current metrics
                const response = await fetch('/performance/api/metrics');
                const data = await response.json();
                
                if (data.success) {
                    updateMetricsDisplay(data.data);
                    updateChart(data.data);
                }
                
                // Get alerts
                const alertsResponse = await fetch('/performance/api/alerts?limit=10');
                const alertsData = await alertsResponse.json();
                
                if (alertsData.success) {
                    updateAlertsDisplay(alertsData.data);
                }
                
            } catch (error) {
                console.error('Error updating dashboard:', error);
            }
        }
        
        function updateMetricsDisplay(metrics) {
            document.getElementById('cpu-value').textContent = 
                metrics.cpu_percent ? metrics.cpu_percent.toFixed(1) : '--';
            document.getElementById('memory-value').textContent = 
                metrics.memory_percent ? metrics.memory_percent.toFixed(1) : '--';
            document.getElementById('process-memory-value').textContent = 
                metrics.process_memory_mb ? metrics.process_memory_mb.toFixed(1) : '--';
            document.getElementById('db-connections-value').textContent = 
                metrics.db_connections_used ? metrics.db_connections_used : '--';
        }
        
        function updateChart(metrics) {
            const now = new Date().toLocaleTimeString();
            
            metricsChart.data.labels.push(now);
            metricsChart.data.datasets[0].data.push(metrics.cpu_percent || 0);
            metricsChart.data.datasets[1].data.push(metrics.memory_percent || 0);
            
            // Keep only last 20 data points
            if (metricsChart.data.labels.length > 20) {
                metricsChart.data.labels.shift();
                metricsChart.data.datasets[0].data.shift();
                metricsChart.data.datasets[1].data.shift();
            }
            
            metricsChart.update();
        }
        
        function updateAlertsDisplay(alerts) {
            const container = document.getElementById('alerts-container');
            container.innerHTML = '';
            
            if (alerts.length === 0) {
                container.innerHTML = '<p>No recent alerts</p>';
                return;
            }
            
            alerts.forEach(alert => {
                const alertDiv = document.createElement('div');
                alertDiv.className = `alert alert-${alert.severity === 'warning' ? 'warning' : 'info'}`;
                alertDiv.innerHTML = `
                    <strong>[${alert.type}]</strong> ${alert.message}
                    <small style="float: right;">${new Date(alert.timestamp).toLocaleString()}</small>
                `;
                container.appendChild(alertDiv);
            });
        }
    </script>
</body>
</html>
    """
    
    # Create templates directory if it doesn't exist
    import os
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'performance')
    os.makedirs(template_dir, exist_ok=True)
    
    # Write template file
    template_path = os.path.join(template_dir, 'dashboard.html')
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(template_content.strip())
    
    logger.info(f"Performance dashboard template created at: {template_path}")

# Flask CLI commands
def register_performance_dashboard_commands(app):
    """Register CLI commands for performance dashboard"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('perf-dashboard-init')
    @with_appcontext
    def init_dashboard():
        """Initialize performance dashboard template"""
        create_dashboard_template()
        click.echo("Performance dashboard template initialized")
    
    @app.cli.command('perf-report')
    @with_appcontext
    def show_performance_report():
        """Show current performance report"""
        if hasattr(app, 'performance_monitor_enhanced'):
            report = app.performance_monitor_enhanced.get_performance_report()
            click.echo(json.dumps(report, indent=2, default=str))
        else:
            click.echo("Performance monitor not initialized")
