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
    telegram_chat_id = db.Column(db.String(50))  # For Telegram notifications
    
    # Relationships
    test_results = db.relationship('TestResult', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='comment_user', lazy=True)
    ratings = db.relationship('Rating', backref='rating_user', lazy=True)
    progress_records = db.relationship('UserProgress', backref='progress_user', lazy=True)
    preferences = db.relationship('UserPreference', backref='preference_user', lazy=True)
    feedbacks = db.relationship('Feedback', backref='feedback_user', lazy=True)
    ab_test_results = db.relationship('ABTestResult', backref='ab_test_user', lazy=True)
    career_goals = db.relationship('CareerGoal', backref='career_goal_user', lazy=True)
    learning_paths = db.relationship('LearningPath', backref='learning_path_user', lazy=True)
    calendar_events = db.relationship('CalendarEvent', backref='calendar_event_user', lazy=True)
    portfolio_projects = db.relationship('PortfolioProject', backref='portfolio_project_user', lazy=True)
    
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
    user = db.relationship('User', backref='user_comments')
    
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
    user = db.relationship('User', backref='user_ratings')
    test_result = db.relationship('TestResult', backref='ratings')
    comment = db.relationship('Comment', backref='ratings')
    
    def __repr__(self):
        return f'<Rating {self.rating_type} by User {self.user_id}>'


class UserProgress(db.Model):
    """Model for tracking user progress over time"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_result_id = db.Column(db.Integer, db.ForeignKey('test_result.id'), nullable=False)
    category_scores = db.Column(db.Text)  # JSON string of category scores
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='user_progress_records')
    test_result = db.relationship('TestResult', backref='progress_record')
    
    def __repr__(self):
        return f'<UserProgress User {self.user_id} - Test {self.test_result_id}>'


class UserPreference(db.Model):
    """Model for user preferences and settings"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vacancy_alerts_enabled = db.Column(db.Boolean, default=False)
    preferred_professions = db.Column(db.Text)  # JSON string of preferred professions
    email_notifications = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='user_preferences')
    
    def __repr__(self):
        return f'<UserPreference for User {self.user_id}>'


class Feedback(db.Model):
    # Модель для хранения отзывов пользователей
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_type = db.Column(db.String(50), nullable=False)  # suggestion, bug_report, feature_request, general_feedback
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)  # 1-5 star rating
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)
    
    # Relationship
    user = db.relationship('User', backref='user_feedbacks')
    
    def __repr__(self):
        return f'<Feedback {self.feedback_type} by User {self.user_id}>'


class ABTest(db.Model):
    # Модель для A/B тестирования экспериментов
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # e.g., "ml_recommendation_algorithm_v2"
    description = db.Column(db.Text)
    variant_a = db.Column(db.String(100), nullable=False)  # e.g., "current_algorithm"
    variant_b = db.Column(db.String(100), nullable=False)  # e.g., "new_algorithm"
    traffic_split = db.Column(db.Float, default=0.5)  # 0.0 to 1.0, proportion for variant B
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<ABTest {self.name}>'


class ABTestResult(db.Model):
    # Модель для результатов A/B тестирования
    id = db.Column(db.Integer, primary_key=True)
    ab_test_id = db.Column(db.Integer, db.ForeignKey('ab_test.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assigned_variant = db.Column(db.String(10), nullable=False)  # 'A' or 'B'
    metric_value = db.Column(db.Float)  # e.g., engagement rate, click-through rate
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ab_test = db.relationship('ABTest', backref='results')
    user = db.relationship('User', backref='user_ab_test_results')
    
    def __repr__(self):
        return f'<ABTestResult for Test {self.ab_test_id}, User {self.user_id}, Variant {self.assigned_variant}>'


class CareerGoal(db.Model):
    # Модель для карьерных целей пользователя
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    target_date = db.Column(db.Date)
    current_status = db.Column(db.String(50), default='planning')  # planning, in_progress, achieved, paused
    priority = db.Column(db.Integer, default=1)  # 1-5 scale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='user_career_goals')
    
    def __repr__(self):
        return f'<CareerGoal {self.title} for User {self.user_id}>'


class LearningPath(db.Model):
    # Модель для образовательных траекторий
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goal_id = db.Column(db.Integer, db.ForeignKey('career_goal.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration_weeks = db.Column(db.Integer, default=4)  # estimated duration in weeks
    difficulty_level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='user_learning_paths')
    goal = db.relationship('CareerGoal', backref='learning_paths')
    
    def __repr__(self):
        return f'<LearningPath {self.title} for User {self.user_id}>'


class CalendarEvent(db.Model):
    # Модель для событий календаря
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), default='event')  # event, meeting, deadline, learning_session
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime)
    location = db.Column(db.String(200))
    is_recurring = db.Column(db.Boolean, default=False)
    recurrence_pattern = db.Column(db.String(50))  # daily, weekly, monthly, yearly
    reminder_minutes = db.Column(db.Integer, default=15)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='user_calendar_events')
    
    def __repr__(self):
        return f'<CalendarEvent {self.title} for User {self.user_id}>'


class PortfolioProject(db.Model):
    # Модель для проектов в портфолио пользователя
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    technologies = db.Column(db.Text)  # JSON string of technologies used
    github_url = db.Column(db.String(500))
    demo_url = db.Column(db.String(500))
    project_type = db.Column(db.String(50), default='personal')  # personal, freelance, work
    status = db.Column(db.String(20), default='in_progress')  # planning, in_progress, completed, archived
    start_date = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='user_portfolio_projects')
    
    def __repr__(self):
        return f'<PortfolioProject {self.title} for User {self.user_id}>'