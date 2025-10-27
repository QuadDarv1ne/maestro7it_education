from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validate input
        if not username or not password:
            flash('Пожалуйста, заполните все поля')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Неверный логин или пароль')
    
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        role = request.form.get('role', '')
        
        # Validate input
        if not username or not email or not password or not password2 or not role:
            flash('Пожалуйста, заполните все поля')
            return render_template('register.html')
        
        if password != password2:
            flash('Пароли не совпадают')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Пароль должен содержать не менее 6 символов')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует')
            return render_template('register.html')
        
        # Create new user
        user = User()
        user.username = username
        user.email = email
        user.role = role
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Вы успешно зарегистрировались! Теперь вы можете войти.')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при регистрации')
            return render_template('register.html')
    
    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы')
    return redirect(url_for('auth.login'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Пожалуйста, введите email')
            return render_template('reset_password_request.html')
        
        user = User.query.filter_by(email=email).first()
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
    
    return render_template('reset_password_request.html')

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.verify_reset_token(token):
        flash('Неверная или просроченная ссылка для восстановления пароля')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        
        # Validate input
        if not password or not password2:
            flash('Пожалуйста, заполните все поля')
            return render_template('reset_password.html')
        
        if password != password2:
            flash('Пароли не совпадают')
            return render_template('reset_password.html')
        
        if len(password) < 6:
            flash('Пароль должен содержать не менее 6 символов')
            return render_template('reset_password.html')
        
        # Reset password
        user.reset_password(password)
        db.session.commit()
        
        flash('Ваш пароль был успешно изменен')
        return redirect(url_for('auth.login'))
    
    return render_template('reset_password.html')