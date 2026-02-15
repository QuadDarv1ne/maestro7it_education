#!/usr/bin/env python3
"""Debug search functionality"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.tournament import Tournament

def debug_search():
    app = create_app()
    
    with app.app_context():
        print("All tournaments in database:")
        all_tournaments = Tournament.query.all()
        for t in all_tournaments:
            print(f"ID: {t.id}, Name: {t.name}, Location: {t.location}")
        
        print("\nTesting search for 'Москва':")
        results = Tournament.query.filter(
            db.or_(
                Tournament.name.contains('Москва'),
                Tournament.location.contains('Москва')
            )
        ).all()
        print(f"Found {len(results)} results")
        for t in results:
            print(f"  - {t.name} in {t.location}")
        
        print("\nTesting search for 'Кубок':")
        results = Tournament.query.filter(
            db.or_(
                Tournament.name.contains('Кубок'),
                Tournament.location.contains('Кубок')
            )
        ).all()
        print(f"Found {len(results)} results")
        for t in results:
            print(f"  - {t.name} in {t.location}")

if __name__ == "__main__":
    debug_search()