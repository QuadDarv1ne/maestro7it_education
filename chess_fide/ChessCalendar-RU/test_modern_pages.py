"""
Тестирование улучшенных страниц ChessCalendar-RU
"""
import requests
import time

def test_page(url, page_name):
    """Тестирование конкретной страницы"""
    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            content_length = len(response.text)
            print(f"✅ {page_name}: Успешно загружена")
            print(f"   🕐 Время загрузки: {end_time - start_time:.2f} секунд")
            print(f"   📏 Размер: {content_length} байт")
            return True
        else:
            print(f"❌ {page_name}: Ошибка {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {page_name}: Ошибка - {str(e)}")
        return False

def test_api(url, api_name):
    """Тестирование API"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {api_name}: Работает")
            print(f"   📊 Возвращено {len(data)} записей")
            return True
        else:
            print(f"❌ {api_name}: Ошибка {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {api_name}: Ошибка - {str(e)}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Тестирование улучшенного ChessCalendar-RU...")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Тестирование страниц
    pages = [
        (f"{base_url}/", "Главная страница"),
        (f"{base_url}/calendar", "Страница календаря"),
        (f"{base_url}/tournaments", "Страница турниров"),
        (f"{base_url}/about", "Страница о проекте")
    ]
    
    print("\n📋 Тестирование страниц:")
    page_results = []
    for url, name in pages:
        result = test_page(url, name)
        page_results.append(result)
        time.sleep(0.5)  # Небольшая пауза между запросами
    
    # Тестирование API
    print("\n📡 Тестирование API:")
    api_results = []
    api_results.append(test_api(f"{base_url}/api/tournaments", "API турниров"))
    
    # Сводка результатов
    print("\n" + "=" * 50)
    print("📊 Результаты тестирования:")
    print(f"✅ Успешных страниц: {sum(page_results)}/{len(page_results)}")
    print(f"✅ Работающих API: {sum(api_results)}/{len(api_results)}")
    
    total_tests = len(page_results) + len(api_results)
    passed_tests = sum(page_results) + sum(api_results)
    
    print(f"🎯 Общий результат: {passed_tests}/{total_tests} тестов пройдено")
    
    if passed_tests == total_tests:
        print("\n🎉 Все тесты пройдены успешно!")
        print("🌐 Проект готов к использованию по адресу: http://localhost:5000")
    else:
        print("\n⚠️ Некоторые тесты не пройдены")
        print("🔧 Проверьте работу сервисов")
    
    print("\n📱 Доступные страницы:")
    print("   🏠 Главная: http://localhost:5000")
    print("   📅 Календарь: http://localhost:5000/calendar")
    print("   🏆 Турниры: http://localhost:5000/tournaments")
    print("   ℹ️  О проекте: http://localhost:5000/about")

if __name__ == "__main__":
    main()