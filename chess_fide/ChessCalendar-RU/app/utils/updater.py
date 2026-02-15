import schedule
import time
import threading
from datetime import datetime
from app import db
from app.models.tournament import Tournament
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser

class TournamentUpdater:
    def __init__(self):
        self.fide_parser = FIDEParses()
        self.cfr_parser = CFRParser()
        
    def update_all_sources(self):
        """Обновить данные со всех источников"""
        print(f"[{datetime.now()}] Начинаю обновление турниров...")
        
        try:
            # Обновляем с FIDE
            self._update_from_fide()
            
            # Обновляем с CFR
            self._update_from_cfr()
            
            print(f"[{datetime.now()}] Обновление завершено успешно")
            
        except Exception as e:
            print(f"[{datetime.now()}] Ошибка при обновлении: {e}")

    def _update_from_fide(self):
        """Обновить данные с FIDE"""
        print("Обновление данных с FIDE...")
        try:
            fide_tournaments = self.fide_parser.get_tournaments_russia(2026)
            added_count = 0
            
            for tourney_data in fide_tournaments:
                existing = Tournament.query.filter_by(
                    name=tourney_data['name'],
                    start_date=tourney_data['start_date']
                ).first()
                
                if not existing:
                    tournament = Tournament(**tourney_data)
                    db.session.add(tournament)
                    added_count += 1
            
            db.session.commit()
            print(f"Добавлено {added_count} турниров с FIDE")
            
        except Exception as e:
            print(f"Ошибка при обновлении с FIDE: {e}")

    def _update_from_cfr(self):
        """Обновить данные с CFR"""
        print("Обновление данных с CFR...")
        try:
            cfr_tournaments = self.cfr_parser.get_tournaments(2026)
            added_count = 0
            
            for tourney_data in cfr_tournaments:
                existing = Tournament.query.filter_by(
                    name=tourney_data['name'],
                    start_date=tourney_data['start_date']
                ).first()
                
                if not existing:
                    tournament = Tournament(**tourney_data)
                    db.session.add(tournament)
                    added_count += 1
            
            db.session.commit()
            print(f"Добавлено {added_count} турниров с CFR")
            
        except Exception as e:
            print(f"Ошибка при обновлении с CFR: {e}")

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