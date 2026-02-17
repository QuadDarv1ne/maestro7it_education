# ... existing imports ...
import redis
import hashlib
import json
from functools import wraps


# Добавим кэширование
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True)
    redis_available = True
except (redis.ConnectionError, redis.RedisError):
    redis_available = False
    redis_client = None

def cache_result(expiration=3600):
    """Декоратор для кэширования результатов"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not redis_available:
                return func(*args, **kwargs)
            
            # Создаем ключ кэша
            cache_key = f"parser_cache:{func.__name__}:{hashlib.md5(str(args).encode()).hexdigest()}"
            
            # Проверяем кэш
            try:
                cached_result = redis_client.get(cache_key)
                if cached_result:
                    print(f"Cache hit for {func.__name__}")
                    return json.loads(cached_result)
            except Exception as e:
                print(f"Cache error: {e}")
            
            # Выполняем функцию
            result = func(*args, **kwargs)
            
            # Сохраняем в кэш
            try:
                redis_client.setex(cache_key, expiration, json.dumps(result))
                print(f"Cache set for {func.__name__}")
            except Exception as e:
                print(f"Cache save error: {e}")
            
            return result
        return wrapper
    return decorator

class EnhancedParserMixin:
    """Миксин для улучшенной обработки ошибок и логирования"""
    
    def __init__(self):
        self.retry_attempts = 3
        self.retry_delay = 1
    
    def safe_request(self, url, **kwargs):
        """Безопасный HTTP запрос с повторными попытками"""
        for attempt in range(self.retry_attempts):
            try:
                response = self.session.get(url, timeout=30, **kwargs)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"Request attempt {attempt + 1} failed: {e}")
                if attempt < self.retry_attempts - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    raise e
    
    def validate_tournament_data(self, tournament):
        """Валидация данных турнира"""
        required_fields = ['name', 'dates', 'location', 'category', 'source']
        for field in required_fields:
            if field not in tournament or not tournament[field]:
                return False
        return True
    
    def clean_tournament_data(self, tournament):
        """Очистка и нормализация данных турнира"""
        # Очистка названия
        tournament['name'] = re.sub(r'\s+', ' ', tournament['name'].strip())
        
        # Нормализация категории
        category_mapping = {
            'championship': 'National Championship',
            'open': 'Open Tournament',
            'rapid': 'Rapid Chess',
            'blitz': 'Blitz',
            'youth': 'Youth Championship',
            'women': 'Women Championship'
        }
        
        category_lower = tournament['category'].lower()
        for key, value in category_mapping.items():
            if key in category_lower:
                tournament['category'] = value
                break
        
        # Добавление отсутствующих полей
        if 'status' not in tournament:
            tournament['status'] = 'Scheduled'
        if 'prize_fund' not in tournament:
            tournament['prize_fund'] = ''
        if 'details_url' not in tournament:
            tournament['details_url'] = ''
            
        return tournament

# ... existing parser classes with EnhancedParserMixin ...

class FideParser(EnhancedParserMixin):
    def __init__(self):
        super().__init__()
        self.base_url = "https://calendar.fide.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
    
    @cache_result(expiration=7200)  # Кэш на 2 часа
    def parse_tournaments(self, year=2026):
        """Парсинг турниров с сайта FIDE"""
        # ... existing implementation ...
        pass

# ... existing AdditionalSourcesParser with caching ...

# Улучшенные маршруты с обработкой ошибок
@app.route('/parse/enhanced', methods=['POST'])
def parse_enhanced():
    """Расширенный парсинг со всех источников"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        year = data.get('year', 2026)
        use_fallback = data.get('use_fallback', True)
        max_retries = data.get('max_retries', 3)
        
        if not isinstance(year, int) or year < 2020 or year > 2030:
            return jsonify({'error': 'Invalid year parameter'}), 400
        
        # Проверка кэша
        cache_key = f"enhanced_parse:{year}"
        if redis_available:
            try:
                cached_result = redis_client.get(cache_key)
                if cached_result:
                    print("Using cached result")
                    return jsonify(json.loads(cached_result))
            except Exception as e:
                print(f"Cache check error: {e}")
        
        # Основная логика парсинга
        results = {}
        
        # Парсинг FIDE с повторными попытками
        for attempt in range(max_retries):
            try:
                fide_parser = FideParser()
                fide_tournaments = fide_parser.parse_tournaments(year)
                results['fide'] = {
                    'tournaments': fide_tournaments,
                    'count': len(fide_tournaments),
                    'status': 'success' if fide_tournaments else 'no_data'
                }
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    results['fide'] = {
                        'tournaments': [],
                        'count': 0,
                        'status': f'error_after_{max_retries}_attempts: {str(e)}'
                    }
                else:
                    time.sleep(2 ** attempt)  # Экспоненциальная задержка
        
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
        for source_data in results.values():
            if 'tournaments' in source_data:
                all_tournaments.extend(source_data['tournaments'])
        
        # Использование тестовых данных если запрошено
        if use_fallback and len(all_tournaments) == 0:
            sample_tournaments = generate_sample_tournaments(year)
            all_tournaments = sample_tournaments
            results['fallback'] = {
                'tournaments': sample_tournaments,
                'count': len(sample_tournaments),
                'status': 'sample_data_used'
            }
        
        response_data = {
            'tournaments': all_tournaments,
            'sources': results,
            'total_count': len(all_tournaments),
            'parsed_at': datetime.utcnow().isoformat(),
            'year': year,
            'cache_available': redis_available
        }
        
        # Сохранение в кэш
        if redis_available and all_tournaments:
            try:
                redis_client.setex(cache_key, 7200, json.dumps(response_data))
                print("Result cached successfully")
            except Exception as e:
                print(f"Cache save error: {e}")
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'error': f'Parsing failed: {str(e)}',
            'parsed_at': datetime.utcnow().isoformat()
        }), 500

