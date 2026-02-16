"""
Integration тесты для Auth API
"""
import pytest
import json
from datetime import datetime, timedelta


class TestAuthRegistration:
    """Тесты регистрации"""
    
    def test_register_success(self, client):
        """Тест успешной регистрации"""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'SecurePass123!'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'User registered successfully'
        assert data['user']['username'] == 'newuser'
    
    def test_register_weak_password(self, client):
        """Тест регистрации со слабым паролем"""
        response = client.post('/auth/register', json={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'weak'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
    
    def test_register_duplicate_username(self, client, regular_user):
        """Тест регистрации с существующим username"""
        response = client.post('/auth/register', json={
            'username': 'user',  # Уже существует
            'email': 'another@test.com',
            'password': 'SecurePass123!'
        })
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'already exists' in data['error'].lower()
    
    def test_register_missing_fields(self, client):
        """Тест регистрации без обязательных полей"""
        response = client.post('/auth/register', json={
            'username': 'newuser'
        })
        
        assert response.status_code == 400


class TestAuthLogin:
    """Тесты входа"""
    
    def test_login_success(self, client, regular_user):
        """Тест успешного входа"""
        response = client.post('/auth/login', json={
            'username': 'user',
            'password': 'user123'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
        assert 'refresh_token' in data
        assert data['user']['username'] == 'user'
    
    def test_login_invalid_credentials(self, client, regular_user):
        """Тест входа с неверными данными"""
        response = client.post('/auth/login', json={
            'username': 'user',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401
        data = response.get_json()
        assert 'error' in data
    
    def test_login_nonexistent_user(self, client):
        """Тест входа несуществующего пользователя"""
        response = client.post('/auth/login', json={
            'username': 'nonexistent',
            'password': 'password'
        })
        
        assert response.status_code == 401
    
    def test_login_missing_credentials(self, client):
        """Тест входа без данных"""
        response = client.post('/auth/login', json={
            'username': 'user'
        })
        
        assert response.status_code == 400
    
    def test_login_rate_limiting(self, client, regular_user):
        """Тест rate limiting при входе"""
        # Делаем много неудачных попыток
        for _ in range(11):
            response = client.post('/auth/login', json={
                'username': 'user',
                'password': 'wrongpassword'
            })
        
        # Последняя попытка должна быть заблокирована
        assert response.status_code == 429


class TestAuthRefresh:
    """Тесты обновления токена"""
    
    def test_refresh_token_success(self, client, regular_user):
        """Тест успешного обновления токена"""
        # Получаем токены
        login_response = client.post('/auth/login', json={
            'username': 'user',
            'password': 'user123'
        })
        
        refresh_token = login_response.get_json()['refresh_token']
        
        # Обновляем токен
        response = client.post('/auth/refresh',
                             headers={'Authorization': f'Bearer {refresh_token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'access_token' in data
    
    def test_refresh_token_invalid(self, client):
        """Тест обновления с неверным токеном"""
        response = client.post('/auth/refresh',
                             headers={'Authorization': 'Bearer invalid_token'})
        
        assert response.status_code == 401
    
    def test_refresh_token_missing(self, client):
        """Тест обновления без токена"""
        response = client.post('/auth/refresh')
        
        assert response.status_code == 401


class TestAuthLogout:
    """Тесты выхода"""
    
    def test_logout_success(self, client, auth_headers):
        """Тест успешного выхода"""
        response = client.post('/auth/logout', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Logged out successfully'
    
    def test_logout_without_token(self, client):
        """Тест выхода без токена"""
        response = client.post('/auth/logout')
        
        assert response.status_code == 401


class TestAuthVerify:
    """Тесты проверки токена"""
    
    def test_verify_valid_token(self, client, auth_headers):
        """Тест проверки валидного токена"""
        response = client.get('/auth/verify', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['valid'] is True
        assert 'user' in data
    
    def test_verify_invalid_token(self, client):
        """Тест проверки невалидного токена"""
        response = client.get('/auth/verify',
                            headers={'Authorization': 'Bearer invalid_token'})
        
        assert response.status_code == 401


class TestAuthChangePassword:
    """Тесты смены пароля"""
    
    def test_change_password_success(self, client, auth_headers, regular_user):
        """Тест успешной смены пароля"""
        response = client.post('/auth/change-password',
                             json={
                                 'old_password': 'user123',
                                 'new_password': 'NewSecurePass123!'
                             },
                             headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'successfully' in data['message'].lower()
    
    def test_change_password_wrong_old(self, client, auth_headers):
        """Тест смены пароля с неверным старым паролем"""
        response = client.post('/auth/change-password',
                             json={
                                 'old_password': 'wrongpassword',
                                 'new_password': 'NewSecurePass123!'
                             },
                             headers=auth_headers)
        
        assert response.status_code == 401
    
    def test_change_password_weak_new(self, client, auth_headers):
        """Тест смены пароля на слабый"""
        response = client.post('/auth/change-password',
                             json={
                                 'old_password': 'user123',
                                 'new_password': 'weak'
                             },
                             headers=auth_headers)
        
        assert response.status_code == 400


class TestAuth2FA:
    """Тесты двухфакторной аутентификации"""
    
    def test_setup_2fa(self, client, auth_headers):
        """Тест настройки 2FA"""
        response = client.post('/auth/2fa/setup', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'secret' in data
        assert 'qr_code_url' in data
    
    def test_enable_2fa_invalid_code(self, client, auth_headers):
        """Тест включения 2FA с неверным кодом"""
        # Сначала настраиваем
        client.post('/auth/2fa/setup', headers=auth_headers)
        
        # Пытаемся включить с неверным кодом
        response = client.post('/auth/2fa/enable',
                             json={'totp_code': '000000'},
                             headers=auth_headers)
        
        assert response.status_code == 401
    
    def test_disable_2fa_without_setup(self, client, auth_headers):
        """Тест отключения 2FA без настройки"""
        response = client.post('/auth/2fa/disable',
                             json={
                                 'password': 'user123',
                                 'totp_code': '123456'
                             },
                             headers=auth_headers)
        
        assert response.status_code == 400


class TestAuthAuditLog:
    """Тесты audit log"""
    
    def test_get_audit_log_admin(self, client, admin_user):
        """Тест получения audit log администратором"""
        # Логинимся как админ
        login_response = client.post('/auth/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        
        token = login_response.get_json()['access_token']
        
        # Получаем audit log
        response = client.get('/auth/audit-log',
                            headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'logs' in data
        assert 'count' in data
    
    def test_get_audit_log_non_admin(self, client, auth_headers):
        """Тест получения audit log не-администратором"""
        response = client.get('/auth/audit-log', headers=auth_headers)
        
        assert response.status_code == 403
    
    def test_get_audit_log_with_filters(self, client, admin_user):
        """Тест получения audit log с фильтрами"""
        # Логинимся как админ
        login_response = client.post('/auth/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        
        token = login_response.get_json()['access_token']
        
        # Получаем audit log с фильтром
        response = client.get('/auth/audit-log?action=login&limit=10',
                            headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'logs' in data


class TestAuthLoginAttempts:
    """Тесты попыток входа"""
    
    def test_get_login_attempts_admin(self, client, admin_user):
        """Тест получения попыток входа администратором"""
        # Логинимся как админ
        login_response = client.post('/auth/login', json={
            'username': 'admin',
            'password': 'admin123'
        })
        
        token = login_response.get_json()['access_token']
        
        # Получаем попытки входа
        response = client.get('/auth/login-attempts',
                            headers={'Authorization': f'Bearer {token}'})
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'attempts' in data
        assert 'count' in data
    
    def test_get_login_attempts_non_admin(self, client, auth_headers):
        """Тест получения попыток входа не-администратором"""
        response = client.get('/auth/login-attempts', headers=auth_headers)
        
        assert response.status_code == 403
