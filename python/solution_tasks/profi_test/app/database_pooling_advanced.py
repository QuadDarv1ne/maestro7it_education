"""
Advanced database connection pooling with performance optimization
"""
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool, NullPool
from sqlalchemy.pool import StaticPool
from typing import Dict, Any, Optional
import time
import threading
from collections import defaultdict, deque
from contextlib import contextmanager
import psutil
import os

logger = logging.getLogger(__name__)

class AdvancedConnectionPool:
    """Advanced database connection pool with performance monitoring and optimization"""
    
    def __init__(self, app=None):
        self.app = app
        self.engine = None
        self.pool_stats = defaultdict(int)
        self.connection_times = deque(maxlen=1000)
        self.query_times = defaultdict(list)
        self.pool_lock = threading.Lock()
        self.monitoring_thread = None
        self.is_monitoring = False
        
        # Performance thresholds
        self.thresholds = {
            'max_pool_size': 20,
            'min_pool_size': 5,
            'pool_timeout': 30,
            'pool_recycle': 3600,  # 1 hour
            'max_overflow': 10,
            'slow_query_threshold': 0.5,  # seconds
            'connection_timeout_threshold': 2.0,  # seconds
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize advanced connection pool with Flask app"""
        self.app = app
        
        # Get database configuration
        database_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        engine_options = app.config.get('SQLALCHEMY_ENGINE_OPTIONS', {})
        
        # Create optimized engine with advanced pooling
        self.engine = self._create_advanced_engine(database_uri, engine_options)
        
        # Store engine in app for easy access
        app.db_engine = self.engine
        app.connection_pool = self
        
        # Register event listeners
        self._register_event_listeners()
        
        # Start performance monitoring
        self._start_monitoring()
    
    def _create_advanced_engine(self, database_uri: str, engine_options: Dict[str, Any]):
        """Create SQLAlchemy engine with advanced pooling configuration"""
        
        # Base pool configuration
        pool_config = {
            'poolclass': QueuePool,
            'pool_size': self.thresholds['min_pool_size'],
            'max_overflow': self.thresholds['max_overflow'],
            'pool_timeout': self.thresholds['pool_timeout'],
            'pool_recycle': self.thresholds['pool_recycle'],
            'pool_pre_ping': True,  # Verify connections before use
            'echo': False,  # Disable SQL logging in production
        }
        
        # Database-specific optimizations
        if 'sqlite' in database_uri:
            # SQLite-specific configuration
            pool_config['poolclass'] = StaticPool
            pool_config['connect_args'] = {
                'check_same_thread': False,
                'timeout': 30,
            }
            # Remove pool sizing options for StaticPool
            pool_config.pop('pool_size', None)
            pool_config.pop('max_overflow', None)
            pool_config.pop('pool_timeout', None)
        elif 'postgresql' in database_uri:
            pool_config.update({
                'pool_size': 10,
                'max_overflow': 20,
                'connect_args': {
                    'connect_timeout': 10,
                    'keepalives': 1,
                    'keepalives_idle': 30,
                    'keepalives_interval': 10,
                    'keepalives_count': 5,
                }
            })
        elif 'mysql' in database_uri:
            pool_config.update({
                'pool_size': 10,
                'max_overflow': 15,
                'connect_args': {
                    'charset': 'utf8mb4',
                    'connect_timeout': 10,
                    'read_timeout': 10,
                    'write_timeout': 10,
                }
            })
        
        # Merge with user-provided options
        pool_config.update(engine_options)
        
        # Create engine - handle SQLite differently
        if 'sqlite' in database_uri:
            # For SQLite with StaticPool, we need to be more careful
            sqlite_config = {
                'poolclass': pool_config['poolclass'],
                'connect_args': pool_config['connect_args'],
                'echo': pool_config.get('echo', False),
                'pool_pre_ping': pool_config.get('pool_pre_ping', True),
                'pool_recycle': pool_config.get('pool_recycle', 3600)
            }
            engine = create_engine(database_uri, **sqlite_config)
        else:
            # For other databases, use full pool configuration
            engine = create_engine(database_uri, **pool_config)
        
        logger.info(f"Advanced connection pool created for {database_uri}")
        if 'sqlite' in database_uri:
            logger.info("SQLite configuration: StaticPool with thread safety")
        else:
            logger.info(f"Pool config: size={pool_config.get('pool_size', 'default')}, overflow={pool_config.get('max_overflow', 'default')}")
        
        return engine
    
    def _register_event_listeners(self):
        """Register SQLAlchemy event listeners for performance monitoring"""
        
        @event.listens_for(self.engine, "connect")
        def set_connection_pragmas(dbapi_connection, connection_record):
            """Set database-specific optimizations on connection"""
            try:
                cursor = dbapi_connection.cursor()
                
                if 'sqlite' in str(self.engine.url):
                    # SQLite optimizations
                    optimizations = [
                        "PRAGMA journal_mode=WAL",
                        "PRAGMA synchronous=NORMAL",
                        "PRAGMA cache_size=10000",
                        "PRAGMA temp_store=MEMORY",
                        "PRAGMA mmap_size=268435456",  # 256MB
                        "PRAGMA foreign_keys=ON",
                    ]
                    for opt in optimizations:
                        cursor.execute(opt)
                
                elif 'postgresql' in str(self.engine.url):
                    # PostgreSQL optimizations
                    cursor.execute("SET statement_timeout = 30000")  # 30 seconds
                    cursor.execute("SET idle_in_transaction_session_timeout = 60000")  # 1 minute
                
                elif 'mysql' in str(self.engine.url):
                    # MySQL optimizations
                    cursor.execute("SET SESSION sql_mode = 'STRICT_TRANS_TABLES'")
                    cursor.execute("SET SESSION innodb_flush_log_at_trx_commit = 2")
                
                cursor.close()
                
            except Exception as e:
                logger.warning(f"Error setting connection pragmas: {e}")
        
        @event.listens_for(self.engine, "checkout")
        def receive_checkout(dbapi_connection, connection_record, connection_proxy):
            """Monitor connection checkout performance"""
            start_time = time.time()
            connection_record.info['checkout_start_time'] = start_time
            
            with self.pool_lock:
                self.pool_stats['connections_checked_out'] += 1
        
        @event.listens_for(self.engine, "checkin")
        def receive_checkin(dbapi_connection, connection_record):
            """Monitor connection checkin and calculate checkout time"""
            checkout_time = time.time() - connection_record.info.get('checkout_start_time', time.time())
            
            with self.pool_lock:
                self.connection_times.append(checkout_time)
                self.pool_stats['connections_checked_in'] += 1
                
                # Track slow connections
                if checkout_time > self.thresholds['connection_timeout_threshold']:
                    self.pool_stats['slow_connections'] += 1
        
        @event.listens_for(self.engine, "close")
        def receive_close(dbapi_connection, connection_record):
            """Monitor connection closure"""
            with self.pool_lock:
                self.pool_stats['connections_closed'] += 1
        
        @event.listens_for(self.engine, "close_detached")
        def receive_close_detached(dbapi_connection):
            """Monitor detached connection closure"""
            with self.pool_lock:
                self.pool_stats['detached_connections_closed'] += 1
    
    def _start_monitoring(self):
        """Start background performance monitoring"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitor_pool_performance, daemon=True)
            self.monitoring_thread.start()
            logger.info("Connection pool performance monitoring started")
    
    def _monitor_pool_performance(self):
        """Background thread for monitoring pool performance"""
        import time
        while self.is_monitoring:
            try:
                # Collect pool statistics
                pool = self.engine.pool
                stats = {
                    'pool_size': pool.size(),
                    'checked_out_connections': pool.checkedout(),
                    'overflow_connections': getattr(pool, 'overflow', 0),
                    'checked_in_connections': pool.checkedin(),
                }
                
                # Log if pool is under pressure
                if stats['checked_out_connections'] > self.thresholds['max_pool_size'] * 0.8:
                    logger.warning(f"High connection pool usage: {stats['checked_out_connections']}/{self.thresholds['max_pool_size']}")
                
                # Update statistics
                with self.pool_lock:
                    self.pool_stats.update(stats)
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in pool monitoring: {e}")
                time.sleep(60)  # Wait longer on error
    
    @contextmanager
    def get_connection(self, timeout: Optional[float] = None):
        """
        Context manager for getting database connections with timeout
        
        Usage:
            with pool.get_connection(timeout=5.0) as conn:
                result = conn.execute(text("SELECT * FROM users"))
        """
        conn = None
        start_time = time.time()
        
        try:
            # Get connection with timeout
            conn = self.engine.connect()
            
            checkout_time = time.time() - start_time
            if timeout and checkout_time > timeout:
                raise TimeoutError(f"Connection checkout timeout: {checkout_time:.2f}s")
            
            yield conn
            
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query, params=None, timeout: Optional[float] = None):
        """
        Execute query with performance monitoring and timeout
        
        Args:
            query: SQL query string or SQLAlchemy text object
            params: Query parameters
            timeout: Query execution timeout in seconds
        """
        start_time = time.time()
        
        try:
            with self.get_connection(timeout=timeout) as conn:
                result = conn.execute(query, params or {})
                execution_time = time.time() - start_time
                
                # Track query performance
                query_key = str(query)[:100]  # First 100 chars as key
                with self.pool_lock:
                    self.query_times[query_key].append(execution_time)
                    if len(self.query_times[query_key]) > 100:
                        self.query_times[query_key] = self.query_times[query_key][-50:]
                
                # Log slow queries
                if execution_time > self.thresholds['slow_query_threshold']:
                    logger.warning(f"Slow query ({execution_time:.3f}s): {query_key}")
                    self.pool_stats['slow_queries'] += 1
                
                self.pool_stats['total_queries'] += 1
                return result
                
        except Exception as e:
            self.pool_stats['failed_queries'] += 1
            logger.error(f"Query execution failed: {e}")
            raise
    
    def get_pool_statistics(self) -> Dict[str, Any]:
        """Get comprehensive pool performance statistics"""
        with self.pool_lock:
            stats = self.pool_stats.copy()
            
            # Add calculated metrics
            if self.connection_times:
                stats['avg_connection_time'] = sum(self.connection_times) / len(self.connection_times)
                stats['min_connection_time'] = min(self.connection_times)
                stats['max_connection_time'] = max(self.connection_times)
            
            # Add query performance metrics
            query_stats = {}
            for query_key, times in self.query_times.items():
                if times:
                    query_stats[query_key] = {
                        'count': len(times),
                        'avg_time': sum(times) / len(times),
                        'min_time': min(times),
                        'max_time': max(times),
                        'slow_queries': len([t for t in times if t > self.thresholds['slow_query_threshold']])
                    }
            
            stats['query_performance'] = query_stats
            
            # Add system metrics
            stats['system_metrics'] = {
                'cpu_percent': psutil.cpu_percent(),
                'memory_percent': psutil.virtual_memory().percent,
                'pool_utilization': stats.get('checked_out_connections', 0) / max(stats.get('pool_size', 1), 1)
            }
            
            return stats
    
    def resize_pool(self, new_size: int, new_overflow: int = None):
        """Dynamically resize the connection pool"""
        try:
            pool = self.engine.pool
            
            # Update pool configuration
            if hasattr(pool, '_pool'):
                pool._pool.maxsize = new_size
            
            if new_overflow is not None and hasattr(pool, '_overflow'):
                pool._overflow = new_overflow
            
            logger.info(f"Pool resized to {new_size} connections, overflow {new_overflow or 'unchanged'}")
            
        except Exception as e:
            logger.error(f"Error resizing pool: {e}")
            raise
    
    def cleanup_connections(self):
        """Force cleanup of stale connections"""
        try:
            pool = self.engine.pool
            pool.recreate()
            logger.info("Connection pool cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up pool: {e}")

