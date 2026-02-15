from app import db
from datetime import datetime
from app.models.user import User
from app.models.tournament import Tournament


class UserPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    category_preference = db.Column(db.Text)  # JSON string of category preferences
    location_preference = db.Column(db.Text)   # JSON string of location preferences
    difficulty_preference = db.Column(db.String(50))  # Rating level preference
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('preferences', lazy=True, uselist=False))
    
    def __init__(self, user_id, category_preference=None, location_preference=None, difficulty_preference=None):
        self.user_id = user_id
        self.category_preference = category_preference or '{}'
        self.location_preference = location_preference or '{}'
        self.difficulty_preference = difficulty_preference
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_preference': self.category_preference,
            'location_preference': self.location_preference,
            'difficulty_preference': self.difficulty_preference,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<UserPreference user_id={self.user_id}>'


class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False, index=True)
    interaction_type = db.Column(db.String(50), nullable=False)  # 'view', 'favorite', 'register', etc.
    interaction_value = db.Column(db.Integer, default=1)  # Weight of interaction
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('interactions', lazy=True))
    tournament = db.relationship('Tournament', backref=db.backref('user_interactions', lazy=True))
    
    def __init__(self, user_id, tournament_id, interaction_type, interaction_value=1):
        self.user_id = user_id
        self.tournament_id = tournament_id
        self.interaction_type = interaction_type
        self.interaction_value = interaction_value
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tournament_id': self.tournament_id,
            'interaction_type': self.interaction_type,
            'interaction_value': self.interaction_value,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<UserInteraction user_id={self.user_id} tournament_id={self.tournament_id} type={self.interaction_type}>'