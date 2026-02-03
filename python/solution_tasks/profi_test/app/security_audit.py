"""
Security Audit Module for Profi Test
Provides advanced security features and audit capabilities
"""
from datetime import datetime, timedelta
from flask import request, current_app
from flask_login import current_user
from app import db
from app.models import User
import hashlib
import secrets
import logging
from enum import Enum


class SecurityEventType(Enum):
    LOGIN_ATTEMPT = "login_attempt"
    FAILED_LOGIN = "failed_login"
    SUCCESSFUL_LOGIN = "successful_login"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    PROFILE_UPDATE = "profile_update"
    ADMIN_ACCESS = "admin_access"
    DATA_EXPORT = "data_export"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"


class SecurityAuditLog(db.Model):
    """Model for security audit logs"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    event_type = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)  # IPv6 support
    user_agent = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, default=True)
    details = db.Column(db.Text)  # Additional details about the event
    risk_level = db.Column(db.String(20), default='low')  # low, medium, high, critical
    
    # Relationships
    user = db.relationship('User', backref='security_logs')


class SecurityManager:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.failed_attempts_threshold = 5
        self.lockout_duration = timedelta(minutes=30)  # 30 minutes lockout
        self.max_sessions_per_user = 5
        self.trusted_networks = []  # List of IP networks that are trusted
    
    def log_security_event(self, event_type, user=None, success=True, details=None, risk_level='low'):
        """
        Log a security event
        """
        try:
            log_entry = SecurityAuditLog(
                user_id=user.id if user else None,
                event_type=event_type.value if isinstance(event_type, SecurityEventType) else event_type,
                ip_address=self._get_client_ip(),
                user_agent=request.headers.get('User-Agent', ''),
                success=success,
                details=details,
                risk_level=risk_level
            )
            
            db.session.add(log_entry)
            db.session.commit()
            
            # Also log to application logger
            log_msg = f"Security Event: {event_type}, User: {user.username if user else 'N/A'}, Success: {success}, Risk: {risk_level}"
            if details:
                log_msg += f", Details: {details}"
            
            if risk_level == 'critical':
                self.logger.critical(log_msg)
            elif risk_level == 'high':
                self.logger.error(log_msg)
            elif risk_level == 'medium':
                self.logger.warning(log_msg)
            else:
                self.logger.info(log_msg)
                
        except Exception as e:
            self.logger.error(f"Error logging security event: {str(e)}")
    
    def _get_client_ip(self):
        """
        Get client IP address considering proxies
        """
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            return request.environ['REMOTE_ADDR']
        else:
            return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0]
    
    def check_failed_login_attempts(self, username_or_email):
        """
        Check if user has exceeded failed login attempts threshold
        """
        try:
            # Get recent failed login attempts
            cutoff_time = datetime.utcnow() - self.lockout_duration
            recent_failures = SecurityAuditLog.query.filter(
                SecurityAuditLog.event_type == SecurityEventType.FAILED_LOGIN.value,
                SecurityAuditLog.timestamp >= cutoff_time,
                SecurityAuditLog.details.like(f'%{username_or_email}%')
            ).count()
            
            return recent_failures >= self.failed_attempts_threshold
        except Exception as e:
            self.logger.error(f"Error checking failed login attempts: {str(e)}")
            return False
    
    def record_login_attempt(self, username_or_email, success, user=None):
        """
        Record a login attempt
        """
        event_type = SecurityEventType.SUCCESSFUL_LOGIN if success else SecurityEventType.FAILED_LOGIN
        risk_level = 'medium' if not success else 'low'
        
        details = f"Username/Email attempted: {username_or_email}"
        if not success and self.check_failed_login_attempts(username_or_email):
            risk_level = 'high'
            details += " - Account may be locked due to too many failed attempts"
        
        self.log_security_event(event_type, user=user, success=success, details=details, risk_level=risk_level)
    
    def check_brute_force_attack(self, ip_address):
        """
        Check if IP address has too many failed attempts recently
        """
        try:
            cutoff_time = datetime.utcnow() - timedelta(minutes=15)  # Check last 15 minutes
            failed_attempts = SecurityAuditLog.query.filter(
                SecurityAuditLog.ip_address == ip_address,
                SecurityAuditLog.event_type == SecurityEventType.FAILED_LOGIN.value,
                SecurityAuditLog.timestamp >= cutoff_time
            ).count()
            
            return failed_attempts >= 10  # More than 10 failed attempts in 15 minutes
        except Exception as e:
            self.logger.error(f"Error checking brute force attack: {str(e)}")
            return False
    
    def is_ip_trusted(self, ip_address):
        """
        Check if IP address is in trusted networks
        """
        # For now, just return False - implement network checking later
        return False
    
    def detect_suspicious_activity(self, user, activity_type, details=None):
        """
        Detect and log suspicious activity
        """
        risk_level = 'medium'
        
        # Check for unusual activity patterns
        if activity_type == 'multiple_logins':
            # Check if user has logged in from multiple IPs recently
            recent_logins = SecurityAuditLog.query.filter(
                SecurityAuditLog.user_id == user.id,
                SecurityAuditLog.event_type == SecurityEventType.SUCCESSFUL_LOGIN.value,
                SecurityAuditLog.timestamp >= datetime.utcnow() - timedelta(hours=1)
            ).distinct(SecurityAuditLog.ip_address).count()
            
            if recent_logins > 3:  # More than 3 different IPs in 1 hour
                risk_level = 'high'
        
        elif activity_type == 'unusual_hours':
            # Check if login is at unusual time
            current_hour = datetime.utcnow().hour
            if current_hour < 6 or current_hour > 23:  # Between 11 PM and 6 AM
                risk_level = 'medium'
        
        elif activity_type == 'location_change':
            # Check if login location has changed dramatically
            risk_level = 'medium'
        
        self.log_security_event(
            SecurityEventType.SUSPICIOUS_ACTIVITY,
            user=user,
            success=True,  # Activity happened, regardless of if it's bad
            details=f"{activity_type}: {details}" if details else activity_type,
            risk_level=risk_level
        )
    
    def enforce_session_limit(self, user):
        """
        Enforce maximum number of concurrent sessions per user
        """
        try:
            # This would require a sessions table to track active sessions
            # For now, just log the check
            active_sessions = 0  # Would be calculated from sessions table
            
            if active_sessions > self.max_sessions_per_user:
                self.log_security_event(
                    'session_limit_exceeded',
                    user=user,
                    success=False,
                    details=f"User had {active_sessions} active sessions, limit is {self.max_sessions_per_user}",
                    risk_level='medium'
                )
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Error enforcing session limit: {str(e)}")
            return True
    
    def generate_secure_token(self, length=32):
        """
        Generate a cryptographically secure token
        """
        return secrets.token_urlsafe(length)
    
    def hash_sensitive_data(self, data):
        """
        Hash sensitive data for storage
        """
        return hashlib.sha256(data.encode()).hexdigest()
    
    def get_user_security_report(self, user_id):
        """
        Get security report for a specific user
        """
        try:
            user = User.query.get(user_id)
            if not user:
                return None
            
            # Get recent security events for the user
            two_weeks_ago = datetime.utcnow() - timedelta(days=14)
            recent_events = SecurityAuditLog.query.filter(
                SecurityAuditLog.user_id == user_id,
                SecurityAuditLog.timestamp >= two_weeks_ago
            ).order_by(SecurityAuditLog.timestamp.desc()).all()
            
            # Calculate statistics
            total_events = len(recent_events)
            failed_logins = sum(1 for event in recent_events if event.event_type == SecurityEventType.FAILED_LOGIN.value)
            successful_logins = sum(1 for event in recent_events if event.event_type == SecurityEventType.SUCCESSFUL_LOGIN.value)
            high_risk_events = sum(1 for event in recent_events if event.risk_level == 'high')
            medium_risk_events = sum(1 for event in recent_events if event.risk_level == 'medium')
            
            # Identify unique IP addresses used
            unique_ips = set(event.ip_address for event in recent_events)
            
            report = {
                'user_id': user_id,
                'username': user.username,
                'period_start': two_weeks_ago.isoformat(),
                'period_end': datetime.utcnow().isoformat(),
                'total_security_events': total_events,
                'failed_login_attempts': failed_logins,
                'successful_logins': successful_logins,
                'high_risk_events': high_risk_events,
                'medium_risk_events': medium_risk_events,
                'unique_ip_addresses_used': list(unique_ips),
                'last_login_event': next((event for event in recent_events 
                                        if event.event_type in [SecurityEventType.SUCCESSFUL_LOGIN.value, SecurityEventType.FAILED_LOGIN.value]), None),
                'recent_events': [{
                    'id': event.id,
                    'event_type': event.event_type,
                    'timestamp': event.timestamp.isoformat(),
                    'ip_address': event.ip_address,
                    'success': event.success,
                    'risk_level': event.risk_level,
                    'details': event.details
                } for event in recent_events[:20]]  # Last 20 events
            }
            
            return report
        except Exception as e:
            self.logger.error(f"Error generating user security report: {str(e)}")
            return None
    
    def get_system_security_report(self):
        """
        Get overall system security report
        """
        try:
            one_week_ago = datetime.utcnow() - timedelta(days=7)
            
            # Get system-wide statistics
            total_events = SecurityAuditLog.query.filter(
                SecurityAuditLog.timestamp >= one_week_ago
            ).count()
            
            failed_logins = SecurityAuditLog.query.filter(
                SecurityAuditLog.event_type == SecurityEventType.FAILED_LOGIN.value,
                SecurityAuditLog.timestamp >= one_week_ago
            ).count()
            
            high_risk_events = SecurityAuditLog.query.filter(
                SecurityAuditLog.risk_level == 'high',
                SecurityAuditLog.timestamp >= one_week_ago
            ).count()
            
            suspicious_activities = SecurityAuditLog.query.filter(
                SecurityAuditLog.event_type == SecurityEventType.SUSPICIOUS_ACTIVITY.value,
                SecurityAuditLog.timestamp >= one_week_ago
            ).count()
            
            # Top IPs with failed attempts
            from sqlalchemy import func
            top_failing_ips = db.session.query(
                SecurityAuditLog.ip_address,
                func.count(SecurityAuditLog.id).label('attempt_count')
            ).filter(
                SecurityAuditLog.event_type == SecurityEventType.FAILED_LOGIN.value,
                SecurityAuditLog.timestamp >= one_week_ago
            ).group_by(SecurityAuditLog.ip_address).order_by(
                func.count(SecurityAuditLog.id).desc()
            ).limit(10).all()
            
            report = {
                'period_start': one_week_ago.isoformat(),
                'period_end': datetime.utcnow().isoformat(),
                'total_security_events': total_events,
                'failed_login_attempts': failed_logins,
                'high_risk_events': high_risk_events,
                'suspicious_activities': suspicious_activities,
                'top_failing_ips': [{'ip': ip, 'count': count} for ip, count in top_failing_ips],
                'security_score': self._calculate_security_score(total_events, failed_logins, high_risk_events)
            }
            
            return report
        except Exception as e:
            self.logger.error(f"Error generating system security report: {str(e)}")
            return None
    
    def _calculate_security_score(self, total_events, failed_logins, high_risk_events):
        """
        Calculate a security score (0-100, higher is better)
        """
        if total_events == 0:
            return 100
        
        # Base score calculation
        login_success_rate = ((total_events - failed_logins) / total_events) * 100
        risk_factor = (high_risk_events / total_events) * 50  # High risk events heavily penalize score
        
        score = login_success_rate - risk_factor
        return max(0, min(100, round(score, 2)))


# Global instance
security_manager = SecurityManager()