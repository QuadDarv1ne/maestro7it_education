"""
Database optimization and indexing strategies for improved performance
"""
import logging
from sqlalchemy import Index, text
from sqlalchemy.schema import CreateTable
from app import db
from app.models import (
    User, TestResult, TestQuestion, Notification, Comment, 
    Rating, UserProgress, UserPreference, Feedback, ABTest, 
    ABTestResult, CareerGoal, LearningPath, CalendarEvent, PortfolioProject
)

logger = logging.getLogger(__name__)

class DatabaseOptimizer:
    """Database optimization and indexing manager"""
    
    def __init__(self):
        self.indexes = {}
        self.optimizations = []
        
    def create_indexes(self):
        """Create database indexes for improved query performance"""
        
        # User table indexes
        user_indexes = [
            Index('idx_user_username', User.username),
            Index('idx_user_email', User.email),
            Index('idx_user_created_at', User.created_at),
            Index('idx_user_is_admin', User.is_admin),
        ]
        
        # TestResult table indexes
        test_result_indexes = [
            Index('idx_test_result_user_id', TestResult.user_id),
            Index('idx_test_result_methodology', TestResult.methodology),
            Index('idx_test_result_created_at', TestResult.created_at),
            Index('idx_test_result_completed_at', TestResult.completed_at),
            Index('idx_test_result_user_method_created', 
                  TestResult.user_id, TestResult.methodology, TestResult.created_at),
        ]
        
        # TestQuestion table indexes
        test_question_indexes = [
            Index('idx_test_question_methodology', TestQuestion.methodology),
            Index('idx_test_question_number', TestQuestion.question_number),
            Index('idx_test_question_category', TestQuestion.category),
            Index('idx_test_question_method_number', 
                  TestQuestion.methodology, TestQuestion.question_number),
        ]
        
        # Notification table indexes
        notification_indexes = [
            Index('idx_notification_user_id', Notification.user_id),
            Index('idx_notification_is_read', Notification.is_read),
            Index('idx_notification_type', Notification.type),
            Index('idx_notification_created_at', Notification.created_at),
            Index('idx_notification_user_read_created', 
                  Notification.user_id, Notification.is_read, Notification.created_at),
        ]
        
        # Comment table indexes
        comment_indexes = [
            Index('idx_comment_test_result_id', Comment.test_result_id),
            Index('idx_comment_user_id', Comment.user_id),
            Index('idx_comment_created_at', Comment.created_at),
        ]
        
        # Rating table indexes
        rating_indexes = [
            Index('idx_rating_user_id', Rating.user_id),
            Index('idx_rating_test_result_id', Rating.test_result_id),
            Index('idx_rating_comment_id', Rating.comment_id),
            Index('idx_rating_type', Rating.rating_type),
            Index('idx_rating_user_test', Rating.user_id, Rating.test_result_id),
            Index('idx_rating_user_comment', Rating.user_id, Rating.comment_id),
        ]
        
        # UserProgress table indexes
        progress_indexes = [
            Index('idx_progress_user_id', UserProgress.user_id),
            Index('idx_progress_test_result_id', UserProgress.test_result_id),
            Index('idx_progress_created_at', UserProgress.created_at),
        ]
        
        # UserPreference table indexes
        preference_indexes = [
            Index('idx_preference_user_id', UserPreference.user_id),
            Index('idx_preference_alerts_enabled', UserPreference.vacancy_alerts_enabled),
        ]
        
        # Feedback table indexes
        feedback_indexes = [
            Index('idx_feedback_user_id', Feedback.user_id),
            Index('idx_feedback_type', Feedback.feedback_type),
            Index('idx_feedback_is_resolved', Feedback.is_resolved),
            Index('idx_feedback_created_at', Feedback.created_at),
        ]
        
        # ABTest table indexes
        abtest_indexes = [
            Index('idx_abtest_name', ABTest.name),
            Index('idx_abtest_is_active', ABTest.is_active),
            Index('idx_abtest_created_at', ABTest.created_at),
        ]
        
        # ABTestResult table indexes
        abtest_result_indexes = [
            Index('idx_abtest_result_test_id', ABTestResult.ab_test_id),
            Index('idx_abtest_result_user_id', ABTestResult.user_id),
            Index('idx_abtest_result_variant', ABTestResult.assigned_variant),
            Index('idx_abtest_result_created_at', ABTestResult.created_at),
        ]
        
        # CareerGoal table indexes
        career_goal_indexes = [
            Index('idx_career_goal_user_id', CareerGoal.user_id),
            Index('idx_career_goal_status', CareerGoal.current_status),
            Index('idx_career_goal_priority', CareerGoal.priority),
            Index('idx_career_goal_created_at', CareerGoal.created_at),
        ]
        
        # LearningPath table indexes
        learning_path_indexes = [
            Index('idx_learning_path_user_id', LearningPath.user_id),
            Index('idx_learning_path_goal_id', LearningPath.goal_id),
            Index('idx_learning_path_status', LearningPath.status),
            Index('idx_learning_path_created_at', LearningPath.created_at),
        ]
        
        # CalendarEvent table indexes
        calendar_indexes = [
            Index('idx_calendar_user_id', CalendarEvent.user_id),
            Index('idx_calendar_event_type', CalendarEvent.event_type),
            Index('idx_calendar_start_datetime', CalendarEvent.start_datetime),
            Index('idx_calendar_user_start', CalendarEvent.user_id, CalendarEvent.start_datetime),
        ]
        
        # PortfolioProject table indexes
        portfolio_indexes = [
            Index('idx_portfolio_user_id', PortfolioProject.user_id),
            Index('idx_portfolio_status', PortfolioProject.status),
            Index('idx_portfolio_project_type', PortfolioProject.project_type),
            Index('idx_portfolio_created_at', PortfolioProject.created_at),
        ]
        
        # Combine all indexes
        all_indexes = (
            user_indexes + test_result_indexes + test_question_indexes +
            notification_indexes + comment_indexes + rating_indexes +
            progress_indexes + preference_indexes + feedback_indexes +
            abtest_indexes + abtest_result_indexes + career_goal_indexes +
            learning_path_indexes + calendar_indexes + portfolio_indexes
        )
        
        # Create indexes
        created_indexes = []
        failed_indexes = []
        
        for index in all_indexes:
            try:
                index.create(db.engine)
                created_indexes.append(index.name)
                logger.info(f"Created index: {index.name}")
            except Exception as e:
                failed_indexes.append((index.name, str(e)))
                logger.warning(f"Failed to create index {index.name}: {e}")
        
        self.indexes = {
            'created': created_indexes,
            'failed': failed_indexes
        }
        
        return self.indexes
    
    def optimize_queries(self):
        """Apply query optimization strategies"""
        
        optimizations = []
        
        # Enable query cache for frequently used queries
        try:
            db.engine.execute(text("PRAGMA cache_size = 10000"))  # Increase cache size
            optimizations.append("Query cache enabled")
        except Exception as e:
            logger.warning(f"Could not enable query cache: {e}")
        
        # Enable foreign key constraints for data integrity
        try:
            db.engine.execute(text("PRAGMA foreign_keys = ON"))
            optimizations.append("Foreign key constraints enabled")
        except Exception as e:
            logger.warning(f"Could not enable foreign keys: {e}")
        
        # Optimize database storage
        try:
            db.engine.execute(text("PRAGMA optimize"))
            optimizations.append("Database optimized")
        except Exception as e:
            logger.warning(f"Could not optimize database: {e}")
        
        self.optimizations = optimizations
        return optimizations
    
    def get_index_statistics(self):
        """Get database index statistics"""
        try:
            # Get index information from SQLite
            result = db.engine.execute(text("""
                SELECT name, tbl_name, sql 
                FROM sqlite_master 
                WHERE type = 'index' 
                AND name NOT LIKE 'sqlite_%'
                ORDER BY tbl_name, name
            """))
            
            index_stats = []
            for row in result:
                index_stats.append({
                    'name': row[0],
                    'table': row[1],
                    'definition': row[2]
                })
            
            return index_stats
            
        except Exception as e:
            logger.error(f"Error getting index statistics: {e}")
            return []
    
    def analyze_query_performance(self):
        """Analyze and suggest query performance improvements"""
        
        suggestions = []
        
        # Check for missing indexes on foreign keys
        foreign_key_columns = [
            ('test_result', 'user_id'),
            ('notification', 'user_id'),
            ('comment', 'user_id'),
            ('comment', 'test_result_id'),
            ('rating', 'user_id'),
            ('rating', 'test_result_id'),
            ('rating', 'comment_id'),
            ('user_progress', 'user_id'),
            ('user_progress', 'test_result_id'),
            ('user_preference', 'user_id'),
            ('feedback', 'user_id'),
            ('ab_test_result', 'user_id'),
            ('ab_test_result', 'ab_test_id'),
            ('career_goal', 'user_id'),
            ('learning_path', 'user_id'),
            ('learning_path', 'goal_id'),
            ('calendar_event', 'user_id'),
            ('portfolio_project', 'user_id'),
        ]
        
        existing_indexes = set()
        try:
            result = db.engine.execute(text("""
                SELECT name, tbl_name 
                FROM sqlite_master 
                WHERE type = 'index'
            """))
            for row in result:
                existing_indexes.add((row[1], row[0]))
        except Exception as e:
            logger.error(f"Error checking existing indexes: {e}")
        
        # Suggest missing indexes
        for table, column in foreign_key_columns:
            index_name = f"idx_{table}_{column}"
            if (table, index_name) not in existing_indexes:
                suggestions.append(f"Consider adding index on {table}.{column}")
        
        return suggestions

