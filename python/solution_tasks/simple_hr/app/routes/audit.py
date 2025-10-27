from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import AuditLog, User
from app.utils.audit import get_recent_audit_logs, get_user_audit_logs, cleanup_old_audit_logs
from app import db

bp = Blueprint('audit', __name__)

@bp.route('/')
@login_required
def list_logs():
    """Список всех записей аудита (только для администраторов)"""
    # Проверяем права доступа
    if current_user.role not in ['admin']:
        flash('У вас нет прав для просмотра аудита')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.created_at.desc())\
                        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('audit/list.html', logs=logs)

@bp.route('/my_logs')
@login_required
def my_logs():
    """Мои записи аудита"""
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.filter_by(user_id=current_user.id)\
                        .order_by(AuditLog.created_at.desc())\
                        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('audit/list.html', logs=logs, my_logs=True)

@bp.route('/user/<int:user_id>')
@login_required
def user_logs(user_id):
    """Записи аудита для конкретного пользователя (только для администраторов)"""
    # Проверяем права доступа
    if current_user.role not in ['admin']:
        flash('У вас нет прав для просмотра аудита других пользователей')
        return redirect(url_for('main.index'))
    
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.filter_by(user_id=user_id)\
                        .order_by(AuditLog.created_at.desc())\
                        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('audit/list.html', logs=logs, target_user=user)

@bp.route('/cleanup', methods=['POST'])
@login_required
def cleanup_logs():
    """Очистка старых записей аудита (только для администраторов)"""
    # Проверяем права доступа
    if current_user.role not in ['admin']:
        flash('У вас нет прав для очистки аудита')
        return redirect(url_for('main.index'))
    
    try:
        count = cleanup_old_audit_logs()
        flash(f'Удалено {count} старых записей аудита')
    except Exception as e:
        flash('Ошибка при очистке аудита')
    
    return redirect(url_for('audit.list_logs'))