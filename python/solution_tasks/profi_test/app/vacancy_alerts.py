import schedule
import time
import threading
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, UserPreference, Notification, TestResult
from app.job_market_api import JobMarketAPI
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

def analyze_user_preferences_and_market():
    """
    Анализирует предпочтения пользователей и текущую ситуацию на рынке труда
    для генерации персонализированных рекомендаций
    """
    print(f"[{datetime.now()}] Запуск анализа предпочтений и рынка труда...")
    
    app = create_app()
    
    with app.app_context():
        # Получаем всех пользователей с включенными уведомлениями
        active_preferences = UserPreference.query.filter_by(vacancy_alerts_enabled=True).all()
        
        if not active_preferences:
            print(f"[{datetime.now()}] Нет пользователей с включенными уведомлениями о вакансиях")
            return
        
        # Инициализируем API для работы с рынком труда
        job_market_api = JobMarketAPI()
        
        for pref in active_preferences:
            user = pref.user
            
            # Получаем историю тестов пользователя
            user_results = TestResult.query.filter_by(user_id=user.id).order_by(TestResult.created_at.desc()).limit(5).all()
            
            if not user_results:
                continue
            
            # Получаем последние результаты теста
            latest_result = user_results[0]
            
            try:
                results_dict = json.loads(latest_result.results) if latest_result.results else {}
                dominant_category = results_dict.get('dominant_category', '')
                
                # Если нет доминирующей категории, получаем топ категорий
                if not dominant_category:
                    top_categories = results_dict.get('top_categories', [])
                    if top_categories:
                        dominant_category = top_categories[0][0] if isinstance(top_categories[0], (list, tuple)) else top_categories[0]
            except:
                continue
            
            # Получаем информацию о профессии и вакансиях
            try:
                profession_info = job_market_api.get_profession_info(dominant_category)
                vacancies = job_market_api.get_vacancies_by_profession(dominant_category, limit=10)
                
                # Проверяем, есть ли новые вакансии за последние 24 часа
                new_vacancies = []
                yesterday = datetime.utcnow() - timedelta(days=1)
                
                for vacancy in vacancies:
                    published_date_str = vacancy.get('published_at', '')
                    if published_date_str:
                        try:
                            if 'T' in published_date_str:
                                published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
                            else:
                                published_date = datetime.strptime(published_date_str, '%Y-%m-%d')
                            
                            if published_date >= yesterday:
                                new_vacancies.append(vacancy)
                        except:
                            new_vacancies.append(vacancy)
                    else:
                        new_vacancies.append(vacancy)
                
                # Создаем уведомление о новых вакансиях
                if new_vacancies:
                    title = f"Новые вакансии по профессии '{dominant_category}'"
                    message = f"Найдено {len(new_vacancies)} новых вакансий по профессии '{dominant_category}', которая соответствует вашим результатам теста. Лучшие предложения: "
                    
                    for i, vacancy in enumerate(new_vacancies[:3]):
                        company = vacancy.get('employer', 'Не указано')
                        salary = vacancy.get('salary', 'Не указана')
                        message += f"\n{i+1}. {vacancy.get('title', 'Не указано')} в {company}, з/п: {salary}"
                    
                    message += f"\n\nВсего найдено: {len(vacancies)} вакансий"
                    
                    notification = Notification(
                        user_id=user.id,
                        title=title,
                        message=message,
                        type='info'
                    )
                    
                    db.session.add(notification)
                    print(f"[{datetime.now()}] Создано уведомление для пользователя {user.username} по профессии {dominant_category}")
                
                # Также анализируем, какие профессии могут быть еще более подходящими
                # на основе рыночных тенденций и зарплат
                if profession_info and profession_info.get('salary_range'):
                    avg_salary = profession_info['salary_range'].get('average', 0)
                    
                    # Если средняя зарплата по профессии высока, уведомляем пользователя
                    if avg_salary > 80000:  # 80,000 руб
                        salary_title = f"Высокая зарплата по профессии '{dominant_category}'"
                        salary_message = f"Профессия '{dominant_category}' имеет высокую среднюю зарплату ({avg_salary:,} руб). Это хорошая перспектива для развития!"
                        
                        salary_notification = Notification(
                            user_id=user.id,
                            title=salary_title,
                            message=salary_message,
                            type='success'
                        )
                        
                        db.session.add(salary_notification)
                
            except Exception as e:
                print(f"[{datetime.now()}] Ошибка при анализе для пользователя {user.username}: {str(e)}")
                continue
        
        # Сохраняем все уведомления в базе данных
        try:
            db.session.commit()
            print(f"[{datetime.now()}] Успешно сохранены уведомления в базе данных")
        except Exception as e:
            print(f"[{datetime.now()}] Ошибка при сохранении уведомлений: {str(e)}")
            db.session.rollback()


