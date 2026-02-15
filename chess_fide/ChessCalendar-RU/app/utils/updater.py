import schedule
import time
import threading
import logging
from datetime import datetime
from app import db
from app.models.tournament import Tournament
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser
from app.utils.notifications import notification_service

# Initialize logging for this module
logger = logging.getLogger('app.scheduler')

try:
    from app.utils.backup import DatabaseBackupManager
    backup_manager = DatabaseBackupManager("chess_calendar.db")
except ImportError:
    # Mock backup manager if backup module not available
    class MockBackupManager:
        def create_compressed_backup(self):
            logger.warning("Backup manager not available, skipping backup")
            return None
    backup_manager = MockBackupManager()
    logger.warning("Backup manager not available, using mock implementation")

class TournamentUpdater:
    def __init__(self):
        self.fide_parser = FIDEParses()
        self.cfr_parser = CFRParser()
        
    def update_all_sources(self):
        """Обновить данные со всех источников"""
        logger.info("Начинаю обновление турниров...")
        
        try:
            # Создаем бэкап перед обновлением
            logger.info("Создаю резервную копию перед обновлением...")
            try:
                backup_result = backup_manager.create_compressed_backup()
                if backup_result:
                    logger.info(f"Резервная копия создана: {backup_result}")
                else:
                    logger.info("Создание резервной копии пропущено")
            except FileNotFoundError:
                logger.warning("Файл базы данных не найден, пропускаю создание резервной копии")
            except Exception as backup_error:
                logger.error(f"Ошибка при создании резервной копии: {backup_error}")
            
            # Обновляем с FIDE
            self._update_from_fide()
            
            # Обновляем с CFR
            self._update_from_cfr()
            
            logger.info("Обновление завершено успешно")
            
        except Exception as e:
            logger.error(f"Критическая ошибка при обновлении: {e}", exc_info=True)
            import traceback
            traceback.print_exc()

    def _update_from_fide(self):
        """Обновить данные с FIDE"""
        logger.info("Обновление данных с FIDE...")
        try:
            fide_tournaments = self.fide_parser.get_tournaments_russia(2026)
            added_count = 0
            processed_count = 0
            
            for tourney_data in fide_tournaments:
                try:
                    existing = Tournament.query.filter_by(
                        name=tourney_data['name'],
                        start_date=tourney_data['start_date']
                    ).first()
                    
                    if not existing:
                        # Filter out None values and ensure required fields are present
                        filtered_data = {k: v for k, v in tourney_data.items() if v is not None}

                        # Ensure required fields have defaults if missing
                        if 'description' not in filtered_data:
                            filtered_data['description'] = None
                        if 'prize_fund' not in filtered_data:
                            filtered_data['prize_fund'] = None
                        if 'organizer' not in filtered_data:
                            filtered_data['organizer'] = None

                        tournament = Tournament(**filtered_data)
                        db.session.add(tournament)
                        added_count += 1
                    processed_count += 1
                except KeyError as ke:
                    logger.error(f"Ошибка при обработке турнира с FIDE: отсутствует поле {ke}")
                    continue
                except Exception as te:
                    logger.error(f"Ошибка при добавлении турнира с FIDE: {te}")
                    continue
            
            try:
                db.session.commit()
                logger.info(f"Обработано {processed_count} турниров с FIDE, добавлено {added_count} новых")
            except Exception as db_error:
                logger.error(f"Ошибка при сохранении в базу: {db_error}")
                db.session.rollback()
                
        except Exception as e:
            logger.error(f"Ошибка при получении данных с FIDE: {e}", exc_info=True)
            import traceback
            traceback.print_exc()

    def _update_from_cfr(self):
        """Обновить данные с CFR"""
        logger.info("Обновление данных с CFR...")
        try:
            cfr_tournaments = self.cfr_parser.get_tournaments(2026)
            added_count = 0
            processed_count = 0
            
            for tourney_data in cfr_tournaments:
                try:
                    existing = Tournament.query.filter_by(
                        name=tourney_data['name'],
                        start_date=tourney_data['start_date']
                    ).first()
                    
                    if not existing:
                        # Filter out None values and ensure required fields are present
                        filtered_data = {k: v for k, v in tourney_data.items() if v is not None}

                        # Ensure required fields have defaults if missing
                        if 'description' not in filtered_data:
                            filtered_data['description'] = None
                        if 'prize_fund' not in filtered_data:
                            filtered_data['prize_fund'] = None
                        if 'organizer' not in filtered_data:
                            filtered_data['organizer'] = None

                        tournament = Tournament(**filtered_data)
                        db.session.add(tournament)
                        added_count += 1
                    processed_count += 1
                except KeyError as ke:
                    logger.error(f"Ошибка при обработке турнира с CFR: отсутствует поле {ke}")
                    continue
                except Exception as te:
                    logger.error(f"Ошибка при добавлении турнира с CFR: {te}")
                    continue
            
            try:
                db.session.commit()
                logger.info(f"Обработано {processed_count} турниров с CFR, добавлено {added_count} новых")
            except Exception as db_error:
                logger.error(f"Ошибка при сохранении в базу: {db_error}")
                db.session.rollback()
                
        except Exception as e:
            logger.error(f"Ошибка при получении данных с CFR: {e}", exc_info=True)
            import traceback
            traceback.print_exc()

    def send_tournament_reminders(self):
        """Отправить напоминания о турнирах"""
        try:
            logger.info("Отправка напоминаний о турнирах...")
            sent_count = notification_service.send_reminders()
            logger.info(f"Отправлено {sent_count} напоминаний о турнирах")
        except Exception as e:
            logger.error(f"Ошибка при отправке напоминаний: {e}", exc_info=True)
    
    def start_scheduler(self):
        """Запустить планировщик обновлений"""
        logger.info("Настройка планировщика обновлений")
        
        # Обновление каждый день в 03:00
        schedule.every().day.at("03:00").do(self.update_all_sources)
        
        # Обновление каждые 6 часов
        schedule.every(6).hours.do(self.update_all_sources)
        
        # Отправка напоминаний каждый день в 09:00
        schedule.every().day.at("09:00").do(self.send_tournament_reminders)
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Проверяем каждую минуту
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        logger.info("Планировщик обновлений запущен")


# Глобальный экземпляр обновлятора
updater = TournamentUpdater()

logger.info("TournamentUpdater инициализирован")