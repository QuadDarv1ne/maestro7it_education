"""
Интеграция с внешними сервисами
Telegram, Slack, Discord боты для уведомлений
"""

import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
import json


class TelegramIntegration:
    """Интеграция с Telegram Bot API"""
    
    def __init__(self, bot_token: Optional[str] = None):
        self.bot_token = bot_token or self._get_bot_token()
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def _get_bot_token(self) -> str:
        """Получить токен бота из конфигурации"""
        try:
            from config.config import Config
            return getattr(Config, 'TELEGRAM_BOT_TOKEN', '')
        except (ImportError, AttributeError):
            return ''
    
    def send_message(
        self,
        chat_id: str,
        text: str,
        parse_mode: str = 'HTML',
        disable_notification: bool = False
    ) -> Dict[str, Any]:
        """
        Отправить сообщение в Telegram
        
        Args:
            chat_id: ID чата или username (@username)
            text: Текст сообщения
            parse_mode: Режим парсинга (HTML, Markdown)
            disable_notification: Отключить звук уведомления
        """
        if not self.bot_token:
            return {'error': 'Bot token not configured'}
        
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
            'disable_notification': disable_notification
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            return {'error': str(e)}
    
    def send_tournament_notification(
        self,
        chat_id: str,
        tournament: Any
    ) -> Dict[str, Any]:
        """Отправить уведомление о турнире"""
        text = f"""
<b>🏆 Новый турнир!</b>

<b>Название:</b> {tournament.name}
<b>Категория:</b> {tournament.category}
<b>Локация:</b> {tournament.location}
<b>Дата начала:</b> {tournament.start_date.strftime('%d.%m.%Y') if tournament.start_date else 'Не указана'}
<b>Статус:</b> {tournament.status}

<a href="https://chesscalendar.ru/tournament/{tournament.id}">Подробнее</a>
        """.strip()
        
        return self.send_message(chat_id, text)
    
    def send_daily_digest(
        self,
        chat_id: str,
        tournaments: List[Any]
    ) -> Dict[str, Any]:
        """Отправить ежедневную сводку турниров"""
        if not tournaments:
            text = "📅 <b>Ежедневная сводка</b>\n\nНовых турниров сегодня нет."
        else:
            text = f"📅 <b>Ежедневная сводка</b>\n\nНовых турниров: {len(tournaments)}\n\n"
            
            for i, tournament in enumerate(tournaments[:5], 1):
                text += f"{i}. <b>{tournament.name}</b>\n"
                text += f"   📍 {tournament.location}\n"
                text += f"   📅 {tournament.start_date.strftime('%d.%m.%Y') if tournament.start_date else 'Не указана'}\n\n"
            
            if len(tournaments) > 5:
                text += f"...и еще {len(tournaments) - 5} турниров"
        
        return self.send_message(chat_id, text)


