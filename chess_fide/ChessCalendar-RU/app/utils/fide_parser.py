import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from app.models.tournament import Tournament
import logging

class FIDEParses:
    def __init__(self):
        self.base_url = "https://calendar.fide.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.logger = logging.getLogger(__name__)

    def get_tournaments_russia(self, year=2026):
        """Получить турниры в России на указанный год"""
        url = f"{self.base_url}/calendar.php"
        params = {
            'name_filter': '',
            'from_date': f'{year}-01-01',
            'to_date': f'{year}-12-31',
            'country': 'rus',
            'show': 'tiles',
            'page': 1,
            'cat_filter': '',
            'cat_cont': 0,
            'event_type': 'undefined',
            'time_control': 'undefined'
        }
        
        try:
            self.logger.info(f"Fetching FIDE tournaments for Russia, year {year}")
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            tournaments = self._parse_tournaments_page(response.text)
            self.logger.info(f"Successfully fetched {len(tournaments)} tournaments from FIDE")
            return tournaments
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout error when fetching FIDE data for year {year}")
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error when fetching FIDE data: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error when fetching FIDE data: {e}")
            return []

    def _parse_tournaments_page(self, html_content):
        """Парсинг страницы с турнирами"""
        soup = BeautifulSoup(html_content, 'html.parser')
        tournaments = []
        
        # Ищем элементы с информацией о турнирах
        tournament_elements = soup.find_all(['div', 'a'], class_=re.compile(r'event|tournament|tile'))
        
        self.logger.info(f"Found {len(tournament_elements)} potential tournament elements")
        
        for i, element in enumerate(tournament_elements):
            try:
                tournament_data = self._extract_tournament_data(element)
                if tournament_data and self._is_valid_russian_tournament(tournament_data):
                    tournaments.append(tournament_data)
            except Exception as e:
                self.logger.error(f"Error parsing tournament element {i}: {e}", exc_info=True)
                continue
                
        self.logger.info(f"Successfully parsed {len(tournaments)} valid Russian tournaments")
        return tournaments

    def _extract_tournament_data(self, element):
        """Извлечение данных о турнире из элемента"""
        # Примерная реализация - нужно адаптировать под реальную структуру страницы
        name_element = element.find(['h3', 'h4', 'span'], class_=re.compile(r'name|title'))
        date_element = element.find(['span', 'div'], class_=re.compile(r'date|time'))
        location_element = element.find(['span', 'div'], class_=re.compile(r'location|place'))
        
        if not name_element:
            return None
            
        name = name_element.get_text(strip=True)
        dates = date_element.get_text(strip=True) if date_element else ""
        location = location_element.get_text(strip=True) if location_element else "Russia"
        
        # Парсинг дат
        start_date, end_date = self._parse_dates(dates)
        
        return {
            'name': name,
            'start_date': start_date,
            'end_date': end_date,
            'location': location,
            'category': 'FIDE',
            'status': 'Scheduled',
            'source_url': element.get('href', ''),
            'fide_id': self._extract_fide_id(element)
        }

    def _parse_dates(self, date_string):
        """Парсинг строки с датами"""
        # Пример: "27 February - 6 March 2026"
        try:
            # Упрощенная реализация
            import dateutil.parser
            if '-' in date_string:
                dates = date_string.split('-')
                start_date = dateutil.parser.parse(dates[0].strip())
                end_date = dateutil.parser.parse(dates[1].strip())
                return start_date.date(), end_date.date()
            else:
                start_date = dateutil.parser.parse(date_string.strip())
                return start_date.date(), start_date.date()
        except:
            return None, None

    def _is_valid_russian_tournament(self, tournament_data):
        """Проверка, что турнир проходит в России"""
        russian_locations = ['moscow', 'москва', 'st. petersburg', 'санкт-петербург', 
                           'ekaterinburg', 'екатеринбург', 'kazan', 'казань', 
                           'sochi', 'сочи', 'russia', 'россия']
        
        location = tournament_data.get('location', '').lower()
        return any(loc in location for loc in russian_locations)

    def _extract_fide_id(self, element):
        """Извлечение FIDE ID из элемента"""
        href = element.get('href', '')
        # Ищем ID в URL вида ?id=12345
        match = re.search(r'id=(\d+)', href)
        return match.group(1) if match else None