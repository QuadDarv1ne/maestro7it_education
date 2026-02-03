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
    """
    Создает и настраивает экземпляр приложения Flask.
    
    Args:
        config_class: Класс конфигурации приложения
        
    Returns:
        app: Настроенный экземпляр Flask-приложения
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)  # Инициализация кэша
    
    # Import models after db initialization to avoid circular imports
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        """
        Загружает пользователя по ID для системы аутентификации.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            User: Объект пользователя
        """
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
    
    # Initialize visualizations
    from app.visualizations import visualizer
    app.visualizer = visualizer
    
    # Initialize enhanced reports
    from app.enhanced_reports import enhanced_reports
    app.enhanced_reports = enhanced_reports
    
    # Initialize advanced notifications
    from app.advanced_notifications import advanced_notifications
    app.advanced_notifications = advanced_notifications
    
    # Initialize data processor
    from app.data_processor import data_processor
    app.data_processor = data_processor
    
    # Initialize advanced cache manager
    from app.advanced_caching import cache_manager
    app.cache_manager = cache_manager
    
    # Initialize system monitor
    from app.system_monitoring import system_monitor
    app.system_monitor = system_monitor
    
    # Initialize error handler
    from app.error_handling import error_handler
    app.error_handler = error_handler
    
    # Initialize config manager
    from app.config_manager import config_manager
    app.config_manager = config_manager
    
    # Initialize task scheduler
    from app.task_scheduler import task_scheduler
    app.task_scheduler = task_scheduler
    task_scheduler.start()  # Автозапуск планировщика
    
    # Initialize security manager
    from app.advanced_security import security_manager
    app.security_manager = security_manager
    
    # Initialize business intelligence engine
    from app.business_intelligence import bi_engine
    app.bi_engine = bi_engine
    
    # Initialize user manager
    from app.user_management import user_manager
    app.user_manager = user_manager
    
    # Initialize content manager
    from app.content_management import content_manager
    app.content_manager = content_manager
    
    # Initialize comment manager
    from app.advanced_comments import comment_manager
    app.comment_manager = comment_manager
    
    # Initialize notification manager
    from app.advanced_notifications import notification_manager
    app.notification_manager = notification_manager
    
    # Initialize rating manager
    from app.advanced_ratings import rating_manager
    app.rating_manager = rating_manager
    
    # Initialize analytics engine
    from app.advanced_analytics import analytics_engine
    app.analytics_engine = analytics_engine
    
    # Initialize ML recommendation engine
    from app.ml_recommendations import recommendation_engine
    app.recommendation_engine = recommendation_engine
    
    # Initialize advanced search engine
    from app.advanced_search import search_engine
    app.search_engine = search_engine
    
    # Initialize enhanced business intelligence engine
    from app.business_intelligence_v2 import bi_engine_v2
    app.bi_engine_v2 = bi_engine_v2
    
    # Initialize advanced content management systems
    from app.content_management_v2 import content_moderation_engine, content_quality_analyzer, content_optimizer
    app.content_moderation_engine = content_moderation_engine
    app.content_quality_analyzer = content_quality_analyzer
    app.content_optimizer = content_optimizer
    
    # Register blueprints
    from app.routes import main
    from app.auth import auth
    from app.test_routes import test
    from app.admin import admin
    from app.recommendations import recommendations_bp
    from app.progress import progress_bp
    from app.mobile_api import mobile_api
    from app.market_api import market_api
    from app.feedback import feedback_bp
    from app.calendar_integration import calendar_bp
    from app.portfolio import portfolio_bp
    from app.telegram_bot import telegram_bot
    from app.monitoring import monitoring
    from app.tasks import task_api
    from app.advanced_api import advanced_api
    from app.ux_api import ux_api
    from app.reports_api import reports_api
    from app.notifications_api import notifications_api
    from app.data_api import data_api
    from app.monitoring_api import monitoring_api
    from app.scheduler_api import scheduler_api
    from app.security_api import security_api
    from app.user_api import user_api
    from app.comments_api import comments_api
    from app.ratings_api import ratings_api
    from app.analytics_api import analytics_api
    app.register_blueprint(analytics_api, url_prefix='/api/analytics')
    
    # Добавляем новые модули рекомендаций и поиска
    from app.recommendations_api import recommendations_api
    app.register_blueprint(recommendations_api, url_prefix='/api/recommendations')
    
    from app.search_api import search_api
    app.register_blueprint(search_api, url_prefix='/api/search')
    
    from app.bi_api_v2 import bi_api_v2
    app.register_blueprint(bi_api_v2, url_prefix='/api/bi-v2')
    
    from app.content_api_v2 import content_api_v2
    app.register_blueprint(content_api_v2, url_prefix='/api/content-v2')
    # api_docs_bp is registered in init_api_docs function
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(test)
    app.register_blueprint(admin)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(mobile_api, url_prefix='/api')
    app.register_blueprint(market_api, url_prefix='/api')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    app.register_blueprint(calendar_bp, url_prefix='/api')
    app.register_blueprint(portfolio_bp, url_prefix='/api')
    app.register_blueprint(monitoring, url_prefix='/api/monitoring')
    app.register_blueprint(task_api, url_prefix='/api')
    app.register_blueprint(advanced_api, url_prefix='/api/advanced')
    app.register_blueprint(ux_api, url_prefix='/api/ux')
    app.register_blueprint(reports_api, url_prefix='/api/reports')
    app.register_blueprint(notifications_api, url_prefix='/api/notifications')
    app.register_blueprint(data_api, url_prefix='/api/data')
    app.register_blueprint(monitoring_api, url_prefix='/api/monitoring')
    app.register_blueprint(scheduler_api, url_prefix='/api/scheduler')
    app.register_blueprint(security_api, url_prefix='/api/security')
    app.register_blueprint(user_api, url_prefix='/api/users')
    app.register_blueprint(comments_api, url_prefix='/api/comments')
    app.register_blueprint(notifications_api, url_prefix='/api/notifications')
    app.register_blueprint(ratings_api, url_prefix='/api/ratings')
    app.register_blueprint(analytics_api, url_prefix='/api/analytics')
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