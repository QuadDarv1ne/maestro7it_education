from app import db
from datetime import datetime
from app.models.user import User
from app.models.forum import ForumThread, ForumPost


class Report(db.Model):
    """Represents a report of inappropriate content"""
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    reported_type = db.Column(db.String(20), nullable=False)  # 'thread' or 'post'
    reported_id = db.Column(db.Integer, nullable=False, index=True)  # ID of the thread or post
    reason = db.Column(db.String(100), nullable=False)  # Reason for the report
    description = db.Column(db.Text)  # Additional details about the report
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime)  # When the report was resolved
    resolved_by = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)  # Admin who resolved
    is_resolved = db.Column(db.Boolean, default=False)  # Whether the report has been addressed
    resolution_notes = db.Column(db.Text)  # Notes about how the report was handled
    
    # Relationships
    reporter = db.relationship('User', foreign_keys=[reporter_id], backref=db.backref('reports_submitted', lazy=True))
    resolver = db.relationship('User', foreign_keys=[resolved_by], backref=db.backref('reports_resolved', lazy=True))
    
    def __init__(self, reporter_id, reported_type, reported_id, reason, description=None):
        self.reporter_id = reporter_id
        self.reported_type = reported_type.lower()  # Normalize to lowercase
        self.reported_id = reported_id
        self.reason = reason
        self.description = description
    
    def to_dict(self):
        return {
            'id': self.id,
            'reporter_id': self.reporter_id,
            'reporter_username': self.reporter.username if self.reporter else None,
            'reported_type': self.reported_type,
            'reported_id': self.reported_id,
            'reason': self.reason,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolved_by': self.resolved_by,
            'resolver_username': self.resolver.username if self.resolver else None,
            'is_resolved': self.is_resolved,
            'resolution_notes': self.resolution_notes
        }
    
    def __repr__(self):
        return f'<Report {self.id} - {self.reported_type} {self.reported_id}>'