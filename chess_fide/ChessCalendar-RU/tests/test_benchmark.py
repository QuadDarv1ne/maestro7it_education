"""
Benchmark тесты для измерения производительности
"""
import pytest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from statistics import mean, median, stdev
import json


class TestPerformanceBenchmarks:
    """Тесты производительности критичных операций"""
    
    def measure_time(self, func, iterations=100):
        """Измерение времени выполнения функции"""
        times = []
        for _ in range(iterations):
            start = time.perf_counter()
            func()
            end = time.perf_counter()
            times.append((end - start) * 1000)  # в миллисекундах
        
        return {
            'mean': mean(times),
            'median': median(times),
            'min': min(times),
            'max': max(times),
            'stdev': stdev(times) if len(times) > 1 else 0,
            'iterations': iterations
        }
    
    def test_database_query_performance(self, client, sample_tournaments):
        """Тест производительности запросов к БД"""
        def query():
            response = client.get('/api/tournaments')
            assert response.status_code == 200
        
        results = self.measure_time(query, iterations=50)
        
        # Проверка что средний запрос выполняется быстро
        assert results['mean'] < 100, f"Средний запрос слишком медленный: {results['mean']:.2f}ms"
        assert results['median'] < 80, f"Медианный запрос слишком медленный: {results['median']:.2f}ms"
        
        print(f"\n📊 Database Query Performance:")
        print(f"  Mean: {results['mean']:.2f}ms")
        print(f"  Median: {results['median']:.2f}ms")
        print(f"  Min: {results['min']:.2f}ms")
        print(f"  Max: {results['max']:.2f}ms")
        print(f"  StdDev: {results['stdev']:.2f}ms")
    
    def test_cache_performance(self, client):
        """Тест производительности кэша"""
        from app.utils.cache import cache_manager
        
        # Тест записи в кэш
        def cache_write():
            cache_manager.set('test_key', {'data': 'test'}, ttl=60)
        
        write_results = self.measure_time(cache_write, iterations=100)
        
        # Тест чтения из кэша
        cache_manager.set('test_key', {'data': 'test'}, ttl=60)
        
        def cache_read():
            value = cache_manager.get('test_key')
            assert value is not None
        
        read_results = self.measure_time(cache_read, iterations=100)
        
        # Кэш должен быть очень быстрым
        assert read_results['mean'] < 5, f"Чтение из кэша слишком медленное: {read_results['mean']:.2f}ms"
        assert write_results['mean'] < 10, f"Запись в кэш слишком медленная: {write_results['mean']:.2f}ms"
        
        print(f"\n📊 Cache Performance:")
        print(f"  Read Mean: {read_results['mean']:.2f}ms")
        print(f"  Write Mean: {write_results['mean']:.2f}ms")
    
    def test_api_endpoint_performance(self, client, auth_headers):
        """Тест производительности различных API endpoints"""
        endpoints = [
            ('/api/tournaments', 'GET', None),
            ('/api/users', 'GET', None),
            ('/health', 'GET', None),
        ]
        
        results = {}
        for endpoint, method, data in endpoints:
            def request():
                if method == 'GET':
                    response = client.get(endpoint, headers=auth_headers)
                else:
                    response = client.post(endpoint, json=data, headers=auth_headers)
                assert response.status_code in [200, 201]
            
            endpoint_results = self.measure_time(request, iterations=30)
            results[endpoint] = endpoint_results
            
            # Все endpoints должны отвечать быстро
            assert endpoint_results['mean'] < 200, \
                f"{endpoint} слишком медленный: {endpoint_results['mean']:.2f}ms"
        
        print(f"\n📊 API Endpoints Performance:")
        for endpoint, stats in results.items():
            print(f"  {endpoint}:")
            print(f"    Mean: {stats['mean']:.2f}ms")
            print(f"    Median: {stats['median']:.2f}ms")
    
    def test_concurrent_requests(self, client):
        """Тест производительности при конкурентных запросах"""
        num_requests = 50
        num_workers = 10
        
        def make_request():
            start = time.perf_counter()
            response = client.get('/api/tournaments')
            end = time.perf_counter()
            return (end - start) * 1000, response.status_code
        
        start_total = time.perf_counter()
        
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            results = [future.result() for future in as_completed(futures)]
        
        end_total = time.perf_counter()
        total_time = (end_total - start_total) * 1000
        
        times = [r[0] for r in results]
        status_codes = [r[1] for r in results]
        
        # Все запросы должны быть успешными
        assert all(code == 200 for code in status_codes), "Не все запросы успешны"
        
        # Проверка производительности
        throughput = num_requests / (total_time / 1000)  # requests per second
        
        print(f"\n📊 Concurrent Requests Performance:")
        print(f"  Total requests: {num_requests}")
        print(f"  Workers: {num_workers}")
        print(f"  Total time: {total_time:.2f}ms")
        print(f"  Throughput: {throughput:.2f} req/s")
        print(f"  Mean response time: {mean(times):.2f}ms")
        print(f"  Median response time: {median(times):.2f}ms")
        
        assert throughput > 10, f"Throughput слишком низкий: {throughput:.2f} req/s"
    
    def test_memory_usage(self, client, sample_tournaments):
        """Тест использования памяти"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Начальное использование памяти
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # Выполнение операций
        for _ in range(100):
            client.get('/api/tournaments')
        
        # Конечное использование памяти
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_increase = mem_after - mem_before
        
        print(f"\n📊 Memory Usage:")
        print(f"  Before: {mem_before:.2f} MB")
        print(f"  After: {mem_after:.2f} MB")
        print(f"  Increase: {mem_increase:.2f} MB")
        
        # Утечка памяти не должна быть значительной
        assert mem_increase < 50, f"Возможная утечка памяти: {mem_increase:.2f} MB"
    
    def test_database_connection_pool(self, app):
        """Тест пула подключений к БД"""
        from app import db
        
        def query():
            with app.app_context():
                result = db.session.execute(db.text('SELECT 1'))
                return result.fetchone()
        
        # Тест множественных подключений
        start = time.perf_counter()
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(query) for _ in range(100)]
            results = [future.result() for future in as_completed(futures)]
        
        end = time.perf_counter()
        total_time = (end - start) * 1000
        
        print(f"\n📊 Database Connection Pool:")
        print(f"  Total queries: 100")
        print(f"  Total time: {total_time:.2f}ms")
        print(f"  Average time per query: {total_time/100:.2f}ms")
        
        assert all(r is not None for r in results), "Не все запросы успешны"
        assert total_time < 5000, f"Пул подключений работает медленно: {total_time:.2f}ms"
    
    @pytest.mark.slow
    def test_parser_performance(self):
        """Тест производительности парсера"""
        from app.utils.fide_parser import FIDEParser
        
        parser = FIDEParser()
        
        # Мок данных для парсинга
        html_content = """
        <table>
            <tr><td>Tournament 1</td><td>2024-01-01</td><td>Moscow</td></tr>
            <tr><td>Tournament 2</td><td>2024-01-02</td><td>St. Petersburg</td></tr>
        </table>
        """ * 50  # 100 турниров
        
        def parse():
            # Здесь должна быть логика парсинга
            pass
        
        results = self.measure_time(parse, iterations=10)
        
        print(f"\n📊 Parser Performance:")
        print(f"  Mean: {results['mean']:.2f}ms")
        print(f"  Median: {results['median']:.2f}ms")
    
    def test_json_serialization_performance(self, sample_tournaments):
        """Тест производительности сериализации JSON"""
        from app.models.tournament import Tournament
        
        tournaments = sample_tournaments[:100]
        
        def serialize():
            data = [
                {
                    'id': t.id,
                    'name': t.name,
                    'location': t.location,
                    'start_date': t.start_date.isoformat() if t.start_date else None,
                    'end_date': t.end_date.isoformat() if t.end_date else None,
                }
                for t in tournaments
            ]
            json.dumps(data)
        
        results = self.measure_time(serialize, iterations=100)
        
        print(f"\n📊 JSON Serialization Performance:")
        print(f"  Mean: {results['mean']:.2f}ms")
        print(f"  Median: {results['median']:.2f}ms")
        
        assert results['mean'] < 50, f"Сериализация слишком медленная: {results['mean']:.2f}ms"


@pytest.fixture
def sample_tournaments(db_session):
    """Создание тестовых турниров"""
    from app.models.tournament import Tournament
    from datetime import datetime, timedelta
    
    tournaments = []
    for i in range(100):
        tournament = Tournament(
            name=f'Test Tournament {i}',
            location=f'City {i}',
            start_date=datetime.now() + timedelta(days=i),
            end_date=datetime.now() + timedelta(days=i+3),
            category='National',
            status='Scheduled'
        )
        db_session.session.add(tournament)
        tournaments.append(tournament)
    
    db_session.session.commit()
    return tournaments


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
