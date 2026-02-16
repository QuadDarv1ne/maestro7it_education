"""
ML Recommendation Service - Сервис персонализированных рекомендаций
"""
from flask import Flask, request, jsonify
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import json
import redis

app = Flask(__name__)

# Redis для хранения пользовательских данных
redis_client = redis.Redis(host='redis', port=6379, db=1)

class RecommendationEngine:
    def __init__(self):
        self.tournaments_data = []
        self.user_profiles = {}
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words=None,
            ngram_range=(1, 2)
        )
        self.tournament_vectors = None
        self.is_trained = False
    
    def load_tournament_data(self, tournaments):
        """Загрузка данных о турнирах"""
        self.tournaments_data = tournaments
        
        # Создание текстовых описаний для векторизации
        tournament_texts = []
        for tournament in tournaments:
            text = f"{tournament['name']} {tournament['location']} {tournament['category']} "
            text += f"{tournament.get('description', '')} {tournament.get('organizer', '')}"
            tournament_texts.append(text)
        
        # Векторизация
        self.tournament_vectors = self.tfidf_vectorizer.fit_transform(tournament_texts)
        self.is_trained = True
        
        # Сохранение в Redis
        redis_client.set('tournaments_data', json.dumps(tournaments))
        redis_client.set('tournament_vectors_shape', json.dumps(self.tournament_vectors.shape))
    
    def create_user_profile(self, user_id, preferences, history=None):
        """Создание профиля пользователя"""
        if history is None:
            history = []
        
        user_profile = {
            'user_id': user_id,
            'preferences': preferences,
            'history': history,
            'created_at': datetime.utcnow().isoformat()
        }
        
        self.user_profiles[user_id] = user_profile
        redis_client.hset('user_profiles', user_id, json.dumps(user_profile))
        
        return user_profile
    
    def get_user_profile(self, user_id):
        """Получение профиля пользователя"""
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]
        
        # Попытка загрузить из Redis
        profile_data = redis_client.hget('user_profiles', user_id)
        if profile_data:
            profile = json.loads(profile_data)
            self.user_profiles[user_id] = profile
            return profile
        
        return None
    
    def content_based_recommendations(self, user_id, n_recommendations=5):
        """Контент-базированные рекомендации"""
        if not self.is_trained:
            return []
        
        user_profile = self.get_user_profile(user_id)
        if not user_profile:
            return []
        
        # Создание пользовательского вектора на основе предпочтений
        preferences_text = ' '.join(user_profile['preferences'])
        user_vector = self.tfidf_vectorizer.transform([preferences_text])
        
        # Вычисление схожести
        similarities = cosine_similarity(user_vector, self.tournament_vectors).flatten()
        
        # Получение индексов турниров с наивысшей схожестью
        top_indices = similarities.argsort()[-n_recommendations:][::-1]
        
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  # Минимальный порог схожести
                tournament = self.tournaments_data[idx].copy()
                tournament['similarity_score'] = float(similarities[idx])
                recommendations.append(tournament)
        
        return recommendations
    
    def collaborative_filtering_recommendations(self, user_id, n_recommendations=5):
        """Коллаборативная фильтрация"""
        user_profile = self.get_user_profile(user_id)
        if not user_profile:
            return []
        
        # Найти пользователей с похожими предпочтениями
        similar_users = []
        current_preferences = set(user_profile['preferences'])
        
        for uid, profile in self.user_profiles.items():
            if uid != user_id:
                other_preferences = set(profile['preferences'])
                similarity = len(current_preferences.intersection(other_preferences)) / len(current_preferences.union(other_preferences))
                if similarity > 0.3:  # Порог схожести
                    similar_users.append((uid, similarity, profile))
        
        # Собрать рекомендации от похожих пользователей
        recommendations = []
        recommended_tournaments = set()
        
        for uid, similarity, profile in sorted(similar_users, key=lambda x: x[1], reverse=True):
            # Добавить турниры из истории похожих пользователей
            for tournament_name in profile.get('history', []):
                if tournament_name not in recommended_tournaments:
                    # Найти турнир в данных
                    for tournament in self.tournaments_data:
                        if tournament['name'] == tournament_name:
                            tournament_copy = tournament.copy()
                            tournament_copy['recommended_by'] = uid
                            tournament_copy['similarity_to_user'] = similarity
                            recommendations.append(tournament_copy)
                            recommended_tournaments.add(tournament_name)
                            break
        
        return recommendations[:n_recommendations]
    
    def hybrid_recommendations(self, user_id, n_recommendations=10):
        """Гибридные рекомендации (комбинация подходов)"""
        content_recs = self.content_based_recommendations(user_id, n_recommendations)
        collab_recs = self.collaborative_filtering_recommendations(user_id, n_recommendations)
        
        # Объединение рекомендаций с весами
        all_recommendations = {}
        
        # Добавить контент-базированные рекомендации (вес 0.7)
        for rec in content_recs:
            tournament_id = rec['name']
            rec['score'] = rec.get('similarity_score', 0) * 0.7
            all_recommendations[tournament_id] = rec
        
        # Добавить коллаборативные рекомендации (вес 0.3)
        for rec in collab_recs:
            tournament_id = rec['name']
            collab_score = rec.get('similarity_to_user', 0) * 0.3
            
            if tournament_id in all_recommendations:
                all_recommendations[tournament_id]['score'] += collab_score
                all_recommendations[tournament_id]['recommended_by'] = rec.get('recommended_by')
            else:
                rec['score'] = collab_score
                all_recommendations[tournament_id] = rec
        
        # Сортировка по общему счету
        sorted_recommendations = sorted(
            all_recommendations.values(),
            key=lambda x: x['score'],
            reverse=True
        )
        
        return sorted_recommendations[:n_recommendations]
    
    def trending_tournaments(self, n_trending=5):
        """Рекомендации популярных турниров"""
        if not self.tournaments_data:
            return []
        
        # Сортировка по количеству упоминаний в пользовательских историях
        tournament_popularity = {}
        
        for profile in self.user_profiles.values():
            for tournament_name in profile.get('history', []):
                tournament_popularity[tournament_name] = tournament_popularity.get(tournament_name, 0) + 1
        
        # Найти турниры и добавить информацию о популярности
        trending = []
        for tournament in self.tournaments_data:
            popularity = tournament_popularity.get(tournament['name'], 0)
            if popularity > 0:
                tournament_copy = tournament.copy()
                tournament_copy['popularity'] = popularity
                trending.append(tournament_copy)
        
        # Сортировка по популярности
        trending.sort(key=lambda x: x['popularity'], reverse=True)
        
        return trending[:n_trending]
    
    def get_statistics(self):
        """Получение статистики движка рекомендаций"""
        return {
            'total_tournaments': len(self.tournaments_data),
            'total_users': len(self.user_profiles),
            'is_trained': self.is_trained,
            'vectorizer_features': len(self.tfidf_vectorizer.get_feature_names_out()) if self.is_trained else 0
        }

# Инициализация движка рекомендаций
recommendation_engine = RecommendationEngine()

@app.route('/recommendations/train', methods=['POST'])
def train_model():
    """Обучение модели на данных турниров"""
    try:
        data = request.get_json()
        tournaments = data.get('tournaments', [])
        
        if not tournaments:
            return jsonify({'error': 'No tournaments data provided'}), 400
        
        recommendation_engine.load_tournament_data(tournaments)
        
        return jsonify({
            'status': 'success',
            'message': 'Recommendation model trained successfully',
            'statistics': recommendation_engine.get_statistics()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommendations/user/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    """Получение рекомендаций для пользователя"""
    try:
        n_recommendations = int(request.args.get('count', 10))
        recommendation_type = request.args.get('type', 'hybrid')  # hybrid, content, collaborative, trending
        
        if recommendation_type == 'content':
            recommendations = recommendation_engine.content_based_recommendations(user_id, n_recommendations)
        elif recommendation_type == 'collaborative':
            recommendations = recommendation_engine.collaborative_filtering_recommendations(user_id, n_recommendations)
        elif recommendation_type == 'trending':
            recommendations = recommendation_engine.trending_tournaments(n_recommendations)
        else:  # hybrid
            recommendations = recommendation_engine.hybrid_recommendations(user_id, n_recommendations)
        
        return jsonify({
            'user_id': user_id,
            'recommendations': recommendations,
            'count': len(recommendations),
            'type': recommendation_type,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommendations/profile', methods=['POST'])
def create_user_profile():
    """Создание профиля пользователя"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        preferences = data.get('preferences', [])
        history = data.get('history', [])
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        profile = recommendation_engine.create_user_profile(user_id, preferences, history)
        
        return jsonify({
            'status': 'success',
            'profile': profile,
            'message': 'User profile created successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommendations/profile/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    """Получение профиля пользователя"""
    try:
        profile = recommendation_engine.get_user_profile(user_id)
        
        if profile:
            return jsonify({
                'profile': profile,
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            return jsonify({'error': 'User profile not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommendations/update-history', methods=['POST'])
def update_user_history():
    """Обновление истории пользователя"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        tournament_name = data.get('tournament_name')
        
        if not user_id or not tournament_name:
            return jsonify({'error': 'User ID and tournament name are required'}), 400
        
        profile = recommendation_engine.get_user_profile(user_id)
        if not profile:
            return jsonify({'error': 'User profile not found'}), 404
        
        # Добавление турнира в историю
        if tournament_name not in profile['history']:
            profile['history'].append(tournament_name)
            recommendation_engine.user_profiles[user_id] = profile
            redis_client.hset('user_profiles', user_id, json.dumps(profile))
        
        return jsonify({
            'status': 'success',
            'message': 'User history updated successfully',
            'history_count': len(profile['history'])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/recommendations/statistics', methods=['GET'])
def get_statistics():
    """Получение статистики сервиса"""
    try:
        stats = recommendation_engine.get_statistics()
        return jsonify({
            'statistics': stats,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    return jsonify({
        'status': 'healthy',
        'service': 'ml-recommendation-service',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)