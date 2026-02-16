"""
Модель для логирования административных действий
"""
from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB


class AuditLog(db.Model):
    """Лог административных действий"""
    
    __tablename__ = 'audit_log'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    action = db.Column(db.String(50), nullable=False, index=True)  # create, update, delete, login, etc.
    resource = db.Column(db.String(50), nullable=False, index=True)  # tournament, user, etc.
    resource_id = db.Column(db.Integer, nullable=True, index=True)
    details = db.Column(db.JSON, nullable=True)  # Дополнительные детали
    ip_address = db.Column(db.String(45), nullable=True)  # IPv4 или IPv6
    user_agent = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('audit_logs', lazy='dynamic'))
    
    def __repr__(self):
        return f'<AuditLog {self.id}: {self.user_id} {self.action} {self.resource}>'
    
    def to_dict(self):
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'action': self.action,
            'resource': self.resource,
            'resource_id': self.resource_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    @staticmethod
    def get_recent_actions(limit=100):
        """Получить последние действия"""
        return AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
    
    @staticmethod
    def get_user_actions(user_id, limit=100):
        """Получить действия пользователя"""
        return AuditLog.query.filter_by(user_id=user_id)\
            .order_by(AuditLog.timestamp.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_resource_history(resource, resource_id):
        """Получить историю ресурса"""
        return AuditLog.query.filter_by(
            resource=resource,
            resource_id=resource_id
        ).order_by(AuditLog.timestamp.desc()).all()
    
    @staticmethod
    def get_actions_by_type(action, limit=100):
        """Получить действия по типу"""
        return AuditLog.query.filter_by(action=action)\
            .order_by(AuditLog.timestamp.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def search(filters=None, limit=100):
        """
        Поиск логов с фильтрами
        
        Args:
            filters: dict с фильтрами (user_id, action, resource, start_date, end_date)
            limit: Максимум результатов
        
        Returns:
            Список логов
        """
        query = AuditLog.query
        
        if filters:
            if 'user_id' in filters:
                query = query.filter_by(user_id=filters['user_id'])
            
            if 'action' in filters:
                query = query.filter_by(action=filters['action'])
            
            if 'resource' in filters:
                query = query.filter_by(resource=filters['resource'])
            
            if 'start_date' in filters:
                query = query.filter(AuditLog.timestamp >= filters['start_date'])
            
            if 'end_date' in filters:
                query = query.filter(AuditLog.timestamp <= filters['end_date'])
            
            if 'ip_address' in filters:
                query = query.filter_by(ip_address=filters['ip_address'])
        
        return query.order_by(AuditLog.timestamp.desc()).limit(limit).all()


class LoginAttempt(db.Model):
    """Попытки входа (для отслеживания брутфорса)"""
    
    __tablename__ = 'login_attempt'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, index=True)
    ip_address = db.Column(db.String(45), nullable=False, index=True)
    success = db.Column(db.Boolean, nullable=False, default=False, index=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    user_agent = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<LoginAttempt {self.id}: {self.username} {"success" if self.success else "failed"}>'
    
    def to_dict(self):
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'username': self.username,
            'ip_address': self.ip_address,
            'success': self.success,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'user_agent': self.user_agent
        }
    
    @staticmethod
    def log_attempt(username, ip_address, success, user_agent=None):
        """Логировать попытку входа"""
        attempt = LoginAttempt(
            username=username,
            ip_address=ip_address,
            success=success,
            user_agent=user_agent,
            timestamp=datetime.utcnow()
        )
        db.session.add(attempt)
        db.session.commit()
        return attempt
    
    @staticmethod
    def get_failed_attempts(username, ip_address, minutes=15):
        """
        Получить количество неудачных попыток
        
        Args:
            username: Имя пользователя
            ip_address: IP адрес
            minutes: За последние N минут
        
        Returns:
            Количество неудачных попыток
        """
        from datetime import timedelta
        
        threshold = datetime.utcnow() - timedelta(minutes=minutes)
        
        return LoginAttempt.query.filter(
            LoginAttempt.username == username,
            LoginAttempt.ip_address == ip_address,
            LoginAttempt.success == False,
            LoginAttempt.timestamp >= threshold
        ).count()
    
    @staticmethod
    def cleanup_old_attempts(days=30):
        """Очистка старых попыток"""
        from datetime import timedelta
        
        threshold = datetime.utcnow() - timedelta(days=days)
        
        deleted = LoginAttempt.query.filter(
            LoginAttempt.timestamp < threshold
        ).delete()
        
        db.session.commit()
        return deleted


class TwoFactorSecret(db.Model):
    """Секреты для двухфакторной аутентификации"""
    
    __tablename__ = 'two_factor_secret'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    secret = db.Column(db.String(255), nullable=False)
    enabled = db.Column(db.Boolean, nullable=False, default=False)
    backup_codes = db.Column(db.JSON, nullable=True)  # Резервные коды
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('two_factor', uselist=False))
    
    def __repr__(self):
        return f'<TwoFactorSecret {self.id}: user={self.user_id} enabled={self.enabled}>'
    
    def to_dict(self):
        """Преобразование в словарь"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'enabled': self.enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'has_backup_codes': bool(self.backup_codes)
        }
    
    def generate_backup_codes(self, count=10):
        """Генерация резервных кодов"""
        import secrets
        from app.utils.security import PasswordManager
        
        codes = [secrets.token_hex(4).upper() for _ in range(count)]
        
        # Хешируем коды перед сохранением
        self.backup_codes = [PasswordManager.hash_password(code) for code in codes]
        db.session.commit()
        
        # Возвращаем незахешированные коды (показываем пользователю только один раз)
        return codes
    
    def verify_backup_code(self, code):
        """Проверка резервного кода"""
        from app.utils.security import PasswordManager
        
        if not self.backup_codes:
            return False
        
        for i, hashed_code in enumerate(self.backup_codes):
            if PasswordManager.verify_password(hashed_code, code):
                # Удаляем использованный код
                self.backup_codes.pop(i)
                db.session.commit()
                return True
        
        return False
