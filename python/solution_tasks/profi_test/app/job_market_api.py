import requests
import json
from typing import List, Dict, Optional
from datetime import datetime

class JobMarketAPI:
    """Интеграция с API сервисов по поиску работы"""
    
    def __init__(self):
        # HH.ru API
        self.hh_base_url = "https://api.hh.ru"
        self.hh_headers = {
            'User-Agent': 'ProfiTest/2.0 (educational project for career orientation)'
        }
        
        # SuperJob API (потребуется регистрация приложения)
        self.superjob_base_url = "https://api.superjob.ru/2.0"
        self.superjob_token = None  # Требуется получить токен
        
        # Кэширование для уменьшения количества запросов
        self.cache = {}
        self.cache_timeout = 3600  # 1 час
    
    def set_superjob_token(self, token: str):
        """Установка токена для SuperJob API"""
        self.superjob_token = token
        self.superjob_headers = {
            'X-Api-App-Id': token,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    
    def get_vacancies_by_profession(self, profession: str, area: str = 'Россия', limit: int = 10) -> List[Dict]:
        """
        Получить вакансии по профессии
        
        Args:
            profession: Название профессии
            area: Регион поиска
            limit: Количество вакансий
            
        Returns:
            Список вакансий с информацией
        """
        vacancies = []
        
        # Поиск через HH.ru
        hh_vacancies = self._search_hh_vacancies(profession, area, limit // 2)
        vacancies.extend(hh_vacancies)
        
        # Поиск через SuperJob (если токен доступен)
        if self.superjob_token:
            sj_vacancies = self._search_superjob_vacancies(profession, area, limit // 2)
            vacancies.extend(sj_vacancies)
        
        return vacancies
    
    def _search_hh_vacancies(self, profession: str, area: str, limit: int) -> List[Dict]:
        """Поиск вакансий через HH.ru API"""
        try:
            # Получаем ID региона
            area_id = self._get_hh_area_id(area)
            
            params = {
                'text': profession,
                'area': area_id,
                'per_page': limit,
                'search_field': 'name'
            }
            
            response = requests.get(
                f"{self.hh_base_url}/vacancies",
                params=params,
                headers=self.hh_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                vacancies = []
                
                for vacancy in data.get('items', [])[:limit]:
                    vacancies.append({
                        'source': 'hh.ru',
                        'title': vacancy['name'],
                        'url': vacancy['alternate_url'],
                        'employer': vacancy['employer']['name'] if vacancy.get('employer') else 'Не указан',
                        'salary': self._format_hh_salary(vacancy.get('salary')),
                        'experience': vacancy.get('experience', {}).get('name', 'Не указан'),
                        'schedule': vacancy.get('schedule', {}).get('name', 'Не указан'),
                        'published_at': vacancy.get('published_at')
                    })
                
                return vacancies
        except Exception as e:
            print(f"Error searching HH.ru vacancies: {e}")
        
        return []
    
    def _search_superjob_vacancies(self, profession: str, area: str, limit: int) -> List[Dict]:
        """Поиск вакансий через SuperJob API"""
        try:
            # Получаем ID региона для SuperJob
            area_id = self._get_superjob_area_id(area)
            
            params = {
                'keyword': profession,
                'town': area_id,
                'count': limit
            }
            
            response = requests.get(
                f"{self.superjob_base_url}/vacancies",
                params=params,
                headers=self.superjob_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                vacancies = []
                
                for vacancy in data.get('objects', [])[:limit]:
                    vacancies.append({
                        'source': 'superjob.ru',
                        'title': vacancy['profession'],
                        'url': vacancy['link'],
                        'employer': vacancy.get('firm_name', 'Не указан'),
                        'salary': self._format_superjob_salary(vacancy),
                        'experience': self._get_experience_level(vacancy.get('experience', {}).get('title', '')),
                        'schedule': vacancy.get('type_of_work', {}).get('title', 'Не указан'),
                        'published_at': vacancy.get('date_published')
                    })
                
                return vacancies
        except Exception as e:
            print(f"Error searching SuperJob vacancies: {e}")
        
        return []
    
    def get_profession_info(self, profession: str) -> Dict:
        """
        Получить подробную информацию о профессии
        
        Args:
            profession: Название профессии
            
        Returns:
            Словарь с информацией о профессии
        """
        cache_key = f"profession_{profession}"
        
        # Проверяем кэш
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if (datetime.now().timestamp() - timestamp) < self.cache_timeout:
                return cached_data
        
        info = {
            'name': profession,
            'description': '',
            'skills': [],
            'salary_range': {},
            'demand': 'unknown',
            'growth_prospects': 'unknown'
        }
        
        try:
            # Получаем информацию через HH.ru
            hh_info = self._get_hh_profession_info(profession)
            info.update(hh_info)
            
            # Получаем информацию через SuperJob
            if self.superjob_token:
                sj_info = self._get_superjob_profession_info(profession)
                # Объединяем информацию
                info = self._merge_profession_info(info, sj_info)
            
            # Кэшируем результат
            self.cache[cache_key] = (info, datetime.now().timestamp())
            
        except Exception as e:
            print(f"Error getting profession info: {e}")
        
        return info
    
    def _get_hh_profession_info(self, profession: str) -> Dict:
        """Получить информацию о профессии через HH.ru"""
        info = {}
        
        try:
            # Поиск специализаций
            response = requests.get(
                f"{self.hh_base_url}/specializations",
                headers=self.hh_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                specializations = response.json()
                
                # Ищем подходящую специализацию
                for spec_group in specializations:
                    for spec in spec_group.get('specializations', []):
                        if profession.lower() in spec['name'].lower():
                            info['description'] = f"Профессия в сфере {spec_group['name']}"
                            info['hh_specialization_id'] = spec['id']
                            break
                    if 'description' in info:
                        break
            
            # Получаем статистику по зарплатам
            salary_stats = self._get_hh_salary_statistics(profession)
            info['salary_range'] = salary_stats
            
        except Exception as e:
            print(f"Error getting HH.ru profession info: {e}")
        
        return info
    
    def _get_superjob_profession_info(self, profession: str) -> Dict:
        """Получить информацию о профессии через SuperJob"""
        info = {}
        
        try:
            # Поиск в каталоге профессий
            response = requests.get(
                f"{self.superjob_base_url}/catalogues",
                headers=self.superjob_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                catalogues = response.json()
                
                # Ищем подходящую профессию
                for category in catalogues:
                    if profession.lower() in category.get('title', '').lower():
                        info['description'] = category.get('title', '')
                        info['sj_catalogue_id'] = category.get('id')
                        break
            
            # Получаем статистику
            salary_stats = self._get_superjob_salary_statistics(profession)
            info['salary_range'] = salary_stats
            
        except Exception as e:
            print(f"Error getting SuperJob profession info: {e}")
        
        return info
    
    def _get_hh_salary_statistics(self, profession: str) -> Dict:
        """Получить статистику зарплат через HH.ru"""
        try:
            params = {
                'text': profession,
                'area': 113,  # Россия
                'only_with_salary': True
            }
            
            response = requests.get(
                f"{self.hh_base_url}/vacancies",
                params=params,
                headers=self.hh_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                salaries = []
                
                for vacancy in data.get('items', [])[:50]:  # Анализируем первые 50 вакансий
                    salary = vacancy.get('salary')
                    if salary:
                        from_salary = salary.get('from')
                        to_salary = salary.get('to')
                        if from_salary:
                            salaries.append(from_salary)
                        elif to_salary:
                            salaries.append(to_salary)
                
                if salaries:
                    return {
                        'min': min(salaries),
                        'max': max(salaries),
                        'average': sum(salaries) // len(salaries),
                        'currency': 'RUR'
                    }
        except Exception as e:
            print(f"Error getting salary statistics: {e}")
        
        return {}
    
    def _get_superjob_salary_statistics(self, profession: str) -> Dict:
        """Получить статистику зарплат через SuperJob"""
        try:
            params = {
                'keyword': profession,
                'no_agreement': 1  # Только с указанной зарплатой
            }
            
            response = requests.get(
                f"{self.superjob_base_url}/vacancies",
                params=params,
                headers=self.superjob_headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                salaries = []
                
                for vacancy in data.get('objects', [])[:50]:
                    payment_from = vacancy.get('payment_from')
                    payment_to = vacancy.get('payment_to')
                    if payment_from and payment_from > 0:
                        salaries.append(payment_from)
                    elif payment_to and payment_to > 0:
                        salaries.append(payment_to)
                
                if salaries:
                    return {
                        'min': min(salaries),
                        'max': max(salaries),
                        'average': sum(salaries) // len(salaries),
                        'currency': 'RUR'
                    }
        except Exception as e:
            print(f"Error getting SuperJob salary statistics: {e}")
        
        return {}
    
    def _format_hh_salary(self, salary_data: Optional[Dict]) -> str:
        """Форматирование информации о зарплате HH.ru"""
        if not salary_data:
            return "Не указана"
        
        from_salary = salary_data.get('from')
        to_salary = salary_data.get('to')
        currency = salary_data.get('currency', 'RUR')
        
        currency_symbols = {
            'RUR': '₽',
            'RUB': '₽',
            'USD': '$',
            'EUR': '€'
        }
        
        symbol = currency_symbols.get(currency, currency)
        
        if from_salary and to_salary:
            return f"{from_salary} - {to_salary} {symbol}"
        elif from_salary:
            return f"от {from_salary} {symbol}"
        elif to_salary:
            return f"до {to_salary} {symbol}"
        else:
            return "Не указана"
    
    def _format_superjob_salary(self, vacancy: Dict) -> str:
        """Форматирование информации о зарплате SuperJob"""
        payment_from = vacancy.get('payment_from')
        payment_to = vacancy.get('payment_to')
        currency = vacancy.get('currency', 'rub')
        
        currency_symbols = {
            'rub': '₽',
            'usd': '$',
            'eur': '€'
        }
        
        symbol = currency_symbols.get(currency.lower(), '₽')
        
        if payment_from and payment_to and payment_from > 0 and payment_to > 0:
            return f"{payment_from} - {payment_to} {symbol}"
        elif payment_from and payment_from > 0:
            return f"от {payment_from} {symbol}"
        elif payment_to and payment_to > 0:
            return f"до {payment_to} {symbol}"
        else:
            return "Не указана"
    
    def _get_experience_level(self, experience_text: str) -> str:
        """Определение уровня опыта из текста"""
        if not experience_text:
            return "Не указан"
        
        experience_text = experience_text.lower()
        
        if 'нет опыта' in experience_text or 'без опыта' in experience_text:
            return "Без опыта"
        elif 'от 1 года' in experience_text or '1-3 года' in experience_text:
            return "От 1 года"
        elif 'от 3 лет' in experience_text or '3-6 лет' in experience_text:
            return "От 3 лет"
        elif 'более 6 лет' in experience_text:
            return "Более 6 лет"
        else:
            return "Не указан"
    
    def _get_hh_area_id(self, area_name: str) -> int:
        """Получить ID региона для HH.ru"""
        area_mapping = {
            'Россия': 113,
            'Москва': 1,
            'Санкт-Петербург': 2,
            'Новосибирск': 4,
            'Екатеринбург': 3,
            'Казань': 88,
            'Нижний Новгород': 66,
            'Челябинск': 77,
            'Самара': 83,
            'Омск': 72
        }
        
        return area_mapping.get(area_name, 113)  # По умолчанию Россия
    
    def _get_superjob_area_id(self, area_name: str) -> int:
        """Получить ID региона для SuperJob"""
        area_mapping = {
            'Россия': 0,
            'Москва': 4,
            'Санкт-Петербург': 149,
            'Новосибирск': 16,
            'Екатеринбург': 10,
            'Казань': 41,
            'Нижний Новгород': 49,
            'Челябинск': 18,
            'Самара': 99,
            'Омск': 42
        }
        
        return area_mapping.get(area_name, 0)  # По умолчанию Россия
    
    def _merge_profession_info(self, info1: Dict, info2: Dict) -> Dict:
        """Объединить информацию о профессии из двух источников"""
        merged = info1.copy()
        
        # Объединяем salary_range, беря средние значения
        if info1.get('salary_range') and info2.get('salary_range'):
            salary1 = info1['salary_range']
            salary2 = info2['salary_range']
            
            merged['salary_range'] = {
                'min': min(salary1.get('min', 0), salary2.get('min', 0)),
                'max': max(salary1.get('max', 0), salary2.get('max', 0)),
                'average': (salary1.get('average', 0) + salary2.get('average', 0)) // 2,
                'currency': 'RUR'
            }
        elif info2.get('salary_range'):
            merged['salary_range'] = info2['salary_range']
        
        # Берем описание из SuperJob если оно лучше
        if info2.get('description') and len(info2['description']) > len(info1.get('description', '')):
            merged['description'] = info2['description']
        
        return merged


# Глобальный экземпляр API
job_market_api = JobMarketAPI()