class SlackIntegration:
    """Интеграция со Slack Webhooks"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or self._get_webhook_url()
    
    def _get_webhook_url(self) -> str:
        """Получить webhook URL из конфигурации"""
        try:
            from config.config import Config
            return getattr(Config, 'SLACK_WEBHOOK_URL', '')
        except (ImportError, AttributeError):
            return ''
    
    def send_message(
        self,
        text: str,
        channel: Optional[str] = None,
        username: str = 'ChessCalendar Bot',
        icon_emoji: str = ':chess_pawn:'
    ) -> Dict[str, Any]:
        """
        Отправить сообщение в Slack
        
        Args:
            text: Текст сообщения
            channel: Канал для отправки (опционально)
            username: Имя бота
            icon_emoji: Эмодзи иконка
        """
        if not self.webhook_url:
            return {'error': 'Webhook URL not configured'}
        
        payload = {
            'text': text,
            'username': username,
            'icon_emoji': icon_emoji
        }
        
        if channel:
            payload['channel'] = channel
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            return {'status': 'sent', 'status_code': response.status_code}
        except Exception as e:
            return {'error': str(e)}
    
    def send_rich_message(
        self,
        title: str,
        text: str,
        fields: Optional[List[Dict[str, str]]] = None,
        color: str = '#2563eb'
    ) -> Dict[str, Any]:
        """Отправить форматированное сообщение с вложениями"""
        if not self.webhook_url:
            return {'error': 'Webhook URL not configured'}
        
        attachment = {
            'title': title,
            'text': text,
            'color': color,
            'footer': 'ChessCalendar-RU',
            'ts': int(datetime.utcnow().timestamp())
        }
        
        if fields:
            attachment['fields'] = fields
        
        payload = {
            'attachments': [attachment]
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            return {'status': 'sent', 'status_code': response.status_code}
        except Exception as e:
            return {'error': str(e)}
    
    def send_tournament_notification(self, tournament: Any) -> Dict[str, Any]:
        """Отправить уведомление о турнире"""
        fields = [
            {
                'title': 'Категория',
                'value': tournament.category,
                'short': True
            },
            {
                'title': 'Локация',
                'value': tournament.location,
                'short': True
            },
            {
                'title': 'Дата начала',
                'value': tournament.start_date.strftime('%d.%m.%Y') if tournament.start_date else 'Не указана',
                'short': True
            },
            {
                'title': 'Статус',
                'value': tournament.status,
                'short': True
            }
        ]
        
        return self.send_rich_message(
            title=f"🏆 Новый турнир: {tournament.name}",
            text=f"Добавлен новый турнир в календарь",
            fields=fields,
            color='#10b981'
        )
    
    def send_alert(
        self,
        alert_type: str,
        message: str,
        severity: str = 'warning'
    ) -> Dict[str, Any]:
        """Отправить алерт"""
        colors = {
            'info': '#2563eb',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'success': '#10b981'
        }
        
        return self.send_rich_message(
            title=f"⚠️ Alert: {alert_type}",
            text=message,
            color=colors.get(severity, '#f59e0b')
        )


class DiscordIntegration:
    """Интеграция с Discord Webhooks"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or self._get_webhook_url()
    
    def _get_webhook_url(self) -> str:
        """Получить webhook URL из конфигурации"""
        try:
            from config.config import Config
            return getattr(Config, 'DISCORD_WEBHOOK_URL', '')
        except (ImportError, AttributeError):
            return ''
    
    def send_message(
        self,
        content: str,
        username: str = 'ChessCalendar Bot',
        avatar_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Отправить сообщение в Discord
        
        Args:
            content: Текст сообщения
            username: Имя бота
            avatar_url: URL аватара бота
        """
        if not self.webhook_url:
            return {'error': 'Webhook URL not configured'}
        
        payload = {
            'content': content,
            'username': username
        }
        
        if avatar_url:
            payload['avatar_url'] = avatar_url
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            return {'status': 'sent', 'status_code': response.status_code}
        except Exception as e:
            return {'error': str(e)}
    
    def send_embed(
        self,
        title: str,
        description: str,
        fields: Optional[List[Dict[str, Any]]] = None,
        color: int = 0x2563eb,
        thumbnail_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Отправить форматированное сообщение (embed)"""
        if not self.webhook_url:
            return {'error': 'Webhook URL not configured'}
        
        embed = {
            'title': title,
            'description': description,
            'color': color,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if fields:
            embed['fields'] = fields
        
        if thumbnail_url:
            embed['thumbnail'] = {'url': thumbnail_url}
        
        payload = {
            'embeds': [embed]
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                timeout=10
            )
            return {'status': 'sent', 'status_code': response.status_code}
        except Exception as e:
            return {'error': str(e)}
    
    def send_tournament_notification(self, tournament: Any) -> Dict[str, Any]:
        """Отправить уведомление о турнире"""
        fields = [
            {
                'name': '📂 Категория',
                'value': tournament.category,
                'inline': True
            },
            {
                'name': '📍 Локация',
                'value': tournament.location,
                'inline': True
            },
            {
                'name': '📅 Дата начала',
                'value': tournament.start_date.strftime('%d.%m.%Y') if tournament.start_date else 'Не указана',
                'inline': True
            },
            {
                'name': '🎯 Статус',
                'value': tournament.status,
                'inline': True
            }
        ]
        
        return self.send_embed(
            title=f"🏆 Новый турнир: {tournament.name}",
            description="Добавлен новый турнир в календарь",
            fields=fields,
            color=0x10b981
        )


class IntegrationManager:
    """Менеджер для управления всеми интеграциями"""
    
    def __init__(self):
        self.telegram = TelegramIntegration()
        self.slack = SlackIntegration()
        self.discord = DiscordIntegration()
        self.enabled_integrations = self._get_enabled_integrations()
    
    def _get_enabled_integrations(self) -> List[str]:
        """Определить, какие интеграции настроены"""
        enabled = []
        
        if self.telegram.bot_token:
            enabled.append('telegram')
        if self.slack.webhook_url:
            enabled.append('slack')
        if self.discord.webhook_url:
            enabled.append('discord')
        
        return enabled
    
    def broadcast_tournament(self, tournament: Any, channels: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Отправить уведомление о турнире во все настроенные каналы
        
        Args:
            tournament: Объект турнира
            channels: Список каналов (опционально, по умолчанию все)
        """
        if channels is None:
            channels = self.enabled_integrations
        
        results = {}
        
        if 'telegram' in channels and 'telegram' in self.enabled_integrations:
            # Нужен chat_id из конфигурации
            try:
                from config.config import Config
                chat_id = getattr(Config, 'TELEGRAM_CHANNEL_ID', '')
                if chat_id:
                    results['telegram'] = self.telegram.send_tournament_notification(
                        chat_id, tournament
                    )
            except Exception as e:
                logger.error(f"Failed to send Telegram notification: {e}")
                results['telegram'] = {'error': 'Channel ID not configured'}
        
        if 'slack' in channels and 'slack' in self.enabled_integrations:
            results['slack'] = self.slack.send_tournament_notification(tournament)
        
        if 'discord' in channels and 'discord' in self.enabled_integrations:
            results['discord'] = self.discord.send_tournament_notification(tournament)
        
        return results
    
    def send_alert(
        self,
        alert_type: str,
        message: str,
        severity: str = 'warning',
        channels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Отправить алерт во все каналы"""
        if channels is None:
            channels = self.enabled_integrations
        
        results = {}
        
        if 'slack' in channels and 'slack' in self.enabled_integrations:
            results['slack'] = self.slack.send_alert(alert_type, message, severity)
        
        if 'discord' in channels and 'discord' in self.enabled_integrations:
            color_map = {
                'info': 0x2563eb,
                'warning': 0xf59e0b,
                'error': 0xef4444,
                'success': 0x10b981
            }
            results['discord'] = self.discord.send_embed(
                title=f"⚠️ Alert: {alert_type}",
                description=message,
                color=color_map.get(severity, 0xf59e0b)
            )
        
        return results
    
    def get_status(self) -> Dict[str, Any]:
        """Получить статус всех интеграций"""
        return {
            'enabled_integrations': self.enabled_integrations,
            'telegram': {
                'configured': 'telegram' in self.enabled_integrations,
                'bot_token_set': bool(self.telegram.bot_token)
            },
            'slack': {
                'configured': 'slack' in self.enabled_integrations,
                'webhook_set': bool(self.slack.webhook_url)
            },
            'discord': {
                'configured': 'discord' in self.enabled_integrations,
                'webhook_set': bool(self.discord.webhook_url)
            }
        }


# Глобальный экземпляр
integration_manager = IntegrationManager()
