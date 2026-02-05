# -*- coding: utf-8 -*-
"""
Advanced Security Audit and Compliance Module
Provides comprehensive security monitoring, auditing, and compliance checking
"""
import logging
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass, asdict
from flask import Blueprint, jsonify, request
from app import db
from app.models import User

logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityEventType(Enum):
    """Security event types"""
    LOGIN_ATTEMPT = "login_attempt"
    FAILED_LOGIN = "failed_login"
    SUCCESSFUL_LOGIN = "successful_login"
    PASSWORD_CHANGE = "password_change"
    AUTH_TOKEN_ISSUED = "auth_token_issued"
    AUTH_TOKEN_REVOKED = "auth_token_revoked"
    PERMISSION_VIOLATION = "permission_violation"
    DATA_ACCESS = "data_access"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    SECURITY_VIOLATION = "security_violation"

@dataclass
class SecurityEvent:
    """Security event data structure"""
    id: str
    event_type: SecurityEventType
    user_id: Optional[int]
    ip_address: str
    user_agent: str
    timestamp: datetime
    severity: SecurityLevel
    details: Dict[str, Any]
    signature: str  # For integrity verification

class SecurityAuditManager:
    """Main security audit manager"""
    
    def __init__(self):
        self.events: List[SecurityEvent] = []
        self.max_events = 10000
        self.suspicious_patterns = self._initialize_suspicious_patterns()
        self.threat_intelligence = self._initialize_threat_intelligence()
    
    def _initialize_suspicious_patterns(self) -> Dict[str, Any]:
        """Initialize suspicious activity patterns"""
        return {
            'failed_login_threshold': 5,
            'failed_login_window_minutes': 15,
            'concurrent_sessions_limit': 3,
            'suspicious_ips': set(),  # IPs flagged for suspicious activity
            'suspicious_user_agents': [
                'sqlmap', 'nikto', 'nessus', 'burp', 'zaproxy'
            ]
        }
    
    def _initialize_threat_intelligence(self) -> Dict[str, Any]:
        """Initialize threat intelligence data"""
        return {
            'known_malicious_ips': set(),
            'known_malicious_user_agents': set(),
            'suspicious_geolocations': set(),
            'last_updated': datetime.now()
        }
    
    def log_security_event(self, event_type: SecurityEventType, user_id: Optional[int] = None,
                          severity: SecurityLevel = SecurityLevel.MEDIUM, 
                          details: Dict[str, Any] = None) -> str:
        """Log a security event"""
        try:
            # Get request context if available
            ip_address = request.remote_addr if request else 'unknown'
            user_agent = request.headers.get('User-Agent', 'unknown') if request else 'unknown'
            
            # Create event
            event_id = f"evt_{int(time.time() * 1000000)}"
            event = SecurityEvent(
                id=event_id,
                event_type=event_type,
                user_id=user_id,
                ip_address=ip_address,
                user_agent=user_agent,
                timestamp=datetime.now(),
                severity=severity,
                details=details or {},
                signature=self._generate_signature(event_type, user_id, ip_address, user_agent)
            )
            
            # Add to events list
            self.events.append(event)
            
            # Maintain event history size
            if len(self.events) > self.max_events:
                self.events = self.events[-self.max_events:]
            
            # Check for suspicious activity
            self._check_suspicious_activity(event)
            
            logger.info(f"Security event logged: {event_type.value} - {event_id}")
            return event_id
            
        except Exception as e:
            logger.error(f"Error logging security event: {e}")
            return None
    
    def _generate_signature(self, event_type: SecurityEventType, user_id: Optional[int], 
                           ip_address: str, user_agent: str) -> str:
        """Generate event signature for integrity verification"""
        data = f"{event_type.value}:{user_id}:{ip_address}:{user_agent}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def _check_suspicious_activity(self, event: SecurityEvent):
        """Check for suspicious activity patterns"""
        try:
            # Check for known malicious patterns
            if self._is_malicious_user_agent(event.user_agent):
                self._flag_suspicious_event(event, "Malicious user agent detected")
                return
            
            # Check for brute force attempts
            if event.event_type == SecurityEventType.FAILED_LOGIN:
                self._check_brute_force(event)
            
            # Check for concurrent sessions
            if event.event_type == SecurityEventType.SUCCESSFUL_LOGIN:
                self._check_concurrent_sessions(event)
                
        except Exception as e:
            logger.error(f"Error checking suspicious activity: {e}")
    
    def _is_malicious_user_agent(self, user_agent: str) -> bool:
        """Check if user agent is potentially malicious"""
        user_agent_lower = user_agent.lower()
        for malicious_agent in self.suspicious_patterns['suspicious_user_agents']:
            if malicious_agent in user_agent_lower:
                return True
        return False
    
    def _check_brute_force(self, event: SecurityEvent):
        """Check for brute force login attempts"""
        try:
            # Get recent failed login attempts from same IP
            recent_failures = [
                e for e in self.events[-100:]  # Check last 100 events
                if (e.event_type == SecurityEventType.FAILED_LOGIN and
                    e.ip_address == event.ip_address and
                    datetime.now() - e.timestamp < timedelta(minutes=15))
            ]
            
            if len(recent_failures) >= self.suspicious_patterns['failed_login_threshold']:
                self._flag_suspicious_event(event, f"Brute force attempt detected: {len(recent_failures)} failed attempts")
                self.suspicious_patterns['suspicious_ips'].add(event.ip_address)
                
        except Exception as e:
            logger.error(f"Error checking brute force: {e}")
    
    def _check_concurrent_sessions(self, event: SecurityEvent):
        """Check for excessive concurrent sessions"""
        try:
            if not event.user_id:
                return
                
            # Get recent successful logins for this user
            recent_logins = [
                e for e in self.events[-50:]
                if (e.event_type == SecurityEventType.SUCCESSFUL_LOGIN and
                    e.user_id == event.user_id and
                    datetime.now() - e.timestamp < timedelta(hours=1))
            ]
            
            if len(recent_logins) > self.suspicious_patterns['concurrent_sessions_limit']:
                self._flag_suspicious_event(event, f"Excessive concurrent sessions: {len(recent_logins)} active sessions")
                
        except Exception as e:
            logger.error(f"Error checking concurrent sessions: {e}")
    
    def _flag_suspicious_event(self, event: SecurityEvent, reason: str):
        """Flag an event as suspicious"""
        logger.warning(f"Suspicious activity detected: {reason} - Event ID: {event.id}")
        
        # Update event severity if needed
        if event.severity.value in [SecurityLevel.LOW.value, SecurityLevel.MEDIUM.value]:
            event.severity = SecurityLevel.HIGH
        
        # Add suspicious flag to details
        event.details['suspicious'] = True
        event.details['suspicion_reason'] = reason
    
    def get_security_events(self, hours: int = 24, severity: SecurityLevel = None) -> List[Dict]:
        """Get security events within time range"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            filtered_events = [
                e for e in self.events
                if e.timestamp > cutoff_time
            ]
            
            if severity:
                filtered_events = [
                    e for e in filtered_events
                    if e.severity == severity
                ]
            
            return [asdict(event) for event in filtered_events]
            
        except Exception as e:
            logger.error(f"Error getting security events: {e}")
            return []
    
    def get_suspicious_activities(self, hours: int = 24) -> List[Dict]:
        """Get suspicious activities"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            suspicious_events = [
                e for e in self.events
                if (e.timestamp > cutoff_time and
                    e.details.get('suspicious', False))
            ]
            
            return [asdict(event) for event in suspicious_events]
            
        except Exception as e:
            logger.error(f"Error getting suspicious activities: {e}")
            return []
    
    def get_security_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get security summary statistics"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            recent_events = [e for e in self.events if e.timestamp > cutoff_time]
            
            # Count events by type
            event_counts = {}
            for event in recent_events:
                event_type = event.event_type.value
                event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
            # Count events by severity
            severity_counts = {}
            for event in recent_events:
                severity = event.severity.value
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Count suspicious activities
            suspicious_count = len([
                e for e in recent_events 
                if e.details.get('suspicious', False)
            ])
            
            return {
                'total_events': len(recent_events),
                'events_by_type': event_counts,
                'events_by_severity': severity_counts,
                'suspicious_activities': suspicious_count,
                'suspicious_ips': list(self.suspicious_patterns['suspicious_ips']),
                'time_period_hours': hours
            }
            
        except Exception as e:
            logger.error(f"Error getting security summary: {e}")
            return {}

