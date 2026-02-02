import requests
import json
from typing import List, Dict, Optional

class HHApi:
    """Класс для работы с API hh.ru"""
    
    def __init__(self):
        self.base_url = "https://api.hh.ru"
        self.headers = {
            'User-Agent': 'ProfiTest/1.0 (educational project for career orientation)'
        }
    
    def get_professions_by_sphere(self, sphere_name: str) -> List[Dict]:
        """
        Получить профессии по сфере деятельности
        
        Args:
            sphere_name: Название профессиональной сферы
            
        Returns:
            Список профессий с информацией
        """
        # Словарь соответствия сфер hh.ru
        sphere_mapping = {
            'Человек-природа': ['наука', 'биология', 'экология', 'геология'],
            'Человек-техника': ['инженер', 'техник', 'строительство', 'механика'],
            'Человек-человек': ['врач', 'учитель', 'психолог', 'социальный'],
            'Человек-знаковая система': ['программист', 'аналитик', 'бухгалтер', 'экономист'],
            'Человек-художественный образ': ['дизайнер', 'художник', 'актер', 'музыкант'],
            'Реалистический': ['ремесленник', 'техник', 'водитель', 'монтажник'],
            'Исследовательский': ['научный', 'исследователь', 'аналитик', 'лаборант'],
            'Артистический': ['творческий', 'дизайн', 'искусство', 'реклама'],
            'Социальный': ['образование', 'медицина', 'социальная', 'психология'],
            'Предпринимательский': ['бизнес', 'продажи', 'управление', 'маркетинг'],
            'Конвенциональный': ['офис', 'документооборот', 'администрирование', 'бухгалтерия']
        }
        
        keywords = sphere_mapping.get(sphere_name, [sphere_name.lower()])
        professions = []
        
        for keyword in keywords[:2]:  # Ограничиваем 2 ключевыми словами
            try:
                params = {
                    'text': keyword,
                    'area': 113,  # Россия
                    'per_page': 5,
                    'search_field': 'name'
                }
                
                response = requests.get(
                    f"{self.base_url}/vacancies",
                    params=params,
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    for vacancy in data.get('items', [])[:3]:  # Берем по 3 вакансии на ключевое слово
                        professions.append({
                            'title': vacancy['name'],
                            'url': vacancy['alternate_url'],
                            'employer': vacancy['employer']['name'] if vacancy.get('employer') else 'Не указан',
                            'salary': self._format_salary(vacancy.get('salary')),
                            'experience': vacancy.get('experience', {}).get('name', 'Не указан')
                        })
            except Exception as e:
                print(f"Error fetching data for {keyword}: {e}")
                continue
        
        return professions
    
    def _format_salary(self, salary_data: Optional[Dict]) -> str:
        """Форматирование информации о зарплате"""
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
    
    def get_profession_info(self, profession_name: str) -> Dict:
        """
        Получить подробную информацию о профессии
        
        Args:
            profession_name: Название профессии
            
        Returns:
            Словарь с информацией о профессии
        """
        try:
            # Поиск специализаций
            response = requests.get(
                f"{self.base_url}/specializations",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                specializations = response.json()
                
                # Ищем подходящую специализацию
                for spec_group in specializations:
                    for spec in spec_group.get('specializations', []):
                        if profession_name.lower() in spec['name'].lower():
                            return {
                                'name': spec['name'],
                                'id': spec['id'],
                                'profarea_id': spec_group['id'],
                                'description': f"Профессия в сфере {spec_group['name']}"
                            }
        except Exception as e:
            print(f"Error getting profession info: {e}")
        
        return {
            'name': profession_name,
            'id': None,
            'profarea_id': None,
            'description': 'Информация недоступна'
        }
    
    def get_industries(self) -> List[Dict]:
        """
        Получить список отраслей
        
        Returns:
            Список отраслей
        """
        try:
            response = requests.get(
                f"{self.base_url}/industries",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Error getting industries: {e}")
        
        return []

# Создаем глобальный экземпляр
hh_api = HHApi()