# Global instance
advanced_connection_pool = AdvancedConnectionPool()

# Flask CLI commands
def register_pool_advanced_commands(app):
    """Register CLI commands for advanced pool management"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('pool-stats-advanced')
    @with_appcontext
    def show_advanced_pool_stats():
        """Show advanced connection pool statistics"""
        if hasattr(app, 'connection_pool'):
            stats = app.connection_pool.get_pool_statistics()
            click.echo("Advanced Connection Pool Statistics:")
            for key, value in stats.items():
                if isinstance(value, dict):
                    click.echo(f"  {key}:")
                    for sub_key, sub_value in value.items():
                        click.echo(f"    {sub_key}: {sub_value}")
                else:
                    click.echo(f"  {key}: {value}")
        else:
            click.echo("Advanced connection pool not initialized")
    
    @app.cli.command('pool-resize')
    @click.option('--size', default=10, help='New pool size')
    @click.option('--overflow', default=None, type=int, help='New overflow size')
    @with_appcontext
    def resize_pool(size, overflow):
        """Resize connection pool"""
        if hasattr(app, 'connection_pool'):
            try:
                app.connection_pool.resize_pool(size, overflow)
                click.echo(f"Pool resized to {size} connections")
            except Exception as e:
                click.echo(f"Error resizing pool: {e}")
        else:
            click.echo("Advanced connection pool not initialized")
