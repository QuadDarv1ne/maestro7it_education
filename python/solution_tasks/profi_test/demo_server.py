from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
from datetime import datetime

# Создаем приложение Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем расширения
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

# Модель теста
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    methodology = db.Column(db.String(50), default='klimov')
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    accuracy = db.Column(db.Float, default=0.0)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Маршруты
@app.route('/')
def index():
    return render_template('index_modern.html')

@app.route('/about')
def about():
    return render_template('about_modern.html')

@app.route('/profile')
@login_required
def profile():
    # Имитируем данные профиля
    user_data = {
        'tests_count': 5,
        'recommendations_count': 12,
        'achievements_count': 3,
        'days_active': 45,
        'activity_level': 'Продвинутый'
    }
    
    # Имитируем историю тестов
    tests_history = [
        {
            'id': 1,
            'methodology': {
                'name': 'Методика Климова',
                'icon': 'users'
            },
            'completed_at': datetime(2026, 2, 5, 14, 30),
            'accuracy': 0.92
        },
        {
            'id': 2,
            'methodology': {
                'name': 'Методика Климова',
                'icon': 'users'
            },
            'completed_at': datetime(2026, 2, 3, 10, 15),
            'accuracy': 0.88
        }
    ]
    
    return render_template('profile_modern.html', 
                         tests_history=tests_history,
                         **user_data)

@app.route('/login')
def login():
    # Создаем тестового пользователя если его нет
    user = User.query.filter_by(username='testuser').first()
    if not user:
        user = User(username='testuser', email='test@example.com')
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return render_template('index_modern.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index_modern.html')

if __name__ == '__main__':
    with app.app_context():
        # Создаем базу данных
        db.create_all()
        
        # Добавляем тестовых пользователей если их нет
        if not User.query.filter_by(username='testuser').first():
            test_user = User(username='testuser', email='test@example.com')
            admin_user = User(username='admin', email='admin@example.com', is_admin=True)
            db.session.add(test_user)
            db.session.add(admin_user)
            db.session.commit()
    
    app.run(debug=True, port=5000)