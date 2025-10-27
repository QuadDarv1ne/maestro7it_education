from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import AuditLog, User
from app.utils.decorators import admin_required
from app import db

bp = Blueprint('audit', __name__)

@bp.route('/')
@login_required
@admin_required
def list_logs():
    """Список всех записей аудита (только для администраторов)"""
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
@admin_required
def user_logs(user_id):
    """Записи аудита для конкретного пользователя (только для администраторов)"""
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.filter_by(user_id=user_id)\
                        .order_by(AuditLog.created_at.desc())\
                        .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('audit/list.html', logs=logs, target_user=user)

@bp.route('/cleanup', methods=['POST'])
@login_required
@admin_required
def cleanup_logs():
    """Очистка старых записей аудита (только для администраторов)"""
    try:
        # Удаляем записи старше 90 дней
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=90)
        
        old_logs = AuditLog.query.filter(AuditLog.created_at < cutoff_date).all()
        count = len(old_logs)
        
        for log in old_logs:
            db.session.delete(log)
        
        db.session.commit()
        flash(f'Удалено {count} старых записей аудита')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при очистке аудита')
    
    return redirect(url_for('audit.list_logs'))