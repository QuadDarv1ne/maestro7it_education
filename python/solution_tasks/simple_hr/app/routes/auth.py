from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
from app.utils.audit import log_user_login, log_user_logout
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            # Логируем вход
            log_user_login(user.id, user.username)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Неверный логин или пароль')
    
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Пользователь с таким именем уже существует')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Пользователь с таким email уже существует')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        user.set_password(form.password.data)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались! Теперь вы можете войти.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при регистрации')
            return render_template('register.html', form=form)
    
    return render_template('register.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы')
    return redirect(url_for('auth.login'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Generate reset token
            token = user.generate_reset_token()
            db.session.commit()
            
            # Here you would normally send an email with the reset link
            # For simplicity, we'll just show the token
            flash(f'Для восстановления пароля перейдите по ссылке: {url_for("auth.reset_password", token=token, _external=True)}')
        else:
            # Don't reveal if email exists or not (security best practice)
            pass
        
        flash('Если email существует в нашей системе, вы получите инструкции по восстановлению пароля')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password_request.html', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Неверная или просроченная ссылка для восстановления пароля')
        return redirect(url_for('auth.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Reset password
        user.reset_password(form.password.data)
        db.session.commit()
        
        flash('Ваш пароль был успешно изменен')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html', form=form)