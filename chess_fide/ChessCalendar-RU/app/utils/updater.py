import schedule
import time
import threading
import logging
from datetime import datetime
from app import db
from app.models.tournament import Tournament
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser
try:
    from app.utils.backup import DatabaseBackupManager
    backup_manager = DatabaseBackupManager("chess_calendar.db")
except ImportError:
    # Mock backup manager if backup module not available
    class MockBackupManager:
        def create_compressed_backup(self):
            print(f"[{datetime.now()}] Backup manager not available, skipping backup")
            return None
    backup_manager = MockBackupManager()
    logging.warning("Backup manager not available, using mock implementation")

class TournamentUpdater:
    def __init__(self):
        self.fide_parser = FIDEParses()
        self.cfr_parser = CFRParser()
        
    def update_all_sources(self):
        """Обновить данные со всех источников"""
        print(f"[{datetime.now()}] Начинаю обновление турниров...")
        
        try:
            # Создаем бэкап перед обновлением
            print(f"[{datetime.now()}] Создаю резервную копию перед обновлением...")
            try:
                backup_result = backup_manager.create_compressed_backup()
                if backup_result:
                    print(f"[{datetime.now()}] Резервная копия создана: {backup_result}")
                else:
                    print(f"[{datetime.now()}] Создание резервной копии пропущено")
            except FileNotFoundError:
                print(f"[{datetime.now()}] Файл базы данных не найден, пропускаю создание резервной копии")
            except Exception as backup_error:
                print(f"[{datetime.now()}] Ошибка при создании резервной копии: {backup_error}")
            
            # Обновляем с FIDE
            self._update_from_fide()
            
            # Обновляем с CFR
            self._update_from_cfr()
            
            print(f"[{datetime.now()}] Обновление завершено успешно")
            
        except Exception as e:
            print(f"[{datetime.now()}] Критическая ошибка при обновлении: {e}")
            import traceback
            traceback.print_exc()

    def _update_from_fide(self):
        """Обновить данные с FIDE"""
        print("Обновление данных с FIDE...")
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
                        tournament = Tournament(**tourney_data)
                        db.session.add(tournament)
                        added_count += 1
                    processed_count += 1
                except KeyError as ke:
                    print(f"Ошибка при обработке турнира с FIDE: отсутствует поле {ke}")
                    continue
                except Exception as te:
                    print(f"Ошибка при добавлении турнира с FIDE: {te}")
                    continue
            
            try:
                db.session.commit()
                print(f"Обработано {processed_count} турниров с FIDE, добавлено {added_count} новых")
            except Exception as db_error:
                print(f"Ошибка при сохранении в базу: {db_error}")
                db.session.rollback()
                
        except Exception as e:
            print(f"Ошибка при получении данных с FIDE: {e}")
            import traceback
            traceback.print_exc()

    def _update_from_cfr(self):
        """Обновить данные с CFR"""
        print("Обновление данных с CFR...")
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
                        tournament = Tournament(**tourney_data)
                        db.session.add(tournament)
                        added_count += 1
                    processed_count += 1
                except KeyError as ke:
                    print(f"Ошибка при обработке турнира с CFR: отсутствует поле {ke}")
                    continue
                except Exception as te:
                    print(f"Ошибка при добавлении турнира с CFR: {te}")
                    continue
            
            try:
                db.session.commit()
                print(f"Обработано {processed_count} турниров с CFR, добавлено {added_count} новых")
            except Exception as db_error:
                print(f"Ошибка при сохранении в базу: {db_error}")
                db.session.rollback()
                
        except Exception as e:
            print(f"Ошибка при получении данных с CFR: {e}")
            import traceback
            traceback.print_exc()

    def start_scheduler(self):
        """Запустить планировщик обновлений"""
        # Обновление каждый день в 03:00
        schedule.every().day.at("03:00").do(self.update_all_sources)
        
        # Обновление каждые 6 часов
        schedule.every(6).hours.do(self.update_all_sources)
        
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Проверяем каждую минуту
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        print("Планировщик обновлений запущен")

# Глобальный экземпляр обновлятора
updater = TournamentUpdater()