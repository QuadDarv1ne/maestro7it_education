from app.models import AuditLog
from app import db
from flask import request
from flask_login import current_user
from datetime import datetime
import hashlib
import re

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
    
    try:
        db.session.add(audit_log)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при логировании действия: {e}")

def log_employee_create(employee_id, employee_name, user_id=None):
    """Логирование создания сотрудника"""
    log_action(
        action='create',
        entity_type='employee',
        entity_id=employee_id,
        description=f'Создан сотрудник: {sanitize_input(employee_name)}',
        user_id=user_id
    )

def log_employee_update(employee_id, employee_name, user_id=None):
    """Логирование обновления сотрудника"""
    log_action(
        action='update',
        entity_type='employee',
        entity_id=employee_id,
        description=f'Обновлен сотрудник: {sanitize_input(employee_name)}',
        user_id=user_id
    )

def log_employee_delete(employee_id, employee_name, user_id=None):
    """Логирование удаления сотрудника"""
    log_action(
        action='delete',
        entity_type='employee',
        entity_id=employee_id,
        description=f'Удален сотрудник: {sanitize_input(employee_name)}',
        user_id=user_id
    )

def log_department_create(department_id, department_name, user_id=None):
    """Логирование создания подразделения"""
    log_action(
        action='create',
        entity_type='department',
        entity_id=department_id,
        description=f'Создано подразделение: {sanitize_input(department_name)}',
        user_id=user_id
    )

def log_department_update(department_id, department_name, user_id=None):
    """Логирование обновления подразделения"""
    log_action(
        action='update',
        entity_type='department',
        entity_id=department_id,
        description=f'Обновлено подразделение: {sanitize_input(department_name)}',
        user_id=user_id
    )

def log_department_delete(department_id, department_name, user_id=None):
    """Логирование удаления подразделения"""
    log_action(
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
    
    log_action(
        action='create',
        entity_type='vacation',
        entity_id=vacation_id,
        description=f'Создан {vacation_type_name} отпуск для сотрудника {sanitize_input(employee_name)}, начиная с {start_date}',
        user_id=user_id
    )

def log_user_login(user_id, username):
    """Логирование входа пользователя"""
    log_action(
        action='login',
        entity_type='user',
        entity_id=user_id,
        description=f'Пользователь {sanitize_input(username)} вошел в систему',
        user_id=user_id
    )

def log_user_logout(user_id, username):
    """Логирование выхода пользователя"""
    log_action(
        action='logout',
        entity_type='user',
        entity_id=user_id,
        description=f'Пользователь {sanitize_input(username)} вышел из системы',
        user_id=user_id
    )

def get_user_audit_logs(user_id, limit=50):
    """Получение логов аудита для пользователя"""
    return AuditLog.query.filter_by(user_id=user_id)\
                        .order_by(AuditLog.created_at.desc())\
                        .limit(limit)\
                        .all()

def get_entity_audit_logs(entity_type, entity_id, limit=50):
    """Получение логов аудита для сущности"""
    return AuditLog.query.filter_by(entity_type=entity_type, entity_id=entity_id)\
                        .order_by(AuditLog.created_at.desc())\
                        .limit(limit)\
                        .all()

def get_recent_audit_logs(limit=100):
    """Получение последних записей аудита"""
    return AuditLog.query.order_by(AuditLog.created_at.desc())\
                        .limit(limit)\
                        .all()

def cleanup_old_audit_logs(days=90):
    """Очистка старых записей аудита (по умолчанию старше 90 дней)"""
    from datetime import timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    old_logs = AuditLog.query.filter(AuditLog.created_at < cutoff_date).all()
    count = len(old_logs)
    
    for log in old_logs:
        db.session.delete(log)
    
    db.session.commit()
    return count