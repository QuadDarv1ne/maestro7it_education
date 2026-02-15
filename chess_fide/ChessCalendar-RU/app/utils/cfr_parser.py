import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from app.models.tournament import Tournament
import logging

logger = logging.getLogger('app.parsers')

class CFRParser:
    def __init__(self):
        self.base_url = "https://ruchess.ru"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.logger = logging.getLogger(__name__)

    def get_tournaments(self, year=2026):
        """Получить турниры с сайта Федерации шахмат России"""
        tournaments = []
        
        # Попробуем несколько возможных URL
        urls = [
            f"{self.base_url}/",
            f"{self.base_url}/championship/",
            f"{self.base_url}/tournaments/"
        ]
        
        self.logger.info(f"Fetching CFR tournaments for year {year}")
        
        for url in urls:
            try:
                page_tournaments = self._parse_page(url, year)
                tournaments.extend(page_tournaments)
                self.logger.info(f"Fetched {len(page_tournaments)} tournaments from {url}")
            except Exception as e:
                self.logger.error(f"Error parsing {url}: {e}", exc_info=True)
                continue
                
        self.logger.info(f"Total CFR tournaments fetched: {len(tournaments)}")
        return tournaments

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
                                  class_=re.compile(r'title|name|heading'))
        if not name_element:
            return None
            
        name = name_element.get_text(strip=True)
        
        # Ищем даты
        date_element = element.find(['span', 'div', 'time'], 
                                  class_=re.compile(r'date|time|period'))
        dates_text = date_element.get_text(strip=True) if date_element else ""
        
        # Ищем место проведения
        location_element = element.find(['span', 'div'], 
                                      class_=re.compile(r'location|place|city'))
        location = location_element.get_text(strip=True) if location_element else "Russia"
        
        # Парсинг дат
        start_date, end_date = self._parse_dates(dates_text, year)
        
        if not start_date:
            return None
            
        return {
            'name': name,
            'start_date': start_date,
            'end_date': end_date or start_date,
            'location': location,
            'category': 'National',
            'status': 'Scheduled',
            'source_url': element.find('a', href=True)['href'] if element.find('a', href=True) else '',
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