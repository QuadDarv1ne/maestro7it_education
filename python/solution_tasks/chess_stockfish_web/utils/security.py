"""
Security utilities for the chess application.
Implements various security measures and best practices.
"""

import logging
import time
import secrets
import hashlib
import hmac
from functools import wraps
from typing import Dict, Any, Callable
from flask import request, session, jsonify, g
from datetime import datetime, timedelta
import re
import bleach
from urllib.parse import urlparse


logger = logging.getLogger(__name__)


class SecurityManager:
    """
    Central security management system for the chess application.
    Handles authentication, authorization, input validation, and security monitoring.
    """
    
    def __init__(self):
        self.failed_login_attempts = {}
        self.blocked_ips = {}
        self.session_tokens = {}
        self.rate_limits = {}
        self.security_log = []
        self.max_login_attempts = 5
        self.block_duration = 900  # 15 minutes
        self.session_timeout = 3600  # 1 hour
        self.csrf_tokens = {}
    
    def generate_secure_token(self, length: int = 32) -> str:
        """
        Generate a cryptographically secure token.
        
        Args:
            length: Length of the token in bytes
            
        Returns:
            Hex-encoded secure token
        """
        return secrets.token_hex(length)
    
    def generate_csrf_token(self) -> str:
        """
        Generate a CSRF token for the current session.
        
        Returns:
            CSRF token string
        """
        if 'user_id' not in session:
            token = self.generate_secure_token()
        else:
            # Create token tied to user session
            user_session = session.get('session_id', '')
            timestamp = str(int(time.time()))
            token_data = f"{user_session}:{timestamp}"
            token = hashlib.sha256(token_data.encode()).hexdigest()
        
        # Store in session and in our tracker
        session['_csrf_token'] = token
        self.csrf_tokens[token] = time.time()
        
        # Clean up old tokens
        self._cleanup_old_csrf_tokens()
        
        return token
    
    def validate_csrf_token(self, token: str) -> bool:
        """
        Validate a CSRF token.
        
        Args:
            token: Token to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not token or token not in self.csrf_tokens:
            return False
        
        # Check if token is expired (1 hour expiration)
        timestamp = self.csrf_tokens[token]
        if time.time() - timestamp > 3600:
            del self.csrf_tokens[token]
            return False
        
        return True
    
    def _cleanup_old_csrf_tokens(self):
        """Remove expired CSRF tokens."""
        current_time = time.time()
        expired_tokens = [
            token for token, timestamp in self.csrf_tokens.items()
            if current_time - timestamp > 3600
        ]
        for token in expired_tokens:
            del self.csrf_tokens[token]
    
    def sanitize_input(self, input_data: str, max_length: int = 1000) -> str:
        """
        Sanitize user input to prevent XSS and injection attacks.
        
        Args:
            input_data: Input string to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not input_data:
            return ""
        
        # Limit length
        if len(input_data) > max_length:
            input_data = input_data[:max_length]
        
        # Use bleach to sanitize HTML
        sanitized = bleach.clean(
            input_data,
            tags=['p', 'br', 'strong', 'em', 'u'],  # Allow minimal safe tags
            strip=True
        )
        
        # Remove potentially dangerous characters/sequences
        dangerous_patterns = [
            r'<script.*?>.*?</script>',  # Script tags
            r'javascript:',              # JS protocol
            r'on\w+\s*=',               # Event handlers
            r'data:',                    # Data URIs
            r'vbscript:',               # VBScript
        ]
        
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    def validate_ip(self, ip_address: str) -> bool:
        """
        Validate IP address format.
        
        Args:
            ip_address: IP address to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Basic IPv4 validation
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ipv4_pattern, ip_address):
            parts = ip_address.split('.')
            return all(0 <= int(part) <= 255 for part in parts)
        
        # Basic IPv6 validation
        ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|^::1$|^::$'
        return bool(re.match(ipv6_pattern, ip_address))
    
    def is_rate_limited(self, identifier: str, limit: int, window: int = 60) -> bool:
        """
        Check if an identifier is rate limited.
        
        Args:
            identifier: Unique identifier (IP, user ID, etc.)
            limit: Number of requests allowed
            window: Time window in seconds
            
        Returns:
            True if rate limited, False otherwise
        """
        current_time = time.time()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Clean old entries
        self.rate_limits[identifier] = [
            req_time for req_time in self.rate_limits[identifier]
            if current_time - req_time < window
        ]
        
        # Check if limit exceeded
        if len(self.rate_limits[identifier]) >= limit:
            return True
        
        # Add current request
        self.rate_limits[identifier].append(current_time)
        return False
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """
        Log a security-related event.
        
        Args:
            event_type: Type of security event
            details: Details about the event
        """
        event = {
            'timestamp': datetime.now(),
            'event_type': event_type,
            'details': details,
            'remote_addr': request.remote_addr if request else 'unknown'
        }
        self.security_log.append(event)
        
        # Also log to standard logger
        logger.info(f"SECURITY EVENT: {event_type} - {details}")
    
    def check_failed_login(self, username_or_ip: str) -> bool:
        """
        Check if login should be blocked due to too many failed attempts.
        
        Args:
            username_or_ip: Username or IP address to check
            
        Returns:
            True if blocked, False otherwise
        """
        current_time = time.time()
        
        # Check if IP is blocked
        if username_or_ip in self.blocked_ips:
            if current_time - self.blocked_ips[username_or_ip] < self.block_duration:
                return True
            else:
                # Unblock after duration
                del self.blocked_ips[username_or_ip]
        
        # Check failed attempts
        if username_or_ip in self.failed_login_attempts:
            attempts, last_attempt = self.failed_login_attempts[username_or_ip]
            # Reset attempts if last attempt was more than 15 minutes ago
            if current_time - last_attempt > self.block_duration:
                del self.failed_login_attempts[username_or_ip]
            elif attempts >= self.max_login_attempts:
                # Block IP/user
                self.blocked_ips[username_or_ip] = current_time
                self.log_security_event('BRUTE_FORCE_BLOCK', {
                    'identifier': username_or_ip,
                    'attempts': attempts
                })
                return True
        
        return False
    
    def record_failed_login(self, username_or_ip: str):
        """
        Record a failed login attempt.
        
        Args:
            username_or_ip: Username or IP address of failed attempt
        """
        current_time = time.time()
        if username_or_ip in self.failed_login_attempts:
            attempts, _ = self.failed_login_attempts[username_or_ip]
            self.failed_login_attempts[username_or_ip] = (attempts + 1, current_time)
        else:
            self.failed_login_attempts[username_or_ip] = (1, current_time)
        
        self.log_security_event('FAILED_LOGIN', {
            'identifier': username_or_ip,
            'timestamp': current_time
        })
    
    def reset_failed_login(self, username_or_ip: str):
        """
        Reset failed login attempts for a user/IP.
        
        Args:
            username_or_ip: Username or IP address to reset
        """
        if username_or_ip in self.failed_login_attempts:
            del self.failed_login_attempts[username_or_ip]
        
        if username_or_ip in self.blocked_ips:
            del self.blocked_ips[username_or_ip]


# Global security manager instance
security_manager = SecurityManager()


def require_csrf_protection(f):
    """
    Decorator to enforce CSRF protection on routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
            if not token or not security_manager.validate_csrf_token(token):
                logger.warning(f"CSRF validation failed for {request.endpoint} from {request.remote_addr}")
                return jsonify({
                    'success': False, 
                    'message': 'Invalid or missing CSRF token'
                }), 400
        return f(*args, **kwargs)
    return decorated_function


