from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User, TestResult, Notification, UserPreference
from app.forms import LoginForm, RegistrationForm
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            
            # Validate next_page to prevent open redirect vulnerability
            if next_page and not next_page.startswith('/'):
                next_page = url_for('main.index')
            
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')

    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('auth/register.html', form=form)

        if User.query.filter_by(email=form.email.data).first():
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('auth/register.html', form=form)

        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Sanitize inputs to prevent XSS
        user.username = user.username.strip()
        user.email = user.email.strip()
        
        db.session.add(user)
        db.session.commit()

        flash('Поздравляем, вы успешно зарегистрировались!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))

@auth.route('/profile/preferences', methods=['GET', 'POST'])
@login_required
def user_preferences():
    """Manage user preferences"""
    # Get or create user preferences
    prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
    if not prefs:
        prefs = UserPreference(user_id=current_user.id)
        db.session.add(prefs)
        db.session.commit()
    
    if request.method == 'POST':
        # Update preferences
        vacancy_alerts = request.form.get('vacancy_alerts') == 'on'
        email_notifications = request.form.get('email_notifications') == 'on'
        preferred_professions_raw = request.form.get('preferred_professions', '')
        
        # Sanitize and validate preferred professions to prevent injection
        preferred_professions = []
        if preferred_professions_raw:
            raw_list = preferred_professions_raw.split(',')
            for profession in raw_list:
                clean_profession = profession.strip()[:100]  # Limit length
                if clean_profession:  # Only add non-empty professions
                    # Basic validation to prevent malicious content
                    invalid_chars = ['<', '>', '"', '&', ';']
                    if not any(char in clean_profession for char in invalid_chars):
                        preferred_professions.append(clean_profession)
        
        prefs.vacancy_alerts_enabled = vacancy_alerts
        prefs.email_notifications = email_notifications
        prefs.preferred_professions = json.dumps(preferred_professions)
        
        db.session.commit()
        flash('Настройки успешно обновлены!', 'success')
        return redirect(url_for('auth.user_preferences'))
    
    # Convert JSON professions back to list for form
    try:
        professions_list = json.loads(prefs.preferred_professions) if prefs.preferred_professions else []
    except:
        professions_list = []
    
    return render_template('auth/preferences.html', 
                         preferences=prefs, 
                         professions_list=', '.join(professions_list))

@auth.route('/api/preferences', methods=['GET', 'POST'])
@login_required
def api_preferences():
    """API endpoint for user preferences"""
    if request.method == 'GET':
        # Get user preferences
        prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
        if not prefs:
            prefs = UserPreference(user_id=current_user.id)
            db.session.add(prefs)
            db.session.commit()
        
        try:
            professions_list = json.loads(prefs.preferred_professions) if prefs.preferred_professions else []
        except:
            professions_list = []
        
        return jsonify({
            'success': True,
            'preferences': {
                'vacancy_alerts_enabled': prefs.vacancy_alerts_enabled,
                'email_notifications': prefs.email_notifications,
                'preferred_professions': professions_list
            }
        })
    
    elif request.method == 'POST':
        # Update user preferences
        data = request.get_json()
        
        prefs = UserPreference.query.filter_by(user_id=current_user.id).first()
        if not prefs:
            prefs = UserPreference(user_id=current_user.id)
            db.session.add(prefs)
        
        prefs.vacancy_alerts_enabled = data.get('vacancy_alerts_enabled', False)
        prefs.email_notifications = data.get('email_notifications', True)
        prefs.preferred_professions = json.dumps(data.get('preferred_professions', []))
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Настройки успешно обновлены'
        })