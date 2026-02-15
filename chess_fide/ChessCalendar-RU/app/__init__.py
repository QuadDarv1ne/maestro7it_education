from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app(config_name='default'):
    import logging
    # Initialize logging before anything else
    try:
        from app.utils.logging_config import init_logging
        init_logging()
    except Exception as e:
        logging.warning(f"Failed to initialize advanced logging: {e}")
        # Fallback to basic logging
        logging.basicConfig(level=logging.INFO)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting application initialization")
    
    app = Flask(__name__, template_folder='../templates')
    
    # Загрузка конфигурации
    app.config.from_object('config.Config')
    
    # Инициализация расширений
    db.init_app(app)
    
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
        return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    @app.route('/robots.txt')
    def robots():
        return send_from_directory('static', 'robots.txt', mimetype='text/plain')
    
    # PWA маршруты
    @app.route('/sw.js')
    def service_worker():
        import os
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        return send_from_directory(static_dir, 'sw.js', mimetype='application/javascript')
    
    @app.route('/manifest.json')
    def manifest():
        return send_from_directory('static', 'manifest.json')
    
    # Регистрация blueprint'ов
    from app.views.main import main_bp
    from app.views.admin import admin_bp
    from app.views.api_docs import api_docs_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_docs_bp)
    
    return app