import io
import csv
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required, current_user
from app import db
from app.models import User, TestResult, Notification
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import json

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
@login_required
def reports_index():
    """Страница с отчетами"""
    return jsonify({
        'success': True,
        'available_reports': [
            {'id': 'personal', 'name': 'Персональный отчет', 'description': 'Ваши личные результаты и прогресс'},
            {'id': 'comparative', 'name': 'Сравнительный отчет', 'description': 'Сравнение с другими пользователями'},
            {'id': 'trend_analysis', 'name': 'Анализ трендов', 'description': 'Изменения во времени'},
            {'id': 'market_insights', 'name': 'Инсайты рынка', 'description': 'Профессии и вакансии'},
            {'id': 'statistical_summary', 'name': 'Статистическая сводка', 'description': 'Общая статистика системы'}
        ]
    })

@reports_bp.route('/reports/generate', methods=['POST'])
@login_required
def generate_report():
    """Генерация отчета"""
    data = request.get_json()
    report_type = data.get('type', 'personal')
    format_type = data.get('format', 'pdf')  # pdf, csv, json
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    
    if report_type == 'personal':
        report_data = generate_personal_report(current_user.id, start_date, end_date)
    elif report_type == 'comparative':
        report_data = generate_comparative_report(current_user.id, start_date, end_date)
    elif report_type == 'trend_analysis':
        report_data = generate_trend_analysis_report(current_user.id, start_date, end_date)
    elif report_type == 'market_insights':
        report_data = generate_market_insights_report(current_user.id, start_date, end_date)
    elif report_type == 'statistical_summary':
        report_data = generate_statistical_summary_report(start_date, end_date)
    else:
        return jsonify({'error': 'Неизвестный тип отчета'}), 400
    
    if format_type == 'pdf':
        return generate_pdf_report(report_data, report_type)
    elif format_type == 'csv':
        return generate_csv_report(report_data, report_type)
    elif format_type == 'json':
        return jsonify({'success': True, 'data': report_data})
    else:
        return jsonify({'error': 'Неизвестный формат'}), 400

def generate_personal_report(user_id, start_date=None, end_date=None):
    """Генерация персонального отчета"""
    user = User.query.get(user_id)
    test_results = TestResult.query.filter_by(user_id=user_id)
    
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        test_results = test_results.filter(TestResult.created_at >= start_dt)
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        test_results = test_results.filter(TestResult.created_at <= end_dt)
    
    test_results = test_results.order_by(TestResult.created_at.desc()).all()
    
    report_data = {
        'user': {
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'is_admin': user.is_admin
        },
        'test_count': len(test_results),
        'tests': [],
        'methodology_stats': {'klimov': 0, 'holland': 0},
        'progress_summary': {}
    }
    
    for result in test_results:
        try:
            results_dict = json.loads(result.results) if result.results else {}
            test_info = {
                'id': result.id,
                'methodology': result.methodology,
                'created_at': result.created_at.isoformat(),
                'formatted_date': result.created_at.strftime('%d.%m.%Y'),
                'scores': results_dict.get('scores', {}),
                'dominant_category': results_dict.get('dominant_category', 'Не определено'),
                'recommendation': result.recommendation
            }
            report_data['tests'].append(test_info)
            report_data['methodology_stats'][result.methodology] += 1
        except:
            test_info = {
                'id': result.id,
                'methodology': result.methodology,
                'created_at': result.created_at.isoformat(),
                'formatted_date': result.created_at.strftime('%d.%m.%Y'),
                'scores': {},
                'dominant_category': 'Не определено',
                'recommendation': result.recommendation
            }
            report_data['tests'].append(test_info)
    
    # Calculate progress summary
    if report_data['tests']:
        latest_test = report_data['tests'][0]
        if len(report_data['tests']) > 1:
            prev_test = report_data['tests'][1]
            changes = calculate_changes(prev_test['scores'], latest_test['scores'])
            report_data['progress_summary'] = {
                'latest_test': latest_test,
                'previous_test': prev_test,
                'changes': changes
            }
        else:
            report_data['progress_summary'] = {
                'latest_test': latest_test,
                'previous_test': None,
                'changes': {}
            }
    
    return report_data

