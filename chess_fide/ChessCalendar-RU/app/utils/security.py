"""
Security utilities for ChessCalendar-RU application

Этот модуль содержит специфические функции безопасности, не дублирующие
функциональность werkzeug.security (generate_password_hash/check_password_hash).
"""
import re
import bleach
from functools import wraps
from flask import request, abort, session
import logging
from datetime import datetime, timedelta
from typing import Optional


class SecurityUtils:
    """Security utilities for input validation and sanitization"""
    
    def __init__(self):
        self.logger = logging.getLogger('app.security')
        # Regex patterns for validation
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
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


# Global security utility instance
security_utils = SecurityUtils()


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
    
    return sanitized    sanitized['name'] = security_utils.sanitize_input(data.get('name', ''), max_length=200)
