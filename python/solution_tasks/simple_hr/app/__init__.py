from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_cors import CORS
from instance.config import Config
import logging
from logging.handlers import RotatingFileHandler
import os
from sqlalchemy import event
from sqlalchemy.pool import Pool

# Set up logging
logger = logging.getLogger(__name__)

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)
cache = Cache()

# Import SocketIO (will be initialized later in create_app)
socketio = None

def create_app(config_class=Config):
    global socketio
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    
    # Настройка логирования
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/simple_hr.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Simple HR startup')
    
    # Configure database connection pooling for better performance
    @event.listens_for(Pool, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        try:
            if 'sqlite' in str(type(dbapi_connection)).lower():
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        except Exception as e:
            logger.error(f"Error setting SQLite pragma: {str(e)}")
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # type: ignore
    limiter.init_app(app)
    cache.init_app(app, config={
        'CACHE_TYPE': 'SimpleCache',
        'CACHE_DEFAULT_TIMEOUT': 300
    })
    
    # Настройка CORS с безопасными параметрами
    CORS(app, resources={
        r"/*": {
            "origins": app.config.get('CORS_ORIGINS', ['http://localhost:5000']),
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Настройка безопасных заголовков
    @app.after_request
    def set_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https:;"
        return response
    
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return User.query.get(int(user_id))
        except Exception as e:
            logger.error(f"Error loading user {user_id}: {str(e)}")
            return None
    
    # Регистрация blueprint'ов
    try:
        from app.routes.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
        
        from app.routes.main import bp as main_bp
        app.register_blueprint(main_bp)
        
        from app.routes.employees import bp as employees_bp
        app.register_blueprint(employees_bp, url_prefix='/employees')
        
        from app.routes.departments import bp as departments_bp
        app.register_blueprint(departments_bp, url_prefix='/departments')
        
        from app.routes.positions import bp as positions_bp
        app.register_blueprint(positions_bp, url_prefix='/positions')
        
        from app.routes.orders import bp as orders_bp
        app.register_blueprint(orders_bp, url_prefix='/orders')
        
        from app.routes.vacations import bp as vacations_bp
        app.register_blueprint(vacations_bp, url_prefix='/vacations')
        
        from app.routes.reports import bp as reports_bp
        app.register_blueprint(reports_bp, url_prefix='/reports')
        
        from app.routes.analytics import bp as analytics_bp
        app.register_blueprint(analytics_bp, url_prefix='/analytics')
        
        from app.routes.notifications import bp as notifications_bp
        app.register_blueprint(notifications_bp, url_prefix='/notifications')
        
        from app.routes.admin import bp as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        from app.routes.audit import bp as audit_bp
        app.register_blueprint(audit_bp, url_prefix='/audit')
        
        # Two-Factor Authentication (temporarily disabled - missing qrcode module)
        # from app.routes.two_factor import bp as two_factor_bp
        # app.register_blueprint(two_factor_bp)
        
        # Advanced Search
        from app.routes.search import bp as search_bp
        app.register_blueprint(search_bp)
        
        # Dashboard with Charts
        from app.routes.dashboard import bp as dashboard_bp
        app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
        
        # REST API endpoints
        from app.routes.api import bp as api_bp
        app.register_blueprint(api_bp)
        
        # Health check endpoints
        from app.utils.health import create_health_check_blueprint
        health_bp = create_health_check_blueprint()
        app.register_blueprint(health_bp)
    except Exception as e:
        logger.error(f"Error registering blueprints: {str(e)}")
    
    # Настройка middleware
    try:
        from app.middleware import setup_middleware
        setup_middleware(app)
    except Exception as e:
        logger.error(f"Error setting up middleware: {str(e)}")
    
    # Регистрация CLI команд
    try:
        from app.cli import register_commands
        register_commands(app)
    except Exception as e:
        logger.error(f"Error registering CLI commands: {str(e)}")
    
    # Обработка ошибок
    @app.errorhandler(400)
    def bad_request_error(error):
        logger.warning(f"400 error: {str(error)}")
        return render_template('errors/400.html'), 400
    
    @app.errorhandler(403)
    def forbidden_error(error):
        logger.warning(f"403 error: {str(error)}")
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"404 error: {str(error)}")
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(429)
    def ratelimit_error(error):
        logger.warning(f"429 error: {str(error)}")
        return render_template('errors/429.html'), 429
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {str(error)}")
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Initialize SocketIO with app (temporarily disabled - compatibility issues)
    # from app.utils.websocket import socketio as ws
    # global socketio
    # socketio = ws
    # socketio.init_app(app)
    
    return app