def generate_comparative_report(user_id, start_date=None, end_date=None):
    """Генерация сравнительного отчета"""
    user = User.query.get(user_id)
    all_users = User.query.count()
    all_results = TestResult.query
    
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        all_results = all_results.filter(TestResult.created_at >= start_dt)
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        all_results = all_results.filter(TestResult.created_at <= end_dt)
    
    all_results = all_results.all()
    
    user_results = TestResult.query.filter_by(user_id=user_id)
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        user_results = user_results.filter(TestResult.created_at >= start_dt)
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        user_results = user_results.filter(TestResult.created_at <= end_date)
    user_results = user_results.all()
    
    comparative_data = {
        'user_info': {
            'username': user.username,
            'test_count': len(user_results),
            'rank_percentile': calculate_percentile(len(user_results), [len(User.query.filter_by(id=u.id).first().test_results) for u in User.query.all()])
        },
        'system_stats': {
            'total_users': all_users,
            'total_tests': len(all_results),
            'avg_tests_per_user': len(all_results) / all_users if all_users > 0 else 0
        },
        'methodology_distribution': calculate_methodology_distribution(all_results)
    }
    
    return comparative_data

def generate_trend_analysis_report(user_id, start_date=None, end_date=None):
    """Генерация отчета по трендам"""
    # Если не указаны даты, берем последние 6 месяцев
    if not start_date:
        start_dt = datetime.now() - timedelta(days=180)
        start_date = start_dt.strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    
    # Получаем результаты за указанный период
    results = TestResult.query.filter(
        TestResult.created_at >= start_dt,
        TestResult.created_at <= end_dt
    ).order_by(TestResult.created_at).all()
    
    # Группируем по датам
    daily_stats = {}
    for result in results:
        date_key = result.created_at.strftime('%Y-%m-%d')
        if date_key not in daily_stats:
            daily_stats[date_key] = {'klimov': 0, 'holland': 0, 'total': 0}
        
        daily_stats[date_key][result.methodology] += 1
        daily_stats[date_key]['total'] += 1
    
    # Преобразуем в массив для графиков
    dates = sorted(daily_stats.keys())
    trend_data = {
        'dates': dates,
        'klimov_counts': [daily_stats[date]['klimov'] for date in dates],
        'holland_counts': [daily_stats[date]['holland'] for date in dates],
        'total_counts': [daily_stats[date]['total'] for date in dates]
    }
    
    # Вычисляем тренды
    if len(dates) > 1:
        first_period_avg = sum(trend_data['total_counts'][:len(trend_data['total_counts'])//2]) / (len(trend_data['total_counts'])//2)
        last_period_avg = sum(trend_data['total_counts'][len(trend_data['total_counts'])//2:]) / len(trend_data['total_counts'][len(trend_data['total_counts'])//2:])
        
        trend_direction = 'increasing' if last_period_avg > first_period_avg else 'decreasing' if last_period_avg < first_period_avg else 'stable'
        trend_percentage = ((last_period_avg - first_period_avg) / first_period_avg * 100) if first_period_avg > 0 else 0
    else:
        trend_direction = 'insufficient_data'
        trend_percentage = 0
    
    report_data = {
        'period': {'start': start_date, 'end': end_date},
        'trend_data': trend_data,
        'trend_analysis': {
            'direction': trend_direction,
            'percentage_change': trend_percentage,
            'total_tests': sum(trend_data['total_counts'])
        }
    }
    
    return report_data

def generate_market_insights_report(user_id, start_date=None, end_date=None):
    """Генерация отчета с инсайтами рынка труда"""
    # В реальной системе это бы интегрировалось с API рынка труда
    # Здесь мы создаем демонстрационные данные
    
    from app.job_market_api import job_market_api
    
    # Получаем последние результаты пользователя
    latest_result = TestResult.query.filter_by(user_id=user_id).order_by(
        TestResult.created_at.desc()
    ).first()
    
    if latest_result:
        try:
            results_dict = json.loads(latest_result.results)
            dominant_category = results_dict.get('dominant_category')
            
            if not dominant_category:
                top_categories = results_dict.get('top_categories', [])
                if top_categories:
                    dominant_category = top_categories[0][0]
        except:
            dominant_category = 'Программист'  # демо-категория
    
    else:
        dominant_category = 'Программист'  # демо-категория
    
    # Получаем информацию о профессии
    profession_info = job_market_api.get_profession_info(dominant_category)
    vacancies = job_market_api.get_vacancies_by_profession(dominant_category, limit=5)
    
    report_data = {
        'focus_profession': dominant_category,
        'profession_info': profession_info,
        'top_vacancies': vacancies[:3],
        'salary_insights': profession_info.get('salary_range', {}),
        'market_demand': 'high' if profession_info.get('demand') == 'high' else 'moderate'
    }
    
    return report_data

def generate_statistical_summary_report(start_date=None, end_date=None):
    """Генерация статистической сводки"""
    all_users = User.query
    all_results = TestResult.query
    
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        all_users = all_users.filter(User.created_at >= start_dt)
        all_results = all_results.filter(TestResult.created_at >= start_dt)
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        all_users = all_users.filter(User.created_at <= end_dt)
        all_results = all_results.filter(TestResult.created_at <= end_dt)
    
    user_count = all_users.count()
    result_count = all_results.count()
    
    # Статистика по методикам
    methodology_stats = {}
    for result in all_results:
        if result.methodology not in methodology_stats:
            methodology_stats[result.methodology] = 0
        methodology_stats[result.methodology] += 1
    
    # Среднее количество тестов на пользователя
    avg_tests_per_user = result_count / user_count if user_count > 0 else 0
    
    # Администраторы
    admin_count = User.query.filter_by(is_admin=True).count()
    
    # Уведомления
    notification_count = Notification.query.count()
    if start_date:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        notification_count = Notification.query.filter(Notification.created_at >= start_dt).count()
    if end_date:
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        notification_count = Notification.query.filter(Notification.created_at <= end_dt).count()
    
    report_data = {
        'period': {'start': start_date, 'end': end_date},
        'system_stats': {
            'total_users': user_count,
            'total_tests': result_count,
            'total_admins': admin_count,
            'total_notifications': notification_count,
            'avg_tests_per_user': round(avg_tests_per_user, 2)
        },
        'methodology_distribution': methodology_stats,
        'growth_metrics': calculate_growth_metrics(all_users, all_results)
    }
    
    return report_data

def calculate_changes(prev_scores, curr_scores):
    """Вычислить изменения между двумя наборами оценок"""
    changes = {}
    all_categories = set(prev_scores.keys()) | set(curr_scores.keys())
    
    for category in all_categories:
        prev_score = prev_scores.get(category, 0)
        curr_score = curr_scores.get(category, 0)
        change = curr_score - prev_score
        changes[category] = {
            'previous': prev_score,
            'current': curr_score,
            'change': change,
            'change_percent': (change / prev_score * 100) if prev_score != 0 else 0
        }
    
    return changes

def calculate_percentile(value, all_values):
    """Вычислить процентиль"""
    if not all_values:
        return 50  # средний
    
    sorted_values = sorted(all_values)
    rank = sum(1 for v in sorted_values if v < value)
    percentile = (rank / len(sorted_values)) * 100
    return round(percentile, 2)

def calculate_methodology_distribution(results):
    """Вычислить распределение по методикам"""
    distribution = {'klimov': 0, 'holland': 0}
    for result in results:
        distribution[result.methodology] += 1
    return distribution

def calculate_growth_metrics(users_query, results_query):
    """Вычислить метрики роста"""
    # За последние 30 дней
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    new_users_30d = users_query.filter(User.created_at >= thirty_days_ago).count()
    new_tests_30d = results_query.filter(TestResult.created_at >= thirty_days_ago).count()
    
    # За последние 7 дней
    seven_days_ago = datetime.now() - timedelta(days=7)
    new_users_7d = users_query.filter(User.created_at >= seven_days_ago).count()
    new_tests_7d = results_query.filter(TestResult.created_at >= seven_days_ago).count()
    
    return {
        'new_users_30d': new_users_30d,
        'new_tests_30d': new_tests_30d,
        'new_users_7d': new_users_7d,
        'new_tests_7d': new_tests_7d
    }

def generate_pdf_report(report_data, report_type):
    """Генерация PDF отчета"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Заголовок
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # center
    )
    
    title_map = {
        'personal': 'Персональный отчет пользователя',
        'comparative': 'Сравнительный отчет',
        'trend_analysis': 'Анализ трендов использования',
        'market_insights': 'Инсайты рынка труда',
        'statistical_summary': 'Статистическая сводка системы'
    }
    
    title = Paragraph(title_map.get(report_type, 'Отчет'), title_style)
    elements.append(title)
    
    # Добавляем контент в зависимости от типа отчета
    if report_type == 'personal':
        elements.extend(create_personal_report_content(report_data, styles))
    elif report_type == 'comparative':
        elements.extend(create_comparative_report_content(report_data, styles))
    elif report_type == 'trend_analysis':
        elements.extend(create_trend_report_content(report_data, styles))
    elif report_type == 'market_insights':
        elements.extend(create_market_report_content(report_data, styles))
    elif report_type == 'statistical_summary':
        elements.extend(create_statistical_report_content(report_data, styles))
    
    # Создаем документ
    doc.build(elements)
    buffer.seek(0)
    
    # Определяем имя файла
    filename_map = {
        'personal': 'personal_report',
        'comparative': 'comparative_report',
        'trend_analysis': 'trend_analysis_report',
        'market_insights': 'market_insights_report',
        'statistical_summary': 'statistical_summary_report'
    }
    
    filename = f"{filename_map.get(report_type, 'report')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

def create_personal_report_content(report_data, styles):
    """Создание контента для персонального отчета"""
    elements = []
    
    # Информация о пользователе
    user_info = [
        ['Имя пользователя', report_data['user']['username']],
        ['Email', report_data['user']['email']],
        ['Дата регистрации', report_data['user']['created_at']],
        ['Всего тестов', str(report_data['test_count'])],
        ['Тестов Климова', str(report_data['methodology_stats']['klimov'])],
        ['Тестов Холланда', str(report_data['methodology_stats']['holland'])]
    ]
    
    user_table = Table(user_info)
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Информация о пользователе", styles['Heading2']))
    elements.append(user_table)
    elements.append(Spacer(1, 20))
    
    # Результаты тестов
    if report_data['tests']:
        elements.append(Paragraph("Результаты тестов", styles['Heading2']))
        
        for test in report_data['tests']:
            test_info = [
                ['ID', 'Методика', 'Дата', 'Основная сфера', 'Рекомендация'],
                [str(test['id']), test['methodology'], test['formatted_date'], 
                 test['dominant_category'], test['recommendation'][:50] + '...' if len(test['recommendation']) > 50 else test['recommendation']]
            ]
            
            test_table = Table(test_info)
            test_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(test_table)
            elements.append(Spacer(1, 10))
    
    # Прогресс
    if report_data['progress_summary']:
        elements.append(Paragraph("Анализ прогресса", styles['Heading2']))
        progress = report_data['progress_summary']
        
        if progress['previous_test']:
            elements.append(Paragraph(f"Сравнение с предыдущим тестом от {progress['previous_test']['formatted_date']}", styles['Normal']))
            
            changes_data = [['Категория', 'Прошло', 'Сейчас', 'Изменение']]
            for cat, change_info in progress['changes'].items():
                changes_data.append([
                    cat,
                    str(change_info['previous']),
                    str(change_info['current']),
                    f"{change_info['change']} ({change_info['change_percent']:.1f}%)"
                ])
            
            changes_table = Table(changes_data)
            changes_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(changes_table)
        else:
            elements.append(Paragraph("Недостаточно данных для анализа прогресса", styles['Normal']))
    
    return elements

def create_comparative_report_content(report_data, styles):
    """Создание контента для сравнительного отчета"""
    elements = []
    
    # Пользовательская статистика
    user_stats = [
        ['Метрика', 'Значение'],
        ['Имя пользователя', report_data['user_info']['username']],
        ['Количество тестов', str(report_data['user_info']['test_count'])],
        ['Процентиль активности', f"{report_data['user_info']['rank_percentile']}%"]
    ]
    
    user_table = Table(user_stats)
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Статистика пользователя", styles['Heading2']))
    elements.append(user_table)
    elements.append(Spacer(1, 20))
    
    # Статистика системы
    system_stats = [
        ['Метрика', 'Значение'],
        ['Всего пользователей', str(report_data['system_stats']['total_users'])],
        ['Всего тестов', str(report_data['system_stats']['total_tests'])],
        ['Среднее тестов на пользователя', f"{report_data['system_stats']['avg_tests_per_user']:.2f}"]
    ]
    
    system_table = Table(system_stats)
    system_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Статистика системы", styles['Heading2']))
    elements.append(system_table)
    elements.append(Spacer(1, 20))
    
    # Распределение методик
    if report_data['methodology_distribution']:
        elements.append(Paragraph("Распределение по методикам", styles['Heading2']))
        dist_data = [['Методика', 'Количество', 'Процент']]
        total = sum(report_data['methodology_distribution'].values())
        
        for method, count in report_data['methodology_distribution'].items():
            percent = (count / total * 100) if total > 0 else 0
            dist_data.append([method, str(count), f"{percent:.1f}%"])
        
        dist_table = Table(dist_data)
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(dist_table)
    
    return elements

def create_trend_report_content(report_data, styles):
    """Создание контента для трендового отчета"""
    elements = []
    
    # Информация о периоде
    period_info = [
        ['Период', f"{report_data['period']['start']} - {report_data['period']['end']}"],
        ['Направление тренда', report_data['trend_analysis']['direction']],
        ['Изменение в процентах', f"{report_data['trend_analysis']['percentage_change']:.2f}%"],
        ['Всего тестов за период', str(report_data['trend_analysis']['total_tests'])]
    ]
    
    period_table = Table(period_info)
    period_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Анализ трендов", styles['Heading2']))
    elements.append(period_table)
    elements.append(Spacer(1, 20))
    
    # Данные по дням
    if report_data['trend_data']['dates']:
        elements.append(Paragraph("Детализация по дням", styles['Heading2']))
        
        # Создаем таблицу с ограниченным количеством строк для отображения
        trend_data = [['Дата', 'Климов', 'Холланд', 'Всего']]
        
        # Ограничиваем количество строк для лучшей читаемости
        dates = report_data['trend_data']['dates']
        klimov_counts = report_data['trend_data']['klimov_counts']
        holland_counts = report_data['trend_data']['holland_counts']
        total_counts = report_data['trend_data']['total_counts']
        
        # Показываем только каждую 5-ю дату для уменьшения объема
        step = max(1, len(dates) // 10)  # максимум 10 строк в таблице
        for i in range(0, len(dates), step):
            trend_data.append([
                dates[i],
                str(klimov_counts[i]),
                str(holland_counts[i]),
                str(total_counts[i])
            ])
        
        trend_table = Table(trend_data)
        trend_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8)
        ]))
        
        elements.append(trend_table)
    
    return elements

def create_market_report_content(report_data, styles):
    """Создание контента для отчета по рынку труда"""
    elements = []
    
    # Основная профессия
    elements.append(Paragraph(f"Фокусная профессия: {report_data['focus_profession']}", styles['Heading2']))
    
    # Информация о профессии
    if report_data['profession_info']:
        info = report_data['profession_info']
        info_table_data = [
            ['Параметр', 'Значение'],
            ['Описание', info.get('description', 'Не указано')],
            ['Навыки', ', '.join(info.get('skills', [])[:3]) if info.get('skills') else 'Не указаны']
        ]
        
        if info.get('salary_range'):
            salary_range = info['salary_range']
            info_table_data.append(['Минимальная зарплата', f"{salary_range.get('min', 0):,}".replace(',', ' ')])
            info_table_data.append(['Средняя зарплата', f"{salary_range.get('average', 0):,}".replace(',', ' ')])
            info_table_data.append(['Максимальная зарплата', f"{salary_range.get('max', 0):,}".replace(',', ' ')])
        
        info_table = Table(info_table_data)
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('WORDWRAP', (1, 1), (-1, -1), 'LTR')
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 20))
    
    # Топ вакансий
    if report_data['top_vacancies']:
        elements.append(Paragraph("Топ актуальных вакансий", styles['Heading2']))
        
        for i, vacancy in enumerate(report_data['top_vacancies'], 1):
            vacancy_info = [
                ['Позиция', str(i)],
                ['Название', vacancy.get('title', 'Не указано')],
                ['Компания', vacancy.get('employer', 'Не указана')],
                ['Зарплата', vacancy.get('salary', 'Не указана')],
                ['Опыт', vacancy.get('experience', 'Не указан')]
            ]
            
            vacancy_table = Table(vacancy_info)
            vacancy_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightyellow),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(vacancy_table)
            elements.append(Spacer(1, 10))
    
    # Рыночный спрос
    demand_map = {
        'high': 'Высокий',
        'moderate': 'Умеренный',
        'low': 'Низкий',
        'unknown': 'Неизвестный'
    }
    
    elements.append(Paragraph(f"Уровень рыночного спроса: {demand_map.get(report_data['market_demand'], 'Неизвестный')}", styles['Normal']))
    
    return elements

def create_statistical_report_content(report_data, styles):
    """Создание контента для статистического отчета"""
    elements = []
    
    # Период отчета
    period_info = [
        ['Период', f"{report_data['period']['start'] or 'Начало'} - {report_data['period']['end'] or 'Текущий'}"]
    ]
    
    period_table = Table(period_info)
    period_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Период отчета", styles['Heading2']))
    elements.append(period_table)
    elements.append(Spacer(1, 20))
    
    # Системная статистика
    sys_stats = [
        ['Метрика', 'Значение'],
        ['Всего пользователей', str(report_data['system_stats']['total_users'])],
        ['Всего тестов', str(report_data['system_stats']['total_tests'])],
        ['Администраторов', str(report_data['system_stats']['total_admins'])],
        ['Уведомлений', str(report_data['system_stats']['total_notifications'])],
        ['Среднее тестов на пользователя', f"{report_data['system_stats']['avg_tests_per_user']:.2f}"]
    ]
    
    sys_table = Table(sys_stats)
    sys_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Системная статистика", styles['Heading2']))
    elements.append(sys_table)
    elements.append(Spacer(1, 20))
    
    # Распределение методик
    if report_data['methodology_distribution']:
        elements.append(Paragraph("Распределение по методикам", styles['Heading2']))
        dist_data = [['Методика', 'Количество', 'Процент']]
        total = sum(report_data['methodology_distribution'].values())
        
        for method, count in report_data['methodology_distribution'].items():
            percent = (count / total * 100) if total > 0 else 0
            dist_data.append([method, str(count), f"{percent:.1f}%"])
        
        dist_table = Table(dist_data)
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(dist_table)
        elements.append(Spacer(1, 20))
    
    # Метрики роста
    growth = report_data['growth_metrics']
    growth_data = [
        ['Метрика', 'За 30 дней', 'За 7 дней'],
        ['Новые пользователи', str(growth['new_users_30d']), str(growth['new_users_7d'])],
        ['Новые тесты', str(growth['new_tests_30d']), str(growth['new_tests_7d'])]
    ]
    
    growth_table = Table(growth_data)
    growth_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightcoral),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(Paragraph("Метрики роста", styles['Heading2']))
    elements.append(growth_table)
    
    return elements

def generate_csv_report(report_data, report_type):
    """Генерация CSV отчета"""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    
    if report_type == 'personal':
        # Заголовки
        writer.writerow(['ID теста', 'Методика', 'Дата', 'Основная сфера', 'Рекомендация'])
        
        # Данные
        for test in report_data['tests']:
            writer.writerow([
                test['id'],
                test['methodology'],
                test['formatted_date'],
                test['dominant_category'],
                test['recommendation']
            ])
    
    elif report_type == 'statistical_summary':
        # Заголовки
        writer.writerow(['Метрика', 'Значение'])
        
        # Системная статистика
        for key, value in report_data['system_stats'].items():
            writer.writerow([key, str(value)])
        
        # Распределение методик
        writer.writerow(['', ''])  # Пустая строка
        writer.writerow(['Распределение методик', ''])
        for method, count in report_data['methodology_distribution'].items():
            writer.writerow([method, count])
    
    else:
        # Для других типов отчетов просто выводим основные данные
        writer.writerow(['Тип отчета', report_type])
        writer.writerow(['Сгенерировано', datetime.now().isoformat()])
        writer.writerow(['Данные', str(len(str(report_data)))])  # Просто размер данных
    
    buffer.seek(0)
    
    # Создаем байтовый поток из строкового
    byte_buffer = io.BytesIO()
    byte_buffer.write(buffer.getvalue().encode('utf-8'))
    byte_buffer.seek(0)
    
    filename_map = {
        'personal': 'personal_report',
        'comparative': 'comparative_report',
        'trend_analysis': 'trend_analysis_report',
        'market_insights': 'market_insights_report',
        'statistical_summary': 'statistical_summary_report'
    }
    
    filename = f"{filename_map.get(report_type, 'report')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return send_file(
        byte_buffer,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )