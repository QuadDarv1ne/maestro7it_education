"""
Unit tests for Celery tasks
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta


class TestParserTasks:
    """Tests for parser tasks"""
    
    @patch('app.tasks.parser_tasks.FIDEParser')
    @patch('app.tasks.parser_tasks.db')
    def test_parse_fide_tournaments(self, mock_db, mock_parser_class):
        """Test FIDE tournament parsing"""
        from app.tasks.parser_tasks import parse_fide_tournaments
        
        # Mock parser
        mock_parser = Mock()
        mock_parser.parse_tournaments.return_value = [
            {
                'name': 'Test Tournament',
                'start_date': datetime.now().date(),
                'end_date': (datetime.now() + timedelta(days=3)).date(),
                'location': 'Moscow',
                'category': 'FIDE',
                'fide_id': 'FIDE123'
            }
        ]
        mock_parser_class.return_value = mock_parser
        
        # Run task
        result = parse_fide_tournaments()
        
        # Verify
        assert result['status'] == 'success'
        assert result['total'] == 1
        mock_parser.parse_tournaments.assert_called_once()
    
    @patch('app.tasks.parser_tasks.CFRParser')
    def test_parse_cfr_tournaments(self, mock_parser_class):
        """Test CFR tournament parsing"""
        from app.tasks.parser_tasks import parse_cfr_tournaments
        
        # Mock parser
        mock_parser = Mock()
        mock_parser.parse_tournaments.return_value = []
        mock_parser_class.return_value = mock_parser
        
        # Run task
        result = parse_cfr_tournaments()
        
        # Verify
        assert result['status'] == 'success'
        mock_parser.parse_tournaments.assert_called_once()


class TestNotificationTasks:
    """Tests for notification tasks"""
    
    @patch('app.tasks.notification_tasks.db')
    def test_send_notification(self, mock_db):
        """Test sending notification"""
        from app.tasks.notification_tasks import send_notification
        
        # Mock user
        mock_user = Mock()
        mock_user.id = 1
        
        with patch('app.tasks.notification_tasks.User') as mock_user_class:
            mock_user_class.query.get.return_value = mock_user
            
            # Run task
            result = send_notification(1, 'Test Title', 'Test Message', 'info')
            
            # Verify
            assert result['status'] == 'success'
            assert result['user_id'] == 1
    
    @patch('app.tasks.notification_tasks.Notification')
    @patch('app.tasks.notification_tasks.db')
    def test_send_pending_notifications(self, mock_db, mock_notification_class):
        """Test sending pending notifications"""
        from app.tasks.notification_tasks import send_pending_notifications
        
        # Mock notifications
        mock_notification_class.query.filter.return_value.limit.return_value.all.return_value = []
        
        # Run task
        result = send_pending_notifications()
        
        # Verify
        assert result['status'] == 'success'
        assert result['sent'] == 0


class TestAnalyticsTasks:
    """Tests for analytics tasks"""
    
    @patch('app.tasks.analytics_tasks.Tournament')
    @patch('app.tasks.analytics_tasks.User')
    @patch('app.tasks.analytics_tasks.cache_manager')
    def test_generate_daily_report(self, mock_cache, mock_user_class, mock_tournament_class):
        """Test daily report generation"""
        from app.tasks.analytics_tasks import generate_daily_report
        
        # Mock queries
        mock_tournament_class.query.filter.return_value.count.return_value = 5
        mock_user_class.query.filter.return_value.count.return_value = 10
        
        # Run task
        result = generate_daily_report()
        
        # Verify
        assert 'date' in result
        assert 'new_tournaments' in result
        assert 'new_users' in result
        mock_cache.set.assert_called_once()
    
    @patch('app.tasks.analytics_tasks.recommendation_service')
    @patch('app.tasks.analytics_tasks.User')
    @patch('app.tasks.analytics_tasks.cache_manager')
    def test_update_recommendations_cache(self, mock_cache, mock_user_class, mock_rec_service):
        """Test recommendations cache update"""
        from app.tasks.analytics_tasks import update_recommendations_cache
        
        # Mock users
        mock_user1 = Mock()
        mock_user1.id = 1
        mock_user2 = Mock()
        mock_user2.id = 2
        
        mock_user_class.query.filter_by.return_value.all.return_value = [mock_user1, mock_user2]
        mock_rec_service.get_recommendations.return_value = []
        
        # Run task
        result = update_recommendations_cache()
        
        # Verify
        assert result['status'] == 'success'
        assert result['updated'] == 2


class TestMaintenanceTasks:
    """Tests for maintenance tasks"""
    
    @patch('app.tasks.maintenance_tasks.Notification')
    @patch('app.tasks.maintenance_tasks.db')
    def test_cleanup_old_data(self, mock_db, mock_notification_class):
        """Test old data cleanup"""
        from app.tasks.maintenance_tasks import cleanup_old_data
        
        # Mock old notifications
        mock_notification_class.query.filter.return_value.all.return_value = []
        
        # Run task
        result = cleanup_old_data()
        
        # Verify
        assert result['status'] == 'success'
        assert 'deleted_notifications' in result
    
    @patch('app.tasks.maintenance_tasks.DatabaseBackupManager')
    def test_backup_database(self, mock_backup_class):
        """Test database backup"""
        from app.tasks.maintenance_tasks import backup_database
        
        # Mock backup manager
        mock_backup = Mock()
        mock_backup.create_compressed_backup.return_value = '/path/to/backup.tar.gz'
        mock_backup_class.return_value = mock_backup
        
        # Run task
        result = backup_database()
        
        # Verify
        assert result['status'] == 'success'
        assert 'backup_path' in result
        mock_backup.create_compressed_backup.assert_called_once()
    
    @patch('app.tasks.maintenance_tasks.db')
    def test_check_system_health(self, mock_db):
        """Test system health check"""
        from app.tasks.maintenance_tasks import check_system_health
        
        # Mock database check
        mock_db.session.execute.return_value = None
        
        # Run task
        result = check_system_health()
        
        # Verify
        assert 'timestamp' in result
        assert 'database' in result
        assert 'status' in result
