from app import db
from datetime import datetime
import bleach


class TournamentRating(db.Model):
    __tablename__ = 'tournament_rating'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review = db.Column(db.Text)  # Optional review text
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    tournament = db.relationship('Tournament', backref=db.backref('ratings', lazy=True))
    
    # Ensure uniqueness: one user can rate the same tournament only once
    __table_args__ = (
        db.UniqueConstraint('user_id', 'tournament_id'),
        # Additional indexes for common query patterns
        db.Index('idx_user_rating', 'user_id', 'rating'),
        db.Index('idx_tournament_rating', 'tournament_id', 'rating'),
        db.Index('idx_created_rating', 'created_at', 'rating'),
    )
    
    def __init__(self, user_id, tournament_id, rating, review=None):
        self.user_id = user_id
        self.tournament_id = tournament_id
        self.rating = rating
        self.review = review
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tournament_id': self.tournament_id,
            'rating': self.rating,
            'review': self.review,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_username': self.user.username if self.user else None
        }
    
    def __repr__(self):
        return f'<TournamentRating user_id={self.user_id} tournament_id={self.tournament_id} rating={self.rating}>'
    
    def validate(self):
        """Валидация данных оценки"""
        errors = []
        
        # Sanitize inputs
        self.sanitize_fields()
        
        # Проверка рейтинга
        if self.rating is None:
            errors.append("Рейтинг не может быть пустым")
        elif not (1 <= self.rating <= 5):
            errors.append("Рейтинг должен быть от 1 до 5")
        
        # Проверка ID пользователя
        if not self.user_id:
            errors.append("ID пользователя обязателен")
        
        # Проверка ID турнира
        if not self.tournament_id:
            errors.append("ID турнира обязателен")
        
        # Проверка отзыва
        if self.review and len(self.review) > 1000:
            errors.append("Отзыв слишком длинный (максимум 1000 символов)")
        
        return errors
    
    def sanitize_fields(self):
        """Sanitize input fields to prevent XSS"""
        if self.review:
            # Allow some safe HTML tags in reviews
            self.review = bleach.clean(self.review, 
                                   tags=['p', 'br', 'strong', 'em'], 
                                   attributes={}, 
                                   strip=True)