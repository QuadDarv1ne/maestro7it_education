"""
Application startup optimization module
"""
import time
import logging
from functools import wraps
from threading import Thread
import importlib
from app import db
from app.models import User, TestResult, Notification


logger = logging.getLogger(__name__)


class StartupOptimizer:
    """Optimizes application startup time by deferring non-critical initializations"""
    
    def __init__(self):
        self.initialized_components = set()
        self.deferred_initializations = []
        self.startup_time_log = {}
    
    def measure_startup_step(self, step_name):
        """Decorator to measure startup time for specific initialization steps"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                
                elapsed = end_time - start_time
                self.startup_time_log[step_name] = elapsed
                logger.info(f"Startup step '{step_name}' took {elapsed:.4f}s")
                
                return result
            return wrapper
        return decorator
    
    def deferred_init(self, component_name):
        """Decorator to mark initialization functions for deferred execution"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Check if we should execute immediately or defer
                if self.should_execute_immediately(component_name):
                    return func(*args, **kwargs)
                else:
                    # Schedule for deferred execution
                    self.deferred_initializations.append({
                        'func': func,
                        'args': args,
                        'kwargs': kwargs,
                        'component_name': component_name
                    })
                    logger.debug(f"Deferred initialization scheduled for {component_name}")
                    return None
            return wrapper
        return decorator
    
    def should_execute_immediately(self, component_name):
        """Determine if a component should be initialized immediately or deferred"""
        # Critical components that must be initialized immediately
        critical_components = {
            'database',
            'security',
            'authentication',
            'basic_routes'
        }
        
        return component_name in critical_components
    
    def execute_deferred_initializations(self):
        """Execute all deferred initializations in background"""
        def run_deferred():
            logger.info(f"Starting {len(self.deferred_initializations)} deferred initializations...")
            start_time = time.time()
            
            for init_data in self.deferred_initializations:
                try:
                    func = init_data['func']
                    args = init_data['args']
                    kwargs = init_data['kwargs']
                    component_name = init_data['component_name']
                    
                    logger.debug(f"Executing deferred initialization for {component_name}")
                    func(*args, **kwargs)
                    self.initialized_components.add(component_name)
                    
                except Exception as e:
                    logger.error(f"Error in deferred initialization for {component_name}: {e}")
            
            end_time = time.time()
            total_time = end_time - start_time
            logger.info(f"Completed {len(self.deferred_initializations)} deferred initializations in {total_time:.4f}s")
        
        # Run in a separate thread to not block the main startup
        thread = Thread(target=run_deferred, daemon=True)
        thread.start()
        
        return thread
    
    def preload_frequently_used_data(self, app):
        """Preload data that is frequently accessed to reduce runtime queries"""
        def preload():
            start_time = time.time()
            logger.info("Preloading frequently used data...")
            
            try:
                with app.app_context():
                    # Preload common user counts
                    user_count = db.session.query(User.id).count()
                    test_result_count = db.session.query(TestResult.id).count()
                    notification_count = db.session.query(Notification.id).count()
                    
                    logger.info(f"Preloaded: {user_count} users, {test_result_count} test results, {notification_count} notifications")
                    
                    # You could also preload other frequently accessed data here
                    # For example: common configurations, cached reports, etc.
                    
            except Exception as e:
                logger.error(f"Error during data preloading: {e}")
            
            end_time = time.time()
            logger.info(f"Data preloading completed in {end_time - start_time:.4f}s")
        
        # Run in background to not block startup
        thread = Thread(target=preload, daemon=True)
        thread.start()
        
        return thread
    
    def optimize_query_cache(self, app):
        """Optimize database query cache with commonly used queries"""
        def optimize():
            start_time = time.time()
            logger.info("Optimizing query cache with commonly used queries...")
            
            try:
                with app.app_context():
                    # Pre-cache common queries that are known to be used frequently
                    from app.models import User, TestResult
                    
                    # Cache the most common query patterns
                    # This will be implemented by caching the results in Redis
                    if hasattr(app, 'cache'):
                        # Cache user statistics
                        user_stats = {
                            'total_users': db.session.query(User).count(),
                            'users_with_tests': db.session.query(User.id)
                                .join(TestResult).distinct().count(),
                        }
                        app.cache.set('startup_user_stats', user_stats, timeout=3600)
                        
                        # Cache recent test results count
                        recent_tests = db.session.query(TestResult).count()
                        app.cache.set('startup_recent_tests_count', recent_tests, timeout=1800)
                        
                        logger.info(f'Cached user stats: {user_stats}')
                    else:
                        logger.warning('Cache not available for query optimization')
                        
            except Exception as e:
                logger.error(f'Error during query cache optimization: {e}')
            
            end_time = time.time()
            logger.info(f'Query cache optimization completed in {end_time - start_time:.4f}s')
        
        # Run in background to not block startup
        thread = Thread(target=optimize, daemon=True)
        thread.start()
    
    def warm_up_endpoints(self, app):
        """Warm up commonly accessed endpoints to prime the cache"""
        def warmup():
            start_time = time.time()
            logger.info("Warming up commonly accessed endpoints...")
            
            try:
                # Simulate requests to common endpoints to prime cache
                # In a real scenario, we'd make actual requests, but for startup,
                # we'll just ensure the routes are loaded
                with app.app_context():
                    # Import common route modules to ensure they're loaded
                    from app import routes
                    from app import test_routes
                    from app import auth
                    
                    # Pre-compile commonly used templates
                    from flask import render_template_string
                    
                    logger.info("Endpoint warm-up completed")
                    
            except Exception as e:
                logger.error(f'Error during endpoint warm-up: {e}')
            
            end_time = time.time()
            logger.info(f'Endpoint warm-up completed in {end_time - start_time:.4f}s')
        
        # Run in background to not block startup
        thread = Thread(target=warmup, daemon=True)
        thread.start()

