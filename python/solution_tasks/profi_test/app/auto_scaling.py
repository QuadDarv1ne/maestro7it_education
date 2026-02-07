# -*- coding: utf-8 -*-
"""
Система автоматического масштабирования на основе метрик производительности
"""
import logging
from typing import Dict, Any, List, Optional
import time
import threading
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
import psutil
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class ScalingAction(Enum):
    """Типы действий масштабирования"""
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"
    NO_ACTION = "no_action"

class ResourceType(Enum):
    """Типы ресурсов для масштабирования"""
    CPU = "cpu"
    MEMORY = "memory"
    DATABASE_CONNECTIONS = "db_connections"
    REQUEST_RATE = "request_rate"
    RESPONSE_TIME = "response_time"

@dataclass
class ScalingRule:
    """Правило масштабирования"""
    resource_type: ResourceType
    threshold_min: float
    threshold_max: float
    scale_factor: float
    cooldown_period: int  # seconds
    enabled: bool = True

@dataclass
class ScalingDecision:
    """Решение о масштабировании"""
    action: ScalingAction
    resource_type: ResourceType
    current_value: float
    threshold: float
    timestamp: datetime
    reason: str

class AutoScaler:
    """Система автоматического масштабирования"""
    
    def __init__(self, app=None):
        self.app = app
        self.is_monitoring = False
        self.monitoring_thread = None
        self.scaling_rules = {}
        self.scaling_history = deque(maxlen=1000)
        self.cooldown_timers = {}
        self.metrics_buffer = defaultdict(lambda: deque(maxlen=100))
        self.scaling_stats = defaultdict(int)
        
        # Default scaling rules
        self._setup_default_rules()
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализирует систему автоматического масштабирования"""
        self.app = app
        app.auto_scaler = self
        self.start_monitoring()
        logger.info("Auto-scaling system initialized")
    
    def _setup_default_rules(self):
        """Устанавливает правила масштабирования по умолчанию"""
        self.scaling_rules = {
            ResourceType.CPU: ScalingRule(
                resource_type=ResourceType.CPU,
                threshold_min=20.0,    # Минимальный порог CPU
                threshold_max=70.0,    # Максимальный порог CPU
                scale_factor=1.5,      # Фактор масштабирования
                cooldown_period=300    # 5 минут cooldown
            ),
            ResourceType.MEMORY: ScalingRule(
                resource_type=ResourceType.MEMORY,
                threshold_min=30.0,    # Минимальный порог памяти
                threshold_max=80.0,    # Максимальный порог памяти
                scale_factor=1.3,
                cooldown_period=600    # 10 минут cooldown
            ),
            ResourceType.REQUEST_RATE: ScalingRule(
                resource_type=ResourceType.REQUEST_RATE,
                threshold_min=10.0,    # Минимальные запросы в секунду
                threshold_max=100.0,   # Максимальные запросы в секунду
                scale_factor=2.0,
                cooldown_period=120    # 2 минуты cooldown
            ),
            ResourceType.RESPONSE_TIME: ScalingRule(
                resource_type=ResourceType.RESPONSE_TIME,
                threshold_min=0.1,     # Минимальное время отклика (сек)
                threshold_max=1.0,     # Максимальное время отклика (сек)
                scale_factor=1.4,
                cooldown_period=180    # 3 минуты cooldown
            )
        }
    
    def start_monitoring(self):
        """Запускает фоновый мониторинг метрик"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitoring_thread.start()
            logger.info("Auto-scaling monitoring started")
    
    def stop_monitoring(self):
        """Останавливает мониторинг"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Auto-scaling monitoring stopped")
    
    def _monitoring_loop(self):
        """Цикл фонового мониторинга"""
        while self.is_monitoring:
            try:
                # Собираем метрики
                metrics = self._collect_metrics()
                
                # Сохраняем метрики в буфер
                for metric_name, value in metrics.items():
                    self.metrics_buffer[metric_name].append({
                        'value': value,
                        'timestamp': time.time()
                    })
                
                # Принимаем решения о масштабировании
                decision = self._make_scaling_decision(metrics)
                if decision.action != ScalingAction.NO_ACTION:
                    self._execute_scaling_decision(decision)
                
                # Обновляем таймеры cooldown
                self._update_cooldown_timers()
                
                time.sleep(30)  # Проверяем каждые 30 секунд
                
            except Exception as e:
                logger.error(f"Error in auto-scaling monitoring: {e}")
                time.sleep(60)  # Ждем дольше при ошибке
    
    def _collect_metrics(self) -> Dict[str, float]:
        """Собирает системные метрики"""
        metrics = {}
        
        try:
            # CPU metrics
            metrics['cpu_percent'] = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            metrics['memory_percent'] = memory.percent
            metrics['memory_available_mb'] = memory.available / (1024 * 1024)
            
            # Process metrics
            current_process = psutil.Process()
            metrics['process_cpu_percent'] = current_process.cpu_percent()
            metrics['process_memory_mb'] = current_process.memory_info().rss / (1024 * 1024)
            
            # Request rate (если доступно)
            if hasattr(self.app, 'request_counter'):
                metrics['request_rate'] = self.app.request_counter.get_requests_per_second()
            else:
                metrics['request_rate'] = 0.0
            
            # Response time (если доступно)
            if hasattr(self.app, 'performance_monitor'):
                recent_metrics = self.app.performance_monitor.get_current_metrics()
                metrics['response_time'] = recent_metrics.get('avg_response_time', 0.5)
            else:
                metrics['response_time'] = 0.5
            
            # Database connections
            if hasattr(self.app, 'db_engine'):
                pool = self.app.db_engine.pool
                if hasattr(pool, 'checkedout'):
                    metrics['db_connections_used'] = pool.checkedout()
                    metrics['db_connections_total'] = pool.size() if hasattr(pool, 'size') else 10
                else:
                    metrics['db_connections_used'] = 0
                    metrics['db_connections_total'] = 10
            else:
                metrics['db_connections_used'] = 0
                metrics['db_connections_total'] = 10
            
        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")
            # Возвращаем безопасные значения по умолчанию
            metrics.update({
                'cpu_percent': 50.0,
                'memory_percent': 50.0,
                'process_cpu_percent': 10.0,
                'process_memory_mb': 100.0,
                'request_rate': 20.0,
                'response_time': 0.5,
                'db_connections_used': 5,
                'db_connections_total': 10
            })
        
        return metrics
    
    def _make_scaling_decision(self, metrics: Dict[str, float]) -> ScalingDecision:
        """Принимает решение о масштабировании на основе метрик"""
        current_time = time.time()
        
        for resource_type, rule in self.scaling_rules.items():
            if not rule.enabled:
                continue
            
            # Проверяем cooldown
            if self._is_in_cooldown(resource_type, current_time):
                continue
            
            # Получаем текущее значение метрики
            metric_value = self._get_metric_value(resource_type, metrics)
            if metric_value is None:
                continue
            
            # Принимаем решение
            if metric_value > rule.threshold_max:
                # Нужно масштабироваться вверх
                return ScalingDecision(
                    action=ScalingAction.SCALE_UP,
                    resource_type=resource_type,
                    current_value=metric_value,
                    threshold=rule.threshold_max,
                    timestamp=datetime.utcnow(),
                    reason=f"{resource_type.value} above threshold {rule.threshold_max}%"
                )
            elif metric_value < rule.threshold_min:
                # Нужно масштабироваться вниз
                return ScalingDecision(
                    action=ScalingAction.SCALE_DOWN,
                    resource_type=resource_type,
                    current_value=metric_value,
                    threshold=rule.threshold_min,
                    timestamp=datetime.utcnow(),
                    reason=f"{resource_type.value} below threshold {rule.threshold_min}%"
                )
        
        # Нет необходимости в масштабировании
        return ScalingDecision(
            action=ScalingAction.NO_ACTION,
            resource_type=ResourceType.CPU,
            current_value=0,
            threshold=0,
            timestamp=datetime.utcnow(),
            reason="No scaling needed"
        )
    
    def _get_metric_value(self, resource_type: ResourceType, metrics: Dict[str, float]) -> Optional[float]:
        """Получает значение метрики для типа ресурса"""
        metric_mapping = {
            ResourceType.CPU: 'cpu_percent',
            ResourceType.MEMORY: 'memory_percent',
            ResourceType.REQUEST_RATE: 'request_rate',
            ResourceType.RESPONSE_TIME: 'response_time'
        }
        
        if resource_type in metric_mapping:
            return metrics.get(metric_mapping[resource_type])
        elif resource_type == ResourceType.DATABASE_CONNECTIONS:
            if 'db_connections_total' > 0:
                return (metrics.get('db_connections_used', 0) / metrics.get('db_connections_total', 1)) * 100
            return 0
        return None
    
    def _is_in_cooldown(self, resource_type: ResourceType, current_time: float) -> bool:
        """Проверяет, находится ли ресурс в режиме cooldown"""
        if resource_type in self.cooldown_timers:
            return current_time < self.cooldown_timers[resource_type]
        return False
    
    def _update_cooldown_timers(self):
        """Обновляет таймеры cooldown"""
        current_time = time.time()
        expired_timers = []
        
        for resource_type, cooldown_end in self.cooldown_timers.items():
            if current_time >= cooldown_end:
                expired_timers.append(resource_type)
        
        # Удаляем истекшие таймеры
        for resource_type in expired_timers:
            del self.cooldown_timers[resource_type]
    
    def _execute_scaling_decision(self, decision: ScalingDecision):
        """Выполняет решение о масштабировании"""
        try:
            # Запускаем cooldown
            rule = self.scaling_rules[decision.resource_type]
            self.cooldown_timers[decision.resource_type] = time.time() + rule.cooldown_period
            
            # Логируем решение
            logger.info(f"Scaling decision: {decision.action.value} for {decision.resource_type.value} "
                       f"(value: {decision.current_value:.2f}, threshold: {decision.threshold:.2f})")
            
            # Выполняем действия масштабирования
            if decision.action == ScalingAction.SCALE_UP:
                self._scale_up(decision.resource_type, rule.scale_factor)
            elif decision.action == ScalingAction.SCALE_DOWN:
                self._scale_down(decision.resource_type, rule.scale_factor)
            
            # Сохраняем в историю
            self.scaling_history.append({
                'decision': decision.__dict__,
                'timestamp': time.time()
            })
            
            self.scaling_stats[f'{decision.action.value}_{decision.resource_type.value}'] += 1
            
        except Exception as e:
            logger.error(f"Error executing scaling decision: {e}")
    
    def _scale_up(self, resource_type: ResourceType, factor: float):
        """Масштабирование вверх"""
        logger.info(f"Scaling UP {resource_type.value} by factor {factor}")
        
        # Для демонстрации - в реальной системе здесь будет:
        # - Добавление worker процессов
        # - Увеличение размера пула соединений
        # - Выделение дополнительных ресурсов
        # - Обновление конфигурации load balancer
        
        if hasattr(self.app, 'connection_pool'):
            current_size = getattr(self.app.connection_pool, 'pool_size', 10)
            new_size = int(current_size * factor)
            logger.info(f"Would increase connection pool from {current_size} to {new_size}")
        
        # Здесь можно добавить интеграцию с облачными провайдерами
        # AWS Auto Scaling, Google Cloud Autoscaler, etc.
    
    def _scale_down(self, resource_type: ResourceType, factor: float):
        """Масштабирование вниз"""
        logger.info(f"Scaling DOWN {resource_type.value} by factor {factor}")
        
        # Для демонстрации - в реальной системе здесь будет:
        # - Уменьшение worker процессов
        # - Снижение размера пула соединений
        # - Освобождение ресурсов
        
        if hasattr(self.app, 'connection_pool'):
            current_size = getattr(self.app.connection_pool, 'pool_size', 10)
            new_size = max(1, int(current_size / factor))
            logger.info(f"Would decrease connection pool from {current_size} to {new_size}")
    
    def add_scaling_rule(self, resource_type: ResourceType, rule: ScalingRule):
        """Добавляет новое правило масштабирования"""
        self.scaling_rules[resource_type] = rule
        logger.info(f"Added scaling rule for {resource_type.value}")
    
    def remove_scaling_rule(self, resource_type: ResourceType):
        """Удаляет правило масштабирования"""
        if resource_type in self.scaling_rules:
            del self.scaling_rules[resource_type]
            logger.info(f"Removed scaling rule for {resource_type.value}")
    
    def get_scaling_history(self, limit: int = 50) -> List[Dict]:
        """Получает историю масштабирования"""
        return list(self.scaling_history)[-limit:]
    
    def get_scaling_stats(self) -> Dict[str, Any]:
        """Получает статистику масштабирования"""
        return dict(self.scaling_stats)
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Получает текущие метрики"""
        return self._collect_metrics()
    
    def get_scaling_rules(self) -> Dict[str, Dict]:
        """Получает текущие правила масштабирования"""
        return {
            resource_type.value: {
                'threshold_min': rule.threshold_min,
                'threshold_max': rule.threshold_max,
                'scale_factor': rule.scale_factor,
                'cooldown_period': rule.cooldown_period,
                'enabled': rule.enabled
            }
            for resource_type, rule in self.scaling_rules.items()
        }

