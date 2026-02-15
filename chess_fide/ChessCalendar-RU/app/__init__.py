from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Загрузка конфигурации
    app.config.from_object('config.Config')
    
    # Инициализация расширений
    db.init_app(app)
    
    # Создание таблиц
    with app.app_context():
        db.create_all()
    
    # Регистрация blueprint'ов
    from app.views.main import main_bp
    from app.views.admin import admin_bp
    from app.views.api_docs import api_docs_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_docs_bp)
    
    return app