# -*- coding: utf-8 -*-
"""
Продвинутое обнаружение аномалий в системе мониторинга
"""
import logging
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from datetime import datetime, timedelta
from collections import deque
import time
import threading
from dataclasses import dataclass
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)

@dataclass
class AnomalyDetectionResult:
    """Результат обнаружения аномалий"""
    is_anomaly: bool
    anomaly_type: str
    confidence: float
    value: float
    threshold: float
    timestamp: datetime
    details: Dict[str, Any]

@dataclass
class MetricData:
    """Данные метрики"""
    timestamp: datetime
    value: float
    tags: Dict[str, str]

class StatisticalAnomalyDetector:
    """Статистический детектор аномалий"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.data_window = deque(maxlen=window_size)
        self.z_threshold = 3.0  # Порог для Z-score (3 сигмы)
        self.iqr_multiplier = 1.5  # Множитель для межквартильного размаха
    
    def add_data_point(self, value: float, timestamp: datetime = None):
        """Добавляет точку данных"""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        self.data_window.append({
            'value': float(value),
            'timestamp': timestamp
        })
    
    def detect_zscore_anomaly(self, value: float) -> AnomalyDetectionResult:
        """Обнаруживает аномалии по Z-оценке"""
        if len(self.data_window) < 10:
            return AnomalyDetectionResult(
                is_anomaly=False,
                anomaly_type="insufficient_data",
                confidence=0.0,
                value=value,
                threshold=0.0,
                timestamp=datetime.utcnow(),
                details={}
            )
        
        # Рассчитываем статистики
        values = [point['value'] for point in self.data_window]
        mean = np.mean(values)
        std = np.std(values)
        
        if std == 0:
            return AnomalyDetectionResult(
                is_anomaly=False,
                anomaly_type="no_variance",
                confidence=0.0,
                value=value,
                threshold=0.0,
                timestamp=datetime.utcnow(),
                details={}
            )
        
        # Рассчитываем Z-оценку
        z_score = abs((value - mean) / std)
        
        is_anomaly = z_score > self.z_threshold
        confidence = min(z_score / self.z_threshold, 1.0) if is_anomaly else 0.0
        
        return AnomalyDetectionResult(
            is_anomaly=is_anomaly,
            anomaly_type="z_score",
            confidence=confidence,
            value=value,
            threshold=self.z_threshold,
            timestamp=datetime.utcnow(),
            details={
                'mean': float(mean),
                'std': float(std),
                'z_score': float(z_score)
            }
        )
    
    def detect_iqr_anomaly(self, value: float) -> AnomalyDetectionResult:
        """Обнаруживает аномалии по межквартильному размаху"""
        if len(self.data_window) < 10:
            return AnomalyDetectionResult(
                is_anomaly=False,
                anomaly_type="insufficient_data",
                confidence=0.0,
                value=value,
                threshold=0.0,
                timestamp=datetime.utcnow(),
                details={}
            )
        
        values = [point['value'] for point in self.data_window]
        q1 = np.percentile(values, 25)
        q3 = np.percentile(values, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - self.iqr_multiplier * iqr
        upper_bound = q3 + self.iqr_multiplier * iqr
        
        is_anomaly = value < lower_bound or value > upper_bound
        confidence = 0.0
        
        if is_anomaly:
            if value < lower_bound:
                distance = lower_bound - value
                max_distance = abs(np.min(values) - lower_bound)
                confidence = min(distance / max_distance if max_distance > 0 else 0, 1.0)
            else:
                distance = value - upper_bound
                max_distance = abs(np.max(values) - upper_bound)
                confidence = min(distance / max_distance if max_distance > 0 else 0, 1.0)
        
        return AnomalyDetectionResult(
            is_anomaly=is_anomaly,
            anomaly_type="iqr",
            confidence=confidence,
            value=value,
            threshold=self.iqr_multiplier,
            timestamp=datetime.utcnow(),
            details={
                'q1': float(q1),
                'q3': float(q3),
                'iqr': float(iqr),
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound)
            }
        )

class MLAnomalyDetector:
    """Детектор аномалий на основе машинного обучения"""
    
    def __init__(self, window_size: int = 200):
        self.window_size = window_size
        self.data_window = deque(maxlen=window_size)
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_names = []
    
    def add_data_point(self, features: Dict[str, float], timestamp: datetime = None):
        """Добавляет точку данных с признаками"""
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        self.data_window.append({
            'features': features,
            'timestamp': timestamp
        })
        
        # Обучаем модель при достаточном количестве данных
        if len(self.data_window) >= 50 and not self.is_trained:
            self._train_model()
    
    def _train_model(self):
        """Обучает модель изоляции леса"""
        try:
            # Подготавливаем данные
            feature_matrix = []
            self.feature_names = []
            
            # Получаем все уникальные признаки
            all_features = set()
            for point in self.data_window:
                all_features.update(point['features'].keys())
            
            self.feature_names = sorted(list(all_features))
            
            # Создаем матрицу признаков
            for point in self.data_window:
                feature_vector = []
                for feature_name in self.feature_names:
                    feature_vector.append(point['features'].get(feature_name, 0.0))
                feature_matrix.append(feature_vector)
            
            if len(feature_matrix) >= 50:
                feature_matrix = np.array(feature_matrix)
                
                # Нормализуем данные
                scaled_features = self.scaler.fit_transform(feature_matrix)
                
                # Обучаем модель
                self.model.fit(scaled_features)
                self.is_trained = True
                logger.info("ML anomaly detector trained successfully")
            
        except Exception as e:
            logger.error(f"Error training ML anomaly detector: {e}")
    
    def detect_anomaly(self, features: Dict[str, float]) -> AnomalyDetectionResult:
        """Обнаруживает аномалии с использованием ML"""
        if not self.is_trained:
            return AnomalyDetectionResult(
                is_anomaly=False,
                anomaly_type="not_trained",
                confidence=0.0,
                value=0.0,
                threshold=0.0,
                timestamp=datetime.utcnow(),
                details={}
            )
        
        try:
            # Подготавливаем вектор признаков
            feature_vector = []
            for feature_name in self.feature_names:
                feature_vector.append(features.get(feature_name, 0.0))
            
            feature_vector = np.array([feature_vector])
            
            # Нормализуем
            scaled_features = self.scaler.transform(feature_vector)
            
            # Предсказываем
            anomaly_prediction = self.model.predict(scaled_features)[0]
            anomaly_score = self.model.decision_function(scaled_features)[0]
            
            # Рассчитываем доверие
            confidence = abs(anomaly_score)
            # Нормализуем доверие в диапазон 0-1
            confidence = min(confidence / 0.5, 1.0)  # Предполагаем максимальный score 0.5
            
            is_anomaly = anomaly_prediction == -1  # -1 означает аномалию
            
            return AnomalyDetectionResult(
                is_anomaly=is_anomaly,
                anomaly_type="ml_isolation_forest",
                confidence=confidence,
                value=float(anomaly_score),
                threshold=0.0,  # Порог встроен в модель
                timestamp=datetime.utcnow(),
                details={
                    'prediction': int(anomaly_prediction),
                    'score': float(anomaly_score),
                    'feature_names': self.feature_names,
                    'features': features
                }
            )
            
        except Exception as e:
            logger.error(f"Error in ML anomaly detection: {e}")
            return AnomalyDetectionResult(
                is_anomaly=False,
                anomaly_type="error",
                confidence=0.0,
                value=0.0,
                threshold=0.0,
                timestamp=datetime.utcnow(),
                details={'error': str(e)}
            )

class AdvancedAnomalyDetector:
    """Продвинутая система обнаружения аномалий"""
    
    def __init__(self, app=None):
        self.app = app
        self.detectors = {}
        self.anomaly_history = deque(maxlen=1000)
        self.alert_threshold = 0.7  # Порог доверия для алертов
        self.is_monitoring = False
        self.monitoring_thread = None
        
        # Инициализируем детекторы
        self._init_detectors()
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализирует систему обнаружения аномалий"""
        self.app = app
        app.anomaly_detector = self
        self.start_monitoring()
        logger.info("Advanced anomaly detection system initialized")
    
    def _init_detectors(self):
        """Инициализирует различные детекторы"""
        # Статистические детекторы
        self.detectors['cpu_anomaly'] = StatisticalAnomalyDetector(window_size=50)
        self.detectors['memory_anomaly'] = StatisticalAnomalyDetector(window_size=50)
        self.detectors['response_time_anomaly'] = StatisticalAnomalyDetector(window_size=30)
        self.detectors['error_rate_anomaly'] = StatisticalAnomalyDetector(window_size=100)
        
        # ML детектор
        self.detectors['ml_anomaly'] = MLAnomalyDetector(window_size=200)
    
    def start_monitoring(self):
        """Запускает мониторинг аномалий"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            logger.info("Anomaly monitoring started")
    
    def stop_monitoring(self):
        """Останавливает мониторинг"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Anomaly monitoring stopped")
    
    def _monitoring_loop(self):
        """Цикл мониторинга аномалий"""
        while self.is_monitoring:
            try:
                # Собираем метрики
                metrics = self._collect_metrics()
                
                # Обнаруживаем аномалии
                anomalies = self._detect_anomalies(metrics)
                
                # Обрабатываем найденные аномалии
                for anomaly in anomalies:
                    self._handle_anomaly(anomaly)
                
                time.sleep(60)  # Проверяем каждую минуту
                
            except Exception as e:
                logger.error(f"Error in anomaly monitoring: {e}")
                time.sleep(120)  # Ждем дольше при ошибке
    
    def _collect_metrics(self) -> Dict[str, float]:
        """Собирает метрики для анализа"""
        metrics = {}
        
        try:
            # CPU и память
            import psutil
            metrics['cpu_percent'] = psutil.cpu_percent(interval=1)
            metrics['memory_percent'] = psutil.virtual_memory().percent
            
            # Метрики приложения
            if hasattr(self.app, 'performance_monitor'):
                app_metrics = self.app.performance_monitor.get_current_metrics()
                metrics['response_time'] = app_metrics.get('avg_response_time', 0.5)
                metrics['request_rate'] = app_metrics.get('requests_per_second', 10.0)
                metrics['error_rate'] = app_metrics.get('error_rate', 0.0)
            
            # Подсчитываем ошибки из логов
            if hasattr(self.app, 'structured_logger'):
                recent_errors = self.app.structured_logger.get_recent_errors(minutes=5)
                metrics['recent_errors'] = len(recent_errors)
                metrics['error_rate'] = len(recent_errors) / max(metrics.get('request_rate', 1), 1) * 100
            
        except Exception as e:
            logger.error(f"Error collecting metrics for anomaly detection: {e}")
            # Безопасные значения по умолчанию
            metrics.update({
                'cpu_percent': 50.0,
                'memory_percent': 50.0,
                'response_time': 0.5,
                'request_rate': 10.0,
                'error_rate': 0.0,
                'recent_errors': 0
            })
        
        return metrics
    
    def _detect_anomalies(self, metrics: Dict[str, float]) -> List[AnomalyDetectionResult]:
        """Обнаруживает аномалии в метриках"""
        anomalies = []
        current_time = datetime.utcnow()
        
        # Добавляем данные в статистические детекторы
        self.detectors['cpu_anomaly'].add_data_point(metrics['cpu_percent'], current_time)
        self.detectors['memory_anomaly'].add_data_point(metrics['memory_percent'], current_time)
        self.detectors['response_time_anomaly'].add_data_point(metrics['response_time'], current_time)
        self.detectors['error_rate_anomaly'].add_data_point(metrics['error_rate'], current_time)
        
        # Добавляем данные в ML детектор
        ml_features = {
            'cpu': metrics['cpu_percent'],
            'memory': metrics['memory_percent'],
            'response_time': metrics['response_time'],
            'request_rate': metrics['request_rate'],
            'error_rate': metrics['error_rate']
        }
        self.detectors['ml_anomaly'].add_data_point(ml_features, current_time)
        
        # Обнаруживаем аномалии
        cpu_anomaly = self.detectors['cpu_anomaly'].detect_zscore_anomaly(metrics['cpu_percent'])
        if cpu_anomaly.is_anomaly:
            anomalies.append(cpu_anomaly)
        
        memory_anomaly = self.detectors['memory_anomaly'].detect_iqr_anomaly(metrics['memory_percent'])
        if memory_anomaly.is_anomaly:
            anomalies.append(memory_anomaly)
        
        response_anomaly = self.detectors['response_time_anomaly'].detect_zscore_anomaly(metrics['response_time'])
        if response_anomaly.is_anomaly:
            anomalies.append(response_anomaly)
        
        error_anomaly = self.detectors['error_rate_anomaly'].detect_iqr_anomaly(metrics['error_rate'])
        if error_anomaly.is_anomaly:
            anomalies.append(error_anomaly)
        
        # ML аномалии
        ml_anomaly = self.detectors['ml_anomaly'].detect_anomaly(ml_features)
        if ml_anomaly.is_anomaly:
            anomalies.append(ml_anomaly)
        
        return anomalies
    
    def _handle_anomaly(self, anomaly: AnomalyDetectionResult):
        """Обрабатывает обнаруженную аномалию"""
        # Добавляем в историю
        self.anomaly_history.append({
            'anomaly': anomaly.__dict__,
            'timestamp': time.time()
        })
        
        # Отправляем алерт если уверенность высокая
        if anomaly.confidence >= self.alert_threshold:
            self._send_alert(anomaly)
        
        logger.warning(f"Anomaly detected: {anomaly.anomaly_type} - "
                      f"value: {anomaly.value}, confidence: {anomaly.confidence:.2f}")
    
    def _send_alert(self, anomaly: AnomalyDetectionResult):
        """Отправляет алерт об аномалии"""
        alert_message = {
            'type': 'ANOMALY_DETECTED',
            'anomaly_type': anomaly.anomaly_type,
            'value': anomaly.value,
            'confidence': anomaly.confidence,
            'timestamp': anomaly.timestamp.isoformat(),
            'details': anomaly.details
        }
        
        # Здесь можно интегрировать с системами оповещения:
        # - Slack
        # - Email
        # - SMS
        # - Telegram
        # - PagerDuty
        
        logger.critical(f"ANOMALY ALERT: {json.dumps(alert_message, default=str)}")
        
        # Отправляем в систему нотификаций если доступна
        if hasattr(self.app, 'notification_manager'):
            self.app.notification_manager.send_notification(
                title=f"Anomaly Detected: {anomaly.anomaly_type}",
                message=f"Value: {anomaly.value:.2f}, Confidence: {anomaly.confidence:.2f}",
                notification_type="anomaly",
                priority="high"
            )
    
    def get_anomaly_history(self, limit: int = 50) -> List[Dict]:
        """Получает историю аномалий"""
        return list(self.anomaly_history)[-limit:]
    
    def get_detector_stats(self) -> Dict[str, Any]:
        """Получает статистику детекторов"""
        stats = {}
        for name, detector in self.detectors.items():
            if hasattr(detector, 'data_window'):
                stats[name] = {
                    'data_points': len(detector.data_window),
                    'is_trained': getattr(detector, 'is_trained', True)
                }
        return stats
    
    def add_custom_detector(self, name: str, detector):
        """Добавляет пользовательский детектор"""
        self.detectors[name] = detector
        logger.info(f"Added custom anomaly detector: {name}")

