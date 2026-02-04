# -*- coding: utf-8 -*-
"""
Модуль обработки данных для ПрофиТест
Предоставляет расширенные возможности обработки и анализа данных пользователей
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app import db
from app.models import User, TestResult, CareerGoal, LearningPath
from collections import defaultdict
import json
import logging


class DataProcessor:
    """
    Процессор данных для системы ПрофиТест.
    Обрабатывает и анализирует данные пользователей для генерации инсайтов.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.processed_data_cache = {}
    
    def process_user_data_batch(self, user_ids=None, batch_size=100):
        """
        Обрабатывает данные пользователей пакетами для повышения производительности.
        
        Args:
            user_ids: Список ID пользователей для обработки (если None, обрабатываются все)
            batch_size: Размер пакета для обработки
            
        Returns:
            dict: Результаты обработки данных
        """
        try:
            if user_ids is None:
                users = User.query.all()
            else:
                users = User.query.filter(User.id.in_(user_ids)).all()
            
            results = {
                'total_users_processed': 0,
                'processing_stats': {},
                'user_insights': [],
                'batch_results': []
            }
            
            # Обработка пакетами
            for i in range(0, len(users), batch_size):
                batch = users[i:i + batch_size]
                batch_result = self._process_user_batch(batch)
                results['batch_results'].append(batch_result)
                results['total_users_processed'] += len(batch)
            
            # Агрегация результатов
            results['processing_stats'] = self._aggregate_batch_stats(results['batch_results'])
            results['user_insights'] = self._generate_batch_insights(results['batch_results'])
            
            return results
            
        except Exception as e:
            self.logger.error(f"Ошибка при пакетной обработке данных: {str(e)}")
            return {'error': str(e)}
    
    def _process_user_batch(self, users):
        """
        Обрабатывает пакет пользователей.
        
        Args:
            users: Список объектов User
            
        Returns:
            dict: Результаты обработки пакета
        """
        batch_results = {
            'user_count': len(users),
            'test_results': [],
            'career_data': [],
            'learning_data': [],
            'engagement_metrics': {}
        }
        
        for user in users:
            try:
                # Получение данных тестов
                user_tests = TestResult.query.filter_by(user_id=user.id).all()
                test_data = []
                for test in user_tests:
                    test_info = {
                        'id': test.id,
                        'methodology': test.methodology,
                        'created_at': test.created_at,
                        'results': json.loads(test.results) if test.results else {}
                    }
                    test_data.append(test_info)
                
                batch_results['test_results'].extend(test_data)
                
                # Получение данных карьерных целей
                user_goals = CareerGoal.query.filter_by(user_id=user.id).all()
                goal_data = [{
                    'id': goal.id,
                    'title': goal.title,
                    'status': goal.current_status,
                    'priority': goal.priority,
                    'created_at': goal.created_at
                } for goal in user_goals]
                
                batch_results['career_data'].extend(goal_data)
                
                # Получение данных образовательных траекторий
                user_paths = LearningPath.query.filter_by(user_id=user.id).all()
                path_data = [{
                    'id': path.id,
                    'title': path.title,
                    'status': path.status,
                    'difficulty': path.difficulty_level,
                    'created_at': path.created_at
                } for path in user_paths]
                
                batch_results['learning_data'].extend(path_data)
                
            except Exception as e:
                self.logger.warning(f"Ошибка при обработке пользователя {user.id}: {str(e)}")
                continue
        
        # Вычисление метрик вовлеченности для пакета
        batch_results['engagement_metrics'] = self._calculate_batch_engagement(batch_results)
        
        return batch_results
    
    def _calculate_batch_engagement(self, batch_data):
        """
        Вычисляет метрики вовлеченности для пакета данных.
        
        Args:
            batch_data: Данные пакета
            
        Returns:
            dict: Метрики вовлеченности
        """
        engagement_metrics = {
            'total_tests': len(batch_data['test_results']),
            'total_goals': len(batch_data['career_data']),
            'total_paths': len(batch_data['learning_data']),
            'avg_tests_per_user': 0,
            'avg_goals_per_user': 0,
            'avg_paths_per_user': 0,
            'activity_score': 0
        }
        
        user_count = batch_data['user_count']
        if user_count > 0:
            engagement_metrics['avg_tests_per_user'] = engagement_metrics['total_tests'] / user_count
            engagement_metrics['avg_goals_per_user'] = engagement_metrics['total_goals'] / user_count
            engagement_metrics['avg_paths_per_user'] = engagement_metrics['total_paths'] / user_count
            
            # Вычисление общего балла активности
            activity_components = [
                engagement_metrics['avg_tests_per_user'] * 0.4,
                engagement_metrics['avg_goals_per_user'] * 0.3,
                engagement_metrics['avg_paths_per_user'] * 0.3
            ]
            engagement_metrics['activity_score'] = sum(activity_components)
        
        return engagement_metrics
    
    def _aggregate_batch_stats(self, batch_results):
        """
        Агрегирует статистику из всех пакетов.
        
        Args:
            batch_results: Результаты обработки пакетов
            
        Returns:
            dict: Агрегированная статистика
        """
        aggregated_stats = {
            'total_users': sum(batch['user_count'] for batch in batch_results),
            'total_tests': sum(batch['engagement_metrics']['total_tests'] for batch in batch_results),
            'total_goals': sum(batch['engagement_metrics']['total_goals'] for batch in batch_results),
            'total_paths': sum(batch['engagement_metrics']['total_paths'] for batch in batch_results),
            'avg_activity_score': np.mean([batch['engagement_metrics']['activity_score'] for batch in batch_results]) if batch_results else 0
        }
        
        return aggregated_stats
    
    def _generate_batch_insights(self, batch_results):
        """
        Генерирует инсайты из результатов пакетной обработки.
        
        Args:
            batch_results: Результаты обработки пакетов
            
        Returns:
            list: Список инсайтов
        """
        insights = []
        
        # Анализ активности
        avg_activity_scores = [batch['engagement_metrics']['activity_score'] for batch in batch_results]
        if avg_activity_scores:
            overall_avg = np.mean(avg_activity_scores)
            if overall_avg < 1:
                insights.append({
                    'type': 'low_engagement',
                    'title': 'Низкий уровень вовлеченности',
                    'description': 'Средний уровень активности пользователей ниже нормы',
                    'recommendation': 'Рассмотрите внедрение программ мотивации и напоминаний'
                })
            elif overall_avg > 3:
                insights.append({
                    'type': 'high_engagement',
                    'title': 'Высокий уровень вовлеченности',
                    'description': 'Пользователи активно используют платформу',
                    'recommendation': 'Поддерживайте текущий уровень вовлеченности'
                })
        
        # Анализ распределения активности
        test_counts = [batch['engagement_metrics']['total_tests'] for batch in batch_results]
        if test_counts and np.std(test_counts) > np.mean(test_counts) * 0.5:
            insights.append({
                'type': 'uneven_distribution',
                'title': 'Неравномерное распределение активности',
                'description': 'Активность пользователей сильно варьируется',
                'recommendation': 'Изучите причины низкой активности у части пользователей'
            })
        
        return insights
    
    def generate_user_profile_analytics(self, user_id):
        """
        Генерирует аналитику профиля пользователя.
        
        Args:
            user_id: ID пользователя
            
        Returns:
            dict: Аналитика профиля пользователя
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return {'error': 'Пользователь не найден'}
            
            # Получение всех данных пользователя
            test_results = TestResult.query.filter_by(user_id=user_id).all()
            career_goals = CareerGoal.query.filter_by(user_id=user_id).all()
            learning_paths = LearningPath.query.filter_by(user_id=user_id).all()
            
            analytics = {
                'user_info': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'created_at': user.created_at,
                    'account_age_days': (datetime.now(datetime.UTC) - user.created_at).days if user.created_at else 0
                },
                'test_analytics': self._analyze_test_data(test_results),
                'career_analytics': self._analyze_career_data(career_goals),
                'learning_analytics': self._analyze_learning_data(learning_paths),
                'engagement_score': 0,
                'recommendations': []
            }
            
            # Вычисление общего балла вовлеченности
            analytics['engagement_score'] = self._calculate_user_engagement_score(
                analytics['test_analytics'],
                analytics['career_analytics'],
                analytics['learning_analytics']
            )
            
            # Генерация рекомендаций
            analytics['recommendations'] = self._generate_user_recommendations(analytics)
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Ошибка при генерации аналитики профиля: {str(e)}")
            return {'error': str(e)}
    
    def _analyze_test_data(self, test_results):
        """
        Анализирует данные тестов пользователя.
        
        Args:
            test_results: Результаты тестов
            
        Returns:
            dict: Аналитика тестов
        """
        if not test_results:
            return {
                'total_tests': 0,
                'methodologies_used': [],
                'test_frequency': 0,
                'latest_test_date': None,
                'test_consistency': 0
            }
        
        methodologies = list(set(test.methodology for test in test_results))
        test_dates = [test.created_at for test in test_results]
        
        # Вычисление частоты тестирования
        if len(test_dates) > 1:
            date_diffs = [(test_dates[i] - test_dates[i-1]).days for i in range(1, len(test_dates))]
            avg_frequency = np.mean(date_diffs) if date_diffs else 0
        else:
            avg_frequency = 0
        
        return {
            'total_tests': len(test_results),
            'methodologies_used': methodologies,
            'test_frequency': avg_frequency,
            'latest_test_date': max(test_dates) if test_dates else None,
            'test_consistency': len(methodologies) / len(test_results) if test_results else 0
        }
    
    def _analyze_career_data(self, career_goals):
        """
        Анализирует данные карьерных целей пользователя.
        
        Args:
            career_goals: Карьерные цели
            
        Returns:
            dict: Аналитика карьерных целей
        """
        if not career_goals:
            return {
                'total_goals': 0,
                'active_goals': 0,
                'completed_goals': 0,
                'avg_priority': 0,
                'goal_diversity': 0
            }
        
        active_goals = len([g for g in career_goals if g.current_status == 'in_progress'])
        completed_goals = len([g for g in career_goals if g.current_status == 'achieved'])
        avg_priority = np.mean([g.priority for g in career_goals]) if career_goals else 0
        
        # Вычисление разнообразия целей
        goal_titles = [g.title.lower() for g in career_goals]
        unique_words = set()
        for title in goal_titles:
            unique_words.update(title.split())
        goal_diversity = len(unique_words) / len(goal_titles) if goal_titles else 0
        
        return {
            'total_goals': len(career_goals),
            'active_goals': active_goals,
            'completed_goals': completed_goals,
            'avg_priority': avg_priority,
            'goal_diversity': goal_diversity
        }
    
    def _analyze_learning_data(self, learning_paths):
        """
        Анализирует данные образовательных траекторий пользователя.
        
        Args:
            learning_paths: Образовательные траектории
            
        Returns:
            dict: Аналитика образовательных траекторий
        """
        if not learning_paths:
            return {
                'total_paths': 0,
                'active_paths': 0,
                'completed_paths': 0,
                'avg_difficulty': 0,
                'learning_intensity': 0
            }
        
        active_paths = len([p for p in learning_paths if p.status == 'in_progress'])
        completed_paths = len([p for p in learning_paths if p.status == 'completed'])
        
        # Вычисление средней сложности
        difficulty_map = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        difficulties = [difficulty_map.get(p.difficulty_level, 1) for p in learning_paths]
        avg_difficulty = np.mean(difficulties) if difficulties else 1
        
        # Вычисление интенсивности обучения
        total_duration = sum([p.duration_weeks or 0 for p in learning_paths])
        learning_intensity = total_duration / len(learning_paths) if learning_paths else 0
        
        return {
            'total_paths': len(learning_paths),
            'active_paths': active_paths,
            'completed_paths': completed_paths,
            'avg_difficulty': avg_difficulty,
            'learning_intensity': learning_intensity
        }
    
    def _calculate_user_engagement_score(self, test_analytics, career_analytics, learning_analytics):
        """
        Вычисляет общий балл вовлеченности пользователя.
        
        Args:
            test_analytics: Аналитика тестов
            career_analytics: Аналитика карьерных целей
            learning_analytics: Аналитика образовательных траекторий
            
        Returns:
            float: Балл вовлеченности (0-10)
        """
        # Нормализованные компоненты
        test_score = min(test_analytics['total_tests'] / 5, 1) * 3  # Максимум 3 балла
        career_score = min((career_analytics['active_goals'] + career_analytics['completed_goals']) / 3, 1) * 3  # Максимум 3 балла
        learning_score = min((learning_analytics['active_paths'] + learning_analytics['completed_paths']) / 3, 1) * 4  # Максимум 4 балла
        
        return round(test_score + career_score + learning_score, 2)
    
    def _generate_user_recommendations(self, analytics):
        """
        Генерирует рекомендации для пользователя на основе аналитики.
        
        Args:
            analytics: Аналитика пользователя
            
        Returns:
            list: Список рекомендаций
        """
        recommendations = []
        engagement_score = analytics['engagement_score']
        
        # Рекомендации на основе балла вовлеченности
        if engagement_score < 3:
            recommendations.append({
                'type': 'low_engagement',
                'priority': 'high',
                'title': 'Повысьте активность',
                'description': 'Ваш уровень вовлеченности низкий. Рекомендуем пройти дополнительные тесты.',
                'actions': ['Пройти тест Холланда', 'Пройти тест Климова', 'Установить карьерные цели']
            })
        elif engagement_score < 6:
            recommendations.append({
                'type': 'moderate_engagement',
                'priority': 'medium',
                'title': 'Развивайте профиль',
                'description': 'У вас хороший старт. Продолжайте развивать карьерные цели и образовательные траектории.',
                'actions': ['Создать образовательную траекторию', 'Обновить карьерные цели', 'Пройти дополнительные тесты']
            })
        else:
            recommendations.append({
                'type': 'high_engagement',
                'priority': 'low',
                'title': 'Отличная активность!',
                'description': 'Вы активно используете платформу. Продолжайте в том же духе!',
                'actions': ['Поделиться опытом с другими пользователями', 'Помочь новичкам', 'Участвовать в обсуждениях']
            })
        
        # Рекомендации на основе анализа тестов
        test_analytics = analytics['test_analytics']
        if test_analytics['total_tests'] == 0:
            recommendations.append({
                'type': 'no_tests',
                'priority': 'high',
                'title': 'Начните с тестирования',
                'description': 'Вы еще не прошли ни одного профессионального теста.',
                'actions': ['Пройти тест Холланда', 'Пройти тест Климова']
            })
        elif test_analytics['total_tests'] < 3:
            recommendations.append({
                'type': 'limited_testing',
                'priority': 'medium',
                'title': 'Пройдите больше тестов',
                'description': 'Для более точных рекомендаций рекомендуем пройти дополнительные тесты.',
                'actions': ['Пройти тест на склонности', 'Пройти тест на интересы']
            })
        
        # Рекомендации на основе карьерных целей
        career_analytics = analytics['career_analytics']
        if career_analytics['total_goals'] == 0:
            recommendations.append({
                'type': 'no_goals',
                'priority': 'high',
                'title': 'Установите карьерные цели',
                'description': 'Создайте карьерные цели для структурированного развития.',
                'actions': ['Создать первую карьерную цель', 'Определить приоритеты развития']
            })
        
        # Рекомендации на основе образовательных траекторий
        learning_analytics = analytics['learning_analytics']
        if learning_analytics['total_paths'] == 0 and career_analytics['total_goals'] > 0:
            recommendations.append({
                'type': 'no_learning_paths',
                'priority': 'medium',
                'title': 'Создайте образовательные траектории',
                'description': 'Создайте план обучения для достижения карьерных целей.',
                'actions': ['Создать первую образовательную траекторию', 'Выбрать подходящие курсы']
            })
        
        return recommendations


# Глобальный экземпляр
data_processor = DataProcessor()