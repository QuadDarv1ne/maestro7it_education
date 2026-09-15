"""
Система тегов для турниров - категоризация и поиск по тегам
"""
from app import db
from datetime import datetime


class Tag(db.Model):
    """Тег для категоризации турниров"""
    __tablename__ = 'tag'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    slug = db.Column(db.String(60), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    color = db.Column(db.String(7), default='#3498db')  # HEX цвет для UI
    usage_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    tournaments = db.relationship('TagTournament', backref='tag', lazy='dynamic')
    
    __table_args__ = (
        db.Index('idx_tag_slug', 'slug'),
        db.Index('idx_tag_usage', 'usage_count', postgresql_using='btree'),
    )
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'color': self.color,
            'usage_count': self.usage_count
        }


class TagTournament(db.Model):
    """Связь тегов с турнирами (многие-ко-многим)"""
    __tablename__ = 'tag_tournament'
    
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False, index=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False, index=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Composite unique constraint - один тег один раз на турнир
    __table_args__ = (
        db.UniqueConstraint('tag_id', 'tournament_id', name='uq_tag_tournament'),
        db.Index('idx_tournament_tags', 'tournament_id', 'tag_id'),
    )
    
    # Relationships
    tournament = db.relationship('Tournament', backref=db.backref('tag_assignments', lazy='dynamic'))
    
    def __repr__(self):
        return f'<TagTournament tag={self.tag_id} tournament={self.tournament_id}>'


class TagService:
    """Сервис для работы с тегами"""
    
    @staticmethod
    def create_tag(name, description=None, color='#3498db'):
        """Создать новый тег"""
        from app.utils.validators import slugify
        
        # Проверяем существование
        existing = Tag.query.filter_by(name=name).first()
        if existing:
            return existing, "Tag already exists"
        
        # Создаём slug
        slug = slugify(name)
        
        tag = Tag(
            name=name,
            slug=slug,
            description=description,
            color=color
        )
        db.session.add(tag)
        db.session.commit()
        
        return tag, None
    
    @staticmethod
    def add_tag_to_tournament(tournament_id, tag_name):
        """Добавить тег к турниру"""
        tag = Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag, error = TagService.create_tag(tag_name)
            if error:
                return None, error
        
        # Проверяем связь
        existing = TagTournament.query.filter_by(
            tag_id=tag.id,
            tournament_id=tournament_id
        ).first()
        
        if existing:
            return tag, None  # Уже существует
        
        assignment = TagTournament(
            tag_id=tag.id,
            tournament_id=tournament_id
        )
        db.session.add(assignment)
        
        # Увеличиваем счётчик использования
        tag.usage_count += 1
        
        db.session.commit()
        return tag, None
    
    @staticmethod
    def get_tournament_tags(tournament_id):
        """Получить все теги турнира"""
        assignments = TagTournament.query.filter_by(tournament_id=tournament_id).all()
        return [assignment.tag for assignment in assignments]
    
    @staticmethod
    def get_tournaments_by_tag(tag_slug):
        """Получить турниры по тегу"""
        tag = Tag.query.filter_by(slug=tag_slug).first()
        if not tag:
            return []
        
        assignments = TagTournament.query.filter_by(tag_id=tag.id).all()
        return [assignment.tournament for assignment in assignments]
    
    @staticmethod
    def get_popular_tags(limit=20):
        """Получить популярные теги"""
        return Tag.query.order_by(Tag.usage_count.desc()).limit(limit).all()
    
    @staticmethod
    def search_tags(query):
        """Поиск тегов по названию"""
        return Tag.query.filter(
            Tag.name.ilike(f'%{query}%')
        ).limit(20).all()
