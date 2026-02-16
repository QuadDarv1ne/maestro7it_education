"""
Интеграционные тесты API
"""
import pytest
import json
from datetime import datetime, timedelta


class TestTournamentAPI:
    """Тесты API турниров"""
    
    def test_get_tournaments(self, client, multiple_tournaments):
        """Тест получения списка турниров"""
        response = client.get('/api/tournaments')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'tournaments' in data
        assert len(data['tournaments']) > 0
    
    def test_get_tournament_by_id(self, client, sample_tournament):
        """Тест получения турнира по ID"""
        response = client.get(f'/api/tournaments/{sample_tournament.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == sample_tournament.id
        assert data['name'] == sample_tournament.name
    
    def test_get_nonexistent_tournament(self, client):
        """Тест получения несуществующего турнира"""
        response = client.get('/api/tournaments/99999')
        
        assert response.status_code == 404
    
    def test_search_tournaments(self, client, multiple_tournaments):
        """Тест поиска турниров"""
        response = client.get('/api/tournaments/search?q=Турнир')
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0
    
    def test_filter_tournaments_by_category(self, client, multiple_tournaments):
        """Тест фильтрации по категории"""
        response = client.get('/api/tournaments?category=FIDE')
        
        assert response.status_code == 200
        data = response.get_json()
        for tournament in data['tournaments']:
            assert tournament['category'] == 'FIDE'
    
    def test_create_tournament_unauthorized(self, client):
        """Тест создания турнира без авторизации"""
        tournament_data = {
            'name': 'Новый турнир',
            'start_date': (datetime.now() + timedelta(days=30)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=32)).isoformat(),
            'location': 'Москва',
            'category': 'Regional'
        }
        
        response = client.post('/api/tournaments',
                             json=tournament_data)
        
        assert response.status_code == 401
    
    def test_create_tournament_authorized(self, client, auth_headers):
        """Тест создания турнира с авторизацией"""
        tournament_data = {
            'name': 'Новый турнир',
            'start_date': (datetime.now() + timedelta(days=30)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=32)).isoformat(),
            'location': 'Москва',
            'category': 'Regional',
            'status': 'Scheduled'
        }
        
        response = client.post('/api/tournaments',
                             json=tournament_data,
                             headers=auth_headers)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['name'] == tournament_data['name']
    
    def test_update_tournament(self, client, auth_headers, sample_tournament):
        """Тест обновления турнира"""
        update_data = {
            'name': 'Обновленное название',
            'location': 'Санкт-Петербург'
        }
        
        response = client.put(f'/api/tournaments/{sample_tournament.id}',
                            json=update_data,
                            headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['name'] == update_data['name']
        assert data['location'] == update_data['location']
    
    def test_delete_tournament(self, client, auth_headers, sample_tournament):
        """Тест удаления турнира"""
        response = client.delete(f'/api/tournaments/{sample_tournament.id}',
                               headers=auth_headers)
        
        assert response.status_code == 204
        
        # Проверяем, что турнир удален
        get_response = client.get(f'/api/tournaments/{sample_tournament.id}')
        assert get_response.status_code == 404


class TestAuthAPI:
    """Тесты API аутентификации"""
    
    def test_login_success(self, client, admin_user):
        """Тест успешной авторизации"""
        response = client.post('/auth/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
    
    def test_login_invalid_credentials(self, client, admin_user):
        """Тест авторизации с неверными данными"""
        response = client.post('/auth/login', json={
            'username': 'admin',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client):
        """Тест авторизации несуществующего пользователя"""
        response = client.post('/auth/login', json={
            'username': 'nonexistent',
            'password': 'password'
        })
        
        assert response.status_code == 401
    
    def test_refresh_token(self, client, admin_user):
        """Тест обновления токена"""
        # Получаем токены
        login_response = client.post('/auth/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        refresh_token = login_response.get_json()['refresh_token']
        
        # Обновляем токен
        response = client.post('/auth/refresh',
                             headers={'Authorization': f'Bearer {refresh_token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
    
    def test_verify_token(self, client, auth_headers):
        """Тест проверки токена"""
        response = client.get('/auth/verify', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['valid'] is True


class TestUserAPI:
    """Тесты API пользователей"""
    
    def test_register_user(self, client):
        """Тест регистрации пользователя"""
        user_data = {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123'
        }
        
        response = client.post('/api/users', json=user_data)
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['username'] == user_data['username']
        assert data['email'] == user_data['email']
        assert 'password' not in data
    
    def test_register_duplicate_username(self, client, regular_user):
        """Тест регистрации с существующим username"""
        user_data = {
            'username': 'user',  # Уже существует
            'email': 'new@test.com',
            'password': 'password123'
        }
        
        response = client.post('/api/users', json=user_data)
        
        assert response.status_code == 400
    
    def test_get_user_profile(self, client, auth_headers, admin_user):
        """Тест получения профиля пользователя"""
        response = client.get(f'/api/users/{admin_user.id}',
                            headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['username'] == admin_user.username
    
    def test_update_user_profile(self, client, auth_headers, admin_user):
        """Тест обновления профиля"""
        update_data = {
            'email': 'newemail@test.com'
        }
        
        response = client.put(f'/api/users/{admin_user.id}',
                            json=update_data,
                            headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['email'] == update_data['email']


class TestFavoritesAPI:
    """Тесты API избранного"""
    
    def test_add_favorite(self, client, auth_headers, sample_tournament):
        """Тест добавления в избранное"""
        response = client.post(f'/api/favorites/{sample_tournament.id}',
                             headers=auth_headers)
        
        assert response.status_code == 201
    
    def test_get_favorites(self, client, auth_headers, sample_tournament):
        """Тест получения избранного"""
        # Добавляем в избранное
        client.post(f'/api/favorites/{sample_tournament.id}',
                   headers=auth_headers)
        
        # Получаем список
        response = client.get('/api/favorites', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0
    
    def test_remove_favorite(self, client, auth_headers, sample_tournament):
        """Тест удаления из избранного"""
        # Добавляем
        client.post(f'/api/favorites/{sample_tournament.id}',
                   headers=auth_headers)
        
        # Удаляем
        response = client.delete(f'/api/favorites/{sample_tournament.id}',
                               headers=auth_headers)
        
        assert response.status_code == 204


class TestHealthAPI:
    """Тесты health check"""
    
    def test_health_check(self, client):
        """Тест health check endpoint"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_metrics_unauthorized(self, client):
        """Тест метрик без авторизации"""
        response = client.get('/metrics')
        
        assert response.status_code == 401
    
    def test_metrics_authorized(self, client, auth_headers):
        """Тест метрик с авторизацией"""
        response = client.get('/metrics', headers=auth_headers)
        
        assert response.status_code == 200
