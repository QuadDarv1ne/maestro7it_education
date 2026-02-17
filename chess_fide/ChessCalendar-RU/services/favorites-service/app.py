"""
API для системы избранных турниров
"""
from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

# Хранилище избранных турниров (в реальном приложении использовать БД)
favorites_storage = {
    "user_1": [
        {
            "id": 1,
            "tournament_id": 1,
            "added_at": "2026-02-15T10:30:00",
            "notes": "Главный чемпионат года"
        },
        {
            "id": 2,
            "tournament_id": 4,
            "added_at": "2026-02-16T14:15:00",
            "notes": "Международный уровень"
        }
    ]
}

# Тестовые данные турниров
tournaments_data = {
    1: {
        "id": 1,
        "name": "Чемпионат России по шахматам 2026",
        "start_date": "2026-03-15",
        "end_date": "2026-03-25",
        "location": "Москва",
        "category": "National Championship",
        "status": "Scheduled",
        "description": "Ежегодный чемпионат России по классическим шахматам",
        "prize_fund": "2 000 000 руб.",
        "organizer": "Федерация шахмат России"
    },
    2: {
        "id": 2,
        "name": "Открытый турнир памяти Александра Алехина",
        "start_date": "2026-04-10",
        "end_date": "2026-04-20",
        "location": "Санкт-Петербург",
        "category": "Open Tournament",
        "status": "Scheduled",
        "description": "Международный открытый турнир по классическим шахматам",
        "prize_fund": "1 500 000 руб.",
        "organizer": "Петербургская шахматная федерация"
    },
    3: {
        "id": 3,
        "name": "Кубок Москвы по быстрым шахматам",
        "start_date": "2026-02-20",
        "end_date": "2026-02-25",
        "location": "Москва",
        "category": "Rapid Chess",
        "status": "Ongoing",
        "description": "Городской турнир по быстрым шахматам",
        "prize_fund": "500 000 руб.",
        "organizer": "Московская шахматная федерация"
    },
    4: {
        "id": 4,
        "name": "Международный турнир в Сочи",
        "start_date": "2026-05-01",
        "end_date": "2026-05-10",
        "location": "Сочи",
        "category": "International Tournament",
        "status": "Scheduled",
        "description": "Международный турнир с участием гроссмейстеров",
        "prize_fund": "3 000 000 руб.",
        "organizer": "ФИДЕ"
    }
}

