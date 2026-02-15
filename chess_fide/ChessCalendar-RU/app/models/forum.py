from app import db
from datetime import datetime
from app.models.user import User
from app.models.tournament import Tournament


class ForumThread(db.Model):
    """Represents a discussion thread for a tournament"""
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    is_locked = db.Column(db.Boolean, default=False)  # Whether the thread is locked for replies
    is_pinned = db.Column(db.Boolean, default=False)  # Whether the thread is pinned
    views_count = db.Column(db.Integer, default=0)  # Number of views
    
    # Relationships
    tournament = db.relationship('Tournament', backref=db.backref('forum_threads', lazy=True))
    author = db.relationship('User', backref=db.backref('forum_threads', lazy=True))
    posts = db.relationship('ForumPost', backref='thread', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, tournament_id, title, author_id):
        self.tournament_id = tournament_id
        self.title = title
        self.author_id = author_id
    
    def to_dict(self):
        return {
            'id': self.id,
            'tournament_id': self.tournament_id,
            'title': self.title,
            'author_id': self.author_id,
            'author_username': self.author.username if self.author else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_locked': self.is_locked,
            'is_pinned': self.is_pinned,
            'views_count': self.views_count,
            'posts_count': len(self.posts),
            'latest_post': self.get_latest_post()
        }
    
    def get_latest_post(self):
        """Get the latest post in the thread"""
        if self.posts:
            latest_post = max(self.posts, key=lambda p: p.created_at)
            return {
                'id': latest_post.id,
                'content_snippet': latest_post.content[:100] + '...' if len(latest_post.content) > 100 else latest_post.content,
                'author_username': latest_post.author.username if latest_post.author else None,
                'created_at': latest_post.created_at.isoformat()
            }
        return None
    
    def __repr__(self):
        return f'<ForumThread {self.title}>'


class ForumPost(db.Model):
    """Represents a post in a forum thread"""
    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('forum_thread.id'), nullable=False, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    author = db.relationship('User', backref=db.backref('forum_posts', lazy=True))
    
    def __init__(self, thread_id, author_id, content):
        self.thread_id = thread_id
        self.author_id = author_id
        self.content = content
    
    def to_dict(self):
        return {
            'id': self.id,
            'thread_id': self.thread_id,
            'author_id': self.author_id,
            'author_username': self.author.username if self.author else None,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def __repr__(self):
        return f'<ForumPost {self.id}>'