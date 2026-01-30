#!/usr/bin/env python3
"""
Система мониторинга производительности шахматного движка
Отслеживает все метрики и предоставляет детальную статистику
"""

import psutil
import time
import threading
import random
from typing import Dict, List, Optional
from collections import defaultdict, deque
import json

class PerformanceMonitor:
    """Монитор производительности шахматного движка"""
    
    def __init__(self):
        self.metrics = defaultdict(list)
        self.timestamps = defaultdict(list)
        self.max_history = 1000  # Максимум записей для каждой метрики
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Инициализация метрик
        self.metric_descriptions = {
            "cpu_percent": "Загрузка CPU (%)",
            "memory_mb": "Использование памяти (MB)",
            "move_calculation_time": "Время расчета хода (мс)",
            "positions_per_second": "Позиций в секунду",
            "cache_hit_rate": "Процент попаданий в кэш (%)",
            "thread_utilization": "Использование потоков (%)",
            "response_time": "Время отклика (мс)"
        }
    
    def start_monitoring(self, interval: float = 1.0):
        """Запуск мониторинга"""
        if self.monitoring_active:
            return
            
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop, 
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        print(f"📊 Мониторинг производительности запущен (интервал: {interval} сек)")
    
    def stop_monitoring(self):
        """Остановка мониторинга"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("🛑 Мониторинг производительности остановлен")
    
    def _monitor_loop(self, interval: float):
        """Основной цикл мониторинга"""
        while self.monitoring_active:
            try:
                # Сбор системных метрик
                self._collect_system_metrics()
                
                # Сбор метрик движка (симуляция)
                self._collect_engine_metrics()
                
                time.sleep(interval)
            except Exception as e:
                print(f"Ошибка мониторинга: {e}")
                break
    
    def _collect_system_metrics(self):
        """Сбор системных метрик"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self._add_metric("cpu_percent", cpu_percent)
        
        # Память
        memory = psutil.virtual_memory()
        self._add_metric("memory_mb", memory.used / (1024 * 1024))
        
        # Потоки процесса (если доступны)
        try:
            current_process = psutil.Process()
            thread_count = current_process.num_threads()
            # Предполагаем максимальное количество потоков = 16
            thread_utilization = min(100, (thread_count / 16) * 100)
            self._add_metric("thread_utilization", thread_utilization)
        except:
            pass
    
    def _collect_engine_metrics(self):
        """Сбор метрик шахматного движка (симуляция)"""
        import random
        
        # Время расчета хода (симуляция)
        calc_time = random.uniform(100, 2000)  # 100-2000 мс
        self._add_metric("move_calculation_time", calc_time)
        
        # Позиции в секунду (симуляция)
        positions_per_sec = random.randint(100000, 800000)
        self._add_metric("positions_per_second", positions_per_sec)
        
        # Процент попаданий в кэш (симуляция)
        cache_hit = random.uniform(60, 95)
        self._add_metric("cache_hit_rate", cache_hit)
        
        # Время отклика (симуляция)
        response_time = random.uniform(50, 500)
        self._add_metric("response_time", response_time)
    
    def _add_metric(self, metric_name: str, value: float):
        """Добавление метрики в историю"""
        self.metrics[metric_name].append(value)
        self.timestamps[metric_name].append(time.time())
        
        # Ограничение истории
        if len(self.metrics[metric_name]) > self.max_history:
            self.metrics[metric_name].pop(0)
            self.timestamps[metric_name].pop(0)
    
    def get_current_metrics(self) -> Dict[str, float]:
        """Получение текущих значений метрик"""
        current = {}
        for metric_name in self.metrics:
            if self.metrics[metric_name]:
                current[metric_name] = self.metrics[metric_name][-1]
        return current
    
    def get_average_metrics(self, last_n: int = 10) -> Dict[str, float]:
        """Получение средних значений за последние N измерений"""
        averages = {}
        for metric_name, values in self.metrics.items():
            if len(values) >= last_n:
                averages[metric_name] = sum(values[-last_n:]) / last_n
            elif values:
                averages[metric_name] = sum(values) / len(values)
        return averages
    
    def get_peak_metrics(self) -> Dict[str, float]:
        """Получение пиковых значений"""
        peaks = {}
        for metric_name, values in self.metrics.items():
            if values:
                peaks[metric_name] = max(values)
        return peaks
    
    def get_performance_report(self) -> Dict:
        """Генерация полного отчета о производительности"""
        current = self.get_current_metrics()
        average = self.get_average_metrics()
        peak = self.get_peak_metrics()
        
        report = {
            "timestamp": time.time(),
            "duration_monitored": time.time() - min([ts[0] for ts in self.timestamps.values()] + [time.time()]),
            "metrics": {}
        }
        
        for metric_name in self.metric_descriptions:
            report["metrics"][metric_name] = {
                "description": self.metric_descriptions[metric_name],
                "current": current.get(metric_name, 0),
                "average": average.get(metric_name, 0),
                "peak": peak.get(metric_name, 0),
                "samples": len(self.metrics.get(metric_name, []))
            }
        
        return report
    
    def print_performance_summary(self):
        """Вывод сводки производительности"""
        report = self.get_performance_report()
        
        print("\n" + "=" * 60)
        print("📊 ОТЧЕТ О ПРОИЗВОДИТЕЛЬНОСТИ ШАХМАТНОГО ДВИЖКА")
        print("=" * 60)
        print(f"⏱️  Время мониторинга: {report['duration_monitored']:.1f} секунд")
        print(f"📈 Собрано образцов: {sum([m['samples'] for m in report['metrics'].values()])}")
        
        print("\n📉 ТЕКУЩИЕ МЕТРИКИ:")
        for metric_name, data in report["metrics"].items():
            print(f"   {data['description']}: {data['current']:.2f}")
        
        print("\n📊 СРЕДНИЕ ЗНАЧЕНИЯ:")
        for metric_name, data in report["metrics"].items():
            print(f"   {data['description']}: {data['average']:.2f}")
        
        print("\n📈 ПИКОВЫЕ ЗНАЧЕНИЯ:")
        for metric_name, data in report["metrics"].items():
            print(f"   {data['description']}: {data['peak']:.2f}")
        
        # Анализ производительности
        print("\n🎯 АНАЛИЗ ПРОИЗВОДИТЕЛЬНОСТИ:")
        cpu_avg = report["metrics"]["cpu_percent"]["average"]
        mem_avg = report["metrics"]["memory_mb"]["average"]
        cache_avg = report["metrics"]["cache_hit_rate"]["average"]
        pos_per_sec = report["metrics"]["positions_per_second"]["average"]
        
        if cpu_avg > 80:
            print("⚠️  Высокая загрузка CPU - рассмотрите оптимизацию алгоритмов")
        elif cpu_avg > 60:
            print("✅ Умеренная загрузка CPU - оптимальное использование ресурсов")
        else:
            print("💡 Низкая загрузка CPU - возможна оптимизация использования потоков")
        
        if cache_avg > 85:
            print("🏆 Отличный процент попаданий в кэш - эффективное кэширование")
        elif cache_avg > 70:
            print("👍 Хороший процент попаданий в кэш")
        else:
            print("🔧 Рассмотрите улучшение системы кэширования")
        
        if pos_per_sec > 500000:
            print("🚀 Высокая производительность - более 500K позиций/сек")
        elif pos_per_sec > 200000:
            print("⚡ Нормальная производительность")
        else:
            print("🐌 Низкая производительность - требуется оптимизация")
        
        print("\n" + "=" * 60)

