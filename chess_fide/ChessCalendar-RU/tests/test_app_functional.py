#!/usr/bin/env python3
"""Простой скрипт для тестирования основных функций приложения"""

import requests
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def test_health_check():
    """Проверка health endpoint"""
    print("\n=== Тест 1: Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200:
            print("✓ Health check пройден")
            return True
        else:
            print("✗ Health check не пройден")
            return False
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False

def test_main_page():
    """Проверка главной страницы"""
    print("\n=== Тест 2: Главная страница ===")
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"Статус: {response.status_code}")
        if response.status_code == 200 and "ChessCalendar" in response.text:
            print("✓ Главная страница загружается")
            return True
        else:
            print("✗ Главная страница не загружается")
            return False
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False

def test_api_tournaments():
    """Проверка API турниров"""
    print("\n=== Тест 3: API турниров ===")
    try:
        # Ждем немного чтобы избежать rate limit
        time.sleep(2)
        response = requests.get(f"{BASE_URL}/api/tournaments", timeout=5)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('pagination', {}).get('total', 0)
            print(f"✓ API работает. Найдено турниров: {total}")
            
            if total > 0:
                tournaments = data.get('tournaments', [])
                print(f"\nПример турнира:")
                if tournaments:
                    t = tournaments[0]
                    print(f"  Название: {t.get('name')}")
                    print(f"  Место: {t.get('location')}")
                    print(f"  Дата: {t.get('start_date')}")
            return True
        else:
            print(f"✗ API вернул ошибку: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False

def test_static_files():
    """Проверка статических файлов"""
    print("\n=== Тест 4: Статические файлы ===")
    try:
        # Проверяем manifest.json для PWA
        response = requests.get(f"{BASE_URL}/manifest.json", timeout=5)
        if response.status_code == 200:
            print("✓ manifest.json доступен")
            manifest_ok = True
        else:
            print("✗ manifest.json недоступен")
            manifest_ok = False
        
        # Проверяем service worker
        response = requests.get(f"{BASE_URL}/sw.js", timeout=5)
        if response.status_code == 200:
            print("✓ service worker доступен")
            sw_ok = True
        else:
            print("✗ service worker недоступен")
            sw_ok = False
        
        return manifest_ok and sw_ok
    except Exception as e:
        print(f"✗ Ошибка: {e}")
        return False

def main():
    """Запуск всех тестов"""
    print("=" * 50)
    print("ТЕСТИРОВАНИЕ ПРИЛОЖЕНИЯ ChessCalendar-RU")
    print("=" * 50)
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"URL: {BASE_URL}")
    
    results = []
    
    # Запускаем тесты
    results.append(("Health Check", test_health_check()))
    results.append(("Главная страница", test_main_page()))
    results.append(("API турниров", test_api_tournaments()))
    results.append(("Статические файлы", test_static_files()))
    
    # Итоги
    print("\n" + "=" * 50)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ ПРОЙДЕН" if result else "✗ НЕ ПРОЙДЕН"
        print(f"{name}: {status}")
    
    print(f"\nВсего тестов: {total}")
    print(f"Пройдено: {passed}")
    print(f"Не пройдено: {total - passed}")
    print(f"Процент успеха: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("\n🎉 Все тесты пройдены успешно!")
    else:
        print(f"\n⚠️  {total - passed} тест(ов) не пройдено")

if __name__ == "__main__":
    main()
