"""
Database query optimization utilities for the profi_test application
"""
from sqlalchemy.orm import joinedload, selectinload, defer, undefer
from sqlalchemy import desc, asc, func, and_, or_
from app import db
from app.models import (
    User, TestResult, TestQuestion, Notification, Comment, 
    Rating, UserProgress, UserPreference, Feedback, ABTest, 
    ABTestResult, CareerGoal, LearningPath, CalendarEvent, PortfolioProject
)
import logging
from typing import List, Dict, Any, Optional
from functools import wraps
from time import time


logger = logging.getLogger(__name__)


class QueryOptimizer:
    """Advanced query optimization utilities"""
    
    @staticmethod
    def optimize_user_query(include_relationships: List[str] = None, defer_fields: List[str] = None):
        """
        Create optimized query for User model with selective loading
        
        Args:
            include_relationships: List of relationships to eagerly load
            defer_fields: List of fields to defer loading
        """
        query = db.session.query(User)
        
        if include_relationships:
            for rel in include_relationships:
                try:
                    query = query.options(selectinload(getattr(User, rel)))
                except AttributeError:
                    logger.warning(f"Relationship {rel} not found on User model")
        
        if defer_fields:
            for field in defer_fields:
                try:
                    query = query.defer(getattr(User, field))
                except AttributeError:
                    logger.warning(f"Field {field} not found on User model")
        
        return query
    
    @staticmethod
    def optimize_test_result_query(user_id: int = None, methodology: str = None, 
                                 include_user: bool = True, include_comments: bool = False,
                                 include_ratings: bool = False, limit: int = 50):
        """
        Create optimized query for TestResult model
        
        Args:
            user_id: Filter by user ID
            methodology: Filter by methodology
            include_user: Whether to include user relationship
            include_comments: Whether to include comments relationship
            include_ratings: Whether to include ratings relationship
            limit: Limit number of results
        """
        query = db.session.query(TestResult)
        
        # Apply filters
        if user_id:
            query = query.filter(TestResult.user_id == user_id)
        
        if methodology:
            query = query.filter(TestResult.methodology == methodology)
        
        # Apply eager loading based on requirements
        if include_user:
            query = query.options(selectinload(TestResult.user))
        
        if include_comments:
            query = query.options(selectinload(TestResult.comments))
        
        if include_ratings:
            query = query.options(selectinload(TestResult.ratings))
        
        # Order by creation date descending
        query = query.order_by(desc(TestResult.created_at))
        
        # Apply limit
        if limit:
            query = query.limit(limit)
        
        return query
    
    @staticmethod
    def optimize_notification_query(user_id: int, unread_only: bool = False, 
                                  notification_type: str = None, limit: int = 50):
        """
        Create optimized query for Notification model
        
        Args:
            user_id: Filter by user ID
            unread_only: Filter for unread notifications only
            notification_type: Filter by notification type
            limit: Limit number of results
        """
        query = db.session.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.is_read == False)
        
        if notification_type:
            query = query.filter(Notification.type == notification_type)
        
        query = query.order_by(desc(Notification.created_at))
        
        if limit:
            query = query.limit(limit)
        
        return query
    
    @staticmethod
    def get_user_with_recent_results(user_id: int, result_limit: int = 10):
        """
        Get user with their recent test results efficiently
        """
        return (db.session.query(User)
                .filter(User.id == user_id)
                .options(selectinload(User.test_results)
                         .joinedload(TestResult.user))
                .options(defer(User.password_hash))  # Don't load password hash unnecessarily
                .first())
    
    @staticmethod
    def get_test_results_with_details(user_id: int, methodologies: List[str] = None):
        """
        Get test results with related data efficiently
        """
        query = (db.session.query(TestResult)
                 .filter(TestResult.user_id == user_id))
        
        if methodologies:
            query = query.filter(TestResult.methodology.in_(methodologies))
        
        # Eagerly load related data
        query = (query
                 .options(selectinload(TestResult.user))
                 .options(selectinload(TestResult.comments))
                 .options(selectinload(TestResult.ratings))
                 .order_by(desc(TestResult.created_at)))
        
        return query.all()
    
    @staticmethod
    def get_paginated_results(model, page: int = 1, per_page: int = 20, 
                           filters: Dict[str, Any] = None, order_by_field = None):
        """
        Get paginated results with filters applied
        
        Args:
            model: SQLAlchemy model class
            page: Page number (1-indexed)
            per_page: Number of items per page
            filters: Dictionary of filters to apply
            order_by_field: Field to order by (desc)
        """
        query = db.session.query(model)
        
        # Apply filters
        if filters:
            for field, value in filters.items():
                try:
                    attr = getattr(model, field)
                    if isinstance(value, list):
                        query = query.filter(attr.in_(value))
                    else:
                        query = query.filter(attr == value)
                except AttributeError:
                    logger.warning(f"Field {field} not found on model {model.__name__}")
        
        # Apply ordering
        if order_by_field:
            try:
                query = query.order_by(desc(getattr(model, order_by_field)))
            except AttributeError:
                logger.warning(f"Order by field {order_by_field} not found on model {model.__name__}")
        
        # Apply pagination
        offset = (page - 1) * per_page
        paginated_query = query.offset(offset).limit(per_page)
        
        return {
            'items': paginated_query.all(),
            'total': query.count(),
            'page': page,
            'per_page': per_page,
            'pages': (query.count() + per_page - 1) // per_page
        }


