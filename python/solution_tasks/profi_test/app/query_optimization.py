"""
Advanced query optimization with eager loading and performance utilities
"""
import logging
import time
from functools import wraps
from sqlalchemy.orm import joinedload, selectinload, subqueryload
from sqlalchemy import text
from collections import defaultdict
from threading import Lock
from datetime import datetime

logger = logging.getLogger(__name__)

class QueryOptimizer:
    """Advanced query optimization utilities"""
    
    def __init__(self):
        self.optimization_stats = defaultdict(int)
        self.lock = Lock()
    
    def eager_load_relationships(self, query, relationships):
        """
        Apply eager loading to prevent N+1 query problems
        
        Args:
            query: SQLAlchemy query object
            relationships: List of relationship names to eager load
            
        Returns:
            Optimized query with eager loading
        """
        if not relationships:
            return query
        
        # Choose loading strategy based on relationship type and size
        for relationship in relationships:
            # For small related collections, use joinedload
            if relationship in ['user', 'test_result', 'comment']:
                query = query.options(joinedload(relationship))
            # For larger collections, use selectinload
            elif relationship in ['test_results', 'comments', 'ratings', 'notifications']:
                query = query.options(selectinload(relationship))
            # For complex nested relationships, use subqueryload
            else:
                query = query.options(subqueryload(relationship))
        
        with self.lock:
            self.optimization_stats['eager_loads_applied'] += 1
        
        return query
    
    def optimize_pagination(self, query, page, per_page, max_per_page=100):
        """
        Optimize paginated queries with proper indexing and limits
        
        Args:
            query: SQLAlchemy query object
            page: Page number (1-based)
            per_page: Items per page
            max_per_page: Maximum allowed items per page
            
        Returns:
            Paginated query with optimizations
        """
        # Validate and limit page size
        per_page = min(per_page, max_per_page)
        page = max(1, page)
        
        # Apply pagination with offset optimization
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)
        
        with self.lock:
            self.optimization_stats['paginated_queries'] += 1
        
        return query, per_page, page
    
    def add_query_hints(self, query, hints):
        """
        Add database-specific query hints for optimization
        
        Args:
            query: SQLAlchemy query object
            hints: List of query hints
            
        Returns:
            Query with hints applied
        """
        if not hints:
            return query
        
        # Apply hints based on database type
        for hint in hints:
            try:
                if 'USE INDEX' in hint:
                    # MySQL/PostgreSQL index hints
                    query = query.execution_options(mysql hints=[hint])
                elif 'INDEX' in hint:
                    # Generic index hint
                    query = query.execution_options(index_hint=hint)
            except Exception as e:
                logger.warning(f"Failed to apply query hint '{hint}': {e}")
        
        with self.lock:
            self.optimization_stats['hints_applied'] += len(hints)
        
        return query
    
    def batch_load_objects(self, model_class, ids, batch_size=100):
        """
        Efficiently load objects by ID in batches to prevent memory issues
        
        Args:
            model_class: SQLAlchemy model class
            ids: List of IDs to load
            batch_size: Size of each batch
            
        Returns:
            Generator yielding objects in batches
        """
        from app import db
        
        for i in range(0, len(ids), batch_size):
            batch_ids = ids[i:i + batch_size]
            batch = db.session.query(model_class).filter(
                model_class.id.in_(batch_ids)
            ).all()
            
            with self.lock:
                self.optimization_stats['batch_loads'] += 1
                self.optimization_stats['objects_loaded'] += len(batch)
            
            yield batch
    
    def get_optimization_statistics(self):
        """Get query optimization statistics"""
        with self.lock:
            return dict(self.optimization_stats)

# Global query optimizer instance
query_optimizer = QueryOptimizer()

