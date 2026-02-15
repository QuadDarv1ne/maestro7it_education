from app import db
from datetime import datetime

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # FIDE, National, Youth, etc.
    status = db.Column(db.String(50), default='Scheduled')  # Scheduled, Ongoing, Completed
    fide_id = db.Column(db.String(20), unique=True)  # FIDE tournament ID
    source_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Tournament {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'location': self.location,
            'category': self.category,
            'status': self.status,
            'fide_id': self.fide_id,
            'source_url': self.source_url
        }

    def get_similar(self, limit=5):
        """Получить похожие турниры (по категории и месту)"""
        similar = Tournament.query.filter(
            Tournament.id != self.id,
            Tournament.category == self.category,
            Tournament.location.like(f'%{self.location}%')
        ).limit(limit).all()
        
        # Если не нашли по категории и месту, ищем по категории
        if len(similar) < limit:
            additional = Tournament.query.filter(
                Tournament.id != self.id,
                Tournament.category == self.category,
                Tournament.id.notin_([t.id for t in similar])
            ).limit(limit - len(similar)).all()
            similar.extend(additional)
            
        return similar