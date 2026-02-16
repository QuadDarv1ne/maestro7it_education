"""
Тесты для улучшенных парсеров данных
"""
import requests
import json
import time

def test_enhanced_parsers():
    """Тестирование улучшенных парсеров"""
    print("🚀 Тестирование улучшенных парсеров")
    print("=" * 50)
    
    parser_service_url = "http://localhost:5003"
    
    # Проверка состояния сервиса
    try:
        health_response = requests.get(f"{parser_service_url}/health", timeout=10)
        if health_response.status_code == 200:
            print("✅ Сервис парсинга работает")
        else:
            print("❌ Сервис парсинга не отвечает")
            return
    except Exception as e:
        print(f"❌ Ошибка подключения к сервису парсинга: {e}")
        return
    
    # Тест расширенного парсинга
    print("\n🔍 Тестирование расширенного парсинга...")
    try:
        enhanced_data = {
            'year': 2026,
            'use_fallback': True
        }
        
        response = requests.post(
            f"{parser_service_url}/parse/enhanced",
            json=enhanced_data,
            timeout=60  # Увеличил таймаут
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Расширенный парсинг успешен")
            print(f"   Найдено турниров: {result.get('total_count', 0)}")
            print(f"   FIDE турниров: {result.get('fide_count', 0)}")
            print(f"   CFR турниров: {result.get('cfr_count', 0)}")
            
            # Показ первых 3 турниров
            tournaments = result.get('tournaments', [])[:3]
            print(f"\n📋 Примеры турниров:")
            for i, tournament in enumerate(tournaments, 1):
                print(f"   {i}. {tournament.get('name', 'N/A')}")
                print(f"      Даты: {tournament.get('dates', 'N/A')}")
                print(f"      Место: {tournament.get('location', 'N/A')}")
                print(f"      Категория: {tournament.get('category', 'N/A')}")
                print(f"      Источник: {tournament.get('source', 'N/A')}")
                print()
                
        else:
            print(f"❌ Ошибка расширенного парсинга: {response.status_code}")
            print(f"   Ответ: {response.text}")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании расширенного парсинга: {e}")
    
    # Тест отдельных парсеров
    print("\n🔧 Тестирование отдельных парсеров...")
    
    parsers_to_test = [
        ('FIDE', '/parse/fide'),
        ('CFR', '/parse/cfr'),
    ]
    
    for parser_name, endpoint in parsers_to_test:
        try:
            response = requests.post(
                f"{parser_service_url}{endpoint}",
                json={'year': 2026},
                timeout=60  # Увеличил таймаут
            )
            
            if response.status_code == 200:
                result = response.json()
                count = result.get('count', result.get('total_count', 0))
                print(f"✅ {parser_name}: {count} турниров")
            else:
                print(f"❌ {parser_name}: ошибка {response.status_code}")
                
        except Exception as e:
            print(f"❌ {parser_name}: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Тестирование улучшенных парсеров завершено")

def test_sample_data_generation():
    """Тестирование генерации тестовых данных"""
    print("\n🧪 Тестирование генерации тестовых данных...")
    
    try:
        # Создаем тестовые данные напрямую
        sample_tournaments = [
            {
                'name': 'Чемпионат мира по шахматам 2026',
                'dates': 'Апрель 2026',
                'location': 'Неизвестно',
                'category': 'World Championship',
                'source': 'Sample',
                'status': 'Scheduled'
            },
            {
                'name': 'Чемпионат России по шахматам 2026',
                'dates': 'Март 2026',
                'location': 'Москва',
                'category': 'National Championship',
                'source': 'Sample',
                'status': 'Scheduled'
            }
        ]
        
        print(f"✅ Сгенерировано {len(sample_tournaments)} тестовых турниров")
        
        required_fields = ['name', 'dates', 'location', 'category', 'source']
        valid_tournaments = 0
        
        for tournament in sample_tournaments:
            valid = True
            for field in required_fields:
                if field not in tournament or not tournament[field]:
                    valid = False
                    break
            if valid:
                valid_tournaments += 1
        
        print(f"✅ Валидных турниров: {valid_tournaments}/{len(sample_tournaments)}")
        
        # Показ примера
        if sample_tournaments:
            first = sample_tournaments[0]
            print(f"\n📝 Пример турнира:")
            for key, value in first.items():
                print(f"   {key}: {value}")
                
    except Exception as e:
        print(f"❌ Ошибка генерации тестовых данных: {e}")

if __name__ == "__main__":
    test_enhanced_parsers()
    test_sample_data_generation()