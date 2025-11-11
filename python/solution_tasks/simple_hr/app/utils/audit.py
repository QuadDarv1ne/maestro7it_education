from app.models import AuditLog
from app import db
from flask import request
from flask_login import current_user
from datetime import datetime, timedelta
import hashlib
import re
import logging

# Set up logging
logger = logging.getLogger(__name__)

def sanitize_input(text):
    """Sanitize user input to prevent XSS and other attacks"""
    if not text:
        return text
    
    # Remove potentially dangerous characters
    # Allow only safe characters: letters, numbers, spaces, and common punctuation
    sanitized = re.sub(r'[<>"\']', '', str(text))
    return sanitized.strip()

def get_client_ip():
    """Get real client IP address considering proxies"""
    if request:
        # Check for forwarded IP (from proxy/load balancer)
        forwarded = request.headers.get('X-Forwarded-For')
        if forwarded:
            # Get the first IP in the list (client IP)
            ip = forwarded.split(',')[0].strip()
            if is_valid_ip(ip):
                return ip
        
        # Check for real IP header
        real_ip = request.headers.get('X-Real-IP')
        if real_ip and is_valid_ip(real_ip):
            return real_ip
        
        # Fallback to remote_addr
        return request.remote_addr
    return None

def is_valid_ip(ip):
    """Validate IP address format"""
    if not ip:
        return False
    
    # IPv4 validation
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipv4_pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    # IPv6 validation (simplified)
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    if re.match(ipv6_pattern, ip):
        return True
    
    return False

def hash_sensitive_data(data):
    """Hash sensitive data for secure logging"""
    if not data:
        return None
    return hashlib.sha256(str(data).encode('utf-8')).hexdigest()

def log_action(action, entity_type, entity_id=None, description=None, user_id=None, sensitive_data=None):
    """Логирование действия пользователя с дополнительными мерами безопасности"""
    try:
        # Если пользователь не указан, используем текущего пользователя
        if user_id is None and hasattr(current_user, 'id'):
            user_id = current_user.id
        
        # Если нет пользователя, не логируем
        if user_id is None:
            return
        
        # Санитизация входных данных
        action = sanitize_input(action)
        entity_type = sanitize_input(entity_type)
        description = sanitize_input(description) if description else None
        
        # Хэширование чувствительных данных
        if sensitive_data:
            hashed_data = hash_sensitive_data(sensitive_data)
            if description:
                description += f" [Хэш: {hashed_data}]"
            else:
                description = f"[Хэш: {hashed_data}]"
        
        # Получаем реальный IP адрес клиента
        ip_address = get_client_ip()
        
        # Ограничиваем длину user agent
        user_agent = request.headers.get('User-Agent') if request else None
        if user_agent and len(user_agent) > 500:
            user_agent = user_agent[:500]
        
        # Создаем запись аудита
        audit_log = AuditLog()
        audit_log.user_id = user_id
        audit_log.action = action
        audit_log.entity_type = entity_type
        audit_log.entity_id = entity_id
        audit_log.description = description
        audit_log.ip_address = ip_address
        audit_log.user_agent = user_agent
        audit_log.created_at = datetime.utcnow()
        
        db.session.add(audit_log)
        db.session.commit()
        return audit_log
    except Exception as e:
        db.session.rollback()
        logger.error(f"Ошибка при логировании действия: {e}")
        return None

def log_employee_create(employee_id, employee_name, user_id=None):
    """Логирование создания сотрудника"""
    return log_action(
        action='create',
        entity_type='employee',
        entity_id=employee_id,
        description=f'Создан сотрудник: {sanitize_input(employee_name)}',
        user_id=user_id
    )

def log_employee_update(employee_id, employee_name, user_id=None):
    """Логирование обновления сотрудника"""
    return log_action(
        action='update',
        entity_type='employee',
        entity_id=employee_id,
        description=f'Обновлен сотрудник: {sanitize_input(employee_name)}',
        user_id=user_id
    )