# Global startup optimizer instance
startup_optimizer = StartupOptimizer()


def optimize_imports():
    """Optimize imports by importing only what's needed initially"""
    # This function can be expanded to handle lazy imports or selective imports
    # For now, it just serves as a placeholder for import optimization strategies
    pass


def lazy_module_loader(module_path):
    """Load modules lazily when needed"""
    def loader():
        return importlib.import_module(module_path)
    return loader


# Example of how to use the optimizer for specific components
@startup_optimizer.measure_startup_step('database_initialization')
def initialize_database_lazy(app):
    """Initialize database with lazy loading where possible"""
    # This would contain database initialization logic
    # that's been measured for startup time
    pass


@startup_optimizer.deferred_init('ml_recommender')
def initialize_ml_recommender_lazy(app):
    """Initialize ML recommender system after startup"""
    # This initialization will be deferred and run in background
    from app.ml_recommendations import recommendation_engine
    recommendation_engine.initialize_models()
    logger.info("ML recommender initialized in background")


@startup_optimizer.deferred_init('telegram_bot')
def initialize_telegram_bot_lazy(app):
    """Initialize Telegram bot after startup"""
    # This initialization will be deferred
    try:
        from app.telegram_bot import start_bot
        start_bot()
        logger.info("Telegram bot started in background")
    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {e}")


def get_startup_performance_report():
    """Get report on startup performance"""
    return {
        'startup_times': startup_optimizer.startup_time_log,
        'initialized_components': list(startup_optimizer.initialized_components),
        'deferred_initializations_count': len(startup_optimizer.deferred_initializations),
        'completed_initializations_count': len(startup_optimizer.initialized_components)
    }


# Example usage in app initialization
def apply_startup_optimizations(app):
    """Apply startup optimizations to the Flask app"""
    logger.info("Applying startup optimizations...")
    
    # Preload frequently used data
    startup_optimizer.preload_frequently_used_data(app)
    
    # Initialize query cache optimization
    startup_optimizer.optimize_query_cache(app)
    
    # Warm up commonly used API endpoints
    startup_optimizer.warm_up_endpoints(app)
    
    # The deferred initializations will be triggered by the calling code
    # after the basic app is ready
    
    logger.info("Startup optimizations applied")