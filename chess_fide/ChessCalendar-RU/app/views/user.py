from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app import db
from app.models.user import User
from app.models.tournament import Tournament
from app.models.favorite import FavoriteTournament
from app.repositories import TournamentRepository, FavoriteRepository
from app.utils.notifications import notification_service
from datetime import datetime
import re

user_bp = Blueprint('user', __name__, url_prefix='/user')

def validate_email(email):
    """Проверка корректности email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Проверка надежности пароля"""
    if len(password) < 8:
        return False, "Пароль должен содержать не менее 8 символов"
    if not re.search(r'[A-Za-z]', password):
        return False, "Пароль должен содержать буквы"
    if not re.search(r'\d', password):
        return False, "Пароль должен содержать цифры"
    if not re.search(r'[!@#$%^&*(),.?":{}|<>\[\]]', password):
        return False, "Пароль должен содержать хотя бы один специальный символ (!@#$%^&*(),.?\":{}|<>[])"
    if re.search(r'(.)\1{2,}', password):  # Check for repeated characters
        return False, "Пароль не должен содержать повторяющиеся символы подряд"
    return True, "Пароль корректный"

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Проверка данных
        if not username or not email or not password:
            flash('Все поля обязательны для заполнения', 'error')
            return render_template('user/register.html')
        
        if password != confirm_password:
            flash('Пароли не совпадают', 'error')
            return render_template('user/register.html')
        
        # Проверка email
        if not validate_email(email):
            flash('Некорректный email адрес', 'error')
            return render_template('user/register.html')
        
        # Проверка пароля
        is_valid, msg = validate_password(password)
        if not is_valid:
            flash(msg, 'error')
            return render_template('user/register.html')
        
        # Проверка, существует ли уже пользователь
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Пользователь с таким именем или email уже существует', 'error')
            return render_template('user/register.html')
        
        try:
            # Создание нового пользователя
            user = User(username=username, email=email, password=password, is_admin=False, is_regular_user=True)
            db.session.add(user)
            db.session.commit()
            
            # Автоматический вход после регистрации
            session['user_id'] = user.id
            session['username'] = user.username
            
            flash('Регистрация успешна! Добро пожаловать!', 'success')
            return redirect(url_for('main.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Ошибка при регистрации: {e}', 'error')
    
    return render_template('user/register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Вход пользователя"""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_regular_user and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash('Вы успешно вошли в систему', 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('main.index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'error')
    
    return render_template('user/login.html')

@user_bp.route('/logout')
def logout():
    """Выход пользователя"""
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('main.index'))

@user_bp.route('/profile')
def profile():
    """Профиль пользователя"""
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('user.login'))
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_regular_user:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.index'))
    
    # Получаем настройки уведомлений пользователя
    subscription = notification_service.get_subscription(user.email)
    preferences = subscription.preferences if subscription else {}
    
    return render_template('user/profile.html', user=user, preferences=preferences)

@user_bp.route('/profile/update', methods=['POST'])
def update_profile():
    """Обновление профиля пользователя"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_regular_user:
        return jsonify({'status': 'error', 'message': 'Access denied'}), 403
    
    try:
        # Обновление основных данных профиля
        new_username = request.form.get('username', '').strip()
        new_email = request.form.get('email', '').strip()
        
        # Проверка email
        if new_email and not validate_email(new_email):
            return jsonify({'status': 'error', 'message': 'Некорректный email адрес'}), 400
        
        # Проверка уникальности email (если он изменяется)
        if new_email and new_email != user.email:
            existing_user = User.query.filter(User.email == new_email, User.id != user.id).first()
            if existing_user:
                return jsonify({'status': 'error', 'message': 'Email уже используется другим пользователем'}), 400
        
        # Обновление данных
        if new_username:
            user.username = new_username
        if new_email:
            user.email = new_email
        
        db.session.commit()
        
        # Обновляем сессию, если имя пользователя изменилось
        if new_username:
            session['username'] = new_username
        
        return jsonify({'status': 'success', 'message': 'Профиль успешно обновлен'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Ошибка при обновлении профиля: {e}'}), 500

@user_bp.route('/change-password', methods=['POST'])
def change_password():
    """Смена пароля"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_regular_user:
        return jsonify({'status': 'error', 'message': 'Access denied'}), 403
    
    current_password = request.form.get('current_password', '')
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Проверка текущего пароля
    if not user.check_password(current_password):
        return jsonify({'status': 'error', 'message': 'Текущий пароль указан неверно'}), 400
    
    # Проверка новых паролей
    if new_password != confirm_password:
        return jsonify({'status': 'error', 'message': 'Новые пароли не совпадают'}), 400
    
    # Проверка надежности нового пароля
    is_valid, msg = validate_password(new_password)
    if not is_valid:
        return jsonify({'status': 'error', 'message': msg}), 400
    
    try:
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Пароль успешно изменен'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Ошибка при смене пароля: {e}'}), 500

@user_bp.route('/favorites')
def favorites():
    """Просмотр избранных турниров пользователя"""
    if 'user_id' not in session:
        flash('Пожалуйста, войдите в систему', 'warning')
        return redirect(url_for('user.login'))
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_regular_user:
        flash('Доступ запрещен', 'error')
        return redirect(url_for('main.index'))
    
    # Получаем избранные турниры пользователя через репозиторий
    favorite_tournaments = FavoriteRepository.get_user_favorite_tournaments(user.id)
    
    return render_template('user/favorites.html', favorite_tournaments=favorite_tournaments)

@user_bp.route('/favorites/toggle/<int:tournament_id>', methods=['POST'])
def toggle_favorite(tournament_id):
    """Добавить/удалить турнир из избранного"""
    if 'user_id' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_regular_user:
        return jsonify({'status': 'error', 'message': 'Access denied'}), 403
    
    try:
        # Проверяем существование турнира через репозиторий
        tournament = TournamentRepository.get_by_id(tournament_id)
        if not tournament:
            return jsonify({'status': 'error', 'message': 'Турнир не найден'}), 404
        
        # Используем метод toggle из репозитория
        is_favorite, message = FavoriteRepository.toggle_favorite(user.id, tournament_id)
        
        return jsonify({
            'status': 'success',
            'message': message,
            'is_favorite': is_favorite
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'Ошибка при работе с избранным: {str(e)}'}), 500

@user_bp.route('/favorites/check/<int:tournament_id>')
def check_favorite(tournament_id):
    """Проверить, находится ли турнир в избранном у пользователя"""
    if 'user_id' not in session:
        return jsonify({'is_favorite': False}), 200
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_regular_user:
        return jsonify({'is_favorite': False}), 200
    
    # Используем метод репозитория для проверки
    is_favorite = FavoriteRepository.is_favorite(user.id, tournament_id)
    
    return jsonify({'is_favorite': is_favorite}), 200