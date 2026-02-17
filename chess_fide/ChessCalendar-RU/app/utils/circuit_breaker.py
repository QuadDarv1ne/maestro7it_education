"""
Circuit Breaker паттерн для защиты от каскадных сбоев
"""
import time
import logging
from enum import Enum
from typing import Callable, Any, Optional
from functools import wraps
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Состояния Circuit Breaker"""
    CLOSED = "closed"      # Нормальная работа
    OPEN = "open"          # Сбой, запросы блокируются
    HALF_OPEN = "half_open"  # Тестирование восстановления


class CircuitBreakerError(Exception):
    """Исключение при открытом circuit breaker"""
    pass


class CircuitBreaker:
    """
    Circuit Breaker для защиты от каскадных сбоев
    
    Работает по принципу:
    1. CLOSED - все запросы проходят
    2. При превышении порога ошибок -> OPEN
    3. OPEN - все запросы блокируются
    4. После timeout -> HALF_OPEN
    5. HALF_OPEN - пропускаем тестовый запрос
    6. Если успешно -> CLOSED, иначе -> OPEN
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        expected_exception: type = Exception,
        name: Optional[str] = None
    ):
        """
        Args:
            failure_threshold: количество ошибок для открытия
            recovery_timeout: время до попытки восстановления (секунды)
            expected_exception: тип ожидаемого исключения
            name: имя circuit breaker для логирования
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.name = name or "unnamed"
        
        self._failure_count = 0
        self._last_failure_time = None
        self._state = CircuitState.CLOSED
        self._last_state_change = datetime.utcnow()
        
        # Статистика
        self._total_calls = 0
        self._successful_calls = 0
        self._failed_calls = 0
        self._rejected_calls = 0
    
    @property
    def state(self) -> CircuitState:
        """Получить текущее состояние"""
        # Проверяем, не пора ли перейти в HALF_OPEN
        if self._state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._state = CircuitState.HALF_OPEN
                logger.info(f"Circuit breaker '{self.name}' moved to HALF_OPEN state")
        
        return self._state
    
    def _should_attempt_reset(self) -> bool:
        """Проверить, можно ли попытаться восстановиться"""
        if self._last_failure_time is None:
            return False
        
        return time.time() - self._last_failure_time >= self.recovery_timeout
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Выполнить функцию через circuit breaker
        
        Args:
            func: функция для выполнения
            *args, **kwargs: аргументы функции
            
        Returns:
            результат выполнения функции
            
        Raises:
            CircuitBreakerError: если circuit breaker открыт
        """
        self._total_calls += 1
        
        current_state = self.state
        
        if current_state == CircuitState.OPEN:
            self._rejected_calls += 1
            raise CircuitBreakerError(
                f"Circuit breaker '{self.name}' is OPEN. "
                f"Retry after {self.recovery_timeout}s"
            )
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Обработка успешного вызова"""
        self._successful_calls += 1
        
        if self._state == CircuitState.HALF_OPEN:
            # Восстановление успешно
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._last_state_change = datetime.utcnow()
            logger.info(f"Circuit breaker '{self.name}' recovered to CLOSED state")
        
        # Сбрасываем счетчик ошибок при успехе
        if self._state == CircuitState.CLOSED:
            self._failure_count = 0
    
    def _on_failure(self):
        """Обработка неудачного вызова"""
        self._failed_calls += 1
        self._failure_count += 1
        self._last_failure_time = time.time()
        
        if self._state == CircuitState.HALF_OPEN:
            # Восстановление не удалось
            self._state = CircuitState.OPEN
            self._last_state_change = datetime.utcnow()
            logger.warning(f"Circuit breaker '{self.name}' failed recovery, back to OPEN")
        
        elif self._failure_count >= self.failure_threshold:
            # Превышен порог ошибок
            self._state = CircuitState.OPEN
            self._last_state_change = datetime.utcnow()
            logger.error(
                f"Circuit breaker '{self.name}' opened after "
                f"{self._failure_count} failures"
            )
    
    def reset(self):
        """Принудительный сброс circuit breaker"""
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._last_state_change = datetime.utcnow()
        logger.info(f"Circuit breaker '{self.name}' manually reset")
    
    def get_stats(self) -> dict:
        """Получить статистику"""
        uptime = (datetime.utcnow() - self._last_state_change).total_seconds()
        
        success_rate = 0
        if self._total_calls > 0:
            success_rate = (self._successful_calls / self._total_calls) * 100
        
        return {
            'name': self.name,
            'state': self._state.value,
            'failure_count': self._failure_count,
            'failure_threshold': self.failure_threshold,
            'total_calls': self._total_calls,
            'successful_calls': self._successful_calls,
            'failed_calls': self._failed_calls,
            'rejected_calls': self._rejected_calls,
            'success_rate': round(success_rate, 2),
            'uptime_seconds': round(uptime, 2),
            'last_state_change': self._last_state_change.isoformat()
        }


def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: int = 60,
    expected_exception: type = Exception,
    name: Optional[str] = None
):
    """
    Декоратор для применения circuit breaker к функции
    
    Args:
        failure_threshold: количество ошибок для открытия
        recovery_timeout: время до попытки восстановления
        expected_exception: тип ожидаемого исключения
        name: имя circuit breaker
    """
    def decorator(func: Callable) -> Callable:
        breaker_name = name or func.__name__
        breaker = CircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            expected_exception=expected_exception,
            name=breaker_name
        )
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            return breaker.call(func, *args, **kwargs)
        
        # Добавляем методы для управления
        wrapper.circuit_breaker = breaker
        wrapper.reset = breaker.reset
        wrapper.get_stats = breaker.get_stats
        
        return wrapper
    
    return decorator


class CircuitBreakerRegistry:
    """Реестр всех circuit breakers в приложении"""
    
    _instance = None
    _breakers = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def register(self, name: str, breaker: CircuitBreaker):
        """Зарегистрировать circuit breaker"""
        self._breakers[name] = breaker
        logger.info(f"Circuit breaker '{name}' registered")
    
    def get(self, name: str) -> Optional[CircuitBreaker]:
        """Получить circuit breaker по имени"""
        return self._breakers.get(name)
    
    def get_all_stats(self) -> dict:
        """Получить статистику всех circuit breakers"""
        return {
            name: breaker.get_stats()
            for name, breaker in self._breakers.items()
        }
    
    def reset_all(self):
        """Сбросить все circuit breakers"""
        for breaker in self._breakers.values():
            breaker.reset()
        logger.info("All circuit breakers reset")


# Глобальный реестр
registry = CircuitBreakerRegistry()


# Примеры использования для внешних сервисов
@circuit_breaker(
    failure_threshold=3,
    recovery_timeout=30,
    expected_exception=Exception,
    name="fide_parser"
)
def call_fide_api():
    """Пример защищенного вызова FIDE API"""
    pass


@circuit_breaker(
    failure_threshold=5,
    recovery_timeout=60,
    expected_exception=Exception,
    name="email_service"
)
def send_email():
    """Пример защищенной отправки email"""
    pass


class RetryWithCircuitBreaker:
    """
    Комбинация retry и circuit breaker
    Сначала пытаемся повторить, затем открываем circuit
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        name: Optional[str] = None
    ):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=failure_threshold,
            recovery_timeout=recovery_timeout,
            name=name or "retry_breaker"
        )
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Выполнить с retry и circuit breaker"""
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return self.circuit_breaker.call(func, *args, **kwargs)
            except CircuitBreakerError:
                # Circuit открыт, не пытаемся повторить
                raise
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    logger.warning(
                        f"Retry attempt {attempt + 1}/{self.max_retries} "
                        f"for {func.__name__}: {e}"
                    )
        
        # Все попытки исчерпаны
        if last_exception:
            raise last_exception