# Global security audit manager
security_audit_manager = SecurityAuditManager()

# Flask blueprint for security audit endpoints
security_audit_bp = Blueprint('security_audit', __name__)

@security_audit_bp.route('/api/security/audit/events')
def get_security_events():
    """Get security events"""
    try:
        hours = int(request.args.get('hours', 24))
        severity = request.args.get('severity')
        
        if severity:
            try:
                severity = SecurityLevel(severity)
            except ValueError:
                severity = None
        
        events = security_audit_manager.get_security_events(hours, severity)
        return jsonify({
            'success': True,
            'events': events,
            'count': len(events)
        })
        
    except Exception as e:
        logger.error(f"Error getting security events: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@security_audit_bp.route('/api/security/audit/suspicious')
def get_suspicious_activities():
    """Get suspicious activities"""
    try:
        hours = int(request.args.get('hours', 24))
        activities = security_audit_manager.get_suspicious_activities(hours)
        return jsonify({
            'success': True,
            'suspicious_activities': activities,
            'count': len(activities)
        })
        
    except Exception as e:
        logger.error(f"Error getting suspicious activities: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@security_audit_bp.route('/api/security/audit/summary')
def get_security_summary():
    """Get security summary"""
    try:
        hours = int(request.args.get('hours', 24))
        summary = security_audit_manager.get_security_summary(hours)
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        logger.error(f"Error getting security summary: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def init_security_audit(app):
    """Initialize security audit system"""
    # Register blueprint
    app.register_blueprint(security_audit_bp)
    
    # Add security event logging to authentication flows
    from flask_login import user_logged_in, user_logged_out
    from flask import g
    
    @user_logged_in.connect_via(app)
    def on_user_logged_in(app, user):
        security_audit_manager.log_security_event(
            SecurityEventType.SUCCESSFUL_LOGIN,
            user_id=user.id,
            severity=SecurityLevel.LOW,
            details={'username': user.username}
        )
    
    @user_logged_out.connect_via(app)
    def on_user_logged_out(app, user):
        if hasattr(user, 'id'):
            security_audit_manager.log_security_event(
                SecurityEventType.AUTH_TOKEN_REVOKED,
                user_id=user.id,
                severity=SecurityLevel.LOW,
                details={'username': user.username}
            )
    
    logger.info("Security audit system initialized")
