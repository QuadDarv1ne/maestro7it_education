"""
Rate limiting and API protection utilities
"""
from functools import wraps
from flask import request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from collections import defaultdict
import time
import logging
from threading import Lock

class RateLimiter:
    """Advanced rate limiting with multiple strategies"""
    
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = Lock()
        self.limits = {
            'default': {'requests': 100, 'window': 60},  # 100 requests per minute
            'auth': {'requests': 10, 'window': 60},      # 10 auth requests per minute
            'api': {'requests': 200, 'window': 60},      # 200 API requests per minute
            'heavy': {'requests': 10, 'window': 300}     # 10 heavy operations per 5 minutes
        }
    
    def check_rate_limit(self, key, limit_type='default'):
        """Check if request exceeds rate limit"""
        with self.lock:
            current_time = time.time()
            limit_config = self.limits.get(limit_type, self.limits['default'])
            window = limit_config['window']
            max_requests = limit_config['requests']
            
            # Clean old requests
            self.requests[key] = [
                req_time for req_time in self.requests[key] 
                if current_time - req_time < window
            ]
            
            # Check limit
            if len(self.requests[key]) >= max_requests:
                return False
            
            # Record request
            self.requests[key].append(current_time)
            return True
    
    def get_reset_time(self, key, limit_type='default'):
        """Get time when rate limit resets"""
        with self.lock:
            if key not in self.requests or not self.requests[key]:
                return 0
            
            limit_config = self.limits.get(limit_type, self.limits['default'])
            window = limit_config['window']
            oldest_request = min(self.requests[key])
            return oldest_request + window

# Global rate limiter instance
rate_limiter = RateLimiter()

def rate_limit(limit_type='default', custom_limit=None):
    """
    Rate limiting decorator
    
    Args:
        limit_type: Type of limit to apply (default, auth, api, heavy)
        custom_limit: Custom limit dict with 'requests' and 'window' keys
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate client key
            client_ip = get_remote_address()
            endpoint = request.endpoint or 'unknown'
            key = f"{client_ip}:{endpoint}"
            
            # Use custom limit if provided
            if custom_limit:
                limit_config = custom_limit
                window = limit_config['window']
                max_requests = limit_config['requests']
                
                # Manual rate limiting for custom limits
                current_time = time.time()
                rate_limiter.requests[key] = [
                    req_time for req_time in rate_limiter.requests[key] 
                    if current_time - req_time < window
                ]
                
                if len(rate_limiter.requests[key]) >= max_requests:
                    reset_time = rate_limiter.get_reset_time(key) if rate_limiter.requests[key] else current_time + window
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'retry_after': int(reset_time - current_time)
                    }), 429
                
                rate_limiter.requests[key].append(current_time)
            else:
                # Use predefined limit type
                if not rate_limiter.check_rate_limit(key, limit_type):
                    reset_time = rate_limiter.get_reset_time(key, limit_type)
                    current_time = time.time()
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'retry_after': int(reset_time - current_time)
                    }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_rate_limit_headers(key, limit_type='default'):
    """Get rate limit headers for response"""
    with rate_limiter.lock:
        limit_config = rate_limiter.limits.get(limit_type, rate_limiter.limits['default'])
        max_requests = limit_config['requests']
        window = limit_config['window']
        
        current_requests = len(rate_limiter.requests.get(key, []))
        remaining = max(0, max_requests - current_requests)
        reset_time = rate_limiter.get_reset_time(key, limit_type)
        
        return {
            'X-RateLimit-Limit': str(max_requests),
            'X-RateLimit-Remaining': str(remaining),
            'X-RateLimit-Reset': str(int(reset_time)),
            'X-RateLimit-Window': str(window)
        }

# Flask-Limiter integration (if available)
try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    
    # Initialize Flask-Limiter
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["100 per minute"],
        storage_uri="memory://"
    )
    
    # Predefined rate limit decorators
    default_limit = limiter.limit("100/minute")
    auth_limit = limiter.limit("10/minute")
    api_limit = limiter.limit("200/minute")
    heavy_limit = limiter.limit("10/5minute")
    
except ImportError:
    # Fallback to custom implementation
    limiter = None
    default_limit = lambda f: f
    auth_limit = lambda f: f
    api_limit = lambda f: f
    heavy_limit = lambda f: f

# API protection utilities
class APIProtector:
    """Advanced API protection utilities"""
    
    def __init__(self):
        self.blocked_ips = set()
        self.suspicious_patterns = [
            'DROP TABLE',
            'DELETE FROM',
            'INSERT INTO',
            'UPDATE .* SET',
            'SELECT .* FROM .* WHERE .* OR',
            '<script>',
            'javascript:',
            'onload=',
            'onerror='
        ]
    
    def is_suspicious_request(self, request):
        """Check if request contains suspicious patterns"""
        # Check URL parameters
        for param, value in request.args.items():
            if any(pattern.lower() in str(value).lower() for pattern in self.suspicious_patterns):
                return True
        
        # Check form data
        for key, value in request.form.items():
            if any(pattern.lower() in str(value).lower() for pattern in self.suspicious_patterns):
                return True
        
        # Check JSON data
        if request.is_json:
            try:
                data = request.get_json()
                if self._check_suspicious_data(data):
                    return True
            except:
                pass
        
        return False
    
    def _check_suspicious_data(self, data):
        """Recursively check data for suspicious patterns"""
        if isinstance(data, dict):
            for key, value in data.items():
                if self._check_suspicious_data(key) or self._check_suspicious_data(value):
                    return True
        elif isinstance(data, list):
            for item in data:
                if self._check_suspicious_data(item):
                    return True
        elif isinstance(data, str):
            return any(pattern.lower() in data.lower() for pattern in self.suspicious_patterns)
        
        return False
    
    def block_ip(self, ip):
        """Block an IP address"""
        self.blocked_ips.add(ip)
        logging.warning(f"Blocked IP address: {ip}")
    
    def unblock_ip(self, ip):
        """Unblock an IP address"""
        self.blocked_ips.discard(ip)
    
    def is_ip_blocked(self, ip):
        """Check if IP is blocked"""
        return ip in self.blocked_ips

# Global API protector instance
api_protector = APIProtector()

def protect_api(f):
    """Decorator to protect API endpoints"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = get_remote_address()
        
        # Check if IP is blocked
        if api_protector.is_ip_blocked(client_ip):
            return jsonify({'error': 'Access denied'}), 403
        
        # Check for suspicious requests
        if api_protector.is_suspicious_request(request):
            api_protector.block_ip(client_ip)
            logging.warning(f"Suspicious request blocked from IP: {client_ip}")
            return jsonify({'error': 'Malicious request detected'}), 400
        
        # Add rate limit headers
        endpoint = request.endpoint or 'unknown'
        key = f"{client_ip}:{endpoint}"
        
        response = f(*args, **kwargs)
        
        # Add rate limit headers if response is JSON
        if hasattr(response, 'headers') and response.headers.get('Content-Type', '').startswith('application/json'):
            headers = get_rate_limit_headers(key)
            for header, value in headers.items():
                response.headers[header] = value
        
        return response
    
    return decorated_function

