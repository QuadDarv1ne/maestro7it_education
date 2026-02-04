"""
Enhanced security features and audit logging system
"""
import logging
import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta, timezone
from collections import defaultdict, deque
from threading import Lock
from functools import wraps
from flask import request, g, abort, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re
import json

logger = logging.getLogger(__name__)

class SecurityManager:
    """Advanced security management system"""
    
    def __init__(self, app=None):
        self.app = app
        self.security_events = deque(maxlen=1000)
        self.blocked_ips = set()
        self.suspicious_patterns = []
        self.rate_limits = {}
        self.lock = Lock()
        
        # Security thresholds
        self.thresholds = {
            'failed_login_attempts': 5,
            'failed_login_window': 300,  # 5 minutes
            'suspicious_request_score': 50,
            'brute_force_threshold': 10
        }
        
        # Common attack patterns
        self.attack_patterns = {
            'sql_injection': [
                r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|UNION)\b)",
                r"('\s*(OR|AND)\s*['\d])",
                r"(--|#).*",
                r"(\b(UNION|SELECT)\b.*\bFROM\b)"
            ],
            'xss': [
                r"(<script.*?>)",
                r"(\bjavascript:)",
                r"(\bon\w+\s*=)",
                r"(<iframe.*?>)",
                r"(\balert\s*\()"
            ],
            'command_injection': [
                r"(&&|\|\||;)",
                r"(\b(cat|ls|rm|wget|curl)\s+)",
                r"(\$\{.*\})",
                r"(`.*`)"
            ],
            'path_traversal': [
                r"(\.\./)",
                r"(\.\.\\)",
                r"(%2e%2e/)",
                r"(\/etc\/)"
            ]
        }
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security manager with Flask app"""
        self.app = app
        
        # Initialize rate limiter
        self.limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=["100 per hour", "10 per minute"],
            storage_uri="memory://"
        )
        
        # Setup security middleware
        self._setup_security_middleware(app)
        
        # Setup audit logging
        self._setup_audit_logging(app)
        
        logger.info("Security manager initialized")
    
    def _setup_security_middleware(self, app):
        """Setup security middleware and request validation"""
        
        @app.before_request
        def security_check():
            client_ip = request.remote_addr
            user_agent = request.headers.get('User-Agent', '')
            
            # Check if IP is blocked
            if client_ip in self.blocked_ips:
                logger.warning(f"Blocked request from {client_ip}")
                abort(403)
            
            # Analyze request for suspicious patterns
            risk_score = self._analyze_request_security(request)
            
            if risk_score > self.thresholds['suspicious_request_score']:
                self._log_security_event(
                    'suspicious_request',
                    client_ip,
                    {'risk_score': risk_score, 'user_agent': user_agent}
                )
                
                # Block extremely suspicious requests
                if risk_score > 80:
                    self._block_ip(client_ip, "High risk score")
                    abort(403)
            
            # Store security context
            g.security_context = {
                'client_ip': client_ip,
                'risk_score': risk_score,
                'user_agent': user_agent,
                'request_id': getattr(g, 'request_id', 'unknown')
            }
    
    def _setup_audit_logging(self, app):
        """Setup comprehensive audit logging"""
        
        @app.after_request
        def audit_log(response):
            if hasattr(g, 'security_context'):
                context = g.security_context
                
                # Log sensitive operations
                if request.method in ['POST', 'PUT', 'DELETE']:
                    self._log_audit_event(
                        'sensitive_operation',
                        context['client_ip'],
                        {
                            'method': request.method,
                            'endpoint': request.endpoint,
                            'status_code': response.status_code,
                            'user_id': getattr(g, 'user_id', 'anonymous')
                        }
                    )
                
                # Log authentication events
                if request.endpoint and 'login' in request.endpoint.lower():
                    self._log_audit_event(
                        'authentication_attempt',
                        context['client_ip'],
                        {
                            'success': response.status_code == 200,
                            'username': request.form.get('username', 'unknown')
                        }
                    )
            
            return response
    
    def _analyze_request_security(self, req):
        """Analyze request for security risks"""
        risk_score = 0
        suspicious_elements = []
        
        # Check URL parameters
        for param, value in req.args.items():
            score, elements = self._check_suspicious_content(value, f"param:{param}")
            risk_score += score
            suspicious_elements.extend(elements)
        
        # Check form data
        for key, value in req.form.items():
            score, elements = self._check_suspicious_content(value, f"form:{key}")
            risk_score += score
            suspicious_elements.extend(elements)
        
        # Check JSON data
        if req.is_json:
            try:
                data = req.get_json()
                score, elements = self._check_suspicious_content(str(data), "json_data")
                risk_score += score
                suspicious_elements.extend(elements)
            except Exception:
                risk_score += 10  # Malformed JSON
        
        # Check headers
        for header, value in req.headers:
            if header.lower() in ['user-agent', 'referer', 'cookie']:
                score, elements = self._check_suspicious_content(value, f"header:{header}")
                risk_score += score
                suspicious_elements.extend(elements)
        
        # Check for known attack patterns
        full_request = f"{req.method} {req.url} {req.data}"
        for pattern_type, patterns in self.attack_patterns.items():
            for pattern in patterns:
                if re.search(pattern, full_request, re.IGNORECASE):
                    risk_score += 25
                    suspicious_elements.append(f"{pattern_type}_pattern")
        
        return min(risk_score, 100)  # Cap at 100
    
    def _check_suspicious_content(self, content, context):
        """Check content for suspicious patterns"""
        if not content:
            return 0, []
        
        risk_score = 0
        suspicious_elements = []
        
        content_str = str(content).lower()
        
        # Check for SQL injection patterns
        for pattern in self.attack_patterns['sql_injection']:
            if re.search(pattern, content_str, re.IGNORECASE):
                risk_score += 15
                suspicious_elements.append(f"sql_injection:{context}")
        
        # Check for XSS patterns
        for pattern in self.attack_patterns['xss']:
            if re.search(pattern, content_str, re.IGNORECASE):
                risk_score += 20
                suspicious_elements.append(f"xss:{context}")
        
        # Check for command injection
        for pattern in self.attack_patterns['command_injection']:
            if re.search(pattern, content_str, re.IGNORECASE):
                risk_score += 25
                suspicious_elements.append(f"command_injection:{context}")
        
        # Check for path traversal
        for pattern in self.attack_patterns['path_traversal']:
            if re.search(pattern, content_str, re.IGNORECASE):
                risk_score += 20
                suspicious_elements.append(f"path_traversal:{context}")
        
        # Check for excessive length
        if len(content_str) > 10000:
            risk_score += 5
            suspicious_elements.append(f"excessive_length:{context}")
        
        return risk_score, suspicious_elements
    
    def _log_security_event(self, event_type, client_ip, details=None):
        """Log security-related events"""
        event = {
            'type': event_type,
            'client_ip': client_ip,
            'timestamp': datetime.now(datetime.UTC).isoformat(),
            'details': details or {}
        }
        
        with self.lock:
            self.security_events.append(event)
        
        logger.warning(f"Security Event [{event_type}] from {client_ip}: {details}")
    
    def _log_audit_event(self, event_type, client_ip, details=None):
        """Log audit trail events"""
        event = {
            'type': event_type,
            'client_ip': client_ip,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'details': details or {},
            'user_id': getattr(g, 'user_id', 'anonymous')
        }
        
        # Store in security events as well
        with self.lock:
            self.security_events.append(event)
        
        logger.info(f"Audit Event [{event_type}] from {client_ip}: {details}")
    
    def _block_ip(self, ip, reason="Security violation"):
        """Block an IP address"""
        with self.lock:
            self.blocked_ips.add(ip)
        
        self._log_security_event('ip_blocked', ip, {'reason': reason})
        logger.warning(f"IP {ip} blocked: {reason}")
    
    def get_security_events(self, event_type=None, hours=24):
        """Get recent security events"""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        cutoff_timestamp = cutoff_time.isoformat()
        
        with self.lock:
            events = list(self.security_events)
        
        filtered_events = [
            event for event in events
            if event['timestamp'] >= cutoff_timestamp
        ]
        
        if event_type:
            filtered_events = [
                event for event in filtered_events
                if event['type'] == event_type
            ]
        
        return filtered_events
    
    def get_blocked_ips(self):
        """Get list of currently blocked IPs"""
        with self.lock:
            return list(self.blocked_ips)
    
    def unblock_ip(self, ip):
        """Unblock an IP address"""
        with self.lock:
            self.blocked_ips.discard(ip)
        logger.info(f"IP {ip} unblocked")
    
    def get_security_report(self):
        """Generate comprehensive security report"""
        recent_events = self.get_security_events(hours=24)
        
        # Categorize events
        event_categories = defaultdict(int)
        blocked_ips_count = len(self.get_blocked_ips())
        suspicious_requests = 0
        
        for event in recent_events:
            event_categories[event['type']] += 1
            if event['type'] == 'suspicious_request':
                suspicious_requests += 1
        
        # Calculate security score
        security_score = self._calculate_security_score(
            len(recent_events), 
            blocked_ips_count, 
            suspicious_requests
        )
        
        return {
            'security_score': security_score,
            'blocked_ips_count': blocked_ips_count,
            'suspicious_requests': suspicious_requests,
            'event_summary': dict(event_categories),
            'recent_events': recent_events[-10:],  # Last 10 events
            'blocked_ips': self.get_blocked_ips(),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def _calculate_security_score(self, total_events, blocked_ips, suspicious_requests):
        """Calculate security health score (0-100)"""
        score = 100
        
        # Deduct points for security events
        score -= min(total_events * 2, 30)  # Max 30 points for events
        score -= min(blocked_ips * 5, 25)   # Max 25 points for blocked IPs
        score -= min(suspicious_requests * 3, 20)  # Max 20 points for suspicious requests
        
        return max(0, score)

class AuthenticationSecurity:
    """Authentication security utilities"""
    
    def __init__(self):
        self.failed_attempts = defaultdict(list)
        self.lock = Lock()
    
    def record_failed_login(self, username, client_ip):
        """Record failed login attempt"""
        now = time.time()
        attempt = {
            'timestamp': now,
            'client_ip': client_ip
        }
        
        with self.lock:
            self.failed_attempts[username].append(attempt)
            
            # Keep only recent attempts (last 5 minutes)
            cutoff = now - 300
            self.failed_attempts[username] = [
                a for a in self.failed_attempts[username]
                if a['timestamp'] > cutoff
            ]
    
    def check_brute_force(self, username, client_ip):
        """Check for brute force attack"""
        with self.lock:
            attempts = self.failed_attempts.get(username, [])
            
            # Check if threshold exceeded
            if len(attempts) >= 5:
                # Check if attempts are from same IP
                same_ip_attempts = [a for a in attempts if a['client_ip'] == client_ip]
                if len(same_ip_attempts) >= 3:
                    return True
        return False
    
    def generate_secure_token(self, length=32):
        """Generate cryptographically secure token"""
        return secrets.token_urlsafe(length)
    
    def hash_password(self, password, salt=None):
        """Secure password hashing"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Use PBKDF2 with SHA-256
        pwd_hash = hashlib.pbkdf2_hmac('sha256', 
                                     password.encode('utf-8'), 
                                     salt.encode('utf-8'), 
                                     100000)
        
        return salt + pwd_hash.hex()

