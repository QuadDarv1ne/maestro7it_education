"""
Advanced database connection pooling and optimization configuration
"""
import logging
import time
from contextlib import contextmanager
from sqlalchemy import event, text
from sqlalchemy.pool import Pool, QueuePool
from sqlalchemy.engine import Engine
from collections import defaultdict, deque
from threading import Lock
from datetime import datetime
import psutil
import os

logger = logging.getLogger(__name__)

class DatabaseConnectionManager:
    """Advanced database connection pool manager with monitoring"""
    
    def __init__(self, app=None):
        self.app = app
        self.pool_stats = defaultdict(int)
        self.query_stats = defaultdict(lambda: {'count': 0, 'total_time': 0, 'slow_queries': 0})
        self.connection_history = deque(maxlen=1000)
        self.lock = Lock()
        self.slow_query_threshold = 0.5  # seconds
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        
        # Configure database connection pool
        app.config.setdefault('SQLALCHEMY_ENGINE_OPTIONS', {
            'poolclass': QueuePool,
            'pool_size': 20,
            'pool_recycle': 3600,  # Recycle connections after 1 hour
            'pool_pre_ping': True,  # Verify connections before use
            'pool_timeout': 30,
            'max_overflow': 30,
            'echo': app.config.get('SQLALCHEMY_ECHO', False),
        })
        
        # Register event listeners
        self._register_event_listeners()
        
        # Initialize database optimization
        self._setup_database_optimization()
    
    def _register_event_listeners(self):
        """Register SQLAlchemy event listeners for monitoring"""
        
        @event.listens_for(Engine, "connect")
        def connect(dbapi_connection, connection_record):
            """Track new database connections"""
            with self.lock:
                self.pool_stats['connections_made'] += 1
                self.connection_history.append({
                    'event': 'connect',
                    'timestamp': datetime.utcnow().isoformat(),
                    'connection_id': id(dbapi_connection)
                })
            
            # Apply database-specific optimizations
            try:
                if 'sqlite' in str(dbapi_connection):
                    cursor = dbapi_connection.cursor()
                    # Enable WAL mode for better concurrency
                    cursor.execute("PRAGMA journal_mode=WAL")
                    # Set synchronous mode for performance
                    cursor.execute("PRAGMA synchronous=NORMAL")
                    # Increase cache size
                    cursor.execute("PRAGMA cache_size=10000")
                    # Enable foreign keys
                    cursor.execute("PRAGMA foreign_keys=ON")
                    cursor.close()
            except Exception as e:
                logger.warning(f"Database optimization failed: {e}")
        
        @event.listens_for(Engine, "checkout")
        def checkout(dbapi_connection, connection_record, connection_proxy):
            """Track connection checkout from pool"""
            with self.lock:
                self.pool_stats['checkouts'] += 1
                connection_record.start_time = time.time()
        
        @event.listens_for(Engine, "checkin")
        def checkin(dbapi_connection, connection_record):
            """Track connection checkin to pool"""
            with self.lock:
                self.pool_stats['checkins'] += 1
                if hasattr(connection_record, 'start_time'):
                    duration = time.time() - connection_record.start_time
                    self.pool_stats['total_checkout_time'] += duration
                    if duration > 30:  # Long checkout time
                        logger.warning(f"Long connection checkout: {duration:.2f}s")
        
        @event.listens_for(Engine, "close")
        def close(dbapi_connection, connection_record):
            """Track connection closure"""
            with self.lock:
                self.pool_stats['connections_closed'] += 1
                self.connection_history.append({
                    'event': 'close',
                    'timestamp': datetime.utcnow().isoformat(),
                    'connection_id': id(dbapi_connection)
                })
        
        @event.listens_for(Engine, "before_cursor_execute")
        def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            """Track query execution start"""
            context._query_start_time = time.time()
            context._query_statement = statement[:100] + "..." if len(statement) > 100 else statement
        
        @event.listens_for(Engine, "after_cursor_execute")
        def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
            """Track query execution completion"""
            duration = time.time() - context._query_start_time
            
            with self.lock:
                # Update query statistics
                query_key = context._query_statement[:50]
                self.query_stats[query_key]['count'] += 1
                self.query_stats[query_key]['total_time'] += duration
                
                if duration > self.slow_query_threshold:
                    self.query_stats[query_key]['slow_queries'] += 1
                    logger.warning(f"Slow query ({duration:.3f}s): {context._query_statement}")
                
                # Update pool stats
                self.pool_stats['queries_executed'] += 1
                self.pool_stats['total_query_time'] += duration
        
        @event.listens_for(Pool, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            """SQLite-specific optimizations"""
            try:
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.close()
            except Exception:
                pass  # Not SQLite or optimization failed
    
    def _setup_database_optimization(self):
        """Apply database-specific optimizations"""
        try:
            from app import db
            
            # Apply general optimizations
            db.engine.execute(text("PRAGMA optimize"))
            
            logger.info("Database optimization applied successfully")
        except Exception as e:
            logger.warning(f"Database optimization failed: {e}")
    
    def get_pool_statistics(self):
        """Get current connection pool statistics"""
        with self.lock:
            stats = dict(self.pool_stats)
            
            # Calculate derived metrics
            if stats.get('checkouts', 0) > 0:
                stats['avg_checkout_time'] = (
                    stats.get('total_checkout_time', 0) / stats['checkouts']
                )
            else:
                stats['avg_checkout_time'] = 0
            
            if stats.get('queries_executed', 0) > 0:
                stats['avg_query_time'] = (
                    stats.get('total_query_time', 0) / stats['queries_executed']
                )
            else:
                stats['avg_query_time'] = 0
            
            # Add current pool status
            try:
                from app import db
                if hasattr(db.engine.pool, 'size'):
                    stats['pool_size'] = db.engine.pool.size()
                if hasattr(db.engine.pool, 'checkedout'):
                    stats['connections_in_use'] = db.engine.pool.checkedout()
                if hasattr(db.engine.pool, 'overflow'):
                    stats['overflow_connections'] = db.engine.pool.overflow()
            except Exception:
                pass
            
            return stats
    
    def get_query_statistics(self, limit=20):
        """Get query performance statistics"""
        with self.lock:
            # Sort queries by total execution time
            sorted_queries = sorted(
                self.query_stats.items(),
                key=lambda x: x[1]['total_time'],
                reverse=True
            )
            
            return {
                'top_slow_queries': [
                    {
                        'query': query[:100] + "..." if len(query) > 100 else query,
                        'count': stats['count'],
                        'total_time': round(stats['total_time'], 3),
                        'avg_time': round(stats['total_time'] / stats['count'], 4) if stats['count'] > 0 else 0,
                        'slow_queries': stats['slow_queries']
                    }
                    for query, stats in sorted_queries[:limit]
                ],
                'total_queries': len(self.query_stats)
            }
    
    def get_connection_history(self, limit=50):
        """Get recent connection history"""
        with self.lock:
            return list(self.connection_history)[-limit:]
    
    def reset_statistics(self):
        """Reset all statistics"""
        with self.lock:
            self.pool_stats.clear()
            self.query_stats.clear()
            self.connection_history.clear()
    
    def diagnose_pool_issues(self):
        """Diagnose potential connection pool issues"""
        issues = []
        stats = self.get_pool_statistics()
        
        # Check for connection leaks
        if stats.get('connections_made', 0) > stats.get('connections_closed', 0) * 2:
            issues.append("Potential connection leak detected")
        
        # Check for long checkout times
        if stats.get('avg_checkout_time', 0) > 5:
            issues.append("Long connection checkout times detected")
        
        # Check for slow queries
        query_stats = self.get_query_statistics()
        slow_queries = sum(1 for q in query_stats['top_slow_queries'] if q['slow_queries'] > 0)
        if slow_queries > 5:
            issues.append(f"High number of slow queries detected: {slow_queries}")
        
        # Check system resources
        try:
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            if memory_mb > 500:  # 500MB threshold
                issues.append(f"High memory usage: {memory_mb:.1f}MB")
        except Exception:
            pass
        
        return issues

# Global connection manager instance
db_connection_manager = DatabaseConnectionManager()

@contextmanager
def database_transaction():
    """Context manager for database transactions with monitoring"""
    from app import db
    
    start_time = time.time()
    try:
        yield db.session
        db.session.commit()
        
        duration = time.time() - start_time
        if duration > 2:  # Long transaction
            logger.warning(f"Long database transaction: {duration:.2f}s")
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database transaction failed: {e}")
        raise
    finally:
        db.session.close()

def get_database_health():
    """Get comprehensive database health status"""
    try:
        from app import db
        
        # Test database connectivity
        db.engine.execute(text("SELECT 1"))
        
        # Get pool statistics
        pool_stats = db_connection_manager.get_pool_statistics()
        
        # Get query statistics
        query_stats = db_connection_manager.get_query_statistics(5)
        
        # Check for issues
        issues = db_connection_manager.diagnose_pool_issues()
        
        return {
            'status': 'healthy' if not issues else 'degraded',
            'pool_statistics': pool_stats,
            'slowest_queries': query_stats['top_slow_queries'],
            'issues': issues,
            'timestamp': datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }

# Flask CLI commands for database management
def register_database_commands(app):
    """Register database management CLI commands"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('db-stats')
    @with_appcontext
    def database_stats():
        """Show database connection pool statistics"""
        stats = db_connection_manager.get_pool_statistics()
        click.echo("Database Connection Pool Statistics:")
        click.echo(f"  Connections made: {stats.get('connections_made', 0)}")
        click.echo(f"  Connections closed: {stats.get('connections_closed', 0)}")
        click.echo(f"  Checkouts: {stats.get('checkouts', 0)}")
        click.echo(f"  Checkins: {stats.get('checkins', 0)}")
        click.echo(f"  Average checkout time: {stats.get('avg_checkout_time', 0):.3f}s")
        click.echo(f"  Queries executed: {stats.get('queries_executed', 0)}")
        click.echo(f"  Average query time: {stats.get('avg_query_time', 0):.3f}s")
    
    @app.cli.command('db-health')
    @with_appcontext
    def database_health():
        """Check database health status"""
        health = get_database_health()
        click.echo(f"Database Status: {health['status']}")
        if health['status'] != 'healthy':
            click.echo("Issues found:")
            for issue in health.get('issues', []):
                click.echo(f"  - {issue}")
    
    @app.cli.command('db-reset-stats')
    @with_appcontext
    def reset_stats():
        """Reset database statistics"""
        db_connection_manager.reset_statistics()
        click.echo("Database statistics reset successfully")