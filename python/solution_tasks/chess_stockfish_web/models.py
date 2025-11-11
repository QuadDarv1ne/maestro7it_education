"""
Модели данных для веб-приложения Chess Stockfish Web.
Этот модуль определяет схему базы данных и ORM модели.
"""

from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy

# Инициализация SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """Модель пользователя для учетных записей игроков"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_login = db.Column(db.DateTime, index=True)
    games_played = db.Column(db.Integer, default=0, index=True)
    games_won = db.Column(db.Integer, default=0)
    rating = db.Column(db.Integer, default=1200, index=True)
    
    # Связь с играми
    games = db.relationship('Game', backref='user', lazy='select', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Game(db.Model):
    """Модель игры для хранения состояний игр"""
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    fen = db.Column(db.Text, nullable=False, index=True)
    move_history = db.Column(db.Text)  # JSON строка ходов
    player_color = db.Column(db.String(10), nullable=False, index=True)
    skill_level = db.Column(db.Integer, nullable=False, index=True)
    result = db.Column(db.String(20), index=True)  # победа, поражение, ничья, в_процессе
    start_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    end_time = db.Column(db.DateTime, index=True)
    duration = db.Column(db.Integer)  # в секундах
    last_move = db.Column(db.String(10))  # Последний ход в игре
    is_active = db.Column(db.Boolean, default=True, index=True)  # Флаг активной игры
    
    # Составные индексы для частых запросов
    __table_args__ = (
        db.Index('idx_user_result_time', 'user_id', 'result', 'start_time'),
        db.Index('idx_user_active_time', 'user_id', 'is_active', 'start_time'),
        db.Index('idx_result_skill', 'result', 'skill_level'),
        db.Index('idx_active_duration', 'is_active', 'duration')
    )
    
    def __repr__(self):
        return f'<Game {self.id} - {self.result}>'

class Puzzle(db.Model):
    """Модель головоломки для тренировочных упражнений"""
    __tablename__ = 'puzzles'
    
    id = db.Column(db.Integer, primary_key=True)
    fen = db.Column(db.Text, nullable=False, index=True)
    solution = db.Column(db.Text, nullable=False)  # JSON строка ходов решения
    difficulty = db.Column(db.Integer, nullable=False, index=True)
    category = db.Column(db.String(50), index=True)  # тактика, эндшпиль, дебют
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    times_solved = db.Column(db.Integer, default=0, index=True)
    times_failed = db.Column(db.Integer, default=0)
    
    # Составной индекс для частых запросов
    __table_args__ = (
        db.Index('idx_difficulty_category', 'difficulty', 'category'),
    )
    
    def __repr__(self):
        return f'<Puzzle {self.id} - {self.category}>'

# Функция инициализации базы данных
def init_db(app):
    """Инициализация базы данных с Flask приложением"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return db

# Вспомогательные функции для операций с базой данных
def create_user(username, email, password_hash):
    """Создание нового пользователя"""
    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    db.session.add(user)
    db.session.commit()
    return user

def create_game(user_id, fen, player_color, skill_level, last_move=None):
    """Создание новой игры"""
    game = Game(
        user_id=user_id,
        fen=fen,
        player_color=player_color,
        skill_level=skill_level,
        last_move=last_move,
        is_active=True,
        result='in_progress'
    )
    db.session.add(game)
    db.session.commit()
    return game

def update_game_result(game_id, result, move_history=None):
    """Обновление результата игры и времени окончания"""
    game = Game.query.get(game_id)
    if game:
        game.result = result
        game.end_time = datetime.utcnow()
        if game.start_time:
            game.duration = int((game.end_time - game.start_time).total_seconds())
        if move_history:
            game.move_history = json.dumps(move_history)
        db.session.commit()
    return game

def get_user_stats(user_id):
    """Получение статистики пользователя с оптимизированным запросом"""
    # Использование get() для поиска по первичному ключу (наиболее эффективно)
    user = User.query.get(user_id)
    if user:
        total_games = user.games_played
        wins = user.games_won
        win_rate = (wins / total_games * 100) if total_games > 0 else 0
        return {
            'total_games': total_games,
            'wins': wins,
            'losses': total_games - wins,
            'win_rate': win_rate,
            'rating': user.rating
        }
    return None

def get_recent_games_optimized(user_id, limit=10):
    """Получение последних игр с оптимизированным запросом с использованием индекса"""
    return Game.query.filter_by(
        user_id=user_id
    ).order_by(
        Game.start_time.desc()
    ).limit(limit).all()

def get_games_by_result(user_id, result, limit=20):
    """Получение игр по результату с оптимизированным запросом"""
    return Game.query.filter(
        Game.user_id == user_id,
        Game.result == result
    ).order_by(
        Game.start_time.desc()
    ).limit(limit).all()