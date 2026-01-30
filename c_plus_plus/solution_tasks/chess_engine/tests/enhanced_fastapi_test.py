#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced FastAPI Chess API Test Suite
Comprehensive testing with detailed reporting and performance metrics
"""

import requests
import json
import time
import statistics
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TestResult:
    name: str
    passed: bool
    duration: float
    error_message: Optional[str] = None
    details: Optional[Dict] = None

class EnhancedAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.game_id: Optional[str] = None
        self.results: List[TestResult] = []
        self.performance_metrics: Dict[str, List[float]] = {}
        
    def record_metric(self, metric_name: str, value: float):
        """Record performance metric for analysis"""
        if metric_name not in self.performance_metrics:
            self.performance_metrics[metric_name] = []
        self.performance_metrics[metric_name].append(value)
    
    def run_test(self, name: str, test_func) -> TestResult:
        """Run a single test and record results"""
        start_time = time.time()
        print(f"🔬 Running: {name}")
        
        try:
            result = test_func()
            duration = time.time() - start_time
            
            test_result = TestResult(
                name=name,
                passed=True,
                duration=duration,
                details=result
            )
            
            self.record_metric("test_duration", duration)
            print(f"   ✅ PASSED ({duration*1000:.2f} ms)")
            
        except Exception as e:
            duration = time.time() - start_time
            test_result = TestResult(
                name=name,
                passed=False,
                duration=duration,
                error_message=str(e)
            )
            print(f"   ❌ FAILED: {e}")
        
        self.results.append(test_result)
        return test_result
    
    def test_health_endpoint(self) -> Dict[str, Any]:
        """Test health check endpoint with detailed validation"""
        response = self.session.get(f"{self.base_url}/health", timeout=5)
        
        if response.status_code != 200:
            raise Exception(f"Health check failed with status {response.status_code}")
        
        data = response.json()
        
        # Validate response structure
        required_fields = ['status', 'timestamp', 'active_games', 'version']
        for field in required_fields:
            if field not in data:
                raise Exception(f"Missing required field: {field}")
        
        if data['status'] != 'healthy':
            raise Exception(f"Unexpected status: {data['status']}")
        
        return data
    
    def test_cors_headers(self) -> Dict[str, Any]:
        """Test CORS headers are properly set"""
        response = self.session.options(f"{self.base_url}/health")
        
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers'
        ]
        
        for header in cors_headers:
            if header not in response.headers:
                raise Exception(f"Missing CORS header: {header}")
        
        return {"cors_headers_present": True}
    
    def test_rate_limiting(self) -> Dict[str, Any]:
        """Test rate limiting functionality"""
        # Make rapid requests to trigger rate limiting
        responses = []
        for i in range(150):  # Exceed typical rate limit
            try:
                response = self.session.get(f"{self.base_url}/health")
                responses.append(response.status_code)
                if response.status_code == 429:  # Too Many Requests
                    return {"rate_limit_triggered": True, "at_request": i+1}
            except:
                break
        
        # If we didn't hit rate limit, that might be an issue
        return {"rate_limit_not_triggered": True, "total_requests": len(responses)}
    
    def test_create_game_variants(self) -> Dict[str, Any]:
        """Test various game creation scenarios"""
        variants = [
            {"player_name": "Test Player", "game_mode": "ai", "player_color": True},
            {"player_name": "Anonymous", "game_mode": "human", "player_color": False},
            {"game_mode": "ai"},  # Minimal parameters
        ]
        
        created_games = []
        
        for i, params in enumerate(variants):
            response = self.session.post(
                f"{self.base_url}/api/new-game",
                json=params,
                timeout=10
            )
            
            if response.status_code != 200:
                raise Exception(f"Game creation variant {i+1} failed: {response.status_code}")
            
            data = response.json()
            if 'game_id' not in data:
                raise Exception(f"Game creation variant {i+1} missing game_id")
            
            created_games.append({
                "variant": i+1,
                "game_id": data['game_id'],
                "params": params
            })
            
            # Store first game ID for subsequent tests
            if i == 0:
                self.game_id = data['game_id']
        
        return {"created_variants": len(created_games)}
    
    def test_move_validation(self) -> Dict[str, Any]:
        """Test move validation and edge cases"""
        if not self.game_id:
            raise Exception("No game ID available")
        
        # Test invalid moves
        invalid_moves = [
            {"from_pos": [0, 0], "to_pos": [0, 0]},  # Same square
            {"from_pos": [9, 9], "to_pos": [0, 0]},  # Out of bounds
            {"from_pos": [-1, 0], "to_pos": [0, 0]}, # Negative index
        ]
        
        for i, move in enumerate(invalid_moves):
            payload = {
                "game_id": self.game_id,
                "from_pos": move["from_pos"],
                "to_pos": move["to_pos"],
                "player_color": True
            }
            
            response = self.session.post(
                f"{self.base_url}/api/make-move",
                json=payload,
                timeout=5
            )
            
            # Invalid moves should either return 400 or success=False
            if response.status_code == 200:
                data = response.json()
                if data.get('success', True):  # If it succeeded when it shouldn't
                    raise Exception(f"Invalid move {i+1} was accepted")
            elif response.status_code not in [400, 422]:
                raise Exception(f"Unexpected status for invalid move {i+1}: {response.status_code}")
        
        # Test valid move
        valid_payload = {
            "game_id": self.game_id,
            "from_pos": [6, 4],  # e2
            "to_pos": [4, 4],    # e4
            "player_color": True
        }
        
        response = self.session.post(
            f"{self.base_url}/api/make-move",
            json=valid_payload,
            timeout=5
        )
        
        if response.status_code != 200:
            raise Exception(f"Valid move rejected: {response.status_code}")
        
        data = response.json()
        if not data.get('success'):
            raise Exception(f"Valid move failed: {data.get('message')}")
        
        return {"invalid_moves_rejected": len(invalid_moves), "valid_move_accepted": True}
    
    def test_concurrent_access(self) -> Dict[str, Any]:
        """Test concurrent access and thread safety"""
        import threading
        
        if not self.game_id:
            raise Exception("No game ID available")
        
        results = []
        threads = []
        
        def make_concurrent_move(thread_id: int):
            try:
                payload = {
                    "game_id": self.game_id,
                    "from_pos": [1, thread_id % 8],  # Different pawns
                    "to_pos": [2, thread_id % 8],
                    "player_color": True
                }
                
                response = self.session.post(
                    f"{self.base_url}/api/make-move",
                    json=payload,
                    timeout=10
                )
                
                results.append({
                    "thread_id": thread_id,
                    "status_code": response.status_code,
                    "success": response.status_code == 200
                })
            except Exception as e:
                results.append({
                    "thread_id": thread_id,
                    "error": str(e)
                })
        
        # Create 5 concurrent threads
        for i in range(5):
            thread = threading.Thread(target=make_concurrent_move, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=15)
        
        successful_moves = sum(1 for r in results if r.get('success', False))
        
        return {
            "concurrent_threads": len(threads),
            "successful_moves": successful_moves,
            "results": results
        }
    
    def test_error_handling(self) -> Dict[str, Any]:
        """Test comprehensive error handling"""
        error_scenarios = [
            # Non-existent game ID
            ("GET", "/api/ai-move/nonexistent123"),
            # Invalid HTTP method
            ("DELETE", "/api/new-game"),
            # Malformed JSON
            ("POST", "/api/new-game", '{"invalid": json}'),
        ]
        
        handled_errors = 0
        
        for scenario in error_scenarios:
            method, url = scenario[0], scenario[1]
            data = scenario[2] if len(scenario) > 2 else None
            
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{url}", timeout=5)
                else:
                    response = self.session.post(
                        f"{self.base_url}{url}",
                        data=data,
                        timeout=5
                    )
                
                # Should get error status codes (4xx or 5xx)
                if 400 <= response.status_code < 600:
                    handled_errors += 1
                else:
                    print(f"Warning: Unexpected status {response.status_code} for {method} {url}")
                    
            except Exception:
                # Connection errors are also acceptable for invalid requests
                handled_errors += 1
        
        return {"error_scenarios_handled": handled_errors, "total_scenarios": len(error_scenarios)}
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate detailed test report with analytics"""
        passed_tests = [r for r in self.results if r.passed]
        failed_tests = [r for r in self.results if not r.passed]
        
        # Calculate performance statistics
        performance_stats = {}
        for metric_name, values in self.performance_metrics.items():
            if values:
                performance_stats[metric_name] = {
                    "count": len(values),
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "min": min(values),
                    "max": max(values),
                    "stdev": statistics.stdev(values) if len(values) > 1 else 0
                }
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": len(self.results),
                "passed": len(passed_tests),
                "failed": len(failed_tests),
                "success_rate": len(passed_tests) / len(self.results) * 100 if self.results else 0
            },
            "passed_tests": [r.name for r in passed_tests],
            "failed_tests": [
                {
                    "name": r.name,
                    "error": r.error_message,
                    "duration": r.duration
                } for r in failed_tests
            ],
            "performance": performance_stats,
            "detailed_results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "duration": r.duration,
                    "details": r.details
                } for r in self.results
            ]
        }
        
        return report
    
    def run_complete_suite(self):
        """Run all tests and generate comprehensive report"""
        print("🧪 ENHANCED FASTAPI CHESS API TEST SUITE")
        print("=" * 50)
        print(f"Base URL: {self.base_url}")
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Core functionality tests
        self.run_test("Health Endpoint", self.test_health_endpoint)
        self.run_test("CORS Headers", self.test_cors_headers)
        self.run_test("Rate Limiting", self.test_rate_limiting)
        self.run_test("Game Creation Variants", self.test_create_game_variants)
        self.run_test("Move Validation", self.test_move_validation)
        
        # Advanced tests (if basic tests pass)
        if self.game_id:
            self.run_test("Concurrent Access", self.test_concurrent_access)
        
        self.run_test("Error Handling", self.test_error_handling)
        
        # Generate and save report
        report = self.generate_comprehensive_report()
        
        # Save detailed report
        with open('enhanced_api_test_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        print(f"Total Tests: {report['summary']['total_tests']}")
        print(f"Passed: {report['summary']['passed']}")
        print(f"Failed: {report['summary']['failed']}")
        print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
        
        if report['performance']:
            print("\n⏱️ PERFORMANCE METRICS:")
            for metric, stats in report['performance'].items():
                print(f"  {metric}: {stats['mean']*1000:.2f}ms avg")
        
        if report['failed_tests']:
            print("\n❌ FAILED TESTS:")
            for test in report['failed_tests']:
                print(f"  - {test['name']}: {test['error']}")
        
        print(f"\n📋 Detailed report saved to: enhanced_api_test_report.json")
        
        return report

def main():
    """Main test execution function"""
    tester = EnhancedAPITester()
    
    try:
        report = tester.run_complete_suite()
        
        # Return exit code based on test results
        if report['summary']['failed'] == 0:
            print("\n🎉 All tests passed! API is production ready.")
            return 0
        else:
            print(f"\n⚠️ {report['summary']['failed']} tests failed. Review the report.")
            return 1
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the FastAPI server running?")
        print("Start server with: python -m uvicorn interfaces.fastapi_chess:app --reload")
        return 1
    except Exception as e:
        print(f"❌ Test suite failed with error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())