"""
Система комментариев к турнирам
"""
from app import db
from datetime import datetime


class TournamentComment(db.Model):
    """Комментарий к турниру"""
    __tablename__ = 'tournament_comment'
    
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('tournament_comment.id'), nullable=True, index=True)  # Для ответов
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
    tournament = db.relationship('Tournament', backref=db.backref('comments', lazy='dynamic'))
    replies = db.relationship('TournamentComment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    
    __table_args__ = (
        db.Index('idx_tournament_created', 'tournament_id', 'created_at'),
        db.Index('idx_user_created', 'user_id', 'created_at'),
    )
    
    def __repr__(self):
        return f'<TournamentComment {self.id} by user {self.user_id}>'
    
    def to_dict(self):
        """Конвертация в словарь"""
        return {
            'id': self.id,
            'tournament_id': self.tournament_id,
            'user_id': self.user_id,
            'user_username': self.user.username if self.user else None,
            'user_avatar': self.user.avatar if hasattr(self.user, 'avatar') and self.user.avatar else None,
            'parent_id': self.parent_id,
            'content': self.content if not self.is_deleted else '[Удалено]',
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted,
            'replies_count': self.replies.count()
        }
    
    def can_edit(self, user_id):
        """Проверка, может ли пользователь редактировать комментарий"""
        return self.user_id == user_id
    
    def can_delete(self, user_id, is_admin=False):
        """Проверка, может ли пользователь удалить комментарий"""
        return self.user_id == user_id or is_admin


class CommentService:
    """Сервис для работы с комментариями"""
    
    @staticmethod
    def create_comment(tournament_id, user_id, content, parent_id=None):
        """Создать новый комментарий"""
        if not content or len(content.strip()) < 2:
            return None, "Comment must be at least 2 characters"
        
        if len(content) > 5000:
            return None, "Comment too long (max 5000 characters)"
        
        comment = TournamentComment(
            tournament_id=tournament_id,
            user_id=user_id,
            content=content,
            parent_id=parent_id
        )
        db.session.add(comment)
        db.session.commit()
        
        return comment, None
    
    @staticmethod
    def get_tournament_comments(tournament_id, page=1, per_page=20):
        """Получить комментарии турнира (тоplevel)"""
        comments = TournamentComment.query.filter_by(
            tournament_id=tournament_id,
            parent_id=None,
            is_deleted=False
        ).order_by(TournamentComment.created_at.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return comments
    
    @staticmethod
    def get_comment_replies(comment_id, page=1, per_page=10):
        """Получить ответы на комментарий"""
        replies = TournamentComment.query.filter_by(
            parent_id=comment_id,
            is_deleted=False
        ).order_by(TournamentComment.created_at.asc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return replies
    
    @staticmethod
    def update_comment(comment_id, user_id, new_content):
        """Обновить комментарий"""
        comment = TournamentComment.query.get(comment_id)
        if not comment:
            return None, "Comment not found"
        
        if not comment.can_edit(user_id):
            return None, "Permission denied"
        
        if not new_content or len(new_content.strip()) < 2:
            return None, "Comment must be at least 2 characters"
        
        comment.content = new_content
        db.session.commit()
        
        return comment, None
    
    @staticmethod
    def delete_comment(comment_id, user_id, is_admin=False):
        """Удалить комментарий (мягкое удаление)"""
        comment = TournamentComment.query.get(comment_id)
        if not comment:
            return None, "Comment not found"
        
        if not comment.can_delete(user_id, is_admin):
            return None, "Permission denied"
        
        comment.is_deleted = True
        db.session.commit()
        
        return comment, None
