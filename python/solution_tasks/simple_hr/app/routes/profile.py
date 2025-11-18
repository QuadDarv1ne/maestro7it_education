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
    flash('Настройки уведомлений сохранены (в разработке)', 'info')
    return redirect(url_for('profile.settings'))

@bp.route('/update_preferences', methods=['POST'])
@login_required
def update_preferences():
    """Обновление предпочтений интерфейса"""
    flash('Предпочтения сохранены (в разработке)', 'info')
    return redirect(url_for('profile.settings'))

@bp.route('/delete_avatar', methods=['POST'])
@login_required
def delete_avatar():
    """Удаление аватара"""
    flash('Функция аватаров в разработке', 'info')
    return redirect(url_for('profile.settings'))

@bp.route('/api/profile')
@login_required
def api_profile():
    """API для получения данных профиля"""
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'role': current_user.role,
        'created_at': current_user.created_at.isoformat() if current_user.created_at else None,
        'last_login': current_user.last_login.isoformat() if current_user.last_login else None
    })
