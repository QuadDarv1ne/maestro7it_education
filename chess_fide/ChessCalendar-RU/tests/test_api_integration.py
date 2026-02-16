"""
Простой скрипт для тестирования API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(name, url, method="GET"):
    """Тестирование эндпоинта"""
    try:
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url)
        
        print(f"✓ {name}: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                print(f"  Ключи: {list(data.keys())}")
        return True
    except Exception as e:
        print(f"✗ {name}: {str(e)}")
        return False

print("=" * 50)
print("Тестирование Chess Calendar API")
print("=" * 50)

# Тест основных эндпоинтов
tests = [
    ("Главная страница", f"{BASE_URL}/"),
    ("Список турниров", f"{BASE_URL}/api/tournaments"),
    ("Предстоящие турниры", f"{BASE_URL}/api/upcoming"),
    ("Поиск турниров", f"{BASE_URL}/api/search?q=chess"),
]

passed = 0
failed = 0

for name, url in tests:
    if test_endpoint(name, url):
        passed += 1
    else:
        failed += 1
    print()

print("=" * 50)
print(f"Результаты: {passed} успешно, {failed} неудачно")
print("=" * 50)
