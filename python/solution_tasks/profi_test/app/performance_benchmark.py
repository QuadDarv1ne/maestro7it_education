"""
Performance benchmarking utilities for the profi_test application
"""
import time
import threading
import functools
import statistics
from datetime import datetime
from collections import defaultdict, deque
import logging

from flask import g, request
from app.performance import PerformanceMonitor
from app.advanced_caching import AdvancedCacheManager
from app.database_pooling import db_connection_manager


logger = logging.getLogger(__name__)


class PerformanceBenchmark:
    """Performance benchmarking and continuous monitoring"""
    
    def __init__(self):
        self.benchmarks = defaultdict(list)
        self.running_stats = defaultdict(deque)  # Use deque for efficient appends/pops
        self.monitor = PerformanceMonitor()
        self.cache_manager = AdvancedCacheManager()
        self.lock = threading.Lock()
    
    def benchmark_function(self, iterations=10, warmup=3):
        """
        Decorator to benchmark function performance
        
        Args:
            iterations: Number of times to run the function
            warmup: Number of warmup runs (not included in results)
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Warmup runs
                for _ in range(warmup):
                    func(*args, **kwargs)
                
                times = []
                for _ in range(iterations):
                    start_time = time.perf_counter()
                    result = func(*args, **kwargs)
                    end_time = time.perf_counter()
                    times.append((end_time - start_time) * 1000)  # Convert to ms
                
                # Calculate statistics
                stats = {
                    'mean': statistics.mean(times),
                    'median': statistics.median(times),
                    'stdev': statistics.stdev(times) if len(times) > 1 else 0,
                    'min': min(times),
                    'max': max(times),
                    'iterations': iterations,
                    'function_name': func.__name__
                }
                
                # Store benchmark results
                with self.lock:
                    self.benchmarks[func.__name__].append({
                        'timestamp': datetime.utcnow(),
                        'stats': stats,
                        'times': times
                    })
                
                logger.info(f"Benchmark for {func.__name__}: "
                           f"Mean={stats['mean']:.2f}ms, "
                           f"Median={stats['median']:.2f}ms, "
                           f"Min={stats['min']:.2f}ms, "
                           f"Max={stats['max']:.2f}ms")
                
                return result
            return wrapper
        return decorator
    
    def benchmark_endpoint(self, url, method='GET', data=None, headers=None, iterations=10):
        """
        Benchmark a specific endpoint
        
        Args:
            url: Endpoint URL to benchmark
            method: HTTP method (GET, POST, etc.)
            data: Request data for POST/PUT requests
            headers: Request headers
            iterations: Number of requests to make
        """
        from app import create_app
        app = create_app()  # Use current app context
        
        times = []
        statuses = []
        
        with app.test_client() as client:
            for _ in range(iterations):
                start_time = time.perf_counter()
                
                if method.upper() == 'GET':
                    response = client.get(url, headers=headers)
                elif method.upper() == 'POST':
                    response = client.post(url, data=data, headers=headers)
                elif method.upper() == 'PUT':
                    response = client.put(url, data=data, headers=headers)
                elif method.upper() == 'DELETE':
                    response = client.delete(url, headers=headers)
                
                end_time = time.perf_counter()
                times.append((end_time - start_time) * 1000)  # Convert to ms
                statuses.append(response.status_code)
        
        # Calculate statistics
        stats = {
            'mean_response_time': statistics.mean(times),
            'median_response_time': statistics.median(times),
            'stdev_response_time': statistics.stdev(times) if len(times) > 1 else 0,
            'min_response_time': min(times),
            'max_response_time': max(times),
            'success_rate': sum(1 for s in statuses if 200 <= s < 300) / len(statuses) * 100,
            'statuses': list(set(statuses)),
            'iterations': iterations,
            'url': url,
            'method': method
        }
        
        # Store benchmark results
        with self.lock:
            self.benchmarks[f"{method}_{url}"].append({
                'timestamp': datetime.utcnow(),
                'stats': stats,
                'times': times
            })
        
        logger.info(f"Endpoint benchmark for {method} {url}: "
                   f"Mean={stats['mean_response_time']:.2f}ms, "
                   f"Success Rate={stats['success_rate']:.1f}%")
        
        return stats
    
    def get_benchmark_history(self, function_name=None):
        """
        Get benchmark history for a specific function or all functions
        
        Args:
            function_name: Specific function to get history for, or None for all
        """
        if function_name:
            return self.benchmarks.get(function_name, [])
        else:
            return dict(self.benchmarks)
    
    def get_latest_benchmark(self, function_name):
        """Get the most recent benchmark for a specific function"""
        if self.benchmarks[function_name]:
            return self.benchmarks[function_name][-1]
        return None
    
    def calculate_performance_trend(self, function_name, window_size=5):
        """
        Calculate performance trend for a function over recent benchmarks
        
        Args:
            function_name: Function to analyze
            window_size: Number of recent benchmarks to consider
        """
        history = self.benchmarks[function_name][-window_size:]
        
        if len(history) < 2:
            return {'trend': 'insufficient_data', 'change': 0}
        
        recent_means = [benchmark['stats']['mean'] for benchmark in history]
        
        # Calculate percentage change from first to last
        first_mean = recent_means[0]
        last_mean = recent_means[-1]
        
        if first_mean != 0:
            change_percent = ((last_mean - first_mean) / first_mean) * 100
        else:
            change_percent = 0
        
        # Determine trend direction
        if change_percent > 5:
            trend = 'degrading'
        elif change_percent < -5:
            trend = 'improving'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'change_percent': change_percent,
            'first_mean': first_mean,
            'last_mean': last_mean,
            'window_size': len(recent_means)
        }
    
    def run_system_benchmark(self):
        """Run comprehensive system benchmark"""
        system_stats = {}
        
        # CPU usage benchmark
        cpu_start = self.monitor.get_cpu_usage()
        time.sleep(0.1)  # Brief pause
        cpu_end = self.monitor.get_cpu_usage()
        system_stats['cpu_usage'] = {
            'before': cpu_start,
            'after': cpu_end
        }
        
        # Memory usage
        system_stats['memory_usage'] = self.monitor.get_memory_usage()
        
        # Cache performance
        system_stats['cache_stats'] = self.cache_manager.get_cache_stats()
        
        # Database connection stats
        system_stats['db_pool_stats'] = db_connection_manager.get_pool_statistics()
        
        # Overall system performance score
        # Lower is better for response times, higher is better for efficiency
        score_components = []
        
        # Normalize different metrics to a 0-100 scale
        if system_stats['memory_usage'].get('percent', 0) <= 50:
            memory_score = 100 - (system_stats['memory_usage'].get('percent', 0) / 0.5)
        else:
            memory_score = max(0, 100 - ((system_stats['memory_usage'].get('percent', 0) - 50) * 2))
        
        # Extract cache hit ratio if available
        cache_stats = system_stats['cache_stats']
        if 'redis_stats' in cache_stats and 'hit_rate' in cache_stats['redis_stats']:
            cache_hit_ratio = cache_stats['redis_stats']['hit_rate']
        else:
            cache_hit_ratio = 0  # Default value if not available
        
        score_components.extend([memory_score, cache_hit_ratio])
        
        system_stats['performance_score'] = sum(score_components) / len(score_components) if score_components else 50
        
        # Store system benchmark
        with self.lock:
            self.benchmarks['system_benchmark'].append({
                'timestamp': datetime.utcnow(),
                'stats': system_stats
            })
        
        logger.info(f"System benchmark completed. Performance score: {system_stats['performance_score']:.1f}")
        
        return system_stats


# Global benchmark instance
benchmark = PerformanceBenchmark()


def register_benchmark_commands(app):
    """Register benchmark CLI commands"""
    import click
    from flask.cli import with_appcontext
    from app import db
    from app.models import User
    
    @app.cli.command('benchmark-function')
    @click.argument('function_name')
    @click.option('--iterations', default=10, help='Number of iterations to run')
    @click.option('--warmup', default=3, help='Number of warmup runs')
    @with_appcontext
    def benchmark_function_cmd(function_name, iterations, warmup):
        """Benchmark a specific function"""
        # This would typically benchmark actual application functions
        click.echo(f"Benchmarking function: {function_name}")
        click.echo("Note: Actual function benchmarking requires specific function implementation")
    
    @app.cli.command('benchmark-endpoint')
    @click.argument('url')
    @click.option('--method', default='GET', help='HTTP method')
    @click.option('--iterations', default=10, help='Number of requests to make')
    @with_appcontext
    def benchmark_endpoint_cmd(url, method, iterations):
        """Benchmark a specific endpoint"""
        click.echo(f"Benchmarking endpoint: {method} {url} ({iterations} iterations)")
        
        try:
            stats = benchmark.benchmark_endpoint(
                url=url,
                method=method,
                iterations=iterations
            )
            click.echo(f"Mean response time: {stats['mean_response_time']:.2f}ms")
            click.echo(f"Success rate: {stats['success_rate']:.1f}%")
        except Exception as e:
            click.echo(f"Error benchmarking endpoint: {e}")
    
    @app.cli.command('benchmark-system')
    @with_appcontext
    def benchmark_system_cmd():
        """Run comprehensive system benchmark"""
        click.echo("Running system benchmark...")
        
        stats = benchmark.run_system_benchmark()
        
        click.echo("System Benchmark Results:")
        click.echo(f"  Performance Score: {stats['performance_score']:.1f}/100")
        click.echo(f"  Memory Usage: {stats['memory_usage'].get('percent', 'N/A')}%")
        click.echo(f"  Cache Hit Ratio: {stats['cache_stats'].get('hit_ratio', 0)*100:.1f}%")
        click.echo(f"  DB Connections: {stats.get('db_pool_stats', {}).get('checkouts', 'N/A')}")
    
    @app.cli.command('benchmark-history')
    @click.argument('function_name', required=False)
    @with_appcontext
    def benchmark_history_cmd(function_name):
        """Show benchmark history"""
        history = benchmark.get_benchmark_history(function_name)
        
        if function_name:
            if history:
                click.echo(f"Benchmark history for '{function_name}':")
                for record in history[-5:]:  # Show last 5 benchmarks
                    timestamp = record['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                    if 'stats' in record:
                        mean_time = record['stats'].get('mean', record['stats'].get('mean_response_time', 'N/A'))
                        click.echo(f"  {timestamp}: {mean_time:.2f}ms")
            else:
                click.echo(f"No benchmark history found for '{function_name}'")
        else:
            click.echo("All benchmarked functions:")
            for func_name in benchmark.benchmarks.keys():
                count = len(benchmark.benchmarks[func_name])
                click.echo(f"  {func_name}: {count} benchmarks")


# Context processor to make benchmark available in templates (optional)
def add_benchmark_to_jinja(app):
    """Add benchmark utilities to Jinja template context"""
    @app.context_processor
    def inject_benchmark():
        return {
            'benchmark': benchmark
        }