"""
Система A/B тестирования для экспериментов с UI/UX
Позволяет тестировать различные варианты функций и интерфейса
"""

import hashlib
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from flask import session, request
from app import db


class ABTest:
    """Класс для управления A/B тестом"""
    
    def __init__(self, name: str, variants: List[str], weights: Optional[List[float]] = None):
        """
        Инициализация A/B теста
        
        Args:
            name: Название теста
            variants: Список вариантов (например, ['control', 'variant_a', 'variant_b'])
            weights: Веса для каждого варианта (сумма должна быть 1.0)
        """
        self.name = name
        self.variants = variants
        self.weights = weights or [1.0 / len(variants)] * len(variants)
        
        if len(self.weights) != len(self.variants):
            raise ValueError("Weights must match variants length")
        if abs(sum(self.weights) - 1.0) > 0.001:
            raise ValueError("Weights must sum to 1.0")
    
    def get_variant(self, user_id: Optional[str] = None) -> str:
        """
        Получить вариант для пользователя
        Использует консистентное хеширование для стабильности
        """
        if user_id is None:
            # Используем session ID или IP адрес
            user_id = session.get('user_id') or request.remote_addr or 'anonymous'
        
        # Консистентное хеширование
        hash_value = int(hashlib.md5(f"{self.name}:{user_id}".encode()).hexdigest(), 16)
        normalized = (hash_value % 10000) / 10000.0
        
        # Выбор варианта на основе весов
        cumulative = 0
        for variant, weight in zip(self.variants, self.weights):
            cumulative += weight
            if normalized <= cumulative:
                return variant
        
        return self.variants[-1]
    
    def track_event(self, user_id: str, variant: str, event: str, value: Optional[float] = None):
        """Отслеживание события в A/B тесте"""
        try:
            from app.models.ab_test_event import ABTestEvent
            
            event_record = ABTestEvent(
                test_name=self.name,
                user_id=user_id,
                variant=variant,
                event=event,
                value=value,
                timestamp=datetime.utcnow()
            )
            db.session.add(event_record)
            db.session.commit()
        except Exception as e:
            # Логируем, но не падаем
            import logging
            logging.error(f"Failed to track A/B test event: {e}")


class ABTestManager:
    """Менеджер для управления всеми A/B тестами"""
    
    def __init__(self):
        self.tests: Dict[str, ABTest] = {}
    
    def register_test(self, test: ABTest):
        """Регистрация нового теста"""
        self.tests[test.name] = test
    
    def get_variant(self, test_name: str, user_id: Optional[str] = None) -> str:
        """Получить вариант для теста"""
        if test_name not in self.tests:
            return 'control'  # Дефолтный вариант
        
        return self.tests[test_name].get_variant(user_id)
    
    def track_event(self, test_name: str, user_id: str, event: str, value: Optional[float] = None):
        """Отслеживание события"""
        if test_name not in self.tests:
            return
        
        variant = self.get_variant(test_name, user_id)
        self.tests[test_name].track_event(user_id, variant, event, value)
    
    def get_results(self, test_name: str, days: int = 7) -> Dict[str, Any]:
        """Получить результаты теста"""
        try:
            from app.models.ab_test_event import ABTestEvent
            from sqlalchemy import func
            
            start_date = datetime.utcnow() - timedelta(days=days)
            
            # Получение статистики по вариантам
            results = db.session.query(
                ABTestEvent.variant,
                ABTestEvent.event,
                func.count(ABTestEvent.id).label('count'),
                func.avg(ABTestEvent.value).label('avg_value')
            ).filter(
                ABTestEvent.test_name == test_name,
                ABTestEvent.timestamp >= start_date
            ).group_by(
                ABTestEvent.variant,
                ABTestEvent.event
            ).all()
            
            # Форматирование результатов
            formatted = {}
            for variant, event, count, avg_value in results:
                if variant not in formatted:
                    formatted[variant] = {}
                formatted[variant][event] = {
                    'count': count,
                    'avg_value': round(avg_value, 2) if avg_value else None
                }
            
            return {
                'test_name': test_name,
                'period_days': days,
                'variants': formatted,
                'timestamp': datetime.utcnow().isoformat()
            }
        except Exception as e:
            import logging
            logging.error(f"Failed to get A/B test results: {e}")
            return {'error': str(e)}
    
    def calculate_significance(self, test_name: str, metric: str = 'conversion') -> Dict[str, Any]:
        """
        Расчет статистической значимости результатов
        Использует z-test для сравнения пропорций
        """
        try:
            from app.models.ab_test_event import ABTestEvent
            from sqlalchemy import func
            import math
            
            # Получение данных для контрольной и тестовой групп
            results = db.session.query(
                ABTestEvent.variant,
                func.count(func.distinct(ABTestEvent.user_id)).label('users'),
                func.count(ABTestEvent.id).label('conversions')
            ).filter(
                ABTestEvent.test_name == test_name,
                ABTestEvent.event == metric
            ).group_by(ABTestEvent.variant).all()
            
            if len(results) < 2:
                return {'error': 'Not enough data for significance test'}
            
            # Предполагаем, что первый вариант - контрольный
            control = results[0]
            variants_data = []
            
            for variant in results[1:]:
                # Расчет конверсии
                p1 = control.conversions / control.users if control.users > 0 else 0
                p2 = variant.conversions / variant.users if variant.users > 0 else 0
                
                # Объединенная пропорция
                p_pool = (control.conversions + variant.conversions) / (control.users + variant.users)
                
                # Стандартная ошибка
                se = math.sqrt(p_pool * (1 - p_pool) * (1/control.users + 1/variant.users))
                
                # Z-score
                z_score = (p2 - p1) / se if se > 0 else 0
                
                # P-value (приблизительно)
                from scipy import stats
                p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
                
                variants_data.append({
                    'variant': variant.variant,
                    'conversion_rate': round(p2 * 100, 2),
                    'control_rate': round(p1 * 100, 2),
                    'lift': round((p2 - p1) / p1 * 100, 2) if p1 > 0 else 0,
                    'z_score': round(z_score, 3),
                    'p_value': round(p_value, 4),
                    'significant': p_value < 0.05
                })
            
            return {
                'test_name': test_name,
                'metric': metric,
                'control_variant': control.variant,
                'variants': variants_data
            }
        except ImportError:
            return {'error': 'scipy not installed, cannot calculate significance'}
        except Exception as e:
            import logging
            logging.error(f"Failed to calculate significance: {e}")
            return {'error': str(e)}


# Глобальный менеджер
ab_test_manager = ABTestManager()

# Регистрация тестов по умолчанию
ab_test_manager.register_test(
    ABTest('homepage_layout', ['control', 'variant_a', 'variant_b'], [0.5, 0.25, 0.25])
)
ab_test_manager.register_test(
    ABTest('tournament_card_design', ['control', 'new_design'], [0.5, 0.5])
)
ab_test_manager.register_test(
    ABTest('search_algorithm', ['default', 'improved'], [0.7, 0.3])
)
