from flask import Flask, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect, generate_csrf

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_name='default'):
    import logging
    # Initialize logging before anything else
    try:
        from app.utils.logger import setup_logging, RequestLogger
        setup_logging(app_name='chess_calendar', json_logs=True)
        logger = logging.getLogger('chess_calendar')
    except Exception as e:
        logging.warning(f"Failed to initialize advanced logging: {e}")
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
    
    logger.info("Starting application initialization")
    
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static',
                static_url_path='/static')
    
    # Initialize rate limiter with proper storage
    # Try to use Redis, but fallback to in-memory if not available
    try:
        import redis
        redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/1')
        # Test Redis connection
        r = redis.from_url(redis_url)
        r.ping()
        # Redis is available, use it
        limiter = Limiter(
            key_func=get_remote_address,
            default_limits=["1000 per day", "100 per hour"],
            storage_uri=redis_url
        )
        logger.info(f"Rate limiter initialized with Redis: {redis_url}")
    except Exception as e:
        logger.warning(f"Redis not available for rate limiting, using in-memory storage: {e}")
        # Fallback to in-memory storage for development
        limiter = Limiter(
            key_func=get_remote_address,
            default_limits=["1000 per day", "100 per hour"]
        )
    limiter.init_app(app)
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    # Exempt API routes from CSRF protection
    # API routes should use token-based authentication instead
    @csrf.exempt
    def csrf_exempt_api():
        """Exempt API routes from CSRF"""
        return request.path.startswith('/api/') or request.path.startswith('/auth/')
    
    # Загрузка конфигурации
    app.config.from_object('config.config.Config')
    
    # Configure connection pooling using our optimization utilities
    from app.utils.db_optimization import QueryOptimizer
    QueryOptimizer.enable_connection_pooling(app, pool_size=20, max_overflow=40)
    
    # Инициализация расширений
    db.init_app(app)
    
    # Регистрация обработчиков ошибок
    try:
        from app.utils.error_handler import register_error_handlers
        register_error_handlers(app)
        logger.info("Error handlers registered")
    except Exception as e:
        logger.warning(f"Failed to register error handlers: {e}")
    
    # Initialize monitoring middleware (v4.0)
    try:
        from app.middleware.monitoring_middleware import monitoring_middleware
        monitoring_middleware.init_app(app)
        logger.info("Monitoring middleware initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize monitoring middleware: {e}")
    
    # Initialize predictive cache (v4.0)
    try:
        from app.utils.predictive_cache import create_predictive_cache
        global predictive_cache
        predictive_cache = create_predictive_cache()
        logger.info("Predictive cache initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize predictive cache: {e}")

    
    # Initialize security middleware
    try:
        from app.middleware.security_middleware import security_middleware
        security_middleware.init_app(app)
        logger.info("Security middleware initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize security middleware: {e}")
    
    # Initialize email notification service
    try:
        from app.utils.email_notifications import email_service
        email_service.init_app(app)
        logger.info("Email notification service initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize email service: {e}")
    
    # Initialize metrics middleware
    try:
        from app.utils.metrics import MetricsMiddleware
        metrics_middleware = MetricsMiddleware(app)
        logger.info("Metrics middleware initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize metrics: {e}")
    
    # Initialize request logger
    try:
        from app.utils.logger import RequestLogger
        request_logger = RequestLogger(app)
        logger.info("Request logger initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize request logger: {e}")
    
    # Initialize scheduler
    try:
        from app.utils.scheduler import scheduler_service
        logger.info("Scheduler initialized")
    except ImportError:
        logger.warning("Scheduler module not available")
    
    # Initialize i18n
    try:
        from app.utils.i18n import translation_manager
        logger.info("Internationalization initialized")
    except Exception as e:
        logger.warning(f"Failed to initialize i18n: {e}")
    
    # Initialize WebSocket handlers
    try:
        from app.websocket_handlers import init_websocket_handlers
        socketio = init_websocket_handlers(app)
        logger.info("WebSocket handlers initialized")
    except ImportError:
        logger.warning("WebSocket handlers module not available")
    
    # Создание таблиц и автоматическая инициализация БД
    with app.app_context():
        db.create_all()
        
        # Автоматическая инициализация и проверка базы данных
        try:
            from app.utils.db_init import init_database
            db_initialized = init_database(app, db)
            if not db_initialized:
                logger.error("Failed to initialize database! Application may not work correctly.")
        except Exception as e:
            logger.error(f"Critical error during database initialization: {e}")
            import traceback
            traceback.print_exc()
        
        # Инициализация health check системы
        try:
            from app.utils.health_check import init_health_check
            init_health_check(app, db)
            logger.info("Health check system initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize health check: {e}")
    
    # Дополнительные статические маршруты для PWA
    @app.route('/favicon.ico')
    def favicon():
        import os
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        return send_from_directory(static_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    @app.route('/robots.txt')
    def robots():
        import os
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        return send_from_directory(static_dir, 'robots.txt', mimetype='text/plain')
    
    # PWA маршруты
    @app.route('/sw.js')
    def service_worker():
        import os
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        return send_from_directory(static_dir, 'sw.js', mimetype='application/javascript')
    
    @app.route('/manifest.json')
    def manifest():
        import os
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        return send_from_directory(static_dir, 'manifest.json', mimetype='application/json')
    
    # Template globals
    @app.template_global()
    def get_user_by_id(user_id):
        from app.models.user import User
        return User.query.get(user_id)
    
    @app.template_global()
    def now():
        from datetime import datetime
        return datetime.now()
    
    @app.template_global()
    def csrf_token():
        """Generate CSRF token for templates"""
        return generate_csrf()
    
    # Jinja2 filters
    @app.template_filter('format_date')
    def format_date_filter(date_obj):
        """Format date object to string"""
        if not date_obj:
            return ''
        if isinstance(date_obj, str):
            from datetime import datetime
            try:
                date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return date_obj
        return date_obj.strftime('%d.%m.%Y')
    
    @app.template_filter('format_day')
    def format_day_filter(date_obj):
        """Format date to day number"""
        if not date_obj:
            return ''
        if isinstance(date_obj, str):
            from datetime import datetime
            try:
                date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return ''
        return date_obj.strftime('%d')
    
    @app.template_filter('format_month')
    def format_month_filter(date_obj):
        """Format date to month name"""
        if not date_obj:
            return ''
        if isinstance(date_obj, str):
            from datetime import datetime
            try:
                date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                return ''
        months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 
                  'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
        return months[date_obj.month - 1]
    
    # Security headers
    @app.after_request
    def after_request(response):
        from app.utils.security import apply_security_headers
        response = apply_security_headers(response)
        response.headers['X-Permitted-Cross-Domain-Policies'] = 'none'
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    # Регистрация blueprint'ов
    from app.views.main import main_bp
    from app.views.admin import admin_bp
    from app.views.user import user_bp
    from app.views.api_docs import api_docs_bp
    from app.views.forum import forum_bp
    from app.views.api import api_bp
    from app.views.health import health_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(api_docs_bp)
    
    # Register monitoring API (v4.0)
    try:
        from app.views.monitoring import monitoring_bp
        app.register_blueprint(monitoring_bp)
        logger.info("Monitoring API registered")
    except Exception as e:
        logger.warning(f"Failed to register monitoring API: {e}")
    
    # Register new API blueprints
    try:
        from app.api.users import users_api
        app.register_blueprint(users_api)
        logger.info("Users API registered")
    except Exception as e:
        logger.warning(f"Failed to register users API: {e}")
    
    # Prometheus metrics endpoint
    @app.route('/metrics')
    def metrics():
        """Prometheus metrics endpoint"""
        try:
            from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
            from app.utils.metrics import update_business_metrics
            
            # Update business metrics before exposing
            update_business_metrics()
            
            return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
        except Exception as e:
            logger.error(f"Error generating metrics: {e}")
            return 'Metrics unavailable', 500
    
    return app