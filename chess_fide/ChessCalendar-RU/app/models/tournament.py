from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint
import re
import bleach

class Tournament(db.Model):
    __tablename__ = 'tournament'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    start_date = db.Column(db.Date, nullable=False, index=True)
    end_date = db.Column(db.Date, nullable=False, index=True)
    location = db.Column(db.String(100), nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)  # FIDE, National, Youth, etc.
    status = db.Column(db.String(50), default='Scheduled', index=True)  # Scheduled, Ongoing, Completed
    description = db.Column(db.Text, nullable=True)  # Description of the tournament
    prize_fund = db.Column(db.String(200), nullable=True)  # Prize fund amount
    organizer = db.Column(db.String(200), nullable=True)  # Organizer of the tournament
    fide_id = db.Column(db.String(20), unique=True, index=True)  # FIDE tournament ID
    source_url = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    
    # Добавляем новые поля
    prize_fund_usd = db.Column(db.Integer, nullable=True)  # Призовой фонд в долларах США
    players_count = db.Column(db.Integer, nullable=True)  # Количество участников
    time_control = db.Column(db.String(50), nullable=True)  # Контроль времени (Classical, Rapid, Blitz)
    
    # Composite indexes for common query patterns
    __table_args__ = (
        db.Index('idx_location_category', 'location', 'category'),
        db.Index('idx_category_status', 'category', 'status'),
        db.Index('idx_start_date_status', 'start_date', 'status'),
        db.Index('idx_created_at_status', 'created_at', 'status'),
        db.Index('idx_end_date_status', 'end_date', 'status'),
        db.Index('idx_name_status', 'name', 'status'),
        db.Index('idx_organizer_status', 'organizer', 'status'),
        db.Index('idx_dates_range', 'start_date', 'end_date'),
        db.Index('idx_location_start_date', 'location', 'start_date'),  # For location + date range queries
        db.Index('idx_category_start_date', 'category', 'start_date'),  # For category + date range queries
        db.Index('idx_status_updated_at', 'status', 'updated_at'),  # For status + updated queries
        # Индексы для новых полей
        db.Index('idx_prize_fund_usd', 'prize_fund_usd'),
        db.Index('idx_players_count', 'players_count'),
        db.Index('idx_time_control', 'time_control'),
    )

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
            'description': self.description,
            'prize_fund': self.prize_fund,
            'organizer': self.organizer,
            'fide_id': self.fide_id,
            'source_url': self.source_url,
            'prize_fund_usd': self.prize_fund_usd,
            'players_count': self.players_count,
            'time_control': self.time_control,
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
        
        # Sanitize inputs
        self.sanitize_fields()
        
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
        
        # Проверка диапазона дат
        if self.start_date and self.end_date:
            # Проверяем, чтобы турнир не был в прошлом более чем на 30 дней
            from datetime import date, timedelta
            thirty_days_ago = date.today() - timedelta(days=30)
            if self.end_date < thirty_days_ago:
                errors.append("Нельзя добавлять турниры, которые уже закончились более чем 30 дней назад")
        
        # Проверка места проведения
        if not self.location or len(self.location.strip()) == 0:
            errors.append("Место проведения не может быть пустым")
        elif len(self.location) > 100:
            errors.append("Название места проведения слишком длинное (максимум 100 символов)")
        
        # Проверка описания
        if self.description and len(self.description) > 2000:
            errors.append("Описание турнира слишком длинное (максимум 2000 символов)")
        
        # Проверка призового фонда
        if self.prize_fund and len(self.prize_fund) > 200:
            errors.append("Информация о призовом фонде слишком длинная (максимум 200 символов)")
        
        # Проверка организатора
        if self.organizer and len(self.organizer) > 200:
            errors.append("Название организатора слишком длинное (максимум 200 символов)")
        
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
    
    def sanitize_fields(self):
        """Sanitize input fields to prevent XSS"""
        if self.name:
            self.name = bleach.clean(self.name, strip=True)
        if self.location:
            self.location = bleach.clean(self.location, strip=True)
        if self.description:
            # Allow some safe HTML tags in description
            self.description = bleach.clean(self.description, 
                                         tags=['p', 'br', 'strong', 'em', 'ul', 'ol', 'li'], 
                                         attributes={}, 
                                         strip=True)
        if self.prize_fund:
            self.prize_fund = bleach.clean(self.prize_fund, strip=True)
        if self.organizer:
            self.organizer = bleach.clean(self.organizer, strip=True)
        if self.source_url:
            self.source_url = bleach.clean(self.source_url, strip=True)
    
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
    
    def is_upcoming(self):
        """Check if the tournament is upcoming"""
        from datetime import date
        return self.start_date >= date.today()
    
    def is_ongoing(self):
        """Check if the tournament is currently ongoing"""
        from datetime import date
        today = date.today()
        return self.start_date <= today <= self.end_date
    
    def duration_days(self):
        """Get tournament duration in days"""
        return (self.end_date - self.start_date).days + 1
    
    @staticmethod
    def get_upcoming_tournaments(limit=10):
        """Get upcoming tournaments"""
        from datetime import date
        return Tournament.query.filter(
            Tournament.start_date >= date.today()
        ).order_by(Tournament.start_date).limit(limit).all()
    
    @staticmethod
    def get_ongoing_tournaments():
        """Get currently ongoing tournaments"""
        from datetime import date
        today = date.today()
        return Tournament.query.filter(
            Tournament.start_date <= today,
            Tournament.end_date >= today
        ).all()
