from flask import Flask, send_from_directory, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect, generate_csrf
import os

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
    
    app = Flask(__name__, template_folder='../templates')
    
    # Initialize rate limiter
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    limiter.init_app(app)
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    # Загрузка конфигурации
    app.config.from_object('config.config.Config')
    
    # Инициализация расширений
    db.init_app(app)
    
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
    
    # Создание таблиц
    with app.app_context():
        db.create_all()
    
    # Статические файлы
    @app.route('/static/<path:filename>')
    def static_files(filename):
        return send_from_directory('static', filename)
    
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
        return send_from_directory('static', 'manifest.json')
    
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
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(forum_bp)
    app.register_blueprint(api_docs_bp)
    
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