# Request throttling for heavy operations
class RequestThrottler:
    """Throttle heavy requests to prevent server overload"""
    
    def __init__(self):
        self.heavy_operations = defaultdict(list)
        self.lock = Lock()
        self.max_concurrent = 5  # Maximum concurrent heavy operations
    
    def can_execute_heavy_operation(self, operation_type):
        """Check if heavy operation can be executed"""
        with self.lock:
            current_time = time.time()
            # Clean old operations (older than 10 minutes)
            self.heavy_operations[operation_type] = [
                op_time for op_time in self.heavy_operations[operation_type]
                if current_time - op_time < 600
            ]
            
            if len(self.heavy_operations[operation_type]) >= self.max_concurrent:
                return False
            
            self.heavy_operations[operation_type].append(current_time)
            return True
    
    def get_queue_position(self, operation_type):
        """Get queue position for heavy operation"""
        with self.lock:
            return len(self.heavy_operations[operation_type])

# Global throttler instance
throttler = RequestThrottler()

def throttle_heavy_operation(operation_type='default'):
    """Decorator to throttle heavy operations"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not throttler.can_execute_heavy_operation(operation_type):
                position = throttler.get_queue_position(operation_type)
                return jsonify({
                    'error': 'Server busy',
                    'message': 'Too many heavy operations in progress',
                    'queue_position': position,
                    'retry_after': 30
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Security headers middleware
def add_security_headers(response):
    """Add security headers to response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response

# Request size limiting
def limit_request_size(max_content_length=10 * 1024 * 1024):  # 10MB default
    """Decorator to limit request size"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.content_length and request.content_length > max_content_length:
                return jsonify({
                    'error': 'Request too large',
                    'max_size': max_content_length
                }), 413
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator