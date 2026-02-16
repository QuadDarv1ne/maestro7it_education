"""
Примеры использования ML Recommendation Service
"""
import requests
import json
from datetime import datetime

# Базовый URL сервиса
BASE_URL = "http://localhost:5008"

def train_model():
    """Обучение модели на примерных данных турниров"""
    
    sample_tournaments = [
        {
            "name": "Чемпионат России по шахматам 2026",
            "location": "Москва",
            "category": "National Championship",
            "description": "Ежегодный чемпионат России по классическим шахматам",
            "organizer": "Федерация шахмат России"
        },
        {
            "name": "Открытый турнир памяти Александра Алехина",
            "location": "Санкт-Петербург",
            "category": "Open Tournament",
            "description": "Международный открытый турнир по классическим шахматам",
            "organizer": "Петербургская шахматная федерация"
        },
        {
            "name": "Кубок Москвы по быстрым шахматам",
            "location": "Москва",
            "category": "Rapid Chess",
            "description": "Городской турнир по быстрым шахматам",
            "organizer": "Московская шахматная федерация"
        },
        {
            "name": "Международный турнир в Сочи",
            "location": "Сочи",
            "category": "International Tournament",
            "description": "Международный турнир с участием гроссмейстеров",
            "organizer": "ФИДЕ"
        },
        {
            "name": "Юношеский чемпионат России",
            "location": "Екатеринбург",
            "category": "Youth Championship",
            "description": "Чемпионат России среди юных шахматистов",
            "organizer": "Федерация шахмат России"
        }
    ]
    
    response = requests.post(f"{BASE_URL}/recommendations/train", json={"tournaments": sample_tournaments})
    if response.status_code == 200:
        result = response.json()
        print("Model Training Result:")
        print(f"Status: {result['status']}")
        print(f"Statistics: {result['statistics']}")
        return True
    else:
        print(f"Training failed: {response.text}")
        return False

def create_user_profiles():
    """Создание профилей пользователей"""
    
    users_data = [
        {
            "user_id": "user_001",
            "preferences": ["National Championship", "Москва", "классические шахматы", "чемпионат"],
            "history": ["Чемпионат России по шахматам 2025", "Кубок Москвы 2025"]
        },
        {
            "user_id": "user_002",
            "preferences": ["Open Tournament", "Санкт-Петербург", "международные турниры", "Алехин"],
            "history": ["Открытый турнир Алехина 2025", "Петербургский турнир 2025"]
        },
        {
            "user_id": "user_003",
            "preferences": ["Rapid Chess", "Москва", "быстрые шахматы", "кубок"],
            "history": ["Кубок Москвы 2025", "Рапид турнир в ЦСК 2025"]
        }
    ]
    
    for user_data in users_data:
        response = requests.post(f"{BASE_URL}/recommendations/profile", json=user_data)
        if response.status_code == 200:
            result = response.json()
            print(f"Created profile for {user_data['user_id']}")
        else:
            print(f"Failed to create profile for {user_data['user_id']}: {response.text}")

def get_recommendations():
    """Получение рекомендаций для пользователей"""
    
    user_ids = ["user_001", "user_002", "user_003"]
    recommendation_types = ["hybrid", "content", "collaborative", "trending"]
    
    for user_id in user_ids:
        print(f"\n=== Recommendations for {user_id} ===")
        
        for rec_type in recommendation_types:
            response = requests.get(
                f"{BASE_URL}/recommendations/user/{user_id}",
                params={"type": rec_type, "count": 3}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\n{rec_type.capitalize()} recommendations:")
                for i, rec in enumerate(result['recommendations'], 1):
                    print(f"  {i}. {rec['name']} ({rec.get('score', rec.get('similarity_score', 'N/A')):.3f})")
                    print(f"     Location: {rec['location']}")
                    print(f"     Category: {rec['category']}")
            else:
                print(f"Failed to get {rec_type} recommendations: {response.text}")

def update_user_history():
    """Обновление истории пользователя"""
    
    history_updates = [
        {"user_id": "user_001", "tournament_name": "Чемпионат России по шахматам 2026"},
        {"user_id": "user_002", "tournament_name": "Открытый турнир памяти Александра Алехина"},
        {"user_id": "user_003", "tournament_name": "Кубок Москвы по быстрым шахматам"}
    ]
    
    for update in history_updates:
        response = requests.post(f"{BASE_URL}/recommendations/update-history", json=update)
        if response.status_code == 200:
            result = response.json()
            print(f"Updated history for {update['user_id']}: {result['history_count']} tournaments")
        else:
            print(f"Failed to update history for {update['user_id']}: {response.text}")

def get_service_statistics():
    """Получение статистики сервиса"""
    
    response = requests.get(f"{BASE_URL}/recommendations/statistics")
    if response.status_code == 200:
        stats = response.json()
        print("\n=== Service Statistics ===")
        print(f"Total tournaments: {stats['statistics']['total_tournaments']}")
        print(f"Total users: {stats['statistics']['total_users']}")
        print(f"Model trained: {stats['statistics']['is_trained']}")
        print(f"Vectorizer features: {stats['statistics']['vectorizer_features']}")

def main():
    """Основная функция демонстрации"""
    print("=== ML Recommendation Service Demo ===\n")
    
    # 1. Обучение модели
    print("1. Training recommendation model...")
    if not train_model():
        return
    
    print("\n" + "="*50 + "\n")
    
    # 2. Создание профилей пользователей
    print("2. Creating user profiles...")
    create_user_profiles()
    
    print("\n" + "="*50 + "\n")
    
    # 3. Получение рекомендаций
    print("3. Getting recommendations...")
    get_recommendations()
    
    print("\n" + "="*50 + "\n")
    
    # 4. Обновление истории
    print("4. Updating user history...")
    update_user_history()
    
    print("\n" + "="*50 + "\n")
    
    # 5. Получение статистики
    print("5. Getting service statistics...")
    get_service_statistics()
    
    print("\n=== Demo completed successfully ===")

if __name__ == "__main__":
    main()