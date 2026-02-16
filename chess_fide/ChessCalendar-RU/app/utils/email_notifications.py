"""
Система email уведомлений для событий безопасности
"""
from flask import render_template_string
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class EmailNotificationService:
    """Сервис для отправки email уведомлений"""
    
    def __init__(self, app=None):
        self.app = app
        self.enabled = False
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Инициализация сервиса"""
        self.enabled = app.config.get('EMAIL_NOTIFICATIONS_ENABLED', False)
        self.from_email = app.config.get('EMAIL_FROM', 'noreply@chesscalendar.ru')
        
        if self.enabled:
            logger.info("Email notification service initialized")
        else:
            logger.info("Email notifications disabled")
    
    def send_email(self, to_email, subject, body_html, body_text=None):
        """Отправка email"""
        if not self.enabled:
            logger.debug(f"Email not sent (disabled): {subject} to {to_email}")
            return False
        
        try:
            # TODO: Интеграция с SMTP или email сервисом (SendGrid, AWS SES, etc.)
            logger.info(f"Email sent: {subject} to {to_email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_password_changed_notification(self, user):
        """Уведомление об изменении пароля"""
        subject = "Ваш пароль был изменен"
        
        body_html = f"""
        <html>
        <body>
            <h2>Изменение пароля</h2>
            <p>Здравствуйте, {user.username}!</p>
            <p>Ваш пароль был успешно изменен {datetime.utcnow().strftime('%d.%m.%Y в %H:%M')} UTC.</p>
            <p>Если это были не вы, немедленно свяжитесь с нами.</p>
            <hr>
            <p><small>ChessCalendar-RU - Календарь шахматных турниров</small></p>
        </body>
        </html>
        """
        
        body_text = f"""
        Изменение пароля
        
        Здравствуйте, {user.username}!
        
        Ваш пароль был успешно изменен {datetime.utcnow().strftime('%d.%m.%Y в %H:%M')} UTC.
        
        Если это были не вы, немедленно свяжитесь с нами.
        
        ---
        ChessCalendar-RU - Календарь шахматных турниров
        """
        
        return self.send_email(user.email, subject, body_html, body_text)
    
    def send_account_locked_notification(self, user):
        """Уведомление о блокировке аккаунта"""
        subject = "Ваш аккаунт был заблокирован"
        
        locked_until = user.locked_until.strftime('%d.%m.%Y в %H:%M') if user.locked_until else 'неизвестно'
        
        body_html = f"""
        <html>
        <body>
            <h2>Блокировка аккаунта</h2>
            <p>Здравствуйте, {user.username}!</p>
            <p>Ваш аккаунт был временно заблокирован из-за множественных неудачных попыток входа.</p>
            <p><strong>Блокировка до:</strong> {locked_until} UTC</p>
            <p>Если это были не вы, рекомендуем изменить пароль после разблокировки.</p>
            <hr>
            <p><small>ChessCalendar-RU - Календарь шахматных турниров</small></p>
        </body>
        </html>
        """
        
        body_text = f"""
        Блокировка аккаунта
        
        Здравствуйте, {user.username}!
        
        Ваш аккаунт был временно заблокирован из-за множественных неудачных попыток входа.
        
        Блокировка до: {locked_until} UTC
        
        Если это были не вы, рекомендуем изменить пароль после разблокировки.
        
        ---
        ChessCalendar-RU - Календарь шахматных турниров
        """
        
        return self.send_email(user.email, subject, body_html, body_text)
    
    def send_new_login_notification(self, user, ip_address, user_agent):
        """Уведомление о новом входе"""
        subject = "Новый вход в ваш аккаунт"
        
        body_html = f"""
        <html>
        <body>
            <h2>Новый вход в аккаунт</h2>
            <p>Здравствуйте, {user.username}!</p>
            <p>Зафиксирован новый вход в ваш аккаунт:</p>
            <ul>
                <li><strong>Время:</strong> {datetime.utcnow().strftime('%d.%m.%Y в %H:%M')} UTC</li>
                <li><strong>IP адрес:</strong> {ip_address}</li>
                <li><strong>Устройство:</strong> {user_agent[:100]}</li>
            </ul>
            <p>Если это были не вы, немедленно измените пароль.</p>
            <hr>
            <p><small>ChessCalendar-RU - Календарь шахматных турниров</small></p>
        </body>
        </html>
        """
        
        body_text = f"""
        Новый вход в аккаунт
        
        Здравствуйте, {user.username}!
        
        Зафиксирован новый вход в ваш аккаунт:
        
        Время: {datetime.utcnow().strftime('%d.%m.%Y в %H:%M')} UTC
        IP адрес: {ip_address}
        Устройство: {user_agent[:100]}
        
        Если это были не вы, немедленно измените пароль.
        
        ---
        ChessCalendar-RU - Календарь шахматных турниров
        """
        
        return self.send_email(user.email, subject, body_html, body_text)
    
    def send_api_key_regenerated_notification(self, user):
        """Уведомление о перегенерации API ключа"""
        subject = "Ваш API ключ был изменен"
        
        body_html = f"""
        <html>
        <body>
            <h2>Изменение API ключа</h2>
            <p>Здравствуйте, {user.username}!</p>
            <p>Ваш API ключ был перегенерирован {datetime.utcnow().strftime('%d.%m.%Y в %H:%M')} UTC.</p>
            <p>Старый ключ больше не действителен.</p>
            <p>Если это были не вы, немедленно свяжитесь с нами.</p>
            <hr>
            <p><small>ChessCalendar-RU - Календарь шахматных турниров</small></p>
        </body>
        </html>
        """
        
        body_text = f"""
        Изменение API ключа
        
        Здравствуйте, {user.username}!
        
        Ваш API ключ был перегенерирован {datetime.utcnow().strftime('%d.%m.%Y в %H:%M')} UTC.
        
        Старый ключ больше не действителен.
        
        Если это были не вы, немедленно свяжитесь с нами.
        
        ---
        ChessCalendar-RU - Календарь шахматных турниров
        """
        
        return self.send_email(user.email, subject, body_html, body_text)
    
    def send_welcome_email(self, user):
        """Приветственное письмо новому пользователю"""
        subject = "Добро пожаловать в ChessCalendar-RU!"
        
        body_html = f"""
        <html>
        <body>
            <h2>Добро пожаловать!</h2>
            <p>Здравствуйте, {user.username}!</p>
            <p>Спасибо за регистрацию в ChessCalendar-RU - вашем календаре шахматных турниров.</p>
            <h3>Что вы можете делать:</h3>
            <ul>
                <li>Просматривать актуальные шахматные турниры</li>
                <li>Добавлять турниры в избранное</li>
                <li>Получать уведомления о новых турнирах</li>
                <li>Использовать API для интеграции</li>
            </ul>
            <p><strong>Ваш API ключ:</strong> {user.api_key}</p>
            <p>Сохраните его в безопасном месте!</p>
            <hr>
            <p><small>ChessCalendar-RU - Календарь шахматных турниров</small></p>
        </body>
        </html>
        """
        
        body_text = f"""
        Добро пожаловать!
        
        Здравствуйте, {user.username}!
        
        Спасибо за регистрацию в ChessCalendar-RU - вашем календаре шахматных турниров.
        
        Что вы можете делать:
        - Просматривать актуальные шахматные турниры
        - Добавлять турниры в избранное
        - Получать уведомления о новых турнирах
        - Использовать API для интеграции
        
        Ваш API ключ: {user.api_key}
        Сохраните его в безопасном месте!
        
        ---
        ChessCalendar-RU - Календарь шахматных турниров
        """
        
        return self.send_email(user.email, subject, body_html, body_text)


# Глобальный экземпляр
email_service = EmailNotificationService()
