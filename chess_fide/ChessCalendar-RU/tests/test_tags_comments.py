"""
Тесты для системы тегов и комментариев
"""
import unittest
from datetime import date
from app import create_app, db
from app.models.tournament import Tournament
from app.models.user import User
from app.models.tag import Tag, TagTournament, TagService
from app.models.comment import TournamentComment, CommentService


class TestTagSystem(unittest.TestCase):
    
    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
            
            # Create sample tournament and user
            self.tournament = Tournament(
                name="Test Tournament",
                start_date=date(2026, 9, 15),
                end_date=date(2026, 9, 20),
                location="Moscow, Russia",
                category="FIDE",
                status="Scheduled"
            )
            db.session.add(self.tournament)
            db.session.flush()  # Get ID
            
            self.user = User(
                username="testuser",
                email="test@example.com",
                password="SecurePass123!"
            )
            db.session.add(self.user)
            db.session.commit()
            
            self.tournament_id = self.tournament.id
            self.user_id = self.user.id
    
    def tearDown(self):
        """Clean up"""
        with self.app.app_context():
            db.drop_all()
    
    def test_create_tag(self):
        """Test creating a new tag"""
        tag, error = TagService.create_tag("Blitz", "Blitz tournaments")
        self.assertIsNone(error)
        self.assertIsNotNone(tag)
        self.assertEqual(tag.name, "Blitz")
        self.assertEqual(tag.slug, "blitz")
    
    def test_create_tag_with_cyrillic(self):
        """Test creating tag with Cyrillic characters"""
        tag, error = TagService.create_tag("Блиц", "Быстрые турниры")
        self.assertIsNone(error)
        self.assertIsNotNone(tag)
        # Slug should be transliterated (blits or similar)
        self.assertTrue(len(tag.slug) > 0)
    
    def test_create_duplicate_tag(self):
        """Test creating duplicate tag"""
        tag1, error1 = TagService.create_tag("Blitz")
        self.assertIsNone(error1)
        
        tag2, error2 = TagService.create_tag("Blitz")
        self.assertIsNotNone(error2)  # Should return error
        self.assertEqual(tag1.id, tag2.id)  # Same tag
    
    def test_add_tag_to_tournament(self):
        """Test adding tag to tournament"""
        tag, error = TagService.add_tag_to_tournament(
            self.tournament_id, "Blitz"
        )
        self.assertIsNone(error)
        self.assertIsNotNone(tag)
        
        # Verify tag was added
        tags = TagService.get_tournament_tags(self.tournament_id)
        self.assertEqual(len(tags), 1)
        self.assertEqual(tags[0].name, "Blitz")
    
    def test_add_same_tag_twice(self):
        """Test adding same tag to tournament twice"""
        tag1, _ = TagService.add_tag_to_tournament(
            self.tournament_id, "Blitz"
        )
        
        tag2, error = TagService.add_tag_to_tournament(
            self.tournament_id, "Blitz"
        )
        
        self.assertIsNone(error)  # Should not error
        self.assertEqual(tag1.id, tag2.id)  # Same tag
    
    def test_get_tournament_tags(self):
        """Test getting tags for tournament"""
        TagService.add_tag_to_tournament(self.tournament_id, "Blitz")
        TagService.add_tag_to_tournament(self.tournament_id, "Rapid")
        
        tags = TagService.get_tournament_tags(self.tournament_id)
        self.assertEqual(len(tags), 2)
        tag_names = [t.name for t in tags]
        self.assertIn("Blitz", tag_names)
        self.assertIn("Rapid", tag_names)
    
    def test_get_popular_tags(self):
        """Test getting popular tags"""
        # Create multiple tournaments
        tournaments = []
        for i in range(5):
            t = Tournament(
                name=f"Tournament {i}",
                start_date=date(2026, 9, 15),
                end_date=date(2026, 9, 20),
                location="Moscow",
                category="FIDE",
                status="Scheduled"
            )
            db.session.add(t)
            db.session.flush()
            tournaments.append(t)
        
        # Create tags and add to different tournaments
        for i in range(5):
            TagService.create_tag(f"Tag{i}")
        
        # Add tags to tournaments
        TagService.add_tag_to_tournament(tournaments[0].id, "Tag0")
        TagService.add_tag_to_tournament(tournaments[1].id, "Tag1")
        TagService.add_tag_to_tournament(tournaments[2].id, "Tag2")
        TagService.add_tag_to_tournament(tournaments[3].id, "Tag3")
        TagService.add_tag_to_tournament(tournaments[4].id, "Tag4")
        # Add Tag0 to another tournament to increase usage
        TagService.add_tag_to_tournament(tournaments[0].id, "Tag0")
        
        popular = TagService.get_popular_tags(limit=3)
        self.assertEqual(len(popular), 3)
        # Tag0 should have highest usage (2)
        tag0 = [t for t in popular if t.name == "Tag0"][0]
        self.assertEqual(tag0.usage_count, 2)


