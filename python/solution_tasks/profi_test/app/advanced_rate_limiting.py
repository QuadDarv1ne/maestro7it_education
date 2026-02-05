# -*- coding: utf-8 -*-
"""
Advanced API Rate Limiting and Monitoring System
Provides sophisticated rate limiting with monitoring and adaptive throttling
"""
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
from enum import Enum
from flask import request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

logger = logging.getLogger(__name__)

class RateLimitStrategy(Enum):
    """Rate limiting strategies"""
    FIXED_WINDOW = "fixed_window"
    SLIDING_WINDOW = "sliding_window"
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"

class RateLimitScope(Enum):
    """Rate limit scopes"""
    GLOBAL = "global"
    PER_USER = "per_user"
    PER_IP = "per_ip"
    PER_ENDPOINT = "per_endpoint"

@dataclass
class RateLimitRule:
    """Rate limit rule definition"""
    name: str
    limit: int
    window_seconds: int
    scope: RateLimitScope
    strategy: RateLimitStrategy
    priority: int = 0  # Higher priority rules take precedence
    exempt_conditions: List[str] = None  # Conditions to exempt from limiting

@dataclass
class RateLimitState:
    """Rate limit state tracking"""
    key: str
    count: int
    last_reset: datetime
    window_start: datetime
    tokens: float = 0.0  # For token bucket strategy
    last_request: datetime = None

