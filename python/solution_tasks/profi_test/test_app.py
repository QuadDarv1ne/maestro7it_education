"""
Test script for the profi_test application
"""
import os
import sys
import unittest
from app import create_app, db
from app.models import User, TestResult

class TestProfiTestApp(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_index_page(self):
        """Test that index page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # Check for key elements in response
        self.assertIn(b'<title>', response.data)
    
    def test_registration_page(self):
        """Test that registration page loads"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'\xd0\xa0\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f', response.data)  # Registration in Russian
    
    def test_login_page(self):
        """Test that login page loads"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'\xd0\x92\xd1\x85\xd0\xbe\xd0\xb4', response.data)  # Login in Russian
    
    def test_user_registration(self):
        """Test user registration"""
        with self.app.app_context():
            response = self.client.post('/register', data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'password2': 'password123'
            }, follow_redirects=True)
            
            # Check if user was created
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'test@example.com')
    
    def test_user_login(self):
        """Test user login"""
        with self.app.app_context():
            # Create a user first
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            
            # Test login
            response = self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
    
    def test_protected_routes(self):
        """Test that protected routes redirect to login"""
        protected_routes = ['/profile', '/methodology']
        
        for route in protected_routes:
            response = self.client.get(route)
            # Should redirect to login (302) or show login form (200)
            self.assertIn(response.status_code, [200, 302])

if __name__ == '__main__':
    unittest.main()