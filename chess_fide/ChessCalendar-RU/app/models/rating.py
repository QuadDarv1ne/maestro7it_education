from app import db
from datetime import datetime
from app.models.user import User
from app.models.tournament import Tournament


class TournamentRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    review = db.Column(db.Text)  # Optional review text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    tournament = db.relationship('Tournament', backref=db.backref('ratings', lazy=True))
    
    # Ensure uniqueness: one user can rate the same tournament only once
    __table_args__ = (db.UniqueConstraint('user_id', 'tournament_id'),)
    
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