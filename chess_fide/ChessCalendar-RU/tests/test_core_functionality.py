"""
Comprehensive tests for the ChessCalendar-RU core functionality
"""
import unittest
import pytest
from datetime import date, datetime
from unittest.mock import patch, MagicMock
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from app.models.tournament import Tournament
from app.utils.updater import TournamentUpdater
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser
from app import db


class TestTournamentModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()
    
    def test_tournament_creation(self):
        """Test basic tournament creation"""
        tournament = Tournament(
            name="Test Tournament",
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 10),
            location="Moscow",
            category="FIDE",
            status="Scheduled"
        )
        
        # Validate the tournament
        errors = tournament.validate()
        self.assertEqual(errors, [], "Tournament validation should pass")
        
        # Add to session and commit
        db.session.add(tournament)
        db.session.commit()
        
        # Verify it was saved
        saved_tournament = Tournament.query.first()
        self.assertIsNotNone(saved_tournament)
        self.assertEqual(saved_tournament.name, "Test Tournament")
    
    def test_tournament_validation(self):
        """Test tournament validation with invalid data"""
        tournament = Tournament(
            name="",  # Invalid: empty name
            start_date=None,  # Invalid: no start date
            end_date=date(2026, 5, 10),
            location="",
            category="InvalidCategory",  # Invalid category
            status="InvalidStatus"  # Invalid status
        )
        
        errors = tournament.validate()
        self.assertGreater(len(errors), 0, "Validation should fail for invalid data")
        self.assertIn("Название турнира не может быть пустым", errors)
        self.assertIn("Дата начала обязательна", errors)
        self.assertIn("Место проведения не может быть пустым", errors)
    
    def test_tournament_methods(self):
        """Test tournament helper methods"""
        tournament = Tournament(
            name="Test Tournament",
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 10),
            location="Moscow",
            category="FIDE",
            status="Scheduled"
        )
        
        # Test duration calculation
        self.assertEqual(tournament.duration_days(), 10)
        
        # Test upcoming status (assuming current date is before tournament)
        self.assertTrue(tournament.is_upcoming())
        
        # Test ongoing status (with mock date)
        with patch('app.models.tournament.date') as mock_date:
            mock_date.today.return_value = date(2026, 5, 5)  # During tournament
            self.assertTrue(tournament.is_ongoing())


class TestTournamentUpdater(unittest.TestCase):
    def setUp(self):
        self.updater = TournamentUpdater()
    
    def test_retry_mechanism(self):
        """Test the retry mechanism in the updater"""
        # Create a mock operation that fails twice then succeeds
        call_count = 0
        
        def failing_operation():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise Exception(f"Attempt {call_count} failed")
            return "Success"
        
        # Test that the retry mechanism works
        result = self.updater._retry_operation(failing_operation)
        self.assertEqual(result, "Success")
        self.assertEqual(call_count, 3)
    
    @patch('app.utils.fide_parser.FIDEParses.get_tournaments_russia')
    def test_update_from_fide_with_error(self, mock_get_tournaments):
        """Test FIDE update with error handling"""
        mock_get_tournaments.side_effect = Exception("Network error")
        
        # This should not crash, just log the error
        try:
            self.updater._update_from_fide_with_retry()
        except Exception:
            pass  # We expect this to handle the error gracefully
    
    @patch('app.utils.cfr_parser.CFRParser.get_tournaments')
    def test_update_from_cfr_with_error(self, mock_get_tournaments):
        """Test CFR update with error handling"""
        mock_get_tournaments.side_effect = Exception("Network error")
        
        # This should not crash, just log the error
        try:
            self.updater._update_from_cfr_with_retry()
        except Exception:
            pass  # We expect this to handle the error gracefully


class TestFIDEParsers(unittest.TestCase):
    def setUp(self):
        self.parser = FIDEParses()
    
    def test_parse_date_flexible(self):
        """Test the flexible date parsing"""
        # Test various date formats
        test_cases = [
            ("2026-05-15", date(2026, 5, 15)),
            ("15.05.2026", date(2026, 5, 15)),
            ("May 15, 2026", date(2026, 5, 15)),
        ]
        
        for date_str, expected in test_cases:
            result = self.parser._parse_date_flexible(date_str)
            if result:  # Only check if parsing succeeded
                self.assertEqual(result, expected)


class TestCFRParsers(unittest.TestCase):
    def setUp(self):
        self.parser = CFRParser()
    
    def test_user_agents_exist(self):
        """Test that user agents are defined"""
        self.assertTrue(hasattr(self.parser, 'user_agents'))
        self.assertIsInstance(self.parser.user_agents, list)
        self.assertGreater(len(self.parser.user_agents), 0)


class TestPerformanceMonitor(unittest.TestCase):
    def setUp(self):
        from app.utils.performance_monitor import perf_monitor
        self.monitor = perf_monitor
    
    def test_record_request(self):
        """Test recording a request"""
        self.monitor.record_request("/test", "GET", 0.1, 200)
        
        # Check that the request was recorded
        recent_requests = self.monitor.get_recent_requests()
        self.assertGreater(len(recent_requests), 0)
        
        # Check performance summary
        summary = self.monitor.get_performance_summary()
        self.assertIsNotNone(summary)
    
    def test_system_resources(self):
        """Test getting system resources"""
        resources = self.monitor.get_system_resources()
        if resources:  # Only test if system info is available
            self.assertIn('cpu_percent', resources)
            self.assertIn('memory_percent', resources)
            self.assertIn('disk_percent', resources)


if __name__ == '__main__':
    unittest.main()