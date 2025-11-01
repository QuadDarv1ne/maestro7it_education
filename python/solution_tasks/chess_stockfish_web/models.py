"""
Data models for the Chess Stockfish Web application.
This module defines the database schema and ORM models.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """User model for player accounts"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    games_played = db.Column(db.Integer, default=0)
    games_won = db.Column(db.Integer, default=0)
    rating = db.Column(db.Integer, default=1200)
    
    # Relationship with games
    games = db.relationship('Game', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Game(db.Model):
    """Game model for storing game states"""
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fen = db.Column(db.Text, nullable=False)
    move_history = db.Column(db.Text)  # JSON string of moves
    player_color = db.Column(db.String(10), nullable=False)
    skill_level = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String(20))  # win, loss, draw, in_progress
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # in seconds
    
    def __repr__(self):
        return f'<Game {self.id} - {self.result}>'

class Puzzle(db.Model):
    """Puzzle model for training exercises"""
    __tablename__ = 'puzzles'
    
    id = db.Column(db.Integer, primary_key=True)
    fen = db.Column(db.Text, nullable=False)
    solution = db.Column(db.Text, nullable=False)  # JSON string of solution moves
    difficulty = db.Column(db.Integer, nullable=False)  # 1-10 scale
    category = db.Column(db.String(50))  # tactic, endgame, opening
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    times_solved = db.Column(db.Integer, default=0)
    times_failed = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Puzzle {self.id} - {self.category}>'

# Database initialization function
def init_db(app):
    """Initialize the database with the Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return db

# Helper functions for database operations
def create_user(username, email, password_hash):
    """Create a new user"""
    user = User(
        username=username,
        email=email,
        password_hash=password_hash
    )
    db.session.add(user)
    db.session.commit()
    return user

def create_game(user_id, fen, player_color, skill_level):
    """Create a new game"""
    game = Game(
        user_id=user_id,
        fen=fen,
        player_color=player_color,
        skill_level=skill_level
    )
    db.session.add(game)
    db.session.commit()
    return game

def update_game_result(game_id, result, move_history=None):
    """Update game result and end time"""
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
    """Get user statistics"""
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