def generate_ml_recommendations():
    """
    Генерирует рекомендации с использованием машинного обучения
    на основе результатов тестов и информации с рынка труда
    """
    print(f"[{datetime.now()}] Запуск ML-рекомендаций...")
    
    app = create_app()
    
    with app.app_context():
        # Получаем все результаты тестов
        all_results = TestResult.query.all()
        
        if not all_results:
            print(f"[{datetime.now()}] Нет результатов тестов для анализа")
            return
        
        # Подготовка данных для анализа
        user_profiles = {}
        profession_descriptions = {}
        
        # Собираем профили пользователей и их результаты
        for result in all_results:
            try:
                results_dict = json.loads(result.results) if result.results else {}
                
                # Используем оценки по категориям как профиль пользователя
                scores = results_dict.get('scores', {})
                dominant_category = results_dict.get('dominant_category', '')
                
                if result.user_id not in user_profiles:
                    user_profiles[result.user_id] = {
                        'scores': scores,
                        'dominant_category': dominant_category,
                        'recommendation': result.recommendation
                    }
                
                # Добавляем описание доминирующей профессии
                if dominant_category and dominant_category not in profession_descriptions:
                    # Здесь в реальной системе мы бы получали описание профессии из базы знаний
                    # или через API, сейчас используем заглушку
                    profession_descriptions[dominant_category] = f"Описание профессии {dominant_category}"
                    
            except:
                continue
        
        # Если недостаточно данных для ML анализа, пропускаем
        if len(user_profiles) < 2:
            print(f"[{datetime.now()}] Недостаточно данных для ML-анализа")
            return
        
        # Создаем векторы для анализа схожести
        try:
            # Подготовка текстовых описаний профессий
            professions = list(profession_descriptions.keys())
            descriptions = list(profession_descriptions.values())
            
            if not descriptions:
                print(f"[{datetime.now()}] Нет описаний профессий для анализа")
                return
            
            # Используем TF-IDF для векторизации описаний
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(descriptions)
            
            # Вычисляем схожесть между профессиями
            similarity_matrix = cosine_similarity(tfidf_matrix)
            
            # Для каждой пары схожих профессий можем сделать рекомендации
            for i, prof1 in enumerate(professions):
                for j, prof2 in enumerate(professions):
                    if i != j and similarity_matrix[i][j] > 0.7:  # Порог схожести
                        # Найдем пользователей, у которых одна из этих профессий как доминирующая
                        users_with_prof1 = [uid for uid, data in user_profiles.items() 
                                          if data['dominant_category'] == prof1]
                        
                        if users_with_prof1:
                            # Создаем уведомления для пользователей с похожими профессиями
                            for user_id in users_with_prof1:
                                user = User.query.get(user_id)
                                if user and user.preferences and user.preferences[0].vacancy_alerts_enabled:
                                    title = f"Рекомендуемая профессия: {prof2}"
                                    message = f"По вашим результатам теста рекомендуем рассмотреть профессию '{prof2}', которая схожа с '{prof1}' и может быть интересна вам."
                                    
                                    notification = Notification(
                                        user_id=user_id,
                                        title=title,
                                        message=message,
                                        type='info'
                                    )
                                    
                                    db.session.add(notification)
            
            print(f"[{datetime.now()}] ML-рекомендации успешно сгенерированы")
            
        except Exception as e:
            print(f"[{datetime.now()}] Ошибка при ML-анализе: {str(e)}")