def measure_query_time(func):
    """Decorator to measure query execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        
        execution_time = end_time - start_time
        logger.info(f"Query '{func.__name__}' executed in {execution_time:.4f}s")
        
        # Log slow queries
        if execution_time > 0.5:  # Log queries taking more than 0.5 seconds
            logger.warning(f"SLOW QUERY: '{func.__name__}' took {execution_time:.4f}s")
        
        return result
    return wrapper


class BulkOperations:
    """Utilities for bulk database operations"""
    
    @staticmethod
    def bulk_insert_or_update(model_class, data_list: List[Dict], 
                            unique_fields: List[str], update_fields: List[str]):
        """
        Perform bulk insert or update operation
        
        Args:
            model_class: SQLAlchemy model class
            data_list: List of dictionaries containing data to insert/update
            unique_fields: Fields that define uniqueness
            update_fields: Fields to update if record exists
        """
        try:
            # For SQLite, we'll use a more efficient approach
            for data in data_list:
                # Build the filter condition
                filter_condition = and_(*[
                    getattr(model_class, field) == data[field] 
                    for field in unique_fields
                ])
                
                # Try to find existing record
                existing_record = db.session.query(model_class).filter(filter_condition).first()
                
                if existing_record:
                    # Update existing record
                    for field in update_fields:
                        if field in data:
                            setattr(existing_record, field, data[field])
                else:
                    # Create new record
                    new_record = model_class(**{k: v for k, v in data.items() 
                                              if k in [col.name for col in model_class.__table__.columns]})
                    db.session.add(new_record)
            
            db.session.commit()
            logger.info(f"Bulk operation completed for {len(data_list)} records")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Bulk operation failed: {e}")
            raise
    
    @staticmethod
    def bulk_delete(model_class, filters: Dict[str, Any]):
        """
        Perform bulk delete operation
        
        Args:
            model_class: SQLAlchemy model class
            filters: Dictionary of filters to determine which records to delete
        """
        try:
            query = db.session.query(model_class)
            
            for field, value in filters.items():
                try:
                    attr = getattr(model_class, field)
                    if isinstance(value, list):
                        query = query.filter(attr.in_(value))
                    else:
                        query = query.filter(attr == value)
                except AttributeError:
                    logger.warning(f"Field {field} not found on model {model_class.__name__}")
            
            deleted_count = query.delete(synchronize_session=False)
            db.session.commit()
            
            logger.info(f"Bulk delete completed: {deleted_count} records deleted")
            return deleted_count
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Bulk delete failed: {e}")
            raise


def create_indexes_if_not_exists():
    """Create database indexes if they don't exist"""
    from sqlalchemy import text
    
    try:
        # Create indexes for frequently queried columns
        indexes_to_create = [
            "CREATE INDEX IF NOT EXISTS idx_user_username ON user (username)",
            "CREATE INDEX IF NOT EXISTS idx_user_email ON user (email)",
            "CREATE INDEX IF NOT EXISTS idx_test_result_user_id ON test_result (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_test_result_methodology ON test_result (methodology)",
            "CREATE INDEX IF NOT EXISTS idx_test_result_created_at ON test_result (created_at)",
            "CREATE INDEX IF NOT EXISTS idx_notification_user_id ON notification (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_notification_is_read ON notification (is_read)",
            "CREATE INDEX IF NOT EXISTS idx_comment_test_result_id ON comment (test_result_id)",
            "CREATE INDEX IF NOT EXISTS idx_rating_user_id ON rating (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_progress (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_feedback_user_id ON feedback (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_career_goal_user_id ON career_goal (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_learning_path_user_id ON learning_path (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_calendar_event_user_id ON calendar_event (user_id)",
            "CREATE INDEX IF NOT EXISTS idx_portfolio_project_user_id ON portfolio_project (user_id)",
        ]
        
        for index_sql in indexes_to_create:
            db.session.execute(text(index_sql))
        
        db.session.commit()
        logger.info("Database indexes created/verified successfully")
        
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
        db.session.rollback()