# Flask CLI commands
def register_anomaly_detection_commands(app):
    """Регистрирует CLI команды для обнаружения аномалий"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('anomaly-status')
    @with_appcontext
    def show_anomaly_status():
        """Показывает статус системы обнаружения аномалий"""
        if hasattr(app, 'anomaly_detector'):
            detector = app.anomaly_detector
            click.echo("Anomaly Detection Status:")
            click.echo(f"  Monitoring: {'Active' if detector.is_monitoring else 'Inactive'}")
            click.echo(f"  Detectors: {len(detector.detectors)}")
            click.echo(f"  History entries: {len(detector.anomaly_history)}")
            click.echo("\nDetector stats:")
            stats = detector.get_detector_stats()
            for name, stat in stats.items():
                click.echo(f"  {name}: {stat['data_points']} points, trained: {stat['is_trained']}")
        else:
            click.echo("Anomaly detector not initialized")
    
    @app.cli.command('anomaly-history')
    @click.option('--limit', default=10, help='Number of history entries to show')
    @with_appcontext
    def show_anomaly_history(limit):
        """Показывает историю обнаруженных аномалий"""
        if hasattr(app, 'anomaly_detector'):
            history = app.anomaly_detector.get_anomaly_history(limit)
            click.echo("Anomaly History:")
            for entry in history:
                anomaly = entry['anomaly']
                timestamp = datetime.fromtimestamp(entry['timestamp'])
                click.echo(f"  {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
                          f"{anomaly['anomaly_type']}: {anomaly['value']:.2f} "
                          f"(confidence: {anomaly['confidence']:.2f})")
        else:
            click.echo("Anomaly detector not initialized")