# Global database optimizer instance
db_optimizer = DatabaseOptimizer()

def initialize_database_optimization(app=None):
    """Initialize database optimization when application starts"""
    try:
        logger.info("Initializing database optimization...")
        
        # Only proceed if we're inside an app context
        from flask import current_app
        if app is None:
            try:
                app = current_app._get_current_object()
            except RuntimeError:
                # We're outside of app context, return early
                logger.info("Outside of application context, deferring database optimization")
                return None
        
        # Create indexes
        indexes = db_optimizer.create_indexes()
        logger.info(f"Created {len(indexes['created'])} indexes")
        if indexes['failed']:
            logger.warning(f"Failed to create {len(indexes['failed'])} indexes")
        
        # Apply optimizations
        optimizations = db_optimizer.optimize_queries()
        logger.info(f"Applied {len(optimizations)} optimizations")
        
        # Log statistics
        index_stats = db_optimizer.get_index_statistics()
        logger.info(f"Total indexes in database: {len(index_stats)}")
        
        return {
            'indexes_created': len(indexes['created']),
            'indexes_failed': len(indexes['failed']),
            'optimizations_applied': len(optimizations),
            'total_indexes': len(index_stats)
        }
        
    except Exception as e:
        logger.error(f"Database optimization initialization failed: {e}")
        return None

def get_database_performance_report():
    """Get comprehensive database performance report"""
    try:
        return {
            'index_statistics': db_optimizer.get_index_statistics(),
            'optimization_suggestions': db_optimizer.analyze_query_performance(),
            'current_indexes': db_optimizer.indexes,
            'applied_optimizations': db_optimizer.optimizations
        }
    except Exception as e:
        logger.error(f"Error generating performance report: {e}")
        return None