from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint
import re

class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    start_date = db.Column(db.Date, nullable=False, index=True)
    end_date = db.Column(db.Date, nullable=False, index=True)
    location = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)  # FIDE, National, Youth, etc.
    status = db.Column(db.String(50), default='Scheduled', index=True)  # Scheduled, Ongoing, Completed
    fide_id = db.Column(db.String(20), unique=True, index=True)  # FIDE tournament ID
    source_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<Tournament {self.name}>'

    def to_dict(self):
        from app.utils.ratings import RatingService
        avg_rating = RatingService.get_tournament_average_rating(self.id)
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'location': self.location,
            'category': self.category,
            'status': self.status,
            'fide_id': self.fide_id,
            'source_url': self.source_url,
            'average_rating': avg_rating['average_rating'],
            'total_ratings': avg_rating['total_ratings']
        }
    
    def get_average_rating(self):
        """Get average rating for this tournament"""
        from app.utils.ratings import RatingService
        avg_rating = RatingService.get_tournament_average_rating(self.id)
        return avg_rating['average_rating']
    
    def validate(self):
        """Валидация данных турнира"""
        errors = []
        
        # Проверка имени
        if not self.name or len(self.name.strip()) == 0:
            errors.append("Название турнира не может быть пустым")
        elif len(self.name) > 200:
            errors.append("Название турнира слишком длинное (максимум 200 символов)")
        
        # Проверка дат
        if not self.start_date:
            errors.append("Дата начала обязательна")
        if not self.end_date:
            errors.append("Дата окончания обязательна")
        if self.start_date and self.end_date and self.start_date > self.end_date:
            errors.append("Дата начала не может быть позже даты окончания")
        
        # Проверка места проведения
        if not self.location or len(self.location.strip()) == 0:
            errors.append("Место проведения не может быть пустым")
        elif len(self.location) > 100:
            errors.append("Название места проведения слишком длинное (максимум 100 символов)")
        
        # Проверка категории
        valid_categories = ['FIDE', 'National', 'Regional', 'Youth', 'Women', 'Senior', 'Online']
        if self.category not in valid_categories:
            errors.append(f"Недопустимая категория. Допустимые значения: {', '.join(valid_categories)}")
        
        # Проверка статуса
        valid_statuses = ['Scheduled', 'Ongoing', 'Completed', 'Cancelled']
        if self.status not in valid_statuses:
            errors.append(f"Недопустимый статус. Допустимые значения: {', '.join(valid_statuses)}")
        
        # Проверка FIDE ID
        if self.fide_id and not re.match(r'^\d+$', self.fide_id):
            errors.append("FIDE ID должен содержать только цифры")
        
        # Проверка URL
        if self.source_url and not self._is_valid_url(self.source_url):
            errors.append("Недопустимый формат URL")
        
        return errors
    
    def _is_valid_url(self, url):
        """Проверка корректности URL"""
        if not url:
            return True
        url_pattern = re.compile(
            r'^https?://'  # http:// или https://
            r'(?:www\.)?'  # необязательный www.
            r'[a-zA-Z0-9.-]+'  # домен
            r'\.[a-zA-Z]{2,}'  # зона домена
            r'(?:/[\w\.@\(?\)\[\]\?\=/&\~\-%]*)?$',  # путь
            re.IGNORECASE
        )
        return re.match(url_pattern, url) is not None

    def get_similar(self, limit=5):
        """Получить похожие турниры (по категории и месту)"""
        # Поиск по категории и месту
        similar = Tournament.query.filter(
            Tournament.id != self.id,
            Tournament.category == self.category,
            Tournament.location.ilike(f'%{self.location}%')
        ).limit(limit).all()
        
        # Если не нашли достаточно по категории и месту, ищем только по категории
        if len(similar) < limit:
            remaining_slots = limit - len(similar)
            exclude_ids = [t.id for t in similar] + [self.id]
            
            additional = Tournament.query.filter(
                Tournament.id.notin_(exclude_ids),
                Tournament.category == self.category
            ).limit(remaining_slots).all()
            
            similar.extend(additional)
            
        return similar