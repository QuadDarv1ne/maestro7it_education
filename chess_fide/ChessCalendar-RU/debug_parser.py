#!/usr/bin/env python3
"""Debug script to test parsers"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser

def test_parsers():
    print("Testing FIDE parser...")
    try:
        fide_parser = FIDEParses()
        fide_tournaments = fide_parser.get_tournaments_russia(2026)
        print(f"FIDE tournaments found: {len(fide_tournaments)}")
        for i, t in enumerate(fide_tournaments[:3]):  # Show first 3
            print(f"  {i+1}. {t.name} - {t.start_date} to {t.end_date} in {t.location}")
    except Exception as e:
        print(f"FIDE parser error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nTesting CFR parser...")
    try:
        cfr_parser = CFRParser()
        cfr_tournaments = cfr_parser.get_tournaments()
        print(f"CFR tournaments found: {len(cfr_tournaments)}")
        for i, t in enumerate(cfr_tournaments[:3]):  # Show first 3
            print(f"  {i+1}. {t.name} - {t.start_date} to {t.end_date} in {t.location}")
    except Exception as e:
        print(f"CFR parser error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_parsers()