# Global security manager instance
security_manager = SecurityManager()
auth_security = AuthenticationSecurity()

# Security decorators
def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            abort(401, "API key required")
        
        # Validate API key (implement your validation logic)
        if not _validate_api_key(api_key):
            abort(403, "Invalid API key")
        
        return f(*args, **kwargs)
    return decorated_function

def _validate_api_key(api_key):
    """Validate API key (implement your logic)"""
    # This is a placeholder - implement proper API key validation
    return api_key == "your-secure-api-key-here"

def rate_limit_exempt(f):
    """Decorator to exempt route from rate limiting"""
    f.rate_limit_exempt = True
    return f

def get_security_status():
    """Get current security status"""
    try:
        return security_manager.get_security_report()
    except Exception as e:
        logger.error(f"Failed to get security status: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

# Flask CLI commands for security management
def register_security_commands(app):
    """Register security management CLI commands"""
    import click
    from flask.cli import with_appcontext
    
    @app.cli.command('security-report')
    @with_appcontext
    def security_report():
        """Generate security report"""
        report = security_manager.get_security_report()
        
        click.echo("Security Report:")
        click.echo(f"Security Score: {report['security_score']}/100")
        click.echo(f"Blocked IPs: {report['blocked_ips_count']}")
        click.echo(f"Suspicious Requests: {report['suspicious_requests']}")
        click.echo(f"Total Events: {sum(report['event_summary'].values())}")
        
        if report['blocked_ips']:
            click.echo("\nBlocked IPs:")
            for ip in report['blocked_ips'][:10]:  # Show first 10
                click.echo(f"  {ip}")
        
        if report['event_summary']:
            click.echo("\nEvent Summary:")
            for event_type, count in report['event_summary'].items():
                click.echo(f"  {event_type}: {count}")
    
    @app.cli.command('unblock-ip')
    @click.argument('ip')
    @with_appcontext
    def unblock_ip(ip):
        """Unblock an IP address"""
        security_manager.unblock_ip(ip)
        click.echo(f"IP {ip} unblocked successfully")