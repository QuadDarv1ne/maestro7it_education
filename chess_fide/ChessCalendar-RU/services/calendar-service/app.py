"""
Calendar Integration Service - Сервис для интеграции с Google Calendar и Outlook
"""
from flask import Flask, request, jsonify, redirect
from datetime import datetime, timezone
import json
import uuid
import base64
import os

app = Flask(__name__)

class CalendarService:
    def __init__(self):
        # Конфигурация Google Calendar API
        self.google_client_id = os.environ.get('GOOGLE_CLIENT_ID', '')
        self.google_client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '')
        self.google_redirect_uri = os.environ.get('GOOGLE_REDIRECT_URI', 'http://localhost:5006/callback/google')
        
        # Конфигурация Outlook API
        self.outlook_client_id = os.environ.get('OUTLOOK_CLIENT_ID', '')
        self.outlook_client_secret = os.environ.get('OUTLOOK_CLIENT_SECRET', '')
        self.outlook_redirect_uri = os.environ.get('OUTLOOK_REDIRECT_URI', 'http://localhost:5006/callback/outlook')
        
        # Хранилище токенов (в реальном приложении использовать Redis/БД)
        self.tokens = {}
    
    def generate_ics_content(self, tournament):
        """Генерация ICS файла для календаря"""
        # Форматирование дат
        start_date = tournament['start_date']
        end_date = tournament['end_date']
        
        # Создание уникального ID события
        event_uid = str(uuid.uuid4())
        
        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ChessCalendar-RU//NONSGML v1.0//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{event_uid}@chesscalendar-ru.ru
