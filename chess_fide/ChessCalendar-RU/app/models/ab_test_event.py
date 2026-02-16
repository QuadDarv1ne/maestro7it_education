"""
Модель для хранения событий A/B тестирования
"""

from datetime import datetime
from app import db


class ABTestEvent(db.Model):
    """События A/B тестирования"""
    __tablename__ = 'ab_test_events'
    
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100), nullable=False, index=True)
    user_id = db.Column(db.String(100), nullable=False, index=True)
    variant = db.Column(db.String(50), nullable=False, index=True)
    event = db.Column(db.String(100), nullable=False, index=True)
    value = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Дополнительные метаданные
    user_agent = db.Column(db.String(500))
    ip_address = db.Column(db.String(50))
    session_id = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<ABTestEvent {self.test_name}:{self.variant}:{self.event}>'
    
    def to_dict(self):
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'test_name': self.test_name,
            'user_id': self.user_id,
            'variant': self.variant,
            'event': self.event,
            'value': self.value,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
