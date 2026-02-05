# -*- coding: utf-8 -*-
"""
Advanced Structured Logging System
Provides comprehensive logging with structured data, analysis, and monitoring
"""
import logging
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum
from collections import defaultdict, deque
from threading import Lock, Thread
import re
from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

class LogLevel(Enum):
    """Log level enumeration"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class LogCategory(Enum):
    """Log category enumeration"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    DATABASE = "database"
    API = "api"
    AUTHENTICATION = "authentication"
    BUSINESS_LOGIC = "business_logic"
    SYSTEM = "system"
    EXTERNAL_SERVICE = "external_service"

@dataclass
class LogEntry:
    """Structured log entry"""
    timestamp: float
    level: LogLevel
    category: LogCategory
    message: str
    module: str
    function: str
    line_number: int
    context: Dict[str, Any]
    trace_id: Optional[str]
    user_id: Optional[int]
    ip_address: Optional[str]
    session_id: Optional[str]
    duration_ms: Optional[float]
    error_details: Optional[Dict[str, Any]]

class LogAnalyzer:
    """Advanced log analysis system"""
    
    def __init__(self, max_entries: int = 10000):
        self.max_entries = max_entries
        self.log_entries: deque = deque(maxlen=max_entries)
        self.lock = Lock()
        self.patterns = self._initialize_patterns()
        self.anomaly_detectors = self._initialize_anomaly_detectors()
    
    def _initialize_patterns(self) -> Dict[str, Any]:
        """Initialize log analysis patterns"""
        return {
            'error_patterns': [
                r'exception|error|failure|timeout|connection refused',
                r'invalid|unauthorized|forbidden|denied',
                r'out of memory|disk full|resource exhausted'
            ],
            'warning_patterns': [
                r'warning|deprecated|slow query|high latency',
                r'retry|fallback|degraded|throttled'
            ],
            'security_patterns': [
                r'login|logout|authentication|authorization',
                r'permission|access|privilege|role'
            ]
        }
    
    def _initialize_anomaly_detectors(self) -> Dict[str, Any]:
        """Initialize anomaly detection rules"""
        return {
            'high_error_rate': {
                'threshold': 0.05,  # 5% error rate
                'window_minutes': 5,
                'enabled': True
            },
            'suspicious_activity': {
                'failed_login_threshold': 10,
                'window_minutes': 15,
                'enabled': True
            },
            'performance_degradation': {
                'latency_threshold_ms': 1000,
                'error_rate_threshold': 0.02,
                'enabled': True
            }
        }
    
    def add_log_entry(self, entry: LogEntry):
        """Add log entry to analyzer"""
        with self.lock:
            self.log_entries.append(entry)
    
    def analyze_logs(self, hours: int = 1) -> Dict[str, Any]:
        """Analyze logs for patterns and anomalies"""
        try:
            cutoff_time = time.time() - (hours * 3600)
            recent_logs = [entry for entry in self.log_entries if entry.timestamp > cutoff_time]
            
            if not recent_logs:
                return {'message': 'No logs found in the specified time period'}
            
            analysis = {
                'time_period_hours': hours,
                'total_entries': len(recent_logs),
                'entries_by_level': self._count_by_level(recent_logs),
                'entries_by_category': self._count_by_category(recent_logs),
                'error_rate': self._calculate_error_rate(recent_logs),
                'performance_metrics': self._analyze_performance(recent_logs),
                'security_events': self._analyze_security(recent_logs),
                'anomalies': self._detect_anomalies(recent_logs),
                'top_modules': self._get_top_modules(recent_logs),
                'trends': self._analyze_trends(recent_logs)
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing logs: {e}")
            return {'error': str(e)}
    
    def _count_by_level(self, logs: List[LogEntry]) -> Dict[str, int]:
        """Count log entries by level"""
        counts = defaultdict(int)
        for log in logs:
            counts[log.level.value] += 1
        return dict(counts)
    
    def _count_by_category(self, logs: List[LogEntry]) -> Dict[str, int]:
        """Count log entries by category"""
        counts = defaultdict(int)
        for log in logs:
            counts[log.category.value] += 1
        return dict(counts)
    
    def _calculate_error_rate(self, logs: List[LogEntry]) -> float:
        """Calculate error rate"""
        error_levels = {LogLevel.ERROR, LogLevel.CRITICAL}
        error_count = sum(1 for log in logs if log.level in error_levels)
        return error_count / len(logs) if logs else 0.0
    
    def _analyze_performance(self, logs: List[LogEntry]) -> Dict[str, Any]:
        """Analyze performance-related logs"""
        perf_logs = [log for log in logs if log.category == LogCategory.PERFORMANCE and log.duration_ms is not None]
        
        if not perf_logs:
            return {'message': 'No performance data available'}
        
        durations = [log.duration_ms for log in perf_logs]
        return {
            'total_operations': len(perf_logs),
            'avg_duration_ms': sum(durations) / len(durations),
            'max_duration_ms': max(durations),
            'min_duration_ms': min(durations),
            'slow_operations': len([d for d in durations if d > 1000]),  # Operations > 1 second
            'percentiles': {
                'p50': self._percentile(durations, 50),
                'p90': self._percentile(durations, 90),
                'p95': self._percentile(durations, 95),
                'p99': self._percentile(durations, 99)
            }
        }
    
    def _analyze_security(self, logs: List[LogEntry]) -> Dict[str, Any]:
        """Analyze security-related logs"""
        security_logs = [log for log in logs if log.category == LogCategory.SECURITY]
        
        if not security_logs:
            return {'message': 'No security events found'}
        
        # Count different types of security events
        event_types = defaultdict(int)
        failed_logins = 0
        successful_logins = 0
        
        for log in security_logs:
            message_lower = log.message.lower()
            if 'failed' in message_lower or 'invalid' in message_lower:
                failed_logins += 1
                event_types['failed_login'] += 1
            elif 'successful' in message_lower or 'logged in' in message_lower:
                successful_logins += 1
                event_types['successful_login'] += 1
            elif 'logout' in message_lower:
                event_types['logout'] += 1
            elif 'permission' in message_lower or 'access denied' in message_lower:
                event_types['access_denied'] += 1
            else:
                event_types['other'] += 1
        
        return {
            'total_security_events': len(security_logs),
            'failed_logins': failed_logins,
            'successful_logins': successful_logins,
            'login_success_rate': successful_logins / max(successful_logins + failed_logins, 1),
            'event_types': dict(event_types),
            'unique_users': len(set(log.user_id for log in security_logs if log.user_id))
        }
    
    def _detect_anomalies(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """Detect anomalies in log data"""
        anomalies = []
        
        # High error rate detection
        if self.anomaly_detectors['high_error_rate']['enabled']:
            error_rate = self._calculate_error_rate(logs)
            threshold = self.anomaly_detectors['high_error_rate']['threshold']
            if error_rate > threshold:
                anomalies.append({
                    'type': 'high_error_rate',
                    'severity': 'high',
                    'value': error_rate,
                    'threshold': threshold,
                    'message': f'Error rate {error_rate:.2%} exceeds threshold {threshold:.2%}'
                })
        
        # Suspicious activity detection
        if self.anomaly_detectors['suspicious_activity']['enabled']:
            security_logs = [log for log in logs if log.category == LogCategory.SECURITY]
            failed_logins = [log for log in security_logs if 'failed' in log.message.lower()]
            
            if len(failed_logins) > self.anomaly_detectors['suspicious_activity']['failed_login_threshold']:
                anomalies.append({
                    'type': 'suspicious_activity',
                    'severity': 'medium',
                    'value': len(failed_logins),
                    'threshold': self.anomaly_detectors['suspicious_activity']['failed_login_threshold'],
                    'message': f'High number of failed login attempts: {len(failed_logins)}'
                })
        
        # Performance degradation detection
        if self.anomaly_detectors['performance_degradation']['enabled']:
            perf_logs = [log for log in logs if log.category == LogCategory.PERFORMANCE and log.duration_ms]
            if perf_logs:
                avg_duration = sum(log.duration_ms for log in perf_logs) / len(perf_logs)
                error_rate = self._calculate_error_rate(perf_logs)
                
                if (avg_duration > self.anomaly_detectors['performance_degradation']['latency_threshold_ms'] or
                    error_rate > self.anomaly_detectors['performance_degradation']['error_rate_threshold']):
                    anomalies.append({
                        'type': 'performance_degradation',
                        'severity': 'medium',
                        'avg_duration_ms': avg_duration,
                        'error_rate': error_rate,
                        'message': 'Performance degradation detected'
                    })
        
        return anomalies
    
    def _get_top_modules(self, logs: List[LogEntry]) -> List[Dict[str, Any]]:
        """Get modules with most log entries"""
        module_counts = defaultdict(int)
        for log in logs:
            module_counts[log.module] += 1
        
        top_modules = sorted(module_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        return [{'module': module, 'count': count} for module, count in top_modules]
    
    def _analyze_trends(self, logs: List[LogEntry]) -> Dict[str, Any]:
        """Analyze log trends over time"""
        if len(logs) < 10:
            return {'message': 'Insufficient data for trend analysis'}
        
        # Group logs by hour
        hourly_counts = defaultdict(lambda: defaultdict(int))
        for log in logs:
            hour = datetime.fromtimestamp(log.timestamp).strftime('%Y-%m-%d %H:00')
            hourly_counts[hour][log.level.value] += 1
        
        # Calculate trends
        hours = sorted(hourly_counts.keys())
        if len(hours) < 2:
            return {'message': 'Insufficient time data for trend analysis'}
        
        trends = {}
        for level in LogLevel:
            counts = [hourly_counts[hour].get(level.value, 0) for hour in hours]
            if len(counts) > 1:
                # Simple trend: positive = increasing, negative = decreasing
                trend = (counts[-1] - counts[0]) / len(counts)
                trends[level.value] = {
                    'trend': trend,
                    'direction': 'increasing' if trend > 0 else 'decreasing' if trend < 0 else 'stable',
                    'first_hour': counts[0],
                    'last_hour': counts[-1]
                }
        
        return {
            'time_range': f"{hours[0]} to {hours[-1]}",
            'hourly_data_points': len(hours),
            'level_trends': trends
        }
    
    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile"""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        index = (percentile / 100) * (len(sorted_data) - 1)
        if index.is_integer():
            return sorted_data[int(index)]
        else:
            lower = sorted_data[int(index)]
            upper = sorted_data[int(index) + 1]
            return lower + (upper - lower) * (index - int(index))

class AdvancedStructuredLogger:
    """Advanced structured logging system"""
    
    def __init__(self):
        self.analyzer = LogAnalyzer()
        self.log_buffer = deque(maxlen=1000)
        self.buffer_lock = Lock()
        
    def log(self, level: LogLevel, category: LogCategory, message: str, 
            module: str = "", function: str = "", line_number: int = 0,
            context: Dict[str, Any] = None, trace_id: str = None,
            user_id: int = None, ip_address: str = None, session_id: str = None,
            duration_ms: float = None, error_details: Dict[str, Any] = None):
        """Log structured message"""
        try:
            entry = LogEntry(
                timestamp=time.time(),
                level=level,
                category=category,
                message=message,
                module=module,
                function=function,
                line_number=line_number,
                context=context or {},
                trace_id=trace_id,
                user_id=user_id,
                ip_address=ip_address,
                session_id=session_id,
                duration_ms=duration_ms,
                error_details=error_details
            )
            
            # Add to analyzer
            self.analyzer.add_log_entry(entry)
            
            # Add to buffer for immediate access
            with self.buffer_lock:
                self.log_buffer.append(entry)
            
            # Log to standard Python logger
            standard_logger = logging.getLogger(module)
            log_method = getattr(standard_logger, level.value.lower())
            
            # Create structured log message
            structured_message = self._create_structured_message(entry)
            log_method(structured_message)
            
        except Exception as e:
            # Fallback to basic logging
            basic_logger = logging.getLogger('structured_logger')
            basic_logger.error(f"Error in structured logging: {e}")
            basic_logger.info(f"Original message: {level.value} - {message}")
    
    def _create_structured_message(self, entry: LogEntry) -> str:
        """Create structured log message"""
        structured_data = {
            'timestamp': datetime.fromtimestamp(entry.timestamp).isoformat(),
            'level': entry.level.value,
            'category': entry.category.value,
            'message': entry.message,
            'module': entry.module,
            'function': entry.function,
            'line': entry.line_number
        }
        
        if entry.context:
            structured_data['context'] = entry.context
        if entry.trace_id:
            structured_data['trace_id'] = entry.trace_id
        if entry.user_id:
            structured_data['user_id'] = entry.user_id
        if entry.ip_address:
            structured_data['ip_address'] = entry.ip_address
        if entry.session_id:
            structured_data['session_id'] = entry.session_id
        if entry.duration_ms is not None:
            structured_data['duration_ms'] = entry.duration_ms
        if entry.error_details:
            structured_data['error'] = entry.error_details
        
        return json.dumps(structured_data, ensure_ascii=False)
    
    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent log entries"""
        with self.buffer_lock:
            recent = list(self.log_buffer)[-limit:]
            return [asdict(entry) for entry in recent]
    
    def get_analysis(self, hours: int = 1) -> Dict[str, Any]:
        """Get log analysis"""
        return self.analyzer.analyze_logs(hours)

# Global structured logger instance
structured_logger = AdvancedStructuredLogger()

# Flask blueprint for log management API
log_management_bp = Blueprint('log_management', __name__)

@log_management_bp.route('/api/logs/recent')
def get_recent_logs():
    """Get recent log entries"""
    try:
        limit = int(request.args.get('limit', 100))
        logs = structured_logger.get_recent_logs(limit)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'count': len(logs)
        })
    except Exception as e:
        logger.error(f"Error getting recent logs: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@log_management_bp.route('/api/logs/analysis')
def get_log_analysis():
    """Get log analysis"""
    try:
        hours = int(request.args.get('hours', 1))
        analysis = structured_logger.get_analysis(hours)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    except Exception as e:
        logger.error(f"Error getting log analysis: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@log_management_bp.route('/api/logs/search')
def search_logs():
    """Search logs by various criteria"""
    try:
        query = request.args.get('query', '')
        level = request.args.get('level')
        category = request.args.get('category')
        hours = int(request.args.get('hours', 1))
        
        # Get recent logs
        cutoff_time = time.time() - (hours * 3600)
        with structured_logger.buffer_lock:
            matching_logs = []
            for entry in structured_logger.log_buffer:
                if entry.timestamp < cutoff_time:
                    continue
                
                # Apply filters
                if level and entry.level.value != level:
                    continue
                if category and entry.category.value != category:
                    continue
                if query and query.lower() not in entry.message.lower():
                    continue
                
                matching_logs.append(asdict(entry))
        
        return jsonify({
            'success': True,
            'logs': matching_logs,
            'count': len(matching_logs),
            'query': {
                'search_term': query,
                'level': level,
                'category': category,
                'hours': hours
            }
        })
    except Exception as e:
        logger.error(f"Error searching logs: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def init_structured_logging(app):
    """Initialize structured logging system"""
    # Register blueprint
    app.register_blueprint(log_management_bp, url_prefix='/admin')
    
    # Setup log handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # File handler
    import os
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    file_handler = logging.FileHandler(os.path.join(log_dir, 'structured.log'))
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    logger.info("Advanced structured logging system initialized")
