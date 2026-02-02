import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///profi_test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    
    # Register blueprints
    from app.routes import main
    from app.auth import auth
    from app.test_routes import test
    
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(test)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Import models after db is initialized to avoid circular imports
        from app.models import User
        
        @login_manager.user_loader
        def load_user(user_id):
            """Load user by ID for Flask-Login"""
            return User.query.get(int(user_id))
    
    return app