def validate_input(max_length: int = 1000):
    """
    Decorator to validate and sanitize input.
    
    Args:
        max_length: Maximum allowed input length
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Sanitize form data
            if request.form:
                for key, value in request.form.items():
                    if isinstance(value, str):
                        sanitized = security_manager.sanitize_input(value, max_length)
                        if sanitized != value:
                            logger.warning(f"Input sanitized for field {key}")
            
            # Sanitize JSON data
            if request.is_json:
                json_data = request.get_json()
                if isinstance(json_data, dict):
                    for key, value in json_data.items():
                        if isinstance(value, str):
                            sanitized = security_manager.sanitize_input(value, max_length)
                            if sanitized != value:
                                logger.warning(f"JSON input sanitized for field {key}")
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def rate_limit(max_requests: int, window: int = 60, per: str = 'ip'):
    """
    Decorator to apply rate limiting.
    
    Args:
        max_requests: Maximum number of requests allowed
        window: Time window in seconds
        per: What to rate limit by ('ip', 'user', 'session')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if per == 'ip':
                identifier = request.remote_addr
            elif per == 'user':
                identifier = session.get('user_id', request.remote_addr)
            elif per == 'session':
                identifier = session.get('session_id', request.remote_addr)
            else:
                identifier = request.remote_addr
            
            if security_manager.is_rate_limited(identifier, max_requests, window):
                logger.warning(f"Rate limit exceeded for {identifier}")
                return jsonify({
                    'success': False,
                    'message': 'Rate limit exceeded. Please try again later.'
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def log_security_event(event_type: str, details: Dict[str, Any] = None):
    """
    Convenience function to log security events.
    
    Args:
        event_type: Type of security event
        details: Additional details about the event
    """
    if details is None:
        details = {}
    
    security_manager.log_security_event(event_type, details)


def validate_url(url: str, allowed_domains: list = None) -> bool:
    """
    Validate URL for security (prevent SSRF, open redirect).
    
    Args:
        url: URL to validate
        allowed_domains: List of allowed domains (optional)
        
    Returns:
        True if URL is safe, False otherwise
    """
    try:
        parsed = urlparse(url)
        
        # Check if it's a relative URL
        if not parsed.scheme and not parsed.netloc:
            return True  # Relative URLs are generally safe
        
        # Check scheme
        if parsed.scheme not in ['http', 'https']:
            return False
        
        # If allowed domains specified, check against them
        if allowed_domains:
            return parsed.netloc in allowed_domains
        
        # Basic check: no internal IPs
        netloc = parsed.netloc.lower()
        if any(internal in netloc for internal in ['localhost', '127.0.0.1', '::1']):
            return False
        
        return True
    except Exception:
        return False


def check_password_strength(password: str) -> tuple[bool, list[str]]:
    """
    Check password strength and return validation results.
    
    Args:
        password: Password to check
        
    Returns:
        Tuple of (is_strong, list_of_issues)
    """
    issues = []
    
    if len(password) < 8:
        issues.append("Password must be at least 8 characters long")
    
    if not re.search(r"[A-Z]", password):
        issues.append("Password must contain at least one uppercase letter")
    
    if not re.search(r"[a-z]", password):
        issues.append("Password must contain at least one lowercase letter")
    
    if not re.search(r"\d", password):
        issues.append("Password must contain at least one digit")
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        issues.append("Password should contain at least one special character")
    
    return len(issues) == 0, issues