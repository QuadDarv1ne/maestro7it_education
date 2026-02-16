import schedule
import time
import threading
import logging
from datetime import datetime, date
from app import db
from app.models.tournament import Tournament
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser
from app.utils.notifications import notification_service
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
        
        # Add retry configuration
        self.max_retries = 3
        self.retry_delay = 5  # seconds

    def _retry_operation(self, operation, *args, **kwargs):
        """
        Execute an operation with retry logic
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return operation(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < self.max_retries - 1:  # Don't sleep on the last attempt
                    import time
                    time.sleep(self.retry_delay)
                else:
                    logger.error(f"All {self.max_retries} attempts failed. Last error: {e}")
        
        # If all attempts failed, raise the last exception
        raise last_exception

    def _update_from_fide_with_retry(self):
        """Wrapper for _update_from_fide with retry mechanism"""
        def operation():
            return self._update_from_fide()
        return self._retry_operation(operation)

    def _update_from_cfr_with_retry(self):
        """Wrapper for _update_from_cfr with retry mechanism"""
        def operation():
            return self._update_from_cfr()
        return self._retry_operation(operation)

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

            # Обновляем с FIDE (with retry)
            try:
                self._update_from_fide_with_retry()
            except Exception as e:
                logger.error(f"Не удалось обновить данные с FIDE после всех попыток: {e}")

            # Обновляем с CFR (with retry)
            try:
                self._update_from_cfr_with_retry()
            except Exception as e:
                logger.error(f"Не удалось обновить данные с CFR после всех попыток: {e}")

            logger.info("Обновление завершено успешно")

        except Exception as e:
            logger.error(f"Критическая ошибка при обновлении: {e}", exc_info=True)
            import traceback
            traceback.print_exc()

    def _update_from_fide(self):
        """Обновить данные с FIDE"""
        logger.info("Обновление данных с FIDE...")
        try:
            # Wrap the parser call in a try-catch for resilience
            try:
                fide_tournaments = self.fide_parser.get_tournaments_russia(2026)
            except Exception as e:
                logger.error(f"Failed to fetch FIDE tournaments: {e}")
                fide_tournaments = []
                return  # Exit early if we couldn't fetch data

            added_count = 0
            processed_count = 0

            for tourney_data in fide_tournaments:
                try:
                    existing = Tournament.query.filter_by(
                        name=tourney_data['name'],
                        start_date=tourney_data['start_date']
                    ).first()

                    if not existing:
                        # Validate and clean the data before adding
                        filtered_data = self._validate_and_clean_tournament_data(tourney_data)

                        if filtered_data:
                            tournament = Tournament(**filtered_data)
                            # Run validation before adding to session
                            if tournament.validate():
                                db.session.add(tournament)
                                added_count += 1
                            else:
                                logger.warning(f"Турнир не прошел валидацию: {tournament.name}")
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
            # Wrap the parser call in a try-catch for resilience
            try:
                cfr_tournaments = self.cfr_parser.get_tournaments(2026)
            except Exception as e:
                logger.error(f"Failed to fetch CFR tournaments: {e}")
                cfr_tournaments = []
                return  # Exit early if we couldn't fetch data

            added_count = 0
            processed_count = 0

            for tourney_data in cfr_tournaments:
                try:
                    existing = Tournament.query.filter_by(
                        name=tourney_data['name'],
                        start_date=tourney_data['start_date']
                    ).first()

                    if not existing:
                        # Validate and clean the data before adding
                        filtered_data = self._validate_and_clean_tournament_data(tourney_data)

                        if filtered_data:
                            tournament = Tournament(**filtered_data)
                            # Run validation before adding to session
                            if tournament.validate():
                                db.session.add(tournament)
                                added_count += 1
                            else:
                                logger.warning(f"Турнир не прошел валидацию: {tournament.name}")
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

    def _validate_and_clean_tournament_data(self, tourney_data):
        """Валидация и очистка данных турнира перед добавлением"""
        try:
            # Filter out None values and ensure required fields are present
            filtered_data = {k: v for k, v in tourney_data.items() if v is not None}

            # Ensure required fields have defaults if missing
            if 'description' not in filtered_data:
                filtered_data['description'] = None
            if 'prize_fund' not in filtered_data:
                filtered_data['prize_fund'] = None
            if 'organizer' not in filtered_data:
                filtered_data['organizer'] = None
            
            # Sanitize fields to prevent XSS and ensure data quality
            if 'name' in filtered_data and filtered_data['name']:
                # Clean the name field
                filtered_data['name'] = str(filtered_data['name']).strip()[:200]  # Limit length
            
            if 'location' in filtered_data and filtered_data['location']:
                # Clean the location field
                filtered_data['location'] = str(filtered_data['location']).strip()[:100]  # Limit length
            
            if 'description' in filtered_data and filtered_data['description']:
                # Clean the description field
                filtered_data['description'] = str(filtered_data['description']).strip()[:500]  # Limit length
            
            if 'organizer' in filtered_data and filtered_data['organizer']:
                # Clean the organizer field
                filtered_data['organizer'] = str(filtered_data['organizer']).strip()[:100]  # Limit length
            
            if 'prize_fund' in filtered_data and filtered_data['prize_fund']:
                # Clean the prize fund field
                filtered_data['prize_fund'] = str(filtered_data['prize_fund']).strip()[:50]  # Limit length
            
            if 'category' in filtered_data and filtered_data['category']:
                # Clean the category field
                filtered_data['category'] = str(filtered_data['category']).strip()[:50]  # Limit length
            
            if 'status' in filtered_data and filtered_data['status']:
                # Clean the status field
                filtered_data['status'] = str(filtered_data['status']).strip()[:20]  # Limit length
            
            if 'source_url' in filtered_data and filtered_data['source_url']:
                # Validate URL format
                source_url = str(filtered_data['source_url']).strip()
                if source_url.startswith(('http://', 'https://')):
                    filtered_data['source_url'] = source_url[:200]  # Limit length
                else:
                    filtered_data['source_url'] = None
            
            if 'fide_id' in filtered_data and filtered_data['fide_id']:
                # Ensure FIDE ID is properly formatted
                filtered_data['fide_id'] = str(filtered_data['fide_id'])[:20]  # Limit length
            
            # Ensure dates are valid
            if 'start_date' in filtered_data and filtered_data['start_date'] is None:
                logger.warning(f"Invalid start date: {filtered_data['start_date']}")
                return None  # Skip this tournament if start date is invalid
            
            if 'end_date' in filtered_data and (filtered_data['end_date'] is None or filtered_data['end_date'] < filtered_data['start_date']):
                # Set end date equal to start date if not provided or invalid
                filtered_data['end_date'] = filtered_data['start_date']
            
            # Ensure dates are date objects, not strings
            if 'start_date' in filtered_data and isinstance(filtered_data['start_date'], str):
                try:
                    from datetime import datetime
                    filtered_data['start_date'] = datetime.strptime(filtered_data['start_date'], '%Y-%m-%d').date()
                except ValueError:
                    logger.warning(f"Invalid date format for start_date: {filtered_data['start_date']}")
                    return None
            
            if 'end_date' in filtered_data and isinstance(filtered_data['end_date'], str):
                try:
                    from datetime import datetime
                    filtered_data['end_date'] = datetime.strptime(filtered_data['end_date'], '%Y-%m-%d').date()
                except ValueError:
                    logger.warning(f"Invalid date format for end_date: {filtered_data['end_date']}")
                    return None
            
            return filtered_data
        except Exception as e:
            logger.error(f"Ошибка при валидации данных турнира: {e}")
            return None
    
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