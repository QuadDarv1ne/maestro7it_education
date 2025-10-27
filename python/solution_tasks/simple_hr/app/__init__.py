from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from instance.config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

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

    db.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Регистрация blueprint'ов
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

    # Обработка ошибок
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    return app