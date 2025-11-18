from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user
from app.models import User
from app import db
import io
import qrcode
from base64 import b64encode

bp = Blueprint('two_factor', __name__, url_prefix='/2fa')

@bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup():
    """Настройка двухфакторной аутентификации"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'enable':
            # Генерируем секрет и резервные коды
            current_user.generate_totp_secret()
            backup_codes = current_user.generate_backup_codes()
            db.session.commit()
            
            # Сохраняем коды в сессии для отображения
            session['backup_codes'] = backup_codes
            
            return render_template('two_factor/setup_codes.html', 
                                 backup_codes=backup_codes,
                                 qr_code=generate_qr_code(current_user.get_totp_uri()))
        
        elif action == 'verify':
            token = request.form.get('token')
            if current_user.verify_totp(token):
                current_user.totp_enabled = True
                db.session.commit()
                flash('Двухфакторная аутентификация успешно включена!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Неверный код. Попробуйте еще раз.', 'danger')
    
    # GET запрос - показываем форму настройки
    if current_user.totp_enabled:
        return render_template('two_factor/manage.html')
    
    return render_template('two_factor/setup.html')

@bp.route('/disable', methods=['POST'])
@login_required
def disable():
    """Отключение двухфакторной аутентификации"""
    password = request.form.get('password')
    
    if not current_user.check_password(password):
        flash('Неверный пароль', 'danger')
        return redirect(url_for('two_factor.setup'))
    
    current_user.totp_enabled = False
    current_user.totp_secret = None
    current_user.backup_codes = None
    db.session.commit()
    
    flash('Двухфакторная аутентификация отключена', 'info')
    return redirect(url_for('main.index'))

@bp.route('/verify', methods=['GET', 'POST'])
def verify():
    """Проверка кода 2FA при входе"""
    if 'user_id_2fa' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        user = User.query.get(session['user_id_2fa'])
        if not user:
            return redirect(url_for('auth.login'))
        
        token = request.form.get('token')
        use_backup = request.form.get('use_backup') == 'true'
        
        verified = False
        if use_backup:
            verified = user.verify_backup_code(token)
            if verified:
                db.session.commit()
                flash('Резервный код использован. Рекомендуем сгенерировать новые коды.', 'warning')
        else:
            verified = user.verify_totp(token)
        
        if verified:
            from flask_login import login_user
            login_user(user)
            session.pop('user_id_2fa', None)
            
            from app.utils.audit import log_user_login
            log_user_login(user.id, user.username)
            
            next_page = session.pop('next_page_2fa', None)
            return redirect(next_page if next_page else url_for('main.index'))
        else:
            flash('Неверный код', 'danger')
    
    return render_template('two_factor/verify.html')

@bp.route('/regenerate-codes', methods=['POST'])
@login_required
def regenerate_codes():
    """Регенерация резервных кодов"""
    if not current_user.totp_enabled:
        return jsonify({'error': 'Двухфакторная аутентификация не включена'}), 400
    
    password = request.form.get('password')
    if not current_user.check_password(password):
        return jsonify({'error': 'Неверный пароль'}), 403
    
    backup_codes = current_user.generate_backup_codes()
    db.session.commit()
    
    return jsonify({'backup_codes': backup_codes})

def generate_qr_code(data):
    """Генерация QR-кода для TOTP URI"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return b64encode(buf.getvalue()).decode()
