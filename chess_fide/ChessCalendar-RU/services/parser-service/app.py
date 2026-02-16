# ... existing routes ...

@app.route('/parse/additional', methods=['POST'])
def parse_additional_sources():
    """Парсинг данных с дополнительных источников"""
    data = request.get_json()
    year = data.get('year', 2026)
    
    parser = AdditionalSourcesParser()
    
    # Парсинг с разных источников
    chess24_events = parser.parse_chess24_events()
    chesscom_events = parser.parse_chesscom_events()
    
    all_additional_events = chess24_events + chesscom_events
    
    return jsonify({
        'tournaments': all_additional_events,
        'chess24_count': len(chess24_events),
        'chesscom_count': len(chesscom_events),
        'total_count': len(all_additional_events),
        'source': 'Additional_Sources',
        'parsed_at': datetime.utcnow().isoformat()
    })

@app.route('/parse/enhanced', methods=['POST'])
def parse_enhanced():
    """Расширенный парсинг со всех источников с улучшенной обработкой"""
    data = request.get_json()
    year = data.get('year', 2026)
    use_fallback = data.get('use_fallback', True)
    
    results = {
        'fide': {'tournaments': [], 'count': 0, 'status': 'pending'},
        'cfr': {'tournaments': [], 'count': 0, 'status': 'pending'},
        'additional': {'tournaments': [], 'count': 0, 'status': 'pending'}
    }
    
    # Парсинг FIDE
    try:
        fide_parser = FideParser()
        fide_tournaments = fide_parser.parse_tournaments(year)
        results['fide'] = {
            'tournaments': fide_tournaments,
            'count': len(fide_tournaments),
            'status': 'success' if fide_tournaments else 'no_data'
        }
    except Exception as e:
        results['fide'] = {
            'tournaments': [],
            'count': 0,
            'status': f'error: {str(e)}'
        }
    
    # Парсинг CFR
    try:
        cfr_parser = CfrParser()
        cfr_tournaments = cfr_parser.parse_tournaments(year)
        results['cfr'] = {
            'tournaments': cfr_tournaments,
            'count': len(cfr_tournaments),
            'status': 'success' if cfr_tournaments else 'no_data'
        }
    except Exception as e:
        results['cfr'] = {
            'tournaments': [],
            'count': 0,
            'status': f'error: {str(e)}'
        }
    
    # Дополнительные источники
    try:
        additional_parser = AdditionalSourcesParser()
        chess24_events = additional_parser.parse_chess24_events()
        chesscom_events = additional_parser.parse_chesscom_events()
        additional_tournaments = chess24_events + chesscom_events
        results['additional'] = {
            'tournaments': additional_tournaments,
            'count': len(additional_tournaments),
            'status': 'success' if additional_tournaments else 'no_data'
        }
    except Exception as e:
        results['additional'] = {
            'tournaments': [],
            'count': 0,
            'status': f'error: {str(e)}'
        }
    
    # Сбор всех турниров
    all_tournaments = []
    for source in results.values():
        all_tournaments.extend(source['tournaments'])
    
    # Использование тестовых данных если запрошено
    if use_fallback and len(all_tournaments) == 0:
        all_tournaments = generate_sample_tournaments(year)
        results['fallback'] = {
            'tournaments': all_tournaments,
            'count': len(all_tournaments),
            'status': 'sample_data_used'
        }
    
    return jsonify({
        'tournaments': all_tournaments,
        'sources': results,
        'total_count': len(all_tournaments),
        'parsed_at': datetime.utcnow().isoformat(),
        'year': year
    })

def generate_sample_tournaments(year):
    """Генерация тестовых данных турниров для демонстрации"""
    return [
        {
            'name': f"Чемпионат мира по шахматам {year}",
            'dates': f"Апрель {year}",
            'location': "Неизвестно",
            'category': 'World Championship',
            'source': 'Sample',
            'details_url': '',
            'prize_fund': '2,000,000 USD',
            'status': 'Scheduled'
        },
        {
            'name': f"Чемпионат России по шахматам {year}",
            'dates': f"Март {year}",
            'location': "Москва",
            'category': 'National Championship',
            'source': 'Sample',
            'details_url': '',
            'prize_fund': '2,000,000 RUB',
            'status': 'Scheduled'
        },
        {
            'name': f"Открытый турнир памяти Александра Алехина {year}",
            'dates': f"Апрель {year}",
            'location': "Санкт-Петербург",
            'category': 'Open Tournament',
            'source': 'Sample',
            'details_url': '',
            'prize_fund': '1,500,000 RUB',
            'status': 'Scheduled'
        },
        {
            'name': f"Кубок Москвы по быстрым шахматам {year}",
            'dates': f"Февраль {year}",
            'location': "Москва",
            'category': 'Rapid Chess',
            'source': 'Sample',
            'details_url': '',
            'prize_fund': '500,000 RUB',
            'status': 'Ongoing'
        },
        {
            'name': f"Международный турнир в Сочи {year}",
            'dates': f"Май {year}",
            'location': "Сочи",
            'category': 'International Tournament',
            'source': 'Sample',
            'details_url': '',
            'prize_fund': '3,000,000 RUB',
            'status': 'Scheduled'
        }
    ]

# ... existing health check route ...