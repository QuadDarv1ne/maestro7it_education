"""
Unit tests for the Chess Stockfish Web application.
"""

import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app_improved import app, ChessGame

class ChessGameTestCase(unittest.TestCase):
    """Test cases for the ChessGame class"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = ChessGame()
    
    def test_game_initialization(self):
        """Test that a new game is properly initialized"""
        self.assertEqual(self.game.player_color, 'white')
        self.assertEqual(self.game.skill_level, 5)
        self.assertIsNone(self.game.engine)
        self.assertFalse(self.game.initialized)
        self.assertIsNone(self.game.last_move)
        self.assertEqual(self.game.move_history, [])
    
    def test_game_initialization_with_params(self):
        """Test that a new game is properly initialized with custom parameters"""
        game = ChessGame(player_color='black', skill_level=10)
        self.assertEqual(game.player_color, 'black')
        self.assertEqual(game.skill_level, 10)
    
    def test_move_history_tracking(self):
        """Test that move history is properly tracked"""
        self.game.move_history = ['e2e4', 'e7e5']
        self.assertEqual(len(self.game.move_history), 2)
        self.assertEqual(self.game.move_history[0], 'e2e4')
        self.assertEqual(self.game.move_history[1], 'e7e5')

class FlaskAppTestCase(unittest.TestCase):
    """Test cases for the Flask application"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        app.config['TESTING'] = True
    
    def test_index_page(self):
        """Test that the index page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Chess Stockfish Web', response.data)
    
    def test_health_endpoint(self):
        """Test that the health endpoint works"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        # Response should be JSON
        self.assertIn('application/json', response.content_type)
    
    def test_static_files(self):
        """Test that static files are served"""
        response = self.app.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/css', response.content_type)

if __name__ == '__main__':
    unittest.main()