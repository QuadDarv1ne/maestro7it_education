import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from app.models.tournament import Tournament
import logging
import random
from urllib.parse import urljoin

logger = logging.getLogger('app.parsers')

class CFRParser:
    def __init__(self):
        self.base_url = "https://ruchess.ru"
        self.logger = logging.getLogger(__name__)
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1'
        ]
        self.session = self._create_session()
    
    def _create_session(self):
        """Создание сессии с ротацией User-Agent"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        return session

    def get_tournaments(self, year=2026):
        """Получить турниры с сайта Федерации шахмат России"""
        self.logger.info(f"Fetching CFR tournaments for year {year}")
        
        # Strategy 1: Try direct access with different sessions
        tournaments = self._try_direct_access(year)
        if tournaments:
            self.logger.info(f"Successfully fetched {len(tournaments)} tournaments via direct access")
            return tournaments
        
        # Strategy 2: Try alternative URLs and paths
        tournaments = self._try_alternative_paths(year)
        if tournaments:
            self.logger.info(f"Successfully fetched {len(tournaments)} tournaments via alternative paths")
            return tournaments
        
        # Strategy 3: Try to find tournaments in main page content
        tournaments = self._try_main_page_scraping(year)
        if tournaments:
            self.logger.info(f"Successfully fetched {len(tournaments)} tournaments via main page scraping")
            return tournaments
        
        # Strategy 4: Try to find tournament links in navigation
        tournaments = self._try_navigation_scraping(year)
        if tournaments:
            self.logger.info(f"Successfully fetched {len(tournaments)} tournaments via navigation scraping")
            return tournaments
        
        self.logger.warning(f"No tournaments found from CFR for year {year}")
        return []
    
    def _try_direct_access(self, year):
        """Попытка прямого доступа с различными сессиями"""
        urls = [
            f"{self.base_url}/",
            f"{self.base_url}/championship/",
            f"{self.base_url}/tournaments/",
            f"{self.base_url}/news/",
            f"{self.base_url}/events/"
        ]
        
        tournaments = []
        
        for url in urls:
            try:
                # Try with fresh session for each URL
                self.session = self._create_session()
                page_tournaments = self._parse_page(url, year)
                if page_tournaments:
                    tournaments.extend(page_tournaments)
                    self.logger.info(f"Fetched {len(page_tournaments)} tournaments from {url}")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    self.logger.info(f"403 Forbidden for {url}, trying alternative approach")
                    continue
                else:
                    self.logger.error(f"HTTP error for {url}: {e}")
                    continue
            except Exception as e:
                self.logger.error(f"Error parsing {url}: {e}", exc_info=True)
                continue
        
        return tournaments
    
    def _try_alternative_paths(self, year):
        """Попытка альтернативных путей"""
        # Try common Russian chess website patterns
        alternative_paths = [
            '/championships/',
            '/competitions/',
            '/calendar/',
            '/events/calendar/',
            '/news/tournaments/',
            '/chess-news/',
            '/turniry/',  # Russian word for tournaments
            '/chempionaty/'  # Russian word for championships
        ]
        
        tournaments = []
        
        for path in alternative_paths:
            try:
                url = urljoin(self.base_url, path)
                self.session = self._create_session()
                page_tournaments = self._parse_page(url, year)
                if page_tournaments:
                    tournaments.extend(page_tournaments)
                    self.logger.info(f"Fetched {len(page_tournaments)} tournaments from {url}")
            except Exception as e:
                self.logger.error(f"Error with alternative path {path}: {e}")
                continue
        
        return tournaments
    
    def _try_main_page_scraping(self, year):
        """Попытка извлечения из главной страницы"""
        try:
            self.session = self._create_session()
            response = self.session.get(self.base_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            tournaments = []
            
            # Look for any links that might contain tournament information
            links = soup.find_all('a', href=True)
            
            for link in links:
                try:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    
                    # Check for tournament-related keywords in Russian and English
                    tournament_keywords = ['турнир', 'чемпионат', 'турниры', 'championship', 'tournament', 'competition']
                    
                    if any(keyword in href.lower() or keyword in text.lower() for keyword in tournament_keywords):
                        # Try to access the tournament page
                        full_url = urljoin(self.base_url, href) if href.startswith('/') else href
                        if full_url != self.base_url:  # Avoid infinite loop
                            try:
                                page_tournaments = self._parse_page(full_url, year)
                                if page_tournaments:
                                    tournaments.extend(page_tournaments)
                            except Exception:
                                continue
                except Exception as e:
                    self.logger.error(f"Error processing main page link: {e}")
                    continue
            
            return tournaments
        except Exception as e:
            self.logger.error(f"Error scraping main page: {e}")
            return []
    
    def _try_navigation_scraping(self, year):
        """Попытка извлечения из навигационного меню"""
        try:
            self.session = self._create_session()
            response = self.session.get(self.base_url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            tournaments = []
            
            # Look for navigation elements
            nav_elements = soup.find_all(['nav', 'ul', 'div'], class_=re.compile(r'menu|nav|navigation'))
            
            for nav in nav_elements:
                links = nav.find_all('a', href=True)
                for link in links:
                    try:
                        href = link.get('href', '')
                        text = link.get_text(strip=True)
                        
                        # Check for tournament-related navigation items
                        if any(keyword in text.lower() for keyword in ['турниры', 'чемпионаты', 'календарь', 'tournaments', 'calendar']):
                            full_url = urljoin(self.base_url, href) if href.startswith('/') else href
                            if full_url != self.base_url:
                                try:
                                    page_tournaments = self._parse_page(full_url, year)
                                    if page_tournaments:
                                        tournaments.extend(page_tournaments)
                                except Exception:
                                    continue
                    except Exception as e:
                        self.logger.error(f"Error processing navigation link: {e}")
                        continue
            
            return tournaments
        except Exception as e:
            self.logger.error(f"Error scraping navigation: {e}")
            return []

    def _parse_page(self, url, year):
        """Парсинг страницы CFR"""
        try:
            self.logger.info(f"Parsing CFR page: {url}")
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            tournaments = []
            
            # Ищем элементы с информацией о турнирах
            # Адаптируем под реальную структуру сайта
            tournament_elements = soup.find_all(['div', 'article', 'li'], 
                                              class_=re.compile(r'tournament|event|competition'))
            
            self.logger.info(f"Found {len(tournament_elements)} potential tournament elements on {url}")
            
            for i, element in enumerate(tournament_elements):
                try:
                    tournament_data = self._extract_tournament_data(element, year)
                    if tournament_data:
                        tournaments.append(tournament_data)
                except Exception as e:
                    self.logger.error(f"Error extracting tournament {i} from {url}: {e}", exc_info=True)
                    continue
                    
            self.logger.info(f"Successfully extracted {len(tournaments)} tournaments from {url}")
            return tournaments
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout error when fetching page {url}")
            return []
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error when fetching page {url}: {e}")
            return []
        except Exception as e:
            self.logger.error(f"Error fetching page {url}: {e}", exc_info=True)
            return []

    def _extract_tournament_data(self, element, year):
        """Извлечение данных о турнире"""
        # Ищем название
        name_element = element.find(['h1', 'h2', 'h3', 'h4', 'span', 'div'], 
                                  class_=re.compile(r'title|name|heading|tournament|event'))
        if not name_element:
            # Try to find text that looks like a tournament name
            text_content = element.get_text(strip=True)
            # Look for text that might be a tournament name
            possible_names = element.find_all(text=re.compile(r'[ШшAa][АаAa][ХхXx][МмMm][АаAa][ТтTt][ЫыYy]', re.IGNORECASE))
            if possible_names:
                name = possible_names[0].strip()
            else:
                return None
        else:
            name = name_element.get_text(strip=True)
            
        # Ищем даты
        date_element = element.find(['span', 'div', 'time', 'p'], 
                                  class_=re.compile(r'date|time|period|calendar|when'))
        if not date_element:
            # Try to find dates in the text content
            text_content = element.get_text(strip=True)
            date_patterns = [
                r'\d{1,2}[.-]\d{1,2}[.-]\d{4}',  # DD.MM.YYYY or DD-MM-YYYY
                r'\d{1,2}\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',  # DD Month YYYY
                r'(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря|January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',  # Month YYYY
            ]
            for pattern in date_patterns:
                matches = re.findall(pattern, text_content)
                if matches:
                    dates_text = matches[0]
                    break
            else:
                dates_text = ""
        else:
            dates_text = date_element.get_text(strip=True)
            
        # Ищем место проведения
        location_element = element.find(['span', 'div', 'p'], 
                                      class_=re.compile(r'location|place|city|region|venue|address|area'))
        if not location_element:
            # Try to find location in text
            text_content = element.get_text(strip=True)
            location_matches = re.findall(r'(Москва|Санкт-Петербург|Московская|СПб|Казань|Екатеринбург|Новосибирск|Нижний Новгород|Красноярск|Самара|Волгоград|Воронеж|Ростов-на-Дону|Сочи|Калининград)', text_content)
            if location_matches:
                location = location_matches[0]
            else:
                location = "Russia"
        else:
            location = location_element.get_text(strip=True)
            
        # Ищем дополнительную информацию
        description_element = element.find(['p', 'div', 'span'], 
                                         class_=re.compile(r'description|desc|info|text|content'))
        description = description_element.get_text(strip=True) if description_element else ""
            
        # Ищем организатора
        organizer_element = element.find(['p', 'div', 'span'], 
                                       class_=re.compile(r'organizer|organiser|org|committee'))
        organizer = organizer_element.get_text(strip=True) if organizer_element else ""
            
        # Ищем призовой фонд
        prize_element = element.find(['p', 'div', 'span'], 
                                   class_=re.compile(r'prize|fund|money|award|cash'))
        prize_fund_text = prize_element.get_text(strip=True) if prize_element else ""
        prize_fund_match = re.search(r'(\d+[\s\d]*(тыс\.?\s*руб|руб|USD|RUB|EUR|€|$|\$))', prize_fund_text)
        prize_fund = prize_fund_match.group(1) if prize_fund_match else ""
            
        # Парсинг дат
        start_date, end_date = self._parse_dates(dates_text, year)
            
        if not start_date:
            return None
                
        # Ищем URL источника
        link_element = element.find('a', href=True)
        source_url = link_element['href'] if link_element else ''
        if source_url and not source_url.startswith('http'):
            source_url = urljoin(self.base_url, source_url)
            
        return {
            'name': name,
            'start_date': start_date,
            'end_date': end_date or start_date,
            'location': location,
            'category': 'National',
            'status': 'Scheduled',
            'description': description,
            'prize_fund': prize_fund,
            'organizer': organizer,
            'source_url': source_url,
            'fide_id': None
        }

    def _parse_dates(self, date_string, year):
        """Парсинг дат из строки"""
        if not date_string:
            return None, None
            
        try:
            import dateutil.parser
            from datetime import datetime
            import calendar
            
            # Примеры форматов: "15-20 марта 2026", "Март 2026", "15.03.2026"
            # Handle different Russian month name cases (nominative and genitive)
            date_string = date_string.replace('января', 'January').replace('Января', 'January').replace('январь', 'January').replace('Январь', 'January')
            date_string = date_string.replace('февраля', 'February').replace('Февраля', 'February').replace('февраль', 'February').replace('Февраль', 'February')
            date_string = date_string.replace('марта', 'March').replace('Марта', 'March').replace('март', 'March').replace('Март', 'March')
            date_string = date_string.replace('апреля', 'April').replace('Апреля', 'April').replace('апрель', 'April').replace('Апрель', 'April')
            date_string = date_string.replace('мая', 'May').replace('Мая', 'May').replace('май', 'May').replace('Май', 'May')
            date_string = date_string.replace('июня', 'June').replace('Июня', 'June').replace('июнь', 'June').replace('Июнь', 'June')
            date_string = date_string.replace('июля', 'July').replace('Июля', 'July').replace('июль', 'July').replace('Июль', 'July')
            date_string = date_string.replace('августа', 'August').replace('Августа', 'August').replace('август', 'August').replace('Август', 'August')
            date_string = date_string.replace('сентября', 'September').replace('Сентября', 'September').replace('сентябрь', 'September').replace('Сентябрь', 'September')
            date_string = date_string.replace('октября', 'October').replace('Октября', 'October').replace('октябрь', 'October').replace('Октябрь', 'October')
            date_string = date_string.replace('ноября', 'November').replace('Ноября', 'November').replace('ноябрь', 'November').replace('Ноябрь', 'November')
            date_string = date_string.replace('декабря', 'December').replace('Декабря', 'December').replace('декабрь', 'December').replace('Декабрь', 'December')
            
            # Handle different date formats
            if '-' in date_string:
                # Диапазон дат, например "15-20 March 2026"
                parts = date_string.split('-')
                if len(parts) == 2:
                    start_part = parts[0].strip()
                    end_part = parts[1].strip()
                    
                    # Extract day numbers
                    start_day_match = re.search(r'(\d+)', start_part)
                    end_day_match = re.search(r'(\d+)', end_part)
                    
                    if start_day_match and end_day_match:
                        start_day = int(start_day_match.group(1))
                        end_day = int(end_day_match.group(1))
                        
                        # Extract month and year from end_part
                        month_year_match = re.search(r'([A-Za-z]+)\s+(\d{4})', end_part)
                        if month_year_match:
                            month_name = month_year_match.group(1)
                            year_num = int(month_year_match.group(2))
                            
                            # Create start and end dates
                            month_num = datetime.strptime(month_name, '%B').month
                            start_date = datetime(year_num, month_num, start_day)
                            end_date = datetime(year_num, month_num, end_day)
                            
                            return start_date.date(), end_date.date()
                        
                    # Fallback: try to parse the individual parts
                    try:
                        start_date = dateutil.parser.parse(f"{start_part} {year}")
                        end_date = dateutil.parser.parse(f"{end_part} {year}")
                        return start_date.date(), end_date.date()
                    except:
                        pass
            
            if '.' in date_string:
                # Format DD.MM.YYYY
                try:
                    date_obj = datetime.strptime(date_string, '%d.%m.%Y')
                    return date_obj.date(), date_obj.date()
                except ValueError:
                    pass
            
            # Handle month-year format like "March 2026" -> first and last day of month
            # First check if the date_string already contains the year
            month_year_pattern = re.match(r'^([A-Za-z]+)\s+(\d{4})$', date_string.strip())
            if month_year_pattern:
                month_name = month_year_pattern.group(1)
                year_num = int(month_year_pattern.group(2))
                
                try:
                    month_num = datetime.strptime(month_name, '%B').month
                    last_day = calendar.monthrange(year_num, month_num)[1]
                    
                    start_date = datetime(year_num, month_num, 1)
                    end_date = datetime(year_num, month_num, last_day)
                    
                    return start_date.date(), end_date.date()
                except ValueError:
                    pass
            else:
                # Check if the date_string is just a month name, then append the provided year
                month_only_pattern = re.match(r'^([A-Za-z]+)$', date_string.strip())
                if month_only_pattern:
                    month_name = month_only_pattern.group(1)
                    try:
                        month_num = datetime.strptime(month_name, '%B').month
                        last_day = calendar.monthrange(year, month_num)[1]
                        
                        start_date = datetime(year, month_num, 1)
                        end_date = datetime(year, month_num, last_day)
                        
                        return start_date.date(), end_date.date()
                    except ValueError:
                        pass
            
            # Single date format
            try:
                date_obj = dateutil.parser.parse(f"{date_string} {year}")
                return date_obj.date(), date_obj.date()
            except:
                pass
                
            # If all parsing attempts fail
            self.logger.error(f"Could not parse date string: '{date_string}'")
            return None, None
                
        except Exception as e:
            self.logger.error(f"Error parsing dates '{date_string}': {e}", exc_info=True)
            return None, None