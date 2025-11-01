"""
Модуль: utils/performance_monitor.py

Описание:
    Содержит классы и функции для мониторинга производительности приложения.
"""

import time
import psutil
import threading
from typing import Dict, List, Optional
from collections import defaultdict, deque
import json
import os


class PerformanceMonitor:
    """
    Класс для мониторинга производительности приложения.
    Оптимизирован для минимального влияния на производительность.
    """
    
    def __init__(self, log_file: str = "performance_log.json"):
        """
        Инициализация монитора производительности.
        
        Параметры:
            log_file (str): Путь к файлу лога производительности
        """
        self.log_file = log_file
        self.metrics = defaultdict(list)
        self.start_time = time.time()
        self.monitoring = False
        self.monitor_thread = None
        self.max_log_entries = 1000  # Уменьшаем для лучшей производительности
        self.event_counter = defaultdict(int)  # Счетчик событий
        self.sampling_interval = 2.0  # Увеличиваем интервал сбора метрик для лучшей производительности
        
    def start_monitoring(self, interval: float = 2.0):  # Увеличиваем интервал для лучшей производительности
        """
        Начать мониторинг производительности.
        
        Параметры:
            interval (float): Интервал между измерениями в секундах
        """
        if self.monitoring:
            return
            
        self.sampling_interval = interval
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, args=(interval,), daemon=True)
        self.monitor_thread.start()
        print("✅ Мониторинг производительности запущен")
    
    def stop_monitoring(self):
        """Остановить мониторинг производительности."""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("✅ Мониторинг производительности остановлен")
    
    def _monitor_loop(self, interval: float):
        """Цикл мониторинга в отдельном потоке."""
        while self.monitoring:
            try:
                # Сбор метрик с минимальным влиянием на производительность
                timestamp = time.time()
                cpu_percent = psutil.cpu_percent(interval=0.05)  # Уменьшаем интервал для лучшей отзывчивости
                memory_info = psutil.virtual_memory()
                process = psutil.Process()
                process_memory = process.memory_info().rss / 1024 / 1024  # MB
                
                # Оптимизация: собираем только основные метрики для лучшей производительности
                # Сбор метрик
                self.metrics['timestamp'].append(timestamp)
                self.metrics['cpu_percent'].append(cpu_percent)
                self.metrics['memory_percent'].append(memory_info.percent)
                self.metrics['process_memory_mb'].append(process_memory)
                self.metrics['available_memory_mb'].append(memory_info.available / 1024 / 1024)
                
                # Ограничение размера лога
                self._trim_log()
                
                time.sleep(interval)
            except Exception as e:
                print(f"⚠️  Ошибка при сборе метрик: {e}")
                time.sleep(interval)
    
    def _trim_log(self):
        """Ограничение размера лога для предотвращения утечек памяти."""
        for key in self.metrics:
            if len(self.metrics[key]) > self.max_log_entries:
                # Удаляем старые записи
                self.metrics[key] = self.metrics[key][-self.max_log_entries:]
    
    def log_event(self, event_name: str, duration: Optional[float] = None, 
                  additional_data: Optional[Dict] = None):
        """
        Залогировать событие производительности.
        Оптимизирован для минимального влияния на производительность.
        """
        # Оптимизация: ограничиваем количество логируемых событий для лучшей производительности
        if self.event_counter[event_name] > 1000:  # Ограничиваем количество событий одного типа
            return
            
        try:
            entry = {
                'timestamp': time.time(),
                'event': event_name,
                'duration': duration,
                'additional_data': additional_data or {}
            }
            
            self.metrics['events'].append(entry)
            self.event_counter[event_name] += 1
            self._trim_log()
        except Exception as e:
            # Игнорируем ошибки логирования для лучшей производительности
            pass
    
    def get_performance_summary(self) -> Dict:
        """
        Получить сводку по производительности.
        
        Возвращает:
            dict: Словарь с метриками производительности
        """
        if not self.metrics['cpu_percent']:
            return {}
        
        try:
            # Базовые метрики
            cpu_avg = sum(self.metrics['cpu_percent']) / len(self.metrics['cpu_percent'])
            cpu_max = max(self.metrics['cpu_percent'])
            
            memory_avg = sum(self.metrics['memory_percent']) / len(self.metrics['memory_percent'])
            memory_max = max(self.metrics['memory_percent'])
            
            process_memory_avg = sum(self.metrics['process_memory_mb']) / len(self.metrics['process_memory_mb'])
            process_memory_max = max(self.metrics['process_memory_mb'])
            
            # Дополнительные метрики
            cpu_freq_avg = sum(self.metrics['cpu_frequency_mhz']) / len(self.metrics['cpu_frequency_mhz']) if self.metrics['cpu_frequency_mhz'] else 0
            
            disk_read_total = sum(self.metrics['disk_read_mb']) if self.metrics['disk_read_mb'] else 0
            disk_write_total = sum(self.metrics['disk_write_mb']) if self.metrics['disk_write_mb'] else 0
            
            # Длительность работы
            uptime = time.time() - self.start_time
            
            summary = {
                'uptime_seconds': uptime,
                'cpu_usage': {
                    'average': round(cpu_avg, 2),
                    'maximum': round(cpu_max, 2),
                    'frequency_mhz_avg': round(cpu_freq_avg, 2)
                },
                'memory_usage': {
                    'average_percent': round(memory_avg, 2),
                    'maximum_percent': round(memory_max, 2),
                    'process_memory_mb': {
                        'average': round(process_memory_avg, 2),
                        'maximum': round(process_memory_max, 2)
                    }
                },
                'disk_io': {
                    'total_read_mb': round(disk_read_total, 2),
                    'total_write_mb': round(disk_write_total, 2)
                },
                'total_events': len(self.metrics['events']) if 'events' in self.metrics else 0,
                'event_counts': dict(self.event_counter)
            }
            
            return summary
        except Exception as e:
            print(f"⚠️  Ошибка при создании сводки: {e}")
            return {}
    
    def save_log(self):
        """Сохранить лог производительности в файл."""
        try:
            # Создаем директорию если её нет
            os.makedirs(os.path.dirname(self.log_file) if os.path.dirname(self.log_file) else '.', exist_ok=True)
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(dict(self.metrics), f, ensure_ascii=False, indent=2, default=str)
            print(f"✅ Лог производительности сохранен в {self.log_file}")
        except Exception as e:
            print(f"⚠️  Ошибка при сохранении лога: {e}")
    
    def load_log(self):
        """Загрузить лог производительности из файла."""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    self.metrics = defaultdict(list, json.load(f))
                print(f"✅ Лог производительности загружен из {self.log_file}")
        except Exception as e:
            print(f"⚠️  Ошибка при загрузке лога: {e}")


class PerformanceTimer:
    """
    Контекстный менеджер для измерения времени выполнения кода.
    """
    
    def __init__(self, monitor: PerformanceMonitor, event_name: str):
        """
        Инициализация таймера.
        
        Параметры:
            monitor (PerformanceMonitor): Экземпляр монитора производительности
            event_name (str): Название события
        """
        self.monitor = monitor
        self.event_name = event_name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            self.monitor.log_event(self.event_name, duration)


# Глобальный экземпляр монитора для всего приложения
performance_monitor = PerformanceMonitor()


def get_performance_monitor() -> PerformanceMonitor:
    """
    Получить глобальный экземпляр монитора производительности.
    
    Возвращает:
        PerformanceMonitor: Экземпляр монитора производительности
    """
    return performance_monitor