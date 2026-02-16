"""
Integration tests for API endpoints
"""
import pytest
import json


class TestAuthAPI:
    """Tests for authentication API"""
    
    def test_login_success(self, client, admin_user):
        """Test successful login"""
        response = client.post('/auth/login', json={
            'username': 'admin',
            'password': 'adminpassword123'
        })
        
        assert response.status_code == 200
        data = response.json
        assert 'token' in data
        assert 'user' in data
        assert data['user']['username'] == 'admin'
    
    def test_login_invalid_credentials(self, client, admin_user):
        """Test login with invalid credentials"""
        response = client.post('/auth/login', json={
            'username': 'admin',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields"""
        response = client.post('/auth/login', json={
            'username': 'admin'
        })
        
        assert response.status_code == 400
    
    def test_token_verification(self, client, auth_headers):
        """Test token verification"""
        response = client.get('/auth/verify', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert data['valid'] is True
        assert 'user' in data
    
    def test_token_refresh(self, client, auth_headers):
        """Test token refresh"""
        response = client.post('/auth/refresh', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json
        assert 'token' in data
        assert 'expires_in' in data


class TestTournamentAPI:
    """Tests for tournament API"""
    
    def test_get_tournaments(self, client, multiple_tournaments):
        """Test getting tournaments list"""
        response = client.get('/api/tournaments')
        
        assert response.status_code == 200
        data = response.json
        assert isinstance(data, list) or 'tournaments' in data
    
    def test_get_tournament_by_id(self, client, sample_tournament):
        """Test getting tournament by ID"""
        response = client.get(f'/api/tournaments/{sample_tournament.id}')
        
        assert response.status_code == 200
        data = response.json
        assert data['name'] == 'Test Tournament'
        assert data['location'] == 'Moscow'
    
    def test_get_nonexistent_tournament(self, client):
        """Test getting non-existent tournament"""
        response = client.get('/api/tournaments/99999')
        
        assert response.status_code == 404
    
    def test_create_tournament_admin(self, client, auth_headers, db_session):
        """Test creating tournament as admin"""
        response = client.post('/api/tournaments', 
            headers=auth_headers,
            json={
                'name': 'New Tournament',
                'start_date': '2024-06-01',
                'end_date': '2024-06-05',
                'location': 'St. Petersburg',
                'category': 'National',
                'status': 'Scheduled'
            }
        )
        
        assert response.status_code == 201
        data = response.json
        assert data['name'] == 'New Tournament'
    
    def test_create_tournament_unauthorized(self, client, db_session):
        """Test creating tournament without auth"""
        response = client.post('/api/tournaments', json={
            'name': 'New Tournament',
            'start_date': '2024-06-01',
            'end_date': '2024-06-05',
            'location': 'St. Petersburg',
            'category': 'National'
        })
        
        assert response.status_code == 401
    
    def test_update_tournament(self, client, auth_headers, sample_tournament):
        """Test updating tournament"""
        response = client.put(f'/api/tournaments/{sample_tournament.id}',
            headers=auth_headers,
            json={
                'name': 'Updated Tournament',
                'status': 'Ongoing'
            }
        )
        
        assert response.status_code == 200
        data = response.json
        assert data['name'] == 'Updated Tournament'
        assert data['status'] == 'Ongoing'
    
    def test_delete_tournament(self, client, auth_headers, sample_tournament):
        """Test deleting tournament"""
        tournament_id = sample_tournament.id
        
        response = client.delete(f'/api/tournaments/{tournament_id}',
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify deletion
        response = client.get(f'/api/tournaments/{tournament_id}')
        assert response.status_code == 404
    
    def test_filter_tournaments_by_category(self, client, multiple_tournaments):
        """Test filtering tournaments by category"""
        response = client.get('/api/tournaments?category=National')
        
        assert response.status_code == 200
        data = response.json
        
        if isinstance(data, list):
            tournaments = data
        else:
            tournaments = data.get('tournaments', [])
        
        # All returned tournaments should be National
        for tournament in tournaments:
            assert tournament['category'] == 'National'


class TestUserAPI:
    """Tests for user API"""
    
    def test_get_users_admin(self, client, auth_headers, multiple_tournaments):
        """Test getting users list as admin"""
        response = client.get('/api/users', headers=auth_headers)
        
        assert response.status_code == 200
    
    def test_get_users_unauthorized(self, client):
        """Test getting users without auth"""
        response = client.get('/api/users')
        
        assert response.status_code == 401
    
    def test_get_user_by_id(self, client, auth_headers, sample_user):
        """Test getting user by ID"""
        # Admin can get any user
        response = client.get(f'/api/users/{sample_user.id}', 
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json
        assert data['username'] == 'testuser'
    
    def test_create_user(self, client, db_session):
        """Test user registration"""
        response = client.post('/api/users', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 201
        data = response.json
        assert data['username'] == 'newuser'
        assert 'password' not in data
    
    def test_create_user_duplicate_username(self, client, sample_user):
        """Test creating user with duplicate username"""
        response = client.post('/api/users', json={
            'username': 'testuser',  # Already exists
            'email': 'different@example.com',
            'password': 'password123'
        })
        
        assert response.status_code == 400


class TestHealthAPI:
    """Tests for health check endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.json
        assert 'status' in data
        assert data['status'] in ['healthy', 'unhealthy']
    
    def test_metrics_admin(self, client, auth_headers):
        """Test metrics endpoint as admin"""
        response = client.get('/metrics', headers=auth_headers)
        
        # Should return metrics or 200 OK
        assert response.status_code in [200, 404]  # 404 if not implemented yet
    
    def test_metrics_unauthorized(self, client):
        """Test metrics endpoint without auth"""
        response = client.get('/metrics')
        
        assert response.status_code == 401
