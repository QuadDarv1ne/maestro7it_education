import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

# Initialize cache
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)  # Initialize cache
    
    # Import models after db initialization to avoid circular imports
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Initialize logging system
    from app.logging_system import setup_logging
    setup_logging(app)
    
    # Initialize enhanced structured logging
    from app.structured_logging import structured_logger, register_logging_commands
    structured_logger.init_app(app)
    app.structured_logger = structured_logger
    register_logging_commands(app)
    
    # Initialize performance monitoring
    from app.performance import performance_monitor
    app.performance_monitor = performance_monitor
    
    # Initialize database optimization
    from app.database_optimization import initialize_database_optimization
    initialize_database_optimization(app)
    
    # Initialize database connection pooling
    from app.database_pooling import db_connection_manager, register_database_commands
    db_connection_manager.init_app(app)
    register_database_commands(app)
    
    # Initialize advanced performance monitoring
    from app.performance_monitoring import db_performance_monitor, register_monitoring_commands
    db_performance_monitor.init_app(app)
    register_monitoring_commands(app)
    
    # Initialize enhanced security features
    from app.security_enhanced import security_manager
    security_manager.init_app(app)
    
    # Initialize security audit
    from app.security_audit import security_manager as audit_security_manager
    app.audit_security_manager = audit_security_manager
    
    # Initialize API documentation
    from app.api_docs import init_api_docs
    init_api_docs(app)
    
    # Initialize enhanced ML recommender
    from app.enhanced_ml_recommender import enhanced_ml_recommender_instance
    app.enhanced_ml_recommender = enhanced_ml_recommender_instance
    
    # Initialize advanced analytics
    from app.advanced_analytics import advanced_analytics_instance
    app.advanced_analytics = advanced_analytics_instance
    
    # Initialize user experience manager
    from app.user_experience import ux_manager
    app.ux_manager = ux_manager
    
    # Register blueprints
    from app.routes import main
    from app.auth import auth
    from app.test_routes import test
    from app.admin import admin
    from app.notifications import notifications
    from app.analytics import analytics
    from app.comments import comments
    from app.ratings import ratings
    from app.recommendations import recommendations_bp
    from app.progress import progress_bp
    from app.mobile_api import mobile_api
    from app.market_api import market_api
    from app.reports import reports_bp
    from app.ml_recommender import ml_recommender
    from app.feedback import feedback_bp
    from app.calendar_integration import calendar_bp
    from app.portfolio import portfolio_bp
    from app.telegram_bot import telegram_bot
    from app.monitoring import monitoring
    from app.tasks import task_api
    from app.advanced_api import advanced_api
    from app.ux_api import ux_api
    # api_docs_bp is registered in init_api_docs function
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(test)
    app.register_blueprint(admin)
    app.register_blueprint(notifications)
    app.register_blueprint(analytics)
    app.register_blueprint(comments)
    app.register_blueprint(ratings)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(mobile_api, url_prefix='/api')
    app.register_blueprint(market_api, url_prefix='/api')
    app.register_blueprint(reports_bp, url_prefix='/api')
    app.register_blueprint(ml_recommender, url_prefix='/api')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    app.register_blueprint(calendar_bp, url_prefix='/api')
    app.register_blueprint(portfolio_bp, url_prefix='/api')
    app.register_blueprint(monitoring, url_prefix='/api/monitoring')
    app.register_blueprint(task_api, url_prefix='/api')
    app.register_blueprint(advanced_api, url_prefix='/api/advanced')
    app.register_blueprint(ux_api, url_prefix='/api/ux')
    # api_docs_bp is registered in init_api_docs function

    # Create database tables
    with app.app_context():
        db.create_all()

    # Start vacancy alerts scheduler
    try:
        from app.vacancy_alerts import start_scheduler
        start_scheduler()
    except Exception as e:
        print(f"Ошибка при запуске планировщика уведомлений: {e}")

    # Start ML recommendations scheduler
    try:
        from app.ml_recommendations import generate_ml_notifications
        import schedule
        import threading
        import time
        from datetime import datetime
        
        def run_ml_scheduler():
            # Планируем генерацию ML-рекомендаций раз в день
            schedule.every().day.at("10:00").do(generate_ml_notifications)
            # Также раз в 12 часов
            schedule.every(12).hours.do(generate_ml_notifications)
            
            while True:
                schedule.run_pending()
                time.sleep(60)  # Проверяем каждую минуту
        
        ml_scheduler_thread = threading.Thread(target=run_ml_scheduler, daemon=True)
        ml_scheduler_thread.start()
        
        print(f"[{datetime.now()}] ML-рекомендательная система запущена")
    except Exception as e:
        print(f"Ошибка при запуске ML-рекомендательной системы: {e}")

    return app