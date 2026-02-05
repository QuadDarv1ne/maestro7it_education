# -*- coding: utf-8 -*-
"""
Advanced API Testing and Documentation Generator
Provides automated API testing, documentation generation, and validation
"""
import json
import time
import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from threading import Thread
import requests
from flask import Blueprint, jsonify, request, render_template
from app import db

logger = logging.getLogger(__name__)

class TestStatus(Enum):
    """Test status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"

class TestCategory(Enum):
    """Test category enumeration"""
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    INTEGRATION = "integration"
    LOAD = "load"

@dataclass
class APITestCase:
    """API test case definition"""
    id: str
    name: str
    description: str
    category: TestCategory
    endpoint: str
    method: str
    headers: Dict[str, str]
    payload: Optional[Dict[str, Any]]
    expected_status: int
    expected_response: Optional[Dict[str, Any]]
    timeout: int = 30
    retries: int = 3

@dataclass
class TestResult:
    """Test result data"""
    test_id: str
    status: TestStatus
    start_time: float
    end_time: float
    response_status: Optional[int]
    response_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    execution_time: float
    retry_count: int

class APITestRunner:
    """Advanced API test runner with parallel execution"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.test_cases: List[APITestCase] = []
        self.test_results: Dict[str, TestResult] = {}
        self.test_history: List[Dict] = []
        self.running = False
        
        # Initialize default test cases
        self._setup_default_tests()
    
    def _setup_default_tests(self):
        """Setup default API test cases"""
        # Health check tests
        self.add_test_case(APITestCase(
            id="health_check_basic",
            name="Basic Health Check",
            description="Test basic health check endpoint",
            category=TestCategory.FUNCTIONAL,
            endpoint="/health",
            method="GET",
            headers={},
            payload=None,
            expected_status=200
        ))
        
        self.add_test_case(APITestCase(
            id="health_check_detailed",
            name="Detailed Health Check",
            description="Test detailed health check endpoint",
            category=TestCategory.FUNCTIONAL,
            endpoint="/health/detailed",
            method="GET",
            headers={},
            payload=None,
            expected_status=200
        ))
        
        # Configuration API tests
        self.add_test_case(APITestCase(
            id="config_list",
            name="List Configurations",
            description="Test configuration listing endpoint",
            category=TestCategory.FUNCTIONAL,
            endpoint="/admin/api/config",
            method="GET",
            headers={"Content-Type": "application/json"},
            payload=None,
            expected_status=200
        ))
        
        # Security API tests
        self.add_test_case(APITestCase(
            id="security_summary",
            name="Security Summary",
            description="Test security audit summary endpoint",
            category=TestCategory.FUNCTIONAL,
            endpoint="/admin/api/security/audit/summary",
            method="GET",
            headers={"Content-Type": "application/json"},
            payload=None,
            expected_status=200
        ))
        
        # Performance API tests
        self.add_test_case(APITestCase(
            id="performance_metrics",
            name="Performance Metrics",
            description="Test performance metrics endpoint",
            category=TestCategory.FUNCTIONAL,
            endpoint="/admin/api/performance/metrics",
            method="GET",
            headers={"Content-Type": "application/json"},
            payload=None,
            expected_status=200
        ))
    
    def add_test_case(self, test_case: APITestCase):
        """Add a test case"""
        self.test_cases.append(test_case)
        logger.info(f"Added test case: {test_case.name}")
    
    def remove_test_case(self, test_id: str):
        """Remove a test case"""
        self.test_cases = [test for test in self.test_cases if test.id != test_id]
        logger.info(f"Removed test case: {test_id}")
    
    def run_single_test(self, test_case: APITestCase) -> TestResult:
        """Run a single test case"""
        start_time = time.time()
        retry_count = 0
        last_error = None
        
        while retry_count <= test_case.retries:
            try:
                # Prepare request
                url = f"{self.base_url}{test_case.endpoint}"
                headers = test_case.headers.copy()
                
                # Add authentication if needed (this would be enhanced in production)
                # headers['Authorization'] = f'Bearer {self.get_auth_token()}'
                
                # Make request
                if test_case.method.upper() == "GET":
                    response = requests.get(url, headers=headers, timeout=test_case.timeout)
                elif test_case.method.upper() == "POST":
                    response = requests.post(url, json=test_case.payload, headers=headers, timeout=test_case.timeout)
                elif test_case.method.upper() == "PUT":
                    response = requests.put(url, json=test_case.payload, headers=headers, timeout=test_case.timeout)
                elif test_case.method.upper() == "DELETE":
                    response = requests.delete(url, headers=headers, timeout=test_case.timeout)
                else:
                    raise ValueError(f"Unsupported HTTP method: {test_case.method}")
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Check response
                status_match = response.status_code == test_case.expected_status
                response_data = None
                
                try:
                    response_data = response.json()
                except:
                    response_data = {"text": response.text}
                
                # Determine test status
                if status_match:
                    status = TestStatus.PASSED
                    error_message = None
                else:
                    status = TestStatus.FAILED
                    error_message = f"Expected status {test_case.expected_status}, got {response.status_code}"
                
                result = TestResult(
                    test_id=test_case.id,
                    status=status,
                    start_time=start_time,
                    end_time=end_time,
                    response_status=response.status_code,
                    response_data=response_data,
                    error_message=error_message,
                    execution_time=execution_time,
                    retry_count=retry_count
                )
                
                return result
                
            except Exception as e:
                retry_count += 1
                last_error = str(e)
                if retry_count <= test_case.retries:
                    time.sleep(1)  # Wait before retry
                else:
                    end_time = time.time()
                    execution_time = end_time - start_time
                    
                    result = TestResult(
                        test_id=test_case.id,
                        status=TestStatus.ERROR,
                        start_time=start_time,
                        end_time=end_time,
                        response_status=None,
                        response_data=None,
                        error_message=last_error,
                        execution_time=execution_time,
                        retry_count=retry_count
                    )
                    return result
    
    def run_all_tests(self, parallel: bool = True) -> Dict[str, TestResult]:
        """Run all test cases"""
        if self.running:
            raise RuntimeError("Tests are already running")
        
        self.running = True
        results = {}
        
        try:
            if parallel:
                # Run tests in parallel using threads
                threads = []
                thread_results = {}
                
                def run_test_thread(test_case):
                    result = self.run_single_test(test_case)
                    thread_results[test_case.id] = result
                
                # Create and start threads
                for test_case in self.test_cases:
                    thread = Thread(target=run_test_thread, args=(test_case,))
                    threads.append(thread)
                    thread.start()
                
                # Wait for all threads to complete
                for thread in threads:
                    thread.join()
                
                results = thread_results
            else:
                # Run tests sequentially
                for test_case in self.test_cases:
                    result = self.run_single_test(test_case)
                    results[test_case.id] = result
            
            # Store results
            self.test_results.update(results)
            self._store_test_history(results)
            
            return results
            
        finally:
            self.running = False
    
    def _store_test_history(self, results: Dict[str, TestResult]):
        """Store test results in history"""
        history_entry = {
            "timestamp": time.time(),
            "results": {test_id: asdict(result) for test_id, result in results.items()},
            "summary": self.get_test_summary(results)
        }
        self.test_history.append(history_entry)
        
        # Keep only recent history
        if len(self.test_history) > 100:
            self.test_history = self.test_history[-100:]
    
    def get_test_summary(self, results: Dict[str, TestResult]) -> Dict[str, Any]:
        """Get summary of test results"""
        total_tests = len(results)
        passed_tests = len([r for r in results.values() if r.status == TestStatus.PASSED])
        failed_tests = len([r for r in results.values() if r.status == TestStatus.FAILED])
        error_tests = len([r for r in results.values() if r.status == TestStatus.ERROR])
        
        total_execution_time = sum(r.execution_time for r in results.values())
        avg_execution_time = total_execution_time / max(total_tests, 1)
        
        return {
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "errors": error_tests,
            "success_rate": passed_tests / max(total_tests, 1),
            "total_execution_time": total_execution_time,
            "average_execution_time": avg_execution_time,
            "timestamp": time.time()
        }
    
    def get_test_results(self) -> Dict[str, TestResult]:
        """Get all test results"""
        return self.test_results.copy()
    
    def get_test_history(self, limit: int = 10) -> List[Dict]:
        """Get test history"""
        return self.test_history[-limit:]
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        if not self.test_results:
            return {"error": "No test results available"}
        
        summary = self.get_test_summary(self.test_results)
        
        # Group results by category
        results_by_category = {}
        for test_case in self.test_cases:
            category = test_case.category.value
            if category not in results_by_category:
                results_by_category[category] = []
            
            if test_case.id in self.test_results:
                result = self.test_results[test_case.id]
                results_by_category[category].append({
                    "test_case": asdict(test_case),
                    "result": asdict(result)
                })
        
        return {
            "summary": summary,
            "results_by_category": results_by_category,
            "test_cases": [asdict(tc) for tc in self.test_cases],
            "generated_at": time.time()
        }

