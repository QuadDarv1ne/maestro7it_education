# -*- coding: utf-8 -*-
"""
Модуль предиктивной аналитики и машинного обучения для ПрофиТест
Обеспечивает прогнозирование пользовательского поведения, рекомендации и аналитику
"""
import logging
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.cluster import KMeans
import joblib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Union
from collections import defaultdict, Counter
import threading
from dataclasses import dataclass
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class PredictionType(Enum):
    """Типы предсказаний"""
    USER_BEHAVIOR = "user_behavior"
    TEST_OUTCOME = "test_outcome"
    CAREER_MATCH = "career_match"
    RETENTION_RISK = "retention_risk"
    PERFORMANCE_TREND = "performance_trend"

@dataclass
class PredictionResult:
    """Результат предсказания"""
    prediction: Any
    confidence: float
    features_used: List[str]
    prediction_type: str
    timestamp: str
    model_version: str
    explanations: Optional[Dict[str, Any]] = None

class PredictiveAnalyticsEngine:
    """Движок предиктивной аналитики с машинным обучением"""
    
    def __init__(self, app=None):
        self.app = app
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_columns = {}
        self.training_data = {}
        self.prediction_history = []
        self.model_versions = {}
        self.lock = threading.Lock()
        
        # Конфигурация
        self.config = {
            'models': {
                'user_behavior': {
                    'type': 'RandomForest',
                    'n_estimators': 100,
                    'max_depth': 10,
                    'random_state': 42
                },
                'test_outcome': {
                    'type': 'LogisticRegression',
                    'random_state': 42
                },
                'career_match': {
                    'type': 'RandomForest',
                    'n_estimators': 150,
                    'max_depth': 12,
                    'random_state': 42
                },
                'retention_risk': {
                    'type': 'RandomForest',
                    'n_estimators': 100,
                    'max_depth': 8,
                    'random_state': 42
                },
                'performance_trend': {
                    'type': 'KMeans',
                    'n_clusters': 5,
                    'random_state': 42
                }
            },
            'training': {
                'min_samples': 50,
                'validation_split': 0.2,
                'cross_validation_folds': 5
            },
            'predictions': {
                'max_history': 1000,
                'confidence_threshold': 0.7,
                'cache_predictions': True
            }
        }
        
        # Кэш предсказаний
        self.prediction_cache = {}
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация с Flask приложением"""
        self.app = app
        logger.info("Движок предиктивной аналитики инициализирован")
    
    def prepare_user_behavior_features(self, user_data: Dict[str, Any]) -> np.ndarray:
        """Подготовка признаков для предсказания поведения пользователя"""
        features = []
        
        # Числовые признаки
        features.extend([
            user_data.get('days_since_registration', 0),
            user_data.get('total_tests_taken', 0),
            user_data.get('avg_test_completion_time', 0),
            user_data.get('success_rate', 0),
            user_data.get('login_frequency', 0),
            user_data.get('last_login_days_ago', 999),
            user_data.get('profile_completion_percentage', 0),
            user_data.get('engagement_score', 0),
            user_data.get('session_duration_avg', 0),
            user_data.get('notifications_opened', 0)
        ])
        
        # Категориальные признаки (конвертированные в числа)
        gender_map = {'male': 1, 'female': 2, 'other': 3, 'not_specified': 0}
        features.append(gender_map.get(user_data.get('gender', 'not_specified'), 0))
        
        age_group = user_data.get('age_group', 'unknown')
        age_groups = {'18-25': 1, '26-35': 2, '36-45': 3, '46-55': 4, '55+': 5, 'unknown': 0}
        features.append(age_groups.get(age_group, 0))
        
        return np.array(features).reshape(1, -1)
    
    def prepare_test_outcome_features(self, test_data: Dict[str, Any]) -> np.ndarray:
        """Подготовка признаков для предсказания результата теста"""
        features = []
        
        # Признаки теста
        features.extend([
            test_data.get('test_complexity', 0),
            test_data.get('time_spent_minutes', 0),
            test_data.get('questions_answered', 0),
            test_data.get('correct_answers', 0),
            test_data.get('user_confidence_score', 0),
            test_data.get('previous_test_scores_avg', 0),
            test_data.get('time_of_day', 0),  # 0-24
            test_data.get('day_of_week', 0)   # 0-6
        ])
        
        # Тип теста (one-hot encoding)
        test_types = ['holland', 'klimov', 'personality', 'skills', 'interests']
        test_type = test_data.get('test_type', 'unknown')
        for ttype in test_types:
            features.append(1 if test_type == ttype else 0)
        
        return np.array(features).reshape(1, -1)
    
    def prepare_career_match_features(self, user_profile: Dict[str, Any], career_data: Dict[str, Any]) -> np.ndarray:
        """Подготовка признаков для предсказания соответствия карьеры"""
        features = []
        
        # Признаки пользователя
        features.extend([
            user_profile.get('personality_score', 0),
            user_profile.get('interest_alignment', 0),
            user_profile.get('skill_matching_score', 0),
            user_profile.get('values_alignment', 0),
            user_profile.get('work_style_fit', 0),
            user_profile.get('motivation_alignment', 0),
            user_profile.get('learning_readiness', 0),
            user_profile.get('career_maturity', 0)
        ])
        
        # Признаки карьеры
        features.extend([
            career_data.get('job_stability', 0),
            career_data.get('growth_potential', 0),
            career_data.get('salary_potential', 0),
            career_data.get('work_life_balance', 0),
            career_data.get('innovation_opportunity', 0),
            career_data.get('remote_work_option', 0)
        ])
        
        # Совместимость
        features.append(user_profile.get('personality_score', 0) * career_data.get('work_style_fit', 0))
        features.append(user_profile.get('interest_alignment', 0) * career_data.get('interest_match', 0))
        
        return np.array(features).reshape(1, -1)
    
    def prepare_retention_risk_features(self, user_data: Dict[str, Any]) -> np.ndarray:
        """Подготовка признаков для предсказания риска ухода пользователя"""
        features = []
        
        features.extend([
            user_data.get('days_since_last_activity', 999),
            user_data.get('total_sessions', 0),
            user_data.get('avg_session_gap', 0),
            user_data.get('feature_usage_diversity', 0),
            user_data.get('support_tickets_count', 0),
            user_data.get('negative_feedback_count', 0),
            user_data.get('subscription_age_months', 0),
            user_data.get('payment_success_rate', 1.0),
            user_data.get('help_center_visits', 0),
            user_data.get('incomplete_actions_count', 0)
        ])
        
        return np.array(features).reshape(1, -1)
    
    def prepare_performance_trend_features(self, user_data: Dict[str, Any]) -> np.ndarray:
        """Подготовка признаков для анализа тенденций производительности"""
        features = []
        
        features.extend([
            user_data.get('improvement_rate', 0),
            user_data.get('consistency_score', 0),
            user_data.get('peak_performance_score', 0),
            user_data.get('recent_decline_rate', 0),
            user_data.get('practice_frequency', 0),
            user_data.get('goal_achievement_rate', 0),
            user_data.get('feedback_responsiveness', 0),
            user_data.get('learning_velocity', 0)
        ])
        
        return np.array(features).reshape(1, -1)
    
    def train_model(self, model_type: str, training_data: List[Dict[str, Any]], target_column: str) -> bool:
        """Обучение модели машинного обучения"""
        try:
            if len(training_data) < self.config['training']['min_samples']:
                logger.warning(f"Недостаточно данных для обучения {model_type}: {len(training_data)} < {self.config['training']['min_samples']}")
                return False
            
            # Преобразование данных
            df = pd.DataFrame(training_data)
            
            if model_type == 'user_behavior':
                X = np.array([self.prepare_user_behavior_features(row) for row in training_data])
            elif model_type == 'test_outcome':
                X = np.array([self.prepare_test_outcome_features(row) for row in training_data])
            elif model_type == 'career_match':
                X = np.array([self.prepare_career_match_features(row.get('user_profile', {}), row.get('career_data', {})) for row in training_data])
            elif model_type == 'retention_risk':
                X = np.array([self.prepare_retention_risk_features(row) for row in training_data])
            elif model_type == 'performance_trend':
                X = np.array([self.prepare_performance_trend_features(row) for row in training_data])
            else:
                logger.error(f"Неизвестный тип модели: {model_type}")
                return False
            
            # Преобразование целевой переменной
            y = df[target_column].values
            
            # Масштабирование признаков
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X.reshape(-1, X.shape[-1])).reshape(X.shape)
            
            # Выбор модели
            model_config = self.config['models'][model_type]
            model_type_name = model_config['type']
            
            if model_type_name == 'RandomForest':
                model = RandomForestClassifier(
                    n_estimators=model_config.get('n_estimators', 100),
                    max_depth=model_config.get('max_depth', 10),
                    random_state=model_config.get('random_state', 42)
                )
            elif model_type_name == 'LogisticRegression':
                model = LogisticRegression(random_state=model_config.get('random_state', 42))
            elif model_type_name == 'KMeans':
                model = KMeans(
                    n_clusters=model_config.get('n_clusters', 5),
                    random_state=model_config.get('random_state', 42)
                )
            else:
                logger.error(f"Неизвестный тип модели ML: {model_type_name}")
                return False
            
            # Обучение модели
            if model_type_name == 'KMeans':
                model.fit(X_scaled)
                # Для KMeans используем кластеры как "предсказания"
                predictions = model.predict(X_scaled)
                y = predictions  # Используем кластеры как целевую переменную
            else:
                model.fit(X_scaled, y)
            
            # Сохранение модели
            with self.lock:
                self.models[model_type] = model
                self.scalers[model_type] = scaler
                self.model_versions[model_type] = datetime.utcnow().isoformat()
                self.feature_columns[model_type] = [f'feature_{i}' for i in range(X_scaled.shape[1])]
            
            logger.info(f"Модель {model_type} успешно обучена на {len(training_data)} образцах")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка обучения модели {model_type}: {e}")
            return False
    
    def predict(self, model_type: str, input_data: Dict[str, Any]) -> Optional[PredictionResult]:
        """Выполнение предсказания"""
        try:
            # Проверка наличия модели
            if model_type not in self.models:
                logger.warning(f"Модель {model_type} не обучена")
                return None
            
            # Подготовка признаков
            if model_type == 'user_behavior':
                X = self.prepare_user_behavior_features(input_data)
            elif model_type == 'test_outcome':
                X = self.prepare_test_outcome_features(input_data)
            elif model_type == 'career_match':
                user_profile = input_data.get('user_profile', {})
                career_data = input_data.get('career_data', {})
                X = self.prepare_career_match_features(user_profile, career_data)
            elif model_type == 'retention_risk':
                X = self.prepare_retention_risk_features(input_data)
            elif model_type == 'performance_trend':
                X = self.prepare_performance_trend_features(input_data)
            else:
                logger.error(f"Неизвестный тип модели: {model_type}")
                return None
            
            # Масштабирование
            scaler = self.scalers[model_type]
            X_scaled = scaler.transform(X)
            
            # Предсказание
            model = self.models[model_type]
            prediction = model.predict(X_scaled)[0]
            
            # Рассчет уверенности (если возможно)
            confidence = 0.8  # Значение по умолчанию
            
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(X_scaled)[0]
                confidence = max(probabilities)
            
            # Формирование результата
            result = PredictionResult(
                prediction=prediction,
                confidence=float(confidence),
                features_used=self.feature_columns[model_type],
                prediction_type=model_type,
                timestamp=datetime.utcnow().isoformat(),
                model_version=self.model_versions.get(model_type, 'unknown'),
                explanations=self._generate_explanations(model_type, input_data, prediction)
            )
            
            # Сохранение в историю
            with self.lock:
                self.prediction_history.append(result)
                if len(self.prediction_history) > self.config['predictions']['max_history']:
                    self.prediction_history.pop(0)
            
            return result
            
        except Exception as e:
            logger.error(f"Ошибка предсказания {model_type}: {e}")
            return None
    
    def _generate_explanations(self, model_type: str, input_data: Dict[str, Any], prediction: Any) -> Dict[str, Any]:
        """Генерация объяснений для предсказания"""
        explanations = {
            'model_type': model_type,
            'input_summary': self._summarize_input(input_data),
            'prediction_reasoning': self._get_prediction_reasoning(model_type, input_data, prediction)
        }
        
        return explanations
    
    def _summarize_input(self, input_data: Dict[str, Any]) -> str:
        """Создание краткого описания входных данных"""
        if 'user_profile' in input_data and 'career_data' in input_data:
            return f"User profile: {input_data['user_profile'].get('personality_score', 0):.2f}, Career: {input_data['career_data'].get('job_stability', 0):.2f}"
        elif 'total_tests_taken' in input_data:
            return f"Tests: {input_data.get('total_tests_taken', 0)}, Success rate: {input_data.get('success_rate', 0):.2f}"
        else:
            return "Input data summary"
    
    def _get_prediction_reasoning(self, model_type: str, input_data: Dict[str, Any], prediction: Any) -> str:
        """Получение обоснования предсказания"""
        reasoning_map = {
            'user_behavior': f"Based on user engagement patterns and historical behavior, predicting {prediction}",
            'test_outcome': f"Based on test-taking patterns and performance indicators, outcome likely {prediction}",
            'career_match': f"Personality and interest alignment suggests strong match for career path: {prediction}",
            'retention_risk': f"Activity patterns indicate {prediction} risk level",
            'performance_trend': f"Performance trajectory analysis shows trend cluster: {prediction}"
        }
        
        return reasoning_map.get(model_type, f"Prediction based on ML model analysis: {prediction}")
    
    def batch_predict(self, model_type: str, input_data_list: List[Dict[str, Any]]) -> List[Optional[PredictionResult]]:
        """Пакетное предсказание"""
        results = []
        for input_data in input_data_list:
            result = self.predict(model_type, input_data)
            results.append(result)
        return results
    
    def get_model_performance(self, model_type: str) -> Dict[str, Any]:
        """Получение метрик производительности модели"""
        if model_type not in self.models:
            return {'error': f'Model {model_type} not trained'}
        
        # В реальном приложении здесь будет вычисление метрик
        # на основе тестовой выборки
        return {
            'model_type': model_type,
            'is_trained': True,
            'training_date': self.model_versions.get(model_type),
            'feature_count': len(self.feature_columns.get(model_type, [])),
            'predictions_made': len([p for p in self.prediction_history if p.prediction_type == model_type])
        }
    
    def get_analytics_dashboard(self) -> Dict[str, Any]:
        """Получение аналитической панели"""
        with self.lock:
            return {
                'model_status': {
                    model_type: {
                        'trained': model_type in self.models,
                        'last_updated': self.model_versions.get(model_type),
                        'prediction_count': len([p for p in self.prediction_history if p.prediction_type == model_type])
                    }
                    for model_type in self.config['models'].keys()
                },
                'prediction_summary': {
                    'total_predictions': len(self.prediction_history),
                    'prediction_types': Counter(p.prediction_type for p in self.prediction_history),
                    'average_confidence': np.mean([p.confidence for p in self.prediction_history]) if self.prediction_history else 0
                },
                'recent_predictions': [
                    {
                        'prediction': p.prediction,
                        'confidence': p.confidence,
                        'type': p.prediction_type,
                        'timestamp': p.timestamp
                    }
                    for p in self.prediction_history[-10:]  # последние 10
                ]
            }
    
    def save_model(self, model_type: str, filepath: str) -> bool:
        """Сохранение модели в файл"""
        try:
            if model_type not in self.models:
                return False
            
            model_data = {
                'model': self.models[model_type],
                'scaler': self.scalers[model_type],
                'feature_columns': self.feature_columns[model_type],
                'model_version': self.model_versions[model_type]
            }
            
            joblib.dump(model_data, filepath)
            logger.info(f"Модель {model_type} сохранена в {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка сохранения модели {model_type}: {e}")
            return False
    
    def load_model(self, model_type: str, filepath: str) -> bool:
        """Загрузка модели из файла"""
        try:
            model_data = joblib.load(filepath)
            
            with self.lock:
                self.models[model_type] = model_data['model']
                self.scalers[model_type] = model_data['scaler']
                self.feature_columns[model_type] = model_data['feature_columns']
                self.model_versions[model_type] = model_data['model_version']
            
            logger.info(f"Модель {model_type} загружена из {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка загрузки модели {model_type}: {e}")
            return False

# Глобальный экземпляр
predictive_analytics = PredictiveAnalyticsEngine()

def register_predictive_analytics_commands(app):
    """Регистрация CLI команд для предиктивной аналитики"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('ml-dashboard')
    @with_appcontext
    def show_ml_dashboard():
        """Показать аналитическую панель ML"""
        dashboard = predictive_analytics.get_analytics_dashboard()
        click.echo("Аналитическая панель предиктивной аналитики:")
        click.echo(f"  Всего предсказаний: {dashboard['prediction_summary']['total_predictions']}")
        click.echo(f"  Средняя уверенность: {dashboard['prediction_summary']['average_confidence']:.2f}")
        
        click.echo("\nСтатус моделей:")
        for model_type, status in dashboard['model_status'].items():
            click.echo(f"  {model_type}: {'✓' if status['trained'] else '✗'} "
                      f"(предсказаний: {status['prediction_count']})")
    
    @app.cli.command('train-model')
    @click.argument('model_type')
    @click.option('--data-file', help='Файл с обучающими данными')
    @with_appcontext
    def train_ml_model(model_type, data_file):
        """Обучить модель машинного обучения"""
        if data_file:
            # Загрузка данных из файла
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    training_data = json.load(f)
                target_column = 'target'  # по умолчанию
            except Exception as e:
                click.echo(f"Ошибка загрузки данных: {e}")
                return
        else:
            # Использование демонстрационных данных
            training_data = [
                {'days_since_registration': 30, 'total_tests_taken': 5, 'success_rate': 0.8, 'target': 1},
                {'days_since_registration': 10, 'total_tests_taken': 2, 'success_rate': 0.6, 'target': 0},
                {'days_since_registration': 60, 'total_tests_taken': 10, 'success_rate': 0.9, 'target': 1}
            ]
            target_column = 'target'
        
        success = predictive_analytics.train_model(model_type, training_data, target_column)
        if success:
            click.echo(f"Модель {model_type} успешно обучена")
        else:
            click.echo(f"Ошибка обучения модели {model_type}")

def ml_predict(prediction_type: PredictionType):
    """Декоратор для ML предсказаний"""
    def decorator(func):
        from functools import wraps
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Попытка выполнения предсказания
            if hasattr(predictive_analytics, 'predict'):
                try:
                    prediction = predictive_analytics.predict(
                        prediction_type.value,
                        result if isinstance(result, dict) else {'input': result}
                    )
                    if prediction:
                        # Добавление предсказания к результату
                        if isinstance(result, dict):
                            result['ml_prediction'] = {
                                'prediction': prediction.prediction,
                                'confidence': prediction.confidence,
                                'timestamp': prediction.timestamp
                            }
                except Exception as e:
                    logger.warning(f"Ошибка ML предсказания: {e}")
            
            return result
        
        return wrapper
    return decorator