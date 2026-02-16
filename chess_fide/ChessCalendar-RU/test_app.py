#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Простой скрипт для тестирования ChessCalendar-RU API
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def print_test_header(test_name):
    """Печать заголовка теста"""
    print("\n" + "="*60)
    print(f"ТЕСТ: {test_name}")
    print("="*60)

def test_health_check():
    """Проверка health endpoint"""
    print_test_header("Health Check")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Статус: {response.status_code}")
        data = response.json()
        print(f"Общий статус: {data.get('health_status')}")
        print("\nПроверки компонентов:")
        for check_name, check_data in data.get('checks', {}).items():
            status = check_data.get('status', 'unknown')
            print(f"  - {check_name}: {status}")
        return response.status_code == 200
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return False

def test_get_tournaments():
    """Получение списка турниров"""
    print_test_header("Получение списка турниров")
    try:
        response = requests.get(f"{BASE_URL}/api/tournaments")
        print(f"Статус: {response.status_code}")
        data = response.json()
        tournaments = data.get('tournaments', [])
        print(f"Найдено турниров: {len(tournaments)}")
        
        if tournaments:
            print("\nПервые 3 турнира:")
            for t in tournaments[:3]:
                print(f"  - {t['name']}")
                print(f"    Место: {t['location']}")
                print(f"    Даты: {t['start_date']} - {t['end_date']}")
        
        return response.status_code == 200 and len(tournaments) > 0
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return False

def test_get_tournament_by_id():
    """Получение турнира по ID"""
    print_test_header("Получение турнира по ID")
    try:
        tournament_id = 1
        response = requests.get(f"{BASE_URL}/api/tournaments/{tournament_id}")
        print(f"Статус: {response.status_code}")
        data = response.json()
        print(f"\nТурнир: {data.get('name')}")
        print(f"Категория: {data.get('category')}")
        print(f"Место: {data.get('location')}")
        print(f"Призовой фонд: {data.get('prize_fund')}")
        print(f"Организатор: {data.get('organizer')}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return False

def test_search_tournaments():
    """Поиск турниров"""
    print_test_header("Поиск турниров")
    try:
        search_query = "Россия"
        response = requests.get(f"{BASE_URL}/api/tournaments/search?q={search_query}")
        print(f"Статус: {response.status_code}")
        data = response.json()
        print(f"Найдено турниров по запросу '{search_query}': {len(data)}")
        
        if data:
            print("\nРезультаты поиска:")
            for t in data[:5]:
                print(f"  - {t['name']}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return False

def test_filter_tournaments():
    """Фильтрация турниров"""
    print_test_header("Фильтрация турниров")
    try:
        response = requests.get(f"{BASE_URL}/api/tournaments?category=World Championship")
        print(f"Статус: {response.status_code}")
        data = response.json()
        tournaments = data.get('tournaments', [])
        print(f"Найдено турниров категории 'World Championship': {len(tournaments)}")
        
        if tournaments:
            for t in tournaments:
                print(f"  - {t['name']} ({t['category']})")
        
        return response.status_code == 200
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return False

def test_main_page():
    """Проверка главной страницы"""
    print_test_header("Главная страница")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Статус: {response.status_code}")
        print(f"Размер ответа: {len(response.text)} байт")
        
        # Проверяем наличие ключевых элементов
        content = response.text
        checks = {
            "ChessCalendar-RU": "ChessCalendar-RU" in content,
            "Турниры": "Турниры" in content or "турниры" in content,
            "Bootstrap": "bootstrap" in content.lower(),
        }
        
        print("\nПроверка содержимого:")
        for check_name, result in checks.items():
            status = "✓" if result else "✗"
            print(f"  {status} {check_name}")
        
        return response.status_code == 200 and all(checks.values())
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return False

def test_calendar_page():
    """Проверка страницы календаря"""
    print_test_header("Страница календаря")
    try:
        response = requests.get(f"{BASE_URL}/calendar")
        print(f"Статус: {response.status_code}")
        print(f"Размер ответа: {len(response.text)} байт")
        
        return response.status_code == 200
    except Exception as e:
        print(f"ОШИБКА: {e}")
        return False

def run_all_tests():
    """Запуск всех тестов"""
    print("\n" + "="*60)
    print("ЗАПУСК ТЕСТОВ ChessCalendar-RU")
    print(f"Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Список турниров", test_get_tournaments),
        ("Турнир по ID", test_get_tournament_by_id),
        ("Поиск турниров", test_search_tournaments),
        ("Фильтрация турниров", test_filter_tournaments),
        ("Главная страница", test_main_page),
        ("Страница календаря", test_calendar_page),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\nОШИБКА при выполнении теста '{test_name}': {e}")
            results.append((test_name, False))
    
    # Итоговый отчет
    print("\n" + "="*60)
    print("ИТОГОВЫЙ ОТЧЕТ")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ ПРОЙДЕН" if result else "✗ ПРОВАЛЕН"
        print(f"{status}: {test_name}")
    
    print("\n" + "-"*60)
    print(f"Пройдено: {passed}/{total} ({passed*100//total}%)")
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