def optimized_query(relationships=None, page=None, per_page=None, hints=None):
    """
    Decorator for optimizing database queries
    
    Args:
        relationships: List of relationships to eager load
        page: Page number for pagination
        per_page: Items per page
        hints: Database query hints
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute the original query
            result = func(*args, **kwargs)
            
            # Apply optimizations if result is a query
            if hasattr(result, 'options'):
                # Apply eager loading
                if relationships:
                    result = query_optimizer.eager_load_relationships(result, relationships)
                
                # Apply pagination
                if page is not None and per_page is not None:
                    result, actual_per_page, actual_page = query_optimizer.optimize_pagination(
                        result, page, per_page
                    )
                    # Store pagination info in kwargs for later use
                    kwargs['_pagination_info'] = {
                        'page': actual_page,
                        'per_page': actual_per_page
                    }
                
                # Apply query hints
                if hints:
                    result = query_optimizer.add_query_hints(result, hints)
            
            return result
        return wrapper
    return decorator

class OptimizedQuery:
    """Helper class for building optimized queries"""
    
    def __init__(self, model, session):
        self.model = model
        self.session = session
        self.query = session.query(model)
        self._relationships = []
        self._columns = None
        self._filters = []
        self._order_by = []
        self._limit = None
        self._offset = None
        self._hints = []
    
    def with_relationships(self, *relationships):
        """Add eager loading for relationships"""
        self._relationships.extend(relationships)
        return self
    
    def with_columns(self, *columns):
        """Select only specific columns"""
        self._columns = columns
        return self
    
    def filter_by(self, **kwargs):
        """Add filter conditions"""
        self._filters.append(kwargs)
        return self
    
    def order_by(self, *columns):
        """Add ordering"""
        self._order_by.extend(columns)
        return self
    
    def limit(self, limit_value):
        """Add limit"""
        self._limit = limit_value
        return self
    
    def offset(self, offset_value):
        """Add offset"""
        self._offset = offset_value
        return self
    
    def with_hints(self, *hints):
        """Add query hints"""
        self._hints.extend(hints)
        return self
    
    def all(self):
        """Execute query and return all results"""
        query = self._build_query()
        return query.all()
    
    def first(self):
        """Execute query and return first result"""
        query = self._build_query()
        return query.first()
    
    def count(self):
        """Execute query and count results"""
        # For count, we don't need eager loading or specific columns
        query = self.session.query(self.model)
        for filter_dict in self._filters:
            query = query.filter_by(**filter_dict)
        return query.count()
    
    def paginate(self, page, per_page, error_out=True):
        """Execute paginated query"""
        query = self._build_query()
        
        # Apply pagination
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        
        # Get total count
        total = self.count()
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    
    def _build_query(self):
        """Build the optimized query"""
        query = self.query
        
        # Apply column selection
        if self._columns:
            query = query.with_entities(*self._columns)
        
        # Apply filters
        for filter_dict in self._filters:
            query = query.filter_by(**filter_dict)
        
        # Apply eager loading
        if self._relationships:
            query = query_optimizer.eager_load_relationships(query, self._relationships)
        
        # Apply ordering
        if self._order_by:
            query = query.order_by(*self._order_by)
        
        # Apply limit and offset
        if self._limit:
            query = query.limit(self._limit)
        if self._offset:
            query = query.offset(self._offset)
        
        # Apply hints
        if self._hints:
            query = query_optimizer.add_query_hints(query, self._hints)
        
        return query

def create_optimized_query(model, session):
    """Factory function for creating optimized queries"""
    return OptimizedQuery(model, session)

def analyze_query_performance(query_func, *args, **kwargs):
    """
    Analyze query performance and provide optimization suggestions
    
    Args:
        query_func: Function that executes the query
        *args, **kwargs: Arguments for the query function
        
    Returns:
        Dictionary with performance analysis and suggestions
    """
    start_time = time.time()
    
    try:
        result = query_func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        analysis = {
            'execution_time': execution_time,
            'result_count': len(result) if hasattr(result, '__len__') else 1,
            'suggestions': []
        }
        
        # Performance suggestions based on execution time
        if execution_time > 1.0:
            analysis['suggestions'].append("Query is slow - consider adding indexes")
        elif execution_time > 0.5:
            analysis['suggestions'].append("Query could benefit from optimization")
        
        # Memory usage estimation
        if hasattr(result, '__sizeof__'):
            size_estimate = result.__sizeof__()
            if size_estimate > 10 * 1024 * 1024:  # 10MB
                analysis['suggestions'].append("Large result set - consider pagination")
        
        # Check for N+1 query patterns
        if hasattr(result, '__iter__'):
            # This is a simplified check - in practice, you'd need more sophisticated analysis
            analysis['suggestions'].append("Consider using eager loading for related data")
        
        return analysis
        
    except Exception as e:
        return {
            'error': str(e),
            'execution_time': time.time() - start_time,
            'suggestions': ['Query failed - check syntax and data integrity']
        }

# Predefined optimized query patterns
class QueryPatterns:
    """Common optimized query patterns"""
    
    @staticmethod
    @optimized_query(relationships=['user', 'test_results'])
    def get_user_with_test_history(user_id):
        """Get user with complete test history"""
        from app.models import User
        from app import db
        return db.session.query(User).filter(User.id == user_id)
    
    @staticmethod
    @optimized_query(relationships=['comments', 'ratings'])
    def get_test_result_with_feedback(test_result_id):
        """Get test result with all comments and ratings"""
        from app.models import TestResult
        from app import db
        return db.session.query(TestResult).filter(TestResult.id == test_result_id)
    
    @staticmethod
    @optimized_query(page=1, per_page=20)
    def get_recent_test_results():
        """Get recent test results with pagination"""
        from app.models import TestResult
        from app import db
        return db.session.query(TestResult).order_by(TestResult.created_at.desc())
    
    @staticmethod
    def get_users_with_preferences():
        """Get users with their preferences using batch loading"""
        from app.models import User, UserPreference
        from app import db
        
        # First get all user IDs
        user_ids = db.session.query(User.id).all()
        user_ids = [uid[0] for uid in user_ids]
        
        # Batch load users and preferences
        users = []
        for batch in query_optimizer.batch_load_objects(User, user_ids, batch_size=50):
            # Load preferences for this batch
            user_dict = {user.id: user for user in batch}
            preference_ids = [user.id for user in batch]
            preferences = db.session.query(UserPreference).filter(
                UserPreference.user_id.in_(preference_ids)
            ).all()
            
            # Attach preferences to users
            for pref in preferences:
                if pref.user_id in user_dict:
                    user_dict[pref.user_id].preference = pref
            
            users.extend(batch)
        
        return users

def get_query_optimization_report():
    """Get comprehensive query optimization report"""
    stats = query_optimizer.get_optimization_statistics()
    
    return {
        'statistics': stats,
        'patterns_used': {
            'eager_loading': QueryPatterns.get_user_with_test_history,
            'pagination': QueryPatterns.get_recent_test_results,
            'batch_loading': QueryPatterns.get_users_with_preferences
        },
        'timestamp': datetime.utcnow().isoformat()
    }