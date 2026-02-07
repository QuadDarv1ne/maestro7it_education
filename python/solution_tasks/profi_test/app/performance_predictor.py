# -*- coding: utf-8 -*-
"""
Предиктивный анализ производительности с машинным обучением
"""
import logging
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import threading
from collections import deque
from dataclasses import dataclass
import pickle
import os
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

@dataclass
class PredictionResult:
    """Результат предиктивного анализа"""
    metric_name: str
    predicted_value: float
    confidence_interval: Tuple[float, float]
    confidence_score: float
    timeframe: str
    timestamp: datetime
    features_used: List[str]

@dataclass
class PerformancePattern:
    """Паттерн производительности"""
    pattern_type: str
    description: str
    confidence: float
    affected_metrics: List[str]
    timestamp: datetime

class PerformancePredictor:
    """Предиктор производительности на основе машинного обучения"""
    
    def __init__(self, app=None):
        self.app = app
        self.models = {}
        self.scalers = {}
        self.training_data = {}
        self.prediction_history = deque(maxlen=1000)
        self.patterns_history = deque(maxlen=500)
        self.is_training = False
        self.training_thread = None
        self.model_accuracy = {}
        self.feature_importance = {}
        
        # Параметры обучения
        self.min_training_samples = 100
        self.training_interval = 3600  # 1 час
        self.prediction_horizons = {
            'short_term': 300,    # 5 минут
            'medium_term': 1800,  # 30 минут
            'long_term': 3600     # 1 час
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализирует предиктор производительности"""
        self.app = app
        app.performance_predictor = self
        self.start_training_cycle()
        logger.info("Performance predictor initialized")
    
    def start_training_cycle(self):
        """Запускает цикл обучения моделей"""
        if not self.is_training:
            self.is_training = True
            self.training_thread = threading.Thread(target=self._training_loop, daemon=True)
            self.training_thread.start()
            logger.info("Performance prediction training cycle started")
    
    def stop_training_cycle(self):
        """Останавливает цикл обучения"""
        self.is_training = False
        if self.training_thread:
            self.training_thread.join(timeout=5)
        logger.info("Performance prediction training cycle stopped")
    
    def _training_loop(self):
        """Цикл автоматического обучения"""
        while self.is_training:
            try:
                # Собираем новые данные
                new_data = self._collect_training_data()
                if new_data:
                    self._update_training_data(new_data)
                
                # Обучаем модели если достаточно данных
                if self._has_sufficient_data():
                    self._train_models()
                
                # Делаем прогнозы
                self._make_predictions()
                
                # Анализируем паттерны
                self._analyze_patterns()
                
                time.sleep(self.training_interval)
                
            except Exception as e:
                logger.error(f"Error in performance prediction training: {e}")
                time.sleep(300)  # Ждем 5 минут при ошибке
    
    def _collect_training_data(self) -> Optional[pd.DataFrame]:
        """Собирает данные для обучения"""
        try:
            # Собираем метрики за последние 24 часа
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=24)
            
            metrics_data = []
            
            # Если есть исторические данные в приложении
            if hasattr(self.app, 'performance_monitor'):
                # Получаем данные метрик
                try:
                    # Try to get metrics history with the expected parameters
                    metrics_history = self.app.performance_monitor.get_metrics_history(
                        start_time=start_time,
                        end_time=end_time,
                        interval_minutes=5
                    )
                    
                    for timestamp, metrics in metrics_history.items():
                        data_point = {
                            'timestamp': timestamp,
                            'cpu_percent': metrics.get('cpu_percent', 0),
                            'memory_percent': metrics.get('memory_percent', 0),
                            'response_time': metrics.get('avg_response_time', 0),
                            'request_rate': metrics.get('requests_per_second', 0),
                            'error_rate': metrics.get('error_rate', 0),
                            'active_users': metrics.get('active_users', 0),
                            'database_connections': metrics.get('db_connections', 0),
                            'hour_of_day': timestamp.hour,
                            'day_of_week': timestamp.weekday(),
                            'is_weekend': 1 if timestamp.weekday() >= 5 else 0
                        }
                        metrics_data.append(data_point)
                except TypeError:
                    # Fallback to the method signature we implemented
                    metrics_history = self.app.performance_monitor.get_metrics_history(hours=24)
                    
                    # Convert the returned data to the expected format
                    for metric_key, metric_values in metrics_history.items():
                        for entry in metric_values:
                            if 'timestamp' in entry and 'value' in entry:
                                timestamp = datetime.fromisoformat(entry['timestamp'])
                                if start_time <= timestamp <= end_time:
                                    # Map the metric to the expected names
                                    if 'cpu' in metric_key.lower():
                                        metric_name = 'cpu_percent'
                                    elif 'memory' in metric_key.lower():
                                        metric_name = 'memory_percent'
                                    elif 'response' in metric_key.lower():
                                        metric_name = 'response_time'
                                    elif 'request' in metric_key.lower():
                                        metric_name = 'request_rate'
                                    elif 'error' in metric_key.lower():
                                        metric_name = 'error_rate'
                                    else:
                                        continue  # Skip unknown metrics
                                        
                                    data_point = {
                                        'timestamp': timestamp,
                                        metric_name: entry['value'],
                                        'hour_of_day': timestamp.hour,
                                        'day_of_week': timestamp.weekday(),
                                        'is_weekend': 1 if timestamp.weekday() >= 5 else 0,
                                        'cpu_percent': entry['value'] if 'cpu' in metric_key.lower() else 0,
                                        'memory_percent': entry['value'] if 'memory' in metric_key.lower() else 0,
                                        'response_time': entry['value'] if 'response' in metric_key.lower() else 0,
                                        'request_rate': entry['value'] if 'request' in metric_key.lower() else 0,
                                        'error_rate': entry['value'] if 'error' in metric_key.lower() else 0,
                                        'active_users': 0,
                                        'database_connections': 0
                                    }
                                    metrics_data.append(data_point)
            
            # Если нет исторических данных, используем текущие
            if not metrics_data:
                current_metrics = self._collect_current_metrics()
                data_point = {
                    'timestamp': datetime.utcnow(),
                    'cpu_percent': current_metrics.get('cpu_percent', 0),
                    'memory_percent': current_metrics.get('memory_percent', 0),
                    'response_time': current_metrics.get('response_time', 0),
                    'request_rate': current_metrics.get('request_rate', 0),
                    'error_rate': current_metrics.get('error_rate', 0),
                    'active_users': current_metrics.get('active_users', 0),
                    'database_connections': current_metrics.get('database_connections', 0),
                    'hour_of_day': datetime.utcnow().hour,
                    'day_of_week': datetime.utcnow().weekday(),
                    'is_weekend': 1 if datetime.utcnow().weekday() >= 5 else 0
                }
                metrics_data.append(data_point)
            
            if metrics_data:
                return pd.DataFrame(metrics_data)
            
        except Exception as e:
            logger.error(f"Error collecting training data: {e}")
        
        return None
    
    def _collect_current_metrics(self) -> Dict[str, float]:
        """Собирает текущие метрики"""
        metrics = {}
        
        try:
            import psutil
            metrics['cpu_percent'] = psutil.cpu_percent(interval=1)
            metrics['memory_percent'] = psutil.virtual_memory().percent
            
            # Метрики приложения
            if hasattr(self.app, 'performance_monitor'):
                app_metrics = self.app.performance_monitor.get_current_metrics()
                metrics['response_time'] = app_metrics.get('avg_response_time', 0.5)
                metrics['request_rate'] = app_metrics.get('requests_per_second', 10.0)
                metrics['error_rate'] = app_metrics.get('error_rate', 0.0)
                metrics['active_users'] = app_metrics.get('active_users', 1)
                metrics['database_connections'] = app_metrics.get('db_connections', 5)
            else:
                metrics.update({
                    'response_time': 0.5,
                    'request_rate': 10.0,
                    'error_rate': 0.0,
                    'active_users': 1,
                    'database_connections': 5
                })
                
        except Exception as e:
            logger.error(f"Error collecting current metrics: {e}")
            metrics.update({
                'cpu_percent': 50.0,
                'memory_percent': 50.0,
                'response_time': 0.5,
                'request_rate': 10.0,
                'error_rate': 0.0,
                'active_users': 1,
                'database_connections': 5
            })
        
        return metrics
    
    def _update_training_data(self, new_data: pd.DataFrame):
        """Обновляет обучающие данные"""
        for metric_name in ['cpu_percent', 'memory_percent', 'response_time', 'request_rate']:
            if metric_name not in self.training_data:
                self.training_data[metric_name] = pd.DataFrame()
            
            # Добавляем новые данные
            self.training_data[metric_name] = pd.concat([
                self.training_data[metric_name],
                new_data
            ]).tail(10000)  # Сохраняем максимум 10000 точек
    
    def _has_sufficient_data(self) -> bool:
        """Проверяет наличие достаточных данных для обучения"""
        if not self.training_data:
            return False
        
        # Проверяем каждый метрик
        for metric_data in self.training_data.values():
            if len(metric_data) < self.min_training_samples:
                return False
        
        return True
    
    def _train_models(self):
        """Обучает предиктивные модели"""
        try:
            for metric_name, data in self.training_data.items():
                if len(data) >= self.min_training_samples:
                    self._train_model_for_metric(metric_name, data)
            
            logger.info("Performance prediction models trained successfully")
            
        except Exception as e:
            logger.error(f"Error training prediction models: {e}")
    
    def _train_model_for_metric(self, metric_name: str, data: pd.DataFrame):
        """Обучает модель для конкретной метрики"""
        try:
            # Подготавливаем данные
            feature_columns = [
                'hour_of_day', 'day_of_week', 'is_weekend',
                'cpu_percent', 'memory_percent', 'request_rate',
                'error_rate', 'active_users', 'database_connections'
            ]
            
            # Убираем целевую метрику из признаков
            feature_columns = [col for col in feature_columns if col != metric_name]
            
            # Фильтруем существующие колонки
            available_features = [col for col in feature_columns if col in data.columns]
            
            if not available_features:
                logger.warning(f"No available features for {metric_name}")
                return
            
            X = data[available_features].values
            y = data[metric_name].values
            
            # Разделяем данные
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Нормализуем признаки
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            # Обучаем несколько моделей
            models = {
                'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'linear': LinearRegression()
            }
            
            best_model = None
            best_score = float('inf')
            
            for model_name, model in models.items():
                try:
                    model.fit(X_train_scaled, y_train)
                    y_pred = model.predict(X_test_scaled)
                    mse = mean_squared_error(y_test, y_pred)
                    
                    if mse < best_score:
                        best_score = mse
                        best_model = model
                    
                    logger.info(f"{metric_name} - {model_name}: MSE = {mse:.4f}")
                    
                except Exception as e:
                    logger.error(f"Error training {model_name} for {metric_name}: {e}")
            
            if best_model:
                # Сохраняем лучшую модель
                model_key = f"predictor_{metric_name}"
                self.models[model_key] = best_model
                self.scalers[model_key] = scaler
                self.model_accuracy[metric_name] = {
                    'mse': best_score,
                    'mae': mean_absolute_error(y_test, best_model.predict(X_test_scaled))
                }
                
                # Рассчитываем важность признаков
                if hasattr(best_model, 'feature_importances_'):
                    self.feature_importance[metric_name] = dict(zip(available_features, best_model.feature_importances_))
                
                logger.info(f"Best model for {metric_name}: MSE = {best_score:.4f}")
            
        except Exception as e:
            logger.error(f"Error training model for {metric_name}: {e}")
    
    def _make_predictions(self):
        """Делает прогнозы для всех метрик"""
        try:
            current_features = self._prepare_current_features()
            
            for metric_name in ['cpu_percent', 'memory_percent', 'response_time', 'request_rate']:
                prediction = self.predict_metric(metric_name, current_features)
                if prediction:
                    self.prediction_history.append({
                        'prediction': prediction.__dict__,
                        'timestamp': time.time()
                    })
                    
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
    
    def _prepare_current_features(self) -> np.ndarray:
        """Подготавливает признаки для текущего момента"""
        current_time = datetime.utcnow()
        current_metrics = self._collect_current_metrics()
        
        features = np.array([[
            current_time.hour,  # hour_of_day
            current_time.weekday(),  # day_of_week
            1 if current_time.weekday() >= 5 else 0,  # is_weekend
            current_metrics.get('cpu_percent', 50.0),
            current_metrics.get('memory_percent', 50.0),
            current_metrics.get('request_rate', 10.0),
            current_metrics.get('error_rate', 0.0),
            current_metrics.get('active_users', 1),
            current_metrics.get('database_connections', 5)
        ]])
        
        return features
    
    def predict_metric(self, metric_name: str, features: np.ndarray = None) -> Optional[PredictionResult]:
        """Делает прогноз для конкретной метрики"""
        try:
            model_key = f"predictor_{metric_name}"
            
            if model_key not in self.models:
                return None
            
            if features is None:
                features = self._prepare_current_features()
            
            # Нормализуем признаки
            scaler = self.scalers[model_key]
            features_scaled = scaler.transform(features)
            
            # Делаем прогноз
            model = self.models[model_key]
            prediction = model.predict(features_scaled)[0]
            
            # Рассчитываем доверительный интервал (упрощенный)
            if metric_name in self.model_accuracy:
                mse = self.model_accuracy[metric_name]['mse']
                std_error = np.sqrt(mse)
                confidence_interval = (
                    max(0, prediction - 2 * std_error),
                    prediction + 2 * std_error
                )
            else:
                confidence_interval = (prediction * 0.8, prediction * 1.2)
            
            # Рассчитываем уровень доверия
            confidence_score = max(0.5, 1.0 - (confidence_interval[1] - confidence_interval[0]) / prediction if prediction > 0 else 0.5)
            
            return PredictionResult(
                metric_name=metric_name,
                predicted_value=float(prediction),
                confidence_interval=confidence_interval,
                confidence_score=float(confidence_score),
                timeframe="30 minutes",
                timestamp=datetime.utcnow(),
                features_used=['hour_of_day', 'day_of_week', 'is_weekend', 'other_metrics']
            )
            
        except Exception as e:
            logger.error(f"Error predicting {metric_name}: {e}")
            return None
    
    def _analyze_patterns(self):
        """Анализирует паттерны производительности"""
        try:
            # Анализируем историю прогнозов и реальных значений
            if len(self.prediction_history) < 10:
                return
            
            recent_predictions = list(self.prediction_history)[-50:]
            
            # Ищем повторяющиеся паттерны
            patterns = []
            
            # Паттерн: высокая нагрузка по выходным
            weekend_high_load = self._detect_weekend_pattern(recent_predictions)
            if weekend_high_load:
                patterns.append(weekend_high_load)
            
            # Паттерн: утренний пик нагрузки
            morning_peak = self._detect_morning_peak_pattern(recent_predictions)
            if morning_peak:
                patterns.append(morning_peak)
            
            # Сохраняем найденные паттерны
            for pattern in patterns:
                self.patterns_history.append({
                    'pattern': pattern.__dict__,
                    'timestamp': time.time()
                })
                
                logger.info(f"Performance pattern detected: {pattern.pattern_type} - {pattern.description}")
            
        except Exception as e:
            logger.error(f"Error analyzing patterns: {e}")
    
    def _detect_weekend_pattern(self, predictions) -> Optional[PerformancePattern]:
        """Обнаруживает паттерн выходных"""
        try:
            weekend_predictions = [
                p for p in predictions
                if datetime.fromtimestamp(p['timestamp']).weekday() >= 5
            ]
            
            if len(weekend_predictions) < 5:
                return None
            
            # Анализируем CPU и память по выходным
            weekend_cpu_avg = np.mean([
                p['prediction']['predicted_value']
                for p in weekend_predictions
                if p['prediction']['metric_name'] == 'cpu_percent'
            ])
            
            if weekend_cpu_avg > 70:  # Высокая нагрузка
                return PerformancePattern(
                    pattern_type="weekend_high_load",
                    description="High CPU usage detected on weekends",
                    confidence=0.8,
                    affected_metrics=['cpu_percent', 'response_time'],
                    timestamp=datetime.utcnow()
                )
                
        except Exception:
            pass
        
        return None
    
    def _detect_morning_peak_pattern(self, predictions) -> Optional[PerformancePattern]:
        """Обнаруживает паттерн утреннего пика"""
        try:
            morning_predictions = [
                p for p in predictions
                if 8 <= datetime.fromtimestamp(p['timestamp']).hour <= 10
            ]
            
            if len(morning_predictions) < 5:
                return None
            
            # Анализируем пик запросов по утрам
            morning_requests_avg = np.mean([
                p['prediction']['predicted_value']
                for p in morning_predictions
                if p['prediction']['metric_name'] == 'request_rate'
            ])
            
            if morning_requests_avg > 50:  # Высокий трафик
                return PerformancePattern(
                    pattern_type="morning_peak",
                    description="High request rate detected during morning hours (8-10 AM)",
                    confidence=0.75,
                    affected_metrics=['request_rate', 'response_time'],
                    timestamp=datetime.utcnow()
                )
                
        except Exception:
            pass
        
        return None
    
    def get_predictions(self, limit: int = 10) -> List[Dict]:
        """Получает последние прогнозы"""
        return list(self.prediction_history)[-limit:]
    
    def get_patterns(self, limit: int = 10) -> List[Dict]:
        """Получает обнаруженные паттерны"""
        return list(self.patterns_history)[-limit:]
    
    def get_model_accuracy(self) -> Dict[str, Any]:
        """Получает точность моделей"""
        return self.model_accuracy
    
    def get_feature_importance(self) -> Dict[str, Any]:
        """Получает важность признаков"""
        return self.feature_importance
    
    def save_models(self, directory: str = "models"):
        """Сохраняет обученные модели"""
        try:
            os.makedirs(directory, exist_ok=True)
            
            for model_name, model in self.models.items():
                model_path = os.path.join(directory, f"{model_name}.pkl")
                with open(model_path, 'wb') as f:
                    pickle.dump(model, f)
            
            for scaler_name, scaler in self.scalers.items():
                scaler_path = os.path.join(directory, f"{scaler_name}_scaler.pkl")
                with open(scaler_path, 'wb') as f:
                    pickle.dump(scaler, f)
            
            logger.info(f"Models saved to {directory}")
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self, directory: str = "models"):
        """Загружает сохраненные модели"""
        try:
            if not os.path.exists(directory):
                return
            
            for filename in os.listdir(directory):
                if filename.endswith('.pkl'):
                    file_path = os.path.join(directory, filename)
                    with open(file_path, 'rb') as f:
                        if '_scaler' in filename:
                            scaler_name = filename.replace('_scaler.pkl', '')
                            self.scalers[scaler_name] = pickle.load(f)
                        else:
                            model_name = filename.replace('.pkl', '')
                            self.models[model_name] = pickle.load(f)
            
            logger.info(f"Models loaded from {directory}")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")

# Flask CLI commands
def register_prediction_commands(app):
    """Регистрирует CLI команды для предиктивного анализа"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('prediction-status')
    @with_appcontext
    def show_prediction_status():
        """Показывает статус предиктивного анализа"""
        if hasattr(app, 'performance_predictor'):
            predictor = app.performance_predictor
            click.echo("Performance Prediction Status:")
            click.echo(f"  Training: {'Active' if predictor.is_training else 'Inactive'}")
            click.echo(f"  Models: {len(predictor.models)}")
            click.echo(f"  Training data sets: {len(predictor.training_data)}")
            click.echo(f"  Predictions made: {len(predictor.prediction_history)}")
            click.echo(f"  Patterns detected: {len(predictor.patterns_history)}")
            
            click.echo("\nModel accuracy:")
            for metric, accuracy in predictor.model_accuracy.items():
                click.echo(f"  {metric}: MSE = {accuracy['mse']:.4f}, MAE = {accuracy['mae']:.4f}")
        else:
            click.echo("Performance predictor not initialized")
    
    @app.cli.command('prediction-results')
    @click.option('--limit', default=5, help='Number of predictions to show')
    @with_appcontext
    def show_prediction_results(limit):
        """Показывает последние прогнозы"""
        if hasattr(app, 'performance_predictor'):
            predictions = app.performance_predictor.get_predictions(limit)
            click.echo("Recent Predictions:")
            for pred in predictions:
                prediction = pred['prediction']
                timestamp = datetime.fromtimestamp(pred['timestamp'])
                click.echo(f"  {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
                          f"{prediction['metric_name']}: {prediction['predicted_value']:.2f} "
                          f"(confidence: {prediction['confidence_score']:.2f})")
        else:
            click.echo("Performance predictor not initialized")
    
    @app.cli.command('performance-patterns')
    @click.option('--limit', default=5, help='Number of patterns to show')
    @with_appcontext
    def show_performance_patterns(limit):
        """Показывает обнаруженные паттерны производительности"""
        if hasattr(app, 'performance_predictor'):
            patterns = app.performance_predictor.get_patterns(limit)
            click.echo("Detected Performance Patterns:")
            for pattern_data in patterns:
                pattern = pattern_data['pattern']
                timestamp = datetime.fromtimestamp(pattern_data['timestamp'])
                click.echo(f"  {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
                          f"{pattern['pattern_type']}: {pattern['description']} "
                          f"(confidence: {pattern['confidence']:.2f})")
        else:
            click.echo("Performance predictor not initialized")