class APIDocumentationGenerator:
    """Advanced API documentation generator"""
    
    def __init__(self):
        self.api_specs = {}
        self.examples = {}
        
    def register_endpoint(self, endpoint: str, method: str, spec: Dict[str, Any]):
        """Register API endpoint specification"""
        key = f"{method.upper()} {endpoint}"
        self.api_specs[key] = spec
        logger.info(f"Registered API endpoint: {key}")
    
    def add_example(self, endpoint: str, method: str, example: Dict[str, Any]):
        """Add example for API endpoint"""
        key = f"{method.upper()} {endpoint}"
        if key not in self.examples:
            self.examples[key] = []
        self.examples[key].append(example)
    
    def generate_openapi_spec(self) -> Dict[str, Any]:
        """Generate OpenAPI 3.0 specification"""
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "ProfiTest API",
                "version": "1.0.0",
                "description": "Enterprise Career Guidance System API"
            },
            "servers": [
                {
                    "url": "http://localhost:5000",
                    "description": "Development server"
                }
            ],
            "paths": {},
            "components": {
                "schemas": {
                    "ErrorResponse": {
                        "type": "object",
                        "properties": {
                            "success": {"type": "boolean", "example": False},
                            "error": {"type": "string", "example": "Error message"}
                        }
                    },
                    "SuccessResponse": {
                        "type": "object",
                        "properties": {
                            "success": {"type": "boolean", "example": True},
                            "data": {"type": "object"}
                        }
                    }
                }
            }
        }
        
        # Add paths from registered endpoints
        for key, endpoint_spec in self.api_specs.items():
            method, path = key.split(" ", 1)
            
            if path not in spec["paths"]:
                spec["paths"][path] = {}
            
            # Add method specification
            spec["paths"][path][method.lower()] = {
                "summary": endpoint_spec.get("summary", ""),
                "description": endpoint_spec.get("description", ""),
                "parameters": endpoint_spec.get("parameters", []),
                "requestBody": endpoint_spec.get("requestBody"),
                "responses": endpoint_spec.get("responses", {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/SuccessResponse"}
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ErrorResponse"}
                            }
                        }
                    }
                })
            }
            
            # Add examples if available
            if key in self.examples:
                examples = self.examples[key]
                if examples:
                    spec["paths"][path][method.lower()]["responses"]["200"]["content"] = {
                        "application/json": {
                            "examples": {
                                f"example_{i+1}": {
                                    "summary": f"Example {i+1}",
                                    "value": example
                                }
                                for i, example in enumerate(examples)
                            }
                        }
                    }
        
        return spec
    
    def generate_markdown_docs(self) -> str:
        """Generate Markdown documentation"""
        lines = []
        lines.append("# ProfiTest API Documentation")
        lines.append("")
        lines.append("## Overview")
        lines.append("Enterprise Career Guidance System API")
        lines.append("")
        
        # Group endpoints by path
        endpoints_by_path = {}
        for key, spec in self.api_specs.items():
            method, path = key.split(" ", 1)
            if path not in endpoints_by_path:
                endpoints_by_path[path] = []
            endpoints_by_path[path].append((method, spec))
        
        # Generate documentation for each path
        for path, methods in endpoints_by_path.items():
            lines.append(f"## {path}")
            lines.append("")
            
            for method, spec in methods:
                lines.append(f"### {method.upper()} {path}")
                lines.append("")
                lines.append(f"**Description:** {spec.get('description', 'No description')}")
                lines.append("")
                
                # Parameters
                parameters = spec.get('parameters', [])
                if parameters:
                    lines.append("**Parameters:**")
                    lines.append("")
                    for param in parameters:
                        lines.append(f"- `{param['name']}` ({param['in']}): {param.get('description', '')}")
                    lines.append("")
                
                # Request body
                request_body = spec.get('requestBody')
                if request_body:
                    lines.append("**Request Body:**")
                    lines.append("")
                    lines.append("```json")
                    lines.append(json.dumps(request_body.get('example', {}), indent=2))
                    lines.append("```")
                    lines.append("")
                
                # Examples
                key = f"{method} {path}"
                if key in self.examples:
                    lines.append("**Examples:**")
                    lines.append("")
                    for i, example in enumerate(self.examples[key], 1):
                        lines.append(f"**Example {i}:**")
                        lines.append("")
                        lines.append("```json")
                        lines.append(json.dumps(example, indent=2))
                        lines.append("```")
                        lines.append("")
        
        return "\n".join(lines)

