"""
Улучшенная система безопасности и аутентификации
"""
import hashlib
import secrets
import time
from datetime import datetime, timedelta
from functools import wraps
from typing import Optional, Dict, Any
import logging
from flask import request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

logger = logging.getLogger(__name__)

# Argon2 для более безопасного хеширования паролей
ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,
        self.username_pattern = re.compile(r'^[a-zA-Z0-9_]{3,20}$')  # 3-20 chars, alphanumeric and underscore
        self.url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:www\.)?'  # optional www.
            r'[a-zA-Z0-9.-]+'  # domain
            r'\.[a-zA-Z]{2,}'  # TLD
            r'(?:/[^\s]*)?$',  # optional path
            re.IGNORECASE
        )
        
    def sanitize_input(self, text: str, max_length: int = 1000) -> str:
        """Sanitize input text to prevent XSS and other injection attacks"""
        if not text:
            return ""
        
        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length]
        
        # Use bleach to sanitize HTML
        cleaned = bleach.clean(
            text, 
            tags=['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'],
            attributes={},
            strip=True
        )
        
        # Remove any potentially dangerous characters
        cleaned = cleaned.replace('\0', '')  # Remove null bytes
        cleaned = cleaned.replace('\x00', '')  # Remove null bytes alternative
        
        return cleaned.strip()
    
    def validate_email(self, email: str) -> tuple[bool, str]:
        """Validate email format"""
        if not email:
            return False, "Email is required"
        
        if len(email) > 100:
            return False, "Email too long"
        
        if not self.email_pattern.match(email):
            return False, "Invalid email format"
        
        return True, "Valid email"
    
    def validate_username(self, username: str) -> tuple[bool, str]:
        """Validate username format"""
        if not username:
            return False, "Username is required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(username) > 20:
            return False, "Username must be no more than 20 characters"
        
        if not self.username_pattern.match(username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, "Valid username"
    
    def validate_url(self, url: str) -> tuple[bool, str]:
        """Validate URL format"""
        if not url:
            return True, "URL is optional"
        
        if len(url) > 500:
            return False, "URL too long"
        
        if not self.url_pattern.match(url):
            return False, "Invalid URL format"
        
        return True, "Valid URL"
    
    def validate_csrf_token(self, token: str) -> bool:
        """Validate CSRF token"""
        if not token:
            return False
        stored_token = session.get('_csrf_token')
        if not stored_token:
            return False
        return token == stored_token
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF token"""
        import secrets
        token = secrets.token_hex(32)
        session['_csrf_token'] = token
        return token

def rate_limit(max_attempts: int = 5, window: int = 300):
    """Rate limiting decorator to prevent brute force attacks"""
    attempts = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ip_addr = request.remote_addr
            now = datetime.now()
            
            # Clean old attempts
            attempts[ip_addr] = [time for time in attempts.get(ip_addr, []) 
                               if now - time < timedelta(seconds=window)]
            
            # Check if limit exceeded
            if len(attempts[ip_addr]) >= max_attempts:
                abort(429, "Too many requests. Please try again later.")
            
            # Record this attempt
            attempts[ip_addr].append(now)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_csrf_token():
    """CSRF token validation decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # In a real implementation, you would check the CSRF token
            # This is a placeholder for demonstration
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def validate_json_input(required_fields: list = None):
    """Validate JSON input data"""
    if required_fields is None:
        required_fields = []
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                abort(400, "Content-Type must be application/json")
            
            data = request.get_json()
            if not data:
                abort(400, "No JSON data provided")
            
            # Check required fields
            for field in required_fields:
                if field not in data:
                    abort(400, f"Missing required field: {field}")
            
            # Sanitize all string inputs
            security_utils = SecurityUtils()
            for key, value in data.items():
                if isinstance(value, str):
                    data[key] = security_utils.sanitize_input(value)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Advanced security utilities
import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin


class AdvancedSecurityUtils(SecurityUtils):
    """Advanced security utilities extending basic security functions"""
    
    def __init__(self):
        super().__init__()
        self.rate_limits = {}  # In-memory rate limiting (use Redis in production)
        self.blocked_ips = set()  # IPs temporarily blocked
        self.suspicious_activities = []  # Track suspicious activities
        
    def hash_password(self, password: str, salt: Optional[str] = None) -> tuple[str, str]:
        """Hash password with salt using PBKDF2 (more secure than SHA-256)"""
        if salt is None:
            salt = secrets.token_hex(32)
        
        import hashlib
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                            salt.encode('utf-8'), 100000)
        return password_hash.hex(), salt
    
    def verify_password(self, password: str, stored_hash: str, salt: str) -> bool:
        """Verify password against stored hash and salt"""
        password_hash, _ = self.hash_password(password, salt)
        return hmac.compare_digest(password_hash, stored_hash)
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate cryptographically secure token"""
        return secrets.token_urlsafe(length)
    
    def validate_ip(self, ip: str) -> bool:
        """Basic IP validation"""
        import ipaddress
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
    
    def is_blocked_ip(self, ip: str) -> bool:
        """Check if IP is blocked"""
        return ip in self.blocked_ips
    
    def block_ip(self, ip: str, duration: int = 3600):
        """Block IP for specified duration (seconds)"""
        self.blocked_ips.add(ip)
        # In production, use Redis with TTL for persistence
        # For demo purposes, we'll just log it
        self.logger.warning(f"IP {ip} blocked for {duration} seconds")
    
    def check_rate_limit(self, identifier: str, max_requests: int = 10, window: int = 60) -> tuple[bool, str]:
        """Check rate limit for an identifier (IP, user_id, etc.)"""
        now = time.time()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Clean old requests outside the window
        self.rate_limits[identifier] = [
            req_time for req_time in self.rate_limits[identifier] 
            if now - req_time < window
        ]
        
        if len(self.rate_limits[identifier]) >= max_requests:
            return False, f"Rate limit exceeded: {max_requests} requests per {window} seconds"
        
        # Add current request
        self.rate_limits[identifier].append(now)
        return True, "OK"
    
    def detect_sql_injection(self, input_str: str) -> bool:
        """Basic SQL injection detection"""
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'UNION', 'EXEC', '--', ';']
        normalized = input_str.upper()
        return any(keyword in normalized for keyword in sql_keywords)
    
    def detect_xss_attempt(self, input_str: str) -> bool:
        """Basic XSS attempt detection"""
        xss_patterns = ['<SCRIPT', 'JAVASCRIPT:', 'ONLOAD=', 'ONCLICK=', '<IMG', 'ONERROR=', 'DATA:']
        normalized = input_str.upper()
        return any(pattern in normalized for pattern in xss_patterns)
    
    def validate_redirect_url(self, redirect_to: str, allowed_domains: list) -> str:
        """Validate redirect URL to prevent open redirect vulnerabilities"""
        if not redirect_to:
            return ''
        
        # Parse the URL
        parsed = urlparse(redirect_to)
        
        # Only allow relative URLs or URLs from allowed domains
        if not parsed.netloc:  # Relative URL
            return redirect_to
        
        if parsed.netloc in allowed_domains:
            return redirect_to
        
        # Return empty string if not in allowed domains
        return ''
    
    def log_security_event(self, event_type: str, details: dict):
        """Log security-related events"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details
        }
        self.logger.warning(f"SECURITY EVENT: {log_entry}")
        self.suspicious_activities.append(log_entry)
    
    def get_security_headers(self) -> dict:
        """Return recommended security headers"""
        return {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
            'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://code.jquery.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://fonts.googleapis.com https://cdn.jsdelivr.net; font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net; img-src 'self' data: https:",
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
        }


