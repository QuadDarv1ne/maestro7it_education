"""
Telegram бот для уведомлений о проходах спутников
"""

import asyncio
from datetime import datetime, timedelta
from typing import Optional, Callable, List
from pathlib import Path

from .logger import get_logger
from .config import Config
from .satellite_tracker import SatelliteTracker, SatellitePass

logger = get_logger("noaa_receiver.telegram_bot")


class TelegramNotifier:
    """
    Telegram бот для отправки уведомлений
    
    Поддерживает:
    - Уведомления о предстоящих проходах
    - Отправка изображений
    - Статус системы
    """
    
    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.telegram_config = self.config.config.get("telegram", {})
        
        self.enabled = self.telegram_config.get("enabled", False)
        self.bot_token = self.telegram_config.get("bot_token", "")
        self.chat_id = self.telegram_config.get("chat_id", "")
        
        self._session = None
        self._initialized = False
    
    def _check_config(self) -> bool:
        """Проверка конфигурации"""
        if not self.enabled:
            logger.debug("Telegram уведомления отключены")
            return False
        
        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram bot_token или chat_id не настроены")
            return False
        
        return True
    
    async def _get_session(self):
        """Получение aiohttp сессии"""
        if self._session is None:
            import aiohttp
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def close(self):
        """Закрытие сессии"""
        if self._session:
            await self._session.close()
            self._session = None
    
    async def send_message(
        self,
        text: str,
        parse_mode: str = "HTML",
    ) -> bool:
        """
        Отправка текстового сообщения
        
        Args:
            text: Текст сообщения
            parse_mode: Режим парсинга ('HTML', 'Markdown')
        
        Returns:
            True если успешно
        """
        if not self._check_config():
            return False
        
        try:
            session = await self._get_session()
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            
            data = {
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": parse_mode,
            }
            
            async with session.post(url, json=data) as response:
                if response.status == 200:
                    logger.debug("Сообщение отправлено")
                    return True
                else:
                    error = await response.json()
                    logger.error(f"Ошибка Telegram API: {error}")
                    return False
                    
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения: {e}")
            return False
    
    async def send_photo(
        self,
        photo_path: str,
        caption: str = "",
    ) -> bool:
        """
        Отправка фотографии
        
        Args:
            photo_path: Путь к файлу изображения
            caption: Подпись к фото
        
        Returns:
            True если успешно
        """
        if not self._check_config():
            return False
        
        try:
            session = await self._get_session()
            url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
            
            path = Path(photo_path)
            if not path.exists():
                logger.error(f"Файл не найден: {photo_path}")
                return False
            
            with open(path, 'rb') as f:
                data = {
                    "chat_id": self.chat_id,
                    "photo": f,
                    "caption": caption,
                }
                
                async with session.post(url, data=data) as response:
                    if response.status == 200:
                        logger.debug(f"Фото отправлено: {photo_path}")
                        return True
                    else:
                        error = await response.json()
                        logger.error(f"Ошибка Telegram API: {error}")
                        return False
                        
        except Exception as e:
            logger.error(f"Ошибка отправки фото: {e}")
            return False
    
    async def send_pass_notification(
        self,
        passage: SatellitePass,
        advance_minutes: int = 30,
    ) -> bool:
        """
        Уведомление о предстоящем проходе спутника
        
        Args:
            passage: Данные о проходе
            advance_minutes: За сколько минут предупредить
        
        Returns:
            True если успешно
        """
        time_to_pass = (passage.aos - datetime.now()).total_seconds() / 60
        
        if time_to_pass < 0:
            return False
        
        # Формирование сообщения
        message = f"""
🛰️ <b>Проход спутника {passage.satellite_name}</b>

⏰ <b>Начало:</b> {passage.aos.strftime('%H:%M:%S')} ({passage.aos.strftime('%d.%m')})
📍 <b>Конец:</b> {passage.los.strftime('%H:%M:%S')}
⏱️  <b>Длительность:</b> {passage.duration_seconds/60:.1f} мин
📐 <b>Макс. элевация:</b> {passage.max_elevation:.1f}°
📻 <b>Частота:</b> {passage.frequency_mhz:.3f} MHz

⏳ До начала: {time_to_pass:.0f} мин
"""
        
        return await self.send_message(message)
    
    async def send_pass_started(
        self,
        passage: SatellitePass,
    ) -> bool:
        """Уведомление о начале прохода"""
        message = f"""
🔴 <b>Запись началась!</b>

🛰️ {passage.satellite_name}
⏱️  {passage.duration_seconds/60:.1f} мин
📐 Max: {passage.max_elevation:.1f}°
"""
        return await self.send_message(message)
    
    async def send_pass_completed(
        self,
        passage: SatellitePass,
        image_path: Optional[str] = None,
    ) -> bool:
        """
        Уведомление о завершении прохода
        
        Args:
            passage: Данные о проходе
            image_path: Путь к изображению (опционально)
        """
        message = f"""
✅ <b>Запись завершена!</b>

🛰️ {passage.satellite_name}
📁 Изображение готово
"""
        
        if image_path and Path(image_path).exists():
            return await self.send_photo(image_path, message)
        else:
            return await self.send_message(message)
    
    async def send_status(
        self,
        system_status: dict,
    ) -> bool:
        """
        Отправка статуса системы
        
        Args:
            system_status: Словарь со статусом системы
        """
        lines = ["📊 <b>Статус системы NOAA Receiver</b>\n"]
        
        for key, value in system_status.items():
            emoji = "✅" if value else "❌"
            lines.append(f"{emoji} {key}: {value}")
        
        message = "\n".join(lines)
        return await self.send_message(message)
    
    def run_notifier(
        self,
        tracker: SatelliteTracker,
        check_interval_minutes: int = 5,
        advance_notification_minutes: int = 30,
    ):
        """
        Запуск цикла уведомлений
        
        Args:
            tracker: Трекер спутников
            check_interval_minutes: Интервал проверки (мин)
            advance_notification_minutes: За сколько минут предупреждать
        """
        logger.info(f"🤖 Запуск Telegram notifier (интервал: {check_interval_minutes} мин)")
        
        notified_passes = set()
        
        async def check_loop():
            while True:
                try:
                    next_pass = tracker.get_next_pass(min_elevation=20)
                    
                    if next_pass:
                        pass_key = f"{next_pass.satellite_name}_{next_pass.aos.isoformat()}"
                        
                        # Проверка времени для уведомления
                        time_to_aos = (next_pass.aos - datetime.now()).total_seconds() / 60
                        
                        if (advance_notification_minutes - 5 <= time_to_aos <= advance_notification_minutes + 5
                                and pass_key not in notified_passes):
                            
                            await self.send_pass_notification(next_pass, advance_notification_minutes)
                            notified_passes.add(pass_key)
                            logger.info(f"Уведомление отправлено: {next_pass}")
                        
                        # Очистка старых уведомлений
                        cutoff = datetime.now() - timedelta(hours=1)
                        notified_passes = {
                            k for k in notified_passes
                            if datetime.fromisoformat(k.split('_', 1)[1]) > cutoff
                        }
                    
                    await asyncio.sleep(check_interval_minutes * 60)
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    logger.error(f"Ошибка в цикле уведомлений: {e}")
                    await asyncio.sleep(60)
        
        try:
            asyncio.run(check_loop())
        except KeyboardInterrupt:
            logger.info("Notifier остановлен")


class SimpleTelegramBot:
    """
    Простой синхронный Telegram клиент для базовых уведомлений
    
    Используется когда asyncio не подходит
    """
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, text: str) -> bool:
        """Отправка сообщения (синхронно)"""
        try:
            import urllib.request
            import json
            
            data = json.dumps({
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": "HTML",
            }).encode('utf-8')
            
            req = urllib.request.Request(
                f"{self.base_url}/sendMessage",
                data=data,
                headers={"Content-Type": "application/json"},
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 200
                
        except Exception as e:
            logger.error(f"Ошибка отправки: {e}")
            return False
    
    def send_pass_alert(self, passage: SatellitePass) -> bool:
        """Отправка уведомления о проходе"""
        message = f"""
🛰️ <b>{passage.satellite_name}</b>
⏰ {passage.aos.strftime('%H:%M:%S')} - {passage.los.strftime('%H:%M:%S')}
📐 Max: {passage.max_elevation:.1f}°
⏱️  {passage.duration_seconds/60:.1f} мин
"""
        return self.send_message(message)
