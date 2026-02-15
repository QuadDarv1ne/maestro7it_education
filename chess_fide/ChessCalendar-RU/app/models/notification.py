from app import db
from datetime import datetime
from enum import Enum


class NotificationType(Enum):
    NEW_TOURNAMENT = "new_tournament"
    TOURNAMENT_UPDATE = "tournament_update"
    TOURNAMENT_CANCELLED = "tournament_cancelled"
    REMINDER = "reminder"


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum(NotificationType), nullable=False)
    recipient_email = db.Column(db.String(120), nullable=True, index=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=True, index=True)
    is_read = db.Column(db.Boolean, default=False, index=True)
    priority = db.Column(db.Integer, default=1)  # 1-low, 2-normal, 3-high
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    sent_at = db.Column(db.DateTime, nullable=True)

    # Relationship
    tournament = db.relationship('Tournament', backref='notifications')

    def __init__(self, title, message, type, recipient_email=None, tournament_id=None, priority=2):
        self.title = title
        self.message = message
        self.type = type
        self.recipient_email = recipient_email
        self.tournament_id = tournament_id
        self.priority = priority

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'type': self.type.value,
            'recipient_email': self.recipient_email,
            'tournament_id': self.tournament_id,
            'is_read': self.is_read,
            'priority': self.priority,
            'created_at': self.created_at.isoformat(),
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }

    def __repr__(self):
        return f'<Notification {self.title}>'


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    active = db.Column(db.Boolean, default=True, index=True)
    preferences = db.Column(db.JSON, default=lambda: {
        'new_tournaments': True,
        'tournament_updates': True,
        'reminders': True
    })
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, email, preferences=None):
        self.email = email
        if preferences:
            self.preferences = preferences

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'active': self.active,
            'preferences': self.preferences,
            'created_at': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<Subscription {self.email}>'