import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import json
from typing import List, Dict, Tuple
from app.models import TestResult, User

class AIRecommendationEngine:
    """
    Система рекомендаций на основе ИИ для профориентации
    """
    
    def __init__(self, db_session):
        self.db_session = db_session
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.profession_profiles = self._load_profession_profiles()
    
    def _load_profession_profiles(self) -> Dict:
        """
        Загрузка профилей профессий с ключевыми характеристиками
        """
        profiles = {
            'Человек-природа': {
                'keywords': ['биология', 'экология', 'животные', 'растения', 'наука', 'лаборатория', 'исследование', 'медицина'],
                'traits': ['наблюдательность', 'терпение', 'внимание к деталям', 'научный подход'],
                'careers': ['биолог', 'ветеринар', 'лаборант', 'агроном', 'геолог', 'охотовед'],
                'skills': ['анализ', 'наблюдение', 'эксперимент', 'документация']
            },
            'Человек-техника': {
                'keywords': ['машины', 'инженерия', 'механика', 'электроника', 'конструирование', 'технологии'],
                'traits': ['логическое мышление', 'техническое воображение', 'практичность', 'точность'],
                'careers': ['инженер', 'механик', 'электрик', 'конструктор', 'программист', 'робототехник'],
                'skills': ['проектирование', 'монтаж', 'ремонт', 'автоматизация']
            },
            'Человек-человек': {
                'keywords': ['общение', 'помощь', 'обучение', 'воспитание', 'здоровье', 'психология'],
                'traits': ['эмоциональный интеллект', 'эмпатия', 'коммуникабельность', 'альтруизм'],
                'careers': ['учитель', 'врач', 'психолог', 'социальный работник', 'воспитатель', 'тренер'],
                'skills': ['обучение', 'поддержка', 'диагностика', 'консультирование']
            },
            'Человек-знаковая система': {
                'keywords': ['числа', 'формулы', 'анализ', 'статистика', 'бухгалтерия', 'экономика'],
                'traits': ['внимание к деталям', 'системность', 'логика', 'организованность'],
                'careers': ['бухгалтер', 'аналитик', 'экономист', 'статистик', 'банкир', 'аудитор'],
                'skills': ['анализ', 'расчеты', 'документация', 'планирование']
            },
            'Человек-художественный образ': {
                'keywords': ['творчество', 'дизайн', 'искусство', 'красота', 'эстетика', 'выражение'],
                'traits': ['креативность', 'воображение', 'эстетическое восприятие', 'самовыражение'],
                'careers': ['дизайнер', 'художник', 'архитектор', 'режиссер', 'актер', 'музыкант'],
                'skills': ['визуализация', 'дизайн', 'создание', 'редактирование']
            },
            'Реалистический': {
                'keywords': ['практика', 'физическая работа', 'инструменты', 'материалы', 'строительство'],
                'traits': ['практичность', 'стабильность', 'надежность', 'трудолюбие'],
                'careers': ['строитель', 'водитель', 'ремесленник', 'мастер', 'монтажник', 'слесарь'],
                'skills': ['работа с инструментами', 'монтаж', 'ремонт', 'физическая сила']
            },
            'Исследовательский': {
                'keywords': ['наука', 'исследование', 'анализ', 'теория', 'эксперимент', 'доказательства'],
                'traits': ['любознательность', 'аналитичность', 'независимость', 'критическое мышление'],
                'careers': ['научный сотрудник', 'исследователь', 'лаборант', 'аналитик', 'статистик', 'генетик'],
                'skills': ['исследование', 'анализ', 'эксперимент', 'публикация']
            },
            'Артистический': {
                'keywords': ['творчество', 'выражение', 'оригинальность', 'инновации', 'искусство', 'свобода'],
                'traits': ['креативность', 'интуиция', 'нестандартность', 'самовыражение'],
                'careers': ['писатель', 'музыкант', 'дизайнер', 'режиссер', 'актер', 'фотограф'],
                'skills': ['творчество', 'дизайн', 'аранжировка', 'режиссура']
            },
            'Социальный': {
                'keywords': ['помощь', 'обучение', 'развитие', 'сотрудничество', 'поддержка', 'воспитание'],
                'traits': ['эмпатия', 'терпение', 'общительность', 'ответственность'],
                'careers': ['учитель', 'врач', 'психолог', 'социальный работник', 'тренер', 'координатор'],
                'skills': ['обучение', 'поддержка', 'консультирование', 'разрешение конфликтов']
            },
            'Предпринимательский': {
                'keywords': ['лидерство', 'продажи', 'бизнес', 'управление', 'финансы', 'стратегия'],
                'traits': ['лидерские качества', 'уверенность', 'амбициозность', 'организованность'],
                'careers': ['менеджер', 'предприниматель', 'маркетолог', 'продажи', 'администратор', 'руководитель'],
                'skills': ['управление', 'переговоры', 'стратегия', 'организация']
            },
            'Конвенциональный': {
                'keywords': ['организация', 'порядок', 'документы', 'процедуры', 'системы', 'бюрократия'],
                'traits': ['организованность', 'внимательность', 'дисциплина', 'пунктуальность'],
                'careers': ['офис-менеджер', 'секретарь', 'бухгалтер', 'администратор', 'архивариус', 'оператор'],
                'skills': ['организация', 'ведение документов', 'архивирование', 'планирование']
            }
        }
        return profiles
    
    def calculate_similarity(self, user_result: TestResult) -> Dict[str, float]:
        """
        Рассчитывает схожесть пользователя с различными профессиональными сферами
        """
        # Извлечение ключевых характеристик из результата
        user_traits = self._extract_user_traits(user_result)
        
        similarities = {}
        
        for sphere, profile in self.profession_profiles.items():
            # Создание текстового представления профиля
            profile_text = ' '.join(profile['keywords'] + profile['traits'] + profile['skills'])
            user_text = ' '.join(user_traits)
            
            # Векторизация и расчет схожести
            try:
                vectorizer = TfidfVectorizer().fit([profile_text, user_text])
                vectors = vectorizer.transform([profile_text, user_text])
                similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
                similarities[sphere] = similarity
            except:
                # Если не удалось рассчитать, используем базовую оценку
                similarities[sphere] = 0.5
        
        return similarities
    
    def _extract_user_traits(self, result: TestResult) -> List[str]:
        """
        Извлекает характеристики пользователя из его результатов теста
        """
        traits = []
        
        # Добавляем сферы с высокими баллами
        if hasattr(result, 'results') and result.results:
            try:
                results_dict = json.loads(result.results)
                scores = results_dict.get('scores', {})
                
                # Берем сферы с высокими баллами
                for category, score in scores.items():
                    if score > 10:  # порог для "высокого" балла
                        traits.append(category.lower())
                        
                        # Добавляем ключевые слова для этой сферы
                        if category in self.profession_profiles:
                            traits.extend(self.profession_profiles[category]['keywords'][:3])
            except:
                pass
        
        # Если нет детализированных результатов, используем основную категорию
        if not traits:
            if result.methodology == 'klimov':
                traits.append(result.recommendation.lower() if result.recommendation else 'человек-природа')
            else:
                traits.append('исследовательский')
        
        return traits
    
    def get_personalized_recommendations(self, user_result: TestResult) -> Dict:
        """
        Получает персонализированные рекомендации для пользователя
        """
        similarities = self.calculate_similarity(user_result)
        
        # Сортировка по схожести
        sorted_similarities = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        
        # Формирование рекомендаций
        recommendations = {
            'top_matches': [],
            'career_suggestions': [],
            'skill_development': [],
            'learning_paths': [],
            'confidence_score': max(similarities.values()) if similarities else 0
        }
        
        for i, (sphere, similarity) in enumerate(sorted_similarities[:3]):
            profile = self.profession_profiles.get(sphere, {})
            
            match_info = {
                'sphere': sphere,
                'similarity': round(similarity * 100, 2),
                'careers': profile.get('careers', [])[:3],
                'skills': profile.get('skills', [])[:3],
                'traits': profile.get('traits', [])[:3]
            }
            
            recommendations['top_matches'].append(match_info)
            
            # Добавляем предложения по карьере
            for career in profile.get('careers', [])[:2]:
                recommendations['career_suggestions'].append({
                    'profession': career,
                    'match_percentage': round(similarity * 100, 2),
                    'reason': f'Соответствует вашим склонностям к {sphere.lower()}'
                })
        
        # Рекомендации по развитию навыков
        for sphere, similarity in sorted_similarities[:2]:
            if similarity > 0.3:  # минимальный порог
                profile = self.profession_profiles.get(sphere, {})
                for skill in profile.get('skills', [])[:2]:
                    recommendations['skill_development'].append({
                        'skill': skill,
                        'relevance': round(similarity * 100, 2),
                        'sphere': sphere
                    })
        
        # Образовательные пути
        if recommendations['top_matches']:
            top_match = recommendations['top_matches'][0]
            recommendations['learning_paths'] = [
                f'Рассмотрите обучение по направлению "{top_match["sphere"]}"',
                f'Изучите профессии: {", ".join(top_match["careers"][:2])}',
                f'Развивайте навыки: {", ".join(top_match["skills"][:3])}'
            ]
        
        return recommendations
    
    def find_similar_users(self, user_result: TestResult, limit: int = 5) -> List[Tuple[User, float]]:
        """
        Находит пользователей с похожими результатами
        """
        all_results = self.db_session.query(TestResult).all()
        similarities = []
        
        for other_result in all_results:
            if other_result.id != user_result.id:
                similarity = self._calculate_result_similarity(user_result, other_result)
                similarities.append((other_result.user, similarity))
        
        # Сортировка по схожести и ограничение количества
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:limit]
    
    def _calculate_result_similarity(self, result1: TestResult, result2: TestResult) -> float:
        """
        Рассчитывает схожесть двух результатов тестов
        """
        try:
            scores1 = json.loads(result1.results).get('scores', {}) if result1.results else {}
            scores2 = json.loads(result2.results).get('scores', {}) if result2.results else {}
            
            # Рассчитываем евклидово расстояние между оценками
            all_categories = set(scores1.keys()) | set(scores2.keys())
            if not all_categories:
                return 0.0
            
            distance = 0
            for category in all_categories:
                score1 = scores1.get(category, 0)
                score2 = scores2.get(category, 0)
                distance += (score1 - score2) ** 2
            
            # Преобразуем расстояние в схожесть (чем меньше расстояние, тем выше схожесть)
            similarity = 1 / (1 + distance ** 0.5)
            return min(similarity, 1.0)
        except:
            return 0.5  # стандартное значение при ошибках


# Глобальный экземпляр движка рекомендаций
recommendation_engine = None