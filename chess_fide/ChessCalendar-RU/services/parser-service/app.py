"""
Parser Service - Микросервис для парсинга данных о турнирах
"""
from flask import Flask, request, jsonify
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import os
import re
from urllib.parse import urljoin, urlparse
import time

app = Flask(__name__)

class FideParser:
    def __init__(self):
        self.base_url = "https://calendar.fide.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def parse_tournaments(self, year=2026):
        """Парсинг турниров с сайта FIDE"""
        try:
            # Пробуем разные URL структуры
            urls_to_try = [
                f"{self.base_url}/?year={year}",
                f"{self.base_url}/events?year={year}",
                f"{self.base_url}/tournaments/{year}",
                f"{self.base_url}/calendar/{year}"
            ]
            
            tournaments = []
            
            for url in urls_to_try:
                try:
                    print(f"Trying URL: {url}")
                    response = self.session.get(url, timeout=30)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        parsed_tournaments = self._extract_tournaments_from_soup(soup, url)
                        if parsed_tournaments:
                            tournaments.extend(parsed_tournaments)
                            print(f"Found {len(parsed_tournaments)} tournaments from {url}")
                            break
                except Exception as e:
                    print(f"Error with URL {url}: {e}")
                    continue
            
            # Если основной парсинг не дал результатов, используем запасной метод
            if not tournaments:
                tournaments = self._fallback_parsing(year)
            
            return tournaments
        except Exception as e:
            print(f"Error fetching FIDE data: {e}")
            return []

    def _extract_tournaments_from_soup(self, soup, source_url):
        """Извлечение турниров из BeautifulSoup объекта"""
        tournaments = []
        
        # Пробуем разные селекторы
        selectors = [
            'div.tournament-item',
            'div.event-item', 
            'div.tournament-card',
            'article.tournament',
            'li.tournament',
            'div.calendar-event',
            '.event-list .event',
            '.tournaments-list .tournament'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                print(f"Found {len(elements)} elements with selector: {selector}")
                for element in elements:
                    try:
                        tournament = self._parse_tournament_element(element, source_url)
                        if tournament:
                            tournaments.append(tournament)
                    except Exception as e:
                        print(f"Error parsing element: {e}")
                        continue
                if tournaments:
                    break
        
        return tournaments

    def _parse_tournament_element(self, element, source_url):
        """Парсинг отдельного элемента турнира"""
        # Извлечение названия
        name_selectors = [
            'h3.tournament-name',
            'h2.event-title', 
            'h4.tournament-title',
            '.event-name',
            '.tournament-title',
            'a.event-link'
        ]
        
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
        date_selectors = [
            '.tournament-dates',
            '.event-dates', 
            '.date-range',
            '.event-date',
            'time',
            '.dates'
        ]
        
        dates = ""
        for selector in date_selectors:
            date_elem = element.select_one(selector)
            if date_elem:
                dates = date_elem.get_text(strip=True)
                if dates:
                    break
        
        # Извлечение локации
        location_selectors = [
            '.tournament-location',
            '.event-location',
            '.location',
            '.venue',
            '.city'
        ]
        
        location = ""
        for selector in location_selectors:
            loc_elem = element.select_one(selector)
            if loc_elem:
                location = loc_elem.get_text(strip=True)
                if location:
                    break
        
        # Извлечение категории
        category_selectors = [
            '.tournament-category',
            '.event-category',
            '.category',
            '.type'
        ]
        
        category = "Open"
        for selector in category_selectors:
            cat_elem = element.select_one(selector)
            if cat_elem:
                category = cat_elem.get_text(strip=True)
                if category:
                    break
        
        # Извлечение ссылки на детали
        link_elem = element.find('a', href=True)
        details_url = ""
        if link_elem:
            href = link_elem.get('href')
            if href:
                details_url = urljoin(source_url, href)
        
        return {
            'name': name,
            'dates': dates,
            'location': location,
            'category': category,
            'source': 'FIDE',
            'details_url': details_url,
            'parsed_date': datetime.utcnow().isoformat()
        }

    def _fallback_parsing(self, year):
        """Запасной метод парсинга с использованием API или других источников"""
        fallback_tournaments = []
        
        # Пробуем FIDE API если доступен
        try:
            api_url = f"https://api.fide.com/events?year={year}"
            response = self.session.get(api_url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for event in data.get('events', []):
                    fallback_tournaments.append({
                        'name': event.get('name', ''),
                        'dates': event.get('dates', ''),
                        'location': event.get('location', ''),
                        'category': event.get('category', 'Open'),
                        'source': 'FIDE_API',
                        'details_url': event.get('url', ''),
                        'parsed_date': datetime.utcnow().isoformat()
                    })
        except Exception as e:
            print(f"FIDE API fallback failed: {e}")
        
        # Если API не работает, возвращаем тестовые данные
        if not fallback_tournaments:
            fallback_tournaments = self._get_sample_fide_tournaments(year)
        
        return fallback_tournaments

    def _get_sample_fide_tournaments(self, year):
        """Тестовые данные FIDE турниров для демонстрации"""
        return [
            {
                'name': f"World Chess Championship {year}",
                'dates': f"April {year}",
                'location': "Undisclosed Location",
                'category': "World Championship",
                'source': 'FIDE_Sample',
                'details_url': '',
                'parsed_date': datetime.utcnow().isoformat()
            },
            {
                'name': f"Candidates Tournament {year}",
                'dates': f"June {year}",
                'location': "Madrid, Spain",
                'category': "Candidates",
                'source': 'FIDE_Sample',
                'details_url': '',
                'parsed_date': datetime.utcnow().isoformat()
            },
            {
                'name': f"Grand Prix Series {year}",
                'dates': f"Various dates {year}",
                'location': "Multiple Cities",
                'category': "Grand Prix",
                'source': 'FIDE_Sample',
                'details_url': '',
                'parsed_date': datetime.utcnow().isoformat()
            }
        ]

# ... existing code for CfrParser and routes ...