import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import json
import pickle
from app import db
from app.models import User, TestResult, Notification


class MLRecommendationEngine:
    """
    Машинообучная система рекомендаций профессий
    """
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.scaler = StandardScaler()
        self.kmeans_model = None
        self.profession_vectors = {}
        self.user_profile_vectors = {}
        self.last_training_time = None
    
    def train_model(self):
        """
        Обучает модель на основе результатов тестов пользователей и информации о профессиях
        """
        print(f"[{datetime.now()}] Начинаю обучение ML-модели...")
        
        # Получаем все результаты тестов
        test_results = TestResult.query.all()
        
        if not test_results:
            print(f"[{datetime.now()}] Нет результатов тестов для обучения")
            return
        
        # Подготовка данных
        user_profiles = []
        user_ids = []
        profession_labels = []
        
        for result in test_results:
            try:
                results_dict = json.loads(result.results) if result.results else {}
                scores = results_dict.get('scores', {})
                
                # Преобразуем оценки в вектор
                if scores:
                    score_values = [float(scores.get(cat, 0)) for cat in sorted(scores.keys())]
                    user_profiles.append(score_values)
                    user_ids.append(result.user_id)
                    
                    # Добавляем доминирующую профессию
                    dominant_cat = results_dict.get('dominant_category', 'Неизвестно')
                    profession_labels.append(dominant_cat)
            except:
                continue
        
        if len(user_profiles) < 2:
            print(f"[{datetime.now()}] Недостаточно данных для обучения модели")
            return
        
        # Преобразуем в numpy массивы
        user_profiles = np.array(user_profiles)
        
        # Нормализуем данные
        user_profiles_scaled = self.scaler.fit_transform(user_profiles)
        
        # Определяем оптимальное количество кластеров (групп профессий)
        n_clusters = min(len(user_profiles), max(2, len(user_profiles) // 5))  # Не более 1/5 от числа пользователей
        
        # Обучаем K-means
        self.kmeans_model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = self.kmeans_model.fit_predict(user_profiles_scaled)
        
        # Создаем словарь соответствий кластеров профессиям
        cluster_professions = {}
        for i, label in enumerate(cluster_labels):
            if label not in cluster_professions:
                cluster_professions[label] = []
            if i < len(profession_labels):
                cluster_professions[label].append(profession_labels[i])
        
        # Назначаем основную профессию для каждого кластера
        self.cluster_main_professions = {}
        for cluster, profs in cluster_professions.items():
            # Находим самую частую профессию в кластере
            prof_counts = {}
            for prof in profs:
                prof_counts[prof] = prof_counts.get(prof, 0) + 1
            main_prof = max(prof_counts, key=prof_counts.get)
            self.cluster_main_professions[cluster] = main_prof
        
        self.last_training_time = datetime.now()
        print(f"[{datetime.now()}] ML-модель обучена. Кластеров: {n_clusters}")
    
    def get_user_cluster(self, user_scores):
        """
        Определяет кластер пользователя
        """
        if not self.kmeans_model:
            return None
        
        # Преобразуем оценки пользователя в вектор
        sorted_categories = sorted(user_scores.keys())
        user_vector = np.array([[float(user_scores.get(cat, 0)) for cat in sorted_categories]])
        
        # Нормализуем
        user_vector_scaled = self.scaler.transform(user_vector)
        
        # Предсказываем кластер
        cluster = self.kmeans_model.predict(user_vector_scaled)[0]
        
        return cluster
    
    def get_recommendations_for_user(self, user_id):
        """
        Генерирует рекомендации для конкретного пользователя
        """
        # Получаем последние результаты пользователя
        latest_result = TestResult.query.filter_by(user_id=user_id).order_by(TestResult.created_at.desc()).first()
        
        if not latest_result:
            return []
        
        try:
            results_dict = json.loads(latest_result.results) if latest_result.results else {}
            user_scores = results_dict.get('scores', {})
            
            if not user_scores:
                return []
            
            # Получаем кластер пользователя
            user_cluster = self.get_user_cluster(user_scores)
            
            if user_cluster is None:
                return []
            
            # Получаем основную профессию кластера
            recommended_profession = self.cluster_main_professions.get(user_cluster, 'Неизвестно')
            
            # Формируем рекомендации
            recommendations = [{
                'profession': recommended_profession,
                'confidence': 0.8,
                'reason': 'Похожие пользователи выбрали эту профессию',
                'similarity_to_others': self.get_similarity_to_cluster(user_scores, user_cluster)
            }]
            
            # Добавляем похожие профессии
            similar_professions = self.get_similar_professions(recommended_profession, limit=2)
            for prof in similar_professions:
                recommendations.append({
                    'profession': prof,
                    'confidence': 0.6,
                    'reason': 'Похожая профессия',
                    'similarity_to_others': 0.5
                })
            
            return recommendations
            
        except Exception as e:
            print(f"Ошибка при генерации рекомендаций для пользователя {user_id}: {str(e)}")
            return []
    
    def get_similarity_to_cluster(self, user_scores, cluster):
        """
        Вычисляет схожесть пользователя с кластером
        """
        if not self.kmeans_model:
            return 0.0
        
        # Преобразуем оценки пользователя в вектор
        sorted_categories = sorted(user_scores.keys())
        user_vector = np.array([[float(user_scores.get(cat, 0)) for cat in sorted_categories]])
        
        # Нормализуем
        user_vector_scaled = self.scaler.transform(user_vector)
        
        # Получаем центр кластера
        cluster_center = self.kmeans_model.cluster_centers_[cluster].reshape(1, -1)
        
        # Вычисляем схожесть
        similarity = cosine_similarity(user_vector_scaled, cluster_center)[0][0]
        
        return float(similarity)
    
    def get_similar_professions(self, profession, limit=3):
        """
        Находит похожие профессии (в упрощенной версии)
        """
        # В реальной системе это было бы сложнее - использовать векторные представления профессий
        # Сейчас используем простую эвристику
        similar_map = {
            'Программист': ['Разработчик', 'Инженер по разработке', 'IT-специалист'],
            'Менеджер': ['Администратор', 'Руководитель', 'Организатор'],
            'Инженер': ['Техник', 'Проектировщик', 'Конструктор'],
            'Дизайнер': ['Художник', 'Арт-директор', 'UX-дизайнер'],
            'Учитель': ['Преподаватель', 'Педагог', 'Воспитатель'],
            'Медик': ['Врач', 'Фармацевт', 'Медсестра'],
            'Юрист': ['Адвокат', 'Нотариус', 'Правовед'],
            'Экономист': ['Бухгалтер', 'Финансист', 'Аналитик'],
            'Психолог': ['Психотерапевт', 'Консультант', 'Психиатр'],
            'Журналист': ['Редактор', 'Копирайтер', 'Контент-мейкер']
        }
        
        return similar_map.get(profession, [])[:limit]
    
    def save_model(self, filepath):
        """
        Сохраняет обученную модель
        """
        model_data = {
            'vectorizer': self.vectorizer,
            'scaler': self.scaler,
            'kmeans_model': self.kmeans_model,
            'cluster_main_professions': getattr(self, 'cluster_main_professions', {}),
            'last_training_time': self.last_training_time
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath):
        """
        Загружает сохраненную модель
        """
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.scaler = model_data['scaler']
            self.kmeans_model = model_data['kmeans_model']
            self.cluster_main_professions = model_data['cluster_main_professions']
            self.last_training_time = model_data['last_training_time']
            
            return True
        except:
            return False


# Глобальный экземпляр движка рекомендаций
ml_engine = MLRecommendationEngine()


def train_ml_model():
    """
    Функция для обучения ML-модели
    """
    ml_engine.train_model()


def get_user_recommendations(user_id):
    """
    Получить рекомендации для пользователя
    """
    return ml_engine.get_recommendations_for_user(user_id)


def generate_ml_notifications():
    """
    Генерирует уведомления на основе ML-рекомендаций
    """
    print(f"[{datetime.now()}] Генерация ML-рекомендаций...")
    
    from app import create_app
    app = create_app()
    
    with app.app_context():
        # Обучаем модель (если нужно)
        if ml_engine.last_training_time is None or \
           (datetime.now() - ml_engine.last_training_time).days > 1:
            ml_engine.train_model()
        
        # Получаем всех пользователей
        users = User.query.all()
        
        for user in users:
            # Проверяем, есть ли у пользователя результаты тестов
            user_results = TestResult.query.filter_by(user_id=user.id).count()
            if user_results == 0:
                continue
            
            # Получаем рекомендации
            recommendations = get_user_recommendations(user.id)
            
            if recommendations:
                # Создаем уведомления для пользователя
                for rec in recommendations[:2]:  # Ограничиваем количество уведомлений
                    title = f"Рекомендация: {rec['profession']}"
                    message = f"На основе ваших результатов теста рекомендуем рассмотреть профессию '{rec['profession']}'. " \
                             f"Уверенность: {rec['confidence']:.0%}. {rec['reason']}."
                    
                    notification = Notification(
                        user_id=user.id,
                        title=title,
                        message=message,
                        type='info'
                    )
                    
                    db.session.add(notification)
        
        # Сохраняем изменения
        try:
            db.session.commit()
            print(f"[{datetime.now()}] ML-уведомления успешно созданы")
        except Exception as e:
            print(f"[{datetime.now()}] Ошибка при сохранении ML-уведомлений: {str(e)}")
            db.session.rollback()


if __name__ == "__main__":
    # При прямом запуске обучаем модель
    ml_engine.train_model()