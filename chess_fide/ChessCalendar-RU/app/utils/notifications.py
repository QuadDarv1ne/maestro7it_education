import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging

class NotificationService:
    def __init__(self, smtp_server='localhost', smtp_port=587, 
                 username=None, password=None, sender_email=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.sender_email = sender_email or username
        self.logger = logging.getLogger(__name__)
        
        # Список подписчиков (в реальном приложении хранить в БД)
        self.subscribers = []
    
    def add_subscriber(self, email, preferences=None):
        """Добавить подписчика на уведомления"""
        if not preferences:
            preferences = {'new_tournaments': True, 'updates': True}
            
        self.subscribers.append({
            'email': email,
            'preferences': preferences,
            'subscribed_at': datetime.utcnow()
        })
        self.logger.info(f"Добавлен подписчик: {email}")
    
    def remove_subscriber(self, email):
        """Удалить подписчика"""
        self.subscribers = [s for s in self.subscribers if s['email'] != email]
        self.logger.info(f"Удален подписчик: {email}")
    
    def send_new_tournament_notification(self, tournament):
        """Отправить уведомление о новом турнире"""
        subject = f"Новый шахматный турнир: {tournament.name}"
        
        html_content = f"""
        <html>
        <body>
            <h2>Новый турнир добавлен в календарь!</h2>
            <h3>{tournament.name}</h3>
            <p><strong>Дата:</strong> {tournament.start_date.strftime('%d.%m.%Y')} - {tournament.end_date.strftime('%d.%m.%Y')}</p>
            <p><strong>Место:</strong> {tournament.location}</p>
            <p><strong>Категория:</strong> {tournament.category}</p>
            <p><strong>Статус:</strong> {tournament.status}</p>
            
            <hr>
            <p><small>Это автоматическое уведомление от ChessCalendar-RU</small></p>
            <p><small>Чтобы отписаться, перейдите в настройки уведомлений на сайте</small></p>
        </body>
        </html>
        """
        
        self._send_bulk_email(subject, html_content, 
                            lambda sub: sub['preferences'].get('new_tournaments', True))
    
    def send_tournament_update_notification(self, tournament, changes):
        """Отправить уведомление об изменении турнира"""
        subject = f"Обновление турнира: {tournament.name}"
        
        changes_html = "<ul>"
        for field, (old_val, new_val) in changes.items():
            changes_html += f"<li><strong>{field}:</strong> {old_val} → {new_val}</li>"
        changes_html += "</ul>"
        
        html_content = f"""
        <html>
        <body>
            <h2>Турнир обновлен!</h2>
            <h3>{tournament.name}</h3>
            <p>В турнире произошли следующие изменения:</p>
            {changes_html}
            
            <hr>
            <p><small>Это автоматическое уведомление от ChessCalendar-RU</small></p>
        </body>
        </html>
        """
        
        self._send_bulk_email(subject, html_content,
                            lambda sub: sub['preferences'].get('updates', True))
    
    def send_daily_summary(self, tournaments_count, new_tournaments):
        """Отправить ежедневную сводку"""
        if not new_tournaments:
            return  # Нет новых турниров
            
        subject = f"Ежедневная сводка: {tournaments_count} турниров в календаре"
        
        tournaments_list = "<ul>"
        for tourney in new_tournaments[:5]:  # Показываем первые 5
            tournaments_list += f"<li>{tourney.name} ({tourney.location})</li>"
        tournaments_list += "</ul>"
        
        html_content = f"""
        <html>
        <body>
            <h2>Ежедневная сводка ChessCalendar-RU</h2>
            <p>В календаре зарегистрировано <strong>{tournaments_count}</strong> турниров.</p>
            
            <h3>Новые турниры за последние сутки:</h3>
            {tournaments_list}
            
            <p><a href="http://127.0.0.1:5000">Перейти к календарю</a></p>
            
            <hr>
            <p><small>Это автоматическое уведомление от ChessCalendar-RU</small></p>
        </body>
        </html>
        """
        
        self._send_bulk_email(subject, html_content, 
                            lambda sub: sub['preferences'].get('daily_summary', True))
    
    def _send_bulk_email(self, subject, html_content, filter_func=None):
        """Отправить email нескольким подписчикам"""
        if not self.subscribers:
            self.logger.warning("Нет подписчиков для отправки уведомлений")
            return
            
        # Фильтруем подписчиков
        if filter_func:
            recipients = [sub for sub in self.subscribers if filter_func(sub)]
        else:
            recipients = self.subscribers
            
        if not recipients:
            return
            
        try:
            # Создаем сообщение
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            
            # Добавляем HTML часть
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Отправляем каждому подписчику отдельно (BCC)
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.username and self.password:
                    server.starttls()
                    server.login(self.username, self.password)
                
                for subscriber in recipients:
                    msg['To'] = subscriber['email']
                    server.send_message(msg)
                    msg.replace_header('To', '')  # Очищаем для следующего получателя
                    
            self.logger.info(f"Отправлено {len(recipients)} уведомлений")
            
        except Exception as e:
            self.logger.error(f"Ошибка отправки уведомлений: {e}")
    
    def get_subscriber_stats(self):
        """Получить статистику по подписчикам"""
        return {
            'total_subscribers': len(self.subscribers),
            'new_tournaments_enabled': len([s for s in self.subscribers 
                                         if s['preferences'].get('new_tournaments', True)]),
            'updates_enabled': len([s for s in self.subscribers 
                                  if s['preferences'].get('updates', True)]),
            'daily_summary_enabled': len([s for s in self.subscribers 
                                        if s['preferences'].get('daily_summary', True)])
        }

# Глобальный экземпляр сервиса уведомлений
notification_service = NotificationService()