from app import create_app

def test_app_creation():
    """Тест создания приложения"""
    try:
        app = create_app()
        print("Приложение успешно создано!")
        
        # Проверим, что все важные компоненты инициализированы
        with app.app_context():
            print("Контекст приложения работает")
            
        with app.test_client() as client:
            # Проверим главную страницу
            response = client.get('/')
            print(f"Главная страница: статус {response.status_code}")
            
            # Проверим страницу входа
            response = client.get('/login')
            print(f"Страница входа: статус {response.status_code}")
        
        return True
    except Exception as e:
        print(f"Ошибка при тестировании приложения: {e}")
        return False

if __name__ == "__main__":
    success = test_app_creation()
    if success:
        print("Тестирование прошло успешно!")
    else:
        print("Тестирование завершилось с ошибками.")