# Улучшенная система кеширования для результатов парсинга
PARSER_CACHE_PREFIX = "parser_results"
PARSER_CACHE_TTL = 3600 * 2  # 2 часа по умолчанию


def get_parser_cache_key(parser_name: str, year: int, source: str = "all") -> str:
    """Получить ключ кэша для результатов парсинга"""
    return f"{PARSER_CACHE_PREFIX}:{parser_name}:{year}:{source}"


def get_cached_parsing_results(parser_name: str, year: int, source: str = "all") -> dict:
    """Получить закешированные результаты парсинга"""
    if not redis_available:
        return None
    
    cache_key = get_parser_cache_key(parser_name, year, source)
    try:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            result = json.loads(cached_data)
            print(f"Parser cache HIT for {parser_name}:{year}:{source}")
            return result
    except Exception as e:
        print(f"Error retrieving parser cache: {e}")
        return None
    
    print(f"Parser cache MISS for {parser_name}:{year}:{source}")
    return None


def cache_parsing_results(parser_name: str, year: int, results: dict, source: str = "all", ttl: int = None) -> bool:
    """Закешировать результаты парсинга"""
    if not redis_available:
        return False
    
    ttl = ttl or PARSER_CACHE_TTL
    cache_key = get_parser_cache_key(parser_name, year, source)
    try:
        redis_client.setex(cache_key, ttl, json.dumps(results, default=str))
        print(f"Parser results cached for {parser_name}:{year}:{source} with TTL {ttl}s")
        return True
    except Exception as e:
        print(f"Error caching parser results: {e}")
        return False


def invalidate_parser_cache(parser_name: str = None, year: int = None, source: str = None) -> bool:
    """Инвалидировать кэш парсинга"""
    if not redis_available:
        return False
    
    try:
        if parser_name:
            pattern = f"{PARSER_CACHE_PREFIX}:{parser_name}:*"
            if year:
                pattern = f"{PARSER_CACHE_PREFIX}:{parser_name}:{year}:*"
            if source:
                pattern = f"{PARSER_CACHE_PREFIX}:{parser_name}:{year}:{source}"
        else:
            pattern = f"{PARSER_CACHE_PREFIX}:*"
        
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
            print(f"Invalidated {len(keys)} parser cache entries for pattern {pattern}")
        else:
            print(f"No parser cache entries found for pattern {pattern}")
        
        return True
    except Exception as e:
        print(f"Error invalidating parser cache: {e}")
        return False


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
