"""
Улучшенный сервис парсинга данных о шахматных турнирах
"""
from flask import Flask, request, jsonify
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from urllib.parse import urljoin
import time

app = Flask(__name__)

class FideParser:
    def __init__(self):
        self.base_url = "https://calendar.fide.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
    
    def parse_tournaments(self, year=2026):
        """Парсинг турниров с сайта FIDE"""
        try:
            # Пробуем разные URL структуры
            urls_to_try = [
                f"{self.base_url}/?year={year}",
                f"{self.base_url}/events?year={year}",
                f"{self.base_url}/tournaments/{year}"
            ]
            
            tournaments = []
            
            for url in urls_to_try:
                try:
                    print(f"Trying URL: {url}")
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        parsed_tournaments = self._extract_tournaments(soup)
                        if parsed_tournaments:
                            tournaments.extend(parsed_tournaments)
                            print(f"Found {len(parsed_tournaments)} tournaments from {url}")
                            break
                except Exception as e:
                    print(f"Error with URL {url}: {e}")
                    continue
            
            # Если основной парсинг не дал результатов, используем запасной метод
            if not tournaments:
                tournaments = self._get_sample_tournaments(year)
            
            return tournaments
        except Exception as e:
            print(f"Error fetching FIDE data: {e}")
            return []

    def _extract_tournaments(self, soup):
        """Извлечение турниров из BeautifulSoup объекта"""
        tournaments = []
        
        # Пробуем разные селекторы
        selectors = [
            'div.tournament-item',
            'div.event-item', 
            'div.tournament-card',
            'article.tournament'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} elements with selector: {selector}")
                for element in elements:
                    try:
                        tournament = self._parse_element(element)
                        if tournament:
                            tournaments.append(tournament)
                    except Exception as e:
                        print(f"Error parsing element: {e}")
                        continue
                if tournaments:
                    break
        
        return tournaments

    def _parse_element(self, element):
        """Парсинг отдельного элемента турнира"""
        # Извлечение названия
        name_selectors = ['h3', 'h2', 'h4', '.title', '.name']
        name = None
        for selector in name_selectors:
            name_elem = element.select_one(selector)
            if name_elem:
                name = name_elem.get_text(strip=True)
                if name:
                    break
        
        if not name:
            return None
            
        # Извлечение дат
        date_elem = element.select_one('.date, .dates, time')
        dates = date_elem.get_text(strip=True) if date_elem else ""
        
        # Извлечение локации
        loc_elem = element.select_one('.location, .venue, .city')
        location = loc_elem.get_text(strip=True) if loc_elem else "International"
        
        # Извлечение категории
        cat_elem = element.select_one('.category, .type')
        category = cat_elem.get_text(strip=True) if cat_elem else "Open"
        
        return {
            'name': name,
            'dates': dates,
            'location': location,
            'category': category,
            'source': 'FIDE',
            'parsed_date': datetime.utcnow().isoformat()
        }

    def _get_sample_tournaments(self, year):
        """Тестовые данные FIDE турниров"""
        return [
            {
                'name': f"World Chess Championship {year}",
                'dates': f"April {year}",
                'location': "Undisclosed Location",
                'category': "World Championship",
                'source': 'FIDE_Sample',
                'parsed_date': datetime.utcnow().isoformat()
            },
            {
                'name': f"Candidates Tournament {year}",
                'dates': f"June {year}",
                'location': "Madrid, Spain",
                'category': "Candidates",
                'source': 'FIDE_Sample',
                'parsed_date': datetime.utcnow().isoformat()
            }
        ]