def log_employee_delete(employee_id, employee_name, user_id=None):
    """Логирование удаления сотрудника"""
    return log_action(
        action='delete',
        entity_type='employee',
        entity_id=employee_id,
        description=f'Удален сотрудник: {sanitize_input(employee_name)}',
        user_id=user_id
    )

def log_department_create(department_id, department_name, user_id=None):
    """Логирование создания подразделения"""
    return log_action(
        action='create',
        entity_type='department',
        entity_id=department_id,
        description=f'Создано подразделение: {sanitize_input(department_name)}',
        user_id=user_id
    )

def log_department_update(department_id, department_name, user_id=None):
    """Логирование обновления подразделения"""
    return log_action(
        action='update',
        entity_type='department',
        entity_id=department_id,
        description=f'Обновлено подразделение: {sanitize_input(department_name)}',
        user_id=user_id
    )

def log_department_delete(department_id, department_name, user_id=None):
    """Логирование удаления подразделения"""
    return log_action(
        action='delete',
        entity_type='department',
        entity_id=department_id,
        description=f'Удалено подразделение: {sanitize_input(department_name)}',
        user_id=user_id
    )

def log_vacation_create(vacation_id, employee_name, vacation_type, start_date, user_id=None):
    """Логирование создания отпуска"""
    vacation_type_name = {
        'paid': 'оплачиваемый',
        'unpaid': 'неоплачиваемый',
        'sick': 'больничный'
    }.get(vacation_type, 'отпуск')
    
    return log_action(
        action='create',
        entity_type='vacation',
        entity_id=vacation_id,
        description=f'Создан {vacation_type_name} отпуск для сотрудника {sanitize_input(employee_name)}, начиная с {start_date}',
        user_id=user_id
    )

def log_user_login(user_id, username):
    """Логирование входа пользователя"""
    return log_action(
        action='login',
        entity_type='user',
        entity_id=user_id,
        description=f'Пользователь {sanitize_input(username)} вошел в систему',
        user_id=user_id
    )

def log_user_logout(user_id, username):
    """Логирование выхода пользователя"""
    return log_action(
        action='logout',
        entity_type='user',
        entity_id=user_id,
        description=f'Пользователь {sanitize_input(username)} вышел из системы',
        user_id=user_id
    )

def get_user_audit_logs(user_id, limit=50):
    """Получение логов аудита для пользователя"""
    try:
        return AuditLog.query.filter_by(user_id=user_id)\
                            .order_by(AuditLog.created_at.desc())\
                            .limit(limit)\
                            .all()
    except Exception as e:
        logger.error(f"Error getting user audit logs: {str(e)}")
        return []

def get_entity_audit_logs(entity_type, entity_id, limit=50):
    """Получение логов аудита для сущности"""
    try:
        return AuditLog.query.filter_by(entity_type=entity_type, entity_id=entity_id)\
                            .order_by(AuditLog.created_at.desc())\
                            .limit(limit)\
                            .all()
    except Exception as e:
        logger.error(f"Error getting entity audit logs: {str(e)}")
        return []

def get_recent_audit_logs(limit=100):
    """Получение последних записей аудита"""
    try:
        return AuditLog.query.order_by(AuditLog.created_at.desc())\
                            .limit(limit)\
                            .all()
    except Exception as e:
        logger.error(f"Error getting recent audit logs: {str(e)}")
        return []

