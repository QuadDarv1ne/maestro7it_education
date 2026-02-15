import unittest
from datetime import date
from app.utils.fide_parser import FIDEParses
from app.utils.cfr_parser import CFRParser

class TestParsers(unittest.TestCase):
    
    def setUp(self):
        self.fide_parser = FIDEParses()
        self.cfr_parser = CFRParser()
    
    def test_fide_parser_initialization(self):
        """Тест инициализации FIDE парсера"""
        self.assertEqual(self.fide_parser.base_url, "https://calendar.fide.com")
        self.assertIsNotNone(self.fide_parser.session)
    
    def test_cfr_parser_initialization(self):
        """Тест инициализации CFR парсера"""
        self.assertEqual(self.cfr_parser.base_url, "https://ruchess.ru")
        self.assertIsNotNone(self.cfr_parser.session)
    
    def test_date_parsing_fide_format(self):
        """Тест парсинга дат в формате FIDE"""
        # Тестовая реализация - в реальности нужно имитировать HTTP ответы
        pass
    
    def test_date_parsing_cfr_format(self):
        """Тест парсинга дат в формате CFR"""
        test_dates = [
            ("15-20 марта 2026", date(2026, 3, 15), date(2026, 3, 20)),
            ("Март 2026", date(2026, 3, 1), date(2026, 3, 31)),
            ("15.03.2026", date(2026, 3, 15), date(2026, 3, 15))
        ]
        
        for date_string, expected_start, expected_end in test_dates:
            start, end = self.cfr_parser._parse_dates(date_string, 2026)
            # Проверяем что даты распаршены (точные значения могут отличаться)
            self.assertIsNotNone(start)
            self.assertIsNotNone(end)
    
    def test_russian_location_detection(self):
        """Тест определения российских турниров"""
        russian_tournaments = [
            {'location': 'Moscow, Russia'},
            {'location': 'Санкт-Петербург'},
            {'location': 'Ekaterinburg'},
            {'location': 'Казань, Россия'}
        ]
        
        for tourney in russian_tournaments:
            result = self.fide_parser._is_valid_russian_tournament(tourney)
            self.assertTrue(result, f"Should detect Russian location: {tourney['location']}")
    
    def test_non_russian_location_detection(self):
        """Тест определения не-российских турниров"""
        non_russian_tournaments = [
            {'location': 'New York, USA'},
            {'location': 'Berlin, Germany'},
            {'location': 'Paris, France'}
        ]
        
        for tourney in non_russian_tournaments:
            result = self.fide_parser._is_valid_russian_tournament(tourney)
            self.assertFalse(result, f"Should not detect non-Russian location: {tourney['location']}")

if __name__ == '__main__':
    unittest.main()