from app.models import AuditLog
from app import db
from flask import request
from flask_login import current_user
from datetime import datetime

def log_action(action, entity_type, entity_id=None, description=None, user_id=None):
    """Логирование действия пользователя"""
    # Если пользователь не указан, используем текущего пользователя
    if user_id is None and hasattr(current_user, 'id'):
        user_id = current_user.id
    
    # Если нет пользователя, не логируем
    if user_id is None:
        return
    
    # Получаем IP адрес и user agent
    ip_address = request.remote_addr if request else None
    user_agent = request.headers.get('User-Agent') if request else None
    
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
        description=f'Создан сотрудник: {employee_name}',
        user_id=user_id
    )

def log_employee_update(employee_id, employee_name, user_id=None):
    """Логирование обновления сотрудника"""
    log_action(
        action='update',
        entity_type='employee',
        entity_id=employee_id,
        description=f'Обновлен сотрудник: {employee_name}',
        user_id=user_id
    )

def log_employee_delete(employee_id, employee_name, user_id=None):
    """Логирование удаления сотрудника"""
    log_action(
        action='delete',
        entity_type='employee',
        entity_id=employee_id,
        description=f'Удален сотрудник: {employee_name}',
        user_id=user_id
    )

def log_department_create(department_id, department_name, user_id=None):
    """Логирование создания подразделения"""
    log_action(
        action='create',
        entity_type='department',
        entity_id=department_id,
        description=f'Создано подразделение: {department_name}',
        user_id=user_id
    )

def log_department_update(department_id, department_name, user_id=None):
    """Логирование обновления подразделения"""
    log_action(
        action='update',
        entity_type='department',
        entity_id=department_id,
        description=f'Обновлено подразделение: {department_name}',
        user_id=user_id
    )

def log_department_delete(department_id, department_name, user_id=None):
    """Логирование удаления подразделения"""
    log_action(
        action='delete',
        entity_type='department',
        entity_id=department_id,
        description=f'Удалено подразделение: {department_name}',
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
        description=f'Создан {vacation_type_name} отпуск для сотрудника {employee_name}, начиная с {start_date}',
        user_id=user_id
    )

def log_user_login(user_id, username):
    """Логирование входа пользователя"""
    log_action(
        action='login',
        entity_type='user',
        entity_id=user_id,
        description=f'Пользователь {username} вошел в систему',
        user_id=user_id
    )

def log_user_logout(user_id, username):
    """Логирование выхода пользователя"""
    log_action(
        action='logout',
        entity_type='user',
        entity_id=user_id,
        description=f'Пользователь {username} вышел из системы',
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