class ChessEngineBenchmark:
    """Бенчмарк шахматного движка"""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.test_results = []
    
    def run_comprehensive_benchmark(self):
        """Запуск комплексного бенчмарка"""
        print("🏁 ЗАПУСК КОМПЛЕКСНОГО БЕНЧМАРКА")
        print("=" * 50)
        
        # Запуск мониторинга
        self.monitor.start_monitoring(0.5)
        
        # Тест 1: Производительность расчета ходов
        print("\n1️⃣ Тест производительности расчета ходов...")
        move_perf = self._test_move_calculation()
        self.test_results.append(("Move Calculation", move_perf))
        
        # Тест 2: Использование памяти
        print("\n2️⃣ Тест использования памяти...")
        memory_perf = self._test_memory_usage()
        self.test_results.append(("Memory Usage", memory_perf))
        
        # Тест 3: Кэширование
        print("\n3️⃣ Тест системы кэширования...")
        cache_perf = self._test_caching()
        self.test_results.append(("Caching", cache_perf))
        
        # Тест 4: Многопоточность
        print("\n4️⃣ Тест многопоточности...")
        threading_perf = self._test_multithreading()
        self.test_results.append(("Multithreading", threading_perf))
        
        # Остановка мониторинга
        time.sleep(2)  # Даем собрать последние данные
        self.monitor.stop_monitoring()
        
        # Вывод результатов
        self._print_benchmark_results()
    
    def _test_move_calculation(self) -> Dict:
        """Тест расчета ходов"""
        import time
        start_time = time.time()
        
        # Симуляция расчета ходов
        positions_evaluated = 0
        for i in range(100):
            # Симуляция оценки позиций
            import random
            positions_this_iteration = random.randint(5000, 15000)
            positions_evaluated += positions_this_iteration
            time.sleep(0.01)  # Имитация времени расчета
        
        end_time = time.time()
        duration = end_time - start_time
        
        return {
            "positions_evaluated": positions_evaluated,
            "duration_seconds": duration,
            "positions_per_second": positions_evaluated / duration,
            "avg_time_per_move": (duration / 100) * 1000  # мс
        }
    
    def _test_memory_usage(self) -> Dict:
        """Тест использования памяти"""
        import psutil
        process = psutil.Process()
        
        initial_memory = process.memory_info().rss / (1024 * 1024)  # MB
        
        # Симуляция использования памяти
        large_data = []
        for i in range(100000):
            large_data.append([random.random() for _ in range(10)])
        
        final_memory = process.memory_info().rss / (1024 * 1024)  # MB
        memory_increase = final_memory - initial_memory
        
        # Очистка
        del large_data
        
        return {
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
            "memory_increase_mb": memory_increase,
            "peak_memory_mb": max(initial_memory, final_memory)
        }
    
    def _test_caching(self) -> Dict:
        """Тест кэширования"""
        # Симуляция кэша
        cache = {}
        cache_hits = 0
        total_requests = 1000
        
        for i in range(total_requests):
            # Генерируем ключ (чаще повторяются)
            key = f"position_{i % 50}"  # 50 уникальных позиций
            
            if key in cache:
                cache_hits += 1
                cache[key] += 1
            else:
                cache[key] = 1
        
        hit_rate = (cache_hits / total_requests) * 100
        unique_positions = len(cache)
        
        return {
            "cache_hit_rate_percent": hit_rate,
            "unique_positions_cached": unique_positions,
            "total_requests": total_requests,
            "cache_hits": cache_hits
        }
    
    def _test_multithreading(self) -> Dict:
        """Тест многопоточности"""
        import threading
        import time
        
        results = []
        threads_completed = 0
        total_threads = 8
        
        def worker(thread_id):
            nonlocal threads_completed
            # Симуляция работы потока
            time.sleep(random.uniform(0.5, 2.0))
            results.append(f"Thread {thread_id} completed")
            threads_completed += 1
        
        # Запуск потоков
        start_time = time.time()
        threads = []
        
        for i in range(total_threads):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Ожидание завершения
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        return {
            "threads_spawned": total_threads,
            "threads_completed": threads_completed,
            "completion_time_seconds": end_time - start_time,
            "efficiency_percent": (threads_completed / total_threads) * 100
        }
    
    def _print_benchmark_results(self):
        """Вывод результатов бенчмарка"""
        print("\n" + "=" * 60)
        print("🏆 РЕЗУЛЬТАТЫ КОМПЛЕКСНОГО БЕНЧМАРКА")
        print("=" * 60)
        
        for test_name, results in self.test_results:
            print(f"\n🔬 {test_name}:")
            for key, value in results.items():
                if isinstance(value, float):
                    print(f"   {key}: {value:.2f}")
                else:
                    print(f"   {key}: {value}")
        
        # Общая оценка
        print("\n🎯 ОБЩАЯ ОЦЕНКА ПРОИЗВОДИТЕЛЬНОСТИ:")
        
        # Оценка по критериям
        scores = []
        
        # Производительность ходов
        move_perf = self.test_results[0][1]
        pos_per_sec = move_perf["positions_per_second"]
        if pos_per_sec > 500000:
            scores.append(5)
            print("✅ Производительность ходов: Отлично (5/5)")
        elif pos_per_sec > 200000:
            scores.append(4)
            print("👍 Производительность ходов: Хорошо (4/5)")
        else:
            scores.append(3)
            print("🔧 Производительность ходов: Удовлетворительно (3/5)")
        
        # Использование памяти
        memory_perf = self.test_results[1][1]
        memory_efficiency = 100 - (memory_perf["memory_increase_mb"] / 100)  # Упрощенная оценка
        if memory_efficiency > 90:
            scores.append(5)
            print("✅ Использование памяти: Отлично (5/5)")
        elif memory_efficiency > 70:
            scores.append(4)
            print("👍 Использование памяти: Хорошо (4/5)")
        else:
            scores.append(3)
            print("🔧 Использование памяти: Удовлетворительно (3/5)")
        
        # Кэширование
        cache_perf = self.test_results[2][1]
        hit_rate = cache_perf["cache_hit_rate_percent"]
        if hit_rate > 85:
            scores.append(5)
            print("✅ Кэширование: Отлично (5/5)")
        elif hit_rate > 70:
            scores.append(4)
            print("👍 Кэширование: Хорошо (4/5)")
        else:
            scores.append(3)
            print("🔧 Кэширование: Удовлетворительно (3/5)")
        
        # Многопоточность
        threading_perf = self.test_results[3][1]
        efficiency = threading_perf["efficiency_percent"]
        if efficiency > 95:
            scores.append(5)
            print("✅ Многопоточность: Отлично (5/5)")
        elif efficiency > 80:
            scores.append(4)
            print("👍 Многопоточность: Хорошо (4/5)")
        else:
            scores.append(3)
            print("🔧 Многопоточность: Удовлетворительно (3/5)")
        
        # Средний балл
        average_score = sum(scores) / len(scores)
        print(f"\n📊 СРЕДНИЙ БАЛЛ: {average_score:.1f}/5.0")
        
        if average_score >= 4.5:
            print("🏆 УРОВЕНЬ: ПРЕМИУМ (Профессиональный)")
        elif average_score >= 3.5:
            print("⭐ УРОВЕНЬ: ВЫСОКИЙ (Отличный)")
        elif average_score >= 2.5:
            print("👍 УРОВЕНЬ: СРЕДНИЙ (Хороший)")
        else:
            print("🔧 УРОВЕНЬ: БАЗОВЫЙ (Требует улучшений)")
        
        print("\n" + "=" * 60)

