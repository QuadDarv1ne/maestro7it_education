#!/usr/bin/env python
"""
Нагрузочное тестирование API
Использование: python scripts/load-test.py [options]
"""
import argparse
import time
import statistics
import concurrent.futures
from typing import List, Dict, Any
import requests
from datetime import datetime
import json


class LoadTester:
    """Нагрузочное тестирование"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.results = []
    
    def make_request(
        self,
        method: str,
        endpoint: str,
        headers: Dict = None,
        data: Dict = None
    ) -> Dict[str, Any]:
        """Выполнить запрос и измерить время"""
        url = f"{self.base_url}{endpoint}"
        
        start_time = time.time()
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=self.timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=self.timeout)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data, timeout=self.timeout)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            elapsed = time.time() - start_time
            
            return {
                'success': True,
                'status_code': response.status_code,
                'elapsed': elapsed,
                'size': len(response.content)
            }
        except Exception as e:
            elapsed = time.time() - start_time
            return {
                'success': False,
                'error': str(e),
                'elapsed': elapsed
            }
    
    def run_sequential(
        self,
        method: str,
        endpoint: str,
        num_requests: int,
        headers: Dict = None,
        data: Dict = None
    ) -> List[Dict]:
        """Последовательное выполнение запросов"""
        print(f"Running {num_requests} sequential requests to {endpoint}...")
        
        results = []
        for i in range(num_requests):
            result = self.make_request(method, endpoint, headers, data)
            results.append(result)
            
            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/{num_requests} requests")
        
        return results
    
    def run_concurrent(
        self,
        method: str,
        endpoint: str,
        num_requests: int,
        num_workers: int = 10,
        headers: Dict = None,
        data: Dict = None
    ) -> List[Dict]:
        """Параллельное выполнение запросов"""
        print(f"Running {num_requests} concurrent requests ({num_workers} workers) to {endpoint}...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [
                executor.submit(self.make_request, method, endpoint, headers, data)
                for _ in range(num_requests)
            ]
            
            results = []
            completed = 0
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
                completed += 1
                
                if completed % 10 == 0:
                    print(f"  Completed {completed}/{num_requests} requests")
        
        return results
    
    def analyze_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Анализ результатов"""
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        if not successful:
            return {
                'total_requests': len(results),
                'successful': 0,
                'failed': len(failed),
                'success_rate': 0.0
            }
        
        response_times = [r['elapsed'] for r in successful]
        status_codes = {}
        
        for r in successful:
            code = r['status_code']
            status_codes[code] = status_codes.get(code, 0) + 1
        
        return {
            'total_requests': len(results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': (len(successful) / len(results)) * 100,
            'response_times': {
                'min': min(response_times),
                'max': max(response_times),
                'mean': statistics.mean(response_times),
                'median': statistics.median(response_times),
                'stdev': statistics.stdev(response_times) if len(response_times) > 1 else 0,
                'p95': statistics.quantiles(response_times, n=20)[18] if len(response_times) > 1 else 0,
                'p99': statistics.quantiles(response_times, n=100)[98] if len(response_times) > 1 else 0
            },
            'status_codes': status_codes,
            'errors': [r['error'] for r in failed] if failed else []
        }
    
    def print_report(self, analysis: Dict[str, Any], duration: float):
        """Вывести отчет"""
        print("\n" + "=" * 80)
        print("LOAD TEST REPORT")
        print("=" * 80)
        
        print(f"\nTotal Requests: {analysis['total_requests']}")
        print(f"Successful: {analysis['successful']}")
        print(f"Failed: {analysis['failed']}")
        print(f"Success Rate: {analysis['success_rate']:.2f}%")
        print(f"Total Duration: {duration:.2f}s")
        print(f"Throughput: {analysis['total_requests'] / duration:.2f} req/s")
        
        if analysis['successful'] > 0:
            rt = analysis['response_times']
            print(f"\nResponse Times (seconds):")
            print(f"  Min:    {rt['min']:.3f}s")
            print(f"  Max:    {rt['max']:.3f}s")
            print(f"  Mean:   {rt['mean']:.3f}s")
            print(f"  Median: {rt['median']:.3f}s")
            print(f"  StdDev: {rt['stdev']:.3f}s")
            print(f"  P95:    {rt['p95']:.3f}s")
            print(f"  P99:    {rt['p99']:.3f}s")
            
            print(f"\nStatus Codes:")
            for code, count in sorted(analysis['status_codes'].items()):
                print(f"  {code}: {count}")
        
        if analysis['errors']:
            print(f"\nErrors ({len(analysis['errors'])}):")
            for error in set(analysis['errors'][:10]):
                print(f"  - {error}")
        
        print("\n" + "=" * 80)
    
    def run_scenario(
        self,
        scenario: List[Dict],
        num_iterations: int = 1,
        concurrent: bool = False,
        num_workers: int = 10
    ):
        """
        Выполнить сценарий тестирования
        
        Args:
            scenario: список запросов [{method, endpoint, data}]
            num_iterations: количество итераций
            concurrent: параллельное выполнение
            num_workers: количество workers
        """
        print(f"\nRunning scenario with {len(scenario)} requests, {num_iterations} iterations")
        print(f"Mode: {'Concurrent' if concurrent else 'Sequential'}")
        
        start_time = time.time()
        all_results = []
        
        for iteration in range(num_iterations):
            print(f"\nIteration {iteration + 1}/{num_iterations}")
            
            for step in scenario:
                method = step.get('method', 'GET')
                endpoint = step['endpoint']
                data = step.get('data')
                headers = step.get('headers')
                
                if concurrent:
                    results = self.run_concurrent(
                        method, endpoint, 1, num_workers, headers, data
                    )
                else:
                    results = self.run_sequential(
                        method, endpoint, 1, headers, data
                    )
                
                all_results.extend(results)
        
        duration = time.time() - start_time
        analysis = self.analyze_results(all_results)
        self.print_report(analysis, duration)
        
        return analysis


def main():
    parser = argparse.ArgumentParser(description='Load testing tool')
    parser.add_argument(
        '--url',
        default='http://localhost:5000',
        help='Base URL (default: http://localhost:5000)'
    )
    parser.add_argument(
        '--endpoint',
        default='/api/tournaments',
        help='API endpoint (default: /api/tournaments)'
    )
    parser.add_argument(
        '--method',
        default='GET',
        choices=['GET', 'POST', 'PUT', 'DELETE'],
        help='HTTP method (default: GET)'
    )
    parser.add_argument(
        '--requests',
        type=int,
        default=100,
        help='Number of requests (default: 100)'
    )
    parser.add_argument(
        '--concurrent',
        action='store_true',
        help='Run requests concurrently'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=10,
        help='Number of concurrent workers (default: 10)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Request timeout in seconds (default: 30)'
    )
    parser.add_argument(
        '--scenario',
        help='JSON file with test scenario'
    )
    parser.add_argument(
        '--output',
        help='Output file for results (JSON)'
    )
    
    args = parser.parse_args()
    
    tester = LoadTester(args.url, args.timeout)
    
    print(f"Load Testing Configuration:")
    print(f"  Base URL: {args.url}")
    print(f"  Endpoint: {args.endpoint}")
    print(f"  Method: {args.method}")
    print(f"  Requests: {args.requests}")
    print(f"  Mode: {'Concurrent' if args.concurrent else 'Sequential'}")
    if args.concurrent:
        print(f"  Workers: {args.workers}")
    
    start_time = time.time()
    
    if args.scenario:
        # Загружаем сценарий из файла
        with open(args.scenario, 'r') as f:
            scenario = json.load(f)
        
        analysis = tester.run_scenario(
            scenario,
            num_iterations=1,
            concurrent=args.concurrent,
            num_workers=args.workers
        )
    else:
        # Простой тест одного endpoint
        if args.concurrent:
            results = tester.run_concurrent(
                args.method,
                args.endpoint,
                args.requests,
                args.workers
            )
        else:
            results = tester.run_sequential(
                args.method,
                args.endpoint,
                args.requests
            )
        
        duration = time.time() - start_time
        analysis = tester.analyze_results(results)
        tester.print_report(analysis, duration)
    
    # Сохраняем результаты
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\nResults saved to {args.output}")
    
    # Возвращаем код ошибки если success rate < 95%
    if analysis['success_rate'] < 95:
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
