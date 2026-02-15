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
        
        # Create sample tournaments
        sample_tournaments = [
            {
                'name': 'Чемпионат России по шахматам 2026',
                'start_date': date(2026, 3, 15),
                'end_date': date(2026, 3, 30),
                'location': 'Москва, Россия',
                'category': 'National',
                'status': 'Scheduled',
                'fide_id': None,
                'source_url': 'https://ruchess.ru'
            },
            {
                'name': 'Международный турнир памяти Чигорина',
                'start_date': date(2026, 5, 10),
                'end_date': date(2026, 5, 20),
                'location': 'Санкт-Петербург, Россия',
                'category': 'FIDE',
                'status': 'Scheduled',
                'fide_id': '12345',
                'source_url': 'https://calendar.fide.com'
            },
            {
                'name': 'Чемпионат Южного федерального округа',
                'start_date': date(2026, 4, 5),
                'end_date': date(2026, 4, 15),
                'location': 'Ростов-на-Дону, Россия',
                'category': 'National',
                'status': 'Scheduled',
                'fide_id': None,
                'source_url': 'https://ruchess.ru'
            },
            {
                'name': 'Кубок Москвы среди юниоров',
                'start_date': date(2026, 2, 20),
                'end_date': date(2026, 2, 25),
                'location': 'Москва, Россия',
                'category': 'Youth',
                'status': 'Ongoing',
                'fide_id': None,
                'source_url': 'https://ruchess.ru'
            },
            {
                'name': 'Турнир ветеранов России',
                'start_date': date(2026, 6, 1),
                'end_date': date(2026, 6, 10),
                'location': 'Сочи, Россия',
                'category': 'Seniors',
                'status': 'Scheduled',
                'fide_id': None,
                'source_url': 'https://ruchess.ru'
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