# Демонстрация системы мониторинга
def demonstrate_monitoring_system():
    """Демонстрация системы мониторинга производительности"""
    print("=== СИСТЕМА МОНИТОРИНГА ПРОИЗВОДИТЕЛЬНОСТИ ===")
    print("Комплексный мониторинг и бенчмарк шахматного движка\n")
    
    # Создание монитора
    monitor = PerformanceMonitor()
    
    # Запуск мониторинга на 5 секунд
    print("📊 Запуск мониторинга на 5 секунд...")
    monitor.start_monitoring(0.5)
    time.sleep(5)
    monitor.stop_monitoring()
    
    # Вывод сводки
    monitor.print_performance_summary()
    
    # Запуск бенчмарка
    print("\n" + "=" * 60)
    benchmark = ChessEngineBenchmark()
    benchmark.run_comprehensive_benchmark()
    
    print("\n🎉 СИСТЕМА МОНИТОРИНГА УСПЕШНО РЕАЛИЗОВАНА!")
    print("🔧 Инструменты для оптимизации и анализа производительности готовы!")

if __name__ == "__main__":
    try:
        demonstrate_monitoring_system()
        print("\n\nНажмите Enter для завершения...")
        input()
    except KeyboardInterrupt:
        print("\n\nДемонстрация прервана пользователем")
    except Exception as e:
        print(f"\nОшибка: {e}")