# Global instance
auto_scaler = AutoScaler()

# Flask CLI commands
def register_auto_scaling_commands(app):
    """Регистрирует CLI команды для автоматического масштабирования"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('scaling-status')
    @with_appcontext
    def show_scaling_status():
        """Показывает статус автоматического масштабирования"""
        if hasattr(app, 'auto_scaler'):
            scaler = app.auto_scaler
            click.echo("Auto-scaling Status:")
            click.echo(f"  Monitoring: {'Active' if scaler.is_monitoring else 'Inactive'}")
            click.echo(f"  Rules: {len(scaler.scaling_rules)}")
            click.echo(f"  History entries: {len(scaler.scaling_history)}")
            click.echo("\nCurrent metrics:")
            metrics = scaler.get_current_metrics()
            for key, value in metrics.items():
                click.echo(f"  {key}: {value}")
        else:
            click.echo("Auto-scaler not initialized")
    
    @app.cli.command('scaling-history')
    @click.option('--limit', default=10, help='Number of history entries to show')
    @with_appcontext
    def show_scaling_history(limit):
        """Показывает историю масштабирования"""
        if hasattr(app, 'auto_scaler'):
            history = app.auto_scaler.get_scaling_history(limit)
            click.echo("Scaling History:")
            for entry in history:
                decision = entry['decision']
                timestamp = datetime.fromtimestamp(entry['timestamp'])
                click.echo(f"  {timestamp.strftime('%Y-%m-%d %H:%M:%S')} - "
                          f"{decision['action']} {decision['resource_type']}: "
                          f"{decision['reason']}")
        else:
            click.echo("Auto-scaler not initialized")
    
    @app.cli.command('scaling-stats')
    @with_appcontext
    def show_scaling_stats():
        """Показывает статистику масштабирования"""
        if hasattr(app, 'auto_scaler'):
            stats = app.auto_scaler.get_scaling_stats()
            click.echo("Scaling Statistics:")
            for key, value in stats.items():
                click.echo(f"  {key}: {value}")
        else:
            click.echo("Auto-scaler not initialized")