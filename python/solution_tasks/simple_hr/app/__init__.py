from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from instance.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

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

    return app