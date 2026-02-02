from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships
    test_results = db.relationship('TestResult', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class TestResult(db.Model):
    """Model for storing test results"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    methodology = db.Column(db.String(50), nullable=False)  # 'klimov', 'holland', etc.
    answers = db.Column(db.Text)  # JSON string of answers
    results = db.Column(db.Text)  # JSON string of calculated results
    recommendation = db.Column(db.Text)  # Personalized recommendation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<TestResult {self.id} for User {self.user_id}>'

class TestQuestion(db.Model):
    """Model for test questions"""
    id = db.Column(db.Integer, primary_key=True)
    methodology = db.Column(db.String(50), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))  # Professional sphere
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<TestQuestion {self.methodology}-{self.question_number}>'

class Notification(db.Model):
    """Model for user notifications"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), default='info')  # info, success, warning, error
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Notification {self.id} for User {self.user_id}>'

class Comment(db.Model):
    """Model for test result comments"""
    id = db.Column(db.Integer, primary_key=True)
    test_result_id = db.Column(db.Integer, db.ForeignKey('test_result.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    test_result = db.relationship('TestResult', backref='comments')
    user = db.relationship('User', backref='comments')
    
    def __repr__(self):
        return f'<Comment {self.id} on Test {self.test_result_id}>'


class Rating(db.Model):
    """Model for ratings (likes/dislikes) for test results and comments"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_result_id = db.Column(db.Integer, db.ForeignKey('test_result.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    rating_type = db.Column(db.String(10), nullable=False)  # 'like' or 'dislike'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure only one rating per user per item
    __table_args__ = (
        db.UniqueConstraint('user_id', 'test_result_id', name='unique_user_test_rating'),
        db.UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_rating'),
    )
    
    # Relationships
    user = db.relationship('User', backref='ratings')
    test_result = db.relationship('TestResult', backref='ratings')
    comment = db.relationship('Comment', backref='ratings')
    
    def __repr__(self):
        return f'<Rating {self.rating_type} by User {self.user_id}>'