def optimize_database_for_production():
    """Apply database optimizations for production use"""
    from sqlalchemy import text
    
    try:
        # Apply SQLite optimizations if using SQLite
        if 'sqlite' in db.engine.url.drivername:
            optimizations = [
                "PRAGMA journal_mode = WAL;",  # Better concurrency
                "PRAGMA synchronous = NORMAL;",  # Better performance
                "PRAGMA cache_size = 10000;",  # Increase cache size
                "PRAGMA temp_store = MEMORY;",  # Store temp tables in memory
                "PRAGMA mmap_size = 268435456;",  # 256MB memory mapping
            ]
            
            for opt in optimizations:
                db.session.execute(text(opt))
        
        db.session.commit()
        logger.info("Database optimizations applied")
        
    except Exception as e:
        logger.error(f"Error applying database optimizations: {e}")
        db.session.rollback()


# Predefined optimized queries for common use cases
class OptimizedQueries:
    """Collection of commonly used optimized queries"""
    
    @staticmethod
    @measure_query_time
    def get_user_profile_data(user_id: int):
        """Get user profile data with related information"""
        return (db.session.query(User)
                .filter(User.id == user_id)
                .options(selectinload(User.test_results))
                .options(selectinload(User.notifications))
                .options(selectinload(User.progress_records))
                .options(defer(User.password_hash))  # Don't load password unnecessarily
                .first())
    
    @staticmethod
    @measure_query_time
    def get_user_test_results_summary(user_id: int):
        """Get summary of user's test results"""
        return (db.session.query(
                    func.count(TestResult.id).label('total_tests'),
                    func.max(TestResult.created_at).label('last_test_date'),
                    func.count(func.distinct(TestResult.methodology)).label('different_methods')
                )
                .filter(TestResult.user_id == user_id)
                .first())
    
    @staticmethod
    @measure_query_time
    def get_recent_notifications(user_id: int, limit: int = 10):
        """Get recent notifications for a user"""
        return (db.session.query(Notification)
                .filter(Notification.user_id == user_id)
                .order_by(desc(Notification.created_at))
                .limit(limit)
                .all())
    
    @staticmethod
    @measure_query_time
    def get_user_career_goals(user_id: int):
        """Get career goals for a user with related learning paths"""
        return (db.session.query(CareerGoal)
                .filter(CareerGoal.user_id == user_id)
                .options(selectinload(CareerGoal.learning_paths))
                .order_by(asc(CareerGoal.priority), desc(CareerGoal.created_at))
                .all())


# Initialize optimizations when module is imported
def init_optimizations():
    """Initialize database optimizations"""
    create_indexes_if_not_exists()
    optimize_database_for_production()


# Call initialization
init_optimizations()