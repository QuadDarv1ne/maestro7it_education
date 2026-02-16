"""
Примеры использования Calendar Integration API
"""
import requests
import json
from datetime import datetime, date

# Базовый URL сервиса
BASE_URL = "http://localhost:5006"

def export_single_tournament():
    """Пример экспорта одного турнира"""
    
    tournament_data = {
        "tournament": {
            "name": "Чемпионат России по шахматам 2026",
            "start_date": "2026-03-15T00:00:00+03:00",
            "end_date": "2026-03-25T00:00:00+03:00",
            "location": "Москва, Центральный шахматный клуб",
            "description": "Ежегодный чемпионат России по классическим шахматам",
            "category": "National Championship"
        }
    }
    
    # Экспорт в ICS
    response = requests.post(f"{BASE_URL}/export/ics", json=tournament_data)
    if response.status_code == 200:
        ics_data = response.json()
        print("ICS Content:")
        print(ics_data['ics_content'])
        print(f"Filename: {ics_data['filename']}")
    
    # Экспорт в Google Calendar
    response = requests.post(f"{BASE_URL}/export/google", json=tournament_data)
    if response.status_code == 200:
        google_data = response.json()
        print(f"\nGoogle Calendar URL: {google_data['google_calendar_url']}")
    
    # Экспорт в Outlook Calendar
    response = requests.post(f"{BASE_URL}/export/outlook", json=tournament_data)
    if response.status_code == 200:
        outlook_data = response.json()
        print(f"Outlook Calendar URL: {outlook_data['outlook_calendar_url']}")

def export_multiple_tournaments():
    """Пример пакетного экспорта турниров"""
    
    tournaments_data = {
        "tournaments": [
            {
                "name": "Открытый турнир памяти Александра Алехина",
                "start_date": "2026-04-10T00:00:00+03:00",
                "end_date": "2026-04-20T00:00:00+03:00",
                "location": "Санкт-Петербург",
                "description": "Международный открытый турнир",
                "category": "Open Tournament"
            },
            {
                "name": "Кубок Москвы",
                "start_date": "2026-05-05T00:00:00+03:00",
                "end_date": "2026-05-15T00:00:00+03:00",
                "location": "Москва",
                "description": "Городской турнир по быстрым шахматам",
                "category": "City Cup"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/export/batch", json=tournaments_data)
    if response.status_code == 200:
        batch_data = response.json()
        print(f"\nBatch Export Results:")
        print(f"Total processed: {batch_data['total_processed']}")
        print(f"Successful: {batch_data['successful']}")
        print(f"Failed: {batch_data['failed']}")
        
        for result in batch_data['results']:
            if result['status'] == 'success':
                print(f"\nTournament: {result['tournament_name']}")
                print(f"ICS available")
                print(f"Google URL: {result['google_calendar_url']}")
                print(f"Outlook URL: {result['outlook_calendar_url']}")

def check_service_health():
    """Проверка состояния сервиса"""
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        health_data = response.json()
        print("Service Health:")
        print(f"Status: {health_data['status']}")
        print(f"Service: {health_data['service']}")
        print(f"Supported formats: {health_data['supported_formats']}")

if __name__ == "__main__":
    print("=== Calendar Integration Service Examples ===\n")
    
    # Проверка состояния сервиса
    check_service_health()
    
    print("\n" + "="*50 + "\n")
    
    # Экспорт одного турнира
    print("1. Exporting single tournament:")
    export_single_tournament()
    
    print("\n" + "="*50 + "\n")
    
    # Пакетный экспорт
    print("2. Exporting multiple tournaments:")
    export_multiple_tournaments()