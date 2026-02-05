# -*- coding: utf-8 -*-
"""
Comprehensive Health Check Module
Provides detailed health monitoring for all application components
"""
import logging
import time
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any
from flask import Blueprint, jsonify
from app import db

logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Health status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class HealthCheckComponent:
    """Base class for health check components"""
    
    def __init__(self, name: str, critical: bool = False):
        self.name = name
        self.critical = critical
        self.last_check = None
        self.last_status = HealthStatus.UNKNOWN
        self.last_error = None
    
    def check_health(self) -> Dict[str, Any]:
        """Perform health check - to be implemented by subclasses"""
        raise NotImplementedError
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status information"""
        return {
            'name': self.name,
            'status': self.last_status.value,
            'critical': self.critical,
            'last_check': self.last_check.isoformat() if self.last_check else None,
            'last_error': str(self.last_error) if self.last_error else None
        }

class DatabaseHealthCheck(HealthCheckComponent):
    """Database health check component"""
    
    def __init__(self):
        super().__init__("database", critical=True)
    
    def check_health(self) -> Dict[str, Any]:
        start_time = time.time()
        try:
            # Test database connection
            db.session.execute(db.text('SELECT 1'))
            db.session.commit()
            
            # Test query performance
            result = db.session.execute(db.text('SELECT COUNT(*) FROM user'))
            user_count = result.scalar()
            
            execution_time = time.time() - start_time
            
            self.last_status = HealthStatus.HEALTHY
            self.last_error = None
            
            return {
                'status': HealthStatus.HEALTHY.value,
                'response_time': execution_time,
                'user_count': user_count,
                'details': 'Database connection successful'
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.last_status = HealthStatus.UNHEALTHY
            self.last_error = e
            
            return {
                'status': HealthStatus.UNHEALTHY.value,
                'response_time': execution_time,
                'error': str(e),
                'details': 'Database connection failed'
            }
        finally:
            self.last_check = datetime.now()

class CacheHealthCheck(HealthCheckComponent):
    """Cache health check component"""
    
    def __init__(self, app):
        super().__init__("cache", critical=False)
        self.app = app
    
    def check_health(self) -> Dict[str, Any]:
        start_time = time.time()
        try:
            if hasattr(self.app, 'cache'):
                # Test cache set/get
                test_key = f"health_check_{int(time.time())}"
                test_value = "test_value"
                
                self.app.cache.set(test_key, test_value, timeout=30)
                cached_value = self.app.cache.get(test_key)
                
                execution_time = time.time() - start_time
                
                if cached_value == test_value:
                    self.last_status = HealthStatus.HEALTHY
                    self.last_error = None
                    return {
                        'status': HealthStatus.HEALTHY.value,
                        'response_time': execution_time,
                        'details': 'Cache connection successful'
                    }
                else:
                    raise Exception("Cache value mismatch")
            else:
                self.last_status = HealthStatus.UNKNOWN
                return {
                    'status': HealthStatus.UNKNOWN.value,
                    'details': 'Cache not configured'
                }
                
        except Exception as e:
            execution_time = time.time() - start_time
            self.last_status = HealthStatus.UNHEALTHY
            self.last_error = e
            
            return {
                'status': HealthStatus.UNHEALTHY.value,
                'response_time': execution_time,
                'error': str(e),
                'details': 'Cache connection failed'
            }
        finally:
            self.last_check = datetime.now()

class RedisHealthCheck(HealthCheckComponent):
    """Redis health check component"""
    
    def __init__(self, app):
        super().__init__("redis", critical=False)
        self.app = app
    
    def check_health(self) -> Dict[str, Any]:
        start_time = time.time()
        try:
            if hasattr(self.app, 'redis_cache'):
                # Test Redis connection
                redis_client = self.app.redis_cache.get_client()
                if redis_client:
                    # Ping Redis server
                    ping_result = redis_client.ping()
                    if ping_result:
                        execution_time = time.time() - start_time
                        self.last_status = HealthStatus.HEALTHY
                        self.last_error = None
                        return {
                            'status': HealthStatus.HEALTHY.value,
                            'response_time': execution_time,
                            'details': 'Redis connection successful'
                        }
            
            self.last_status = HealthStatus.UNKNOWN
            return {
                'status': HealthStatus.UNKNOWN.value,
                'details': 'Redis not available or configured'
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.last_status = HealthStatus.UNHEALTHY
            self.last_error = e
            
            return {
                'status': HealthStatus.UNHEALTHY.value,
                'response_time': execution_time,
                'error': str(e),
                'details': 'Redis connection failed'
            }
        finally:
            self.last_check = datetime.now()

class ApplicationHealthCheck(HealthCheckComponent):
    """Application health check component"""
    
    def __init__(self):
        super().__init__("application", critical=True)
    
    def check_health(self) -> Dict[str, Any]:
        try:
            # Check basic application functionality
            current_time = datetime.now()
            
            self.last_status = HealthStatus.HEALTHY
            self.last_error = None
            
            return {
                'status': HealthStatus.HEALTHY.value,
                'timestamp': current_time.isoformat(),
                'details': 'Application is running',
                'uptime': 'Not implemented'  # Could be implemented with application start time
            }
            
        except Exception as e:
            self.last_status = HealthStatus.UNHEALTHY
            self.last_error = e
            
            return {
                'status': HealthStatus.UNHEALTHY.value,
                'error': str(e),
                'details': 'Application check failed'
            }
        finally:
            self.last_check = datetime.now()

class ComprehensiveHealthCheck:
    """Main health check orchestrator"""
    
    def __init__(self, app):
        self.app = app
        self.components: List[HealthCheckComponent] = []
        self.setup_components()
    
    def setup_components(self):
        """Initialize all health check components"""
        self.components = [
            ApplicationHealthCheck(),
            DatabaseHealthCheck(),
            CacheHealthCheck(self.app),
            RedisHealthCheck(self.app)
        ]
        
        # Add custom components
        try:
            from app.task_scheduler import task_scheduler
            self.components.append(CeleryHealthCheck())
        except ImportError:
            pass
    
    def perform_health_check(self, detailed: bool = False) -> Dict[str, Any]:
        """Perform comprehensive health check"""
        start_time = time.time()
        
        results = []
        overall_status = HealthStatus.HEALTHY
        critical_failures = []
        
        for component in self.components:
            try:
                result = component.check_health()
                result['name'] = component.name
                result['critical'] = component.critical
                results.append(result)
                
                # Determine overall status
                if result['status'] == HealthStatus.UNHEALTHY.value:
                    if component.critical:
                        critical_failures.append(component.name)
                        overall_status = HealthStatus.UNHEALTHY
                    elif overall_status == HealthStatus.HEALTHY:
                        overall_status = HealthStatus.DEGRADED
                        
            except Exception as e:
                logger.error(f"Error checking health of {component.name}: {e}")
                # If a critical component fails completely, mark as unhealthy
                if component.critical:
                    critical_failures.append(component.name)
                    overall_status = HealthStatus.UNHEALTHY
                elif overall_status == HealthStatus.HEALTHY:
                    overall_status = HealthStatus.DEGRADED
        
        execution_time = time.time() - start_time
        
        response = {
            'status': overall_status.value,
            'timestamp': datetime.now().isoformat(),
            'execution_time': execution_time,
            'total_components': len(self.components),
            'healthy_components': len([r for r in results if r['status'] == HealthStatus.HEALTHY.value]),
            'degraded_components': len([r for r in results if r['status'] == HealthStatus.DEGRADED.value]),
            'unhealthy_components': len([r for r in results if r['status'] == HealthStatus.UNHEALTHY.value])
        }
        
        if detailed:
            response['components'] = results
            if critical_failures:
                response['critical_failures'] = critical_failures
        
        return response

class CeleryHealthCheck(HealthCheckComponent):
    """Celery worker health check"""
    
    def __init__(self):
        super().__init__("celery", critical=False)
    
    def check_health(self) -> Dict[str, Any]:
        try:
            # Check if Celery is available
            from app.tasks import celery
            
            # Test basic Celery functionality
            inspector = celery.control.inspect()
            stats = inspector.stats()
            
            if stats:
                active_tasks = inspector.active()
                self.last_status = HealthStatus.HEALTHY
                self.last_error = None
                
                return {
                    'status': HealthStatus.HEALTHY.value,
                    'workers': len(stats),
                    'active_tasks': len(active_tasks) if active_tasks else 0,
                    'details': 'Celery workers are running'
                }
            else:
                self.last_status = HealthStatus.DEGRADED
                return {
                    'status': HealthStatus.DEGRADED.value,
                    'details': 'No Celery workers found'
                }
                
        except Exception as e:
            self.last_status = HealthStatus.UNHEALTHY
            self.last_error = e
            
            return {
                'status': HealthStatus.UNHEALTHY.value,
                'error': str(e),
                'details': 'Celery connection failed'
            }
        finally:
            self.last_check = datetime.now()

# Flask blueprint for health check endpoints
health_check_bp = Blueprint('health_check', __name__)
health_checker = None

@health_check_bp.route('/health')
def health_check():
    """Basic health check endpoint"""
    if not health_checker:
        return jsonify({'status': 'unknown', 'error': 'Health checker not initialized'}), 500
    
    try:
        result = health_checker.perform_health_check(detailed=False)
        status_code = 200 if result['status'] == HealthStatus.HEALTHY.value else 503
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': HealthStatus.UNHEALTHY.value,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@health_check_bp.route('/health/detailed')
def detailed_health_check():
    """Detailed health check endpoint"""
    if not health_checker:
        return jsonify({'status': 'unknown', 'error': 'Health checker not initialized'}), 500
    
    try:
        result = health_checker.perform_health_check(detailed=True)
        status_code = 200 if result['status'] == HealthStatus.HEALTHY.value else 503
        return jsonify(result), status_code
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        return jsonify({
            'status': HealthStatus.UNHEALTHY.value,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

def init_health_check(app):
    """Initialize health check system"""
    global health_checker
    health_checker = ComprehensiveHealthCheck(app)
    
    # Register blueprint
    app.register_blueprint(health_check_bp)
    
    logger.info("Health check system initialized")
