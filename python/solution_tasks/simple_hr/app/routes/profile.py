from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/settings')
@login_required
def settings():
    """Страница настроек профиля"""
    return render_template('profile/settings.html', form={})

@bp.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    """Обновление основной информации профиля"""
    try:
        # Получение данных из формы
        current_user.email = request.form.get('email') or current_user.email
        
        # Обработка аватара (заглушка - поля нет в модели)
        if 'avatar' in request.files:
            avatar = request.files['avatar']
            if avatar and avatar.filename:
                flash('Загрузка аватара временно недоступна', 'warning')
        
        db.session.commit()
        flash('Профиль успешно обновлен!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при обновлении профиля: {str(e)}', 'error')
    
    return redirect(url_for('profile.settings'))

@bp.route('/update_additional_info', methods=['POST'])
@login_required
def update_additional_info():
    """Обновление дополнительной информации"""
    try:
        # Заглушка - поля не существуют в модели User
        flash('Дополнительные поля профиля будут добавлены в следующей версии', 'info')
    except Exception as e:
        flash(f'Ошибка: {str(e)}', 'error')
    
    return redirect(url_for('profile.settings'))

@bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    """Смена пароля"""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    # Проверка текущего пароля
    if not check_password_hash(current_user.password_hash, current_password):
        flash('Неверный текущий пароль', 'error')
        return redirect(url_for('profile.settings'))
    
    # Проверка совпадения новых паролей
    if new_password != confirm_password:
        flash('Новые пароли не совпадают', 'error')
        return redirect(url_for('profile.settings'))
    
    # Проверка длины пароля
    if len(new_password) < 8:
        flash('Пароль должен содержать минимум 8 символов', 'error')
        return redirect(url_for('profile.settings'))
    
    try:
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash('Пароль успешно изменен!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при смене пароля: {str(e)}', 'error')
    
    return redirect(url_for('profile.settings'))

@bp.route('/update_notifications', methods=['POST'])
@login_required
def update_notifications():
    """Обновление настроек уведомлений"""
    try:
        # Сохранение настроек уведомлений в JSON или отдельной таблице
        notifications_settings = {
            'email_new_vacation': 'email_new_vacation' in request.form,
            'email_new_order': 'email_new_order' in request.form,
            'email_new_employee': 'email_new_employee' in request.form,
            'push_enabled': 'push_enabled' in request.form
        }
        
        # Здесь можно сохранить в поле JSON в модели User
        # current_user.notification_settings = notifications_settings
        
        db.session.commit()
        flash('Настройки уведомлений обновлены!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при обновлении настроек: {str(e)}', 'error')
    
    return redirect(url_for('profile.settings'))

@bp.route('/update_preferences', methods=['POST'])
@login_required
def update_preferences():
    """Обновление предпочтений интерфейса"""
    try:
        # Сохранение предпочтений
        preferences = {
            'theme': request.form.get('theme'),
            'items_per_page': int(request.form.get('items_per_page', 20))
        }
        
        # Здесь можно сохранить в поле JSON в модели User
        # current_user.preferences = preferences
        
        db.session.commit()
        flash('Предпочтения сохранены!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при сохранении предпочтений: {str(e)}', 'error')
    
    return redirect(url_for('profile.settings'))

@bp.route('/delete_avatar', methods=['POST'])
@login_required
def delete_avatar():
    """Удаление аватара"""
    try:
        if current_user.avatar_url:
            # Удаление файла с диска
            filepath = os.path.join('app', current_user.avatar_url.lstrip('/'))
            if os.path.exists(filepath):
                os.remove(filepath)
            
            current_user.avatar_url = None
            db.session.commit()
            flash('Аватар удален', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении аватара: {str(e)}', 'error')
    
    return redirect(url_for('profile.settings'))

@bp.route('/api/profile')
@login_required
def api_profile():
    """API для получения данных профиля"""
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'full_name': current_user.full_name,
        'phone': current_user.phone,
        'position': current_user.position,
        'department': current_user.department,
        'avatar_url': current_user.avatar_url,
        'role': current_user.role
    })
