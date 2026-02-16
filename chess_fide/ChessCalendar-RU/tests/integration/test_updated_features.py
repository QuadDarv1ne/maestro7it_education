#!/usr/bin/env python3
"""
Test script to verify the updated features in ChessCalendar-RU
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.tournament import Tournament
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser
from app.utils.updater import updater
from datetime import datetime

def test_parsers():
    """Test the updated parsers"""
    print("Testing FIDE Parser...")
    fide_parser = FIDEParses()
    try:
        fide_tournaments = fide_parser.get_tournaments_russia(2026)
        print(f"FIDE parser returned {len(fide_tournaments)} tournaments")
        
        # Test flexible date parsing
        if fide_tournaments:
            print(f"Sample tournament: {fide_tournaments[0]['name']}")
            print(f"Start date: {fide_tournaments[0]['start_date']}")
            print(f"End date: {fide_tournaments[0]['end_date']}")
    except Exception as e:
        print(f"Error in FIDE parser: {e}")

    print("\nTesting CFR Parser...")
    cfr_parser = CFRParser()
    try:
        cfr_tournaments = cfr_parser.get_tournaments(2026)
        print(f"CFR parser returned {len(cfr_tournaments)} tournaments")
        
        # Test flexible date parsing
        if cfr_tournaments:
            print(f"Sample tournament: {cfr_tournaments[0]['name']}")
            print(f"Start date: {cfr_tournaments[0]['start_date']}")
            print(f"End date: {cfr_tournaments[0]['end_date']}")
    except Exception as e:
        print(f"Error in CFR parser: {e}")

def test_updater():
    """Test the updated updater"""
    print("\nTesting Tournament Updater...")
    try:
        # This will run the update process
        updater.update_all_sources()
        print("Update process completed successfully")
    except Exception as e:
        print(f"Error in updater: {e}")

def test_database():
    """Test database operations"""
    print("\nTesting Database Operations...")
    try:
        app = create_app()
        with app.app_context():
            # Count tournaments
            total_tournaments = Tournament.query.count()
            print(f"Total tournaments in database: {total_tournaments}")
            
            # Show recent tournaments
            recent_tournaments = Tournament.query.order_by(Tournament.created_at.desc()).limit(5).all()
            print(f"\nRecent 5 tournaments:")
            for t in recent_tournaments:
                print(f"  - {t.name} ({t.start_date} to {t.end_date}) - {t.category}")
                
            # Test validation on a sample tournament
            if recent_tournaments:
                sample_tournament = recent_tournaments[0]
                validation_errors = sample_tournament.validate()
                print(f"\nValidation errors for sample tournament: {len(validation_errors)}")
                if validation_errors:
                    for error in validation_errors:
                        print(f"  - {error}")
                        
    except Exception as e:
        print(f"Error in database test: {e}")

def main():
    print("Starting tests for updated ChessCalendar-RU features...")
    print("="*60)
    
    test_parsers()
    print("="*60)
    test_updater()
    print("="*60)
    test_database()
    print("="*60)
    
    print("Tests completed!")

if __name__ == "__main__":
    main()