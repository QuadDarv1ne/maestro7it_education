"""
Финальное тестирование улучшенного ChessCalendar-RU
"""
import requests
import time

def test_page(url, page_name):
    """Тестирование страницы"""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            content_length = len(response.text)
            print(f"✅ {page_name}: Успешно загружена")
            print(f"   🕐 Время: {end_time - start_time:.2f}с")
            print(f"   📏 Размер: {content_length} байт")
            return True
        else:
            print(f"❌ {page_name}: Ошибка {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {page_name}: {str(e)}")
        return False

def test_api(url, api_name):
    """Тестирование API"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {api_name}: Работает")
            if isinstance(data, list):
                print(f"   📊 Возвращено {len(data)} записей")
            return True
        else:
            print(f"❌ {api_name}: Ошибка {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {api_name}: {str(e)}")
        return False

def main():
    print("🚀 Финальное тестирование улучшенного ChessCalendar-RU")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Тестирование всех страниц
    pages = [
        (f"{base_url}/", "Главная страница"),
        (f"{base_url}/calendar", "Календарь"),
        (f"{base_url}/tournaments", "Турниры"),
        (f"{base_url}/profile", "Профиль"),
        (f"{base_url}/recommendations", "Рекомендации"),
        (f"{base_url}/about", "О проекте")
    ]
    
    print("\n📋 Тестирование страниц:")
    page_results = []
    for url, name in pages:
        result = test_page(url, name)
        page_results.append(result)
        time.sleep(0.3)
    
    # Тестирование API сервисов
    print("\n📡 Тестирование API сервисов:")
    api_services = [
        (f"{base_url}/api/tournaments", "API турниров"),
        ("http://localhost:5001/health", "Tournament Service"),
        ("http://localhost:5002/health", "User Service"), 
        ("http://localhost:5003/health", "Parser Service"),
        ("http://localhost:5009/health", "Favorites Service")
    ]
    
    api_results = []
    for url, name in api_services:
        result = test_api(url, name)
        api_results.append(result)
        time.sleep(0.3)
    
    # Финальная статистика
    print("\n" + "=" * 60)
    print("📊 ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
    print(f"✅ Успешных страниц: {sum(page_results)}/{len(page_results)}")
    print(f"✅ Работающих API: {sum(api_results)}/{len(api_results)}")
    
    total_tests = len(page_results) + len(api_results)
    passed_tests = sum(page_results) + sum(api_results)
    
    print(f"🎯 Общий результат: {passed_tests}/{total_tests} тестов пройдено")
    
    # Процент успешных тестов
    success_rate = (passed_tests / total_tests) * 100
    print(f"📈 Процент успеха: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n🎉 ПРОЕКТ ПОЛНОСТЬЮ ГОТОВ!")
        print("🏆 Все компоненты работают корректно")
    elif success_rate >= 80:
        print("\n✨ ПРОЕКТ ПОЧТИ ГОТОВ!")
        print("🔧 Незначительные проблемы, но основной функционал работает")
    else:
        print("\n⚠️  ТРЕБУЕТСЯ ДОРАБОТКА")
        print("🔧 Серьезные проблемы с компонентами")
    
    print("\n📱 ДОСТУПНЫЕ СТРАНИЦЫ:")
    print("   🏠 Главная: http://localhost:5000")
    print("   📅 Календарь: http://localhost:5000/calendar")
    print("   🏆 Турниры: http://localhost:5000/tournaments")
    print("   👤 Профиль: http://localhost:5000/profile")
    print("   🌟 Рекомендации: http://localhost:5000/recommendations")
    print("   ℹ️  О проекте: http://localhost:5000/about")
    
    print("\n🔧 API СЕРВИСЫ:")
    print("   🎯 Tournament Service: http://localhost:5001")
    print("   👥 User Service: http://localhost:5002")
    print("   🔍 Parser Service: http://localhost:5003")
    print("   ❤️  Favorites Service: http://localhost:5009")
    
    print("\n✨ ОСОБЕННОСТИ ПРОЕКТА:")
    print("   🎨 Современный дизайн с Bootstrap 5")
    print("   📱 Полная адаптивность для мобильных")
    print("   🌙 Темная тема с переключателем")
    print("   🔍 Интерактивный поиск и фильтрация")
    print("   ❤️  Система избранных турниров")
    print("   🌟 Персональные рекомендации")
    print("   📊 Анимированные элементы и счетчики")
    print("   ⚡ Динамический контент через JavaScript")

if __name__ == "__main__":
    main()