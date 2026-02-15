import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from app.models.tournament import Tournament

class CFRParser:
    def __init__(self):
        self.base_url = "https://ruchess.ru"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_tournaments(self, year=2026):
        """Получить турниры с сайта Федерации шахмат России"""
        tournaments = []
        
        # Попробуем несколько возможных URL
        urls = [
            f"{self.base_url}/",
            f"{self.base_url}/championship/",
            f"{self.base_url}/tournaments/"
        ]
        
        for url in urls:
            try:
                tournaments.extend(self._parse_page(url, year))
            except Exception as e:
                print(f"Error parsing {url}: {e}")
                continue
                
        return tournaments

    def _parse_page(self, url, year):
        """Парсинг страницы CFR"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            tournaments = []
            
            # Ищем элементы с информацией о турнирах
            # Адаптируем под реальную структуру сайта
            tournament_elements = soup.find_all(['div', 'article', 'li'], 
                                              class_=re.compile(r'tournament|event|competition'))
            
            for element in tournament_elements:
                try:
                    tournament_data = self._extract_tournament_data(element, year)
                    if tournament_data:
                        tournaments.append(tournament_data)
                except Exception as e:
                    print(f"Error extracting tournament: {e}")
                    continue
                    
            return tournaments
        except Exception as e:
            print(f"Error fetching page {url}: {e}")
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
            
            # Примеры форматов: "15-20 марта 2026", "Март 2026", "15.03.2026"
            date_string = date_string.replace('января', 'January').replace('февраля', 'February')
            date_string = date_string.replace('марта', 'March').replace('апреля', 'April')
            date_string = date_string.replace('мая', 'May').replace('июня', 'June')
            date_string = date_string.replace('июля', 'July').replace('августа', 'August')
            date_string = date_string.replace('сентября', 'September').replace('октября', 'October')
            date_string = date_string.replace('ноября', 'November').replace('декабря', 'December')
            
            if '-' in date_string:
                # Диапазон дат
                parts = date_string.split('-')
                start_str = parts[0].strip()
                end_str = parts[1].strip() if len(parts) > 1 else start_str
                
                start_date = dateutil.parser.parse(f"{start_str} {year}")
                end_date = dateutil.parser.parse(f"{end_str} {year}")
                
                return start_date.date(), end_date.date()
            else:
                # Одна дата
                date = dateutil.parser.parse(f"{date_string} {year}")
                return date.date(), date.date()
                
        except Exception as e:
            print(f"Error parsing dates '{date_string}': {e}")
            return None, None