class InputValidator:
    """Comprehensive input validation utilities"""
    
    @staticmethod
    def validate_json_schema(data: dict, schema: dict) -> tuple[bool, list]:
        """Validate data against a simple schema definition"""
        errors = []
        
        # Check required fields
        for field, field_def in schema.items():
            if field_def.get('required', False):
                if field not in data or data[field] is None:
                    errors.append(f"Field '{field}' is required")
                    continue
            
            if field in data:
                value = data[field]
                field_type = field_def.get('type')
                max_length = field_def.get('max_length')
                min_length = field_def.get('min_length')
                
                # Type checking
                if field_type:
                    if field_type == 'string' and not isinstance(value, str):
                        errors.append(f"Field '{field}' must be a string")
                    elif field_type == 'integer' and not isinstance(value, int):
                        errors.append(f"Field '{field}' must be an integer")
                    elif field_type == 'boolean' and not isinstance(value, bool):
                        errors.append(f"Field '{field}' must be a boolean")
                    elif field_type == 'email' and not isinstance(value, str):
                        errors.append(f"Field '{field}' must be a string")
                    elif field_type == 'url' and not isinstance(value, str):
                        errors.append(f"Field '{field}' must be a string")
                
                # Length validation
                if isinstance(value, str):
                    if max_length and len(value) > max_length:
                        errors.append(f"Field '{field}' exceeds maximum length of {max_length}")
                    if min_length and len(value) < min_length:
                        errors.append(f"Field '{field}' is shorter than minimum length of {min_length}")
                
                # Special validations
                if field_type == 'email' and isinstance(value, str):
                    import re
                    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                    if not email_pattern.match(value):
                        errors.append(f"Field '{field}' must be a valid email address")
                
                if field_type == 'url' and isinstance(value, str):
                    import re
                    url_pattern = re.compile(
                        r'^https?://'  # http:// or https://
                        r'(?:www\.)?'  # optional www.
                        r'[a-zA-Z0-9.-]+'  # domain
                        r'\.[a-zA-Z]{2,}'  # TLD
                        r'(?:/[^\s]*)?$',  # optional path
                        re.IGNORECASE
                    )
                    if not url_pattern.match(value):
                        errors.append(f"Field '{field}' must be a valid URL")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def clean_input(text: str, allowed_tags: list = None, allowed_attributes: dict = None) -> str:
        """Clean input using bleach with customizable allowed tags"""
        if allowed_tags is None:
            allowed_tags = ['p', 'br', 'strong', 'em', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        if allowed_attributes is None:
            allowed_attributes = {}
        
        import bleach
        return bleach.clean(text, tags=allowed_tags, attributes=allowed_attributes, strip=True)


# Global security utility instances
security_utils = SecurityUtils()
advanced_security = AdvancedSecurityUtils()
input_validator = InputValidator()


def sanitize_tournament_data(data: dict) -> dict:
    """Specific sanitizer for tournament data"""
    sanitized = {}
    security_utils = SecurityUtils()
    
    # Sanitize each field according to its purpose
    sanitized['name'] = security_utils.sanitize_input(data.get('name', ''), max_length=200)
    sanitized['location'] = security_utils.sanitize_input(data.get('location', ''), max_length=100)
    sanitized['description'] = security_utils.sanitize_input(data.get('description', ''), max_length=2000)
    sanitized['prize_fund'] = security_utils.sanitize_input(data.get('prize_fund', ''), max_length=200)
    sanitized['organizer'] = security_utils.sanitize_input(data.get('organizer', ''), max_length=200)
    
    # Validate and sanitize URL
    source_url = data.get('source_url', '')
    if source_url:
        is_valid, msg = security_utils.validate_url(source_url)
        if is_valid:
            sanitized['source_url'] = security_utils.sanitize_input(source_url, max_length=300)
        else:
            sanitized['source_url'] = None
    
    # Keep certain fields as-is (they should be validated separately)
    sanitized['start_date'] = data.get('start_date')
    sanitized['end_date'] = data.get('end_date')
    sanitized['category'] = data.get('category')
    sanitized['status'] = data.get('status')
    sanitized['fide_id'] = data.get('fide_id')
    
    return sanitized


def apply_security_headers(response):
    """Apply security headers to Flask response"""
    headers = advanced_security.get_security_headers()
    for header, value in headers.items():
        response.headers[header] = value
    return response
