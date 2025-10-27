from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User
from app.forms import UserForm
from app.utils.backup import list_backups, backup_database, cleanup_old_backups
from app.utils.decorators import admin_required
from app import db

bp = Blueprint('admin', __name__)

@bp.route('/')
@login_required
@admin_required
def index():
    """Панель администратора"""
    users = User.query.all()
    return render_template('admin/index.html', users=users)

@bp.route('/users')
@login_required
@admin_required
def list_users():
    """Список пользователей"""
    users = User.query.all()
    return render_template('admin/users/list.html', users=users)

@bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    """Создание нового пользователя"""
    form = UserForm()
    if form.validate_on_submit():
        # Проверяем, существует ли пользователь с таким именем или email
        if User.query.filter_by(username=form.username.data).first():
            flash('Пользователь с таким именем уже существует')
            return render_template('admin/users/form.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Пользователь с таким email уже существует')
            return render_template('admin/users/form.html', form=form)
        
        # Создаем нового пользователя
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Пользователь успешно создан')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании пользователя')
            return render_template('admin/users/form.html', form=form)
    
    return render_template('admin/users/form.html', form=form)

@bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(id):
    """Редактирование пользователя"""
    user = User.query.get_or_404(id)
    
    # Нельзя редактировать самого себя
    if user.id == current_user.id:
        flash('Вы не можете редактировать自己的 профиль через панель администратора')
        return redirect(url_for('admin.list_users'))
    
    form = UserForm(obj=user)
    
    # Убираем валидацию пароля при редактировании (если не указан новый пароль)
    if request.method == 'GET':
        form.password.data = ''
    
    if form.validate_on_submit():
        # Проверяем уникальность имени пользователя и email
        if User.query.filter(User.username == form.username.data, User.id != user.id).first():
            flash('Пользователь с таким именем уже существует')
            return render_template('admin/users/form.html', form=form, user=user)
        
        if User.query.filter(User.email == form.email.data, User.id != user.id).first():
            flash('Пользователь с таким email уже существует')
            return render_template('admin/users/form.html', form=form, user=user)
        
        # Обновляем данные пользователя
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        
        # Обновляем пароль, если он был указан
        if form.password.data:
            user.set_password(form.password.data)
        
        try:
            db.session.commit()
            flash('Пользователь успешно обновлен')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении пользователя')
            return render_template('admin/users/form.html', form=form, user=user)
    
    return render_template('admin/users/form.html', form=form, user=user)

@bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_user(id):
    """Удаление пользователя"""
    user = User.query.get_or_404(id)
    
    # Нельзя удалить самого себя
    if user.id == current_user.id:
        flash('Вы не можете удалить自己的 профиль')
        return redirect(url_for('admin.list_users'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('Пользователь успешно удален')
    except Exception as e:
        db.session.rollback()
        flash('Ошибка при удалении пользователя')
    
    return redirect(url_for('admin.list_users'))

@bp.route('/backup')
@login_required
@admin_required
def backup():
    """Резервное копирование данных"""
    from app.utils.backup import list_backups, backup_database
    backups = list_backups()
    return render_template('admin/backup.html', backups=backups)

@bp.route('/backup/create')
@login_required
@admin_required
def create_backup():
    """Создание резервной копии"""
    from app.utils.backup import backup_database
    try:
        result = backup_database()
        flash(f'Резервная копия успешно создана: {result["timestamp"]}')
    except Exception as e:
        flash(f'Ошибка при создании резервной копии: {str(e)}')
    
    return redirect(url_for('admin.backup'))

@bp.route('/backup/cleanup')
@login_required
@admin_required
def cleanup_backups():
    """Очистка старых резервных копий"""
    from app.utils.backup import cleanup_old_backups
    try:
        deleted_count = cleanup_old_backups()
        flash(f'Удалено старых резервных копий: {deleted_count}')
    except Exception as e:
        flash(f'Ошибка при очистке резервных копий: {str(e)}')
    
    return redirect(url_for('admin.backup'))