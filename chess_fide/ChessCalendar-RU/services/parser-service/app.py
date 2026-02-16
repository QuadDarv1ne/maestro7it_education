"""
Parser Service - Микросервис для парсинга данных о турнирах
"""
from flask import Flask, request, jsonify
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

class FideParser:
    def __init__(self):
        self.base_url = "https://calendar.fide.com"
    
    def parse_tournaments(self, year=2026):
        """Парсинг турниров с сайта FIDE"""
        try:
            response = requests.get(f"{self.base_url}/?year={year}", timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            tournaments = []
            
            # Поиск элементов с турнирами
            tournament_elements = soup.find_all('div', class_='tournament-item')
            
            for element in tournament_elements:
                try:
                    name = element.find('h3', class_='tournament-name')
                    if name:
                        name = name.get_text(strip=True)
                    else:
                        continue
                    
                    dates = element.find('span', class_='tournament-dates')
                    dates = dates.get_text(strip=True) if dates else ""
                    
                    location = element.find('span', class_='tournament-location')
                    location = location.get_text(strip=True) if location else ""
                    
                    category = element.find('span', class_='tournament-category')
                    category = category.get_text(strip=True) if category else "Open"
                    
                    tournaments.append({
                        'name': name,
                        'dates': dates,
                        'location': location,
                        'category': category,
                        'source': 'FIDE'
                    })
                except Exception as e:
                    print(f"Error parsing tournament element: {e}")
                    continue
            
            return tournaments
        except Exception as e:
            print(f"Error fetching FIDE data: {e}")
            return []

class CfrParser:
    def __init__(self):
        self.base_url = "https://ruchess.ru"
    
    def parse_tournaments(self, year=2026):
        """Парсинг турниров с сайта РФШ"""
        try:
            response = requests.get(f"{self.base_url}/tournaments", timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            tournaments = []
            
            # Поиск элементов с турнирами
            tournament_elements = soup.find_all('div', class_='event-item')
            
            for element in tournament_elements:
                try:
                    name = element.find('h4', class_='event-title')
                    if name:
                        name = name.get_text(strip=True)
                    else:
                        continue
                    
                    dates = element.find('div', class_='event-dates')
                    dates = dates.get_text(strip=True) if dates else ""
                    
                    location = element.find('div', class_='event-location')
                    location = location.get_text(strip=True) if location else ""
                    
                    tournaments.append({
                        'name': name,
                        'dates': dates,
                        'location': location,
                        'category': 'National',
                        'source': 'CFR'
                    })
                except Exception as e:
                    print(f"Error parsing CFR tournament: {e}")
                    continue
            
            return tournaments
        except Exception as e:
            print(f"Error fetching CFR data: {e}")
            return []

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

@app.route('/parse/all', methods=['POST'])
def parse_all():
    """Парсинг данных со всех источников"""
    data = request.get_json()
    year = data.get('year', 2026)
    
    fide_parser = FideParser()
    cfr_parser = CfrParser()
    
    fide_tournaments = fide_parser.parse_tournaments(year)
    cfr_tournaments = cfr_parser.parse_tournaments(year)
    
    all_tournaments = fide_tournaments + cfr_tournaments
    
    return jsonify({
        'tournaments': all_tournaments,
        'fide_count': len(fide_tournaments),
        'cfr_count': len(cfr_tournaments),
        'total_count': len(all_tournaments),
        'parsed_at': datetime.utcnow().isoformat()
    })

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