import requests
import time

def test_service_health(service_name, url):
    """Проверка состояния сервиса"""
    try:
        response = requests.get(f"{url}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name}: Работает")
            return True
        else:
            print(f"❌ {service_name}: Ошибка {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {service_name}: Недоступен - {str(e)}")
        return False

def test_tournament_service():
    """Тест сервиса турниров"""
    print("\n=== Тестирование Tournament Service ===")
    
    # Проверка состояния
    if not test_service_health("Tournament Service", "http://localhost:5001"):
        return False
    
    # Создание турнира
    tournament_data = {
        "name": "Тестовый турнир",
        "start_date": "2026-04-01",
        "end_date": "2026-04-10",
        "location": "Санкт-Петербург",
        "category": "Test Tournament"
    }
    
    try:
        response = requests.post("http://localhost:5001/tournaments", json=tournament_data)
        if response.status_code == 201:
            tournament = response.json()
            print(f"✅ Создан турнир: {tournament['name']}")
            
            # Получение списка турниров
            response = requests.get("http://localhost:5001/tournaments")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Получен список турниров: {data['pagination']['total']} турниров")
                return True
            else:
                print(f"❌ Ошибка получения списка турниров: {response.status_code}")
                return False
        else:
            print(f"❌ Ошибка создания турнира: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка тестирования турниров: {str(e)}")
        return False

def test_user_service():
    """Тест сервиса пользователей"""
    print("\n=== Тестирование User Service ===")
    
    # Проверка состояния
    if not test_service_health("User Service", "http://localhost:5002"):
        return False
    
    # Создание пользователя
    user_data = {
        "username": f"testuser_{int(time.time())}",
        "email": f"test{int(time.time())}@example.com",
        "password": "testpassword123",
        "first_name": "Тест",
        "last_name": "Пользователь"
    }
    
    try:
        response = requests.post("http://localhost:5002/users", json=user_data)
        if response.status_code == 201:
            user = response.json()
            print(f"✅ Создан пользователь: {user['username']}")
            
            # Аутентификация
            auth_data = {
                "username": user["username"],
                "password": "testpassword123"
            }
            response = requests.post("http://localhost:5002/auth/login", json=auth_data)
            if response.status_code == 200:
                print("✅ Аутентификация успешна")
                return True
            else:
                print(f"❌ Ошибка аутентификации: {response.status_code}")
                return False
        else:
            print(f"❌ Ошибка создания пользователя: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка тестирования пользователей: {str(e)}")
        return False

def test_parser_service():
    """Тест сервиса парсера"""
    print("\n=== Тестирование Parser Service ===")
    
    # Проверка состояния
    if not test_service_health("Parser Service", "http://localhost:5003"):
        return False
    
    # Тест парсинга FIDE
    try:
        response = requests.post("http://localhost:5003/parse/fide", json={"year": 2026})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Парсинг FIDE: {data['count']} турниров")
        else:
            print(f"❌ Ошибка парсинга FIDE: {response.status_code}")
            
        # Тест парсинга CFR
        response = requests.post("http://localhost:5003/parse/cfr", json={"year": 2026})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Парсинг CFR: {data['count']} турниров")
            return True
        else:
            print(f"❌ Ошибка парсинга CFR: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка тестирования парсера: {str(e)}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Начинаю тестирование ChessCalendar-RU проекта...")
    
    start_time = time.time()
    
    results = {
        "tournament_service": test_tournament_service(),
        "user_service": test_user_service(),
        "parser_service": test_parser_service()
    }
    
    end_time = time.time()
    
    print(f"\n📊 Результаты тестирования:")
    print(f"🕐 Время выполнения: {end_time - start_time:.2f} секунд")
    print(f"✅ Успешных тестов: {sum(results.values())}")
    print(f"❌ Проваленных тестов: {len(results) - sum(results.values())}")
    
    if all(results.values()):
        print("\n🎉 Все сервисы работают корректно!")
        return True
    else:
        print("\n⚠️  Некоторые сервисы имеют проблемы")
        return False

if __name__ == "__main__":
    main()