import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_caching import Cache
from config import Config, TestConfig

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

# Инициализация кэша
cache = Cache()

def create_app(config=None):
    """
    Создает и настраивает экземпляр приложения Flask.
    
    Args:
        config: Конфигурация приложения (словарь или класс)
        
    Returns:
        app: Настроенный экземпляр Flask-приложения
    """
    app = Flask(__name__)
    
    # Применяем конфигурацию
    if config is None:
        # Используем стандартную конфигурацию
        app.config.from_object(Config)
    elif isinstance(config, dict):
        # Применяем словарь конфигурации
        app.config.update(config)
    else:
        # Применяем класс конфигурации
        app.config.from_object(config)
    
    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # Инициализация кэша после применения конфигурации
    cache.init_app(app)
    
    # Инициализация кэша для производительности
    from app.performance import cache as performance_cache
    performance_cache.init_app(app)
    
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
    
    # Инициализация системы логирования
    from app.logging_system import setup_logging
    setup_logging(app)
    
    # Инициализация расширенного структурированного логирования
    from app.structured_logging import structured_logger, register_logging_commands
    structured_logger.init_app(app)
    app.structured_logger = structured_logger
    register_logging_commands(app)
    
    # Инициализация оптимизатора запуска приложения
    from app.startup_optimizer import startup_optimizer, apply_startup_optimizations
    apply_startup_optimizations(app)
    
    # Инициализация оптимизатора памяти
    from app.memory_optimizer import memory_optimizer, periodic_memory_cleanup
    import atexit
    atexit.register(periodic_memory_cleanup)  # Clean up on exit
    
    # Инициализация бенчмаркинга производительности
    from app.performance_benchmark import register_benchmark_commands, add_benchmark_to_jinja
    register_benchmark_commands(app)
    add_benchmark_to_jinja(app)
    
    # Инициализация мониторинга производительности
    from app.performance import performance_monitor
    app.performance_monitor = performance_monitor
    
    # Инициализация оптимизации базы данных
    from app.database_optimization import initialize_database_optimization
    initialize_database_optimization(app)
    
    # Инициализация пула соединений с базой данных (уже импортировано ранее)
    # db_connection_manager.init_app(app)  # Уже вызывается в строках 87-89
    
    # Инициализация пула соединений с базой данных
    from app.database_pooling_config import db_pool_manager
    app.db_pool_manager = db_pool_manager
    db_pool_manager.init_app(app)
    
    # Регистрация команд управления пулом
    from app.database_pooling_config import register_pool_commands
    register_pool_commands(app)
    
    # Инициализация расширенного мониторинга производительности
    from app.performance_monitoring import db_performance_monitor, register_monitoring_commands
    db_performance_monitor.init_app(app)
    register_monitoring_commands(app)
    
    # Инициализация расширенных функций безопасности
    from app.security_enhanced import security_manager
    security_manager.init_app(app)
    
    # Инициализация аудита безопасности
    from app.security_audit import security_manager as audit_security_manager
    app.audit_security_manager = audit_security_manager
    
    # Инициализация документации API
    from app.api_docs import init_api_docs
    init_api_docs(app)
    
    # Инициализация расширенного ML рекомендатора
    from app.enhanced_ml_recommender import enhanced_ml_recommender_instance
    app.enhanced_ml_recommender = enhanced_ml_recommender_instance
    
    # Инициализация расширенной аналитики
    from app.advanced_analytics import analytics_engine
    app.advanced_analytics = analytics_engine
    
    # Инициализация менеджера пользовательского опыта
    from app.ux_api import ux_manager
    app.ux_manager = ux_manager
    
    # Инициализация визуализаций
    from app.visualizations import visualizer
    app.visualizer = visualizer
    
    # Инициализация расширенных отчетов
    from app.enhanced_reports import enhanced_reports
    app.enhanced_reports = enhanced_reports
    
    # Инициализация расширенных уведомлений
    from app.advanced_notifications import notification_manager
    app.advanced_notifications = notification_manager
    
    # Инициализация обработчика данных
    from app.data_processor import data_processor
    app.data_processor = data_processor
    
    # Инициализация расширенного менеджера кэша
    from app.advanced_caching import cache_manager
    app.cache_manager = cache_manager
    
    # Инициализация Redis кэша
    from app.redis_cache import redis_cache_manager
    app.redis_cache = redis_cache_manager
    redis_cache_manager.init_app(app)
    
    # Регистрация команд управления кэшем
    from app.redis_cache import register_cache_commands
    register_cache_commands(app)
    
    # Инициализация системного монитора
    from app.system_monitoring import system_monitor
    app.system_monitor = system_monitor
    
    # Инициализация расширенных проверок состояния
    from app.health_check import health_api
    app.register_blueprint(health_api, url_prefix='/api')
    # Инициализация комплексной системы проверки состояния
    from app.health_check_comprehensive import init_health_check
    init_health_check(app)
    # Инициализация расширенного аудита безопасности
    from app.security_audit_advanced import init_security_audit
    init_security_audit(app)
    # Инициализация расширенного управления конфигурацией
    from app.config_management_advanced import init_config_management
    init_config_management(app)

    # Инициализация расширенного структурированного логирования
    from app.structured_logging_advanced import init_structured_logging
    init_structured_logging(app)
    # Инициализация расширенного тестирования API
    from app.api_testing_advanced import init_api_testing
    init_api_testing(app)
    
    # Инициализация продвинутой асинхронной обработки задач
    from app.async_task_processor import async_task_processor, register_async_commands
    async_task_processor.init_app(app)
    register_async_commands(app)
    
    # Инициализация middleware сжатия запросов/ответов
    from app.compression_middleware import CompressionMiddleware, register_compression_commands
    compression_middleware = CompressionMiddleware(app)
    register_compression_commands(app)
    
    # Инициализация продвинутого пула соединений с БД
    from app.database_pooling_advanced import advanced_connection_pool, register_pool_advanced_commands
    advanced_connection_pool.init_app(app)
    register_pool_advanced_commands(app)
    
    # Инициализация кэширования результатов запросов
    from app.query_result_cache import cache_manager, register_cache_result_commands
    cache_manager.init_app(app)
    register_cache_result_commands(app)
    
    # Инициализация оптимизации статических ресурсов
    from app.static_asset_optimizer import static_asset_optimizer, cdn_manager, register_static_asset_commands
    static_asset_optimizer.init_app(app)
    cdn_manager.init_app(app)
    register_static_asset_commands(app)
    
    # Инициализация пакетной обработки запросов
    from app.request_batching import request_batcher, bulk_manager, register_batching_commands
    request_batcher.init_app(app)
    bulk_manager.init_app(app)
    register_batching_commands(app)
    
    # Инициализация расширенной панели мониторинга производительности
    from app.performance_dashboard_enhanced import performance_monitor, register_performance_dashboard_commands
    performance_monitor.init_app(app)
    register_performance_dashboard_commands(app)
    
    # Инициализация автоматического масштабирования
    from app.auto_scaling import auto_scaler, register_auto_scaling_commands
    auto_scaler.init_app(app)
    register_auto_scaling_commands(app)
    
    # Инициализация продвинутого обнаружения аномалий
    from app.anomaly_detection import AdvancedAnomalyDetector, register_anomaly_detection_commands
    anomaly_detector = AdvancedAnomalyDetector(app)
    register_anomaly_detection_commands(app)
    
    # Инициализация предиктивного анализа производительности
    from app.performance_predictor import PerformancePredictor, register_prediction_commands
    performance_predictor = PerformancePredictor(app)
    register_prediction_commands(app)
    
    # Инициализация интеллектуального оптимизатора запросов
    from app.intelligent_query_optimizer import intelligent_optimizer, register_intelligent_optimization_commands
    intelligent_optimizer.init_app(app)
    register_intelligent_optimization_commands(app)
    
    # Инициализация оптимизатора памяти
    from app.memory_optimizer import memory_optimizer, register_memory_commands
    memory_optimizer.init_app(app)
    register_memory_commands(app)
    
    # Инициализация продвинутого сжатия
    from app.advanced_compression import compression_middleware, register_compression_commands
    compression_middleware.init_app(app)
    register_compression_commands(app)
    
    # Инициализация расширенного структурированного логирования
    from app.structured_logging_advanced import structured_logger, register_structured_logging_commands
    structured_logger.init_app(app)
    register_structured_logging_commands(app)
    
    # Инициализация предиктивной аналитики и машинного обучения
    from app.predictive_analytics_ml import predictive_analytics, register_predictive_analytics_commands
    predictive_analytics.init_app(app)
    register_predictive_analytics_commands(app)
    
    # Инициализация комплексного мониторинга здоровья системы
    from app.system_health_monitor import health_monitor, register_health_monitor_commands, register_default_health_checks
    health_monitor.init_app(app)
    register_health_monitor_commands(app)
    register_default_health_checks(app)
    
    # Инициализация продвинутого менеджера безопасности
    from app.advanced_security_manager import security_manager, register_security_commands
    security_manager.init_app(app)
    register_security_commands(app)
    
    # Инициализация продвинутого движка аналитики
    from app.advanced_analytics_engine import analytics_engine, register_analytics_commands
    analytics_engine.init_app(app)
    register_analytics_commands(app)
    
    # Инициализация менеджера пользовательского опыта
    from app.ux_manager import ux_manager, register_ux_commands
    ux_manager.init_app(app)
    register_ux_commands(app)




    
    # Инициализация middleware корреляции запросов
    from app.request_correlation import correlation_middleware
    app.correlation_middleware = correlation_middleware
    correlation_middleware.init_app(app)
    
    # Регистрация команд управления correlation ID
    from app.request_correlation import register_correlation_commands
    register_correlation_commands(app)
    
    # Инициализация продвинутого оптимизатора запросов
    from app.advanced_query_optimizer import query_optimizer
    app.query_optimizer = query_optimizer
    query_optimizer.init_app(app)
    
    # Регистрация команд управления оптимизатором
    from app.advanced_query_optimizer import register_optimizer_commands
    register_optimizer_commands(app)
    
    # Инициализация умной системы прогрева кэша
    from app.smart_cache_warming import cache_warmer
    app.cache_warmer = cache_warmer
    cache_warmer.init_app(app)
    
    # Регистрация команд управления прогревом кэша
    from app.smart_cache_warming import register_cache_warming_commands
    register_cache_warming_commands(app)
    
    # Инициализация анализатора планов запросов
    from app.query_plan_analyzer import query_plan_analyzer
    app.query_plan_analyzer = query_plan_analyzer
    query_plan_analyzer.init_app(app)
    
    # Регистрация команд управления анализатором
    from app.query_plan_analyzer import register_query_plan_commands
    register_query_plan_commands(app)
    
    # Инициализация профилировщика производительности
    from app.performance_profiler import performance_profiler, profiling_api
    app.performance_profiler = performance_profiler
    app.register_blueprint(profiling_api, url_prefix='/api/profiling')
    
    # Регистрация команд управления профилированием
    from app.performance_profiler import register_profiling_commands
    register_profiling_commands(app)
    
    # Инициализация панели мониторинга производительности
    from app.performance_dashboard import init_performance_monitoring
    init_performance_monitoring(app)
    
    # Инициализация обработчика ошибок
    from app.error_handling import error_handler
    app.error_handler = error_handler
    
    # Инициализация менеджера конфигурации
    from app.config_manager import config_manager
    app.config_manager = config_manager
    
    # Инициализация планировщика задач
    from app.task_scheduler import task_scheduler
    app.task_scheduler = task_scheduler
    
    # Инициализация Celery
    from app.tasks import init_celery_app, define_tasks
    init_celery_app(app)  # Initialize Celery with the app
    define_tasks()  # Define all tasks after celery is initialized
    
    # Инициализация продвинутого асинхронного процессора задач
    from app.async_task_processor import async_task_processor
    app.async_task_processor = async_task_processor
    
    # Отложенная инициализация планировщика для ускорения запуска приложения
    if not (config and hasattr(config, 'TESTING') and config.TESTING):
        # Запуск планировщика в отдельном потоке для ускорения старта приложения
        import threading
        scheduler_thread = threading.Thread(target=task_scheduler.start, daemon=True)
        scheduler_thread.start()  # Автозапуск планировщика только в продакшене в отдельном потоке
    
    # Инициализация менеджера безопасности
    from app.advanced_security import security_manager
    app.security_manager = security_manager
    
    # Инициализация расширенного менеджера безопасности
    from app.enhanced_security import enhanced_security
    app.enhanced_security = enhanced_security
    enhanced_security.init_app(app)
    
    # Регистрация команд управления безопасностью
    from app.enhanced_security import register_security_commands
    register_security_commands(app)
    
    # Инициализация движка бизнес-аналитики
    from app.business_intelligence import bi_engine_v2
    app.bi_engine = bi_engine_v2
    app.bi_engine_v2 = bi_engine_v2  # Avoid duplicate assignment
    
    # Инициализация менеджера пользователей
    from app.user_management import user_manager
    app.user_manager = user_manager
    
    # Инициализация систем управления контентом
    from app.content_management import content_moderation_engine, content_quality_analyzer, content_optimizer
    app.content_moderation_engine = content_moderation_engine
    app.content_quality_analyzer = content_quality_analyzer
    app.content_optimizer = content_optimizer
    
    # Инициализация менеджера комментариев
    from app.advanced_comments import comment_manager
    app.comment_manager = comment_manager
    
    # Инициализация менеджера уведомлений - используем ту же переменную, чтобы избежать дублирования
    # from app.advanced_notifications import notification_manager  # Уже импортирован выше
    app.notification_manager = notification_manager
    
    # Инициализация менеджера рейтингов
    from app.advanced_ratings import rating_manager
    app.rating_manager = rating_manager
    
    # Инициализация движка ML рекомендаций
    from app.ml_recommendations import recommendation_engine
    app.recommendation_engine = recommendation_engine
    
    # Инициализация расширенного поискового движка
    from app.advanced_search import search_engine
    app.search_engine = search_engine
    
    # bi_engine_v2 уже инициализован выше, избегаем дублирования
    

    
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
    from app.task_api import task_api
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
    from app.notifications import notifications
    app.register_blueprint(analytics_api, url_prefix='/api/analytics')
    
    # Добавляем новые модули рекомендаций и поиска
    from app.recommendations_api import recommendations_api
    app.register_blueprint(recommendations_api, url_prefix='/api/recommendations')
    
    from app.search_api import search_api
    app.register_blueprint(search_api, url_prefix='/api/search')
    
    from app.bi_api import bi_api_v2
    app.register_blueprint(bi_api_v2, url_prefix='/api/bi')
    
    from app.content_api import content_api_v2
    app.register_blueprint(content_api_v2, url_prefix='/api/content')
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
    app.register_blueprint(data_api, url_prefix='/api/data')
    app.register_blueprint(monitoring_api, url_prefix='/api/monitoring')
    app.register_blueprint(scheduler_api, url_prefix='/api/scheduler')
    app.register_blueprint(security_api, url_prefix='/api/security')
    app.register_blueprint(user_api, url_prefix='/api/users')
    app.register_blueprint(comments_api, url_prefix='/api/comments')
    app.register_blueprint(notifications_api, url_prefix='/api/notifications')
    app.register_blueprint(notifications)
    app.register_blueprint(ratings_api, url_prefix='/api/ratings')
    # api_docs_bp is registered in init_api_docs function

    # Create database tables only in application context
    # Fixed condition to properly handle TestConfig and testing environments
    is_testing = (config and hasattr(config, 'TESTING') and config.TESTING) or \
                 (isinstance(config, dict) and config.get('TESTING'))
    
    if not is_testing:
        with app.app_context():
            db.create_all()
        
        # Start vacancy alerts scheduler in a separate thread for faster startup
        try:
            from app.vacancy_alerts import start_scheduler
            import threading
            scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
            scheduler_thread.start()
        except Exception as e:
            print(f"Ошибка при запуске планировщика уведомлений: {e}")
    
        # Start ML recommendations scheduler only in production
        if not is_testing:
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
    else:
        print("Пропуск инициализации базы данных и планировщиков для тестовой среды")
    
    return app
