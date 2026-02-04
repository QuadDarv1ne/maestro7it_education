"""
Database connection pooling and optimization module
"""
import logging
from sqlalchemy import event
from sqlalchemy.pool import Pool
from flask import current_app
import threading
import time
from collections import defaultdict


class DatabaseConnectionManager:
    """Manages database connection pooling and optimization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.pool_stats = defaultdict(int)
        self.connection_times = []
        self.lock = threading.Lock()
        
    def init_app(self, app):
        """Initialize with Flask app"""
        self.app = app
        
        # Register connection pool event listeners
        @event.listens_for(Pool, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """Set SQLite pragmas for better performance"""
            if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
                cursor = dbapi_connection.cursor()
                # Improve performance with these pragmas
                cursor.execute("PRAGMA journal_mode=WAL")
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.execute("PRAGMA cache_size=10000")
                cursor.execute("PRAGMA temp_store=MEMORY")
                cursor.close()
                
        @event.listens_for(Pool, "checkout")
        def receive_checkout(dbapi_connection, connection_record, connection_proxy):
            """Track connection checkout"""
            with self.lock:
                self.pool_stats['checkouts'] += 1
                self.connection_times.append(time.time())
                
        @event.listens_for(Pool, "checkin")
        def receive_checkin(dbapi_connection, connection_record):
            """Track connection checkin"""
            with self.lock:
                self.pool_stats['checkins'] += 1
                
        @event.listens_for(Pool, "connect")
        def track_connect(dbapi_connection, connection_record):
            """Track new connections"""
            with self.lock:
                self.pool_stats['connects'] += 1
    
    def get_pool_statistics(self):
        """Get current pool statistics"""
        from app import db
        
        with self.lock:
            stats = dict(self.pool_stats)
            
        # Add SQLAlchemy pool-specific stats
        try:
            engine = db.engine
            if hasattr(engine.pool, 'size'):
                stats['pool_size'] = engine.pool.size()
            if hasattr(engine.pool, 'checkedin'):
                stats['checkedin_connections'] = engine.pool.checkedin()
            if hasattr(engine.pool, 'overflow'):
                stats['overflow_connections'] = engine.pool.overflow()
        except Exception as e:
            self.logger.warning(f"Could not get pool statistics: {e}")
            
        return stats
    
    def optimize_connection_settings(self):
        """Apply database-specific optimizations"""
        if self.app and 'sqlite' in self.app.config['SQLALCHEMY_DATABASE_URI']:
            # SQLite-specific optimizations
            from app import db
            
            with db.engine.connect() as conn:
                conn.execute("PRAGMA mmap_size = 268435456")  # 256MB
                conn.execute("PRAGMA read_uncommitted = true")
                conn.execute("PRAGMA threads = 4")
    
    def cleanup_idle_connections(self):
        """Clean up idle connections if needed"""
        # This is a placeholder - actual cleanup depends on the database backend
        pass


class QueryOptimizer:
    """Provides query optimization utilities"""
    
    @staticmethod
    def optimize_query(query, entity_class=None, eager_load_relations=None):
        """
        Optimize query with proper loading strategies
        
        Args:
            query: SQLAlchemy query object
            entity_class: Model class for the query
            eager_load_relations: List of relations to eager load
        """
        from sqlalchemy.orm import selectinload, joinedload
        
        if eager_load_relations and entity_class:
            for relation in eager_load_relations:
                try:
                    # Use selectinload for many-to-one or one-to-many relationships
                    query = query.options(selectinload(getattr(entity_class, relation)))
                except AttributeError:
                    # Fallback to joinedload if selectinload fails
                    query = query.options(joinedload(getattr(entity_class, relation)))
        
        return query
    
    @staticmethod
    def add_query_timeout(query, timeout_seconds=30):
        """Add timeout to query (database-specific)"""
        # This is a simplified implementation - actual timeout handling depends on the database
        return query.execution_options(query_timeout=timeout_seconds)
    
    @staticmethod
    def optimize_pagination(query, page=1, per_page=20, max_per_page=100):
        """Optimize paginated queries"""
        # Limit per_page to prevent abuse
        per_page = min(per_page, max_per_page)
        
        # Calculate offset
        offset = (page - 1) * per_page
        
        # Apply pagination
        paginated_query = query.offset(offset).limit(per_page)
        
        return paginated_query, offset, per_page


# Global connection manager instance
db_connection_manager = DatabaseConnectionManager()


def register_database_commands(app):
    """Register database optimization CLI commands"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('db-optimize')
    @with_appcontext
    def optimize_database():
        """Optimize database connections and settings"""
        db_connection_manager.optimize_connection_settings()
        click.echo("Database connections optimized.")
        
        stats = db_connection_manager.get_pool_statistics()
        click.echo("Current pool statistics:")
        for key, value in stats.items():
            click.echo(f"  {key}: {value}")
    
    @app.cli.command('db-stats')
    @with_appcontext
    def show_db_stats():
        """Show database connection statistics"""
        stats = db_connection_manager.get_pool_statistics()
        click.echo("Database connection statistics:")
        for key, value in stats.items():
            click.echo(f"  {key}: {value}")


def optimize_model_queries(model_class, query_func, *args, **kwargs):
    """
    Generic function to optimize queries for a specific model
    
    Args:
        model_class: SQLAlchemy model class
        query_func: Function that creates the base query
        *args, **kwargs: Arguments for query optimization
    """
    from app import db
    
    # Create base query
    query = query_func()
    
    # Apply common optimizations
    query = db_connection_manager.optimize_query(
        query, 
        entity_class=model_class,
        eager_load_relations=kwargs.get('eager_load', [])
    )
    
    # Apply pagination if requested
    if 'page' in kwargs and 'per_page' in kwargs:
        query, _, _ = QueryOptimizer.optimize_pagination(
            query, 
            page=kwargs['page'], 
            per_page=kwargs['per_page']
        )
    
    return query.all()


def get_optimized_user_query(user_id, include_relationships=None):
    """Get optimized query for user with common relationships"""
    from app import db
    from app.models import User
    
    query = db.session.query(User).filter(User.id == user_id)
    
    if include_relationships is None:
        include_relationships = [
            'test_results',
            'notifications',
            'progress_records'
        ]
    
    return db_connection_manager.optimize_query(
        query,
        entity_class=User,
        eager_load_relations=include_relationships
    ).first()


def get_optimized_test_results_query(user_id, methodology=None, limit=50):
    """Get optimized query for test results"""
    from app import db
    from app.models import TestResult
    
    query = db.session.query(TestResult).filter(TestResult.user_id == user_id)
    
    if methodology:
        query = query.filter(TestResult.methodology == methodology)
    
    # Order by creation date descending
    query = query.order_by(TestResult.created_at.desc())
    
    # Limit results
    query = query.limit(limit)
    
    return db_connection_manager.optimize_query(
        query,
        entity_class=TestResult,
        eager_load_relations=['user']
    ).all()