from app import db
from app.models.user import User
from app.models.tournament import Tournament
from app.models.forum import ForumThread, ForumPost
from datetime import datetime


class ForumService:
    """Service for handling forum operations"""
    
    @staticmethod
    def create_thread(tournament_id, title, author_id, content=None):
        """Create a new forum thread with an optional first post"""
        # Validate inputs
        tournament = Tournament.query.get(tournament_id)
        if not tournament:
            raise ValueError("Tournament not found")
        
        author = User.query.get(author_id)
        if not author or not author.is_regular_user:
            raise ValueError("Invalid author")
        
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        
        # Create the thread
        thread = ForumThread(tournament_id=tournament_id, title=title, author_id=author_id)
        db.session.add(thread)
        db.session.flush()  # Get the thread ID without committing
        
        # If content is provided, create the first post
        if content:
            post = ForumPost(thread_id=thread.id, author_id=author_id, content=content)
            db.session.add(post)
        
        db.session.commit()
        return thread
    
    @staticmethod
    def create_post(thread_id, author_id, content):
        """Create a new post in a thread"""
        # Validate inputs
        thread = ForumThread.query.get(thread_id)
        if not thread:
            raise ValueError("Thread not found")
        
        if thread.is_locked:
            raise ValueError("This thread is locked")
        
        author = User.query.get(author_id)
        if not author or not author.is_regular_user:
            raise ValueError("Invalid author")
        
        if not content or len(content.strip()) == 0:
            raise ValueError("Content cannot be empty")
        
        # Create the post
        post = ForumPost(thread_id=thread_id, author_id=author_id, content=content)
        db.session.add(post)
        db.session.commit()
        
        # Update thread timestamp
        thread.updated_at = datetime.utcnow()
        db.session.commit()
        
        return post
    
    @staticmethod
    def get_thread_with_posts(thread_id):
        """Get a thread with its posts"""
        thread = ForumThread.query.get(thread_id)
        if not thread:
            return None
        
        # Increment view count
        thread.views_count += 1
        db.session.commit()
        
        # Get posts ordered by creation date
        posts = ForumPost.query.filter_by(thread_id=thread_id).order_by(ForumPost.created_at.asc()).all()
        
        return {
            'thread': thread.to_dict(),
            'posts': [post.to_dict() for post in posts]
        }
    
    @staticmethod
    def get_threads_for_tournament(tournament_id, page=1, per_page=10, sort_by='updated'):
        """Get threads for a tournament with pagination"""
        query = ForumThread.query.filter_by(tournament_id=tournament_id)
        
        # Apply sorting
        if sort_by == 'updated':
            query = query.order_by(ForumThread.updated_at.desc())
        elif sort_by == 'created':
            query = query.order_by(ForumThread.created_at.desc())
        elif sort_by == 'pinned':
            query = query.order_by(ForumThread.is_pinned.desc(), ForumThread.updated_at.desc())
        
        # Apply pagination
        threads = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'threads': [thread.to_dict() for thread in threads.items],
            'pagination': {
                'page': threads.page,
                'pages': threads.pages,
                'per_page': threads.per_page,
                'total': threads.total
            }
        }
    
    @staticmethod
    def lock_thread(thread_id, admin_user_id):
        """Lock a thread (admin function)"""
        thread = ForumThread.query.get(thread_id)
        if not thread:
            raise ValueError("Thread not found")
        
        # Verify admin rights (in a real app, we'd check admin permissions)
        admin_user = User.query.get(admin_user_id)
        if not admin_user or not admin_user.is_admin:
            raise ValueError("Insufficient permissions")
        
        thread.is_locked = True
        db.session.commit()
        return thread
    
    @staticmethod
    def pin_thread(thread_id, admin_user_id):
        """Pin a thread (admin function)"""
        thread = ForumThread.query.get(thread_id)
        if not thread:
            raise ValueError("Thread not found")
        
        # Verify admin rights
        admin_user = User.query.get(admin_user_id)
        if not admin_user or not admin_user.is_admin:
            raise ValueError("Insufficient permissions")
        
        thread.is_pinned = True
        db.session.commit()
        return thread
    
    @staticmethod
    def unpin_thread(thread_id, admin_user_id):
        """Unpin a thread (admin function)"""
        thread = ForumThread.query.get(thread_id)
        if not thread:
            raise ValueError("Thread not found")
        
        # Verify admin rights
        admin_user = User.query.get(admin_user_id)
        if not admin_user or not admin_user.is_admin:
            raise ValueError("Insufficient permissions")
        
        thread.is_pinned = False
        db.session.commit()
        return thread
    
    @staticmethod
    def delete_post(post_id, user_id):
        """Delete a post (user can delete own post, admin can delete any)"""
        post = ForumPost.query.get(post_id)
        if not post:
            raise ValueError("Post not found")
        
        user = User.query.get(user_id)
        if not user:
            raise ValueError("Invalid user")
        
        # Check permissions
        if not (user.id == post.author_id or user.is_admin):
            raise ValueError("Insufficient permissions")
        
        db.session.delete(post)
        db.session.commit()
        return True
    
    @staticmethod
    def delete_thread(thread_id, user_id):
        """Delete a thread (admin only)"""
        thread = ForumThread.query.get(thread_id)
        if not thread:
            raise ValueError("Thread not found")
        
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            raise ValueError("Insufficient permissions")
        
        db.session.delete(thread)
        db.session.commit()
        return True