from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from instance.config import Config
import logging
from logging.handlers import RotatingFileHandler
import os
from sqlalchemy import event
from sqlalchemy.pool import Pool

# Set up logging
logger = logging.getLogger(__name__)

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
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
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # type: ignore
    
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
    except Exception as e:
        logger.error(f"Error registering blueprints: {str(e)}")
    
    # Обработка ошибок
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"404 error: {str(error)}")
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 error: {str(error)}")
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    return app