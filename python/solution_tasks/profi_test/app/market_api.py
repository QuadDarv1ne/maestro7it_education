from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.job_market_api import job_market_api

market_api = Blueprint('market_api', __name__)

@market_api.route('/market/professions')
@login_required
def get_professions_list():
    """Получить список популярных профессий"""
    popular_professions = [
        'Программист', 'Веб-дизайнер', 'Маркетолог', 'Финансист', 'Юрист',
        'Медицинская сестра', 'Учитель', 'Инженер', 'Аналитик', 'Дизайнер',
        'Менеджер', 'Бухгалтер', 'Переводчик', 'Журналист', 'Психолог',
        'Врач', 'Стоматолог', 'Фармацевт', 'Экономист', 'HR-специалист'
    ]
    
    return jsonify({
        'success': True,
        'professions': popular_professions
    })

@market_api.route('/market/profession/<profession_name>')
@login_required
def get_profession_details(profession_name):
    """Получить подробную информацию о профессии"""
    try:
        # Получаем информацию о профессии
        profession_info = job_market_api.get_profession_info(profession_name)
        
        # Получаем вакансии
        vacancies = job_market_api.get_vacancies_by_profession(profession_name, limit=5)
        
        return jsonify({
            'success': True,
            'profession': {
                'name': profession_name,
                'info': profession_info,
                'vacancies': vacancies
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@market_api.route('/market/search')
@login_required
def search_market():
    """Поиск профессий и вакансий"""
    query = request.args.get('q', '')
    area = request.args.get('area', 'Россия')
    limit = request.args.get('limit', 10, type=int)
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Параметр поиска обязателен'
        }), 400
    
    try:
        # Получаем вакансии
        vacancies = job_market_api.get_vacancies_by_profession(query, area, limit)
        
        # Получаем информацию о профессии
        profession_info = job_market_api.get_profession_info(query)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': {
                'vacancies': vacancies,
                'profession_info': profession_info
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@market_api.route('/market/salary/<profession_name>')
@login_required
def get_salary_info(profession_name):
    """Получить информацию о зарплатах по профессии"""
    try:
        # Получаем статистику зарплат
        hh_stats = job_market_api._get_hh_salary_statistics(profession_name)
        sj_stats = {}
        
        if job_market_api.superjob_token:
            sj_stats = job_market_api._get_superjob_salary_statistics(profession_name)
        
        # Объединяем статистику
        combined_stats = _merge_salary_stats(hh_stats, sj_stats)
        
        return jsonify({
            'success': True,
            'profession': profession_name,
            'salary_info': combined_stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@market_api.route('/market/trends')
@login_required
def get_market_trends():
    """Получить тренды рынка труда"""
    try:
        # Список востребованных профессий
        trending_professions = [
            'Data Scientist', 'Frontend Developer', 'Backend Developer',
            'DevOps Engineer', 'UX/UI Designer', 'Product Manager',
            'Cybersecurity Specialist', 'AI/Machine Learning Engineer',
            'Digital Marketing Specialist', 'Cloud Architect'
        ]
        
        # Получаем информацию по каждой профессии
        trends_data = []
        for profession in trending_professions[:5]:  # Ограничиваем 5 профессиями
            try:
                info = job_market_api.get_profession_info(profession)
                vacancies = job_market_api.get_vacancies_by_profession(profession, limit=3)
                
                trends_data.append({
                    'profession': profession,
                    'info': info,
                    'vacancy_count': len(vacancies),
                    'sample_vacancies': vacancies[:2]  # Показываем 2 примера
                })
            except Exception as e:
                print(f"Error getting data for {profession}: {e}")
                continue
        
        return jsonify({
            'success': True,
            'trends': trends_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@market_api.route('/market/compare')
@login_required
def compare_professions():
    """Сравнить несколько профессий"""
    professions = request.args.getlist('professions')
    
    if not professions:
        return jsonify({
            'success': False,
            'error': 'Список профессий обязателен'
        }), 400
    
    try:
        comparison_data = []
        
        for profession in professions[:5]:  # Ограничиваем 5 профессиями
            try:
                info = job_market_api.get_profession_info(profession)
                salary_stats = job_market_api._get_hh_salary_statistics(profession)
                
                comparison_data.append({
                    'profession': profession,
                    'info': info,
                    'salary_stats': salary_stats
                })
            except Exception as e:
                print(f"Error getting data for {profession}: {e}")
                comparison_data.append({
                    'profession': profession,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'comparison': comparison_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@market_api.route('/market/user_recommendations')
@login_required
def get_user_recommendations():
    """Получить рекомендации на основе результатов пользователя"""
    try:
        # Получаем последние результаты пользователя
        from app.models import TestResult
        import json
        
        latest_result = TestResult.query.filter_by(user_id=current_user.id).order_by(
            TestResult.created_at.desc()
        ).first()
        
        if not latest_result:
            return jsonify({
                'success': False,
                'error': 'У пользователя нет результатов тестов'
            }), 404
        
        # Извлекаем доминирующую категорию
        try:
            results_dict = json.loads(latest_result.results)
            dominant_category = results_dict.get('dominant_category')
            
            if not dominant_category:
                # Для Холланда берем первую категорию
                top_categories = results_dict.get('top_categories', [])
                if top_categories:
                    dominant_category = top_categories[0][0]
        except:
            return jsonify({
                'success': False,
                'error': 'Не удалось обработать результаты теста'
            }), 500
        
        if not dominant_category:
            return jsonify({
                'success': False,
                'error': 'Не удалось определить профессиональную категорию'
            }), 400
        
        # Сопоставляем категории с профессиями
        category_to_professions = {
            'Человек-природа': ['Биолог', 'Эколог', 'Ветеринар', 'Агроном', 'Геолог'],
            'Человек-техника': ['Инженер', 'Техник', 'Механик', 'Электрик', 'Конструктор'],
            'Человек-человек': ['Учитель', 'Врач', 'Психолог', 'Социальный работник', 'Тренер'],
            'Человек-знаковая система': ['Программист', 'Аналитик', 'Бухгалтер', 'Экономист', 'Статистик'],
            'Человек-художественный образ': ['Дизайнер', 'Художник', 'Архитектор', 'Режиссер', 'Актер'],
            'Реалистический': ['Строитель', 'Водитель', 'Ремесленник', 'Мастер', 'Монтажник'],
            'Исследовательский': ['Научный сотрудник', 'Исследователь', 'Лаборант', 'Аналитик', 'Генетик'],
            'Артистический': ['Писатель', 'Музыкант', 'Дизайнер', 'Режиссер', 'Фотограф'],
            'Социальный': ['Учитель', 'Врач', 'Психолог', 'Социальный работник', 'Координатор'],
            'Предпринимательский': ['Менеджер', 'Предприниматель', 'Маркетолог', 'Продажи', 'Администратор'],
            'Конвенциональный': ['Офис-менеджер', 'Секретарь', 'Бухгалтер', 'Администратор', 'Архивариус']
        }
        
        # Получаем рекомендуемые профессии
        recommended_professions = category_to_professions.get(dominant_category, ['Специалист'])
        
        # Получаем информацию по каждой профессии
        recommendations = []
        for profession in recommended_professions[:3]:  # Ограничиваем 3 профессиями
            try:
                info = job_market_api.get_profession_info(profession)
                vacancies = job_market_api.get_vacancies_by_profession(profession, limit=2)
                
                recommendations.append({
                    'profession': profession,
                    'match_reason': f'Соответствует вашей профессиональной сфере: {dominant_category}',
                    'info': info,
                    'vacancies': vacancies
                })
            except Exception as e:
                print(f"Error getting data for {profession}: {e}")
                continue
        
        return jsonify({
            'success': True,
            'user_category': dominant_category,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def _merge_salary_stats(stats1: dict, stats2: dict) -> dict:
    """Объединить статистику зарплат из двух источников"""
    if not stats1 and not stats2:
        return {}
    
    if not stats1:
        return stats2
    if not stats2:
        return stats1
    
    return {
        'min': min(stats1.get('min', 0), stats2.get('min', 0)),
        'max': max(stats1.get('max', 0), stats2.get('max', 0)),
        'average': (stats1.get('average', 0) + stats2.get('average', 0)) // 2,
        'currency': 'RUR'
    }