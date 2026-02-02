"""
Minimal Flask app for testing
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Create a simple model
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        
        def __repr__(self):
            return f'<User {self.username}>'
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Simple routes for testing
    @app.route('/')
    def index():
        return '<h1>Profi Test Application</h1><p>Application is running successfully!</p>'
    
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'message': 'Application is running'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting minimal Flask application...")
    app.run(debug=True, host='127.0.0.1', port=5000)