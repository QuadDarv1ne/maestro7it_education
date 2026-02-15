from app import db
from datetime import datetime


class TournamentSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('tournament_subscriptions', lazy=True))
    tournament = db.relationship('Tournament', backref=db.backref('subscribers', lazy=True))
    
    def __repr__(self):
        return f'<TournamentSubscription user_id={self.user_id} tournament_id={self.tournament_id}>'
    
    @classmethod
    def is_subscribed(cls, user_id, tournament_id):
        """Check if a user is subscribed to a specific tournament"""
        subscription = cls.query.filter_by(user_id=user_id, tournament_id=tournament_id).first()
        return subscription is not None
    
    @classmethod
    def subscribe(cls, user_id, tournament_id):
        """Subscribe a user to a tournament"""
        if not cls.is_subscribed(user_id, tournament_id):
            subscription = cls(user_id=user_id, tournament_id=tournament_id)
            db.session.add(subscription)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def unsubscribe(cls, user_id, tournament_id):
        """Unsubscribe a user from a tournament"""
        subscription = cls.query.filter_by(user_id=user_id, tournament_id=tournament_id).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
            return True
        return False