def cleanup_old_audit_logs(days=90):
    """Очистка старых записей аудита (по умолчанию старше 90 дней)"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        old_logs = AuditLog.query.filter(AuditLog.created_at < cutoff_date).all()
        count = len(old_logs)
        
        for log in old_logs:
            db.session.delete(log)
        
        db.session.commit()
        return count
    except Exception as e:
        logger.error(f"Error cleaning up old audit logs: {str(e)}")
        db.session.rollback()
        return 0

# New enhanced audit functions

def get_audit_logs_by_action(action, limit=50):
    """Получение логов аудита по типу действия"""
    try:
        return AuditLog.query.filter_by(action=action)\
                            .order_by(AuditLog.created_at.desc())\
                            .limit(limit)\
                            .all()
    except Exception as e:
        logger.error(f"Error getting audit logs by action: {str(e)}")
        return []

def get_audit_logs_by_date_range(start_date, end_date):
    """Получение логов аудита за период"""
    try:
        return AuditLog.query.filter(AuditLog.created_at >= start_date)\
                            .filter(AuditLog.created_at <= end_date)\
                            .order_by(AuditLog.created_at.desc())\
                            .all()
    except Exception as e:
        logger.error(f"Error getting audit logs by date range: {str(e)}")
        return []

def get_audit_statistics():
    """Получение статистики аудита"""
    try:
        total_logs = AuditLog.query.count()
        
        # Статистика по действиям
        action_stats = {}
        actions = db.session.query(AuditLog.action, db.func.count(AuditLog.action))\
                           .group_by(AuditLog.action)\
                           .all()
        for action, count in actions:
            action_stats[action] = count
        
        # Статистика по типам сущностей
        entity_stats = {}
        entities = db.session.query(AuditLog.entity_type, db.func.count(AuditLog.entity_type))\
                            .group_by(AuditLog.entity_type)\
                            .all()
        for entity_type, count in entities:
            entity_stats[entity_type] = count
        
        # Статистика по пользователям
        user_stats = {}
        users = db.session.query(AuditLog.user_id, db.func.count(AuditLog.user_id))\
                         .group_by(AuditLog.user_id)\
                         .all()
        for user_id, count in users:
            user_stats[user_id] = count
        
        return {
            'total_logs': total_logs,
            'action_stats': action_stats,
            'entity_stats': entity_stats,
            'user_stats': user_stats
        }
    except Exception as e:
        logger.error(f"Error getting audit statistics: {str(e)}")
        return {
            'total_logs': 0,
            'action_stats': {},
            'entity_stats': {},
            'user_stats': {}
        }

def search_audit_logs(query_string, limit=50):
    """Поиск логов аудита по строке запроса"""
    try:
        return AuditLog.query.filter(
            AuditLog.description.contains(query_string) |
            AuditLog.action.contains(query_string) |
            AuditLog.entity_type.contains(query_string)
        ).order_by(AuditLog.created_at.desc()).limit(limit).all()
    except Exception as e:
        logger.error(f"Error searching audit logs: {str(e)}")
        return []

def export_audit_logs_to_csv(filename, days=30):
    """Экспорт логов аудита в CSV файл"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        logs = AuditLog.query.filter(AuditLog.created_at >= cutoff_date)\
                            .order_by(AuditLog.created_at.desc())\
                            .all()
        
        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['timestamp', 'user_id', 'action', 'entity_type', 'entity_id', 'description', 'ip_address']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for log in logs:
                writer.writerow({
                    'timestamp': log.created_at.isoformat(),
                    'user_id': log.user_id,
                    'action': log.action,
                    'entity_type': log.entity_type,
                    'entity_id': log.entity_id,
                    'description': log.description,
                    'ip_address': log.ip_address
                })
        
        return len(logs)
    except Exception as e:
        logger.error(f"Error exporting audit logs to CSV: {str(e)}")
        return 0

def get_user_activity_summary(user_id, days=30):
    """Получение сводки активности пользователя за период"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        logs = AuditLog.query.filter_by(user_id=user_id)\
                            .filter(AuditLog.created_at >= cutoff_date)\
                            .order_by(AuditLog.created_at.desc())\
                            .all()
        
        # Группируем по действиям
        action_summary = {}
        for log in logs:
            if log.action in action_summary:
                action_summary[log.action] += 1
            else:
                action_summary[log.action] = 1
        
        # Группируем по типам сущностей
        entity_summary = {}
        for log in logs:
            if log.entity_type in entity_summary:
                entity_summary[log.entity_type] += 1
            else:
                entity_summary[log.entity_type] = 1
        
        return {
            'total_actions': len(logs),
            'action_summary': action_summary,
            'entity_summary': entity_summary,
            'period_days': days
        }
    except Exception as e:
        logger.error(f"Error getting user activity summary: {str(e)}")
        return {
            'total_actions': 0,
            'action_summary': {},
            'entity_summary': {},
            'period_days': days
        }