# Global instances
api_test_runner = APITestRunner()
api_doc_generator = APIDocumentationGenerator()

# Flask blueprint for API testing and documentation
api_test_bp = Blueprint('api_testing', __name__)

@api_test_bp.route('/admin/api/testing/run')
def run_api_tests():
    """Run all API tests"""
    try:
        parallel = request.args.get('parallel', 'true').lower() == 'true'
        results = api_test_runner.run_all_tests(parallel=parallel)
        summary = api_test_runner.get_test_summary(results)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'results': {test_id: asdict(result) for test_id, result in results.items()}
        })
    except Exception as e:
        logger.error(f"Error running API tests: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_test_bp.route('/admin/api/testing/results')
def get_test_results():
    """Get test results"""
    try:
        results = api_test_runner.get_test_results()
        summary = api_test_runner.get_test_summary(results)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'results': {test_id: asdict(result) for test_id, result in results.items()}
        })
    except Exception as e:
        logger.error(f"Error getting test results: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_test_bp.route('/admin/api/testing/history')
def get_test_history():
    """Get test history"""
    try:
        limit = int(request.args.get('limit', 10))
        history = api_test_runner.get_test_history(limit)
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        })
    except Exception as e:
        logger.error(f"Error getting test history: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_test_bp.route('/admin/api/testing/report')
def generate_test_report():
    """Generate test report"""
    try:
        report = api_test_runner.generate_test_report()
        
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        logger.error(f"Error generating test report: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_test_bp.route('/admin/api/docs/spec')
def get_openapi_spec():
    """Get OpenAPI specification"""
    try:
        spec = api_doc_generator.generate_openapi_spec()
        return jsonify(spec)
    except Exception as e:
        logger.error(f"Error generating OpenAPI spec: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_test_bp.route('/admin/api/docs/markdown')
def get_markdown_docs():
    """Get Markdown documentation"""
    try:
        docs = api_doc_generator.generate_markdown_docs()
        return jsonify({
            'success': True,
            'markdown': docs
        })
    except Exception as e:
        logger.error(f"Error generating Markdown docs: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def init_api_testing(app):
    """Initialize API testing and documentation system"""
    # Register blueprint
    app.register_blueprint(api_test_bp)
    
    # Register common API endpoints
    api_doc_generator.register_endpoint(
        "/health",
        "GET",
        {
            "summary": "Health Check",
            "description": "Check if the application is running properly",
            "responses": {
                "200": {
                    "description": "Application is healthy"
                }
            }
        }
    )
    
    api_doc_generator.register_endpoint(
        "/admin/api/config",
        "GET",
        {
            "summary": "Get Configurations",
            "description": "Retrieve all application configurations",
            "responses": {
                "200": {
                    "description": "Configurations retrieved successfully"
                }
            }
        }
    )
    
    # Add examples
    api_doc_generator.add_example(
        "/health",
        "GET",
        {
            "status": "healthy",
            "timestamp": "2026-02-05T15:30:00Z"
        }
    )
    
    api_doc_generator.add_example(
        "/admin/api/config",
        "GET",
        {
            "success": True,
            "configs": {
                "app": {"name": "profi_test", "version": "1.0.0"},
                "database": {"url": "sqlite:///profi_test.db"}
            }
        }
    )
    
    logger.info("API testing and documentation system initialized")
