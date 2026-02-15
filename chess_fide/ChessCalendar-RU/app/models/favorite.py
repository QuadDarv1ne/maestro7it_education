from app import db
from datetime import datetime
from app.models.user import User
from app.models.tournament import Tournament


class FavoriteTournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('favorites', lazy=True))
    tournament = db.relationship('Tournament', backref=db.backref('favorited_by', lazy=True))
    
    # Ensure uniqueness: one user can favorite the same tournament only once
    __table_args__ = (db.UniqueConstraint('user_id', 'tournament_id'),)
    
    def __init__(self, user_id, tournament_id):
        self.user_id = user_id
        self.tournament_id = tournament_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tournament_id': self.tournament_id,
            'created_at': self.created_at.isoformat(),
            'tournament': self.tournament.to_dict() if self.tournament else None
        }
    
    def __repr__(self):
        return f'<FavoriteTournament user_id={self.user_id} tournament_id={self.tournament_id}>'