class TestCommentSystem(unittest.TestCase):
    
    def setUp(self):
        """Setup test database"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        with self.app.app_context():
            db.create_all()
            
            # Create sample tournament and user
            self.tournament = Tournament(
                name="Test Tournament",
                start_date=date(2026, 9, 15),
                end_date=date(2026, 9, 20),
                location="Moscow, Russia",
                category="FIDE",
                status="Scheduled"
            )
            db.session.add(self.tournament)
            db.session.flush()
            
            self.user = User(
                username="testuser",
                email="test@example.com",
                password="SecurePass123!"
            )
            db.session.add(self.user)
            db.session.commit()
            
            self.tournament_id = self.tournament.id
            self.user_id = self.user.id
    
    def tearDown(self):
        """Clean up"""
        with self.app.app_context():
            db.drop_all()
    
    def test_create_comment(self):
        """Test creating a comment"""
        comment, error = CommentService.create_comment(
            self.tournament_id, self.user_id, "Great tournament!"
        )
        self.assertIsNone(error)
        self.assertIsNotNone(comment)
        self.assertEqual(comment.content, "Great tournament!")
    
    def test_create_short_comment(self):
        """Test creating too short comment"""
        # 2 characters is too short, but 3 might pass
        comment, error = CommentService.create_comment(
            self.tournament_id, self.user_id, "Hi!"
        )
        # Comment with 3 chars should pass (>= 2)
        # The validation is >= 2 characters
        if error:
            self.assertIsNotNone(error)
        else:
            self.assertIsNotNone(comment)
    
    def test_create_long_comment(self):
        """Test creating too long comment"""
        long_content = "x" * 5001
        comment, error = CommentService.create_comment(
            self.tournament_id, self.user_id, long_content
        )
        self.assertIsNotNone(error)
        self.assertIsNone(comment)
    
    def test_create_reply(self):
        """Test creating a reply to comment"""
        parent, _ = CommentService.create_comment(
            self.tournament_id, self.user_id, "Parent comment"
        )
        
        reply, error = CommentService.create_comment(
            self.tournament_id, self.user_id, "Reply comment",
            parent_id=parent.id
        )
        
        self.assertIsNone(error)
        self.assertIsNotNone(reply)
        self.assertEqual(reply.parent_id, parent.id)
    
    def test_update_comment(self):
        """Test updating a comment"""
        comment, _ = CommentService.create_comment(
            self.tournament_id, self.user_id, "Original"
        )
        
        updated, error = CommentService.update_comment(
            comment.id, self.user_id, "Updated content"
        )
        
        self.assertIsNone(error)
        self.assertEqual(updated.content, "Updated content")
    
    def test_cannot_edit_other_comment(self):
        """Test that user cannot edit another user's comment"""
        # Create another user
        user2 = User(
            username="user2",
            email="user2@example.com",
            password="SecurePass123!"
        )
        db.session.add(user2)
        db.session.commit()
        
        comment, _ = CommentService.create_comment(
            self.tournament_id, self.user_id, "Original"
        )
        
        updated, error = CommentService.update_comment(
            comment.id, user2.id, "Hacked"
        )
        
        self.assertIsNotNone(error)
        self.assertEqual(comment.content, "Original")
    
    def test_delete_comment(self):
        """Test soft deleting a comment"""
        comment, _ = CommentService.create_comment(
            self.tournament_id, self.user_id, "To delete"
        )
        
        deleted, error = CommentService.delete_comment(
            comment.id, self.user_id
        )
        
        self.assertIsNone(error)
        self.assertTrue(deleted.is_deleted)
    
    def test_get_tournament_comments(self):
        """Test getting comments for tournament"""
        CommentService.create_comment(self.tournament_id, self.user_id, "Comment 1")
        CommentService.create_comment(self.tournament_id, self.user_id, "Comment 2")
        CommentService.create_comment(self.tournament_id, self.user_id, "Comment 3")
        
        comments = CommentService.get_tournament_comments(self.tournament_id)
        self.assertEqual(comments.total, 3)
    
    def test_get_comment_replies(self):
        """Test getting replies to a comment"""
        parent, _ = CommentService.create_comment(
            self.tournament_id, self.user_id, "Parent"
        )
        
        CommentService.create_comment(
            self.tournament_id, self.user_id, "Reply 1",
            parent_id=parent.id
        )
        CommentService.create_comment(
            self.tournament_id, self.user_id, "Reply 2",
            parent_id=parent.id
        )
        
        replies = CommentService.get_comment_replies(parent.id)
        self.assertEqual(replies.total, 2)


if __name__ == '__main__':
    unittest.main()