class AdvancedRateLimiter:
    """Advanced rate limiting system with monitoring"""
    
    def __init__(self):
        self.rules: List[RateLimitRule] = []
        self.states: Dict[str, RateLimitState] = {}
        self.monitoring_data: Dict[str, List] = defaultdict(list)
        self.max_monitoring_history = 1000
        self.exempt_ips = set()
        self.exempt_users = set()
        
        # Initialize default rules
        self._setup_default_rules()
    
    def _setup_default_rules(self):
        """Setup default rate limiting rules"""
        # Global rate limit
        self.add_rule(RateLimitRule(
            name="global_limit",
            limit=1000,
            window_seconds=3600,  # 1000 requests per hour globally
            scope=RateLimitScope.GLOBAL,
            strategy=RateLimitStrategy.FIXED_WINDOW,
            priority=0
        ))
        
        # Per IP limits
        self.add_rule(RateLimitRule(
            name="ip_limit_basic",
            limit=100,
            window_seconds=3600,  # 100 requests per hour per IP
            scope=RateLimitScope.PER_IP,
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            priority=10
        ))
        
        # Per user limits (authenticated users)
        self.add_rule(RateLimitRule(
            name="user_limit_basic",
            limit=500,
            window_seconds=3600,  # 500 requests per hour per user
            scope=RateLimitScope.PER_USER,
            strategy=RateLimitStrategy.SLIDING_WINDOW,
            priority=20
        ))
        
        # API endpoint specific limits
        self.add_rule(RateLimitRule(
            name="api_heavy_endpoint",
            limit=30,
            window_seconds=3600,  # 30 requests per hour for heavy endpoints
            scope=RateLimitScope.PER_ENDPOINT,
            strategy=RateLimitStrategy.TOKEN_BUCKET,
            priority=30
        ))
    
    def add_rule(self, rule: RateLimitRule):
        """Add a rate limiting rule"""
        self.rules.append(rule)
        self.rules.sort(key=lambda x: x.priority, reverse=True)
        logger.info(f"Added rate limit rule: {rule.name}")
    
    def remove_rule(self, rule_name: str):
        """Remove a rate limiting rule"""
        self.rules = [rule for rule in self.rules if rule.name != rule_name]
        logger.info(f"Removed rate limit rule: {rule_name}")
    
    def exempt_ip(self, ip: str):
        """Exempt an IP from rate limiting"""
        self.exempt_ips.add(ip)
        logger.info(f"Exempted IP from rate limiting: {ip}")
    
    def exempt_user(self, user_id: int):
        """Exempt a user from rate limiting"""
        self.exempt_users.add(user_id)
        logger.info(f"Exempted user from rate limiting: {user_id}")
    
    def check_rate_limit(self, user_id: Optional[int] = None, 
                        endpoint: Optional[str] = None) -> Tuple[bool, Optional[Dict]]:
        """Check if request should be rate limited"""
        try:
            client_ip = get_remote_address()
            
            # Check exemptions
            if client_ip in self.exempt_ips:
                return True, None
            
            if user_id and user_id in self.exempt_users:
                return True, None
            
            # Get applicable rules
            applicable_rules = self._get_applicable_rules(user_id, endpoint, client_ip)
            
            # Check each rule
            for rule in applicable_rules:
                key = self._generate_key(rule, user_id, endpoint, client_ip)
                allowed, details = self._check_rule(rule, key, user_id, endpoint, client_ip)
                
                if not allowed:
                    # Log the rate limit violation
                    self._log_rate_limit_violation(rule, key, user_id, client_ip, details)
                    return False, details
            
            # Record successful request
            self._record_request(user_id, endpoint, client_ip)
            return True, None
            
        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return True, None  # Fail open on errors
    
    def _get_applicable_rules(self, user_id: Optional[int], endpoint: Optional[str], 
                             client_ip: str) -> List[RateLimitRule]:
        """Get rules that apply to this request"""
        applicable = []
        
        for rule in self.rules:
            # Check exemption conditions
            if rule.exempt_conditions:
                if self._check_exemption_conditions(rule, user_id, endpoint, client_ip):
                    continue
            
            # Check scope matching
            if rule.scope == RateLimitScope.GLOBAL:
                applicable.append(rule)
            elif rule.scope == RateLimitScope.PER_IP:
                applicable.append(rule)
            elif rule.scope == RateLimitScope.PER_USER and user_id:
                applicable.append(rule)
            elif rule.scope == RateLimitScope.PER_ENDPOINT and endpoint:
                # Check if this is a heavy endpoint
                heavy_endpoints = ['/api/ml/recommend', '/api/search', '/api/analytics']
                if endpoint in heavy_endpoints:
                    applicable.append(rule)
        
        return applicable
    
    def _check_exemption_conditions(self, rule: RateLimitRule, user_id: Optional[int],
                                   endpoint: Optional[str], client_ip: str) -> bool:
        """Check if request meets exemption conditions"""
        for condition in rule.exempt_conditions or []:
            if condition == 'admin_user' and user_id:
                # Check if user is admin (would need user lookup)
                pass
            elif condition == 'local_ip' and client_ip in ['127.0.0.1', '::1']:
                return True
        return False
    
    def _generate_key(self, rule: RateLimitRule, user_id: Optional[int],
                     endpoint: Optional[str], client_ip: str) -> str:
        """Generate unique key for rate limit tracking"""
        if rule.scope == RateLimitScope.GLOBAL:
            return f"global_{rule.name}"
        elif rule.scope == RateLimitScope.PER_IP:
            return f"ip_{client_ip}_{rule.name}"
        elif rule.scope == RateLimitScope.PER_USER:
            return f"user_{user_id}_{rule.name}"
        elif rule.scope == RateLimitScope.PER_ENDPOINT:
            return f"endpoint_{endpoint}_{rule.name}"
    
    def _check_rule(self, rule: RateLimitRule, key: str, user_id: Optional[int],
                   endpoint: Optional[str], client_ip: str) -> Tuple[bool, Optional[Dict]]:
        """Check a specific rate limit rule"""
        current_time = datetime.now()
        
        # Initialize state if not exists
        if key not in self.states:
            self.states[key] = RateLimitState(
                key=key,
                count=0,
                last_reset=current_time,
                window_start=current_time,
                tokens=float(rule.limit)
            )
        
        state = self.states[key]
        
        # Apply strategy-specific logic
        if rule.strategy == RateLimitStrategy.FIXED_WINDOW:
            return self._check_fixed_window(rule, state, current_time)
        elif rule.strategy == RateLimitStrategy.SLIDING_WINDOW:
            return self._check_sliding_window(rule, state, current_time)
        elif rule.strategy == RateLimitStrategy.TOKEN_BUCKET:
            return self._check_token_bucket(rule, state, current_time)
        elif rule.strategy == RateLimitStrategy.LEAKY_BUCKET:
            return self._check_leaky_bucket(rule, state, current_time)
        
        return True, None
    
    def _check_fixed_window(self, rule: RateLimitRule, state: RateLimitState, 
                           current_time: datetime) -> Tuple[bool, Optional[Dict]]:
        """Fixed window rate limiting"""
        window_end = state.window_start + timedelta(seconds=rule.window_seconds)
        
        if current_time >= window_end:
            # Reset window
            state.count = 1
            state.window_start = current_time
            state.last_reset = current_time
            return True, None
        else:
            state.count += 1
            if state.count > rule.limit:
                reset_time = window_end
                return False, {
                    'limit': rule.limit,
                    'remaining': 0,
                    'reset': reset_time.isoformat(),
                    'retry_after': int((reset_time - current_time).total_seconds())
                }
            else:
                return True, {
                    'limit': rule.limit,
                    'remaining': rule.limit - state.count,
                    'reset': window_end.isoformat()
                }
    
    def _check_sliding_window(self, rule: RateLimitRule, state: RateLimitState,
                             current_time: datetime) -> Tuple[bool, Optional[Dict]]:
        """Sliding window rate limiting"""
        window_start = current_time - timedelta(seconds=rule.window_seconds)
        
        # For simplicity, we'll approximate sliding window with fixed window
        # In production, you'd want a more sophisticated implementation
        return self._check_fixed_window(rule, state, current_time)
    
    def _check_token_bucket(self, rule: RateLimitRule, state: RateLimitState,
                           current_time: datetime) -> Tuple[bool, Optional[Dict]]:
        """Token bucket rate limiting"""
        # Add tokens based on time passed
        time_passed = (current_time - state.last_reset).total_seconds()
        tokens_to_add = (time_passed / rule.window_seconds) * rule.limit
        state.tokens = min(rule.limit, state.tokens + tokens_to_add)
        state.last_reset = current_time
        
        if state.tokens >= 1:
            state.tokens -= 1
            return True, {
                'limit': rule.limit,
                'remaining': int(state.tokens),
                'reset': current_time.isoformat()
            }
        else:
            return False, {
                'limit': rule.limit,
                'remaining': 0,
                'reset': (current_time + timedelta(seconds=(1-state.tokens)*rule.window_seconds/rule.limit)).isoformat()
            }
    
    def _check_leaky_bucket(self, rule: RateLimitRule, state: RateLimitState,
                           current_time: datetime) -> Tuple[bool, Optional[Dict]]:
        """Leaky bucket rate limiting"""
        # Simplified implementation - similar to token bucket
        return self._check_token_bucket(rule, state, current_time)
    
    def _log_rate_limit_violation(self, rule: RateLimitRule, key: str, 
                                 user_id: Optional[int], client_ip: str, details: Dict):
        """Log rate limit violation"""
        violation_data = {
            'timestamp': datetime.now().isoformat(),
            'rule_name': rule.name,
            'key': key,
            'user_id': user_id,
            'ip_address': client_ip,
            'details': details
        }
        
        self.monitoring_data['violations'].append(violation_data)
        if len(self.monitoring_data['violations']) > self.max_monitoring_history:
            self.monitoring_data['violations'] = self.monitoring_data['violations'][-self.max_monitoring_history:]
        
        logger.warning(f"Rate limit violation: {rule.name} for {key}")
    
    def _record_request(self, user_id: Optional[int], endpoint: Optional[str], client_ip: str):
        """Record successful request for monitoring"""
        request_data = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'endpoint': endpoint,
            'ip_address': client_ip
        }
        
        self.monitoring_data['requests'].append(request_data)
        if len(self.monitoring_data['requests']) > self.max_monitoring_history:
            self.monitoring_data['requests'] = self.monitoring_data['requests'][-self.max_monitoring_history:]
    
    def get_monitoring_stats(self, hours: int = 24) -> Dict:
        """Get rate limiting monitoring statistics"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            
            # Filter recent data
            recent_violations = [
                v for v in self.monitoring_data['violations']
                if datetime.fromisoformat(v['timestamp']) > cutoff_time
            ]
            
            recent_requests = [
                r for r in self.monitoring_data['requests']
                if datetime.fromisoformat(r['timestamp']) > cutoff_time
            ]
            
            # Calculate statistics
            violation_by_rule = {}
            violation_by_ip = {}
            
            for violation in recent_violations:
                rule_name = violation['rule_name']
                ip_address = violation['ip_address']
                
                violation_by_rule[rule_name] = violation_by_rule.get(rule_name, 0) + 1
                violation_by_ip[ip_address] = violation_by_ip.get(ip_address, 0) + 1
            
            return {
                'total_requests': len(recent_requests),
                'total_violations': len(recent_violations),
                'violation_rate': len(recent_violations) / max(len(recent_requests), 1),
                'violations_by_rule': violation_by_rule,
                'violations_by_ip': dict(sorted(violation_by_ip.items(), 
                                              key=lambda x: x[1], reverse=True)[:10]),
                'time_period_hours': hours
            }
            
        except Exception as e:
            logger.error(f"Error getting monitoring stats: {e}")
            return {}

# Global rate limiter instance
advanced_rate_limiter = AdvancedRateLimiter()

# Flask decorator for rate limiting
def rate_limit(user_id_getter=None, endpoint_getter=None):
    """Decorator for applying rate limiting to Flask routes"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            # Get user ID if function provided
            user_id = None
            if user_id_getter:
                try:
                    user_id = user_id_getter()
                except:
                    pass
            
            # Get endpoint
            endpoint = request.endpoint if not endpoint_getter else endpoint_getter()
            
            # Check rate limit
            allowed, details = advanced_rate_limiter.check_rate_limit(user_id, endpoint)
            
            if not allowed:
                response = jsonify({
                    'error': 'Rate limit exceeded',
                    'details': details
                })
                response.status_code = 429
                response.headers['Retry-After'] = str(details.get('retry_after', 60))
                return response
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

def init_advanced_rate_limiting(app):
    """Initialize advanced rate limiting"""
    # You can integrate with Flask-Limiter or use the custom implementation
    logger.info("Advanced rate limiting system initialized")