DTSTART:{start_date.strftime('%Y%m%d')}
DTEND:{end_date.strftime('%Y%m%d')}
SUMMARY:{tournament['name']}
LOCATION:{tournament['location']}
DESCRIPTION:{tournament.get('description', 'Шахматный турнир')}
CATEGORIES:Chess Tournament
END:VEVENT
END:VCALENDAR"""
        
        return ics_content
    
    def generate_google_calendar_url(self, tournament):
        """Генерация URL для добавления в Google Calendar"""
        import urllib.parse
        
        params = {
            'action': 'TEMPLATE',
            'text': tournament['name'],
            'dates': f"{tournament['start_date'].strftime('%Y%m%d')}/{tournament['end_date'].strftime('%Y%m%d')}",
            'details': tournament.get('description', 'Шахматный турнир'),
            'location': tournament['location'],
            'trp': 'false'
        }
        
        query_string = urllib.parse.urlencode(params)
        return f"https://www.google.com/calendar/render?{query_string}"
    
    def generate_outlook_calendar_url(self, tournament):
        """Генерация URL для добавления в Outlook Calendar"""
        import urllib.parse
        
        params = {
            'path': '/calendar/action/compose',
            'rru': 'addevent',
            'subject': tournament['name'],
            'startdt': tournament['start_date'].isoformat(),
            'enddt': tournament['end_date'].isoformat(),
            'location': tournament['location'],
            'body': tournament.get('description', 'Шахматный турнир')
        }
        
        query_string = urllib.parse.urlencode(params)
        return f"https://outlook.office.com/calendar/0/deeplink/compose?{query_string}"

calendar_service = CalendarService()

@app.route('/export/ics', methods=['POST'])
def export_ics():
    """Экспорт турнира в ICS файл"""
    try:
        data = request.get_json()
        tournament = data.get('tournament')
        
        if not tournament:
            return jsonify({'error': 'No tournament data provided'}), 400
        
        # Проверка обязательных полей
        required_fields = ['name', 'start_date', 'end_date', 'location']
        for field in required_fields:
            if field not in tournament:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Преобразование строк в даты
        if isinstance(tournament['start_date'], str):
            tournament['start_date'] = datetime.fromisoformat(tournament['start_date'].replace('Z', '+00:00'))
        if isinstance(tournament['end_date'], str):
            tournament['end_date'] = datetime.fromisoformat(tournament['end_date'].replace('Z', '+00:00'))
        
        # Генерация ICS контента
        ics_content = calendar_service.generate_ics_content(tournament)
        
        return jsonify({
            'ics_content': ics_content,
            'filename': f"tournament_{tournament['name'].replace(' ', '_')}.ics",
            'content_type': 'text/calendar',
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export/google', methods=['POST'])
def export_google():
    """Генерация URL для Google Calendar"""
    try:
        data = request.get_json()
        tournament = data.get('tournament')
        
        if not tournament:
            return jsonify({'error': 'No tournament data provided'}), 400
        
        # Проверка обязательных полей
        required_fields = ['name', 'start_date', 'end_date', 'location']
        for field in required_fields:
            if field not in tournament:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Преобразование строк в даты
        if isinstance(tournament['start_date'], str):
            tournament['start_date'] = datetime.fromisoformat(tournament['start_date'].replace('Z', '+00:00'))
        if isinstance(tournament['end_date'], str):
            tournament['end_date'] = datetime.fromisoformat(tournament['end_date'].replace('Z', '+00:00'))
        
        # Генерация Google Calendar URL
        google_url = calendar_service.generate_google_calendar_url(tournament)
        
        return jsonify({
            'google_calendar_url': google_url,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export/outlook', methods=['POST'])
def export_outlook():
    """Генерация URL для Outlook Calendar"""
    try:
        data = request.get_json()
        tournament = data.get('tournament')
        
        if not tournament:
            return jsonify({'error': 'No tournament data provided'}), 400
        
        # Проверка обязательных полей
        required_fields = ['name', 'start_date', 'end_date', 'location']
        for field in required_fields:
            if field not in tournament:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Преобразование строк в даты
        if isinstance(tournament['start_date'], str):
            tournament['start_date'] = datetime.fromisoformat(tournament['start_date'].replace('Z', '+00:00'))
        if isinstance(tournament['end_date'], str):
            tournament['end_date'] = datetime.fromisoformat(tournament['end_date'].replace('Z', '+00:00'))
        
        # Генерация Outlook Calendar URL
        outlook_url = calendar_service.generate_outlook_calendar_url(tournament)
        
        return jsonify({
            'outlook_calendar_url': outlook_url,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export/batch', methods=['POST'])
def batch_export():
    """Пакетный экспорт нескольких турниров"""
    try:
        data = request.get_json()
        tournaments = data.get('tournaments', [])
        
        if not tournaments:
            return jsonify({'error': 'No tournaments provided'}), 400
        
        results = []
        
        for i, tournament in enumerate(tournaments):
            try:
                # Проверка обязательных полей
                required_fields = ['name', 'start_date', 'end_date', 'location']
                for field in required_fields:
                    if field not in tournament:
                        raise ValueError(f'Missing required field: {field}')
                
                # Преобразование дат
                if isinstance(tournament['start_date'], str):
                    tournament['start_date'] = datetime.fromisoformat(tournament['start_date'].replace('Z', '+00:00'))
                if isinstance(tournament['end_date'], str):
                    tournament['end_date'] = datetime.fromisoformat(tournament['end_date'].replace('Z', '+00:00'))
                
                # Генерация всех форматов
                ics_content = calendar_service.generate_ics_content(tournament)
                google_url = calendar_service.generate_google_calendar_url(tournament)
                outlook_url = calendar_service.generate_outlook_calendar_url(tournament)
                
                results.append({
                    'index': i,
                    'tournament_name': tournament['name'],
                    'ics_content': ics_content,
                    'google_calendar_url': google_url,
                    'outlook_calendar_url': outlook_url,
                    'status': 'success'
                })
                
            except Exception as e:
                results.append({
                    'index': i,
                    'tournament_name': tournament.get('name', 'Unknown'),
                    'error': str(e),
                    'status': 'failed'
                })
        
        return jsonify({
            'results': results,
            'total_processed': len(tournaments),
            'successful': len([r for r in results if r['status'] == 'success']),
            'failed': len([r for r in results if r['status'] == 'failed']),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/google', methods=['GET'])
def auth_google():
    """Аутентификация через Google"""
    # В реальном приложении здесь будет OAuth2 flow
    return jsonify({
        'status': 'not_implemented',
        'message': 'Google OAuth integration needs to be implemented with proper client credentials'
    })

@app.route('/auth/outlook', methods=['GET'])
def auth_outlook():
    """Аутентификация через Outlook"""
    # В реальном приложении здесь будет OAuth2 flow
    return jsonify({
        'status': 'not_implemented',
        'message': 'Outlook OAuth integration needs to be implemented with proper client credentials'
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    return jsonify({
        'status': 'healthy',
        'service': 'calendar-integration-service',
        'supported_formats': ['ICS', 'Google Calendar', 'Outlook Calendar'],
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)