class CfrParser:
    def __init__(self):
        self.base_url = "https://ruchess.ru"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        })
    
    def parse_tournaments(self, year=2026):
        """Парсинг турниров с сайта РФШ"""
        try:
            urls_to_try = [
                f"{self.base_url}/tournaments",
                f"{self.base_url}/events",
                f"{self.base_url}/turniry"
            ]
            
            tournaments = []
            
            for url in urls_to_try:
                try:
                    print(f"Trying CFR URL: {url}")
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        parsed_tournaments = self._extract_tournaments(soup)
                        if parsed_tournaments:
                            tournaments.extend(parsed_tournaments)
                            print(f"Found {len(parsed_tournaments)} CFR tournaments from {url}")
                            break
                except Exception as e:
                    print(f"Error with CFR URL {url}: {e}")
                    continue
            
            if not tournaments:
                tournaments = self._get_sample_tournaments(year)
            
            return tournaments
        except Exception as e:
            print(f"Error fetching CFR data: {e}")
            return []

    def _extract_tournaments(self, soup):
        """Извлечение турниров из BeautifulSoup объекта"""
        tournaments = []
        
        selectors = [
            'div.event-item',
            'div.tournament-card',
            'article.news-item',
            '.events-list .event'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} CFR elements with selector: {selector}")
                for element in elements:
                    try:
                        tournament = self._parse_element(element)
                        if tournament:
                            tournaments.append(tournament)
                    except Exception as e:
                        print(f"Error parsing CFR element: {e}")
                        continue
                if tournaments:
                    break
        
        return tournaments

    def _parse_element(self, element):
        """Парсинг отдельного элемента турнира для CFR"""
        name_selectors = ['h4', 'h3', 'h2', '.title', '.name']
        name = None
        for selector in name_selectors:
            name_elem = element.select_one(selector)
            if name_elem:
                name = name_elem.get_text(strip=True)
                if name:
                    break
        
        if not name:
            return None
            
        date_elem = element.select_one('.date, .time')
        dates = date_elem.get_text(strip=True) if date_elem else ""
        
        loc_elem = element.select_one('.location, .city')
        location = loc_elem.get_text(strip=True) if loc_elem else "Россия"
        
        return {
            'name': name,
            'dates': dates,
            'location': location,
            'category': 'National',
            'source': 'CFR',
            'parsed_date': datetime.utcnow().isoformat()
        }

    def _get_sample_tournaments(self, year):
        """Тестовые данные CFR турниров"""
        return [
            {
                'name': f"Чемпионат России по шахматам {year}",
                'dates': f"Март {year}",
                'location': "Москва",
                'category': 'National Championship',
                'source': 'CFR_Sample',
                'parsed_date': datetime.utcnow().isoformat()
            },
            {
                'name': f"Кубок России по быстрым шахматам {year}",
                'dates': f"Апрель {year}",
                'location': "Санкт-Петербург",
                'category': 'Rapid Chess',
                'source': 'CFR_Sample',
                'parsed_date': datetime.utcnow().isoformat()
            }
        ]

def generate_sample_tournaments(year):
    """Генерация тестовых данных турниров"""
    return [
        {
            'name': f"Чемпионат мира по шахматам {year}",
            'dates': f"Апрель {year}",
            'location': "Неизвестно",
            'category': 'World Championship',
            'source': 'Sample',
            'status': 'Scheduled'
        },
        {
            'name': f"Чемпионат России по шахматам {year}",
            'dates': f"Март {year}",
            'location': "Москва",
            'category': 'National Championship',
            'source': 'Sample',
            'status': 'Scheduled'
        },
        {
            'name': f"Открытый турнир в Санкт-Петербурге {year}",
            'dates': f"Май {year}",
            'location': "Санкт-Петербург",
            'category': 'Open Tournament',
            'source': 'Sample',
            'status': 'Scheduled'
        }
    ]

@app.route('/parse/fide', methods=['POST'])
def parse_fide():
    """Парсинг данных с FIDE"""
    data = request.get_json()
    year = data.get('year', 2026)
    
    parser = FideParser()
    tournaments = parser.parse_tournaments(year)
    
    return jsonify({
        'tournaments': tournaments,
        'count': len(tournaments),
        'source': 'FIDE',
        'parsed_at': datetime.utcnow().isoformat()
    })

@app.route('/parse/cfr', methods=['POST'])
def parse_cfr():
    """Парсинг данных с CFR"""
    data = request.get_json()
    year = data.get('year', 2026)
    
    parser = CfrParser()
    tournaments = parser.parse_tournaments(year)
    
    return jsonify({
        'tournaments': tournaments,
        'count': len(tournaments),
        'source': 'CFR',
        'parsed_at': datetime.utcnow().isoformat()
    })

@app.route('/parse/enhanced', methods=['POST'])
def parse_enhanced():
    """Расширенный парсинг со всех источников"""
    try:
        data = request.get_json()
        year = data.get('year', 2026)
        use_fallback = data.get('use_fallback', True)
        
        # Парсинг FIDE
        fide_parser = FideParser()
        fide_tournaments = fide_parser.parse_tournaments(year)
        
        # Парсинг CFR
        cfr_parser = CfrParser()
        cfr_tournaments = cfr_parser.parse_tournaments(year)
        
        # Сбор всех турниров
        all_tournaments = fide_tournaments + cfr_tournaments
        
        # Использование тестовых данных если запрошено
        if use_fallback and len(all_tournaments) == 0:
            all_tournaments = generate_sample_tournaments(year)
        
        return jsonify({
            'tournaments': all_tournaments,
            'fide_count': len(fide_tournaments),
            'cfr_count': len(cfr_tournaments),
            'total_count': len(all_tournaments),
            'parsed_at': datetime.utcnow().isoformat(),
            'year': year
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Parsing failed: {str(e)}',
            'parsed_at': datetime.utcnow().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    return jsonify({
        'status': 'healthy',
        'service': 'parser-service',
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)