@app.route('/favorites/<user_id>', methods=['GET'])
def get_favorites(user_id):
    """Получение избранных турниров пользователя"""
    try:
        user_favorites = favorites_storage.get(user_id, [])
        
        # Добавляем полную информацию о турнирах
        favorites_with_details = []
        for favorite in user_favorites:
            tournament = tournaments_data.get(favorite['tournament_id'])
            if tournament:
                favorite_detail = {
                    **favorite,
                    'tournament': tournament
                }
                favorites_with_details.append(favorite_detail)
        
        return jsonify({
            'user_id': user_id,
            'favorites': favorites_with_details,
            'count': len(favorites_with_details),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/favorites/<user_id>', methods=['POST'])
def add_favorite(user_id):
    """Добавление турнира в избранное"""
    try:
        data = request.get_json()
        tournament_id = data.get('tournament_id')
        notes = data.get('notes', '')
        
        if not tournament_id:
            return jsonify({'error': 'tournament_id is required'}), 400
        
        # Проверка существования турнира
        if tournament_id not in tournaments_data:
            return jsonify({'error': 'Tournament not found'}), 404
        
        # Проверка, не добавлен ли уже в избранное
        user_favorites = favorites_storage.get(user_id, [])
        if any(fav['tournament_id'] == tournament_id for fav in user_favorites):
            return jsonify({'error': 'Tournament already in favorites'}), 409
        
        # Создание новой записи
        new_favorite = {
            'id': len(user_favorites) + 1,
            'tournament_id': tournament_id,
            'added_at': datetime.utcnow().isoformat(),
            'notes': notes
        }
        
        # Добавление в хранилище
        if user_id not in favorites_storage:
            favorites_storage[user_id] = []
        favorites_storage[user_id].append(new_favorite)
        
        # Получение полной информации о турнире
        tournament = tournaments_data[tournament_id]
        
        return jsonify({
            'status': 'success',
            'message': 'Tournament added to favorites',
            'favorite': {
                **new_favorite,
                'tournament': tournament
            },
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/favorites/<user_id>/<int:favorite_id>', methods=['DELETE'])
def remove_favorite(user_id, favorite_id):
    """Удаление турнира из избранного"""
    try:
        user_favorites = favorites_storage.get(user_id, [])
        
        # Поиск и удаление
        favorite_to_remove = None
        for i, favorite in enumerate(user_favorites):
            if favorite['id'] == favorite_id:
                favorite_to_remove = user_favorites.pop(i)
                break
        
        if not favorite_to_remove:
            return jsonify({'error': 'Favorite not found'}), 404
        
        # Получение информации о турнире для ответа
        tournament = tournaments_data.get(favorite_to_remove['tournament_id'])
        
        return jsonify({
            'status': 'success',
            'message': 'Tournament removed from favorites',
            'removed_favorite': {
                **favorite_to_remove,
                'tournament': tournament
            },
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/favorites/<user_id>/<int:favorite_id>', methods=['PUT'])
def update_favorite(user_id, favorite_id):
    """Обновление заметок к избранному турниру"""
    try:
        data = request.get_json()
        notes = data.get('notes')
        
        if notes is None:
            return jsonify({'error': 'notes field is required'}), 400
        
        user_favorites = favorites_storage.get(user_id, [])
        
        # Поиск и обновление
        favorite_to_update = None
        for favorite in user_favorites:
            if favorite['id'] == favorite_id:
                favorite['notes'] = notes
                favorite['updated_at'] = datetime.utcnow().isoformat()
                favorite_to_update = favorite
                break
        
        if not favorite_to_update:
            return jsonify({'error': 'Favorite not found'}), 404
        
        # Получение информации о турнире
        tournament = tournaments_data.get(favorite_to_update['tournament_id'])
        
        return jsonify({
            'status': 'success',
            'message': 'Favorite updated successfully',
            'favorite': {
                **favorite_to_update,
                'tournament': tournament
            },
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/favorites/check/<user_id>/<int:tournament_id>', methods=['GET'])
def check_favorite(user_id, tournament_id):
    """Проверка, находится ли турнир в избранном"""
    try:
        user_favorites = favorites_storage.get(user_id, [])
        is_favorite = any(fav['tournament_id'] == tournament_id for fav in user_favorites)
        
        return jsonify({
            'user_id': user_id,
            'tournament_id': tournament_id,
            'is_favorite': is_favorite,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/favorites/stats/<user_id>', methods=['GET'])
def get_favorites_stats(user_id):
    """Получение статистики избранных турниров"""
    try:
        user_favorites = favorites_storage.get(user_id, [])
        
        # Статистика по категориям
        category_stats = {}
        location_stats = {}
        status_stats = {}
        
        for favorite in user_favorites:
            tournament = tournaments_data.get(favorite['tournament_id'])
            if tournament:
                # Категории
                category = tournament['category']
                category_stats[category] = category_stats.get(category, 0) + 1
                
                # Локации
                location = tournament['location']
                location_stats[location] = location_stats.get(location, 0) + 1
                
                # Статусы
                status = tournament['status']
                status_stats[status] = status_stats.get(status, 0) + 1
        
        return jsonify({
            'user_id': user_id,
            'total_favorites': len(user_favorites),
            'category_stats': category_stats,
            'location_stats': location_stats,
            'status_stats': status_stats,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    return jsonify({
        'status': 'healthy',
        'service': 'favorites-api',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    debug_mode = os.environ.get('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5009, debug=debug_mode)