#!/usr/bin/env python3
"""Script to populate database with sample tournament data"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.tournament import Tournament
from datetime import date

def create_sample_data():
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        Tournament.query.delete()
        
        # Create sample tournaments with more diverse and realistic data
        sample_tournaments = [
            {
                'name': 'Чемпионат мира по шахматам 2026',
                'start_date': date(2026, 4, 15),
                'end_date': date(2026, 5, 5),
                'location': 'Москва, Россия',
                'category': 'World Championship',
                'status': 'Scheduled',
                'fide_id': 'WCH2026',
                'source_url': 'https://fide.com',
                'prize_fund_usd': 2000000,
                'players_count': 16,
                'time_control': 'Classical'
            },
            {
                'name': 'Чемпионат России по классическим шахматам 2026',
                'start_date': date(2026, 3, 10),
                'end_date': date(2026, 3, 25),
                'location': 'Санкт-Петербург, Россия',
                'category': 'National Championship',
                'status': 'Scheduled',
                'fide_id': 'RUS2026',
                'source_url': 'https://ruchess.ru',
                'prize_fund_usd': 250000,
                'players_count': 128,
                'time_control': 'Classical'
            },
            {
                'name': 'Кубок России по быстрым шахматам 2026',
                'start_date': date(2026, 5, 20),
                'end_date': date(2026, 5, 25),
                'location': 'Нижний Новгород, Россия',
                'category': 'Rapid & Blitz',
                'status': 'Scheduled',
                'fide_id': 'RUS-RB-2026',
                'source_url': 'https://ruchess.ru',
                'prize_fund_usd': 150000,
                'players_count': 64,
                'time_control': 'Rapid & Blitz'
            },
            {
                'name': 'Международный турнир "Кубок Сибири" 2026',
                'start_date': date(2026, 6, 1),
                'end_date': date(2026, 6, 10),
                'location': 'Новосибирск, Россия',
                'category': 'Open International',
                'status': 'Scheduled',
                'fide_id': 'SIBERIA2026',
                'source_url': 'https://chesstour.ru',
                'prize_fund_usd': 100000,
                'players_count': 120,
                'time_control': 'Classical'
            },
            {
                'name': 'Турнир претендентов FIDE 2026',
                'start_date': date(2026, 7, 5),
                'end_date': date(2026, 7, 25),
                'location': 'Мадрид, Испания',
                'category': 'FIDE Candidates',
                'status': 'Scheduled',
                'fide_id': 'FIDE-CAND-2026',
                'source_url': 'https://fide.com',
                'prize_fund_usd': 500000,
                'players_count': 8,
                'time_control': 'Classical'
            },
            {
                'name': 'Чемпионат России по блиц-шахматам 2026',
                'start_date': date(2026, 8, 15),
                'end_date': date(2026, 8, 17),
                'location': 'Екатеринбург, Россия',
                'category': 'Blitz Championship',
                'status': 'Scheduled',
                'fide_id': 'RUS-BLITZ-2026',
                'source_url': 'https://ruchess.ru',
                'prize_fund_usd': 80000,
                'players_count': 150,
                'time_control': 'Blitz'
            },
            {
                'name': 'Международный женский турнир "Кубок Европы" 2026',
                'start_date': date(2026, 9, 10),
                'end_date': date(2026, 9, 20),
                'location': 'Бухарест, Румыния',
                'category': 'Women\'s Open',
                'status': 'Scheduled',
                'fide_id': 'WOMEN-EUROPE-2026',
                'source_url': 'https://fide.com',
                'prize_fund_usd': 120000,
                'players_count': 96,
                'time_control': 'Classical'
            },
            {
                'name': 'Юношеский чемпионат России U16 2026',
                'start_date': date(2026, 10, 5),
                'end_date': date(2026, 10, 12),
                'location': 'Казань, Россия',
                'category': 'Youth Championship',
                'status': 'Scheduled',
                'fide_id': 'YOUTH-RUS-2026',
                'source_url': 'https://ruchess.ru',
                'prize_fund_usd': 30000,
                'players_count': 200,
                'time_control': 'Classical'
            },
            {
                'name': 'Открытый турнир памяти Александра Алехина 2026',
                'start_date': date(2026, 11, 1),
                'end_date': date(2026, 11, 10),
                'location': 'Париж, Франция',
                'category': 'Historic Memorial',
                'status': 'Scheduled',
                'fide_id': 'ALEKHINE-2026',
                'source_url': 'https://chesspro.ru',
                'prize_fund_usd': 300000,
                'players_count': 128,
                'time_control': 'Classical'
            },
            {
                'name': 'Турнир ветеранов СНГ 2026',
                'start_date': date(2026, 12, 15),
                'end_date': date(2026, 12, 22),
                'location': 'Тбилиси, Грузия',
                'category': 'Senior Championship',
                'status': 'Scheduled',
                'fide_id': 'SENIOR-CIS-2026',
                'source_url': 'https://chesstour.ge',
                'prize_fund_usd': 40000,
                'players_count': 80,
                'time_control': 'Classical'
            }
        ]
        
        # Add tournaments to database
        for tournament_data in sample_tournaments:
            tournament = Tournament(**tournament_data)
            db.session.add(tournament)
        
        # Commit changes
        db.session.commit()
        print(f"Successfully added {len(sample_tournaments)} sample tournaments to database")

if __name__ == "__main__":
    create_sample_data()