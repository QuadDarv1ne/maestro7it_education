import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from app.models.tournament import Tournament
import logging
import json
from urllib.parse import urljoin

logger = logging.getLogger('app.parsers')

class FIDEParses:
    def __init__(self):
        self.base_url = "https://calendar.fide.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.logger = logger  # Use centralized logger

    def get_tournaments_russia(self, year=2026):
        """Получить турниры в России на указанный год"""
        logger.info(f"Fetching FIDE tournaments for Russia, year {year}")
        
        # Strategy 1: Try direct API approach
        tournaments = self._try_direct_api(year)
        if tournaments:
            logger.info(f"Successfully fetched {len(tournaments)} tournaments via direct API")
            return tournaments
        
        # Strategy 2: Try different page formats
        tournaments = self._try_different_formats(year)
        if tournaments:
            logger.info(f"Successfully fetched {len(tournaments)} tournaments via alternative formats")
            return tournaments
        
        # Strategy 3: Try table view instead of tiles
        tournaments = self._try_table_view(year)
        if tournaments:
            logger.info(f"Successfully fetched {len(tournaments)} tournaments via table view")
            return tournaments
        
        # Strategy 4: Try year view
        tournaments = self._try_year_view(year)
        if tournaments:
            logger.info(f"Successfully fetched {len(tournaments)} tournaments via year view")
            return tournaments
        
        logger.warning(f"No tournaments found from FIDE for year {year}")
        return []
    
    def _try_direct_api(self, year):
        """Попытка получить данные через прямой API запрос"""
        try:
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
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            # Check if response contains JSON data
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                try:
                    json_data = response.json()
                    return self._parse_json_response(json_data)
                except json.JSONDecodeError:
                    pass
            
            # Check if it's actually HTML with embedded data
            if '<html' in response.text.lower() and 'ship' in response.text:
                # This is the JavaScript response we've been seeing
                logger.info("FIDE returned client-side rendered content, trying alternative approaches")
                return []
            
            # Try to parse as regular HTML
            return self._parse_tournaments_page(response.text)
            
        except Exception as e:
            logger.error(f"Direct API attempt failed: {e}")
            return []
    
    def _try_different_formats(self, year):
        """Попытка разных форматов отображения"""
        formats = ['list', 'table', 'cards']
        
        for fmt in formats:
            try:
                url = f"{self.base_url}/calendar.php"
                params = {
                    'name_filter': '',
                    'from_date': f'{year}-01-01',
                    'to_date': f'{year}-12-31',
                    'country': 'rus',
                    'show': fmt,
                    'page': 1
                }
                
                response = self.session.get(url, params=params, timeout=15)
                response.raise_for_status()
                
                if '<html' in response.text.lower() and 'ship' in response.text:
                    continue  # Skip JavaScript responses
                
                tournaments = self._parse_tournaments_page(response.text)
                if tournaments:
                    return tournaments
                    
            except Exception as e:
                logger.error(f"Format {fmt} attempt failed: {e}")
                continue
        
        return []
    
    def _try_table_view(self, year):
        """Попытка получить данные в табличном виде"""
        try:
            url = f"{self.base_url}/calendar.php"
            params = {
                'name_filter': '',
                'from_date': f'{year}-01-01',
                'to_date': f'{year}-12-31',
                'country': 'rus',
                'show': 'table',
                'page': 1
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            if '<html' in response.text.lower() and 'ship' in response.text:
                return []
            
            return self._parse_tournaments_page(response.text)
        except Exception as e:
            logger.error(f"Table view attempt failed: {e}")
            return []
    
    def _try_year_view(self, year):
        """Попытка получить данные в годовом виде"""
        try:
            url = f"{self.base_url}/calendar.php"
            params = {
                'name_filter': '',
                'year': year,
                'country': 'rus',
                'show': 'year',
                'page': 1
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            if '<html' in response.text.lower() and 'ship' in response.text:
                return []
            
            return self._parse_tournaments_page(response.text)
        except Exception as e:
            logger.error(f"Year view attempt failed: {e}")
            return []
    
    def _parse_json_response(self, json_data):
        """Парсинг JSON ответа"""
        tournaments = []
        try:
            # Handle different JSON structures
            if isinstance(json_data, list):
                items = json_data
            elif isinstance(json_data, dict) and 'events' in json_data:
                items = json_data['events']
            elif isinstance(json_data, dict) and 'tournaments' in json_data:
                items = json_data['tournaments']
            else:
                items = []
            
            for item in items:
                try:
                    tournament_data = self._extract_tournament_from_json(item)
                    if tournament_data and self._is_valid_russian_tournament(tournament_data):
                        tournaments.append(tournament_data)
                except Exception as e:
                    logger.error(f"Error parsing JSON tournament item: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing JSON response: {e}")
        
        return tournaments
    
    def _extract_tournament_from_json(self, item):
        """Извлечение данных турнира из JSON элемента"""
        try:
            # Handle various JSON field names
            name = (item.get('name') or item.get('title') or item.get('event_name') or '').strip()
            if not name:
                return None
            
            # Parse dates
            start_date_str = item.get('start_date') or item.get('date_start') or item.get('from')
            end_date_str = item.get('end_date') or item.get('date_end') or item.get('to')
            
            start_date, end_date = self._parse_json_dates(start_date_str, end_date_str)
            if not start_date:
                return None
            
            # Get location
            location = (item.get('location') or item.get('city') or item.get('place') or 'Russia').strip()
            
            # Get FIDE ID
            fide_id = item.get('id') or item.get('fide_id') or item.get('event_id')
            
            return {
                'name': name,
                'start_date': start_date,
                'end_date': end_date,
                'location': location,
                'category': 'FIDE',
                'status': 'Scheduled',
                'source_url': item.get('url') or '',
                'fide_id': str(fide_id) if fide_id else None
            }
        except Exception as e:
            logger.error(f"Error extracting tournament from JSON: {e}")
            return None
    
    def _parse_json_dates(self, start_date_str, end_date_str):
        """Парсинг дат из JSON"""
        try:
            from dateutil import parser
            
            if not start_date_str:
                return None, None
            
            start_date = parser.parse(str(start_date_str)).date()
            end_date = start_date
            
            if end_date_str:
                end_date = parser.parse(str(end_date_str)).date()
            
            return start_date, end_date
        except Exception:
            return None, None

    def _parse_tournaments_page(self, html_content):
        """Парсинг страницы с турнирами"""
        if not html_content or len(html_content.strip()) == 0:
            logger.warning("Empty HTML content received")
            return []
        
        # Check if this is JavaScript content
        if '<html' in html_content.lower() and 'ship' in html_content:
            logger.info("Received client-side rendered JavaScript content, cannot parse")
            return []
        
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
        except Exception as e:
            logger.error(f"Error parsing HTML: {e}")
            return []
        
        tournaments = []
        
        # Try multiple selector strategies
        selector_strategies = [
            # Strategy 1: Look for event/tournament containers
            {'tags': ['div', 'a'], 'class_pattern': re.compile(r'event|tournament|tile|card')},
            # Strategy 2: Look for calendar items
            {'tags': ['div', 'li'], 'class_pattern': re.compile(r'calendar|item|entry')},
            # Strategy 3: Look for general containers with data
            {'tags': ['div', 'article'], 'class_pattern': re.compile(r'container|content|main')}
        ]
        
        for strategy in selector_strategies:
            tournament_elements = soup.find_all(strategy['tags'], class_=strategy['class_pattern'])
            logger.info(f"Strategy {selector_strategies.index(strategy) + 1}: Found {len(tournament_elements)} potential tournament elements")
            
            if tournament_elements:
                for i, element in enumerate(tournament_elements):
                    try:
                        tournament_data = self._extract_tournament_data(element)
                        if tournament_data and self._is_valid_russian_tournament(tournament_data):
                            tournaments.append(tournament_data)
                    except Exception as e:
                        logger.error(f"Error parsing tournament element {i}: {e}", exc_info=True)
                        continue
                
                # If we found tournaments, break out of the loop
                if tournaments:
                    break
        
        # If no tournaments found with specific selectors, try a more general approach
        if not tournaments:
            logger.info("Trying general parsing approach")
            tournaments = self._parse_general_html(soup)
        
        logger.info(f"Successfully parsed {len(tournaments)} valid Russian tournaments")
        return tournaments
    
    def _parse_general_html(self, soup):
        """Общий парсинг HTML для поиска турниров"""
        tournaments = []
        
        # Look for links that might contain tournament information
        links = soup.find_all('a', href=True)
        
        for link in links:
            try:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Check if this looks like a tournament link
                if any(keyword in href.lower() or keyword in text.lower() 
                       for keyword in ['tournament', 'event', 'chess', 'fide', 'calendar']):
                    
                    # Extract FIDE ID from URL
                    fide_id_match = re.search(r'(?:id|event)=([\d]+)', href)
                    fide_id = fide_id_match.group(1) if fide_id_match else None
                    
                    if text and len(text) > 10:  # Reasonable tournament name length
                        tournament_data = {
                            'name': text[:100],  # Limit name length
                            'start_date': None,  # Will need to be set later
                            'end_date': None,
                            'location': 'Russia',  # Default assumption
                            'category': 'FIDE',
                            'status': 'Scheduled',
                            'source_url': urljoin(self.base_url, href) if href.startswith('/') else href,
                            'fide_id': fide_id
                        }
                        
                        if self._is_valid_russian_tournament(tournament_data):
                            tournaments.append(tournament_data)
            
            except Exception as e:
                logger.error(f"Error parsing general HTML element: {e}")
                continue
        
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