def check_vacancy_alerts():
    """
    Проверяет наличие новых вакансий по интересующим пользователям профессиям
    и отправляет уведомления тем, кто включил эту опцию
    """
    print(f"[{datetime.now()}] Запуск проверки уведомлений о вакансиях...")
    
    app = create_app()
    
    with app.app_context():
        # Получаем всех пользователей с включенными уведомлениями
        active_preferences = UserPreference.query.filter_by(vacancy_alerts_enabled=True).all()
        
        if not active_preferences:
            print(f"[{datetime.now()}] Нет пользователей с включенными уведомлениями о вакансиях")
            return
        
        # Инициализируем API для работы с рынком труда
        job_market_api = JobMarketAPI()
        
        for pref in active_preferences:
            user = pref.user
            
            # Получаем список интересующих профессий
            try:
                import json
                preferred_professions = json.loads(pref.preferred_professions) if pref.preferred_professions else []
            except:
                preferred_professions = []
            
            if not preferred_professions:
                continue
            
            # Для каждой профессии проверяем наличие новых вакансий
            for profession in preferred_professions:
                try:
                    # Получаем вакансии для профессии
                    vacancies = job_market_api.get_vacancies_by_profession(profession, limit=5)
                    
                    if vacancies:
                        # Проверяем, есть ли новые вакансии за последние 24 часа
                        new_vacancies = []
                        yesterday = datetime.utcnow() - timedelta(days=1)
                        
                        for vacancy in vacancies:
                            # Предполагаем, что дата публикации есть в данных вакансии
                            published_date_str = vacancy.get('published_at', '')
                            if published_date_str:
                                try:
                                    # Преобразуем строку даты в объект datetime
                                    # Формат может отличаться в зависимости от API
                                    if 'T' in published_date_str:
                                        published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
                                    else:
                                        published_date = datetime.strptime(published_date_str, '%Y-%m-%d')
                                    
                                    if published_date >= yesterday:
                                        new_vacancies.append(vacancy)
                                except:
                                    # Если не удается распознать формат даты, просто считаем вакансию новой
                                    new_vacancies.append(vacancy)
                            else:
                                # Если дата не указана, считаем вакансию потенциально новой
                                new_vacancies.append(vacancy)
                        
                        if new_vacancies:
                            # Создаем уведомление для пользователя
                            title = f"Новые вакансии по профессии '{profession}'"
                            message = f"Найдено {len(new_vacancies)} новых вакансий по профессии '{profession}'. Лучшие предложения: "
                            
                            # Добавляем информацию о нескольких лучших вакансиях
                            for i, vacancy in enumerate(new_vacancies[:3]):
                                company = vacancy.get('employer', 'Не указано')
                                salary = vacancy.get('salary', 'Не указана')
                                message += f"\n{i+1}. {vacancy.get('title', 'Не указано')} в {company}, з/п: {salary}"
                            
                            message += f"\n\nВсего найдено: {len(vacancies)} вакансий"
                            
                            # Создаем уведомление
                            notification = Notification(
                                user_id=user.id,
                                title=title,
                                message=message,
                                type='info'
                            )
                            
                            db.session.add(notification)
                            print(f"[{datetime.now()}] Создано уведомление для пользователя {user.username} по профессии {profession}")
                
                except Exception as e:
                    print(f"[{datetime.now()}] Ошибка при проверке вакансий для {profession}: {str(e)}")
                    continue
        
        # Сохраняем все уведомления в базе данных
        try:
            db.session.commit()
            print(f"[{datetime.now()}] Успешно сохранены уведомления в базе данных")
        except Exception as e:
            print(f"[{datetime.now()}] Ошибка при сохранении уведомлений: {str(e)}")
            db.session.rollback()


def start_scheduler():
    """
    Запускает планировщик проверки уведомлений о вакансиях
    """
    # Планируем проверку каждые 6 часов
    schedule.every(6).hours.do(check_vacancy_alerts)
    schedule.every(6).hours.do(analyze_user_preferences_and_market)
    schedule.every(12).hours.do(generate_ml_recommendations)
    
    # Также планируем ежедневную проверку в определенное время (например, в 9 утра)
    schedule.every().day.at("09:00").do(check_vacancy_alerts)
    schedule.every().day.at("09:15").do(analyze_user_preferences_and_market)
    schedule.every().day.at("09:30").do(generate_ml_recommendations)
    
    print(f"[{datetime.now()}] Планировщик уведомлений запущен")
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(60)  # Проверяем каждую минуту
    
    # Запускаем планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    return scheduler_thread


def manual_check_for_user(user_id):
    """
    Ручная проверка уведомлений для конкретного пользователя
    """
    app = create_app()
    
    with app.app_context():
        user = User.query.get(user_id)
        if not user:
            return {"success": False, "message": "Пользователь не найден"}
        
        pref = UserPreference.query.filter_by(user_id=user_id).first()
        if not pref or not pref.vacancy_alerts_enabled:
            return {"success": False, "message": "Уведомления о вакансиях не включены"}
        
        try:
            import json
            preferred_professions = json.loads(pref.preferred_professions) if pref.preferred_professions else []
        except:
            preferred_professions = []
        
        if not preferred_professions:
            return {"success": False, "message": "Нет указанных профессий для отслеживания"}
        
        # Инициализируем API для работы с рынком труда
        job_market_api = JobMarketAPI()
        
        results = {}
        
        for profession in preferred_professions:
            try:
                vacancies = job_market_api.get_vacancies_by_profession(profession, limit=3)
                results[profession] = {
                    "count": len(vacancies),
                    "vacancies": vacancies
                }
                
                # Создаем уведомление если есть новые вакансии
                if vacancies:
                    title = f"Найдены вакансии по профессии '{profession}'"
                    message = f"По вашей интересующей профессии '{profession}' найдено {len(vacancies)} вакансий:"
                    
                    for i, vacancy in enumerate(vacancies[:3]):
                        company = vacancy.get('employer', 'Не указано')
                        salary = vacancy.get('salary', 'Не указана')
                        message += f"\n{i+1}. {vacancy.get('title', 'Не указано')} в {company}, з/п: {salary}"
                    
                    notification = Notification(
                        user_id=user.id,
                        title=title,
                        message=message,
                        type='info'
                    )
                    
                    db.session.add(notification)
                
            except Exception as e:
                results[profession] = {"error": str(e)}
        
        db.session.commit()
        
        return {"success": True, "results": results}


if __name__ == "__main__":
    # При прямом запуске файла
    scheduler_thread = start_scheduler()
    
    # Оставляем программу работающей
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nПланировщик остановлен")